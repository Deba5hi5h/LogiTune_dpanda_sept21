import ctypes
import os
import subprocess
import time
from typing import Callable

import psutil

from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all
from extentreport.report import Report

from apps.tune.logi_sync_personal_collab.download_provisioning_package import \
                    DownloadLogiSyncPersonalCollab, DownloadProvisioningJson

WAIT_INTERVAL = 5
MAX_WAIT_TIME = 150


class InstallLogiSyncPersonalCollab:

    def install_logi_sync_personal_collab(self, disconnect_devices: bool = True) -> bool:
        try:
            if disconnect_devices:
                disconnect_all()

            Report.logInfo(f"Install LogiSyncPersonalCollab service.")

            installer_file = DownloadLogiSyncPersonalCollab().download_helvellyn_installer()
            DownloadProvisioningJson().create_provisioning_file()

            if get_custom_platform() == "windows":
                from apps.tune.logi_sync_personal_collab.logi_sync_personal_collab_uuid import \
                    LogiSyncPersonalCollabWindowsInfo

                _current_directory = os.path.dirname(__file__)
                _target_dir = os.path.join(_current_directory, "logi_sync_personal_collab_utils")

                windows_info = LogiSyncPersonalCollabWindowsInfo()

                if windows_info.is_installed():
                    self._uninstall_service_windows(_target_dir, windows_info.get_product_id())
                    self._wait_for_service_status_change(windows_info.is_installed,
                                                         desired_status=False)
                    Report.logInfo("LogiSyncPersonalCollab successfully uninstalled")

                self._install_service_windows(_target_dir)
                return self._wait_for_service_status_change(windows_info.is_installed,
                                                            desired_status=True)

            else:
                if self._is_macos_process_running('SyncPersonalCollab'):
                    self._uninstall_service_mac()

                self._install_service_mac(installer_file)
                return self._wait_for_service_status_change(
                    lambda: self._is_macos_process_running('SyncPersonalCollab'),
                    desired_status=True
                )

        except Exception as e:
            Report.logException(str(e))

    def uninstall_logi_sync_personal_collab(self) -> bool:
        try:

            Report.logInfo(f"Uninstalling LogiSyncPersonalCollab.")

            if get_custom_platform() == "windows":
                from apps.tune.logi_sync_personal_collab.logi_sync_personal_collab_uuid import \
                    LogiSyncPersonalCollabWindowsInfo

                windows_info = LogiSyncPersonalCollabWindowsInfo()

                if windows_info.is_installed():
                    _current_directory = os.path.dirname(__file__)
                    _target_dir = os.path.join(_current_directory, "logi_sync_personal_collab_utils")
                    self._uninstall_service_windows(_target_dir, windows_info.get_product_id())
                    self._wait_for_service_status_change(windows_info.is_installed, desired_status=False)
                    Report.logInfo("LogiSyncPersonalCollab successfully uninstalled")

                return not windows_info.is_installed()
            else:
                if self._is_macos_process_running('SyncPersonalCollab'):
                    self._uninstall_service_mac()

                return not self._is_macos_process_running('SyncPersonalCollab')
        except Exception as e:
            Report.logException(str(e))

    def _uninstall_service_windows(self, target_dir: str, prod_id: str) -> None:
        Report.logInfo("Start removing the service.")
        uninstall_bat = os.path.join(target_dir, "uninstall_logi_sync_personal_collab.bat")
        subprocess.run([uninstall_bat, prod_id], capture_output=True, shell=True, check=True)
        self._wait_till_batch_is_running(file_path=uninstall_bat)

    def _install_service_windows(self, target_dir: str) -> None:
        Report.logInfo("Start installing the service.")
        install_bat = os.path.join(target_dir, "install_logi_sync_personal_collab.bat")
        subprocess.run([install_bat], capture_output=True, text=True, check=True)
        self._wait_till_batch_is_running(file_path=install_bat)

    @staticmethod
    def _uninstall_service_mac() -> None:
        uninstall_response = subprocess.run(['sudo', '/Library/LogiSyncPersonalCollab/uninstall.sh'],
                                            capture_output=True,
                                            text=True, check=False)
        if 'sudo: a password is required' in uninstall_response.stderr:
            raise PermissionError('sudo: a password is required. Probably user not added NOPASSWD flag for the script '
                                  'in "sudo visudo". Please check TUNE_DESKTOP_README.md point 6 for more information')
        assert "Done" in uninstall_response.stdout, Report.logFail("Failed to uninstall LogiSyncPersonalCollab.")
        Report.logInfo("LogiSyncPersonalCollab successfully uninstalled")
        time.sleep(10)

    @staticmethod
    def _install_service_mac(installer_file: str) -> None:
        install_response = subprocess.check_output(f"sudo installer -pkg {installer_file} -target /", shell=True)
        assert "The upgrade was successful." in install_response.decode("utf-8"), (
            Report.logFail("Failed to install LogiSyncPersonalCollab."))
        Report.logInfo("Start installing the service.")

    @staticmethod
    def _wait_for_service_status_change(is_installed_func: Callable, desired_status: bool,
                                        max_time: int = MAX_WAIT_TIME) -> bool:
        elapsed_time = 0
        while elapsed_time <= max_time:
            current_status = is_installed_func()
            if current_status == desired_status:
                return True
            else:
                Report.logInfo(f"Current status is {current_status}. Service status not changed in the system. "
                               f"Another try in {WAIT_INTERVAL} sec.")
                time.sleep(WAIT_INTERVAL)
                elapsed_time += WAIT_INTERVAL
        return False

    @staticmethod
    def _is_macos_process_running(process_name: str) -> bool:
        try:
            subprocess.check_output(['pgrep', '-x', process_name])
            return True
        except subprocess.CalledProcessError:
            Report.logInfo(f'No process named {process_name} is currently running.')
            return False

    def _wait_till_batch_is_running(self, file_path: str, max_time: int = MAX_WAIT_TIME) -> bool:
        short_path_file = self._get_short_path_windows_file(file_path)
        elapsed_time = 0
        while elapsed_time <= max_time:
            if not self._check_if_batch_running(short_path_file):
                return True
            else:
                Report.logInfo(
                    f"Batch script is still running. Another try in {WAIT_INTERVAL} sec.")
                time.sleep(WAIT_INTERVAL)
                elapsed_time += WAIT_INTERVAL
        return False

    @staticmethod
    def _check_if_batch_running(short_file_path: str) -> bool:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] == 'cmd.exe':
                if short_file_path in proc.info['cmdline'][3]:
                    return True
        return False

    @staticmethod
    def _get_short_path_windows_file(long_path: str) -> str:
        """
        Takes the long path of a file and then returns its short path.
        :param long_path: str: The long path of the file.
        :return: str: The short (8.3) version of the path.
        """
        # Make the GetShortPathNameW function.
        get_short_path_name_w = ctypes.windll.kernel32.GetShortPathNameW
        # Make storage for the short path name and get it.
        short_path = ctypes.create_unicode_buffer(500)  # Adjust size, if required.
        if get_short_path_name_w(long_path, short_path, len(short_path)):
            return short_path.value


if __name__ == '__main__':
    print(InstallLogiSyncPersonalCollab().install_logi_sync_personal_collab())
