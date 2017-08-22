import unittest
from unittest.mock import MagicMock

import requests
import time
import errno

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes, error_table


class TestRequester(unittest.TestCase):
    """
    This test case assesses the functions of the request_handler.py code such as how various responses are
    dealt with and if the delay for the next request (if appropriate) is set correctly.
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

    def test_response_loop(self):
        self._response.status_code = ResponseCodes.FETCHING_DATA

        self.assertRaisesRegex(IrobotClientException, f"{errno.ECONNABORTED}",
                               self._test_requester.get_data)

    def test_200(self):
        self._response.status_code = ResponseCodes.SUCCESS
        self.assertEqual(self._test_requester.get_data(), self._response)

    @unittest.skip("206 to be implemented")
    def test_206(self):
        self._response.status_code = ResponseCodes.RANGED_DATA
        # TODO - Implement

    @unittest.skip("304 to be implemented")
    def test_304(self):
        self._response.status_code = ResponseCodes.CLIENT_MATCHED
        # TODO - Implement

    @unittest.skip("Check authentication function to be implemented")
    def test_set_authentication_header(self):
        pass
        # TODO - Implement

    def test_error_responses(self):
        for code in error_table.keys():
            self._response.status_code = code

            self.assertRaisesRegex(IrobotClientException, str(error_table[code][0]), self._test_requester.get_data)
            self.assertRaisesRegex(IrobotClientException, error_table[code][1], self._test_requester.get_data)


if __name__ == '__main__':
    unittest.main()