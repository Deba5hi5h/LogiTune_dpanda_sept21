import os
import subprocess
from typing import Optional
import requests

from apps.tune.TuneAppSettings import TuneAppSettings
from base import global_variables, base_settings
from base.base_settings import LOGITUNES_PROD_EP, LOGITUNE_HEADER
from base.base_ui import UIBase
from base.global_variables import TUNE_DEBUG_PORT
from pathlib import Path
import time

from common.aws_s3_utils import AwsS3Utils

from extentreport.report import Report


class TunesUIInstallMacOS(UIBase):

    def __init__(self):
        self.desired_cap = {}
        self.report = Report()

    def download_app_from_s3(self, version, root_path) -> Optional[str]:
        try:
            path = os.path.join(root_path, "installers")
            file_path = os.path.join(root_path, "installers", f"LogiTuneInstaller{version}.pkg")
            app_file = Path(file_path)
            if not app_file.exists():
                self.report.logInfo(f"Looking for valid S3 path to Logi Tune {version}")
                aws_utils = AwsS3Utils()
                found_path = aws_utils.find_prefix_with_tune_version(version)
                if found_path is None:
                    raise FileNotFoundError
                self.report.logInfo(f"Found valid path for '{version}' - {found_path}")
                version = found_path.split("/")[2]
                if os.path.isfile(os.path.join(path, f"LogiTuneInstaller{version}.pkg")):
                    self.report.logInfo("Logi Tune file already downloaded")
                    return version
                prefix = f'vc-sw-release/{found_path}mac/LogiTuneInstaller.pkg'
                aws_utils.download_from_S3(source=prefix, destination=path)
                os.rename(os.path.join(path, "LogiTuneInstaller.pkg"),
                          os.path.join(path, f"LogiTuneInstaller{version}.pkg"))
                self.report.logInfo(f"LogiTuneInstaller{version}.pkg "
                                    f"downloaded to \\installers\\ folder.")
                return version
            else:
                self.report.logInfo("Logi Tune file already downloaded")
        except Exception as e:
            self.report.logException("Not possible to download file from S3.")
            raise e

    def installApp(self, version, tune_env: Optional[str] = None, app_update: Optional[str] = None):
        rootPath = UIBase.rootPath
        filePath = os.path.join(rootPath, "installers", f"LogiTuneInstaller{version}.pkg")
        appFile = Path(filePath)
        if not appFile.exists():
            self.report.logInfo("File not exists locally. Downloading from S3...")
            valid_version = self.download_app_from_s3(version, rootPath)
            version = version if valid_version is None else valid_version
            filePath = os.path.join(rootPath, "installers", f"LogiTuneInstaller{version}.pkg")
        self.report.logInfo("Installing LogiTune...")
        res = subprocess.check_output(f"sudo installer -pkg {filePath} -target /", shell=True)
        assert "installer: The upgrade was successful." in res.decode('utf-8') or "installer: The install was successful." in res.decode('utf-8'), "AAAAAAAA"

        time.sleep(5)
        cmd = f"sh {str(UIBase.rootPath)}/WinApp/tune.sh {TUNE_DEBUG_PORT}"
        subprocess.run(cmd, shell=True)
        time.sleep(30)
        self.report.logInfo(f"Launch LogiTune: {cmd}")
        tune_settings = TuneAppSettings()
        if tune_env or app_update:
            tune_settings.adjust_logitune_settings_file(tune_env=tune_env, app_update=app_update)
        time.sleep(5)

    def uninstallApp(self):
        app_name = "Logi Tune" if self.check_for_app_installed_macos("Logi Tune") else "LogiTune"
        self.report.logInfo("Unistalling LogiTune...")
        cmd = f'sudo rm -rf "/Applications/{app_name}.app"'
        subprocess.run(cmd, shell=True)
        assert self.check_tune_installed_macos() is not True, \
            ("LogiTune uninstalling failed. Make sure there is "
             "'NOPASSWD: /bin/rm' added in 'sudo visudo' file (check README)")
        self.assert_tune_is_not_in_mac()
        self.report.logInfo("LogiTune uninstalled successfully!")

    def assert_tune_is_not_in_mac(self):
        cmd = f'mdfind -name "LogiTune"'
        res = subprocess.check_output(cmd, shell=True)
        tune_uninstall_err_msg = "Error! After uninstallation, still found relevant files in this Mac!"
        res_decoded = res.decode('utf-8')
        paths = ["/Applications/LogiTune.app", "/Applications/Logi Tune.app", "/Users/Shared/logitune",
                 "/Library/Application Support/logitune",
                 "/Library/LaunchAgents/com.logitech.logitune.launcher.plist"]
        for line in res_decoded:
            for path in paths:
                assert path is not line, tune_uninstall_err_msg

    @staticmethod
    def check_for_app_installed_macos(app_name: str) -> bool:
        res = subprocess.check_output("system_profiler SPApplicationsDataType", shell=True)
        apps = res.decode("utf-8")
        return f"Location: /Applications/{app_name}.app" in apps

    def check_tune_installed_macos(self) -> bool:
        return any((self.check_for_app_installed_macos('Logi Tune'),
                   self.check_for_app_installed_macos('LogiTune')))

    def get_production_version_tune(self) -> str:
        """
        This method is to get the version of latest tuneapp from production server.

        :return: production_version
        """
        try:
            req = requests.get(LOGITUNES_PROD_EP,
                               headers=LOGITUNE_HEADER)
            response = req.json()
            _version = response['version']
            self.report.logInfo(f"Latest version of the tuneapp in production server is {_version}")
            return _version

        except Exception as ex:
            self.report.logException("Failed to get current production version")
            raise ex
