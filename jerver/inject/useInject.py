from jerver.inject.injectable import Registry


def useInject[T](cls: type[T]) -> T:
    return Registry[cls.__name__]
