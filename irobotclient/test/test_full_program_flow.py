import unittest
import os
import subprocess
from useintest.predefined.bissell.bissell import BissellServiceController

BISSELL_TOKEN = "testtoken"
BISSELL_USER = "testuser"
BISSELL_PASSWORD = "testpass"
BISSELL_CRAM = "test.cram"
BISSELL_CRAI = "test.crai"


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
        self._temp_directory = "temp_output_dir"
        i = 0
        while os.path.exists(self._temp_directory):
            self._temp_directory = f"{self._temp_directory}{i}"
            i += 1
        os.makedirs(self._temp_directory)

    def tearDown(self):
        # Destroy bissell container
        self._bissell_controller.stop_service(self._bissell_service)

        # Destroy temporary test directory
        os.removedirs(self._temp_directory)
        return

    def test_cli(self):
        """
        Test the command line interface against the bissell service.

        :return:
        """
        subprocess.run([f"../entrypoint.py",                    # Call the program from the test directory
                       f"{BISSELL_CRAM}",                       # Input file
                       f"{self._temp_directory}",               # Output directory
                       f"-u {self._bissell_url}",               # URL for bissell
                       f"--arvados_token {BISSELL_TOKEN}",      # Bissel authentication token
                       f"--basic_username {BISSELL_USER}",      # Bissell basic username
                       f"--basic_password {BISSELL_PASSWORD}",  # Bissell basic password
                       f"-f"])

        self.assertEqual(os.path.exists(f"{self._temp_directory}/{BISSELL_CRAM}"), True)
        self.assertEqual(os.path.exists(f"{self._temp_directory}/{BISSELL_CRAI}"), True)


    # Test CWL with cwl-runner against bissell.


if __name__ == '__main__':
    unittest.main()
