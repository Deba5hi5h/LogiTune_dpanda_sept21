import unittest

from apps.tune.TunesAppInstall import TunesUIInstallWindows
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS


class TuneUninstall(UIBase):

    @staticmethod
    def test_002_VC_42612_uninstall_logi_tune():
        try:
            Report.logInfo("Start uninstall process")
            if get_custom_platform() == "windows":
                app = TunesUIInstallWindows()
                app.uninstall_app()
                services = app.verify_logi_tune_services_uninstall()
                if not services:
                    Report.logPass("Successfully uninstalled Logi Tune")
                else:
                    Report.logFail("Logi Tune not uninstalled successfully")
            else:
                app = TunesUIInstallMacOS()
                app.uninstallApp()
                if not app.check_tune_installed_macos():
                    Report.logPass("Successfully uninstalled Logi Tune")
                else:
                    Report.logFail("Logi Tune not uninstalled successfully")
        except Exception as e:
            Report.logException(str(e))


if __name__ == "__main__":
    unittest.main()
