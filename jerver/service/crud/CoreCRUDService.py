from typing import get_origin, get_args, TypeVar

from j_core.businessobject.BusinessObject import BusinessObject
from sqlalchemy.orm import Session

from jerver.transaction.transactional import transactional


class CoreCRUDService[BUSINESS_OBJECT_TYPE: BusinessObject]:
    BUSINESS_OBJECT_TYPE_ARG: type[BUSINESS_OBJECT_TYPE]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__orig_bases__:  # type: ignore[attr-defined]
            origin = get_origin(base)
            if origin is None or not issubclass(origin, CoreCRUDService):
                continue
            type_arg = get_args(base)[0]
            # Do not set the attribute for GENERIC subclasses!
            if not isinstance(type_arg, TypeVar):
                cls.BUSINESS_OBJECT_TYPE_ARG = type_arg
                return

    @transactional
    def get(self, session: Session, id: int) -> BUSINESS_OBJECT_TYPE:
        result: BUSINESS_OBJECT_TYPE = session.get_one(self.BUSINESS_OBJECT_TYPE_ARG, id)
        session.expunge(result)
        return result

    @transactional
    def find(self, session: Session, filter_dict) -> list[BUSINESS_OBJECT_TYPE]:
        result_list: list[BUSINESS_OBJECT_TYPE] = (
            session.query(self.BUSINESS_OBJECT_TYPE_ARG).filter_by(**filter_dict).all())
        for result in result_list:
            session.expunge(result)
        return result_list

    @transactional(required=True)
    def save(self, session: Session, data_object: BUSINESS_OBJECT_TYPE) -> BUSINESS_OBJECT_TYPE:
        session.add(data_object)
        session.commit()
        session.refresh(data_object)
        session.expunge(data_object)
        return data_object

    @transactional
    def delete(self, session: Session) -> bool:
        pass
