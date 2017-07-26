import argparse
import string
import re
import os
import errno

from irobotclient.custom_exceptions import IrobotClientException


def _get_command_line_agrs():
    """
    Get program arguments, calls validation methods, and returns the values in the argparse object.

    :return: args
    """

    parser = argparse.ArgumentParser(prog="irobot-client",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="Command line interface for iRobot HTTP requests",
                                     usage="irobot-client [options] INPUT_FILE OUTPUT_FILE")
    parser.add_argument("input_file", help="path and name of input file")
    parser.add_argument("output_dir", help="path of output directory")
    parser.add_argument("-u", "--url", help="URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/")
    parser.add_argument("-t", "--token", help="Arvados authentication token")
    parser.add_argument("-f", "--force", default=False, action="store_true", help="force overwrite output file if "
                                                                                  "it already exists")
    parser.add_argument("--no-index", default=False, action="store_true", help="Do not download index files for"
                                                                               "CRAM/BAM files")
    args = parser.parse_args()

    print(f'_get_command_line_args() args: {args}')  # Beth - debug

    return args


def _validate_command_line_args(args):
    """
    Ensures all the necessary details are set to form the requests.

    :param args:
    :return:
    """
    _check_input_file_argument(args)
    _check_output_directory_argument(args)
    _check_url_argument(args)
    _check_authorisation_token(args)


def _check_input_file_argument(args):
    """
    Strip leading slash from input argument to prevent double slashes in API request.

    :param args: the command line arguments
    """

    if args.input_file.startswith('/'):
        args.input_file = args.input_file.lstrip('/')


def _check_output_directory_argument(args):
    """
    Check if the output directory already exists and if it already contains files of the same name as the input file.

    :return: n/a

    """

    try:
        # Expand the output_dir argument so the full directory path can be used in the rest of the program.
        args.output_dir = os.path.expanduser(args.output_dir)

        # Split up the path string to obtain just the file name without extensions and full path.
        file_name = os.path.splitext((os.path.split(args.input_file))[1])[0]

        for dir_file in os.listdir(args.output_dir):

            # Basic match; will return true if the directory file begins with the input_file string.
            # TODO - Improve regex on checking whether input file already exists.
            if re.match(dir_file, file_name) and not args.force:
                raise IrobotClientException(errno=errno.EEXIST, message="File already exists. Please use the "
                                                                        "--force option to overwrite.")

    except IrobotClientException:
        raise
    except OSError:
        raise
    except:
        raise Exception("UNKNOWN ERROR: Failed to validate the output directory.")


def _check_url_argument(args):
    """
    Check if a url has been provided via command line or environment setting and check trailing slash.

    :param args:
    :return:
    """

    try:
        if args.url is None:
            args.url = os.environ['IROBOTURL']
    except KeyError:
        raise IrobotClientException(errno.ENOKEY, "Cannot set URL from command line argument or environment"
                                                  " variable.")
    except:
        raise Exception("UNKNOWN ERROR: Failed to set the URL.")

    if not args.url.endswith('/'):
        args.url += '/'


def _check_authorisation_token(args):
    """
    Check is the authorisation token has been set on the command line or environment variable.

    :param args:
    :return:
    """

    # TODO - Going to have to handle basic authorisation eventually which will involve a new interface/class.
    try:
        if args.token is None:
            args.token = os.environ['ARVADOSTOKEN']
    except KeyError:
        raise IrobotClientException(errno.ENOKEY, "Cannot set authentication token from command line argument "
                                                  "or environment variable.")
    except:
        raise Exception("UNKNOWN ERROR: Failed to set the authorisation token.")


def run():
    """
    Calls the functions to collect any command line arguments, set configuration details needed for the iRobot
    requests, and return the argparse object to the request formatter.

    :return:
    """

    args = _get_command_line_agrs()
    _validate_command_line_args(args)

    return args
