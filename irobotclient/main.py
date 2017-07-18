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

from irobotclient.client import Irobot_Client


def _get_command_line_agrs():
    """
    Get program arguments

    :return: args
    """

    parser = argparse.ArgumentParser(description="Comand line interface for iRobot HTTP requests")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    args = parser.parse_args()

    print("From _get_command_line_args: ", args)

    args = _check_input_file_argument(args)
    args = _check_output_file_argument(args)

    print("After processing: ", args)

    return args

def _check_input_file_argument(args):
    '''
    Strip leading slashes and file extensions for input argument

    :param args:
    :return: args
    '''
    # Remove leading slash from input
    if args.input.startswith('\\') or args.input.startswith('/'):
        args.input = args.input.lstrip('/\\')

    # Remove file extensions
    if args.input.find('.'):
        arg_split = args.input.split('.')
        args.input = arg_split[0]   # Keeps the leftmost side of the '.'

    return args


def _check_output_file_argument(args):
    '''
    Check that the output file exists, if not create one.  If the file already exists
    ask the user if they want to overwrite the file or specify a new one, else add an increment to the
    file name.

    :return: n/a
    '''
    if os.path.exists(args.output):
        # TODO - handle output file argument
        print("Ask user if they want to overwrite the file?")
    else:
        print("Output file doesn't exist")

    return args


if __name__ == "__main__":
    args = _get_command_line_agrs()
    irobot_client = Irobot_Client(args.input, args.output)
    irobot_client.run()
    exit(0)




