import unittest
from unittest import SkipTest

from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_sync_app.tc_syncutil_methods import SyncUtilMethods


class LogiSyncUtil(UIBase):
    """
    Contains all the LogiSyncUtil related test cases
    """
    sync_util_methods = SyncUtilMethods()

    def test_2401_VC_69041_meetup_logisyncutil(self):
        '''
        Tests logisyncutil commands for meetup device
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_util_methods.tc_logisyncutil_rs_commands(device_name="MeetUp")

    def test_2402_VC_69040_rally_camera_logisyncutil(self):
        '''
        Tests logisyncutil commands for rally camera
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_util_methods.tc_logisyncutil_rs_commands(device_name="Rally Camera")

    def test_2403_VC_69039_rally_logisyncutil(self):
        '''
        Tests logisyncutil commands for rally system
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_util_methods.tc_logisyncutil_rs_commands(device_name="Rally")

    def test_2404_VC_69038_rally_bar_logisyncutil(self):
        '''
        Tests logisyncutil commands for rally bar
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_util_methods.tc_logisyncutil_rs_commands(device_name="Rally Bar")

    def test_2405_VC_69036_rally_bar_mini_logisyncutil(self):
        '''
        Tests logisyncutil commands for rally bar mini
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        self.sync_util_methods.tc_logisyncutil_rs_commands(device_name="Rally Bar Mini")

    def test_2406_VC_67035_help_logisyncutil(self):
        '''
        Tests logisyncutil help command
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        verification_list = ["-h", "-gd", "-gv", "-cu", "-ud",
                             "SUPPORTED DEVICES: {RALLY_BAR, RALLY_BAR_MINI, SIGHT, HUDDLE, MEETUP2, RALLY_BAR_NR}",
                             "RightSight commands",
                             "SUPPORTED DEVICES: {RALLY_BAR, RALLY_BAR_MINI, HUDDLE, MEETUP, RALLY, RALLY_CAMERA, "
                             "MEETUP2, RALLY_BAR_NR}"]
        option = "-h"
        self.sync_util_methods.tc_logisyncutil_commands(option, verification_list)

    def test_2407_VC_67041_invalid_command_logisyncutil(self):
        '''
        Tests command output when a command is invalid
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        verification_list = ["Result: 7 - Invalid command"]
        option = "-gu"
        self.sync_util_methods.tc_logisyncutil_commands(option, verification_list)

    def test_2408_VC_71103_unsupported_device_logisyncutil(self):
        '''
        Tests command output when a device name is unsupported or missing
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        verification_list = ["Result: 100 - Unsupported device or invalid device name."]
        option = "-rs-on"
        self.sync_util_methods.tc_logisyncutil_commands(option, verification_list)

    def test_2409_VC_67043_device_not_found_logisyncutil(self):
        '''
        Tests command output when a device is disconnected
        '''
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        verification_list = ["Result: 101 - Device not found."]
        option = "-rs-on"
        device = "RALLY_BAR"
        self.sync_util_methods.tc_logisyncutil_commands(option, verification_list, device)


if __name__ == "__main__":
    unittest.main()
