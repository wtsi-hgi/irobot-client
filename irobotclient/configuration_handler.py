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
"""configuration_handler.py - acquire and validate program input."""
import argparse
import os
import errno

from irobotclient.custom_exceptions import IrobotClientException


def _get_command_line_args(args=None):
    # Get program arguments from the commandline, parse them, and then return them.

    parser = argparse.ArgumentParser(prog="irobot-client",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="Command line interface for iRobot HTTP requests",
                                     usage="irobot-client [options] INPUT_FILE OUTPUT_DIR")
    parser.add_argument("input_file", help="path and name of input file")
    parser.add_argument("output_dir", help="path of output directory")
    parser.add_argument("-u", "--url",
                        help="Use this tag if no irobot URL is set as an environment variable {IROBOT_URL}. "
                             "URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/",
                        default=os.getenv('IROBOT_URL'))
    parser.add_argument("--arvados_token",
                        help="Arvados authentication token; if not supplied here it will be sourced from the "
                             "environment {ARVADOS_TOKEN} or default to an",
                        default=os.getenv('ARVADOS_TOKEN'))
    parser.add_argument("--basic_username",
                        help="Basic authentication username; if not supplied here it will be sourced from the "
                             "environment {BASIC_USERNAME} then, failing that, current system user",
                        default=os.getenv('BASIC_USERNAME', os.uname()))
    parser.add_argument("--basic_password",
                        help="Basic authentication password; if not supplied here it will be sourced from the "
                             "environment {BASIC_PASSWORD}",
                        default=os.getenv('BASIC_PASSWORD'))
    parser.add_argument("-f", "--force", default=False, action="store_true", help="force overwrite output file if "
                                                                                  "it already exists")
    parser.add_argument("--no_index", default=False, action="store_true", help="Do not download index files for"
                                                                               "CRAM/BAM files")
    args = parser.parse_args(args)

    return args


def _validate_command_line_args(args):
    # Ensures all the necessary details are set and formatted.

    _check_input_file_argument(args)
    _check_output_directory_argument(args)
    _check_url_argument(args)
    _check_authorisation_credentials(args)


def _check_input_file_argument(args):
    # Simple check to see if the input argument is a directory.
    # Strips the leading slash from the input argument to prevent double slashes in the API request.

    if args.input_file.endswith('/'):
        raise IrobotClientException(errno=errno.ECONNABORTED,
                                    message="Cannot download entire directories at present.")

    if args.input_file.startswith('/'):
        args.input_file = args.input_file.lstrip('/')


def _check_output_directory_argument(args):
    # Check if the output directory already exists and if it already contains files of the same name as the input file.

    # Expand the output_dir argument so the full directory path can be used in the rest of the program.
    args.output_dir = os.path.expanduser(args.output_dir)

    # Add a trailing slash to indicate directory.
    if not args.output_dir.endswith('/'):
        args.output_dir = args.output_dir + '/'

    try:
        for dir_file in os.listdir(args.output_dir):
            if not args.force and args.input_file == dir_file:
                raise IrobotClientException(errno=errno.EEXIST, message="File already exists. Please use the "
                                                                        "--force option to overwrite.")

    except IrobotClientException:
        raise
    except OSError:
        raise
    except:
        raise


def _check_url_argument(args):
    # Check if a url has been provided via command line or environment setting and check trailing slash.

    if args.url is None:
        raise IrobotClientException(errno=errno.EINVAL, message="No iRobot URL specified; please check input "
                                                                "arguments and/or environment variables.")

    if not args.url.endswith('/'):
        args.url += '/'


def _check_authorisation_credentials(args):
    # Check if the authorisation credentials have been set on the command line or environment variable.

    if not args.arvados_token and not args.basic_password:
        raise IrobotClientException(errno=errno.EACCES, message="No Arvados or Basic authentication set; please check "
                                                                "input arguments and/or environment variables.")


def run(config_args=None) -> argparse.ArgumentParser:
    """
    Calls the functions to collect any command line arguments, set configuration details needed for the iRobot
    requests, and return the argparse object to the request formatter.

    :return: ArgumentParser object - containing all the necessary formatted request details.
    """

    args = _get_command_line_args(config_args)
    _validate_command_line_args(args)

    return args
