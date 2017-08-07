import unittest
from unittest.mock import MagicMock, patch

import requests
import time
import errno
import argparse
import os

from datetime import datetime, timedelta

from irobotclient import configuration_handler
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, RESPONSES, DEFAULT_REQUEST_DELAY


class TestConfigurationSetup(unittest.TestCase):

    def setUp(self):
        self._parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        self._parser.add_argument("input_file", default="input")
        self._parser.add_argument("output_dir", default="output")
        self._parser.add_argument("-u", "--url")
        self._parser.add_argument("-t", "--token")
        self._parser.add_argument("-f", "--force", default=False, action="store_true")
        self._parser.add_argument("--no-index", default=False, action="store_true")

    def test_input_file_slash_removal(self):
        args = self._parser.parse_args(["/some/place/on/irods/input.cram", None])
        configuration_handler._check_input_file_argument(args)
        self.assertFalse(args.input_file.startswith('/'))

    def test_output_directory_formatting(self):
        old_listdir = os.listdir
        os.listdir = MagicMock(spec=os.listdir)
        os.listdir.return_value = []

        args = self._parser.parse_args(["", "~/some/output/dir"])
        configuration_handler._check_output_directory_argument(args)
        self.assertTrue(os.path.isabs(args.output_dir))
        self.assertTrue(args.output_dir.endswith('/'))

        os.listdir = old_listdir

    def test_output_directory_not_exist(self):
        args = self._parser.parse_args(["", "~/some/output/dir"])
        configuration_handler._check_output_directory_argument(args)
        self.assertRaisesRegex(OSError, "directory")

    # Beth - This test fails but it raises the exception I am expecting.
    def test_file_exist_in_output_dir_with_extension_and_no_overwrite(self):
        old_listdir = os.listdir
        os.listdir = MagicMock(spec=os.listdir)
        os.listdir.return_value = {"hello", "test", "file", "one"}

        args = self._parser.parse_args(["file.cram", "~/some/output/dir"])
        configuration_handler._check_output_directory_argument(args)
        self.assertRaisesRegex(IrobotClientException, f"{errno.EEXIST}")

        os.listdir = old_listdir

class TestResponses(unittest.TestCase):
    def setUp(self):
        self._old_request_head = requests.head
        self._response = requests.Response()
        requests.head = MagicMock(spec=requests.head)
        requests.head.return_value = self._response
        self._test_requester = Requester("testURL", {"testKey": "testValue"})

        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

    def tearDown(self):
        requests.head = self._old_request_head
        time.sleep = self._old_time_sleep

    def test_response_loop(self):
        self._response.status_code = RESPONSES['FETCHING_DATA'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{errno.ECONNABORTED}",
                               self._test_requester.get_data)

    def test_200(self):
        old_requests_get = requests.get
        requests.get = MagicMock(spec=requests.get)
        requests.get.return_value = 123

        self._response.status_code = RESPONSES['SUCCESS'].status_code
        self.assertEqual(self._test_requester.get_data(), 123)

        requests.get = old_requests_get

    def test_202_with_eta_header(self):
        self._response.status_code = RESPONSES['FETCHING_DATA'].status_code
        future_time = datetime.now() + timedelta(minutes=5)
        self._response.headers['iRobot-ETA'] = future_time.strftime("%Y-%m-%dT%H:%M:%SZ+00:00 +/- 123")

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(self._test_requester._request_delay,
                             int((future_time - datetime.now()).total_seconds()))

    def test_202_without_eta_header(self):
        self._response.status_code = RESPONSES['FETCHING_DATA'].status_code

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(self._test_requester._request_delay, DEFAULT_REQUEST_DELAY)

    @unittest.skip("206 to be implemented")
    def test_206(self):
        self._response.status_code = RESPONSES['RANGED_DATA'].status_code
        # TODO - Implement

    @unittest.skip("304 to be implemented")
    def test_304(self):
        self._response.status_code = RESPONSES['CLIENT_MATCHED'].status_code
        # TODO - Implement

    @unittest.skip("401 fail to be implemented")
    def test_401_fail(self):
        self._response.status_code = RESPONSES['AUTH_FAIL'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['AUTH_FAIL'].errno}",
                               self._test_requester.get_data)

    @unittest.skip("401 to be implemented")
    def test_401(self):
        self._response.status_code = RESPONSES['AUTH_FAIL'].status_code

    def test_403(self):
        self._response.status_code = RESPONSES['DENIED_IRODS'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['DENIED_IRODS'].errno}",
                               self._test_requester.get_data)

    def test_404(self):
        self._response.status_code = RESPONSES['NOT_FOUND'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['NOT_FOUND'].errno}",
                               self._test_requester.get_data)

    def test_405(self):
        self._response.status_code = RESPONSES['INVALID_REQUEST_METHOD'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['INVALID_REQUEST_METHOD'].errno}",
                               self._test_requester.get_data)

    def test_406(self):
        self._response.status_code = RESPONSES['INVALID_MEDIA_REQUESTED'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['INVALID_MEDIA_REQUESTED'].errno}",
                               self._test_requester.get_data)

    def test_416(self):
        self._response.status_code = RESPONSES['INVALID_RANGE'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['INVALID_RANGE'].errno}",
                               self._test_requester.get_data)

    def test_504(self):
        self._response.status_code = RESPONSES['TIMEOUT'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['TIMEOUT'].errno}",
                               self._test_requester.get_data)

    def test_507(self):
        self._response.status_code = RESPONSES['PRECACHE_FULL'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['PRECACHE_FULL'].errno}",
                               self._test_requester.get_data)

class TestDataDownload(unittest.TestCase):
    pass
    # TODO - Implement test for successful data download.


if __name__ == '__main__':
    unittest.main()