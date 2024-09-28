import logging
import os
import subprocess
import unittest
import time
from typing import List

from apps.tune.firmware_downloader import FirmwareDownloader
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from parameterized import parameterized
from testsuite_tune_app.update_easteregg.device_parameters import zone_vibe_130


log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
firmware_directory = os.path.join(directory, "firmware_tunes", "easterEgg")
updater_directory = os.path.join(directory, "firmware_tunes", "standalone_updaters")
PLATFORM = get_custom_platform()

S3_FOLDER = "Logitech_Zone_Vibe_130"
DEVICE = zone_vibe_130
DEVICE_ADDRESS = DEVICE.dongle_address


class InstallZoneVibe130FwDirectBT(UIBase):

    @classmethod
    def setUpClass(cls):
        super(InstallZoneVibe130FwDirectBT, cls).setUpClass()

        baseline_file = os.path.join(
            firmware_directory, f"ZoneVibe130_Headset_{DEVICE.baseline_device_version}.img"
        )
        target_file = os.path.join(
            firmware_directory, f"ZoneVibe130_Headset_{DEVICE.target_device_version}.img"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, baseline_file)
        t_files.prepare_firmware_files_for_test(S3_FOLDER, target_file)

    @classmethod
    def tearDownClass(cls):
        super(InstallZoneVibe130FwDirectBT, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, DEVICE.repeats + 1)])
    def test_XXX_VC_YYYYY_install_Enduro_FW(self, retry):
        Report.logInfo(f"Try number: {retry}")
        timeout = 20

        try:
            fw_version = DEVICE.baseline_device_version
            Report.logInfo(f"Start Zone Vibe 130 FW {fw_version} installation.")
            self.start_performance_test()
            self._install_enduro_fw(DEVICE_ADDRESS, fw_version)
            self.end_performance_test(f"Zone Vibe 130 FW installation {fw_version} finished!")

            time.sleep(timeout)

            fw_version = DEVICE.target_device_version
            Report.logInfo(f"Start Zone Vibe 130 FW {fw_version} installation.")
            self.start_performance_test()
            self._install_enduro_fw(DEVICE_ADDRESS, fw_version)
            self.end_performance_test(f"Zone Vibe 130 FW installation {fw_version} finished!")
            time.sleep(timeout)

        except Exception as e:
            Report.logException(str(e))
            time.sleep(5)
            raise e

    def _install_enduro_fw(self, device_address, fw_version):
        Report.logInfo(f"Installing Zone Vibe 130 FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{updater_directory}\\zone_vibe_updater_win\\FWU_Sample.exe hid " \
                  f"{device_address} {firmware_directory}\\ZoneVibe130_Headset_{fw_version}.img"
        else:
            cmd = f"{updater_directory}/zone_vibe_updater_mac/LGT_HID_E_FW_Update_CLT hid " \
                  f"{device_address} {firmware_directory}/ZoneVibe130_Headset_{fw_version}.img"

        Report.logInfo(f"Command: {cmd}")

        try:
            last_lines = self._read_stdout(cmd)
            Report.logInfo(f"OUTPUT: {last_lines}")
            assert ("update_successfully" in last_lines or "Headset update completed" in last_lines)

            time.sleep(20)

            Report.logInfo(f"Check FW version...")
            self._verify_fw_version(device_address, fw_version)

            Report.logInfo(f"Zone Vibe 130 Firmware installation to {fw_version} "
                           f"finished with success!!!!")

        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")
            time.sleep(5)
            raise e3

    def _read_stdout(self, cmd: str) -> List[str]:
        last_lines = ["" for _ in range(10)]
        for line in self._run_command(cmd):
            Report.logInfo(line.strip())
            if line:
                last_lines.pop(0)
                last_lines.append(line.strip())
            else:
                break
        return last_lines

    @staticmethod
    def _run_command(cmd: str) -> str:
        with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as popen:
            for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line.decode('utf-8')
            popen.kill()

    @staticmethod
    def _verify_fw_version(device_address, fw_version):
        Report.logInfo(f"Checking Zone Vibe 130 FW version: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{updater_directory}\\zone_vibe_updater_win\\FWU_Sample.exe hid_version " \
                  f"{device_address}"
        else:
            cmd = f"{updater_directory}/zone_vibe_updater_mac/LGT_HID_E_FW_Update_CLT hid_version" \
                  f" {device_address}"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)
            Report.logInfo(f"Response: {t_res.decode('utf-8')}")

            assert fw_version in t_res.decode('utf-8')
        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")
            time.sleep(5)
            raise e3


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InstallZoneVibe130FwDirectBT)
    unittest.TextTestRunner(verbosity=2).run(suite)
