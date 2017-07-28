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
import time

from datetime import datetime


class Requester:

    def __init__(self, requested_url: str, headers: dict):
        """

        :param requested_url:
        :param headers:
        """

        self.url = requested_url
        self.headers = headers
        self.response = requests.Response()
        self.request_delay = 0

    def handle_request(self):
        """

        :param method:
        :return:
        """

        time.sleep(self.request_delay)

        try:
            self.response = requests.get(self.url, headers=self.headers)
        except ConnectionError:
            raise
        except TimeoutError:
            raise
        except:
            raise

        self._process_response()

        print(f'Exiting Requester.handle_request with response of: {self.response}')

    def _process_response(self):
        """

        :return:
        """

        if self.response.status_code == 202:
            self._set_request_delay()
            self.handle_request()
        else:
            print("More to come")
            # TODO - implement error handling and download stream to output

        self.headers["Method"] = "GET"

    def _set_request_delay(self):
        """

        :return:
        """

        if self.response.headers.values() is "application/vnd.irobot.eta":
            self.response.encoding = "ISO8601 UTC"

            # Eg:  2017-09-25T12:34:56Z+00:00 +/- 123
            stripped_response_eta = (self.response.text.split('Z'))[0]
            response_time = datetime.strptime(stripped_response_eta, "%Y-%m-%dT%H:%M:%S")

            self.request_delay = (response_time - datetime.now()).total_seconds()



