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
"""response_handler.py - handles specific unsuccessful iRobot responses codes to attempt the request again."""
import os
import requests
import re

from datetime import datetime, timezone

# Default response wait time.
DEFAULT_WAIT_RESPONSE_TIME = 600

# The useful headers expected in responses from iRobot
response_headers = {
    'ETA': "iRobot-ETA",
    'ACCEPTED_AUTH_TYPES': "WWW-Authenticate",
    'CHECKSUM': "ETag"
}


def _get_default_request_delay() -> int:
    # If a 202 response returns with no iRobot-ETA header then a delay will be set by this method.

    try:
        return os.environ['IROBOT_REQUEST_DELAY_TIME']
    except:
        return DEFAULT_WAIT_RESPONSE_TIME


def get_request_delay(response: requests.Response) -> int:
    """
    Handle the wait time for 202 responses by processing the ETA header or setting a default value if necessary.

    :param response: the response from iRobot.
    :return: an integer value equating to seconds to wait until the request should be sent again.
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
    Returns an accepted authentication string to use in the next request following an authentication failure response.

    If none of the credentials match any of the accepted authentication methods supplied in the response header,
    the list of credentials is clear to avoid this method being called again unnecessarily.

    :param response: the response from iRobot.
    :param auth_credentials: a list of authentication credentials.
    :return: a string to set the authentication header on the request.
    """

    try:
        response_auth_header_string = response.headers[response_headers['ACCEPTED_AUTH_TYPES']]
    except KeyError:
        raise

    if '=' in response_auth_header_string:
        # Get the auth types based on strings following the 'realm=' properties.
        accepted_auth_types = re.findall(r'\w+\s+realm=', response_auth_header_string)
        # Remove the realm keyword property
        for index, string in enumerate(accepted_auth_types):
            accepted_auth_types[index] = re.sub(r'realm=', '', string)
    else:
        accepted_auth_types = response_auth_header_string.split(',')

    for auth_type in accepted_auth_types:
        for index, auth_string in enumerate(auth_credentials):
            if auth_type.strip() in auth_string:
                return f"{auth_type} {auth_credentials.pop(index)}"

    auth_credentials.clear()
    return ""
