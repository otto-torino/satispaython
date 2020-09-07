class SatispaythonException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnexpectedRequestMethod(SatispaythonException):
    def __init__(self, message):
        super().__init__(message)