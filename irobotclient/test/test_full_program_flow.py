import unittest
import os
import tempfile
import subprocess
import yaml
import socket

import sys
from useintest.predefined.bissell.bissell import BissellServiceController

from irobotclient.custom_exceptions import IrobotClientException

PROGRAM_ENTRYPOINT = f"{os.path.dirname(os.path.realpath(__file__))}/../entrypoint.py"
BISSELL_TOKEN = "testtoken"
BISSELL_USER = "testuser"
BISSELL_PASSWORD = "testpass"
BISSELL_CRAM = "test.cram"
BISSELL_CRAI = "test.crai"

CWL_WRAPPER = f"{os.path.dirname(os.path.realpath(__file__))}/../../cwl/cwl_wrapper.cwl"

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
    @classmethod
    def setUpClass(cls):
        # Get the IP address of the machine the tests and docker are running on.
        # For origin of solution see: https://stackoverflow.com/a/166589
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip_address = s.getsockname()[0]
        s.close()

        # Spin up bissell container
        cls._bissell_controller = BissellServiceController()
        cls._bissell_service = cls._bissell_controller.start_service()
        cls._bissell_url = f"http://{ip_address}:{cls._bissell_service.port}"

    @classmethod
    def tearDownClass(cls):
        # Destroy bissell container
        cls._bissell_controller.stop_service(cls._bissell_service)

    def setUp(self):
        # Create a temporary output directory
        self._temp_directory = tempfile.TemporaryDirectory()

        # Set the test environment
        self._environment = os.environ.copy()
        if not os.getenv("PYTHONPATH"):
            self._environment["PYTHONPATH"] = f"{os.path.dirname(os.path.realpath(__file__))}/../../"

    def tearDown(self):
        # Destroy temporary test directory
        self._temp_directory.cleanup()

    def test_cli(self):
        """
        Test the command line interface against the bissell service.

        :return:
        """

        subprocess.run(_PYTHON_EXECUTOR + [
            PROGRAM_ENTRYPOINT,                          # Call the program from the test directory
            f"{BISSELL_CRAM}",                           # Input file
            f"{self._temp_directory.name}",              # Output directory
            f"-u", f"{self._bissell_url}",               # URL for bissell
            f"--arvados_token", f"{BISSELL_TOKEN}",      # Bissel authentication token
            f"--basic_username", f"{BISSELL_USER}",      # Bissell basic username
            f"--basic_password", f"{BISSELL_PASSWORD}",  # Bissell basic password
            f"-f"], env=self._environment)

        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAM}"))
        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAI}"))

    def test_cwl(self):
        """
        Test the Common Workflow Language interface against the cwl-runner and a yaml object.

        :return:
        """
        yaml_file_path = f"{self._temp_directory.name}/test.yml"

        with open(yaml_file_path, 'w') as yml:
            yaml.dump({
                "input_file": BISSELL_CRAM,
                "irobot_url": self._bissell_url,
                "arvados_token": BISSELL_TOKEN,
                "basic_username": BISSELL_USER,
                "basic_password": BISSELL_PASSWORD,
                "force": True,
                "no_index": False
            },yml)

        subprocess.run(["cwl-runner", "--outdir", f"{self._temp_directory.name}", CWL_WRAPPER, yaml_file_path])

        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAM}"))
        self.assertTrue(os.path.exists(f"{self._temp_directory.name}/{BISSELL_CRAI}"))

    # The following tests evaluate exception handling
    def test_authentication_fail(self):
        """
        This test should result in an authentication exception being raised.

        :return:
        """
        subprocess.run(_PYTHON_EXECUTOR + [
            PROGRAM_ENTRYPOINT,                          # Call the program from the test directory
            f"{BISSELL_CRAM}",                           # Input file
            f"{self._temp_directory.name}",              # Output directory
            f"-u", f"{self._bissell_url}",               # URL for bissell
            f"--arvados_token", f"invalid_token",        # Not a valid credential
            f"--basic_username", f"invalid_username",    # Not a valid credential
            f"--basic_password", f"invalid_password",    # Not a valid credential
            f"-f"], env=self._environment)

        self.assertRaisesRegex(IrobotClientException, "401")  # 401 == Authentication failed response code.


if __name__ == '__main__':
    unittest.main()
