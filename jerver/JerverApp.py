import json
from json import JSONEncoder
from typing import Any

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_restful import Api

from j_core.businessobject.BusinessObject import BusinessObject
from jerver.resources import Service

__all__ = ['JSONEncoderBusinessObject', 'BusinessObjectJSONProvider', 'JerverApp']


class JSONEncoderBusinessObject(JSONEncoder):
    def default(self, o: object) -> Any:
        if isinstance(o, BusinessObject):
            return o.to_dictionary()
        return None


class BusinessObjectJSONProvider(DefaultJSONProvider):
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        if isinstance(obj, BusinessObject):
            return json.dumps(obj, **kwargs, cls=JSONEncoderBusinessObject)
        else:
            return super().dumps(obj, **kwargs)

    # def loads(self, s: str | bytes, **kwargs):
    #     return super().loads(s, **kwargs)


class JerverApp(Flask):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        # register custom json parser for business objects
        # works
        self.config['RESTFUL_JSON'] = {'cls': JSONEncoderBusinessObject}
        # worksn't :P
        # app.json_provider_class = BusinessObjectJSONProvider
        # app.json = BusinessObjectJSONProvider(app)

        # register endpoints
        api = Api(self)
        api.add_resource(Service, '/service/<path:servicecall>', endpoint='/service')
