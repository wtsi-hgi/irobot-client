import unittest
from unittest.mock import MagicMock

import requests
import time
import errno
import re

from datetime import datetime,timedelta, timezone

from irobotclient import configuration_handler
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes, error_table


class TestRequester(unittest.TestCase):
    """
    This test case assesses the functions of the request_handler.py code such as how various responses are
    dealt with and if the delay for the next request (if appropriate) is set correctly.
    """
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
        self._response.status_code = ResponseCodes.FETCHING_DATA

        self.assertRaisesRegex(IrobotClientException, f"{errno.ECONNABORTED}",
                               self._test_requester.get_data)

    def test_200(self):
        old_requests_get = requests.get
        requests.get = MagicMock(spec=requests.get)
        requests.get.return_value = 123

        self._response.status_code = ResponseCodes.SUCCESS
        self.assertEqual(self._test_requester.get_data(), 123)

        requests.get = old_requests_get

    def test_202_with_eta_header(self):
        self._response.status_code = ResponseCodes.FETCHING_DATA
        future_time = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        self._response.headers['iRobot-ETA'] = future_time.strftime("%Y-%m-%dT%H:%M:%SZ+0000 +/- 123")

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(self._test_requester._request_delay,
                             int((future_time - datetime.now(tz=timezone.utc)).total_seconds()))

    def test_202_without_eta_header(self):
        self._response.status_code = ResponseCodes.FETCHING_DATA

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(self._test_requester._request_delay, configuration_handler.get_default_request_delay())

    @unittest.skip("206 to be implemented")
    def test_206(self):
        self._response.status_code = ResponseCodes.RANGED_DATA
        # TODO - Implement

    @unittest.skip("304 to be implemented")
    def test_304(self):
        self._response.status_code = ResponseCodes.CLIENT_MATCHED
        # TODO - Implement

    def test_error_responses(self):
        for code in error_table.keys():
            self._response.status_code = code

            self.assertRaisesRegex(IrobotClientException, str(error_table[code][0]), self._test_requester.get_data)
            self.assertRaisesRegex(IrobotClientException, error_table[code][1], self._test_requester.get_data)


if __name__ == '__main__':
    unittest.main()