import unittest
from unittest.mock import MagicMock

import requests
import errno
from collections import namedtuple

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester

# The below structures are a straight copy and paste from the request_handle code.
ResponseStruct = namedtuple("ResponseStruct", "status_code, errno")

RESPONSE_SUCCESS = ResponseStruct(status_code=200, errno=None)
RESPONSE_FETCHING_DATA = ResponseStruct(status_code=202, errno=None)
RESPONSE_RANGED_DATA = ResponseStruct(status_code=206, errno=None)
RESPONSE_CLIENT_MATCHED = ResponseStruct(status_code=304, errno=None)
RESPONSE_AUTH_FAIL = ResponseStruct(status_code=401, errno=errno.ECONNREFUSED)
RESPONSE_DENIED_IRODS = ResponseStruct(status_code=403, errno=errno.EACCES)
RESPONSE_NOT_FOUND = ResponseStruct(status_code=404, errno=errno.ENODATA)
RESPONSE_INVALID_REQUEST_METHOD = ResponseStruct(status_code=405, errno=errno.EPROTO)
RESPONSE_INVALID_MEDIA_REQUESTED = ResponseStruct(status_code=406, errno=errno.EINVAL)
RESPONSE_INVALID_RANGE = ResponseStruct(status_code=416, errno=errno.ERANGE)
RESPONSE_TIMEOUT = ResponseStruct(status_code=504, errno=errno.ETIMEDOUT)
RESPONSE_PRECACHE_FULL = ResponseStruct(status_code=507, errno=errno.ENOMEM)

class TestResponses(unittest.TestCase):
    def setUp(self):
        self.__old_request_head = requests.head
        self._response = requests.Response
        requests.head = MagicMock(spec=requests.head)
        requests.get = MagicMock(spec=requests.get)

    def tearDown(self):
        requests.head = self.__old_request_head

    def test_404_response(self):
        self._response.status_code = RESPONSE_NOT_FOUND.status_code
        requests.head.return_value = self._response

        test_requester = Requester("testURL", {"testKey": "testValue"})
        self.assertRaisesRegex(IrobotClientException, f'{RESPONSE_NOT_FOUND.errno}', lambda: test_requester.get_data())




if __name__ == '__main__':
    unittest.main()