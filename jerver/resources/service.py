import inspect
import json

from flask import request, abort
from j_core.businessobject.BusinessObject import BusinessObject
from marshmallow import Schema, fields

from jerver.service.ServiceInterface import Registry
from .base_resource import BaseResource


class Service(BaseResource):
    class ServiceCallSchema(Schema):
        servicecall = fields.String(required=False)

    def __init__(self):
        super().__init__()
        self.schema = Service.ServiceCallSchema()

    def extract_args_from_request_data(self, service_method, data) -> dict:
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

    def call_service(self, servicecall: str, *args, **kwargs):
        # extract service and method name and resolve the service
        service_name = servicecall.split('.')[0]
        method_name = servicecall.split('.')[1]

        service_interface = Registry.get('/service/' + service_name)
        service = service_interface.CLS_TYPE
        if service is None:
            # TODO: may be possible due to lazy loading: try to find and load the service
            print('Service not found... too bad!')

        # get and call the method
        service_method = getattr(service, method_name)
        if service_method is not None:
            arg_data = self.extract_args_from_request_data(service_method, request.data)
            return service_method(service, *args, **arg_data)

    def do_get(self, *args, session, **kwargs) -> BusinessObject:
        errors = self.schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        # load users from db, whose username equals the passed name
        # return session.query(BUser).filter(BUser.username == kwargs.get('username')).one()
        return None

    def do_post(self, *args, session, **kwargs):
        errors = self.schema.validate(request.args)
        if errors:
            abort(400, str(errors))
        return self.call_service(kwargs.pop('servicecall'), *args, **kwargs)

    def do_put(self, *args, session, **kwargs):
        pass

    def do_delete(self, *args, session, **kwargs):
        pass
