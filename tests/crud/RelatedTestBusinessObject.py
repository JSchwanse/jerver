from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from j_core.businessobject import businessobject
from j_core.businessobject.BusinessObject import BusinessObject, Base

BUSINESS_OBJECT_NAME: str = '/bo/RelatedTestBusinessObject'


@businessobject(name=BUSINESS_OBJECT_NAME)
class RelatedTestBusinessObject(BusinessObject, Base):
    __tablename__ = 'RelatedTestBusinessObject'

    strfield: Mapped[str] = mapped_column(String(20))
