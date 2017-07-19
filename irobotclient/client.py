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

from irobotclient.configuration import ConfigurationData

SUCCESS_RESPONSE = 200
WAIT_RESPONSE = 202, 206
MATCHED_RESPONSE = 304


class IrobotClient:

    def __init__(self, input_file, output_file):

        self.configuration_data = ConfigurationData()
        self.input_file_location = input_file
        self.output_file_location = output_file


    def _check_input_files_exist(self):
        """
        If the input file exists the code goes on to get the data

        :return:
        """

        url = self.configuration_data.irobot_url + self.input_file_location

        hdrs = {'Authorization': self.configuration_data.arvados_token}

        for file_extension in self.configuration_data.input_file_extensions:
            head_response = requests.head(url + file_extension, headers=hdrs)
            print(head_response.status_code)  # Beth: help with debugging
            self._handle_HEAD_request_response(head_response)

        return None

    def _handle_HEAD_request_response(self, response: requests.Response):
        '''
        Handle the response from the HEAD request on the input files.  A successful, file available response
        will allow continuation on to a GET request.  Failed responses will be logged and the program
        will exit.

        :rtype: object
        :return:
        '''

        # TODO - handle responses
        if response.status_code == SUCCESS_RESPONSE:
            print("Success")
            return
        elif response.status_code == WAIT_RESPONSE:
            print("Wait")
            return
        elif response.status_code == MATCHED_RESPONSE:
            print("Already Downloaded")
            return
        else:
            exit()

    def run(self):
        self._check_input_files_exist()
        return None