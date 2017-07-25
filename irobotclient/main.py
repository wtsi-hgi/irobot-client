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
from irobotclient.custom_exceptions import IrobotClientException


def _print_error_details(error: OSError):
    """
    Print the output of any errors raised.

    Utilises the OSError exception class which the iRobot Client uses for custom exceptions too.

    :param error:
    :return:
    """
    print("Inside _output_error_details") # Beth - debug
    print(error)
    exit(error.errno)

if __name__ == "__main__":

    try:

        # Set configurations from command line and/or environment.
        config_details = configuration_handler.run()
        print(f'Configuration complete: {config_details}') # Beth - debug

        # Set a list of files that are going to be called.
        # Send HTTP request.
        # Handle responses.
        exit()
    except IrobotClientException as err:
        _print_error_details(err)
    except OSError as err:
        _print_error_details(err)
    except Exception as err:
        print(err)
        exit(1)