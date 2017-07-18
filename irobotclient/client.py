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

import os
import requests
import json

_response_codes = {
    'SUCCESS': 200,
    'WAIT': 202,
    'RANGES': 206,
    'ALREADY_DOWNLOADED': 304,
    'ERROR': {None, 401, 403, 404, 406, 416, 507}
}

class Irobot_Client():

    def __init__(self, input_arg, output_arg):
        '''

        :return:
        '''

        # TODO - create a hierarchy of irobot config files: /etc/ < /USER/local/
        _system_conf = '/etc/irobot.conf'
        _user_conf = '~/.irobot.conf'
        _test_conf = '../test_irobot_client_config.json'

        try:
            if os.path.exists(_system_conf):
                config_file = open(_system_conf)
            elif os.path.exists(_user_conf):
                config_file = open(_user_conf)
            elif os.path.exists(_test_conf):
                config_file = open(_test_conf)

            config_data = json.load(config_file)
            config_file.close()
        except:
            print("ERROR: No .irobot.conf file found.  Please create one with vi ~/.irobot.conf\n"
                  "For more details on the config file please see:\n"
                  "https://github.com/wtsi-hgi/irobot-client")
            exit()

        self._arvados_token = config_data["arvados_token"]
        self._irobot_url = config_data["irobot_address"]
        self._input_file_extensions = config_data["file_extensions"]

        self._input_file_location = input_arg
        self._output_file_location = output_arg

        # Beth - testing
        print("Beth testing:\n", self._input_file_location, " ", self._output_file_location, "\n",
              self._arvados_token, " ", self._irobot_url, "\n",
              self._input_file_extensions)

    def _check_input_files_exist(self):
        '''

        :return:
        '''

        url = self._irobot_url + self._input_file_location

        hdrs = {'Authorization': self._arvados_token}

        for file_extension in self._input_file_extensions:
            head_response = requests.head(url + file_extension, headers=hdrs)
            print(head_response.status_code)  # Beth: help with debugging
            self._handle_HEAD_request_response(head_response)

        return None

    def _handle_HEAD_request_response(response: requests.Response):
        '''
        Handle the response from the HEAD request on the input files.  A successful, file available response
        will allow continuation on to a GET request.  Failed responses will be logged and the program
        will exit.

        :rtype: object
        :return:
        '''

        global _response_codes

        # TODO - handle responses
        if response.status_code == _response_codes['SUCCESS']:
            print("Success")
            return
        elif response.status_code == _response_codes['WAIT']:
            print("Wait")
            return
        elif response.status_code == _response_codes['RANGES']:
            print("Ranges")
            return
        elif response.status_code == _response_codes['ALREADY_DOWNLOADED']:
            print("Already Downloaded")
            return
        else:
            for err in _response_codes['ERROR']:
                if response.status_code == err:
                    print("Error")
            exit()

    def run(self):
        return None