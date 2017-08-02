import unittest
from unittest.mock import MagicMock, patch

import requests
import time

from datetime import datetime

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, RESPONSES


class TestResponses(unittest.TestCase):
    def setUp(self):
        self._old_request_head = requests.head
        self._old_request_get = requests.get
        self._response = requests.Response()
        requests.head = MagicMock(spec=requests.head)
        requests.get = MagicMock(spec=requests.get)

    def tearDown(self):
        requests.head = self._old_request_head
        requests.get = self._old_request_get

    def test_202_response(self):
        self._response.status_code = RESPONSES['FETCHING_DATA'].status_code
        self._response.headers['iRobot-ETA'] = "2017-09-25T12:34:56Z+00:00 +/- 123"
        requests.head.return_value = self._response

        old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

        old_datetime_now = datetime.now
        datetime.now = MagicMock(spec=datetime.now)
        datetime.now.return_Value = datetime(2017, 9, 25, 12, 30, 56) # 240 second until iRobot-ETA

        test_requester = Requester("testURL", {"testKey": "testValue"})
        try:
            test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(test_requester._request_delay, 240)

        time.sleep = old_time_sleep
        datetime.now = old_datetime_now

    def test_404_response(self):
        self._response.status_code = RESPONSES['NOT_FOUND'].status_code
        requests.head.return_value = self._response

        test_requester = Requester("testURL", {"testKey": "testValue"})
        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['NOT_FOUND'].errno}", test_requester.get_data)




if __name__ == '__main__':
    unittest.main()