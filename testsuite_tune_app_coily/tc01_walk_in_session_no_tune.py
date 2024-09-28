import os
import time
import unittest

from apps.collabos.coily.tune_coily_test_methods import WIN_APP_BAT_PATH, WIN_APP_CLOSE_BAT_PATH
from base.base_coily import CoilyBase
from base.base_settings import TUNEAPP_NAME
from base.base_ui import UIBase
from common.framework_params import INSTALLER
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all
from extentreport.report import Report
from apps.tune.TunesAppInstall import TunesUIInstallWindows
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS


class WalkInSessionNoTune(CoilyBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def setUp(self, *args):
        super().setUp()
        self._uninstall_logi_tune()


    def tearDown(self, *args):
        super().tearDown(tune_installed=False)
    @classmethod
    def _uninstall_logi_tune(cls):
        disconnect_all()
        Report.logInfo(f"Uninstall existing LogiTune.")
        if get_custom_platform() == "windows":
            os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
            app = TunesUIInstallWindows()
            if app.check_for_app_installed_win(TUNEAPP_NAME):
                app.uninstall_app()
            time.sleep(1)
            os.system(str(UIBase.rootPath) + WIN_APP_CLOSE_BAT_PATH)
        else:
            app = TunesUIInstallMacOS()
            if app.check_tune_installed_macos():
                app.uninstallApp()
        time.sleep(5)

    @classmethod
    def _install_logi_tune(cls):
        os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
        if get_custom_platform() == "windows":
            app = TunesUIInstallWindows()
            if app.check_for_app_installed_win(TUNEAPP_NAME):
                app.uninstall_app()
            time.sleep(10)
            app.install_app(INSTALLER)
            services = app.verify_logi_tune_services_install()
            if services:
                Report.logPass("Successfully installed Logi Tune")
            else:
                Report.logFail("Logi Tune not installed Successfully")
        else:
            app = TunesUIInstallMacOS()
            if app.check_tune_installed_macos():
                app.uninstallApp()
            time.sleep(5)
            app.installApp(INSTALLER)
        os.system(str(UIBase.rootPath) + WIN_APP_CLOSE_BAT_PATH)

    def test_1001_VC_112857_walk_in_session_enabled_logi_tune_not_installed(self):
        self.coily_test_methods.tc_walk_in_session_enabled_logi_tune_not_installed()


if __name__ == "__main__":
    unittest.main()
