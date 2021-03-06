import os
import json
import random

__all__ = 'ApiRequestData',


class ApiRequestData:

    def __init__(self, s, c, f):
        self.__server = s
        self.__controller = c
        self.__function = f
        self.__filter_params()
        self.__host_json = 'Server.json'
        self.__api_key = 'api'
        self.__request_type_key = 'request_type'
        self.__host_key = 'host'
        self.__params_method_key = 'params_method'
        self.__body_params_key = 'body_params'
        self.__headers_key = 'headers'
        self.__request_number_key = 'request_number'
        self.__complete_second_key = 'complete_second'
        self.__function_key = 'function'
        self.__base_dir = '../data/request/'
        self.__base_json_dir = '../data/request/%s/'
        self.__base_json_file = '../data/request/%s/%s'
        self.__json_data_arr = self.__init_data()

    def get_api(self, json_data):
        api = json_data.get(self.__api_key)
        return api

    def get_request_type(self, json_data):
        request_type = json_data.get(self.__request_type_key)
        return request_type

    def get_params(self, json_data):
        params_method = json_data.get(self.__params_method_key)
        if params_method is not None and params_method != '':
            return self.__params_method_dispatch(params_method)
        else:
            return json_data.get(self.__body_params_key)

    def get_headers(self, json_data):
        headers = json_data.get(self.__headers_key)
        return headers

    def get_request_number(self, json_data):
        request_number = json_data.get(self.__request_number_key)
        return request_number

    def get_complete_second(self, json_data):
        complete_second = json_data.get(self.__complete_second_key)
        return complete_second

    def get_function(self, json_data):
        return json_data.get(self.__function_key)

    # 自定义生成body参数
    @staticmethod
    def __params_method_dispatch(params_method):
        if params_method == 'random_keyword':
            return ApiRequestData.__random_keyword()

    @staticmethod
    def __random_keyword():
        letter_arr = ['a', 'b', 'c', 'd', 'e', 'f']
        count = 0
        word = ''
        while count < random.randrange(1, 5):
            count = count + 1
            word = word + random.choice(letter_arr)

        return {
            'keyword': word
        }

    def __filter_params(self):
        if self.__server == 'all':
            self.__controller = 'all'
            self.__function = 'all'
        else:
            if self.__controller == 'all':
                self.__function = 'all'

    def get_json_data(self):
        return self.__json_data_arr

    def __init_data(self):
        server_dict = self.__file_names()
        data = self.__filter_controller(server_dict)
        step1_data = self.__data_handle_step1(data)
        step2_data = self.__data_handle_step2(step1_data)
        return step2_data

    def __data_handle_step1(self, data):
        step1_data = {}
        for k, v in data.items():
            host_json_path = self.__base_json_file % (k, self.__host_json)
            host_json_obj = self.__read_data(host_json_path)
            host = host_json_obj.get(self.__host_key)
            file_data_arr = []
            for file_name in v:
                file_name_path = self.__base_json_file % (k, file_name)
                file_data_obj = self.__read_data(file_name_path)
                if self.__function == 'all':
                    file_data_arr.append(file_data_obj)
                else:
                    if self.__function.__contains__(','):
                        for f in self.__function.split(','):
                            file_data = file_data_obj.get(f)
                            if file_data is not None:
                                file_data[self.__function_key] = f
                                file_data_arr.append(file_data)
                    else:
                        file_data = file_data_obj.get(self.__function)
                        if file_data is not None:
                            file_data[self.__function_key] = self.__function
                            file_data_arr.append(file_data)
            step1_data[host] = file_data_arr
        return step1_data

    def __data_handle_step2(self, step1_data):
        api_data_arr = []
        for k, v in step1_data.items():
            for obj in v:
                obj[self.__api_key] = k + obj[self.__api_key]
                api_data_arr.append(obj)
        return api_data_arr

    def __filter_controller(self, data):
        if self.__server == 'all':
            return data
        else:
            if self.__controller == 'all':
                return data
            else:
                file_name_arr = data.get(self.__server)
                for file_name in file_name_arr:
                    if not file_name.__contains__(self.__controller):
                        file_name_arr.remove(file_name)
                data[self.__server] = file_name_arr
                return data

    def __file_names(self):
        server_dict = {}
        dir_name_arr = []
        if self.__server == 'all':
            for dir_name in self.dir_names(self.__base_dir):
                dir_name_arr.append(dir_name)
        else:
            dir_name_arr.append(self.__server)

        for dir_name in dir_name_arr:
            file_name_arr = []
            dir_path = os.path.abspath(self.__base_json_dir % dir_name)
            for file_name in os.listdir(dir_path):
                if file_name == self.__host_json:
                    continue
                file_name_arr.append(file_name)
            server_dict[dir_name] = file_name_arr
        return server_dict

    @staticmethod
    def __read_data(file_path):
        with open(file_path, 'r', encoding='utf=8') as content:
            return json.load(content)

    @staticmethod
    def dir_names(base_dir):
        dir_name_arr = []
        for file in os.listdir(base_dir):
            if not os.path.isfile(os.path.join(base_dir, file)):
                dir_name_arr.append(file)
        return dir_name_arr
