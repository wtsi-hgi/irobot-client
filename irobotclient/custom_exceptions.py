"""
custom_exceptions.py - create exceptions based on iRobot responses and other program failures where necessary.

"""


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