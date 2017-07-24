import argparse
import string
import re
import os
import errno

from irobotclient.custom_exceptions import IrobotClientFileExistsError


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

    print(f'_get_command_line_args() args: {args}')

    return args

def _validate_command_line_args(args):
    """

    :param args:
    :return:
    """
    _check_input_file_argument(args)
    _check_output_directory_argument(args)

    # TODO - Check URL (with trailing slash) and auth token; if not supplied on the command line then check environement

    return args

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

        for file in os.listdir(args.output_dir):

            # Basic match; will return true if the file begins with the input_file string.
            # TODO - Improve regex on checking whether input file already exists.
            if re.match(file, args.input_file) and not args.force:
                raise IrobotClientFileExistsError(errno=errno.EEXIST, message="File already exists. Please use the "
                                                                              "--force option to overwrite.")

    except NotADirectoryError:
        raise
    except:
        raise

def run():
    """

    :return:
    """

    args = _get_command_line_agrs()
    _validate_command_line_args(args)

    print(f'Configuration complete: {args}')

    return args
