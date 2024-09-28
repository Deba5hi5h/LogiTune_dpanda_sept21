import base64
import json
import os
import shutil
import sys

import boto3

from common.aws_s3_utils import AwsS3Utils
from common.aws_wrappers import Boto3Wrapper
from common.json_helper import JsonHelper
from common.json_helper import Struct

S3_BUCKET = 'qa-auto-repo'
ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT_PATH, "config", "config_files")

class AWSHelper():

    @staticmethod
    def get_config(env: str) -> Struct:
        """
        Method to get config. Checks for env.json file in /config/config_files folder.
        If the json file not found, downloads the encrypted env.txt file from qa-auto-repo/config
        Decrypts env.txt to env.json

        :param env: Name of sync portal environment
        :return Struct containing URL, email, password
        """
        config_json_path = f'{CONFIG_PATH}/{env}.json'
        config_key_path = f'{CONFIG_PATH}/{env}.txt'
        if os.path.isfile(config_json_path):
            print(f'Config Json for {env} already downloaded')
            return JsonHelper.convert_json_file_to_struct(json_file_path=config_json_path)
        # elif os.path.isfile(config_key_path):
        #     config_file = config_key_path
        else:
            config_file = AWSHelper.get_config_file_from_s3(env=env)

        if os.path.isfile(config_file):
            with open(config_file, 'r') as config_data:
                contents = config_data.read()
            result = base64.decodebytes(contents.encode('utf-8')).decode('utf-8')
            result = result.replace("\'", "\"")
            value = json.loads(result)
            original_stdout = sys.stdout
            with open(config_json_path, 'w') as json_file:
                sys.stdout = json_file
                print(json.dumps(value, indent=4))
                sys.stdout = original_stdout
                os.remove(config_file)
            return JsonHelper.convert_json_file_to_struct(json_file_path=config_json_path)

    @staticmethod
    def get_json_config(env: str, force_download: bool = False) -> dict:
        """
        Method to get json config. Checks for env.json file in /config/config_files folder.
        If the json file not found, downloads the encrypted env.txt file from qa-auto-repo/config
        Decrypts env.txt to env.json

        :param env: Name of sync portal environment
        :return dict
        """
        config_json_path = f'{CONFIG_PATH}/{env}.json'
        if os.path.isfile(config_json_path) and not force_download:
            print(f'Config Json for {env} already downloaded')
            with open(config_json_path, 'r') as json_file:
                return json.load(json_file)
        else:
            config_file = AWSHelper.get_config_file_from_s3(env=env)

        if os.path.isfile(config_file):
            with open(config_file, 'r') as config_data:
                contents = config_data.read()
            result = base64.decodebytes(contents.encode('utf-8')).decode('utf-8')
            result = result.replace("\'", "\"")
            value = json.loads(result)
            original_stdout = sys.stdout
            with open(config_json_path, 'w') as json_file:
                sys.stdout = json_file
                print(json.dumps(value, indent=4))
                sys.stdout = original_stdout
                os.remove(config_file)
            with open(config_json_path, 'r') as json_file:
                return json.load(json_file)

    @staticmethod
    def get_config_file_from_s3(env: str) -> str:
        """
        Method to download the encrypted env.txt file from qa-auto-repo/config
        Decrypts env.txt to env.json

        :param env: Name of sync portal environment
        :return str: Containing the encrypted json file
        """
        folder = 'config'
        file_name = f'{env}.txt'
        download_path = f'{S3_BUCKET}/{folder}/{file_name}'
        destination_path = CONFIG_PATH
        config_file = AWSHelper._download_file_from_s3(download_path=download_path, destination_path=destination_path)
        if os.path.isfile(config_file):
            return config_file
        else:
            print(f"Unable to get config file for {env}")
            return ''

    @staticmethod
    def _download_file_from_s3(download_path: str, destination_path: str) -> str:
        """
        Method to download file from S3 bucket

        :param download_path: Full Path of file in S3 bucket to download
        :param destination_path: Path of local computer where file will be downloaded
        :return str: Containing the full path of the downloaded file on local computer
        """
        file_name = os.path.basename(download_path)
        try:
            awsutils = AwsS3Utils()
            awsutils.download_from_S3(download_path, destination=destination_path)
        except Exception as e:
            print(str(e))
        return f"{destination_path}/{file_name}"

    @staticmethod
    def upload_encrypted_json(env: str):
        """
        Method to convert env.json file to encrypted env.txt file and upload to qa-auto-repo/config S3 bucket
        env.json should be placed in /config/config_files folder

        :param env: Name of json file to be uploaded
        :return None
        """
        json_file_path = f'{CONFIG_PATH}/{env}.json'
        json_encrypt_path = f'{CONFIG_PATH}/{env}.txt'
        json_file = open(json_file_path, 'r')
        value = json.load(json_file)
        if type(value) not in [dict, str]:
            raise Exception('Invalid input format. Supported only dict and string for now')

        if isinstance(value, dict):
            value = json.dumps(value)

        data = base64.b64encode(value.encode('utf-8')).decode('utf-8')

        with open(json_encrypt_path, 'w') as encrypt_file:
            encrypt_file.write(data)

        aws_wrappers = Boto3Wrapper()
        # client = aws_wrappers.init_boto_client('s3')
        s3 = boto3.resource('s3')
        BUCKET = "qa-auto-repo"

        s3.Bucket(BUCKET).upload_file(json_encrypt_path, f"config/{env}.txt")
        os.remove(json_encrypt_path)

if __name__ == '__main__':
    aws = AWSHelper()
    aws.upload_encrypted_json('coily_end_users_v2')
