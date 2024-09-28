import json
import os
import re
import subprocess
import time
from typing import Optional

from apps.tune.helpers import get_logitune_version
from base import global_variables, base_settings
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform, is_windows_service_running
from extentreport.report import Report
from common.framework_params import TUNE_ENV


class TuneBaseDaemon:
    """Class for easy Tune daemon handling used on macOS

    Class which allows easy loading/unloading Tune daemon process used on macOS
    """
    def __init__(self, daemon_name: str, plist_path: str, sudo_launch: bool):
        self.daemon_name = daemon_name
        self.plist_path = plist_path
        self.launchctl_command = 'sudo launchctl' if sudo_launch else 'launchctl'

    def load(self) -> None:
        self._call_daemon_command('load')

    def unload(self) -> None:
        self._call_daemon_command('unload')

    def _call_daemon_command(self, command: str) -> None:
        cmd = f'{self.launchctl_command} {command} {self.plist_path}'
        try:
            pattern = r'failed: (\d*):'
            response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
            errors = re.search(pattern, response)
            if errors:
                Report.logInfo(f'Tune {self.daemon_name} daemon {command}ing issue:')
                if errors.group(1) == 5 or errors.group(1) == 113:
                    Report.logInfo(f'Tune {self.daemon_name} daemon was {command}ed already. - {response}')
                    return
                self._handle_error(int(errors.group(1)), response)
            else:
                Report.logInfo(f'Tune {self.daemon_name} daemon {command}ing finished successfully!')
        except subprocess.CalledProcessError as e:
            Report.logException(f'Exception occurred when {command}ing '
                                f'Tune {self.daemon_name} daemon: {e}')
            Report.logInfo('Probably no password for /bin/launchctl hasn\'t been added to '
                           '"sudo visudo". Please check README.md file, point 6 for instructions')
            raise e

    @staticmethod
    def _handle_error(error_id: int, response: str) -> None:
        if error_id == 37:
            Report.logInfo(f'Error ID {error_id} - Operation already in progress')
        elif error_id == 113:
            Report.logInfo(f'Error ID {error_id} - Could not find specified service')
        elif error_id == 2:
            Report.logInfo(f'Error ID {error_id} - No such file or directory')
        elif error_id == 5:
            if 'Unload failed' in response:
                msg = 'Unloading failed. Try to Load daemon first.'
            else:
                msg = 'Loading failed. Try to Unload daemon first.'
            Report.logInfo(f'Error ID {error_id} - {msg}')
        else:
            Report.logException(f'Error ID {error_id} - Error without handle: {response}')
            raise TypeError(f'Error ID {error_id} - Error without handle: {response}')


class TuneUpdaterDaemon(TuneBaseDaemon):
    """Class for easy Tune Updater daemon handling used on macOS

    Class which allows easy loading/unloading Tune Updater daemon process used on macOS
    """
    def __init__(self):
        super().__init__(
            daemon_name='Updater',
            plist_path='/Library/LaunchDaemons/com.logitech.logitune.updater.plist',
            sudo_launch=True
        )


class TuneAgentDaemon(TuneBaseDaemon):
    """Class for easy Tune Agent daemon handling used on macOS

    Class which allows easy loading/unloading Tune Agent daemon process used on macOS
    Valid from Tune 3.7.x
    """
    def __init__(self):
        super().__init__(
            daemon_name='Agent',
            plist_path='/Library/LaunchAgents/com.logitech.logitune.agent.plist',
            sudo_launch=False
        )


