from typing import Any, cast
from xml.etree import ElementTree

__all__ = ['ApiServerConfig', 'ClientServerConfig', 'ServerConfiguration']


class ApiServerConfig:
    def __init__(self, config: dict[str, Any]):
        self.config = config

    def get_name(self) -> str | None:
        return self.config['name'] if 'name' in self.config else None

    def get_port(self) -> int | None:
        return self.config['port'] if 'port' in self.config else None

    def is_active(self) -> bool | None:
        return self.config['active'] if 'active' in self.config else None


class ClientServerConfig:
    def __init__(self, config: dict[str, Any]):
        self.config = config

    def get_name(self) -> str | None:
        return self.config['name'] if 'name' in self.config else None

    def get_port(self) -> int | None:
        return self.config['port'] if 'port' in self.config else None

    def get_directory(self) -> str | None:
        return self.config['dir'] if 'dir' in self.config else None

    def is_active(self) -> bool | None:
        return self.config['active'] if 'active' in self.config else None


class ServerConfiguration:
    def __init__(self, config_path: str):

        if config_path is None:
            raise FileNotFoundError('ServerConfiguration config_path is missing!')

        self.config_path = config_path
        self.api_server_list: dict[str, ApiServerConfig] = {}
        self.client_server_list: dict[str, ClientServerConfig] = {}

        root = ElementTree.parse('server.xml').getroot()

        # define api servers
        api_tag_list = root.findall('ApiServer')
        for api_tag in api_tag_list:
            name = str(api_tag.get('name'))
            port = None
            if api_tag.get('port') is not None:
                port = cast(int, api_tag.get('port'))
            api_config = {
                'name': name,
                'port': port,
                'active': str(api_tag.get('active')).lower() == 'true'
            }
            self.api_server_list[name] = ApiServerConfig(api_config)

        # define client servers
        client_tag_list = root.findall('ClientServer')
        for client_tag in client_tag_list:
            name = str(client_tag.get('name'))
            port = None
            if client_tag.get('port') is not None:
                port = cast(int, client_tag.get('port'))
            client_config = {
                'name': name,
                'port': port,
                'dir': str(client_tag.get('dir')),
                'active': str(client_tag.get('active')).lower() == 'true'
            }
            self.client_server_list[name] = ClientServerConfig(client_config)

    def get_api_server(self, name: str) -> ApiServerConfig:
        return self.api_server_list[name]

    def get_client_server(self, name: str) -> ClientServerConfig:
        return self.client_server_list[name]
