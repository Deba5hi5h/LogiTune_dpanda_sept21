import subprocess

from typing import List

from apps.sync.sync_app_methods import SyncAppMethods
from base import base_settings
from base.base_ui import UIBase
from common.usb_switch import *


class SyncUtilMethods(UIBase):
    """LogiSyncUtil related methods and tests

    Attributes:
        device_name : Name of the meeting room camera
    """
    sync_app = SyncAppMethods()
    device_name = None

    def tc_logisyncutil_commands(self, option: str, verification_list: List[str], device: str = None) -> None:
        """
        Method to execute miscellaneous commands and validation messages
        :param:
        option : command line option
        verification_list : list of strings in expected output
        device : Name of the meeting room camera
        """
        disconnect_all()
        try:
            cmd_out = self.execute_cmd(option, device)
        except subprocess.CalledProcessError as e:
            cmd_out = e.output
            Report.logInfo(cmd_out)
        self.verify_output(verification_list, cmd_out, "-h")

    def tc_logisyncutil_rs_commands(self, device_name: str) -> None:
        """
        Method to execute right sight logisyncutil command line options for the given device
        -gd, -rs-off, -rs-on, -rs-ocs, -rs-dynamic
        :param:
                device_name: Name of the meeting room camera
                mapping : MeetUp - MEETUP ; Rally - RALLY ; Rally Camera - RALLY_CAMERA;
                Rally Bar - RALLY_BAR ; Rally Bar Mini - RALLY_BAR_MINI
        """
        # Execute -gd command
        disconnect_all()
        self.sync_app.open()
        self.sync_app.add_device(device_name=device_name)
        time.sleep(3)
        option = "-gd"
        cmd_out = self.execute_cmd(option, device_name.replace(" ", '_').upper())
        verification_list = ["Device: " + device_name.replace(" ", '_').upper(), "RightSight state:",
                             "Result: 0 - No Error."]
        self.verify_output(verification_list, cmd_out, option, device_name)
        time.sleep(3)

        # Execute -rs-ocs command
        self.sync_app.home.click_device_camera(device_name=device_name)
        option = "-rs-ocs"
        cmd_out = self.execute_cmd(option, device_name.replace(" ", '_').upper())
        verification_list = ["Result: 0 - No Error."]
        self.verify_output(verification_list, cmd_out, option, device_name)

        self.sync_app.verify_on_call_start(selected=True)
        time.sleep(3)

        # Execute -rs-dynamic command
        option = "-rs-dynamic"
        cmd_out = self.execute_cmd(option, device_name.replace(" ", '_').upper())
        verification_list = ["RightSight mode is auto.", "Result: 0 - No Error."]
        self.verify_output(verification_list, cmd_out, option, device_name)
        self.sync_app.verify_dynamic(selected=True)
        time.sleep(3)

        # Execute -rs-off command
        option = "-rs-off"
        cmd_out = self.execute_cmd(option, device_name.replace(" ", '_').upper())
        verification_list = ["RightSight is off.", "Result: 0 - No Error."]
        self.verify_output(verification_list, cmd_out, option, device_name)
        self.sync_app.verify_rightsight(enabled=False)
        time.sleep(3)

        # Execute -rs-on command
        option = "-rs-on"
        cmd_out = self.execute_cmd(option, device_name.replace(" ", '_').upper())
        verification_list = ["RightSight is on.", "Result: 0 - No Error."]
        self.verify_output(verification_list, cmd_out, option, device_name)
        self.sync_app.verify_rightsight(enabled=True)
        self.sync_app.forget_problem_device(device_name=device_name)
        self.sync_app.close()

    def execute_cmd(self, option: str, device_name: str = None) -> str:
        '''
        Method to run command and return command output.
        :param:
                option: command line option to execute
                device_name: Name of the meeting room camera
        :return: command ouput
        '''
        cmd = base_settings.SYNC_UTIL_PATH_WIN + " " + option
        if device_name is not None:
            cmd = cmd + " " + device_name.replace(" ", '_').upper()
        cmd_out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
        print(cmd_out)
        return cmd_out

    def verify_output(self, verification_list: List[str], cmd_out: str, option: str, device: str = None) -> None:
        """
        Method to verify if the expected output is present in the text file
        :param:
                verification_list: list of strings in expected output
                cmd_out: output from the executed command
                option : command line option
                device: Name of the meeting room camera
        :return: None
        """
        for item in verification_list:
            if item not in cmd_out:
                Report.logFail("LogiSyncUtil" + option + " " + "device" + " command output is incorrect. "
                               + item + " is not found in: " + cmd_out)
                return
            Report.logInfo("LogiSyncUtil Option " + option + ": Found -- " + item)
        if device is not None:
            Report.logPass("LogiSyncUtil " + option + " command is successful for the device, " + device +
                           ". Output contains ---- " + ' ; '.join(verification_list), True)
        else:
            Report.logPass("LogiSyncUtil " + option + " command is successful " +
                           ". Output contains ---- " + ' ; '.join(verification_list), True)
