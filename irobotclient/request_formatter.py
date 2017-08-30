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
from requests.auth import HTTPBasicAuth

# A map of sorts to couple the data files to their index files.
EXT_MAPPING = {
    ".cram": (".crai",),
    ".bam":  (".bai", ".pbi")
}

# A dictionary of the headers required for the request.
request_headers = {
    'AUTHORIZATION': "Authorization",
    'ACCEPT': "Accept"
}

# TODO - update docstrings
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


def get_authentication_strings(arvados_token: str, basic_username: str, basic_password: str) -> list:
    """
    Set the request authentication_credentials and return them as a dictionary.

    :param auth_type:
    :param arvados_token:
    :return:
    """

    authentication_credentials = []

    if arvados_token is not None:
        authentication_credentials.append(f'Arvados {arvados_token}')

    if basic_password is not None:
        base_password = HTTPBasicAuth(basic_username, basic_password)
        authentication_credentials.append(f'Basic {base_password}')

    return authentication_credentials


def get_headers(authentication_credentials: list) -> dict:
    """

    :return:
    """

    headers = {
        request_headers['AUTHORIZATION']: authentication_credentials.pop(0),
        request_headers['ACCEPT']: "application/octet-stream"
    }

    return headers





