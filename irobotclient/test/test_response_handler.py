import unittest
import time

from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock

import requests

from irobotclient import response_handler
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes


class TestResponseHandler(unittest.TestCase):
    """

    """
    def setUp(self):
        self._old_request_head = requests.get
        self._response = requests.Response()
        requests.get = MagicMock(spec=requests.get)
        self._response.headers['WWW-Authenticate'] = "Arvados, Basic"
        requests.get.return_value = self._response
        self._test_requester = Requester("testURL", {"testKey": "testValue"})

        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

    def tearDown(self):
        requests.get = self._old_request_head
        time.sleep = self._old_time_sleep

    def test_202_with_eta_header(self):
        future_time = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        self._response.headers['iRobot-ETA'] = future_time.strftime("%Y-%m-%dT%H:%M:%SZ+0000 +/- 123")

        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(response_handler.get_request_delay(self._response),
                             int((future_time - datetime.now(tz=timezone.utc)).total_seconds()))

    def test_202_without_eta_header(self):
        try:
            self._test_requester.get_data()
        except IrobotClientException:
            self.assertEqual(response_handler.get_request_delay(self._response),
                             response_handler._get_default_request_delay())


if __name__ == '__main__':
    unittest.main()
