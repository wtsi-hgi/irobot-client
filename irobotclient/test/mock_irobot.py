import unittest
from unittest.mock import MagicMock

import requests

from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester

# class _MockRequest(unittest.TestCase):
#     """
#
#     """
#     def setUp(self):
#         # set up request but how?
#
# class TestResponses(unittest.TestCase): # Too general I think
#     """
#
#     """
#     def setUp(self):
#         # set up request?
#         # set up response?
#
#     # Test wait response
#         # request a cram or bam file
#         # return 202 response for cram or bam
#         # receive delayed request
#         # return 200 response
#
#     # Test file with no extension specified
#         # return 200 response
#
#     # Test failure codes
#
#
# # Test inputs?

# Start simple


class TestResponses(unittest.TestCase):
    def setUp(self):
        self.__old_request_head = requests.head
        self._response = MagicMock(spec=requests.Response)
        requests.head = MagicMock(spec=requests.head)

    def tearDown(self):
        requests.head = self.__old_request_head

    def test_404_response(self):
        self._response.return_value = requests.Response.status_code =[404]
        test_requester = Requester("testURL", {"testKey": "testValue"})
        self.assertRaises(IrobotClientException, test_requester.get_data())




if __name__ == '__main__':
    unittest.main()