__all__ = ['ResourceException', 'EndpointNotFoundException', 'MissingDBConnectionException']


class ResourceException(Exception):
    pass


class EndpointNotFoundException(ResourceException):
    pass


class MissingDBConnectionException(Exception):
    pass
