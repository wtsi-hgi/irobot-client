"""
main.py - the entry point of the program.

"""
import logging

from logging.handlers import RotatingFileHandler
from os import path
from requests import Response

from irobotclient import configuration_handler
from irobotclient import request_formatter
from irobotclient.custom_exceptions import IrobotClientException
from irobotclient.request_handler import Requester, ResponseCodes

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


def _download_data(response: Response, output_dir:str):
    # Downloads data to a file in the the output directory in iterable chunks.

    file_name = (path.split(response.url))[1]

    with open(f"{output_dir}{file_name}", "wb") as file:
        for data_chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if data_chunk:
                file.write(bytes(data_chunk))


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

        _download_data(response, config_details.output_dir)
        # TODO - checksum test for each file if possible

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