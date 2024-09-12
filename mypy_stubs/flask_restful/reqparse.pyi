from _typeshed import Incomplete


class Namespace(dict):
    def __getattr__(self, name): ...

    def __setattr__(self, name, value) -> None: ...


text_type: Incomplete


class Argument:
    name: Incomplete
    default: Incomplete
    dest: Incomplete
    required: Incomplete
    ignore: Incomplete
    location: Incomplete
    type: Incomplete
    choices: Incomplete
    action: Incomplete
    help: Incomplete
    case_sensitive: Incomplete
    operators: Incomplete
    store_missing: Incomplete
    trim: Incomplete
    nullable: Incomplete

    def __init__(self, name, default: Incomplete | None = None, dest: Incomplete | None = None, required: bool = False,
                 ignore: bool = False, type=..., location=('json', 'values'), choices=(), action: str = 'store',
                 help: Incomplete | None = None, operators=('=',), case_sensitive: bool = True,
                 store_missing: bool = True, trim: bool = False, nullable: bool = True) -> None: ...

    def source(self, request): ...

    def convert(self, value, op): ...

    def handle_validation_error(self, error, bundle_errors): ...

    def parse(self, request, bundle_errors: bool = False): ...


class RequestParser:
    args: Incomplete
    argument_class: Incomplete
    namespace_class: Incomplete
    trim: Incomplete
    bundle_errors: Incomplete

    def __init__(self, argument_class=..., namespace_class=..., trim: bool = False,
                 bundle_errors: bool = False) -> None: ...

    def add_argument(self, *args, **kwargs): ...

    def parse_args(self, req: Incomplete | None = None, strict: bool = False, http_error_code: int = 400): ...

    def copy(self): ...

    def replace_argument(self, name, *args, **kwargs): ...

    def remove_argument(self, name): ...
