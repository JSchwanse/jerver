from jerver.service.ServiceInterface import serviceinterface
from jerver.service.crud import CoreCRUDService
from tests.crud.AnyTestBusinessObject import AnyTestBusinessObject

SERVICE_NAME = '/service/TestBusinessObjectCRUDService'


@serviceinterface(name=SERVICE_NAME)
class AnyTestBusinessObjectCRUDService(CoreCRUDService[AnyTestBusinessObject]):
    pass
