import unittest
from unittest.mock import MagicMock, patch

import requests
import time
import errno

from datetime import datetime

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, RESPONSES


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

    def test_202(self):
        self._response.status_code = RESPONSES['FETCHING_DATA'].status_code
        self._response.headers['iRobot-ETA'] = "2017-09-25T12:34:56Z+00:00 +/- 123"

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(self._test_requester._request_delay,
                             int((datetime(2017, 9, 25, 12, 34, 56) - datetime.now()).total_seconds()))

    def test_404(self):
        self._response.status_code = RESPONSES['NOT_FOUND'].status_code

        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['NOT_FOUND'].errno}",
                               self._test_requester.get_data)


if __name__ == '__main__':
    unittest.main()