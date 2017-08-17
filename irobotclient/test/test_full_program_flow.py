import unittest
from unittest.mock import MagicMock

import argparse
import os
import time
import requests

from collections import namedtuple

import irobotclient.main

TestDataStruct = namedtuple("TestDataStruct", "full_input_url, full_output_url")


class TestFullProgramFlow(unittest.TestCase):
    """
    Testing the entire program flow.  Checking that the program input generates the expected program output.
    """
    def setUp(self):

        # The test data/directory, all part of the irobot repository so it should work when pulled to other locations.
        self._input_file_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata/')
        self._output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testdir/')

        # Mocking requests.head() to return a default custom response without the need for middleware/server.
        self._old_request_head = requests.head
        requests.head = MagicMock(spec=requests.head)
        self._response_head = requests.Response()
        requests.head.return_value = self._response_head

        # Mocking requests.get() to return a response with a body.
        self._old_request_get = requests.get
        requests.get = MagicMock(spec=requests.get)
        self._response_get = requests.Response()
        requests.get.return_value = self._response_get

        # Mocking time.sleep() so the wait response processes instantly.
        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)

        time.sleep.return_value = None

    def tearDown(self):
        requests.head = self._old_request_head
        requests.get = self._old_request_get
        time.sleep = self._old_time_sleep

    def _append_filename_to_urls(self, filename:str) -> TestDataStruct:

        return TestDataStruct(full_input_url=self._input_file_dir + filename,
                              full_output_url=self._output_dir + filename)

    def _set_response_get_content(self, file_url:str):

        with open(file_url, "rb") as file:
            self._response_get._content = file.read()

    @unittest.skip("test_pipeline_for_cram_and_index is a work in progress")
    def test_pipeline_for_cram_and_index(self):
        test_file = "test.cram"
        test_data = self._append_filename_to_urls(test_file)

        self._test_arg_parser.input_file = test_data.full_input_url
        self._response_head.status_code = 200
        self._response_get.status_code = 200
        self._response_get.url = test_data.full_input_url

        # TODO - Figure out side effects
        # requests.get.side_effect = [
        #     self._set_response_get_content(test_data.full_input_url),
        #     self._set_response_get_content(self._input_file_dir + "test.crai")
        # ]

        requests.head.return_value = self._response_head
        requests.get.return_value =self._response_get

        irobotclient.main._run()

        self.assertTrue(os.path.exists(test_data.full_input_url) and
                        os.path.exists(self._input_file_dir + "test.crai"))

        self.assertTrue(os.path.getsize(test_data.full_input_url) ==
                        os.path.getsize(test_data.full_output_url))


    @unittest.skip("test_pipeline_for_bam_wait_and_no_index - to be implemented")
    def test_pipeline_for_bam_wait_and_no_index(self):
        # Request bam file without index
        # Simulate wait response followed by 200 response
        # Download both bam file
        # Check it worked
        pass

    @unittest.skip("test_pipeline_for_bam_and_alternative_index - to be implemented")
    def test_pipeline_for_bam_alternative_index(self):
        # Request bam file from testdata directory
        # Download both bam and pbi while outputing bai cannot be found
        # Check it worked
        pass


if __name__ == '__main__':
    unittest.main()
