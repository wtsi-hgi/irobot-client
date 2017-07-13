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
import os

# Global vars
_input_file_extensions = [".cram", ".crai"]
_input_file_location = ""
_output_file_location = ""

def _get_command_line_agrs():
    """
    Get command line arguments and set global variables for file locations

    :return:
    """

    parser = argparse.ArgumentParser(description="Comand line interface for iRobot HTTP requests")
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file")
    args = parser.parse_args()

    global  _input_file_location
    global _output_file_location
    _input_file_location = args.input
    _output_file_location = args.output


def _check_input_file_argument():
    '''
    Send a HEAD HTTP request to check the status of the files, including all expected extensions

    HEAD /path/to/file/index.html HTTP/1.1


    :return: n/a
    '''

    # TODO


def _handle_HEAD_request_response(response_code : int):
    '''
    Handle the response from the HEAD request on the input files.  A successful, file available response
    will allow continuation on to a GET request.  Failed responses will be logged and the program
    will exit.

    :return:
    '''

    # TODO

def _check_output_file_argument():
    '''
    Check that the output file exists, if not create one.  If the file already exists
    ask the user if they want to overwrite the file or specify a new one, else add an increment to the
    file name.

    :return: n/a
    '''
    if os.path.exists(_input_file_location):
        # TODO
        print("Ask user if they want to overwrite the file?")


if __name__ == "__main__":
    _get_command_line_agrs()
    _check_input_file_argument()
    _check_output_file_argument()




