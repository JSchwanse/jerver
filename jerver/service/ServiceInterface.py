from jerver.inject import injectable


class ServiceInterface[CLS]:
    """ Meta data for a client-callable backend service """

    CLS_TYPE: type[CLS]

    def __init__(self, cls: CLS, name: str):
        self.cls = cls
        self.name = name


Registry: dict[str, ServiceInterface] = {}


def serviceinterface(name: str):
    """
    Use as decorator to include a class in the registry.
    Each entry in the registry is registered as an api endpoint,
    thus this should only be used for client-callable endpoints
    """

    def _serviceinterface(cls):
        service_interface = ServiceInterface(cls, name)
        service_interface.CLS_TYPE = cls
        Registry[name] = service_interface
        injectable(cls)
        return cls

    return _serviceinterface
