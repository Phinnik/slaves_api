class SlaveIsLockedError(Exception):
    pass


class UnknownMethodError(Exception):
    def __str__(self) -> str:
        return 'Unknown Method: should either Get or Post'
