import configparser
import json
import os
import base64
import hashlib

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError as e:
    raise Exception('Please install boto3 with AWS credentials')
import logging

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Boto3Wrapper(object):
    aws_config = configparser.ConfigParser()

    def __init__(self, aws_config_file=None):
        try:
            if aws_config_file:
                logger.info(f"Read AWS variables from aws config file: '{aws_config_file}'")
                parser = configparser.ConfigParser()
                parser.read(aws_config_file)

                self.aws_config = {
                    'default': {
                        'region': parser['default'].get('region', 'us-east-1'),
                        'aws_access_key_id': parser['default'].get('aws_access_key_id'),
                        'aws_secret_access_key': parser['default'].get('aws_secret_access_key'),
                    }
                }

                if not self.aws_config['default']['aws_access_key_id'] or not self.aws_config['default'][
                    'aws_secret_access_key']:
                    raise Exception('Config is empty')

            else:
                logger.info("Read AWS variables from aws config file: '~\.aws\credentials'")
                self.aws_config = {
                    'default': {
                        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
                        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
                        'region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
                    }
                }

        except Exception as error:
            if aws_config_file:
                logger.info(f"Failed to read from AWS config file: {aws_config_file}: {error}")
            else:
                logger.info(f"Failed to read from default AWS credentials file: '~/.aws/credentials': {error}")

    def init_boto_client(self, service, **kwargs):
        return boto3.client(
            service,
            region_name=self.aws_config['default'].get('region', 'us-east-1'),
            aws_access_key_id=self.aws_config['default']['aws_access_key_id'],
            aws_secret_access_key=self.aws_config['default']['aws_secret_access_key'],
            **kwargs
        )

    def init_boto_session(self, **kwargs):
        return boto3.Session(
            region_name=self.aws_config['default']['region'],
            aws_access_key_id=self.aws_config['default']['aws_access_key_id'],
            aws_secret_access_key=self.aws_config['default']['aws_secret_access_key'],
            **kwargs
        )


class SSMParameterStore(Boto3Wrapper):
    client = None
    prefix = None
    path_delimiter = None
    fernet_key_path = '/fernet/key'

    def __init__(self, prefix=None, aws_config_file=None, fernet_key_path=None, **client_kwargs):
        Boto3Wrapper.__init__(self, aws_config_file)
        self.client = self.init_boto_client('ssm', **client_kwargs)
        self.prefix = prefix
        self.path_delimiter = '/'

        if fernet_key_path is not None:
            self.fernet_key_path = fernet_key_path

    def update_prefix(self, prefix):
        self.prefix = prefix

    @staticmethod
    def set_env(parameter_dict, prefix=None):
        for k, v in parameter_dict.items():
            os.environ.setdefault(os.path.join(prefix, k), v)

    def _get_paginated_parameters(self, client_method, strip_path=True, **get_kwargs):
        next_token = None
        parameters = []
        while True:
            result = client_method(**get_kwargs)
            parameters += result.get('Parameters')
            next_token = result.get('NextToken')
            if next_token is None:
                break
            get_kwargs.update({'NextToken': next_token})
        return dict(self.extract_parameter(p, strip_path=strip_path) for p in parameters)

    def put_value(self, name, value, description=None, param_type='String', fernet_key=None):
        if type(value) not in [dict, str]:
            raise Exception('Invalid input format. Supported only dict and string for now')

        if isinstance(value, dict):
            value = json.dumps(value)

        data = base64.b64encode(value.encode('utf-8')).decode('utf-8')
        if fernet_key is not None:
            try:
                from cryptography.fernet import Fernet
                f = Fernet(fernet_key.encode('utf-8'))
                data = f.encrypt(value.encode('utf-8')).decode('utf-8')

                logger.debug('Using fernet key to encode string')
            except ImportError:
                raise('Cannot use fernet key as cryptography is not installed')

        return self.client.put_parameter(
            Name=os.path.join(self.prefix, name),
            Description=description or name,
            Value=data,
            Type=param_type,
            Overwrite=True,
        )

    def extract_parameter(self, parameter, strip_path=True):
        key = parameter['Name']
        if strip_path:
            key_parts = key.split(self.path_delimiter)
            key = key_parts[-1]
        value = parameter['Value']
        if parameter['Type'] == 'StringList':
            value = value.split(',')
        return (key, value)

    def get_parameter_value_as_struct(self, name, decrypt=True, strip_path=True):
        result = self.get_parameter(name, decrypt, strip_path)
        # print(result)
        return Struct(**result['value'])

    def get_parameter(self, name, decrypt=True, strip_path=True):
        result = self.client.get_parameter(Name=os.path.join(self.prefix, name), WithDecryption=decrypt)
        p = result['Parameter']
        data = self.extract_parameter(p, strip_path=strip_path)

        try:
            result = base64.decodebytes(data[1].encode('utf-8')).decode('utf-8')
        except Exception:
            try:
                from cryptography.fernet import Fernet

                fernet_key = self.get_fernet_key()
                f = Fernet(fernet_key.encode('utf-8'))
                result = f.decrypt(data[1].encode('utf-8')).decode('utf-8')
            except ImportError:
                result = data[1]
        try:
            value = json.loads(result)
        except Exception:
            value = result

        return {
            'key': data[0],
            'value': value
        }

    def update_fernet_key_path(self, fernet_key_path):
        self.fernet_key_path = fernet_key_path

    def get_fernet_key(self):
        result = self.client.get_parameter(Name=self.fernet_key_path, WithDecryption=True).get('Parameter', {}).get('Value', '')

        return base64.decodebytes(result.encode('utf-8')).decode('utf-8')

    def update_fernet_key(self, fernet_key):
        data = base64.b64encode(fernet_key.encode('utf-8')).decode('utf-8')

        return self.client.put_parameter(
            Name=self.fernet_key_path,
            Description='Fernet key',
            Value=data,
            Type='String',
            Overwrite=True,
        )

    def get_parameters(self, names, decrypt=True, strip_path=True):
        get_kwargs = dict(Names=[os.path.join(self.prefix, name) for name in names], WithDecryption=decrypt)
        return self._get_paginated_parameters(
            client_method=self.client.get_parameters,
            strip_path=strip_path,
            **get_kwargs
        )

    def get_parameters_by_path(self, path, decrypt=True, recursive=True, strip_path=True):
        get_kwargs = dict(Path=path, WithDecryption=decrypt, Recursive=recursive)
        return self._get_paginated_parameters(
            client_method=self.client.get_parameters_by_path,
            strip_path=strip_path,
            **get_kwargs
        )

    def get_parameters_with_hierarchy(self, path, decrypt=True, strip_path=True):
        """Recursively get all parameters under path, keeping the hierarchy
        as a structure of nested dictionaries.
        """
        # Get a flat dictionary
        get_kwargs = dict(Path=path, WithDecryption=decrypt, Recursive=True)
        flat = self._get_paginated_parameters(
            client_method=self.client.get_parameters_by_path,
            strip_path=False,
            **get_kwargs
        )

        # Convert to a nested dictionary and strip leading path component
        result = {}

        for key, value in flat.items():
            if strip_path:
                key = key[len(path):]
            if key and key[0] == "/":
                key = key[1:]

            leafdict = result
            key_segments = key.split("/")
            for key_segment in key_segments[:-1]:
                leafdict = leafdict.setdefault(key_segment, {})
            leafdict[key_segments[-1]] = value

        return result
