__all__ = ['ElementNotFoundException', 'MissingDBConnectionException']


class ElementNotFoundException(Exception):
    pass


class MissingDBConnectionException(Exception):
    pass
