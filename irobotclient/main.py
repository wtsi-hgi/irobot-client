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

import argparse
import string
import os

from irobotclient.client import IrobotClient


def _get_command_line_agrs():
    """
    Get program arguments

    :return: args
    """

    parser = argparse.ArgumentParser(prog="irobot-client",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="Comand line interface for iRobot HTTP requests",
                                     usage="irobot-client [options] INPUT_FILE OUTPUT_FILE")
    parser.add_argument("input_file", help="path and name of input file")
    parser.add_argument("output_file", help="path and name of output file")
    parser.add_argument("-u", "--url", help="URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/")
    parser.add_argument("-f", "--force", default=False, action="store_true",
                        help="force overwrite output file if it already exists")
    args = parser.parse_args()

    print("From _get_command_line_args: ", args)

    args.input_file = _check_input_file_argument(args.input_file)
    args.output_file = _check_output_file_argument(args.output_file, args.force)

    print("After processing: ", args)

    return args

def _check_input_file_argument(arg):
    '''
    Strip leading slashes and file extensions for input argument

    :param args:
    :return: args
    '''
    # Remove leading slash from input
    if arg.startswith('\\') or arg.startswith('/'):
        arg = arg.lstrip('/\\')

    # Remove file extensions
    if arg.find('.'):
        arg_split = arg.split('.')
        arg = arg_split[0]   # Keeps the leftmost side of the '.'

    return arg


def _check_output_file_argument(arg, overwrite):
    '''
    Check that the output file exists, if not create one.  If the file already exists
    ask the user if they want to overwrite the file or specify a new one, else add an increment to the
    file name.

    :return: n/a
    '''
    if os.path.exists(arg) and not overwrite:
        print("Output file already exists.  Use --force option to overwrite")
        exit()

    return arg


if __name__ == "__main__":
    args = _get_command_line_agrs()
    irobot_client = IrobotClient(args.input, args.output)
    irobot_client.run()
    exit(0)




