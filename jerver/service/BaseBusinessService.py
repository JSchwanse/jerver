from typing import TypeVar

from j_core.businessobject.BusinessObject import BusinessObject
from jerver.service.crud import CoreCRUDService

__all__ = ['BaseBusinessService']

BUSINESS_OBJ_TYPE = TypeVar('BUSINESS_OBJ_TYPE', bound=BusinessObject)


class BaseBusinessService(CoreCRUDService[BUSINESS_OBJ_TYPE]):
    pass
