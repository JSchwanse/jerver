from abc import abstractmethod
from typing import Tuple, Any

from sqlalchemy.orm import Session

from j_core.Runtime import Runtime
from jerver.resources import BaseResource


class SessionResource(BaseResource):

    def get(self, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Tuple[Any, int]:
        session = Runtime.Session()
        try:
            result = self.do_get(session, *args, **kwargs)
            session.commit()
            return result.to_dictionary(), 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def post(self, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Tuple[Any, int]:
        session = Runtime.Session()
        try:
            result = self.do_post(session, *args, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def put(self, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Tuple[Any, int]:
        session = Runtime.Session()
        try:
            result = self.do_put(session, *args, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Tuple[Any, int]:
        session = Runtime.Session()
        try:
            result = self.do_delete(session, *args, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @abstractmethod
    def do_get(self, session: Session, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Any:
        # do something with the session
        pass

    @abstractmethod
    def do_post(self, session: Session, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Any:
        # do something with the session
        pass

    @abstractmethod
    def do_put(self, session: Session, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Any:
        # do something with the session
        pass

    @abstractmethod
    def do_delete(self, session: Session, *args: BaseResource.P.args, **kwargs: BaseResource.P.kwargs) -> Any:
        # do something with the session
        pass
