import unittest
import os
import tempfile
import subprocess

import sys
from useintest.predefined.bissell.bissell import BissellServiceController

BISSELL_TOKEN = "testtoken"
BISSELL_USER = "testuser"
BISSELL_PASSWORD = "testpass"
BISSELL_CRAM = "test.cram"
BISSELL_CRAI = "test.crai"

try:
    import coverage
    _PYTHON_EXECUTOR = [sys.executable, "-m", "coverage", "run"]
except ImportError:
    _PYTHON_EXECUTOR = [sys.executable]


class TestFullProgramFlow(unittest.TestCase):
    """
    Testing the entire program flow.  Checking that the program input generates the expected program output.
    These test should cover much of the code in the entrypoint.py file.  The code is run against a pseudo-irobot
    web server called 'bissell'.

    """
    def setUp(self):
        # Spin up bissell container
        self._bissell_controller = BissellServiceController()
        self._bissell_service = self._bissell_controller.start_service()
        self._bissell_url = f"http://{self._bissell_service.host}:{self._bissell_service.port}"

        # Create a temporary output directory
        self._temp_directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Destroy bissell container
        self._bissell_controller.stop_service(self._bissell_service)

        # Destroy temporary test directory
        self._temp_directory.cleanup()

    def test_cli(self):
        """
        Test the command line interface against the bissell service.

        :return:
        """
        environment = os.environ.copy()
        if not os.getenv("PYTHONPATH"):
            environment["PYTHONPATH"] = f"{os.path.dirname(os.path.realpath(__file__))}/../../"
        subprocess.run(_PYTHON_EXECUTOR + [
            f"{os.path.dirname(os.path.realpath(__file__))}/../entrypoint.py",  # Call the program from the test directory
            f"{BISSELL_CRAM}",                           # Input file
            f"{self._temp_directory.name}",              # Output directory
            f"-u", f"{self._bissell_url}",               # URL for bissell
            f"--arvados_token", f"{BISSELL_TOKEN}",      # Bissel authentication token
            f"--basic_username", f"{BISSELL_USER}",      # Bissell basic username
            f"--basic_password", f"{BISSELL_PASSWORD}",  # Bissell basic password
            f"-f"], env=environment)

        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAM}"))
        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAI}"))

    # TODO - Test CWL with cwl-runner against bissell.


if __name__ == '__main__':
    unittest.main()
