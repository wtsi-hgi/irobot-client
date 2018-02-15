import unittest
from unittest.mock import MagicMock

import requests
import time
import errno
import json

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes


class TestRequester(unittest.TestCase):
    """
    This test case assesses the functions of the request_handler.py code such as how various responses are
    dealt with and if the delay for the next request (if appropriate) is set correctly.
    """
    def setUp(self):
        self._session_send = requests.Session.send
        self._response = requests.Response()
        requests.Session.send = MagicMock(spec=requests.Session.send)
        self._response.headers['WWW-Authenticate'] = "Arvados, Basic"
        requests.Session.send.return_value = self._response
        self._test_requester = Requester({"testKey": "testValue"}, "http://testURL")

        self._old_time_sleep = time.sleep
        time.sleep = MagicMock(spec=time.sleep)
        time.sleep.return_value = None

    def tearDown(self):
        requests.Session.send = self._session_send
        time.sleep = self._old_time_sleep

    # Tests for future functionality
    @unittest.skip("206 to be implemented")
    def test_206(self):
        self._response.status_code = ResponseCodes['RANGED_DATA']
        # TODO - Implement

    @unittest.skip("304 to be implemented")
    def test_304(self):
        self._response.status_code = ResponseCodes['CLIENT_MATCHED']
        # TODO - Implement

    @unittest.skip("Check authentication function to be implemented")
    def test_set_authentication_header(self):
        pass
        # TODO - Implement

    # Exception Testing
    def test_exceeded_request_retires_exception(self):
        self._response.status_code = ResponseCodes['FETCHING_DATA']

        self.assertRaisesRegex(IrobotClientException, f"{errno.ECONNABORTED}",
                               self._test_requester.get_data, "test/file/path")

    def test_error_responses(self):
        self._response.status_code = ResponseCodes['NOT_FOUND']
        self._response._content = bytearray(json.dumps({'description': 'Content not found'}), 'utf-8')
        test_path = "test/file/path"

        self.assertRaisesRegex(IrobotClientException, str(ResponseCodes['NOT_FOUND']),
                               self._test_requester.get_data, test_path)
        self.assertRaisesRegex(IrobotClientException, 'Content not found',
                               self._test_requester.get_data, test_path)


if __name__ == '__main__':
    unittest.main()