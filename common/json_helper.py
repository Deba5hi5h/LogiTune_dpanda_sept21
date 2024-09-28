import json
import sys
from collections import namedtuple
from functools import reduce
from operator import getitem


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class JsonHelper:

    @staticmethod
    def convert_json_data_to_struct(json_data: str) -> Struct:
        """
        Method to convert json string data to Struct data

        :param json_data: as string
        :return Struct
        """
        try:
            value = json.loads(json_data)
            return Struct(**value)
        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def convert_json_file_to_struct(json_file_path: str) -> Struct:
        """
        Method to extract data from json file and convert to Struct data

        :param json_file_path: Full path of json file to be converted to Struct
        :return Struct
        """
        try:
            json_file = open(json_file_path, 'r')
            json_data = json.load(json_file)
            json_file.close()
            # string_data = json.dumps(json_data)
            # return json.loads(string_data, object_hook=JsonHelper._custom_decoder)
            return Struct(**json_data)
        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def _custom_decoder(json_dict):
        return namedtuple('X', json_dict.keys())(*json_dict.values())

    @staticmethod
    def update_json(json_file_path: str, key: str, value: str) -> None:
        """
        Method to update value in json file based key. To update the value of nested key, it should be
        hierarchy of key separated by comma

        :param json_file_path: Full path of json file to be updated
        :param key:
        :param value:

        :return None
        """
        try:
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
            key_list = key.split(',')
            d = JsonHelper._set_nested_item(json_data, key_list, value)
            with open(json_file_path, 'w') as json_file:
                json.dump(d, json_file, indent=4)
        except Exception as e:
            print(str(e))
            raise e

    @staticmethod
    def _set_nested_item(dataDict, mapList, val):
        """Set item in nested dictionary"""
        reduce(getitem, mapList[:-1], dataDict)[mapList[-1]] = val
        return dataDict

    @staticmethod
    def add_key_value_to_json(json_file_path: str, key: list, value: list) -> None:
        """
        Method to add Key and Value to json file

        :param json_file_path: Full path of json file to be updated
        :param key:
        :param value:

        :return None
        """
        if len(key) != len(value):
            print("Key value pair is not correct, and cannot be updated")
            raise Exception
        try:
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
                for i in range(0, len(key)):
                    json_data[key[i]] = value[i]
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
        except Exception as e:
            print(str(e))
            raise e