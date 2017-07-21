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

import os
import collections

CRAM = {"data": ".cram", "index": ".crai"}
BAM = {"data": ".bam", "index": ".bai" and ".pbi"}

class Interface:

    def __init__(self, command_line_args):
        """
        Initiate the class variables with command or environment values.

        :param command_line_args:
        """

        self._input_file = self._remove_file_extension(command_line_args.input_file)
        self._output_file = command_line_args.output_file
        self._file_extensions = self._get_file_extensions(command_line_args.input_file)

        if command_line_args.url is not None:
            self._irobot_url = command_line_args.url
        else:
            try:
                self._irobot_url = os.getenv("IROBOT_URL")
                assert self._irobot_url is not None
            except:
                print("Cannot establish iRobot URL")
                exit()

        if command_line_args.token is not None:
            self._arvados_token = command_line_args.token
        else:
            try:
                self._arvados_token = os.getenv("ARVADOS_TOKEN")
                assert self.arvados_token is not None
            except:
                print("Cannot establish Arvados authentication token")
                exit()

    def _get_file_extensions(self, input_file, no_index=False):
        """
        Assesses the file extension on the input file and returns a list of associate file to download.

        :param input_file:
        :return: associated file extensions for the type of
        """
        split_values = input_file.split('.')
        extension = "." + split_values[1]

        print(extension) # Beth: debug

        file_extensions = {}

        # TODO - Convert file extensions into a list to return
        if not no_index:
            if extension == CRAM["data"]:
                file_extensions = CRAM
            elif extension == BAM["data"]:
                file_extensions = BAM
            else:
                print("ERROR: Unknown input file extension")
                exit()
        else:
            if extension == CRAM["data"]:
                file_extensions = CRAM["data"]
            elif extension == BAM["data"]:
                file_extensions = BAM["data"]
            else:
                print(("ERROR: Unknown input file extension"))
                exit()

        return file_extensions

    def _remove_file_extension(self, input_file):
        """
        Remove the file extension and returns just the name of the file.

        :param input_file:
        :return: file name without the extension
        """

        split_values = input_file.split('.')
        return split_values[0]

    @property
    def irobot_url(self):
        return self._irobot_url

    @property
    def arvados_token(self):
        return self._arvados_token

    @property
    def file_extensions(self):
        return self._file_extensions

    @property
    def input_file(self):
        return self._input_file

    @property
    def output_file(self):
        return self._output_file

