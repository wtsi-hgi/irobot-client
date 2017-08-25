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
import logging

from logging.handlers import RotatingFileHandler
from os import path
from requests import Response

from irobotclient import configuration_handler
from irobotclient import request_formatter
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester

# Error log
ERROR_LOG_FILE = "irobot_client_error.log"

# Limit for the size (in bytes) of data downloaded at a time.
CHUNK_SIZE = 1024


def _set_error_logger(file_name: str) -> logging.Logger:
    logger = logging.getLogger("Rotating log")
    logger.setLevel(logging.ERROR)

    handler = RotatingFileHandler(ERROR_LOG_FILE, maxBytes=10000)
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def _handle_error_details(error: Exception, log: logging.Logger):
    """
    Print the output of any errors raised.

    Utilises the OSError exception class which the iRobot Client uses for custom exceptions too.

    :param error:
    :return:
    """
    log.exception(error)

    print(f"{error}\nError: program terminated; please check irobot_client_error.log for more details")

    if hasattr(error, 'errno'):
        exit(error.errno)
    exit(1)


def _download_data(response: Response, output_dir:str):
    """

    :param response:
    :param output_dir:
    :return:
    """
    file_name = (path.split(response.url))[1]

    with open(f"{output_dir}{file_name}", "wb") as file:
        for data_chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if data_chunk:
                file.write(bytes(data_chunk))


def _run(request_handler: Requester, file_list: list):
    """

    :param request_handler:
    :param file_list:
    :return:
    """
    for file in file_list:
        # TODO - handle index file issues whereby a bam bai file may not be present but a pbi might.
        response = request_handler.get_data(file)

        print(f"Response inside main.run(): {response}")  # Beth - debug

        _download_data(response, config_details.output_dir)
        # TODO - checksum test for each file if possible

    print("Exiting....")


if __name__ == "__main__":

    log = _set_error_logger(ERROR_LOG_FILE)

    # Set configurations from command line and/or environment.
    try:
        config_details = configuration_handler.run()

        url = request_formatter.get_url_request_path(config_details.url, config_details.input_file)
        authentication_credentials = request_formatter.get_authentication_strings(config_details.arvados_token,
                                                                                  config_details.basic_username,
                                                                                  config_details.basic_password)
        headers = request_formatter.get_headers(authentication_credentials)
        file_list = request_formatter.get_file_list(config_details.input_file, config_details.no_index)

        _run(Requester(url, headers, authentication_credentials), file_list)
    except IrobotClientException as err:
        _handle_error_details(err, log)
    except OSError as err:
        _handle_error_details(err, log)
    except Exception as err:
        print("Download failed, please check error log")
        _handle_error_details(err, log)