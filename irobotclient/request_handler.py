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

from irobotclient import response_handler
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_formatter import request_headers

# Limit the amount of consecutive request retries.
REQUEST_LIMIT = 10

# An enumeration to name HTTP response status codes.
ResponseCodes = {
    'SUCCESS': 200,
    'FETCHING_DATA': 202,
    'RANGED_DATA': 206,
    'CLIENT_MATCHED': 304,
    'AUTHENTICATION_FAILED': 401,
    'DENIED_IRODS': 403,
    'NOT_FOUND': 404,
    'INVALID_REQUEST_METHOD': 405,
    'INVALID_MEDIA_REQUESTED': 406,
    'INVALID_RANGE': 416,
    'TIMEOUT': 504,
    'PRECACHE_FULL': 507
}

# TODO - update docstrings
class Requester:
    def __init__(self, requested_url: str, headers: dict, additional_auth_credentials=None):
        """

        :param requested_url:
        :param headers:
        """

        self._requested_url = requested_url
        self._headers = headers
        self._additional_auth_credentials = additional_auth_credentials

    def get_data(self, file_path: str) -> requests.Response:
        """

        :return:
        """
        full_url = self._requested_url + file_path

        try:
            for index in range(REQUEST_LIMIT):

                request = requests.Request(method='GET', url=full_url, headers=self._headers)
                req = request.prepare()
                session = requests.Session()
                response = session.send(req, stream=True)

                print(f"Response Full_URL: {full_url}")

                if response.status_code == ResponseCodes['SUCCESS']:
                    return response

                elif response.status_code == ResponseCodes['FETCHING_DATA']:
                    time.sleep(response_handler.get_request_delay(response))

                elif response.status_code == ResponseCodes['RANGED_DATA']:
                    pass  # TODO - This response could have a ETA of remaining data ranges

                elif response.status_code == ResponseCodes['CLIENT_MATCHED']:
                    pass  # TODO - Client has already downloaded this data; need to add sum to request for this to work?

                elif response.status_code == ResponseCodes['AUTHENTICATION_FAILED'] and \
                        self._additional_auth_credentials:
                    self._headers[request_headers['AUTHORIZATION']] = \
                        response_handler.update_authentication_header(response, self._additional_auth_credentials)

                elif 400 <= response.status_code < 600:
                    try:
                        raise IrobotClientException(response.status_code, response.json()['description'])
                    except ValueError:
                        raise

            raise IrobotClientException(errno=errno.ECONNABORTED, message="ERROR: Maximum number of request "
                                                                          "retries.  This could be because of a large "
                                                                          "file being fetch.  Please try again later.")

        except ConnectionError:
            raise
        except TimeoutError:
            raise
        except IrobotClientException:
            raise
        except:
            raise
