import time
import json
import requests

from abc import ABC, abstractmethod
from dataclasses import fields
from typing import Iterable, Optional


from apps.tune.device_parameters_utilities import TuneEnv
from common.aws_s3_utils import AwsS3Utils
from common.platform_helper import retry_request
from testsuite_tune_app.update_easteregg import device_parameters as dp, device_parameters_jenkins as dpj


class TuneRequests(ABC):
    _headers = {'Content-Type': 'application/json', 'X-API-KEY': ''}

    def __init__(self):
        self._get_key()

    def _get_version(self, *args: str) -> Optional[dict]:
        self._prepare_request_data(*args)
        response = self._request_version()
        return self._parse_data(response)

    @abstractmethod
    def _prepare_request_data(self, *args: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def _parse_data(response: Optional[dict]) -> dict:
        pass

    @abstractmethod
    def _request_version(self) -> Optional[dict]:
        pass

    def _get_key(self, retry: int = 0, max_retries: int = 5) -> None:
        bucket = 'qa-auto-repo'
        s3_folder = 'LogiTuneUtils/'
        file_name = 'ota_test.json'

        try:
            s3 = AwsS3Utils()
            bucket = s3.resource.Bucket(bucket)
            for obj in bucket.objects.all():
                if s3_folder in obj.key and file_name in obj.key:
                    body = obj.get()['Body'].read()
                    data = json.loads(body)
                    self._headers['X-API-KEY'] = data['key']
        except (KeyError, AttributeError) as e:
            retry += 1
            if max_retries > retry:
                time.sleep(5)
                print(f'Retrying for {retry} time')
                self._get_key(retry=retry)
            else:
                raise e(f'Cannot retrieve the key from S3 within {retry} tries')


class TuneVersionGetter(TuneRequests):
    _url_staging = "https://updates-staging.vc.logitech.com/api/files/manifest/tune/latest"
    _url_prod = "https://updates.vc.logitech.com/api/files/manifest/tune/latest"
    _params = {'channel': ''}

    def __init__(self):
        super().__init__()

    def get_tune_version_all_branches(self) -> dict:
        app = 'Logi Tune'
        output = {app: dict()}
        for branch in fields(TuneEnv):
            version = self._get_version(branch.name)
            output[app][branch.name] = version
        return output

    def _prepare_request_data(self, branch: str) -> None:
        self._params['channel'] = branch

    def _request_version(self, retry: int = 0) -> Optional[dict]:
        try:
            if self._params['channel'] == TuneEnv.prod:
                response = retry_request.get(self._url_prod, headers=self._headers, timeout=30)
            else:
                response = retry_request.get(self._url_staging, headers=self._headers,
                                             params=self._params, timeout=30)
            if response.status_code == 200:
                response = json.loads(response.text)
                return response
        except requests.exceptions.ConnectionError as cn:
            if retry < 5:
                retry += 1
                print(f'Connection error occurred when requesting device versions - retry {retry}. '
                      f'Waiting 5 seconds before next retry...')
                time.sleep(5)
                return self._request_version(retry)
            else:
                print(f'Connection error still persist after 5 retries, exiting with error.')
                raise cn
        except Exception as e:
            print(f'Unhandled error occurred when getting device versions from branches: {repr(e)}')
            raise e

    @staticmethod
    def _parse_data(response: Optional[dict]) -> dict:
        output = dict()
        if response is not None:
            output['version'] = response.get('version')
            return output


class DeviceFirmwareVersionGetter(TuneRequests):
    _url_staging = "https://updates-staging.vc.logitech.com/api/firmware/manifest/latest"
    _url_prod = "https://updates.vc.logitech.com/api/firmware/manifest/latest"
    _request_body = {
        "channel": '',
        "product": '',
        "version": "0.0.0",
        "meta": {
            "tune": {
                "appVersion": "1.55.0"
            },
            "machineId": "123",
            "os": "Win",
            "osv": "2.0000"
        }
    }

    def __init__(self, jenkins_configuration: bool = False):
        self.jenkins_configuration = jenkins_configuration
        super().__init__()

    def get_device_version_all_branches(self, device_name: str, endpoint_provided: bool = False) -> dict:
        if endpoint_provided:
            device = dp.Device(device_name, device_name, "", "", 0)
        else:
            device = self._get_device_by_name(device_name)
        output = {device.device_name: dict()}
        for branch in fields(TuneEnv):
            version = self._get_version(device.ota_api_product_name, branch.name)
            output[device.device_name][branch.name] = version
        return output

    def get_branch_all_devices_version(self, branch: str) -> dict:
        output = {branch: dict()}
        for device in self._get_devices():
            version = self._get_version(device.ota_api_product_name, branch)
            output[branch][device.device_name] = version
        return output

    @staticmethod
    def check_availability(version_data: dict, device_fw: str,
                           dongle_fw: Optional[str] = None) -> list:
        valid_branches = list()
        for data in version_data.values():
            for env, firmwares in data.items():
                if env and firmwares:
                    if device_fw not in firmwares.get('device'):
                        continue
                    if dongle_fw is not None:
                        if firmwares.get('dongle') is None:
                            continue
                        elif dongle_fw in firmwares.get('dongle'):
                            valid_branches.append(env)
                    else:
                        valid_branches.append(env)
        return valid_branches

    def _prepare_request_data(self, ota_api_product_name: str, branch: str) -> None:
        self._request_body['channel'] = branch
        self._request_body['product'] = ota_api_product_name

    def _request_version(self) -> Optional[dict]:
        if self._request_body['channel'] == TuneEnv.prod:
            self._request_body.pop('channel')
            response = retry_request.post(self._url_prod, json=self._request_body, headers=self._headers,
                                          timeout=30)
        else:
            response = retry_request.post(self._url_staging, json=self._request_body,
                                          headers=self._headers, timeout=30)
        if response.status_code == 200:
            response = json.loads(response.text)
            return response

    @staticmethod
    def _parse_data(response: Optional[dict]) -> dict:
        output = dict()
        if response is not None:
            output['device'] = response.get('ver')
            if response.get('dongle'):
                output['dongle'] = response['dongle'].get('ver')
            elif response.get('quadrun'):
                output['dongle'] = response['quadrun'].get('ver')
            return output

    def _get_device_by_name(self, device_name: str) -> dp.Device:
        for device in self._get_devices():
            if device.device_name == device_name:
                return device

    def _get_devices(self) -> Iterable[dp.Device]:
        parameters = dpj if self.jenkins_configuration else dp
        for value in parameters.__dict__.values():
            if isinstance(value, parameters.Device):
                yield value


def get_tune_version_across_branches() -> None:
    vg = TuneVersionGetter()
    results = vg.get_tune_version_all_branches()
    print(json.dumps(results, indent=2))


def get_device_fw_across_branches(device_name: str) -> None:
    vg = DeviceFirmwareVersionGetter()
    results = vg.get_device_version_all_branches(device_name)
    print(json.dumps(results, indent=2))


def get_branch_fw_across_devices(branch: str) -> None:
    vg = DeviceFirmwareVersionGetter()
    results = vg.get_branch_all_devices_version(branch)
    print(json.dumps(results, indent=2))


def get_branch_with_valid_fw_version(device_name: str, device_fw: str,
                                     receiver_fw: Optional[str]) -> list:
    vg = DeviceFirmwareVersionGetter()
    data = vg.get_device_version_all_branches(device_name)
    return vg.check_availability(data, device_fw, receiver_fw)
