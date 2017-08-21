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
from requests.auth import HTTPBasicAuth
import os

EXT_MAPPING = {
    ".cram": (".crai",),
    ".bam":  (".bai", ".pbi")
}


def get_authentication_strings(arvados_token=None, basic_username=None, basic_password=None) -> dict:
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


def get_headers() -> dict:
    """

    :return:
    """
    # TODO - support other headers
    return {}


def get_url_request_path(irobot_url: str, input_file: str) -> str:
    """
    Return the URL for the requested data without any file extensions if supplied.

    :param irobot_url:
    :param input_file:
    :return:
    """

    input_path = os.path.splitext(input_file)

    return irobot_url + input_path[0]


def get_file_extensions(input_file: str, no_index: bool) -> list:
    """
    Return all the file type extensions that are to be requested.

    :param input_file:
    :return:
    """

    extension = (os.path.splitext(input_file))[1]

    # Return an empty list if there is no extension
    if extension == "":
        return []

    if extension in EXT_MAPPING.keys():
        if no_index:
            return [extension]
        else:
            return [extension, *EXT_MAPPING[extension]]
    else:
        return [extension]




