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
"""main.py - the entry point of the program."""
import logging
import hashlib
import errno

from logging.handlers import RotatingFileHandler
from os import path
from requests import Response

from irobotclient import configuration_handler
from irobotclient import request_formatter
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes
from irobotclient.response_handler import response_headers

# Error log
ERROR_LOG_FILE = "irobot_client_error.log"

# Limit for the size (in bytes) of data downloaded at a time.
CHUNK_SIZE = 1024


def _set_error_logger(file_name: str) -> logging.Logger:
    # Set up the logger for writing exceptions to file_name.

    logger = logging.getLogger("Rotating log")
    logger.setLevel(logging.ERROR)

    handler = RotatingFileHandler(ERROR_LOG_FILE, maxBytes=10000)
    formatter = logging.Formatter('\n%(asctime)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def _handle_error_details(error: Exception, log: logging.Logger):
    # Log the exception to file and exit with a non-zero code.

    log.exception(error)

    print(f"{error}\nError: program terminated; please check irobot_client_error.log for more details")

    if hasattr(error, 'errno'):
        exit(error.errno)
    exit(1)


def _download_data(response: Response, save_location: str):
    # Downloads data to a file in the the output directory in iterable chunks.

    with open(save_location, "wb") as file:
        for data_chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if data_chunk:
                file.write(bytes(data_chunk))


def _validate_downloaded_data(response: Response, file_path: str):
    # Check that the response checksum tag matches the file checksum.

    try:
        checksum = response.headers[response_headers['CHECKSUM']]
    except KeyError:
        raise

    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)

    if not hasher.hexdigest() == checksum:
        raise IrobotClientException(errno=errno.ECONNABORTED, message="ERROR: The checksum of the downloaded file does "
                                                                      "not match the checksum expected.  The file may "
                                                                      "be corrupt or missing data.  Please try again.")


def _run(request_handler: Requester, file_list: list, log=None):
    # Call the core functionality of the program; sending the request and getting the response

    for file in file_list:
        try:
            response = request_handler.get_data(file)
        except IrobotClientException as err:
            if file != file_list[-1] and err.errno is ResponseCodes['NOT_FOUND']:
                log.exception(IrobotClientException)
                print(f"WARNING: Could not find {file}. Continuing with next requested file.")
                continue
            else:
                raise

        full_file_path = config_details.output_dir + (path.split(response.url))[1]
        _download_data(response, full_file_path)
        _validate_downloaded_data(response, full_file_path)

    print("Downloads complete. Exiting....")


if __name__ == "__main__":

    log = _set_error_logger(ERROR_LOG_FILE)

    try:
        config_details = configuration_handler.run()

        authentication_credentials = request_formatter.get_authentication_strings(config_details.arvados_token,
                                                                                  config_details.basic_username,
                                                                                  config_details.basic_password)
        headers = request_formatter.get_headers(authentication_credentials.pop(0))
        file_list = request_formatter.get_file_list(config_details.input_file, config_details.no_index)

        _run(Requester(config_details.url, headers, authentication_credentials), file_list)
    except IrobotClientException as err:
        _handle_error_details(err, log)
    except OSError as err:
        _handle_error_details(err, log)
    except Exception as err:
        print("Download failed, please check error log")
        _handle_error_details(err, log)