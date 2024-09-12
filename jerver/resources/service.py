import inspect
import json
from typing import Any

from flask import request, abort
from marshmallow import Schema, fields
from sqlalchemy.orm import Session

from jerver.resources.base_resource import BaseResource
from jerver.service.ServiceInterface import Registry

__all__ = ['Service']


class Service(BaseResource):
    class ServiceCallSchema(Schema):
        servicecall = fields.String(required=False)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.schema = Service.ServiceCallSchema()

    def extract_args_from_request_data(self, service_method: Any, data: bytes) -> dict[str, Any]:
        service_method_signature = inspect.signature(service_method)
        dict_data = json.loads(data)
        # extract those arguments from data which reflect a method argument and parse it into a dict
        arg_data = {}
        for parameter in service_method_signature.parameters:
            if parameter in ['self', 'session']:  # hard exclude
                continue
            if dict_data.get(parameter) is not None:
                arg_data[parameter] = dict_data.get(parameter)

        return arg_data

    def call_service(self, servicecall: str, *args: Any, **kwargs: Any) -> Any:
        # extract service and method name and resolve the service
        service_name = servicecall.split('.')[0]
        method_name = servicecall.split('.')[1]

        service_interface = Registry.get(f'/service/{service_name}')
        if service_interface is None:
            # TODO: may be possible due to lazy loading: try to find and load the service
            print('Service not found... too bad!')
            return None
        service = service_interface.cls
        if service is None:
            # TODO: may be possible due to lazy loading: try to find and load the service
            print('Service not found... too bad!')
            return None

        # get and call the method
        service_method = getattr(service, method_name)
        if service_method is not None:
            arg_data = self.extract_args_from_request_data(service_method, request.data)
            return service_method(service, *args, **arg_data)

    def do_get(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        if errors := self.schema.validate(request.args):
            abort(400, str(errors))
        # load users from db, whose username equals the passed name
        # return session.query(BUser).filter(BUser.username == kwargs.get('username')).one()
        return self.call_service(kwargs.pop('servicecall'), *args, **kwargs)

    def do_post(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        if errors := self.schema.validate(request.args):
            abort(400, str(errors))
        return self.call_service(kwargs.pop('servicecall'), *args, **kwargs)

    def do_put(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass

    def do_delete(self, *args: Any, session: Session, **kwargs: Any) -> Any:
        pass