class TuneAppSettings:
    """Class allows to modify settings.json file from Logi Tune app

    Class allows to modify settings.json file depending on properties.LOCAL argument (TUNE_ENV)
    and changes Logi Tune environment to be automated.
    """
    _mac_settings_path = base_settings.TUNE_SETTINGS_PATH_MAC
    _win_settings_path = base_settings.TUNE_SETTINGS_PATH_WIN
    _win_tune_updater = os.path.join(str(UIBase.rootPath), "firmware_tunes", "restart_tune_updater_service.bat")

    def __init__(self):
        self._platform = get_custom_platform()
        self._settings_path = self._win_settings_path if self._platform == "windows" else self._mac_settings_path
        if self._platform == 'macos':
            self._tune_daemon = TuneUpdaterDaemon() if (
                get_logitune_version().startswith('3.6')) else TuneAgentDaemon()
        self._settings_json = self._read_json(self._settings_path)

    def adjust_logitune_settings_file(self, tune_env: Optional[str] = None,
                                      app_update: Optional[str] = None) -> None:
        """Changes settings.json file

        Adjusts settings.json file and executes any needed actions depending on operating system.

        Returns:
            None
        """
        try:
            Report.logInfo("Modify settings.json file...")
            if "macos" in self._platform:
                Report.logInfo(f"Kill LogiTune")
                os.system('pkill -9 LogiTune')
                os.system('pkill -9 LogiTune')
                self._tune_daemon.unload()
                time.sleep(10)
                self._modify_logi_tune_settings_file(tune_env=tune_env, app_update=app_update)
                self._tune_daemon.load()
            else:
                self._modify_logi_tune_settings_file(tune_env=tune_env, app_update=app_update)
                time.sleep(5)
                self._restart_logitune_updater_service()
            Report.logInfo("Settings.json modified successfully!")
        except Exception as e:
            Report.logException(
                f"There was a problem when changing Logi Tune settings.json file: {e}")

    def _modify_logi_tune_settings_file(self, tune_env: Optional[str] = None,
                                        app_update: Optional[str] = None) -> None:
        if not tune_env:
            tune_env = TUNE_ENV

        try:
            if 'prod' in tune_env:
                if "FWUpdateManifestUrl" in self._settings_json:
                    self._settings_json.pop("FWUpdateManifestUrl")
                if "FWUpdateChannel" in self._settings_json:
                    self._settings_json.pop("FWUpdateChannel")
            else:
                if "FWUpdateManifestUrl" not in self._settings_json:
                    self._settings_json["FWUpdateManifestUrl"] = global_variables.TUNE_FW_UPDATE_MANIFEST_URL
                if "FWUpdateChannel" not in self._settings_json or (
                        tune_env != self._settings_json.get("FWUpdateChannel")):
                    self._settings_json["FWUpdateChannel"] = tune_env
            if not app_update or 'prod' in app_update:
                if "UpdateManifestUrl" in self._settings_json:
                    self._settings_json.pop("UpdateManifestUrl")
                if "UpdateChannel" in self._settings_json:
                    self._settings_json.pop("UpdateChannel")
            else:
                if "UpdateManifestUrl" not in self._settings_json:
                    if get_logitune_version().startswith('3.6'):
                        self._settings_json["UpdateManifestUrl"] = global_variables.TUNE_UPDATE_MANIFEST_URL_OLD
                    else:
                        self._settings_json["UpdateManifestUrl"] = global_variables.TUNE_UPDATE_MANIFEST_URL
                if "UpdateChannel" not in self._settings_json or (
                        app_update != self._settings_json.get("UpdateChannel")):
                    self._settings_json["UpdateChannel"] = app_update
            if "easterEgg" not in self._settings_json:
                self._settings_json["easterEgg"] = True
            if "automate" not in self._settings_json:
                self._settings_json["automate"] = True
            self._save_json(self._settings_path, self._settings_json)
        except Exception as e:
            Report.logException(f"Not possible to modify settings dictionary: {e}")

    @staticmethod
    def _read_json(file_path: str) -> dict:
        try:
            with open(file_path, "r") as a_file:
                return json.load(a_file)
        except Exception as e:
            Report.logException(f"Not possible to read settings.json file: {e}")

    @staticmethod
    def _save_json(file_path: str, json_object: dict) -> None:
        try:
            with open(file_path, "w") as a_file:
                json.dump(json_object, a_file, indent=2)
        except Exception as e:
            Report.logException(f"Not possible to save to settings.json file: {e}")

    def check_settings_file_flags(self, *args) -> dict:

        current_settings = self._settings_json
        checked_flags = {}

        for flag in args:
            checked_flags[flag] = current_settings.get(flag)

        return checked_flags

    def modify_settings_flags(self, **kwargs):

        current_settings = self._settings_json
        for key, value in kwargs.items():
            current_settings[key] = value
            try:
                if "macos" in self._platform:
                    Report.logInfo(f"Kill LogiTune")
                    os.system('pkill -9 LogiTune')
                    os.system('pkill -9 LogiTune')
                    self._tune_daemon.unload()
                    time.sleep(10)
                    self._save_json(self._settings_path, current_settings)
                    self._tune_daemon.load()
                else:
                    self._save_json(self._settings_path, current_settings)
                    self._restart_logitune_updater_service()
            except Exception as e:
                print(e)

    def _restart_logitune_updater_service(self, retry: int = 3) -> None:
        subprocess.run(self._win_tune_updater, shell=True)
        time.sleep(15)
        if is_windows_service_running("LogiTuneUpdaterService"):
            Report.logInfo("LogiTuneUpdaterService restarted successfully.")
        else:
            if retry > 0:
                retry -= 1
                Report.logInfo(f"LogiTuneUpdaterService not restarted properly, "
                               f"retries left: {retry}")
                self._restart_logitune_updater_service(retry=retry)
            else:
                Report.logFail("LogiTuneUpdaterService not restarted properly after 3 retries!")
