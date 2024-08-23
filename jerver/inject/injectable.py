import inspect

Registry: dict[str, object] = {}


def injectable(*args):
    """ Use on class to add to registry of injectable instances """
    if inspect.isclass(args[0]):
        # call constructor and register instance
        Registry[args[0].__name__] = args[0]()  # TODO: resolve and use other injectables as constructor arguments
    elif isinstance(args[0], str):
        def _injectable(cls):
            Registry[cls.__name__] = cls()  # TODO: resolve and use other injectables as constructor arguments

        return _injectable
