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
from requests.auth import HTTPBasicAuth

from irobotclient.request_handler import ResponseCodes
from irobotclient.response_handler import response_headers

EXT_MAPPING = {
    ".cram": (".crai",),
    ".bam":  (".bai", ".pbi")
}


request_headers = {
    'AUTHORIZATION': "Authorization"
}


def get_url_request_path(irobot_url: str, input_file: str) -> str:
    """
    Return the URL for the requested data without any file extensions if supplied.

    :param irobot_url:
    :param input_file:
    :return:
    """

    input_path = os.path.splitext(input_file)

    return irobot_url + input_path[0]


def get_file_list(input_file: str, no_index: bool) -> list:
    """
    Return all the files that are to be requested.

    :param input_file:
    :return:
    """
    file_list = [input_file]

    file, extension = os.path.splitext(input_file)

    if extension in EXT_MAPPING.keys() and not no_index:
        for ext in EXT_MAPPING[extension]:
            file_list.append(file + ext)

    return file_list


def _get_authentication_strings(arvados_token: str, basic_username: str, basic_password: str) -> dict:
    """
    Set the request authentication_credentials and return them as a dictionary.

    :param auth_type:
    :param arvados_token:
    :return:
    """

    authentication_credentials = {}

    if arvados_token is not None:
        authentication_credentials['Arvados'] = f'Arvados {arvados_token}'

    if basic_password is not None:
        base_password = HTTPBasicAuth(basic_username, basic_password)
        authentication_credentials['Basic'] = f'Basic {base_password}'

    return authentication_credentials


def _set_authentication_header(url: str, auth_credentials: dict) -> str:
    """

    :param response:
    :return:
    """
    request_status_url = url + "/status"
    auth_response = requests.head(request_status_url)

    try:
        accepted_auth_types = auth_response.headers[response_headers['ACCEPTED_AUTH_TYPES']].split(',')
    except KeyError:
        raise

    for auth_type in accepted_auth_types:
        if auth_type.strip() in auth_credentials.keys():
            auth_string = f"{auth_type} {auth_credentials['auth_type']}"
            response = requests.head(request_status_url,
                                     headers={request_headers['AUTHORIZATION']: auth_string})
            if response.status_code == ResponseCodes.SUCCESS:
                return auth_string
        else:
            continue

    return ""


def get_headers(url: str, arvados_token: str, basic_username: str, basic_password: str) -> dict:
    """

    :return:
    """

    headers = {
        request_headers['AUTHORIZATION']: _set_authentication_header(url, _get_authentication_strings(arvados_token,
                                                                                                      basic_username,
                                                                                                      basic_password))
    }

    return headers





