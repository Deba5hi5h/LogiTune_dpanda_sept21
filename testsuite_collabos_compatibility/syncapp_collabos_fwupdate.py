import unittest

from apps.sync.Firmware import Firmware
from apps.sync.middleware_log import MiddlewareLog
from testsuite_sync_app.tc_methods import SyncTCMethods
from base.base_ui import UIBase
from common.usb_switch import *


class SyncAppCollabOSFWUpdate(UIBase):
    sync_methods = SyncTCMethods()
    device_name = "Rally Bar"

    def setUp(self) -> None:
        global_variables.testStatus = "Pass"
        testName = self.__getattribute__("_testMethodName")
        global_variables.reportInstance = global_variables.extent.createTest(f"{testName}_{self.device_name}",
                                                                             "Test Case Details")

    def test_201_VC_XXXX_update_device(self):
        time.sleep(5)
        self.sync_methods.tc_update_firmware(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
