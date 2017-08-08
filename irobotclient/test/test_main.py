import unittest
from unittest.mock import MagicMock

import requests
import time
import os

import irobotclient.main


class test_main(unittest.TestCase):

    test_file = os.path.join(os.path.dirname(__file__), '..', '..',  'testdata/test.cram')
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testdir/')

    def setUp(self):
        self._old_request_head = requests.head
        self._response = requests.Response()
        requests.head = MagicMock(spec=requests.head)
        requests.head.return_value = self._response

    def tearDown(self):
        requests.head = self._old_request_head

    def test_download(self):
        self._response.status_code = 200
        self._response.url = self.test_file

        with open(self.test_file, "rb") as file:
            self._response._content = file.read()

        print(self._response.content) # Beth - debug
        irobotclient.main._download_data(response=self._response, output_dir=self.output_dir)

        self.assertTrue(os.path.getsize(f"{self.output_dir}test.cram") == os.path.getsize(self.test_file))


if __name__ == '__main__':
    unittest.main()
