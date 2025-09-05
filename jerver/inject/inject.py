import inspect
from typing import Callable, Type, TypeVar, Any

from jerver.inject import DependencyRegistry

__all__ = ['Registry', 'useInject', 'injectable']

T = TypeVar('T')

Registry = DependencyRegistry[Any]()


def useInject(cls: Type[T]) -> Any:
    return Registry.resolve(cls.__name__)


def injectable(class_or_name: Type[T] | str) -> Callable[[Type[T]], None] | None:
    """ Use on class to add to registry of injectable instances """
    if inspect.isclass(class_or_name):
        # call constructor and register instance
        # TODO: resolve and use other injectables as constructor arguments
        Registry.register(class_or_name.__name__, class_or_name())
    elif isinstance(class_or_name, str):
        def _injectable(cls: Type[T]) -> None:
            # TODO: resolve and use other injectables as constructor arguments
            Registry.register(cls.__name__, cls())

        return _injectable

    return None
