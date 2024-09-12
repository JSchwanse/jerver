from _typeshed import Incomplete

START_OF_DAY: Incomplete
END_OF_DAY: Incomplete
url_regex: Incomplete


def url(value): ...


class regex:
    pattern: Incomplete
    re: Incomplete

    def __init__(self, pattern, flags: int = 0) -> None: ...

    def __call__(self, value): ...

    def __deepcopy__(self, memo): ...


def iso8601interval(value, argument: str = 'argument'): ...


def date(value): ...


def natural(value, argument: str = 'argument'): ...


def positive(value, argument: str = 'argument'): ...


class int_range:
    low: Incomplete
    high: Incomplete
    argument: Incomplete

    def __init__(self, low, high, argument: str = 'argument') -> None: ...

    def __call__(self, value): ...


def boolean(value): ...


def datetime_from_rfc822(datetime_str): ...


def datetime_from_iso8601(datetime_str): ...
