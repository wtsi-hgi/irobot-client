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
        self._session_send = requests.Session.send
        self._response = requests.Response()
        requests.Session.send = MagicMock(spec=requests.Session.send)
        self._response.headers['WWW-Authenticate'] = "Arvados, Basic"
        requests.Session.send.return_value = self._response
        self._test_requester = Requester("http://testURL", {"testKey": "testValue"})

        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

    def tearDown(self):
        requests.Session.send = self._session_send
        time.sleep = self._old_time_sleep

    def test_202_with_eta_header(self):
        future_time = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        self._response.headers['iRobot-ETA'] = future_time.strftime("%Y-%m-%dT%H:%M:%SZ+0000 +/- 123")

        try:
            self._test_requester.get_data("test/file/path")
        except IrobotClientException:
            self.assertEqual(response_handler.get_request_delay(self._response),
                             int((future_time - datetime.now(tz=timezone.utc)).total_seconds()))

    def test_202_without_eta_header(self):
        try:
            self._test_requester.get_data("test/file/path")
        except IrobotClientException:
            self.assertEqual(response_handler.get_request_delay(self._response),
                             response_handler._get_default_request_delay())


if __name__ == '__main__':
    unittest.main()
