import os
import time
import unittest

import psutil

from apps.tune.firmware_downgrade import Firmware
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base import global_variables
from base.base_ui import UIBase
from common.framework_params import INSTALLER
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_device, connect_device
from extentreport.report import Report


class TuneProxy(UIBase):
    """
    Test class containing LogiTune Proxy tests.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()


    def test_1901_VC_XXXX_update_tune(self) -> None:
        version = INSTALLER
        self.tune_methods.tc_install_logitune(version=version)
        self.tune_methods.tc_update_logitune()

    def test_1902_VC_XXXX_firmware_update_webcam_brio(self) -> None:
        device_name = "Brio"
        connect_device(device_name=device_name)
        self.tune_app.close_tune_app()
        brio = Firmware(device_name=device_name)
        brio.downgrade_firmware()
        self.tune_methods.tc_firmware_update_brio4k(device_name=device_name)


if __name__ == "__main__":
    unittest.main()
