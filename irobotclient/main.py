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


def _print_error_details(error: OSError):
    """
    Print the output of any errors raised.

    Utilises the OSError exception class which the iRobot Client uses for custom exceptions too.

    :param error:
    :return:
    """
    print("Inside _output_error_details") # Beth - debug
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

        if response.headers["content-type"] == "application/octet-stream":
            with open(f"{output_dir}{file_name}", "wb") as file:
                file.write(bytes(response.content))
        else:
            with open(f"{output_dir}{file_name}", "w") as file:
                file.write(response.content)
    except:
        response.close()
        raise IrobotClientException(errno=errno.ECONNABORTED, message="")


def _run():
    try:

        # Set configurations from command line and/or environment.
        config_details = configuration_handler.run()

        file_extensions = request_formatter.get_file_extensions(config_details.input_file, config_details.no_index)
        url = request_formatter.get_url_request_path(config_details.url, config_details.input_file)
        headers = request_formatter.get_header(config_details.token)

        if not file_extensions:
            request_handler = Requester(url, headers)
            response = request_handler.get_data()
            _download_data(response, config_details.output_dir)
        else:
            for ext in file_extensions:
                # TODO - handle index file issues whereby a bam bai file may not be present but a pbi might.
                request_handler = Requester(url + ext, headers)
                response = request_handler.get_data()
                _download_data(response, config_details.output_dir)

        print("Exiting....")
        exit()
    except IrobotClientException as err:
        _print_error_details(err)
    except OSError as err:
        _print_error_details(err)
    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":

    _run()