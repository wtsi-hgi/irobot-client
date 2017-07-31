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
import errno

from datetime import datetime
from irobotclient.custom_exceptions import IrobotClientException

# Request count limit
REQUEST_LIMIT = 10


class Requester:

    def __init__(self, requested_url: str, headers: dict):
        """

        :param requested_url:
        :param headers:
        """

        self.url = requested_url
        self.headers = headers
        self.request_delay = 0
        self.request_count = 0
        self.response = requests.Response


    def handle_request(self):
        """

        :return:
        """

        if self.request_count is REQUEST_LIMIT:
            raise IrobotClientException(errno=errno.ECONNABORTED, message="ERROR: Maximum number of request retries. "
                                                                          "Please try again later.")

        self.response = self._make_request()

        if self.response.headers.values() is "application/vnd.irobot.eta":
            self.request_delay = self._get_request_delay(self.response)

        self.request_count += 1


    def _make_request(self) -> requests.Response:
        """

        :param method:
        :return:
        """

        time.sleep(self.request_delay)

        try:
            response = requests.get(self.url, headers=self.headers)
        except ConnectionError:
            raise
        except TimeoutError:
            raise
        except:
            raise Exception("UNKNOWN ERROR: Failed to obtain a response to the request.")

        return response


    def _get_request_delay(self, response:requests.Response) -> int:
        """

        :return:
        """

        response.encoding = "ISO8601 UTC"

        # Eg:  2017-09-25T12:34:56Z+00:00 +/- 123
        stripped_response_eta = (response.text.split('Z'))[0]
        response_time = datetime.strptime(stripped_response_eta, "%Y-%m-%dT%H:%M:%S")

        return int((response_time - datetime.now()).total_seconds())



