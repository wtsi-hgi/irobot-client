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
The iRobot response status codes are declared below.
"""
RESPONSE_SUCCESS = 200
RESPONSE_FETCHING_DATA = 202
RESPONSE_RANGED_DATA = 206
RESPONSE_CLIENT_MATCHED = 304
RESPONSE_AUTH_FAIL = 401
RESPONSE_DENIED_IRODS = 403
RESPONSE_NOT_FOUND = 404
RESPONSE_INVALID_REQUEST_METHOD = 405
RESPONSE_INVALID_MEDIA_REQUESTED = 406
RESPONSE_INVALID_RANGE = 416
RESPONSE_TIMEOUT = 504
RESPONSE_PRECACHE_FULL = 507


class Requester:

    def __init__(self, requested_url: str, headers: dict):
        """

        :param requested_url:
        :param headers:
        """

        self._request = requests.Request(url=requested_url, headers=headers)
        self._request_delay = 0

    def get_data(self) -> requests.Response:
        """

        :return:
        """
        try:
            for index in range(REQUEST_LIMIT):

                time.sleep(self._request_delay)

                response = requests.head(self._request)

                if response.status_code == RESPONSE_SUCCESS:
                    return requests.get(self._request_delay, stream=True)

                elif response.status_code == RESPONSE_FETCHING_DATA:
                    self._request_delay = self._get_request_delay(response)

                elif response.status_code == RESPONSE_RANGED_DATA:
                    pass # TODO - This response could have a ETA of remaining data ranges

                elif response.status_code == RESPONSE_CLIENT_MATCHED:
                    pass # TODO - Client has already downloaded this data; need to add sum to request for this to work?

                elif response.status_code == RESPONSE_AUTH_FAIL:
                    pass # TODO - Check for response expected authorisation type; try basic auth.

                elif response.status_code == RESPONSE_DENIED_IRODS:
                    raise IrobotClientException(errno=errno.EACCES, message="ERROR: Access to IRODs denied.")

                elif response.status_code == RESPONSE_NOT_FOUND:
                    raise IrobotClientException(errno=errno.ENODATA, message="ERROR: The file requested cannot be "
                                                                             "found.  Please check the path and name "
                                                                             "of the requested file.")

                elif response.status_code == RESPONSE_INVALID_REQUEST_METHOD:
                    raise IrobotClientException(errno=errno.EPROTO, message="ERROR: Invalid HTTP request method; only "
                                                                            "GET, HEAD, POST, DELETE, and OPTIONS "
                                                                            "are supported.")

                elif response.status_code == RESPONSE_INVALID_MEDIA_REQUESTED:
                    raise IrobotClientException(errno=errno.EINVAL, message="ERROR: Unsupported HTTP media type "
                                                                            "requested.")

                elif response.status_code == RESPONSE_INVALID_RANGE:
                    raise IrobotClientException(errno=errno.ERANGE, message="ERROR: Invalid data range requested.")

                elif response.status_code == RESPONSE_TIMEOUT:
                    raise IrobotClientException(errno=errno.ETIMEDOUT, message="ERROR: Connection timeout from iRobot.")

                elif response.status_code == RESPONSE_PRECACHE_FULL:
                    raise IrobotClientException(errno=errno.ENOMEM, message="ERROR: Precache is full or too small for "
                                                                            "the size of the requested file.")

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

    def _get_request_delay(self, response:requests.Response) -> int:
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
