import logging
import os
import subprocess
import unittest
import time

from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from parameterized import parameterized

from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import Features

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
firmware_directory = os.path.join(directory, "firmware_tunes", "Logitech_Enduro")
PLATFORM = get_custom_platform()

enduro_BT = "046D_0AEE_2129ML000028"
enduro_new_MFI_BT = "046D_0AEE_2140ML000EQ8"
enduro_new_not_MFI_BT = "046D_0AEE_2140ML000DJ8"


class InstallEnduroFwDirectBT(UIBase):

    @classmethod
    def setUpClass(cls):
        super(InstallEnduroFwDirectBT, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(InstallEnduroFwDirectBT, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, 26)])
    def test_XXX_VC_YYYYY_install_Enduro_FW(self, retry):
        Report.logInfo(f"Try number: {retry}")
        device_mac = enduro_new_not_MFI_BT
        timeout = 20

        try:
            versions = ["0.17.0"]

            for version in versions:
                fw_version = f"0.16.0"
                Report.logInfo(f"Start FW {fw_version} installation.")
                self.start_performance_test()
                self.__install_enduro_fw(device_mac, fw_version)
                self.end_performance_test(f"Enduro FW installation {fw_version} finished!")

                time.sleep(timeout)

                fw_version = f"{version}"
                Report.logInfo(f"Start FW {fw_version} installation.")
                self.start_performance_test()
                self.__install_enduro_fw(device_mac, fw_version)
                self.end_performance_test(f"Enduro FW installation {fw_version} finished!")
                self.__verify_fw_version(device_mac, fw_version)
                time.sleep(timeout)

        except Exception as e:
            Report.logException(str(e))


    def __install_enduro_fw(self, device_mac, fw_version):
        Report.logInfo(f"Installing Enduro FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater_win\\FWU_Sample.exe hid {device_mac} {firmware_directory}\\files\\Enduro_V{fw_version}.img"
        else:
            cmd = f"{firmware_directory}/updater_mac/LGT_HID_E_FW_Update_CLT hid {device_mac} {firmware_directory}/files/Enduro_V{fw_version}.img"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)

            Report.logInfo(f" OUTPUT: {t_res}")
            assert "update_successfully" in t_res.decode('utf-8')

            time.sleep(20)

            Report.logInfo(f"Check FW version...")
            self.__verify_fw_version(device_mac, fw_version)

            Report.logInfo(f"Enduro Firmware installation to {fw_version} finished with success!!!!")

        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")

    def __verify_fw_version(self, device_mac, fw_version):
        Report.logInfo(f"Installing Enduro FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater_win\\FWU_Sample.exe hid_version {device_mac}"
        else:
            cmd = f"{firmware_directory}/updater_mac/LGT_HID_E_FW_Update_CLT hid_version {device_mac}"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)
            Report.logInfo(f"Response: {t_res}")

            assert fw_version in t_res.decode('utf-8')
        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InstallEnduroFwDirectBT)
    unittest.TextTestRunner(verbosity=2).run(suite)
