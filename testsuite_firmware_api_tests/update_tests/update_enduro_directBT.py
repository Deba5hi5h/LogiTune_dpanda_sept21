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

enduro_BT = "44:73:d6:a3:19:e2"
enduro_new_mfi = "44:73:D6:A3:1A:BC"
enduro_new_not_mfi = "44:73:D6:A3:1A:D2"


class InstallEnduroFwDirectBT(UIBase):

    @classmethod
    def setUpClass(cls):
        super(InstallEnduroFwDirectBT, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(InstallEnduroFwDirectBT, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, 11)])
    def test_XXX_VC_YYYYY_install_Enduro_FW(self, retry):
        Report.logInfo(f"Try number: {retry}")
        device_mac = enduro_new_not_mfi
        timeout = 30

        try:
            versions = ["0.17.0"]

            for version in versions:
                fw_version = f"0.18.0"
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
                time.sleep(timeout)

        except Exception as e:
            Report.logException(str(e))


    def __install_enduro_fw(self, device_mac, fw_version):
        Report.logInfo(f"Installing Zaxxon FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater_win\\FWU_Sample.exe bt_spp {device_mac} {firmware_directory}\\files\\Enduro_V{fw_version}.img"
        else:
            cmd = f"{firmware_directory}/updater_mac/LGT_HID_E_FW_Update_CLT bt_spp {device_mac} {firmware_directory}/files/Enduro_V{fw_version}.img"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)

            Report.logInfo(f"OUTPUT: {t_res}")
            assert "update_successfully" in t_res.decode('utf-8')

            time.sleep(30)

            Report.logInfo(f"Check FW version...")
            self.__verify_fw_version(device_mac, fw_version)

            Report.logInfo(f"Zaxxon Firmware installation to {fw_version} finished with success!!!!")

        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")

    def __verify_fw_version(self, device_mac, fw_version):
        Report.logInfo(f"Installing Zaxxon FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater_win\\FWU_Sample.exe bt_spp_version {device_mac}"
        else:
            cmd = f"{firmware_directory}/updater_mac/LGT_HID_E_FW_Update_CLT bt_spp_version {device_mac}"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_ver = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)
            Report.logInfo(f"Response: {t_ver}")

            assert fw_version in t_ver.decode('utf-8')
        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InstallEnduroFwDirectBT)
    unittest.TextTestRunner(verbosity=2).run(suite)
