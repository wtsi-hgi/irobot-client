import unittest
from unittest.mock import MagicMock

import argparse
import os
import time

import irobotclient.main

"""
Likely need to mock request, response, time.sleep.
"""


class TestPipeline(unittest.TestCase):

    input_file_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testdata/')
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'testdir/')

    def setUp(self):
        self._old_parse_args = argparse.ArgumentParser.parse_args
        argparse.ArgumentParser.parse_args = MagicMock(spec=argparse.ArgumentParser.parse_args)
        self._test_arg_parser = argparse.Namespace(input_file=self.input_file_dir,
                                                   output_dir=self.output_dir,
                                                   url="",
                                                   token="abc123",
                                                   force=True,
                                                   no_index=False)

        argparse.ArgumentParser.parse_args.return_value = self._test_arg_parser

        # TODO - Implement response mock

        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

    def tearDown(self):
        argparse.ArgumentParser.parse_args = self._old_parse_args
        time.sleep = self._old_time_sleep

    @unittest.skip("test_pipeline_for_cram_and_index - to be implemented")
    def test_pipeline_for_cram_and_index(self):
        test_file = "test.cram"

        self._test_arg_parser.input_file = self._test_arg_parser.input_file + test_file

        irobotclient.main._run()

        self.assertTrue(os.path.exists(self.input_file_dir + test_file) and
                        os.path.exists(self.input_file_dir + test_file))

        self.assertTrue(os.path.getsize(self.input_file_dir + test_file) ==
                        os.path.getsize(self.output_dir + test_file))


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
