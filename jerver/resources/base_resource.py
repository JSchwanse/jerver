from abc import abstractmethod
from typing import Any, Tuple

from flask_restful import Resource
from sqlalchemy.orm import Session

from j_core.Runtime import Runtime
from j_core.businessobject.BusinessObject import BusinessObject
from jerver.exceptions import ElementNotFoundException

__all__ = ['BaseResource']


class BaseResource(Resource):

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def get(self, *args: Any, **kwargs: Any) -> Tuple[dict[Any, Any] | str, int]:
        session = Runtime.Session()
        try:
            result = self.do_get(*args, session=session, **kwargs)
            session.commit()
            return result.to_dictionary(), 200
        except ElementNotFoundException:
            session.rollback()
            return f'{self.__class__.__name__} not found', 404
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def post(self, *args: Any, **kwargs: Any) -> Tuple[BusinessObject, int]:
        session = Runtime.Session()
        try:
            result = self.do_post(*args, session=session, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def put(self, *args: Any, **kwargs: Any) -> Tuple[Any, int]:
        session = Runtime.Session()
        try:
            result = self.do_put(*args, session=session, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[bool, int]:
        session = Runtime.Session()
        try:
            result = self.do_delete(*args, session=session, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @abstractmethod
    def do_get(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def do_post(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def do_put(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def do_delete(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass
