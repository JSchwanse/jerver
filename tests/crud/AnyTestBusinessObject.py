from typing import Optional

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from j_core.businessobject import businessobject
from j_core.businessobject.BusinessObject import BusinessObject, Base
from tests.crud.RelatedTestBusinessObject import RelatedTestBusinessObject

BUSINESS_OBJECT_NAME: str = '/bo/TestBusinessObject'


@businessobject(name=BUSINESS_OBJECT_NAME)
class AnyTestBusinessObject(BusinessObject, Base):
    __tablename__ = 'TestBusinessObject'

    strfield: Mapped[str] = mapped_column(String(20))
    intfield: Mapped[int] = mapped_column(Integer())

    foreign_field: Mapped[Optional[int]] = mapped_column(ForeignKey(f'{RelatedTestBusinessObject.__tablename__}.id'))
    foreign_object: Mapped[RelatedTestBusinessObject] = relationship(uselist=False, lazy='joined',
                                                                     cascade='save-update, merge, expunge')
