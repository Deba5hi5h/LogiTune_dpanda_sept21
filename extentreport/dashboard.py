import os
import time

import requests
import shutil
import json
from datetime import datetime

from base import global_variables, base_settings
from common.email_notification import EmailNotification
from common.framework_params import INSTALLER, PROJECT, SYNC_API_VERSION
from common.platform_helper import (get_cpu_vendor, get_custom_platform,
                                    get_current_system_version, get_installer_version)
from common.report_handler import (create_report_folder, upload_files_from_directory,
                                   verify_server_is_up)


class dashboardAPI():
    base_url = "https://swqa-dashboard"
    create_report_end_point = "/api/automation"

    def add_report(self, passed, failed, blocked, skipped):
        """
        Method to copy report folder to server and publish in Dashboard

        :param passed, failed, blocked, skipped
        :return none
        """
        if "API" in str(PROJECT).upper():
            server_folder = "apis"
        else:
            server_folder = "reports"
        now = datetime.now()
        installer_version = get_installer_version() if PROJECT == 'LogiTune' else INSTALLER
        folder = PROJECT + "_" + installer_version + "_" + now.strftime("%Y%m%d%H%M%S")
        platform = get_custom_platform()
        if platform == "macos":
            directory = os.getcwd() + "/netshare"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                os.system("mount_smbfs //vc-swqa:vcqa@swqa-dashboard/"+server_folder+" " + directory)
            except:
                print("already mounted")
            shutil.copytree(global_variables.reportPath, directory + "/" + folder,
                            ignore=shutil.ignore_patterns("*.zip"))
            if global_variables.dashboard_unmount:
                i = 6
                while i > 0:
                    result = os.system("umount " + directory)
                    if result == 0:
                        break
                    i -= 1
                    time.sleep(10)
        else:
            shutil.copytree(global_variables.reportPath, base_settings.DASHBOARD_FOLDER + server_folder + "\\"+ folder,
                            ignore=shutil.ignore_patterns("*.zip"))
        reportUrl = "./assets/"+server_folder+"/"+folder+"/Test_Report.html"
        system_version = get_current_system_version()
        if "FirmwareApi" in str(PROJECT):
            body = {"project": PROJECT, "app": f"{global_variables.firmware_api_device_name}_{global_variables.firmware_api_device_conn}",
                    "category": global_variables.test_category, "platform": f"{platform}-{system_version}",
                    "version": SYNC_API_VERSION, "passed": passed, "failed": failed, "blocked": blocked,
                    "skipped": skipped, "reportUrl": reportUrl}
        elif "API" in str(PROJECT).upper():
            body = {"project": PROJECT, "app": installer_version,
                    "category": global_variables.test_category, "platform": f"{platform}-{system_version}",
                    "version": SYNC_API_VERSION, "passed": passed, "failed": failed, "blocked": blocked,
                    "skipped": skipped, "reportUrl": reportUrl}
        elif "TuneMobile" in str(PROJECT):
            body = {"project": PROJECT, "app": "",
                    "category": global_variables.test_category,
                    "platform": f"{global_variables.PLATFORM_NAME}-{global_variables.PLATFORM_VERSION}",
                    "version": installer_version, "passed": passed, "failed": failed, "blocked": blocked,
                    "skipped": skipped, "reportUrl": reportUrl}
        elif "LogiTune" in str(PROJECT):
            cpu_vendor = get_cpu_vendor()
            body = {"project": PROJECT, "app": "", "platform": f"{platform}-{system_version}-{cpu_vendor}",
                    "category": global_variables.test_category, "version": installer_version, "passed": passed,
                    "failed": failed, "blocked": blocked, "skipped": skipped, "reportUrl": reportUrl}
        else:
            body = {"project": PROJECT, "app": "", "platform": f"{platform}-{system_version}",
                    "category": global_variables.test_category, "version": installer_version, "passed": passed,
                    "failed": failed, "blocked": blocked, "skipped": skipped, "reportUrl": reportUrl}

        headers = {'content-type': 'application/json'}
        response = requests.post(self.base_url + self.create_report_end_point, data=json.dumps(body), headers=headers, verify=False)
        print(response.status_code)
        if global_variables.email_flag or (global_variables.email_failed and global_variables.failed > 0):
            url = self.base_url + "/assets/" + server_folder + "/" + folder + "/Test_Report.html"
            EmailNotification.send_report_email(url=url, passed=passed, failed=failed, blocked=blocked, skipped=skipped)

    def add_tune_report(self, passed: int, failed: int, blocked: int, skipped: int) -> None:
        """
        Add Tune Report

        Args:
            passed (int): Number of test cases passed.
            failed (int): Number of test cases failed.
            blocked (int): Number of test cases blocked.
            skipped (int): Number of test cases skipped.

        Raises:
            Exception: If unable to create report folder.

        Returns:
            None

        Description:
            This method is used to add a tune report. It creates a report folder,
            uploads files from a directory in batches, and sends a POST request to create a report.
            It also sends an email notification if required.
        """
        if not verify_server_is_up():
            print(f'Problem with report server, running old tune_report method')
            self.add_report(passed, failed, blocked, skipped)
            return
        now = datetime.now()
        installer_version = get_installer_version() if PROJECT == 'LogiTune' else INSTALLER
        main_upload_folder = 'reports'
        folder = f'{PROJECT}_{installer_version}_{now.strftime("%Y%m%d%H%M%S")}'
        response = create_report_folder(main_upload_folder, folder)
        if not response.ok or response.json().get('status') != 'OK':
            raise Exception(f'Unable to create report folder: '
                            f'{response.status_code} - {response.text}')

        platform = get_custom_platform()
        report_url = f"./assets/{main_upload_folder}/{folder}/Test_Report.html"
        system_version = get_current_system_version()
        cpu_vendor = get_cpu_vendor()

        body = {
            "project": PROJECT,
            "app": "",
            "platform": f"{platform}-{system_version}-{cpu_vendor}",
            "category": global_variables.test_category,
            "version": installer_version,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "skipped": skipped,
            "reportUrl": report_url
        }

        headers = {'content-type': 'application/json'}
        response = requests.post(f'{self.base_url}{self.create_report_end_point}',
                                 data=json.dumps(body), headers=headers, verify=False)
        print(response.status_code)
        upload_files_from_directory(global_variables.reportPath, main_upload_folder, folder)
        if global_variables.email_flag or (
                global_variables.email_failed and global_variables.failed > 0):
            url = f"{self.base_url}/assets/{main_upload_folder}/{folder}/Test_Report.html"
            EmailNotification.send_report_email(url=url, passed=passed, failed=failed,
                                                blocked=blocked, skipped=skipped)
