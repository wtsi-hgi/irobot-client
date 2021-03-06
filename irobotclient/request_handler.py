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
import json

"""request_handler.py - Requester class to make the request to iRobot and attempt to rectify any failure responses."""
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


class Requester:
    """
    This class sends a request to iRobot and attempts to rectify any failed attempts dependent on the response
    return code.  A successful request causes the class to pass the response up to the calling code to handle
    the data download.

    Public methods:
    get_data - handles the requesting of data.
    """

    def __init__(self, headers: dict, requested_url=None, additional_auth_credentials=None):
        """
        Instantiates a class object with the data require for a request attempt.

        :param requested_url: a string of the iRobot server url not including the file path.
        :param headers: a dictionary of the headers for the request.
        :param additional_auth_credentials: a list of additional authentication credentials is available.
        """

        self._requested_url = requested_url
        self._headers = headers
        self._additional_auth_credentials = additional_auth_credentials

    def get_data(self, file_path: str) -> requests.Response:
        """
        Requests the data from iRobot

        :param file_path: the full path of the file requested.
        :return: a successful iRobot response
        """

        if self._requested_url:
            file_path = self._requested_url + file_path

        try:
            for index in range(REQUEST_LIMIT):

                request = requests.Request(method='GET', url=file_path, headers=self._headers)
                req = request.prepare()
                session = requests.Session()
                response = session.send(req, stream=True)

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
                    except json.JSONDecodeError:
                        raise IrobotClientException(response.status_code, f"{response.reason}. URL: {file_path}")

            raise IrobotClientException(errno.ECONNABORTED, "ERROR: Maximum number of request retries.  This could be "
                                                            "because of a large file being fetch.  Please try again "
                                                            "later.")

        except ConnectionError:
            raise
        except TimeoutError:
            raise
        except IrobotClientException:
            raise
        except:
            raise
