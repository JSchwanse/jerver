from jerver.service.ServiceInterface import serviceinterface
from jerver.service.crud import CoreCRUDService
from tests.crud.AnyTestBusinessObject import AnyTestBusinessObject


@serviceinterface(name='TestBusinessObjectCRUDService')
class AnyTestBusinessObjectCRUDService(CoreCRUDService[AnyTestBusinessObject]):
    pass
