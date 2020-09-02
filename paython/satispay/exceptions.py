class PaythonException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnexpectedRequestMethod(PaythonException):
    def __init__(self, message):
        super().__init__(message)