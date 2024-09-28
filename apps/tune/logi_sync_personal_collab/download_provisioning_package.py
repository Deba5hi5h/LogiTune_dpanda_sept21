import logging
import os
import time
import json
from pathlib import Path
from typing import Any, Optional

import requests
import wget
from urllib3.exceptions import InsecureRequestWarning

from common import raiden_config
from common.platform_helper import get_custom_platform
from config.aws_helper import AWSHelper
from extentreport.report import Report
from base import global_variables

log = logging.getLogger(__name__)
BASE_URL = "https://sync.logitech.com/"

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DownloadProvisioningJson:
    org_id = 'hzlvTkSj3ax9EXZubDHaAT12f127ersX'  # Aladdin QA

    def __init__(self):
        self.token = self._signin_method()

    @staticmethod
    def _token_gen(token: Any) -> dict[str, str]:
        return {'Authorization': f'Bearer {token}'}

    def _send_request(self, method: str,
                      url: str,
                      body: Optional[str] = None,
                      token: Optional[str] = None,
                      params: Optional[str] = None,
                      retry: int = 3) -> dict:
        """
        Create the request and returns the response using the request library

        """
        if retry == 0:
            return Report.logException("Number of retries reached its maximum, could not send the request.")
        try:

            kwargs = dict()
            kwargs['method'] = method
            kwargs['url'] = url

            kwargs['headers'] = self._token_gen(token) if token else None
            kwargs['data'] = body if method is not 'GET' else None
            kwargs['params'] = params if method is 'GET' else None
            response = requests.request(**kwargs)
            if global_variables.reportInstance:
                Report.logRequest(f"Request data: "
                                  f"{json.dumps({k: v for k,v in kwargs.items()  if k != 'headers'}, indent=2)}")

            # Send the request
            if response.ok:
                response_json = response.json()
                if global_variables.reportInstance:
                    Report.logResponse(f"Request response data: {response_json}")
                return response_json
            else:
                Report.logInfo(f"Could not fetch data from Sync Portal, retrying... Error: {repr(response)}")
                try:
                    Report.logInfo(f"Response json: {response.json()}")
                except AttributeError:
                    pass
                self.token = self._signin_method()
                time.sleep(20)
                return self._send_request(method, url, body, self.token, params, retry-1)

        except Exception as err:
            AssertionError(f'Request Error {err}')

    def _validate_sign_in(self, response: dict) -> tuple[bool, Optional[str]]:
        """
        Validate the Token and TTL of the Signin Users response message

        """
        try:
            assert response['token'] is not None, 'Error in Token Field'
            assert response['ttl'] is not None, 'Error in TTL Field'

            if response['token']:
                Report.logPass("Token generated successfully")
            else:
                Report.logFail("Token not generated successfully")

            if response['ttl']:
                Report.logPass("TTL field occurred")
            else:
                Report.logFail("Error in TTL Field")
            return True, response['token']

        except AssertionError as e:
            log.error(f'validate_signinuser - {e}')
            return (False, None)

    def _signin_method(self) -> Optional[str]:
        """
        Signin Api - added as part of setup method in unittest case class

        """

        # Construct header
        role = 'Owner'
        _url = BASE_URL + raiden_config.SIGNIN_ENDPNT
        roles = AWSHelper.get_config('raiden-latest1')
        _data = roles.ROLES[role]['signin_payload']

        Report.logInfo(f'Sign in: {role}')

        try:
            # Send the request
            response = self._send_request(method='POST', url=_url, body=_data)

            # Validate the response
            (_status, token) = self._validate_sign_in(response)
            if _status:
                Report.logPass(f'{role} Sign-in validation passed')
                return token
            else:
                log.info(f'{role} Sign-in validation failed')
                return None
        except Exception as e:
            log.error(f'{role} - Unable to sign in with the user role')
            raise e

    def _get_provisioning_token(self) -> dict:
        try:
            provisioning_url = f'{BASE_URL}api/org/{self.org_id}/prov/{self.org_id}-host-default/completion'

            response = self._send_request(
                method='GET', url=provisioning_url, token=self.token
            )

            return response
        except Exception as e:
            log.error(f'Unable to get org id: {e}')
            raise e

    def create_provisioning_file(self) -> None:
        current_directory = os.path.dirname(__file__)
        root_path = Path(current_directory).parent

        json_dir = os.path.join(root_path, 'logi_sync_personal_collab', 'logi_sync_personal_collab_utils')

        _target = os.path.join(json_dir, 'ProvisioningToken.json')

        # Delete the target file if exists
        if os.path.exists(_target):
            os.remove(_target)

        # Your JSON data as a Python object
        data = self._get_provisioning_token()

        # Use 'with' to ensure the file is properly closed after writing
        with open(_target, 'w') as f:
            # Use json.dump to write data to a JSON file
            json.dump(data, f)


class DownloadLogiSyncPersonalCollab:

    def download_helvellyn_installer(self) -> str:
        try:
            platform = get_custom_platform()
            app_suffix = '.msi' if platform == 'windows' else '.pkg'

            current_directory = os.path.dirname(__file__)
            root_path = Path(current_directory).parent

            helvellyn_app_url = f'https://sync.logitech.com/downloads/helvellyn/LogiSyncPersonalCollab{app_suffix}'
            tune_binary = os.path.join(root_path, 'logi_sync_personal_collab', 'logi_sync_personal_collab_utils')
            if not os.path.exists(tune_binary):
                os.makedirs(tune_binary)

            _target = os.path.join(tune_binary, f"LogiSyncPersonalCollab{app_suffix}")

            retries = 3
            for attempt in range(retries):
                try:
                    # Delete the target file if exists
                    if os.path.exists(_target):
                        os.remove(_target)

                    Report.logInfo(f'Attempt {attempt + 1}: Please wait till Helvellyn App get downloads')

                    # Skipping SSL verification
                    response = requests.get(helvellyn_app_url, stream=True, verify=False)

                    if platform == 'windows':
                        wget.download(helvellyn_app_url, _target)
                    else:
                        with open(_target, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)

                    return _target

                except Exception as ex:
                    Report.logException("Attempt {attempt+1} of {retries}: Download of Helvellyn failed")
                    time.sleep(2 ** attempt)

            raise Exception("All download attempts failed")

        except Exception as ex:
            Report.logException("Download of Helvellyn failed")
            raise ex
