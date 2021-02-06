import requests

__all__ = 'ApiRequest',


class ApiRequest:

    @staticmethod
    def get(url='', headers=None, params=None):
        try:
            response = requests.get(url=url, headers=headers, params=params)
            return response
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def post(url='', headers=None, params=None):
        try:
            response = requests.post(url=url, headers=headers, data=params)
            return response.elapsed.microseconds
        except Exception as e:
            print(e)
            return None
