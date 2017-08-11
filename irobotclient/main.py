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
import errno

from os import path
from requests import Response

from irobotclient import configuration_handler
from irobotclient import request_formatter
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester

# Limit for the size (in bytes) of data downloaded at a time.
CHUNK_SIZE = 1024


def _print_error_details(error: OSError):
    """
    Print the output of any errors raised.

    Utilises the OSError exception class which the iRobot Client uses for custom exceptions too.

    :param error:
    :return:
    """

    print(error)
    exit(error.errno)


def _download_data(response: Response, output_dir:str):
    """

    :param response:
    :param output_dir:
    :return:
    """
    try:
        file_name = (path.split(response.url))[1]

        with open(f"{output_dir}{file_name}", "wb") as file:
            for data_chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if data_chunk:
                    file.write(bytes(data_chunk))
    except OSError as err:
        _print_error_details(err)
    except:
        raise IrobotClientException(errno=errno.ECONNABORTED, message="Cannot write content to file.")


def _run(request_handler: Requester, file_extensions: []):
    try:

        if not file_extensions:
            response = request_handler.get_data()
            _download_data(response, config_details.output_dir)
            # TODO - checksum test if possible
        else:
            for ext in file_extensions:
                # TODO - handle index file issues whereby a bam bai file may not be present but a pbi might.
                response = request_handler.get_data(ext)

                print(f"Response inside main.run(): {response}")  # Beth - debug

                _download_data(response, config_details.output_dir)
                # TODO - checksum test for each file if possible

        print("Exiting....")
    except IrobotClientException as err:
        _print_error_details(err)
    except OSError as err:
        _print_error_details(err)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":

    # Set configurations from command line and/or environment.
    config_details = configuration_handler.run()

    url = request_formatter.get_url_request_path(config_details.url, config_details.input_file)
    headers = request_formatter.get_header(config_details.token)
    file_extensions = request_formatter.get_file_extensions(config_details.input_file, config_details.no_index)

    _run(Requester(url, headers), file_extensions)