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

EXT_MAPPING = {
    ".cram": (".crai",),
    ".bam":  (".bai", ".pbi")
}


def get_header(method: str, auth_type: str, auth_token: str) -> dict:
    """
    Set the request headers and return them as a dictionary.

    :param method:
    :param auth_type:
    :param auth_token:
    :return:
    """
    headers = {
        "method": {method},
        "authorization": f'{auth_type} {auth_token}'
    }

    return headers


def get_url_request_path(irobout_url: str, input_file: str) -> str:
    """
    Return the URL for the requested data without any file extensions if supplied.

    :param irobout_url:
    :param input_file:
    :return:
    """

    input_path = os.path.splitext(input_file)

    return irobout_url + input_path[0]


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
            return [extension, EXT_MAPPING[extension]]
    else:
        return [extension]




