from _typeshed import Incomplete
from typing import Any, Type, Callable

from builtins import function
from flask import Flask
from flask.views import MethodView

__all__ = ['Api', 'Resource', 'marshal', 'marshal_with', 'marshal_with_field', 'abort']


def abort(http_status_code: int, **kwargs: Any) -> None: ...


class Api:
    representations: Incomplete
    urls: Incomplete
    prefix: Incomplete
    default_mediatype: Incomplete
    decorators: Incomplete
    catch_all_404s: Incomplete
    serve_challenge_on_401: Incomplete
    url_part_order: Incomplete
    errors: Incomplete
    blueprint_setup: Incomplete
    endpoints: Incomplete
    resources: Incomplete
    app: Incomplete
    blueprint: Incomplete

    def __init__(self, app: Incomplete | None = None, prefix: str = '', default_mediatype: str = 'application/json',
                 decorators: Incomplete | None = None, catch_all_404s: bool = False,
                 serve_challenge_on_401: bool = False, url_part_order: str = 'bae',
                 errors: Incomplete | None = None) -> None: ...

    def init_app(self, app: Flask) -> None: ...

    def owns_endpoint(self, endpoint: str) -> bool: ...

    def error_router(self, original_handler: function, e: Exception) -> Any: ...

    def handle_error(self, e: Exception) -> Any: ...

    def mediatypes_method(self) -> function: ...

    def add_resource(self, resource: Type[Resource], *urls: Any, **kwargs: Any) -> None: ...

    def resource(self, *urls: Any, **kwargs: Any) -> Any: ...

    def output(self, resource: Callable[[Any, Any], Any]) -> Any: ...

    def url_for(self, resource: Any, **values: Any) -> Any: ...

    def make_response(self, data: Any, *args: Any, **kwargs: Any) -> Any: ...

    def mediatypes(self) -> Any: ...

    def representation(self, mediatype: Any) -> Any: ...

    def unauthorized(self, response: Any) -> Any: ...


class Resource(MethodView):
    representations: Incomplete
    method_decorators: Incomplete

    def dispatch_request(self, *args: Any, **kwargs: Any) -> Any: ...


def marshal(data: Any, fields: Any, envelope: Incomplete | None = None) -> Any: ...


class marshal_with:
    fields: Incomplete
    envelope: Incomplete

    def __init__(self, fields: Any, envelope: Incomplete | None = None) -> None: ...

    def __call__(self, f: Any) -> Any: ...


class marshal_with_field:
    field: Incomplete

    def __init__(self, field: Any) -> None: ...

    def __call__(self, f: Any) -> Any: ...
