from typing import TypeVar, Dict, Generic, Any

__all__ = ['DependencyRegistry']

T = TypeVar('T')


class DependencyRegistry(Generic[T]):
    def __init__(self, *args: Any, **kwargs: Any):
        self._registry: Dict[str, T] = {}

    def register(self, key: str, instance: T) -> None:
        self._registry[key] = instance

    def resolve(self, key: str) -> T:
        return self._registry[key]
