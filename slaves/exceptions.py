class SlavesBaseException(Exception):
    pass


class SlaveIsLocked(SlavesBaseException):
    pass


class InvalidSign(SlavesBaseException):
    pass


class UnknownError(SlavesBaseException):
    pass
