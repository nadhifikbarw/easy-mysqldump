class AppException(Exception):
    pass


class MetadataDBClosedException(AppException):
    pass


class IllegalFilenameException(AppException):
    pass


class DatabaseClosedException(AppException):
    pass


class IllegalExpirationException(AppException):
    pass
