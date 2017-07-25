class IrobotClientException(OSError):
    """
    Not all built-in exceptions return an error code.  Therefore this customer exception inherits the structure
    of the OSError which does support the errno property along with all the other meaningful exception properties.
    This will be used to raise an exception object that can also be used as a meaningful standard error exit code.
    """

    def __init__(self, errno:int, message:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.errno = errno
        self.strerror = message