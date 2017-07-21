"""
Copyright (c) 2017 Genome Research Ltd.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import requests

# from irobotclient.interface import Interface
#
# SUCCESS_RESPONSE = 200
# WAIT_RESPONSE = 202
# MATCHED_RESPONSE = 304
#
# # Mapping request responses to function handlers.
#
#
# class IrobotClient(Interface):
#
#
#     def _check_input_files_exist(self):
#         """
#         If the input file exists the code goes on to get the data.
#
#         :return:
#         """
#
#         url = self.irobot_url + self.input_file
#
#         request_headers = {'Authorization': self.arvados_token}
#
#         print(f'In client object: {self.file_extensions}')  # Beth - debug
#
#         for key, value in self.file_extensions.items():
#             print(f'Requesting: {value}')
#             head_response = requests.head(url + value, headers=request_headers)
#             print(f'{head_response} with {url + value}')  # Beth: help with debugging
#             self._handle_head_request_response(head_response)
#
#     def _handle_head_request_response(self, response: requests.Response):
#         """
#         Handle the response from the HEAD request on the input files.
#
#         :rtype: object
#         :return:
#         """
#
#         # TODO - handle responses
#         if response.status_code == SUCCESS_RESPONSE:
#             print("Success")
#             return
#         elif response.status_code == WAIT_RESPONSE:
#             print("Wait")
#             return
#         elif response.status_code == MATCHED_RESPONSE:
#             print("Already Downloaded")
#             return
#         else:
#             print("Download Failed")
#             exit()
#
#     def run(self):
#         self._check_input_files_exist()
class IrobotClient:

    def __init__(self, requested_file, irobot_url, authentication_type, authentication_token):
        """

        :param requested_file:
        :param irobot_url:
        :param authentication_type:
        :param authentication_token:
        """

        # TODO - Implement class
        print("Do stuff")

