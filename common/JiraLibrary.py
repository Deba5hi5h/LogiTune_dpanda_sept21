import json
import re
import time
import requests

from datetime import datetime

from base import global_variables
from base.base_settings import TEST_USER_AUTH
from common.framework_params import INSTALLER, PROJECT, SYNC_API_VERSION
from common.platform_helper import get_cpu_vendor, get_current_system_version, get_custom_platform, \
    get_installer_version
from extentreport.report import Report
from typing import List, Dict


class JiraAPI:
    base_url = "https://jira.logitech.com"  # "https://staging-jira.logitech.com"
    get_all_cycles_endpoint = "/rest/zapi/latest/cycle?projectId="
    get_issue_endpoint = "/rest/api/2/search?jql=key="
    create_cyle_endpoint = "/rest/zapi/latest/cycle"
    add_test_to_cycle_endpoint = "/rest/zapi/latest/execution/"
    execute_test_endpoint = "/rest/zapi/latest/execution/id/execute"
    execution_information_endpoint = "/rest/zapi/latest/execution?cycleId="
    get_all_projects_endpoint = "/rest/zapi/latest/util/project-list"
    get_executions_by_test = "/rest/zapi/latest/traceability/executionsByTest?testIdOrKey="
    get_folders_by_cycle = "/rest/zapi/latest/cycle/{}/folders?projectId={}&versionId={}"
    get_job_progress_endpoint = "/rest/zapi/latest/execution/jobProgress/{}"
    update_folder_endpoint = "/rest/zapi/latest/folder/{}"
    create_folder_endpoint = "/rest/zapi/latest/folder/create"
    get_all_versions_endpoint = "/rest/zapi/latest/util/versionBoard-list"
    get_all_folders_endpoint = "/rest/zapi/latest/cycle/{}/folders"
    put_folder = "/rest/zapi/latest/folder/{}"
    update_issue = "/rest/api/2/issue/{}"
    get_all_cycles_for_version = "/rest/zapi/latest/cycle?projectId={}&versionId={}"
    get_all_project_versions = "/rest/api/latest/project/{}/versions"
    get_previous_test_results = "/rest/zapi/latest/traceability/executionsByTest?testIdOrKey={}"
    delete_executions_endpoint = "/rest/zapi/latest/execution/deleteExecutions"
    resultSet = {"PASS": 1, "FAIL": 2, "WIP": 3, "BLOCKED": 4, "SKIPPED": 5}
    projectId = "15004"
    auth = TEST_USER_AUTH.split(":")

    def execute_test(self, test_name, result, comment=None):
        try:
            if global_variables.update_test_automation_field:
                self.update_test_automation_field(test_case=test_name)
                
            body = {"status": self.resultSet[result]}

            if comment:
                body["comment"] = str(comment)

            testid = self.get_testid_from_unexecuted_cycle(test_name)
            if testid == -1:
                Report.logWarning("Test Case not found in unexecuted cycle")
                return None
            endPoint = self.execute_test_endpoint.replace("id", str(testid))
            headers = {"content-type": "application/json"}
            response = requests.put(
                self.base_url + endPoint,
                data=json.dumps(body),
                headers=headers,
                auth=(self.auth[0], self.auth[1]),
                verify=False,
            )
            Report.logInfo("Test Result updated")
            return response.json()
        except Exception as e:
            Report.logWarning("Exception: Failed to update results {}".format(e))
        # print(response.text)
        # print(response.status_code)

    def update_test_automation_field(self, test_case: str):
        try:
            headers = {"content-type": "application/json"}
            body = {"fields": {"customfield_20200": {"value": "Yes"}, "customfield_20201": {"value": "Yes"}}}
            test_update_status = requests.put(
                self.base_url + self.update_issue.format(test_case),
                data=json.dumps(body),
                headers=headers,
                auth=(self.auth[0], self.auth[1]),
                verify=False,
            )
            if test_update_status.status_code == 204:
                print(f"Test case {test_case} automation fields updated successfully")
            else:
                print(f"Test case {test_case} automation field update failed")
        except Exception as e:
            print("Exception: Failed to update Automation field {}".format(e))

    def add_test_to_cycle(self, issueName, cycleName):
        issueId = self.get_issue_id(issueName)
        cycleId = self.get_cycle_id(cycleName)
        body = {
            "cycleId": cycleId,
            "priorities": "10100",
            "projectId": self.projectId,
            "versionId": "-1",
            "issueId": issueId,
        }
        headers = {"content-type": "application/json"}
        response = requests.post(
            self.base_url + self.add_test_to_cycle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        # print(response.status_code)
        resp = json.loads(response.text)
        for k in resp:
            return resp[k]["id"]
        return 0

    def create_cycle(self):
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        cycleName = "SyncApp" + INSTALLER + "_" + date_time
        body = {"name": cycleName, "description": "Automation Cycle", "projectId": self.projectId, "versionId": "-1"}
        headers = {"content-type": "application/json"}
        response = requests.post(
            self.base_url + self.create_cyle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        # print(response.status_code)
        return cycleName

    def get_testcase_id_from_cycle(self, testName, cycleName):
        cycleId = self.get_cycle_id(cycleName)
        response = requests.get(
            self.base_url + self.execution_information_endpoint + cycleId,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        resp = json.loads(response.text)
        for item in resp["executions"]:
            if item["issueKey"] == testName:
                return item["id"]
        return 0

    def get_issue_id(self, issueName):
        response = requests.get(
            self.base_url + self.get_issue_endpoint + issueName, auth=(self.auth[0], self.auth[1]), verify=False
        )
        resp = json.loads(response.text)
        try:
            return resp["issues"][0]["id"]
        except:
            return 0

    def get_cycle_id(self, cycleName):
        response = requests.get(
            self.base_url + self.get_all_cycles_endpoint + self.projectId,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        resp = json.loads(response.text)
        keys = []
        for k in resp:
            keys.append(k)
        for i in keys:
            resp2 = resp[i]
            keys2 = []
            for k in resp2:
                keys2.append(k)
            for j in keys2:
                resp3 = j
                keys3 = []
                for k in resp3:
                    keys3.append(k)
                for k in keys3:
                    try:
                        # print(resp3[k]['name'] + " id " + str(k))
                        if resp3[k]["name"] == cycleName:
                            return str(k)
                    except:
                        print("Undefined")
        return 0

    def get_project_id(self, projectName):
        response = requests.get(
            self.base_url + self.get_all_projects_endpoint, auth=(self.auth[0], self.auth[1]), verify=False
        )
        resp = json.loads(response.text)
        for item in resp["options"]:
            if item["label"] == projectName:
                return item["value"]
        return 0

    def get_testid_from_unexecuted_cycle(self, test_name):
        try:
            if get_custom_platform() == "windows":
                platform = "WIN"
            else:
                platform = "MAC"
            cpu_vendor_info = get_cpu_vendor()
            response = requests.get(
                self.base_url + self.get_executions_by_test + test_name, auth=(self.auth[0], self.auth[1]), verify=False
            )
            resp = json.loads(response.text)

            if PROJECT != "FirmwareApi":
                for execution in resp["executions"]:
                    cycle_name = execution["execution"]["testCycle"]
                    folder_name = execution["execution"].get('folderName')

                    if execution["execution"]["statusId"] == "-1" or execution["execution"]["statusId"] == "2" or \
                            execution["execution"]["statusId"] == "3":
                        if global_variables.firmware_project is not None:
                            if (
                                    INSTALLER in cycle_name
                                    and global_variables.firmware_version in cycle_name
                                    and global_variables.firmware_project[:-1] in cycle_name
                                    and global_variables.firmware_project in folder_name
                                    and get_current_system_version() in folder_name
                            ):
                                print(f"cycle_name: {cycle_name}, folder_name: {folder_name}")
                                return execution["execution"]["id"]
                        else:
                            if "API" in str(PROJECT).upper():
                                if SYNC_API_VERSION in cycle_name and platform in platform in cycle_name.upper():
                                    print(cycle_name)
                                    return execution["execution"]["id"]

                            elif "STRESS" in global_variables.test_category.upper():
                                system_under_test_version = platform + get_current_system_version()
                                if (
                                        INSTALLER in cycle_name
                                        and system_under_test_version in cycle_name.upper()
                                ):
                                    print(f"cycle_name: {cycle_name}, folder_name: {folder_name}")
                                    return execution["execution"]["id"]

                            elif "LogiTune" in PROJECT:
                                system_under_test_version = f"{platform}{get_current_system_version()}-{cpu_vendor_info}"
                                installer_version = get_installer_version()

                                if (
                                        PROJECT in cycle_name
                                        and installer_version in cycle_name
                                        and system_under_test_version.upper() in cycle_name.upper()
                                ):
                                    print(f'reported test name {test_name}')
                                    print(f"system_under_test_version: {system_under_test_version}")
                                    print(f'cycle_name: {cycle_name}')
                                    print(f'PROJECT: {PROJECT}, INSTALLER: {installer_version}')
                                    return execution["execution"]["id"]
                            elif "TuneMobile" in PROJECT:

                                if (
                                        INSTALLER in cycle_name
                                        and str(global_variables.PLATFORM_NAME).upper() in cycle_name.upper()
                                        and str(global_variables.PLATFORM_VERSION).upper() in cycle_name.upper()
                                        and folder_name.upper().endswith(global_variables.HEADSET.upper())
                                ):
                                    print(f"cycle_name: {cycle_name}, folder_name: {folder_name}")
                                    return execution["execution"]["id"]
                            elif "Hsinchu" in PROJECT:
                                execution_path = global_variables.ZEPHYR_EXECUTION_PATH
                                if (
                                        execution_path is not None
                                        and re.sub(' FW .*', '', execution_path.cycle_name) == re.sub(' FW .*', '',
                                                                                                      cycle_name)
                                        and (
                                        execution_path.folder_name is None or execution_path.folder_name == folder_name)
                                ):
                                    print(f"cycle_name: {cycle_name}, folder_name: {folder_name}")
                                    return execution["execution"]["id"]
                            else:
                                if INSTALLER in cycle_name and platform in cycle_name.upper():
                                    print(cycle_name)
                                    return execution["execution"]["id"]
                else:
                    Report.logInfo("Jira reporting: unexecuted test_id not found!")
                    return -1

            else:
                for execution in resp["executions"]:
                    if execution["execution"]["statusId"] == "-1" or execution["execution"]["statusId"] == "2":
                        cycle_name = execution["execution"]["testCycle"]
                        folder_name = execution["execution"]["folderName"]
                        if "API" in str(PROJECT).upper():
                            if (
                                    SYNC_API_VERSION in cycle_name
                                    and platform in folder_name.upper()
                                    and global_variables.firmware_api_device_conn.upper() in folder_name.upper()
                                    and global_variables.firmware_api_device_name in folder_name.upper()
                                    and get_current_system_version() in folder_name
                            ):
                                print(f"folderName: {folder_name}")
                                return execution["execution"]["id"]
                else:
                    return -1

        except Exception as e:
            Report.logWarning("Failed to send test id - {}".format(e))

    def rename_folder(self):
        headers = {"content-type": "application/json"}
        response = requests.get(
            self.base_url + self.get_all_cycles_endpoint + self.projectId,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        resp = json.loads(response.text)
        keys = []
        for k in resp:
            keys.append(k)
        for i in keys:
            resp2 = resp[i]
            keys2 = []
            for k in resp2:
                keys2.append(k)
            for j in keys2:
                resp3 = j
                keys3 = []
                for k in resp3:
                    keys3.append(k)
                for k in keys3:
                    try:
                        # print(resp3[k]['name'] + " id " + str(k))
                        if INSTALLER in resp3[k]["name"]:
                            cycle_id = k
                            version_id = resp3[k]["versionId"]
                            folder_response = requests.get(
                                self.base_url + self.get_folders_by_cycle.format(cycle_id, self.projectId, version_id),
                                auth=(self.auth[0], self.auth[1]),
                                verify=False,
                            )
                            folders = json.loads(folder_response.text)
                            for folder in folders:
                                folder_id = folder["folderId"]
                                folder_name = folder["folderName"]
                                update_name = str(folder_name).replace("Clone", "").strip()
                                body = {
                                    "folderId": folder_id,
                                    "name": update_name,
                                    "description": "",
                                    "cycleId": cycle_id,
                                    "projectId": self.projectId,
                                    "versionId": version_id,
                                }
                                folder_update = requests.put(
                                    self.base_url + self.put_folder.format(folder_id),
                                    data=json.dumps(body),
                                    headers=headers,
                                    auth=(self.auth[0], self.auth[1]),
                                    verify=False,
                                )

                    except:
                        print("Undefined")
        return 0

    def poll_job_progress(func, retries=100):
        """This is a decorator that continuously checks the progress of a job until it is completed.

        If response not a job progress, it will return the response as is.
        """

        def wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if not hasattr(response, 'json'):
                return response

            jobProgressResponse = response.json()
            if 'jobProgressToken' not in jobProgressResponse:
                Report.logWarning('response is not a job progress')
                return jobProgressResponse

            token = jobProgressResponse['jobProgressToken']

            headers = {"content-type": "application/json"}
            retry = 1
            status = {"progress": 0}
            while status["progress"] < 1:
                status = requests.get(self.base_url + self.get_job_progress_endpoint.format(token),
                                      headers=headers,
                                      auth=(self.auth[0], self.auth[1]),
                                      verify=False,
                                      ).json()

                time.sleep(0.5)
                retry += 1
                if retry > retries:
                    return None

            return status

        return wrapper

    @poll_job_progress
    def create_cycle_v2(self, cycleName, versionId="-1", clonedCycleId=None):
        body = {
            "name": cycleName,
            "description": "Automation Cycle",
            "projectId": self.projectId,
            "versionId": versionId,
            "clonedCycleId": clonedCycleId
        }

        headers = {"content-type": "application/json"}
        response = requests.post(
            self.base_url + self.create_cyle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response

    def get_execution_by_issue_key(self, issueKey, cycleId, folderId=None, versionId=None):
        """Get execution information by issue key from a cycle (required), folder (optional) and version (optional)"""
        response = requests.get(
            self.base_url + self.execution_information_endpoint + f"{cycleId}&projectId={self.projectId}&versionId={versionId}&folderId={folderId}",
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )
        resp = json.loads(response.text)
        for item in resp["executions"]:
            if item["issueKey"] == issueKey:
                return item
        return None

    def _get_all_versions(self):
        """Get all versions for a project"""
        params = {"projectId": self.projectId}
        headers = {"content-type": "application/json"}
        response = requests.get(
            self.base_url + self.get_all_versions_endpoint,
            params=params,
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response.json()

    def get_version_by_fn(self, fn):
        """Get version id by a function that returns True for the version you want"""
        all_versions_info = self._get_all_versions()
        all_versions = (all_versions_info['unreleasedVersions'] + all_versions_info['releasedVersions'])

        version_id = next(filter(fn, all_versions), {'value': None})['value']

        return version_id

    def get_cycle_by_fn(self, fn, versionId=None):
        """Get cycle info by a function that returns True for the cycle you want"""
        cycles_info = self._get_all_cycles(versionId)

        for key in cycles_info:
            if not key.isdigit():
                continue

            cycle_info = cycles_info[key]
            cycle_info['id'] = key
            if fn(cycle_info):
                return cycle_info

        return None

    def _get_all_cycles(self, version_id: int):
        """Get all cycles for a project and version"""
        response = requests.get(
            self.base_url + self.get_all_cycles_endpoint,
            params={"projectId": self.projectId, "versionId": version_id},
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response.json()

    def create_or_update_cycle(self, clonedCycleId, cycleName, versionId, is_target_cloned_cycle):
        """
        Create or update a cycle.

        Create a cycle if there is no cloned cycle in the version.
        Update the cycle if there is a cloned cycle in the version.

        :param clonedCycleId: The cycle ID to clone.
        :param cycleName: The name of the cycle to create/update.
        :param versionId: The version ID to create/update the cycle in.
        :param is_target_cloned_cycle: A function that returns True for the cycle to update.
        :return: The cycle ID of the created/updated cycle.
        """
        test_cycle = self.get_cycle_by_fn(is_target_cloned_cycle, versionId=versionId)
        if not test_cycle:
            test_cycle = self.create_cycle_v2(
                cycleName=cycleName,
                versionId=versionId,
                clonedCycleId=clonedCycleId
            )

            Report.logInfo(f"[Jira Zephyr] Cycle ID created: {test_cycle['entityId']}")
            return test_cycle['entityId']

        Report.logInfo(f"[Jira Zephyr] Cycle ID found: {test_cycle['id']}")
        return test_cycle['id']

    def update_cycle(self, cycleId, cycleName, versionId="-1"):
        """Update a cycle name"""
        body = {
            "id": cycleId,
            "versionId": versionId,
            "projectId": self.projectId,
            "name": cycleName,
        }

        headers = {"content-type": "application/json"}
        response = requests.put(
            self.base_url + self.create_cyle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response.json()

    @poll_job_progress
    def create_folder(self, cycleId, folderName, description="Folder", versionId="-1", clonedFolderId=None):
        """Create a folder in a cycle"""
        body = {
            "cloneAssignedTo": False,
            "cloneCustomFields": False,
            "cloneDefects": False,
            "cycleId": cycleId,
            "name": folderName,
            "description": description,
            "projectId": self.projectId,
            "versionId": versionId,
            "clonedFolderId": clonedFolderId
        }

        headers = {"content-type": "application/json"}
        response = requests.post(
            self.base_url + self.create_folder_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        if not clonedFolderId:
            return response.json()

        return response

    def update_folder(self, cycleId, folderId, folderName, versionId="-1"):
        """Update a folder name"""
        body = {
            "cycleId": cycleId,
            "versionId": versionId,
            "projectId": self.projectId,
            "name": folderName,
        }

        headers = {"content-type": "application/json"}
        response = requests.put(
            self.base_url + self.update_folder_endpoint.format(folderId),
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response.json()

    def _get_all_folder(self, cycleId, versionId):
        """Get all folders for a cycle and version"""
        params = {"projectId": self.projectId, "versionId": versionId}
        headers = {"content-type": "application/json"}
        response = requests.get(
            self.base_url + self.get_all_folders_endpoint.format(cycleId),
            params=params,
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        return response.json()

    def create_or_update_folder(self, folderName, cycleId, versionId, is_target_cloned_folder):
        """
        Create or update a folder.

        Create a folder if there is no cloned folder in the cycle.
        Update the folder if there is a cloned folder in the cycle.

        :param folderName: The name of the folder to create/update.
        :param cycleId: The cycle ID to create/update the folder in.
        :param versionId: The version ID to create/update the folder in.
        :param is_target_cloned_folder: A function that returns True for the folder to update.
        :return: The folder ID of the created/updated folder.
        """

        if folderName is None:
            return None

        all_folders = self._get_all_folder(cycleId=cycleId, versionId=versionId)

        folder_info = next(filter(lambda x: x['folderName'] == folderName, all_folders), None)
        if folder_info is None:
            folder_info = next(filter(is_target_cloned_folder, all_folders), None)

        if folder_info is None:
            raise Exception("target folder not found by using `is_target_cloned_folder`")

        # process default folder name 'Clone XXX' to current environment os name 'Win XXX'
        if folder_info['folderName'].startswith('Clone '):
            folder_info = self.update_folder(
                cycleId=cycleId,
                folderId=folder_info['folderId'],
                folderName=folderName,
                versionId=versionId
            )

            folder_info['folderId'] = folder_info['id']
            folder_info['folderName'] = folderName

        # clone from other folder but same type such as 'Mac XXX' to 'Win XXX'
        if folder_info['folderName'] != folderName:
            folder_info = self.create_folder(
                cycleId=cycleId,
                folderName=folderName,
                clonedFolderId=folder_info['folderId'],
                versionId=versionId
            )

            folder_info['folderId'] = folder_info['entityId']

        return folder_info['folderId']

    def get_folders_for_cycle(self, cycle, project_id, version_id):

        headers = {"content-type": "application/json"}
        response = requests.get(self.base_url +
                                self.get_folders_by_cycle.format(cycle, project_id, version_id),
                                auth=(self.auth[0], self.auth[1]),
                                verify=False)
        if response.ok:
            return response.json()
        return None

    def await_zephyr_token(self, token, cycle_name):

        headers = {"content-type": "application/json"}

        while True:
            time.sleep(1)
            response = requests.get(
                self.base_url + self.get_job_progress_endpoint.format(token),
                headers=headers,
                auth=(self.auth[0], self.auth[1]),
                verify=False)
            if response.ok:
                response_json = response.json()
                progress = response_json["progress"]
                print(f"Cloning {cycle_name} Progress: {int(progress * 100)} %")
                if progress == 1.0:
                    return response_json
            else:
                return None

    def get_version_id_by_name(self, version_name):

        headers = {"content-type": "application/json"}
        response = requests.get(
            self.base_url + self.get_all_project_versions.format(self.projectId),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False)

        if response.ok:
            version_id = next((_["id"] for _ in response.json() if _["name"] == version_name), None)
            return version_id

    def get_cycle_id_by_name(self, cycle_name, version_id):

        headers = {"content-type": "application/json"}
        response = requests.get(
            self.base_url + self.get_all_cycles_for_version.format(self.projectId, version_id),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False)

        response_json = response.json()
        # Remove last item which is count of cycles found
        response_json.popitem()

        if response.ok:
            cycle_id = next((key for key, value in response_json.items() \
                             if value["name"] == cycle_name), None)
            return cycle_id

    def clone_cycle_tune(self, source_release_folder_name, source_cycle_name, destination_release_folder_name, destination_cycle_name):

        destination_version_id = self.get_version_id_by_name(destination_release_folder_name)
        if destination_version_id is None:
            raise Exception("No Destination Version ID matched with provided name")

        # Check if cycle already exists
        destination_cycle_exists = self.get_cycle_id_by_name(destination_cycle_name, destination_version_id)
        if destination_cycle_exists:
            raise Exception(f"Destination Cycle {destination_cycle_name} already exists")

        source_version_id = self.get_version_id_by_name(source_release_folder_name)
        if source_version_id is None:
            raise Exception("No Source Version ID matched with provided name")

        source_cycle_id = self.get_cycle_id_by_name(source_cycle_name, source_version_id)
        if source_cycle_id is None:
            raise Exception("No Source Cycle ID matched with provided name and VersionId")

        headers = {"content-type": "application/json"}
        body = {
            "clonedCycleId": source_cycle_id,
            "name": destination_cycle_name,
            "projectId": self.projectId,
            "versionId": destination_version_id
        }
        response = requests.post(
            self.base_url + self.create_cyle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False)

        if not response.ok:
            raise Exception("Clone request went wrong.")
        print(f"Cloning {destination_cycle_name}")
        response_json = response.json()
        token = response_json['jobProgressToken']
        awaited_token = self.await_zephyr_token(token, destination_cycle_name)
        if awaited_token['errorMessage'] or awaited_token is None:
            raise Exception(f"During {destination_cycle_name} creating something went wrong")
        created_cycle = awaited_token.get("entityId")
        if not created_cycle:
            raise Exception(f"Cycle not created - visit"
                            f" {self.base_url + self.get_job_progress_endpoint.format(awaited_token)}")
        folders = self.get_folders_for_cycle(created_cycle, self.projectId, destination_version_id)
        if not folders:
            raise Exception("Folders in cycle not created")
        for folder in folders:
            print(f"Removing \"clone\" in folder {folders.index(folder) + 1} / {len(folders)} for cycle "
                  f"{destination_cycle_name}")
            update_name = str(folder["folderName"]).replace("Clone", "").strip()
            body = {
                "folderId": folder["folderId"],
                "name": update_name,
                "description": "",
                "cycleId": folder["cycleId"],
                "projectId": self.projectId,
                "versionId": folder["versionId"],
            }
            response = requests.put(self.base_url + self.put_folder.format(folder["folderId"]),
                                    data=json.dumps(body),
                                    headers=headers,
                                    auth=(self.auth[0], self.auth[1]),
                                    verify=False)
            if not response.ok:
                raise Exception(f"Removing \"Clone\" went wrong. {response}")
        print(f"Creating {destination_cycle_name} success")

    def tune_check_previous_results_on_platform(self, tc_id, system_platform, occurs=5):
        headers = {"content-type": "application/json"}
        auth = (self.auth[0], self.auth[1])
        response = requests.get(
            self.base_url + self.get_previous_test_results.format(tc_id),
            headers=headers,
            auth=auth,
            verify=False
        )
        if response.ok:
            try:
                response_json = response.json()
                executions = [el["execution"] for el in response_json["executions"]]
                prev_executions = [(el["testCycle"], el["status"]) for el in executions
                                   if "LogiTune" in el["testCycle"]
                                   and system_platform.upper() in el["testCycle"].upper()]
                return prev_executions[:occurs]
            except:
                return []
        else:
            return []

    def tune_check_previous_defects_on_platform(self, tc_id, system_platform, occurs=3):
        headers = {"content-type": "application/json"}
        auth = (self.auth[0], self.auth[1])
        response = requests.get(
            self.base_url + self.get_previous_test_results.format(tc_id),
            headers=headers,
            auth=auth,
            verify=False
        )
        if response.ok:
            try:
                response_json = response.json()
                executions = [el for el in response_json["executions"]]
                prev_executions_failed = [el for el in executions
                                          if "LogiTune" in el['execution']["testCycle"]
                                          and el['execution']["status"] == "FAIL"
                                          and system_platform.upper() in el['execution']["testCycle"].upper()]
                previous_defects = [el['defects'] for el in prev_executions_failed[:occurs] if el['defects']]
                return previous_defects
            except Exception as e:
                return []
        else:
            return []

    def add_sanity_tests_to_cycle(self, project_version, tests_to_add):
        parts = project_version.split('.')
        project_prefix = '.'.join(parts[:2]) + '.x'

        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        print('Get release version ID for Sanity project')
        release_name = f'Tune-{project_prefix}-Automated-Sanity'
        release_version_id = self.get_version_id_by_name(release_name)
        print(f'Release Id for release {release_name} is {release_version_id}')

        print(f'Create new cycle in Sanity release: {release_name}')
        if get_custom_platform() == "windows":
            platform = "WIN"
        else:
            platform = "MAC"
        system_under_test_version = f"{platform}{get_current_system_version()}-{get_cpu_vendor()}"
        cycle_name = f"LogiTune-{project_version}-Automated-Sanity-{system_under_test_version}-" + date_time
        body = {"name": cycle_name, "description": "Automation Cycle", "projectId": self.projectId, "versionId": release_version_id}
        headers = {"content-type": "application/json"}
        response = requests.post(
            self.base_url + self.create_cyle_endpoint,
            data=json.dumps(body),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False,
        )

        if response.status_code == 200:
            print(f'Successfully create new cycle {cycle_name}')
        else:
            print(f'Failed to create new cycle {cycle_name}')

        print(f'Add new tests to created cycle: {cycle_name}')

        data_dict = json.loads(response.text)
        cycle_id = data_dict['id']

        data = {
            "issues": tests_to_add,
            "versionId": release_version_id,  # Release (version) ID to which the cycle belongs
            "cycleId": cycle_id,
            "projectId": self.projectId
        }

        headers = {'content-type': 'application/json'}

        response = requests.post(
            self.base_url + '/rest/zapi/latest/execution/addTestsToCycle',
            data=json.dumps(data),
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False
        )

        if response.status_code == 200:
            print(f'Successfully added tests {tests_to_add} to cycle {cycle_name}')
        else:
            print(f'Failed to add new tests to cycle {cycle_name}')

    def update_test_execution(self, jira_id: str, data: dict) -> dict:

        headers = {'content-type': 'application/json'}
        execution_id = self.get_testid_from_unexecuted_cycle(jira_id)
        if execution_id == -1:
            Report.logWarning("Test Case not found in unexecuted cycle - execution edit failed")
            return {}
        response = requests.put(
            self.base_url + self.execute_test_endpoint.replace('id', str(execution_id)),
            json=data,
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            verify=False
        )
        if response.ok:
            return response.json()
        return {}

    def add_defects_to_execution(self, jira_id: str, defects: List[str]):

        json_body = dict()
        json_body['updateDefectList'] = True
        json_body['defectList'] = defects
        self.update_test_execution(jira_id=jira_id, data=json_body)

    def add_comment_to_execution(self, jira_id: str, comment: str):

        json_body = dict()
        json_body['comment'] = comment
        self.update_test_execution(jira_id=jira_id, data=json_body)

    def remove_unexecuted_folders_from_cycle(self, release_name: str, cycle_name: str) -> None:
        """
        Removes unexecuted folders from a given cycle.

        Args:
            release_name: The name of the release.
            cycle_name: The name of the cycle.

        """
        release_version_id = self.get_version_id_by_name(release_name)

        cycle_id = self.get_cycle_id_by_name(cycle_name=cycle_name, version_id=release_version_id)
        version_id = self.get_version_id_by_name(release_name)

        all_folders = self._get_all_folder(cycle_id, version_id)

        for folder in all_folders:
            if folder['totalExecutions'] == self._get_unexecuted_count_from_folder_response(folder):
                print(f'Remove folder: {folder["folderName"]}')
                self._remove_folder(folder_id=folder['folderId'], version_id=version_id, cycle_id=cycle_id)

    def _get_unexecuted_count_from_folder_response(self, data: Dict) -> int:
        """
        Args:
            data: A dictionary containing the response data received from the folder API.

        Returns:
            An integer representing the count of unexecuted items.

        Description:
            This method takes in the response data received from the folder API and returns the count of unexecuted items.
            It iterates through the list of execution summaries in the data and checks if the status name is 'UNEXECUTED'.
            If found, it returns the count of unexecuted items.

        Example usage:
            data = {
                'executionSummaries': {
                    'executionSummary': [
                        {
                            'statusName': 'UNEXECUTED',
                            'count': 10
                        },
                        {
                            'statusName': 'PASSED',
                            'count': 5
                        },
                        {
                            'statusName': 'FAILED',
                            'count': 3
                        }
                    ]
                }
            }
            unexecuted_count = _get_unexecuted_count_from_folder_response(data)
            # unexecuted_count will be 10
        """
        for item in data['executionSummaries']['executionSummary']:
            if item['statusName'] == 'UNEXECUTED':
                return item['count']

    def _remove_folder(self,
                       folder_id: int,
                       version_id: int,
                       cycle_id: int) -> None:
        """
        Removes a folder from the test management system.

        Args:
            folder_id (int): The ID of the folder to be removed.
            version_id (int): The ID of the version associated with the folder.
            cycle_id (int): The ID of the cycle associated with the folder.

        """
        headers = {"content-type": "application/json"}

        delete_url = f'{self.base_url}/rest/zapi/latest/folder/{folder_id}'
        payload = {'cycleId': cycle_id,
                   'projectId': self.projectId,
                   'versionId': version_id}

        response = requests.delete(
            delete_url,
            headers=headers,
            params=payload,
            auth=(self.auth[0], self.auth[1]),
            verify=False)

        if response.status_code == 200:
            print("Folder removed successfully")
        else:
            print("Failed to remove folder")

    def remove_empty_folders_for_every_cycle_in_release(self, release_name: str) -> None:
        """
        Remove empty folders for every cycle in release.

        Args:
            release_name (str): Name of the release.

        Returns:
            None
        """
        version_id = self.get_version_id_by_name(release_name)
        all_cycles = self._get_all_cycles(version_id=version_id)
        for cycle_id, value in all_cycles.items():
            if cycle_id != '-1' and isinstance(value, dict):
                all_folders = self._get_all_folder(cycle_id, version_id)
                for folder in all_folders:
                    if folder['totalExecutions'] == self._get_unexecuted_count_from_folder_response(folder):
                        print(f'Remove folder: {folder["folderName"]} from cycle {value["name"]}')
                        self._remove_folder(folder_id=folder['folderId'], version_id=version_id, cycle_id=cycle_id)

    def remove_unexecuted_tests_from_release(self, release_name: str) -> None:
        """
        Removes unexecuted tests from a given release.

        Args:
            release_name (str): The name of the release.

        Returns:
            None
        """
        version_id = self.get_version_id_by_name(release_name)
        all_cycles = self._get_all_cycles(version_id=version_id)
        for cycle_id, value in all_cycles.items():
            if cycle_id != '-1' and isinstance(value, dict):
                self.remove_unexecuted_tests_from_cycle(release_name=release_name, cycle_name=value["name"])

    def remove_unexecuted_tests_from_cycle(self, release_name: str, cycle_name: str) -> None:
        """
        Args:
            release_name: A string specifying the name of the release.
            cycle_name: A string specifying the name of the cycle.

        Returns:
            None

        Description:
        This method removes unexecuted tests from a specific cycle in Zephyr for Jira. It takes the release name and cycle name as input parameters. It first retrieves the version ID and cycle
        * ID based on the provided names. It then obtains all the folders within the cycle. For each folder, it retrieves the executions and checks if any tests are unexecuted. If an unexec
        *uted test is found, its ID is added to the tests_to_delete list. Finally, it calls the remove_tests_from_folder method to remove the unexecuted tests from the folder.
        """
        version_id = self.get_version_id_by_name(release_name)
        cycle_id = self.get_cycle_id_by_name(cycle_name=cycle_name, version_id=version_id)

        all_folders = self._get_all_folder(cycle_id, version_id)

        for folder in all_folders:

            headers = {"content-type": "application/json"}
            execution_url = f"{self.base_url}/rest/zapi/latest/execution?cycleId={cycle_id}&projectId={self.projectId}&versionId={version_id}&folderId={folder['folderId']}"
            response = requests.get(
                execution_url,
                headers=headers,
                auth=(self.auth[0], self.auth[1]),
                verify=False)

            if self._get_unexecuted_count_from_folder_response(folder) > 0:
                tests_to_delete = self._get_unexecuted_tests_list(response)
                self.remove_tests_from_folder(tests_to_delete)

    @staticmethod
    def _get_unexecuted_tests_list(response: dict) -> list:
        """Returns a list of test IDs that have not been executed.

        Args:
            response (dict): A dictionary containing the JSON response received from the server.

        Returns:
            list: A list of test IDs that have not been executed.
        """
        tests_to_delete = []
        for test_execution in response.json().get('executions'):
            if test_execution['executionStatus'] == '-1':
                tests_to_delete.append(test_execution["id"])
        return tests_to_delete

    def remove_tests_from_folder(self, tests_to_delete: list) -> None:
        """
        Remove tests from a folder.

        Args:
            tests_to_delete (list): A list of IDs representing the tests to be deleted.

        Returns:
            None
        """
        headers = {"content-type": "application/json"}

        delete_url = f'{self.base_url}{self.delete_executions_endpoint}'
        data = {'executions': tests_to_delete}

        response = requests.delete(
            delete_url,
            headers=headers,
            auth=(self.auth[0], self.auth[1]),
            json=data,
            verify=False)

        if response.status_code == 200:
            print("Tests removed successfully from cycle.")
        else:
            print("Failed to remove tests from cycle.")




if __name__ == "__main__":
    jira = JiraAPI()
    jira.remove_unexecuted_tests_from_release(release_name='Tune-3.6.x-Automated-Regular')
