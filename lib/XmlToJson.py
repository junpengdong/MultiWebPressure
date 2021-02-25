import json
import xmltojson
from core import ApiRequest

__all__ = 'ServerHost',


class ServerHost:

    def __init__(self):
        self.__server_dict = {}
        api_request = ApiRequest()
        response = api_request.get('http://192.168.2.206:8761/eureka/apps')
        json_str = xmltojson.parse(response.content)
        json_obj = json.loads(json_str).get('applications').get('application')
        for data in json_obj:
            server_name = data.get('name').lower()
            instance_obj = data.get('instance')
            if isinstance(instance_obj, dict):
                ip = instance_obj.get('ipAddr')
                port = instance_obj.get('port').get('#text')
            else:
                ip = instance_obj[0].get('ipAddr')
                port = instance_obj[0].get('port').get('#text')
            self.__server_dict[server_name] = 'http://' + ip + ':' + str(port)

    def get_host(self, server):
        return self.__server_dict.get(server.lower())
