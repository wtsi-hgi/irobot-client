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
                                     description="Command line interface for iRobot HTTP requests",
                                     usage="irobot-client [options] INPUT_FILE OUTPUT_FILE")
    parser.add_argument("input_file", help="path and name of input file")
    parser.add_argument("output_file", help="path and name of output file")
    parser.add_argument("-u", "--url", help="URL scheme, domain and port for irobot. EXAMPLE: http://irobot:5000/")
    parser.add_argument("-t", "--token", help="Arvados authentication token")
    parser.add_argument("-f", "--force", default=False, action="store_true", help="force overwrite output file if "
                                                                                  "it already exists")
    parser.add_argument("--no-index", default=False, action="store_true", help="Do not download index files for"
                                                                               "CRAM/BAM files")
    args = parser.parse_args()

    _check_input_file_argument(args)
    _check_output_file_argument(args.output_file, args.force)

    print("After processing: ", args) # Beth - debug

    return args

def _check_input_file_argument(args):
    '''
    Strip leading slash from input argument and check there is an file extension so the type of associated index
    file can be determined.

    :param args: the command line arguments
    '''
    # Remove leading slash from input
    if args.input_file.startswith('\\') or args.input_file.startswith('/'):
        args.input_file = args.input_file.lstrip('/\\')

    if not args.input_file.find('.'):
        print("ERROR: Cannot determine file type.  Please specify a file extension in your input file name")
        exit()


def _check_output_file_argument(arg, overwrite):
    '''
    Check if the output file already exists; if it does and the force overwite command argument is not set the
    print error and exit.

    :return: n/a
    '''
    if os.path.exists(arg) and not overwrite:
        print("WARNING: Output file already exists.  Use --force option to overwrite")
        exit()


if __name__ == "__main__":
    irobot_client = IrobotClient(_get_command_line_agrs())
    irobot_client.run()
    exit(0)




