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
from datetime import datetime, timezone


# Default response wait time.
DEFAULT_WAIT_RESPONSE_TIME = 600

response_headers = {
    'ETA': "iRobot-ETA",
    'ACCEPTED_AUTH_TYPES': "WWW-Authenticate"
}


def _get_default_request_delay() -> int:
    """
    If a 202 response returns with no iRobot-ETA header then a default delay (in seconds) will be set from the
    environment or hardcoded in this function.

    :return:
    """

    try:
        return os.environ['IROBOT_REQUEST_DELAY_TIME']
    except:
        return DEFAULT_WAIT_RESPONSE_TIME


def get_request_delay(response: requests.Response) -> int:
    """

    :return:
    """

    if response_headers['ETA'] in response.headers:
        # Eg:  iRobot-ETA: 2017-09-25T12:34:56Z+0000 +/- 123
        stripped_response_eta = (response.headers[response_headers['ETA']].split(' '))[0]
        response_time = datetime.strptime(stripped_response_eta, "%Y-%m-%dT%H:%M:%SZ%z")
        return int((response_time - datetime.now(tz=timezone.utc)).total_seconds())
    else:
        return _get_default_request_delay()


def update_authentication_header(response: requests.Response, auth_credentials: list) -> str:
    """

    :param response:
    :return:
    """

    try:
        accepted_auth_types = response.headers[response_headers['ACCEPTED_AUTH_TYPES']].split(',')
    except KeyError:
        raise

    for auth_type in accepted_auth_types:
        for index, auth_string in enumerate(auth_credentials):
            if auth_type.strip() in auth_string:
                return f"{auth_type} {auth_credentials.pop(index)}"

    return ""
