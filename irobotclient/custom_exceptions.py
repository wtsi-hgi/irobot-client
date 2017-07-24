class IrobotClientFileExistsError(FileExistsError):
    def __init__(self, errno:int, message:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.errno = errno
        self.strerror = message