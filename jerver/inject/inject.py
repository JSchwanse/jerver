import inspect
from typing import Callable, Type, TypeVar

__all__ = ['Registry', 'useInject', 'injectable']

T = TypeVar('T', bound=object)

Registry: dict[str, T] = {}  # type: ignore[valid-type]


def useInject(cls: Type[T]) -> T:
    return Registry[cls.__name__]


def injectable(class_or_name: Type[T] | str) -> Callable[[Type[T]], None] | None:
    """ Use on class to add to registry of injectable instances """
    if inspect.isclass(class_or_name):
        # call constructor and register instance
        # TODO: resolve and use other injectables as constructor arguments
        Registry[class_or_name.__name__] = class_or_name()
    elif isinstance(class_or_name, str):
        def _injectable(cls: Type[T]) -> None:
            # TODO: resolve and use other injectables as constructor arguments
            Registry[cls.__name__] = cls()

        return _injectable

    return None
