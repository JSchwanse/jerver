from flask_restful import Resource
from j_core.Runtime import Runtime
from j_core.businessobject.BusinessObject import BusinessObject
from sqlalchemy.orm.exc import NoResultFound


class BaseResource(Resource):

    def get(self, *args, **kwargs):
        session = Runtime.Session()
        try:
            result = self.do_get(*args, session=session, **kwargs)
            session.commit()
            return result.to_dictionary(), 200
        except NoResultFound:
            session.rollback()
            return self.__class__.__name__ + ' not found', 404
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def post(self, *args, **kwargs):
        session = Runtime.Session()
        try:
            result = self.do_post(*args, session=session, **kwargs)
            session.commit()
            return result, 200
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def put(self, *args, **kwargs):
        session = Runtime.Session()
        try:
            self.do_put(*args, session=session, **kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, *args, **kwargs):
        session = Runtime.Session()
        try:
            self.do_delete(*args, session=session, **kwargs)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def do_get(self, *args, session, **kwargs) -> BusinessObject:
        pass

    def do_post(self, *args, session, **kwargs):
        pass

    def do_put(self, *args, session, **kwargs):
        pass

    def do_delete(self, *args, session, **kwargs):
        pass
