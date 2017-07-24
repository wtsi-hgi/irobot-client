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

from irobotclient import configuration_handler


def _print_error_details(error: OSError):
    print("Inside _output_error_details")
    print(error)
    exit(error.errno)

if __name__ == "__main__":

    try:

        # Set configurations from command line and/or environment.
        configuration_handler.run()

        # Set a list of files that are going to be called.
        # Send HTTP request.
        # Handle responses.
        exit()
    except OSError as err:
        _print_error_details(err)
    except Exception as err:
        print(err)