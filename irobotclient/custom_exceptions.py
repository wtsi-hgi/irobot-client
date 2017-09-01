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
"""custom_exceptions.py - create exceptions based on iRobot responses and other program failures where necessary."""


class IrobotClientException(OSError):
    """
    Not all built-in exceptions return an error code.  Therefore this custom exception inherits the structure
    of the OSError which does support the errno property, along with all the other meaningful exception properties.
    This will be used to raise an exception object that can also be used as a meaningful non-zero exit code.
    """

    def __init__(self, errno:int, message:str, *args, **kwargs) -> None:
        """
        Instatntiate a class onject with a custom error number and message.

        :param errno: a integer returned by an iRobot failure response or a standard error code.
        :param message: populated by the content of an iRobot failure response or a custom string.
        """
        super().__init__(*args, **kwargs)

        self.errno = errno
        self.strerror = message