import unittest
from unittest.mock import MagicMock

import requests
import os

import irobotclient.main


class TestMain(unittest.TestCase):
    """
    Test case for the main.py module.
    """
    test_data_dir = os.path.join(os.path.dirname(__file__), 'resources/testdata/')
    output_dir = os.path.join(os.path.dirname(__file__), 'resources/testdir/')

    def setUp(self):
        self._old_request_head = requests.head
        self._response = requests.Response()
        requests.head = MagicMock(spec=requests.head)
        requests.head.return_value = self._response

    def tearDown(self):
        requests.head = self._old_request_head

    @unittest.skip("test_download_binary - need to figure out how to mark the response as stream=True")
    def test_download_binary(self):
        test_file = "test.cram"
        self._response.status_code = 200
        self._response.url = self.test_data_dir + test_file

        with open(self.test_data_dir + test_file, "rb") as file:
            self._response._content = file.read()

        irobotclient.main._download_data(response=self._response, save_location=self.output_dir)

        self.assertTrue(os.path.getsize(f"{self.output_dir}{test_file}") ==
                        os.path.getsize(self.test_data_dir + test_file))

    @unittest.skip("test_download_text - need to figure out how to mark the response as stream=True")
    def test_download_text(self):
        test_file = "test.txt"
        self._response.status_code = 200
        self._response.url = self.test_data_dir + test_file

        with open(self.test_data_dir + test_file, "r") as file:
            self._response._content = file.read()

        irobotclient.main._download_data(response=self._response, save_location=self.output_dir)

        self.assertTrue(os.path.getsize(f"{self.output_dir}{test_file}") ==
                        os.path.getsize(self.test_data_dir + test_file))


if __name__ == '__main__':
    unittest.main()
