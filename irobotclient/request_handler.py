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

from enum import Enum

from irobotclient import response_handler
from irobotclient.custom_exceptions import IrobotClientException

"""
Limit on how many times the same request is sent, including any alterations such as changes to the header.
In theory a single request will take two attempts; one for the HEAD request to make sure the data exists and
a second to GET the data.

However, a request may generate a response to wait for the data to be fetched and try again later or to attempt
a different authorisation method.

Either way, the limit defined below helps prevent stack overflow and unnecessary requests when it is clear a request
is not going to work.
"""
REQUEST_LIMIT = 10

# An enumeration to name HTTP response status codes.
class ResponseCodes(Enum):
    SUCCESS = 200
    FETCHING_DATA = 202
    RANGED_DATA = 206
    CLIENT_MATCHED = 304
    AUTHENTICATION_FAILED = 401
    DENIED_IRODS = 403
    NOT_FOUND = 404
    INVALID_REQUEST_METHOD = 405
    INVALID_MEDIA_REQUESTED = 406
    INVALID_RANGE = 416
    TIMEOUT = 504
    PRECACHE_FULL = 507

# Set HTTP response error codes to an associated standard error number and custom message.
error_table = {
    ResponseCodes.AUTHENTICATION_FAILED: (errno.ECONNABORTED, "Authentication failed."),
    ResponseCodes.DENIED_IRODS: (errno.EACCES, "Access to IRODs denied."),
    ResponseCodes.NOT_FOUND: (errno.ENODATA, "The file requested cannot be found.  Please check the "
                                             "path and name of the requested file."),
    ResponseCodes.INVALID_REQUEST_METHOD: (errno.EPROTO, "Invalid HTTP request method."),
    ResponseCodes.INVALID_MEDIA_REQUESTED: (errno.EINVAL, "Unsupported HTTP media type requested."),
    ResponseCodes.INVALID_RANGE: (errno.ERANGE, "Invalid data range requested."),
    ResponseCodes.TIMEOUT: (errno.ETIMEDOUT, "Connection timeout from iRobot."),
    ResponseCodes.PRECACHE_FULL: (errno.ENOMEM, "Precache is full or too small for the size of the "
                                                "requested file.")
}


class Requester:
    def __init__(self, requested_url: str, headers: dict):
        """

        :param requested_url:
        :param headers:
        """
        self._request = requests.Request(url=requested_url, headers=headers)

    def get_data(self, file_path="") -> requests.Response:
        """

        :return:
        """
        self._request.url += file_path

        try:
            for index in range(REQUEST_LIMIT):

                response = requests.get(self._request, stream=True)

                #print("self._request inside get_data() general: ", self._request)  # Beth - Debug

                if response.status_code == ResponseCodes.SUCCESS:
                    return response

                elif response.status_code == ResponseCodes.FETCHING_DATA:
                    time.sleep(response_handler.get_request_delay(response))

                elif response.status_code == ResponseCodes.RANGED_DATA:
                    pass  # TODO - This response could have a ETA of remaining data ranges

                elif response.status_code == ResponseCodes.CLIENT_MATCHED:
                    pass  # TODO - Client has already downloaded this data; need to add sum to request for this to work?

                elif response.status_code in error_table.keys():
                    raise IrobotClientException(*error_table[response.status_code])

                continue

            raise IrobotClientException(errno=errno.ECONNABORTED, message="ERROR: Maximum number of request "
                                                                          "retries. Please try again later.")
        except ConnectionError:
            raise
        except TimeoutError:
            raise
        except IrobotClientException:
            raise
        except:
            raise
