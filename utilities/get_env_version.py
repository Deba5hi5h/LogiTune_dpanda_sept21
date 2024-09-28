import logging
import os
import unittest
import re
from subprocess import check_output

from apps.tune.helpers import return_valid_windows_logi_tune_path
from apps.tune.TuneElectron import TuneElectron, disconnect_all, connect_device, disconnect_device
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class GetEnvironment(UIBase):
    """
    This class is created to get environment information (os version, tune version, headsets firmware) for the dashboard of allure report
    The result will be saved in result/environment.properties
    You can see the result on the right-bottom of https://docs.qameta.io/allure/images/tab_overview.png
    The following is an example of using this suite in Jenkins pipeline
    ```python
    stage('Allure report generate') {
        dir('vc-cloud-apps-automation-e2e') {
            catchError(buildResult:'SUCCESS',stageResult:'FAILURE')
            {
                if(params.node_name == 'Windows'){
                    bat 'pytest utilities\\get_env_version.py'
                }
                else if(params.node_name == 'macOS'){
                    sh 'pytest utilities/get_env_version.py'
                }
            }
            script{
                allure includeProperties: false, jdk: '', report: 'report', results: [[path: 'result']]
            }
        }
    }
    ```
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        setUpClass:
        1. Disconnect all devices on USB hub to avoid headset connect to dongle
        2. Check if result folder is existed
        """
        try:
            super(GetEnvironment, cls).setUpClass()

            # Disconnect all USB devices before tests
            disconnect_all()

            os.chdir(directory)
            if not os.path.isdir("result"):
                os.mkdir("result")
            os.chdir("result")

            if os.path.isfile("environment.properties"):
                os.remove("environment.properties")
                if os.path.isfile("environment.properties"):
                    print("file is not remove")
                else:
                    print("file is removed")

        except Exception as e:
            Report.logException('Unable to setUp test_get_env')
            raise e

    @classmethod
    def tearDownClass(cls) -> None:
        """
        tearDown: Closing USB communication
        """
        disconnect_all()

        super(GetEnvironment, cls).tearDownClass()

    def test_001_VC_get_env(self):
        """
        This part is used to get OS version
        """
        # 1. Get OS version
        try:
            if get_custom_platform() == "windows":
                batcmd = "systeminfo"
                result = check_output(batcmd, shell=True)
                result = result.decode("utf-8")
                result = re.search(r'\bMicrosoft Windows \d+ \S+', result)
                with open("environment.properties", "a") as f:
                    f.write("platform=" + str(result.group()) + "\n")

            # MacOS
            else:
                shcmd = "sw_vers"
                result = check_output(shcmd, shell=True)
                result = result.decode("utf-8")
                result = re.search(r"\d+\.\d+", result)
                with open("environment.properties", "a") as f:
                    f.write("platform=" + str("macOS") + str(result.group()) + "\n")

        except Exception as e:
            Report.logException(str(e))

    def test_002_VC_get_tune_ver(self):
        """
        This script is used to get Tune version
        """
        # 2. Get LogiTune version
        try:
            if get_custom_platform() == "windows":
                tune_path = os.path.join(return_valid_windows_logi_tune_path(), 'LogiTune.exe')
                batcmd = f"wmic datafile where 'name=\"{tune_path}\"' get version"
                result = check_output(batcmd, shell=True)
                result = result.decode("utf-8")
                result = re.search(r"\d+\.\d+\.\d+\.\d+", result)
                with open("environment.properties", "a") as f:
                    f.write("Tune_version="+str(result.group())+"\n")

            # MacOS
            else:
                shcmd = "system_profiler SPApplicationsDataType |grep 'LogiTune' -A 4"
                result = check_output(shcmd, shell=True)
                result = result.decode("utf-8")
                result = re.search(r"\d+\.\d+\.\d+", result)
                with open("environment.properties", "a") as f:
                    f.write("Tune_version="+str(result.group())+"\n")

        except Exception as e:
            Report.logException(str(e))

    def test_003_VC_get_all_headsets_ver(self):
        """
        This script is used to get all headsets' version
        """
        # 3. Get all headsets' version
        try:
            headset_list = [
                "Zone Wired Earbuds",
                "Zone 900",
                "Zone 750",
                "Zone True Wireless",
                "Zone Wireless",
                "Zone Wireless Plus",
                "Zone Vibe 125",
                "Zone Vibe 130",
                "Zone Vibe Wireless",
                "Zone Wired",
                "Zone Wireless 2"
            ]  # Zone 950 are waited to be added.

            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()

            # Scan port one by one
            for i in range(len(headset_list)):
                device_name = headset_list[i]
                connect_device(device_name)
                is_device_connected = self.tunesApp.check_is_device_connected(device_name)
                print("connected_device_text: ", is_device_connected)
                # Check if device is on the specific port. Otherwise, continue to the next port
                if not is_device_connected:
                    Report.logInfo("Device not found, continue to the next port.")
                    continue
                version_info = self.tunesApp.check_firmware_version(device_name, skip_exception=True)
                device_fw_version = re.search(r"\d+\.\d+\.\d+", version_info)
                #  environment.properties cannot have any space. Replace space with underscore
                device_name = device_name.replace(" ", "_")
                with open("environment.properties", "a") as f:
                    f.write(str(device_name) + "=" + str(device_fw_version.group())+"\n")
                # Record receiver version if it's wireless headset
                if "Receiver" in version_info:
                    dongle_version = re.search(r"\bBT\b +\d+\.\d+\.\d+", version_info)
                    if dongle_version is not None:
                        with open("environment.properties", "a") as f:
                            f.write(str(device_name) + "_dongle" + "=" + str(dongle_version.group()) + "\n")
                    else:
                        dongle_version = re.search(r"\bSU\b +\d+\.\d+\.\d+", version_info)
                        with open("environment.properties", "a") as f:
                            f.write(str(device_name) + "_dongle" + "=" + str(dongle_version.group()) + "\n")
                disconnect_device(device_name)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GetEnvironment)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
