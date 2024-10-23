from typing import TypeVar, Generic, Callable

from jerver.inject import injectable, DependencyRegistry

__all__ = ['Registry', 'ServiceInterface', 'serviceinterface', 'SERVICE_PREFIX']

CLS = TypeVar('CLS', bound=type)

SERVICE_PREFIX = '/service/'


class ServiceInterface(Generic[CLS]):
    """ Meta data for a client-callable backend service """

    def __init__(self, cls: CLS, name: str):
        self.cls = cls
        self.name = name


Registry = DependencyRegistry[ServiceInterface[type]]()


def serviceinterface(name: str) -> Callable[[CLS], CLS]:
    """
    Use as decorator to include a class in the registry.
    Each entry in the registry is registered as an api endpoint,
    thus this should only be used for client-callable endpoints
    """

    def _serviceinterface(cls: CLS) -> CLS:
        servicename = f'{SERVICE_PREFIX}{name}'
        Registry.register(servicename, ServiceInterface(cls, servicename))
        injectable(cls)
        return cls

    return _serviceinterface
