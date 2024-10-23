import inspect
import json
from typing import Any, Callable

from flask import request, abort
from marshmallow import Schema, fields

from jerver.exceptions import EndpointNotFoundException
from jerver.resources import BaseResource
from jerver.service.ServiceInterface import Registry, SERVICE_PREFIX

__all__ = ['Service']


def extract_method_arguments(service_method: Callable[..., Any], data: bytes) -> dict[str, Any]:
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


def call_service(servicecall: str, *args: Any, **kwargs: Any) -> Any:
    # extract service and method name and resolve the service
    service_name = servicecall.split('.')[0]
    method_name = servicecall.split('.')[1]

    # resolve service interface
    endpoint_name = f'{SERVICE_PREFIX}{service_name}'
    service_interface = Registry.resolve(endpoint_name)
    if service_interface is None:
        raise EndpointNotFoundException(f'Could not find service endpoint: "{endpoint_name}"')
    service = service_interface.cls
    if service is None:
        raise EndpointNotFoundException(f'Service interface "{endpoint_name}" is missing its class definition!')

    # get and call the method
    service_method: Callable[..., Any] = getattr(service, method_name)
    if service_method is not None:
        arg_data = extract_method_arguments(service_method, request.data)
        return service_method(service, *args, **arg_data)


class Service(BaseResource):
    class ServiceCallSchema(Schema):
        servicecall = fields.String(required=False)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.schema = Service.ServiceCallSchema()

    def get(self, *args: Any, **kwargs: Any) -> Any:
        if errors := self.schema.validate(request.args):
            abort(400, str(errors))
        try:
            return call_service(kwargs.pop('servicecall'), *args, **kwargs)
        except EndpointNotFoundException as e:
            return {'exception': e}, 404
        except Exception as e:
            return {'exception': e}, 500

    def post(self, *args: Any, **kwargs: Any) -> Any:
        if errors := self.schema.validate(request.args):
            abort(400, str(errors))
        try:
            return call_service(kwargs.pop('servicecall'), *args, **kwargs)
        except EndpointNotFoundException as e:
            return {'exception': e}, 404
        except Exception as e:
            return {'exception': e}, 500

    def put(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        pass
