import functools
import inspect
from typing import TypedDict, NotRequired, Optional, Callable, Any, Unpack

from j_core.Runtime import Runtime

__all__ = ['transactional']


class Transaction(TypedDict):
    required: NotRequired[bool]
    read_only: NotRequired[bool]
    requires_new: NotRequired[bool]
    rollback_only: NotRequired[bool]


def bind_read_only(func: Callable[..., Any]) -> Callable[..., Any]:
    def bound_read_only(self: Any, *_args: Any, **_kwargs: Any) -> Any:
        session = Runtime.Session()
        try:
            result = func(self, session, *_args, **_kwargs)
            session.rollback()
            return result
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    return bound_read_only


def bind_required(func: Callable[..., Any]) -> Callable[..., Any]:
    def bound_required(self: Any, *_args: Any, **_kwargs: Any) -> Any:
        session = Runtime.Session()
        try:
            result = func(self, session, *_args, **_kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    return bound_required


def transactional(member_function: Optional[Callable[..., Any]] = None, /, **kwargs: Unpack[Transaction]) -> (
        Callable[..., Any]):
    """
    Use on functions to create a session AND limit the functions execution to that session.
    If used without arguments, the default will be a read_only transaction.
    The decorated method will receive the :class:`sqlalchemy.orm.Session` instance as it's first parameter

    :param member_function: Function which is passed in the current active transaction

    :param read_only: the session will discard any insert/update/delete operations
    :type read_only: bool

    :param rollback_only: the session will allow any changes which are visible within the functions scope and
        will be rolled back after execution
    :type rollback_only: bool

    :param required: creates a new transaction if none exists, yet.
        Uses the existing transaction if one is currently running
    :type required: bool

    :param requires_new: creates a new transaction, parallel to any running
    :type requires_new: bool
    """

    required = kwargs.get('required')
    read_only = kwargs.get('read_only')
    requires_new = kwargs.get('requires_new')
    rollback_only = kwargs.get('rollback_only')

    wrapper_assignments = ('__module__', '__name__', '__qualname__', '__doc__', '__type_params__')
    wrapper_updates = ('__dict__',)

    if inspect.ismethod(member_function) or inspect.isfunction(member_function):
        return functools.wraps(member_function, wrapper_assignments, wrapper_updates)(bind_read_only(member_function))

    def _inner(func: Callable[..., Any]) -> Callable[..., Any]:
        if required is True:
            return functools.wraps(func, wrapper_assignments, wrapper_updates)(bind_required(func))
        elif read_only is True:
            return functools.wraps(func, wrapper_assignments, wrapper_updates)(bind_read_only(func))

        # default
        return functools.wraps(func, wrapper_assignments, wrapper_updates)(bind_required(func))

    return _inner
