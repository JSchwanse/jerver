import functools
import inspect
from typing import Callable, Optional

from j_core.Runtime import Runtime


def transactional(read_only: Optional[bool | Callable] = None, rollback_only: Optional[bool] = None,
                  required: Optional[bool] = None, requires_new: Optional[bool] = None):
    """
    Use on functions to create a session AND limit the functions execution to that session.
    If used without arguments, the default will be a read_only transaction.
    The decorated method will receive the :class:`sqlalchemy.orm.Session` instance as it's first parameter

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

    def bind_read_only(func):
        def bound_read_only(self, *_args, **_kwargs):
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

    def bind_required(func):
        def bound_required(self, *_args, **_kwargs):
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

    if inspect.isfunction(read_only):
        return functools.wraps(read_only)(bind_read_only(read_only))
    else:
        def _inner(func):
            if required is True:
                return functools.wraps(func)(bind_required(func))

        return _inner
