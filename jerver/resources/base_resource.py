from abc import abstractmethod
from typing import Any, ParamSpec, Tuple

from flask_restful import Resource

__all__ = ['BaseResource']


class BaseResource(Resource):
    P = ParamSpec('P')

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__()

    @abstractmethod
    def get(self, *args: P.args, **kwargs: P.kwargs) -> Tuple[Any, int]:
        pass

    @abstractmethod
    def post(self, *args: P.args, **kwargs: P.kwargs) -> Tuple[Any, int]:
        pass

    @abstractmethod
    def put(self, *args: P.args, **kwargs: P.kwargs) -> Tuple[Any, int]:
        pass

    @abstractmethod
    def delete(self, *args: P.args, **kwargs: P.kwargs) -> Tuple[Any, int]:
        pass
