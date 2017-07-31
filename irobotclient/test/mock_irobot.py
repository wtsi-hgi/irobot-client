import unittest

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


class Test202Response(unittest.TestCase):
    def runTest(self):
        mock_request_handler = Requester("test", {"test": "test"})
        mock_request_handler.response.status_code = 202
        mock_request_handler._make_request()



if __name__ == '__main__':
    unittest.main()