import logging
import os
import subprocess
import time
from typing import List

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.helpers import return_valid_windows_logi_tune_path
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform, substring_in_iterable, check_for_app_installed_macos
from extentreport.report import Report

log = logging.getLogger(__name__)
app_name = 'Logi Tune' if check_for_app_installed_macos('Logi Tune') else 'LogiTune'
MAC_UPDATER = os.path.join('Applications', f'{app_name}.app', 'Contents', 'Frameworks', 'LogiTuneAgent.app',
                           'Contents', 'MacOS', 'QuadrunUpdater')
WIN_UPDATER = os.path.join(return_valid_windows_logi_tune_path(), 'tools', 'QuadrunUpdater', 'QuadrunUpdater.exe')
PLATFORM = get_custom_platform()

S3_FOLDER = "Quadrun"


class UpdateQuadrunReceiver(UIBase):
    device_address = None
    device_name = None
    firmware_downgrade = None
    firmware_update = None
    timeout = None

    @classmethod
    def setUpClass(cls):
        super(UpdateQuadrunReceiver, cls).setUpClass()
        assert "0AF0" in cls.device_address, f"PID 0AF0 not in Quadrun address {cls.device_address}"
        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.firmware_downgrade['binary_path'])
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.firmware_update['binary_path'])
        cls._kill_tune()

    @classmethod
    def tearDownClass(cls):
        super(UpdateQuadrunReceiver, cls).tearDownClass()

    def flash_firmware(self, fw_version: str, binary_path: str, timeout: int) -> None:
        Report.logInfo(f"Start {self.device_name} Quadrun Dongle FW {fw_version} installation.")
        self.start_performance_test()
        self._install_quadrun_fw(self.device_address, binary_path, fw_version)
        self.end_performance_test(f"{self.device_name} Quadrun Dongle FW installation "
                                  f"{fw_version} finished!")
        time.sleep(timeout)

    def _install_quadrun_fw(self, device_address, fw_file, fw_version):
        flash_success = "finished: success!"
        Report.logInfo(f"Installing {self.device_name} Quadrun Dongle FW: {fw_version}")
        updater = WIN_UPDATER if PLATFORM == 'windows' else MAC_UPDATER
        cmd = f"{updater} -u -t {device_address} -f {fw_file}"
        Report.logInfo(f"Command: {cmd}")

        last_lines = self._read_stdout(cmd)
        assert substring_in_iterable(flash_success, *last_lines), \
            f"Substring: '{flash_success}' not in {last_lines}"

        time.sleep(20)

        Report.logInfo(f"Check FW version...")
        self._verify_fw_version(device_address, fw_version)

        Report.logInfo(f"{self.device_name} Quadrun Dongle Firmware installation to {fw_version} "
                       f"finished with success!!!!")

    def _read_stdout(self, cmd: str) -> List[str]:
        buffer = list()
        for line in self._run_command(cmd):
            print(line.strip())
            if line:
                if len(buffer) == 10:
                    buffer.pop(0)
                buffer.append(line.strip())
            else:
                break
        return buffer

    def _verify_fw_version(self, device_address, fw_version):
        Report.logInfo(f"Checking {self.device_name} Quadrun Dongle FW version: {fw_version}")
        updater = WIN_UPDATER if PLATFORM == 'windows' else MAC_UPDATER
        cmd = f"{updater} -v -t {device_address}"
        Report.logInfo(f"Command: {cmd}")

        t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)
        Report.logInfo(f"Response: {t_res.decode('utf-8')}")

        assert fw_version in t_res.decode('utf-8').replace(',', '.'), \
            f"FW version is not equal {fw_version}"

    @staticmethod
    def _run_command(cmd: str) -> str:
        with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as popen:
            for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line.decode('utf-8')
            popen.kill()

    @staticmethod
    def _kill_tune():
        if PLATFORM == 'windows':
            os.system(r"taskkill /IM LogiTune.exe /T /F")
        else:
            os.system(r"pkill -9 LogiTune")
