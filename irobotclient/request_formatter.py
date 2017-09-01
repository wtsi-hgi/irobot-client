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
"""request_formatter.py - formats the headers, URL and other necessary features of the requests."""
import os
from requests.auth import HTTPBasicAuth

# A map to couple the data files to their index files.
EXT_MAPPING = {
    ".cram": (".crai",),
    ".bam":  (".bai", ".pbi")
}

# A dictionary of the headers required for the request.
request_headers = {
    'AUTHORIZATION': "Authorization",
    'ACCEPT': "Accept"
}


def get_file_list(input_file: str, no_index: bool) -> list:
    """
    Return all the files (full paths) that are to be downloaded.  This includes index files unless otherwise requested.

    :param input_file: the full path to the requested file.
    :param no_index: flag to not download the index files by default.
    :return: a list of all full paths of all the files to be downloaded.
    """

    file_list = [input_file]

    file, extension = os.path.splitext(input_file)

    if extension in EXT_MAPPING.keys() and not no_index:
        for ext in EXT_MAPPING[extension]:
            file_list.append(file + ext)

    return file_list


def get_authentication_strings(arvados_token: str, basic_username: str, basic_password: str) -> list:
    """
    Set the authentication credentials and return them as a dictionary to be used in the request header.

    This includes creating a 64-bit hash of the username and password for basic authentication.

    :param arvados_token: the string to enable arvados authentication.
    :param basic_username: a string of the username to be used for basic authentication.
    :param basic_password: a string of the password to be used for basic authentication.
    :return: a list of of strings contain authentication credentials.
    """

    authentication_credentials = []

    if arvados_token is not None:
        authentication_credentials.append(f'Arvados {arvados_token}')

    if basic_password is not None:
        base_password = HTTPBasicAuth(basic_username, basic_password)
        authentication_credentials.append(f'Basic {base_password}')

    return authentication_credentials


def get_headers(authentication_credentials: str) -> dict:
    """
    Sets the correct values for the needed request headers and returns them as a dictionary.

    :param authentication_credentials: the string to be used in the first request.
    :return: a dictionary of the request headers.
    """

    headers = {
        request_headers['AUTHORIZATION']: authentication_credentials,
        request_headers['ACCEPT']: "application/octet-stream"  # TODO - remove this explicit header definition
    }

    return headers





