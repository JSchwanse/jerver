from _typeshed import Incomplete

__all__ = ['String', 'FormattedString', 'Url', 'DateTime', 'Float', 'Integer', 'Arbitrary', 'Nested', 'List', 'Raw',
           'Boolean', 'Fixed', 'Price']


class MarshallingException(Exception):
    def __init__(self, underlying_exception) -> None: ...


class Raw:
    attribute: Incomplete
    default: Incomplete

    def __init__(self, default: Incomplete | None = None, attribute: Incomplete | None = None) -> None: ...

    def format(self, value): ...

    def output(self, key, obj): ...


class Nested(Raw):
    nested: Incomplete
    allow_null: Incomplete

    def __init__(self, nested, allow_null: bool = False, **kwargs) -> None: ...

    def output(self, key, obj): ...


class List(Raw):
    container: Incomplete

    def __init__(self, cls_or_instance, **kwargs) -> None: ...

    def format(self, value): ...

    def output(self, key, data): ...


class String(Raw):
    def format(self, value): ...


class Integer(Raw):
    def __init__(self, default: int = 0, **kwargs) -> None: ...

    def format(self, value): ...


class Boolean(Raw):
    def format(self, value): ...


class FormattedString(Raw):
    src_str: Incomplete

    def __init__(self, src_str) -> None: ...

    def output(self, key, obj): ...


class Url(Raw):
    endpoint: Incomplete
    absolute: Incomplete
    scheme: Incomplete

    def __init__(self, endpoint: Incomplete | None = None, absolute: bool = False, scheme: Incomplete | None = None,
                 **kwargs) -> None: ...

    def output(self, key, obj): ...


class Float(Raw):
    def format(self, value): ...


class Arbitrary(Raw):
    def format(self, value): ...


class DateTime(Raw):
    dt_format: Incomplete

    def __init__(self, dt_format: str = 'rfc822', **kwargs) -> None: ...

    def format(self, value): ...


class Fixed(Raw):
    precision: Incomplete

    def __init__(self, decimals: int = 5, **kwargs) -> None: ...

    def format(self, value): ...


Price = Fixed
