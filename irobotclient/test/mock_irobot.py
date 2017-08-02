import unittest
from unittest.mock import MagicMock

import requests
import errno
from collections import namedtuple

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, RESPONSES


class TestResponses(unittest.TestCase):
    def setUp(self):
        self.__old_request_head = requests.head
        self._response = requests.Response()
        requests.head = MagicMock(spec=requests.head)
        requests.get = MagicMock(spec=requests.get)

    def tearDown(self):
        requests.head = self.__old_request_head

    def test_404_response(self):
        self._response.status_code = RESPONSES['NOT_FOUND'].status_code
        requests.head.return_value = self._response

        test_requester = Requester("testURL", {"testKey": "testValue"})
        self.assertRaisesRegex(IrobotClientException, f"{RESPONSES['NOT_FOUND'].errno}", test_requester.get_data)




if __name__ == '__main__':
    unittest.main()