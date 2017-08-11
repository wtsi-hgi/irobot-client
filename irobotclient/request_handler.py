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
from collections import namedtuple

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

"""
If a 202 response returns with not iRobot-ETA header then a default delay (in seconds) will be set.
"""
DEFAULT_REQUEST_DELAY = 600

"""
The iRobot response status codes are declared below along with an associated standard error number if applicable.
"""
ResponseStruct = namedtuple("ResponseStruct", "status_code, errno")

RESPONSES = {
    'SUCCESS': ResponseStruct(status_code=200, errno=None),
    'FETCHING_DATA': ResponseStruct(status_code=202, errno=None),
    'RANGED_DATA': ResponseStruct(status_code=206, errno=None),
    'CLIENT_MATCHED': ResponseStruct(status_code=304, errno=None),
    'AUTH_FAIL': ResponseStruct(status_code=401, errno=errno.ECONNREFUSED),
    'DENIED_IRODS': ResponseStruct(status_code=403, errno=errno.EACCES),
    'NOT_FOUND': ResponseStruct(status_code=404, errno=errno.ENODATA),
    'INVALID_REQUEST_METHOD': ResponseStruct(status_code=405, errno=errno.EPROTO),
    'INVALID_MEDIA_REQUESTED': ResponseStruct(status_code=406, errno=errno.EINVAL),
    'INVALID_RANGE': ResponseStruct(status_code=416, errno=errno.ERANGE),
    'TIMEOUT': ResponseStruct(status_code=504, errno=errno.ETIMEDOUT),
    'PRECACHE_FULL': ResponseStruct(status_code=507, errno=errno.ENOMEM)
}


class Requester:
    def __init__(self, requested_url: str, headers: dict):
        """

        :param requested_url:
        :param headers:
        """

        self._request = requests.Request(url=requested_url, headers=headers)
        self._request_delay = 0

    def get_data(self, file_extension="") -> requests.Response:
        """

        :return:
        """
        self._request.url += file_extension

        try:
            for index in range(REQUEST_LIMIT):

                time.sleep(self._request_delay)

                response = requests.head(self._request)

                print("self._request inside get_data() general: ", self._request.url)  # Beth - Debug

                if response.status_code == RESPONSES['SUCCESS'].status_code:
                    return requests.get(self._request, stream=True)

                elif response.status_code == RESPONSES['FETCHING_DATA'].status_code:
                    self._request_delay = self._get_request_delay(response)

                elif response.status_code == RESPONSES['RANGED_DATA'].status_code:
                    pass  # TODO - This response could have a ETA of remaining data ranges

                elif response.status_code == RESPONSES['CLIENT_MATCHED'].status_code:
                    pass  # TODO - Client has already downloaded this data; need to add sum to request for this to work?

                elif response.status_code == RESPONSES['AUTH_FAIL'].status_code:
                    pass  # TODO - Check for response expected authorisation type; try basic auth.

                elif response.status_code == RESPONSES['DENIED_IRODS'].status_code:
                    raise IrobotClientException(errno=RESPONSES['DENIED_IRODS'].errno,
                                                message="ERROR: Access to IRODs denied.")

                elif response.status_code == RESPONSES['NOT_FOUND'].status_code:
                    raise IrobotClientException(errno=RESPONSES['NOT_FOUND'].errno,
                                                message="ERROR: The file requested cannot be found.  Please check the "
                                                        "path and name of the requested file.")

                elif response.status_code == RESPONSES['INVALID_REQUEST_METHOD'].status_code:
                    raise IrobotClientException(errno=RESPONSES['INVALID_REQUEST_METHOD'].errno,
                                                message="ERROR: Invalid HTTP request method; only GET, HEAD, POST, "
                                                        "DELETE, and OPTIONS are supported.")

                elif response.status_code == RESPONSES['INVALID_MEDIA_REQUESTED'].status_code:
                    raise IrobotClientException(errno=RESPONSES['INVALID_MEDIA_REQUESTED'].errno,
                                                message="ERROR: Unsupported HTTP media type requested.")

                elif response.status_code == RESPONSES['INVALID_RANGE'].status_code:
                    raise IrobotClientException(errno=RESPONSES['INVALID_RANGE'].errno,
                                                message="ERROR: Invalid data range requested.")

                elif response.status_code == RESPONSES['TIMEOUT'].status_code:
                    raise IrobotClientException(errno=RESPONSES['TIMEOUT'].errno,
                                                message="ERROR: Connection timeout from iRobot.")

                elif response.status_code == RESPONSES['PRECACHE_FULL'].status_code:
                    raise IrobotClientException(errno=RESPONSES['PRECACHE_FULL'].errno,
                                                message="ERROR: Precache is full or too small for the size of the "
                                                        "requested file.")

                continue

            else:
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

    def _get_request_delay(self, response: requests.Response) -> int:
        """

        :return:
        """

        if "iRobot-ETA" in response.headers:
            # Eg:  iRobot-ETA: 2017-09-25T12:34:56Z+00:00 +/- 123
            stripped_response_eta = (response.headers["iRobot-ETA"].split('Z'))[0]
            response_time = datetime.strptime(stripped_response_eta, "%Y-%m-%dT%H:%M:%S")
            return int((response_time - datetime.now()).total_seconds())
        else:
            return DEFAULT_REQUEST_DELAY
