import time
import unittest

from unittest import SkipTest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.TunesAppInstall import TunesUIInstall

from base.base_ui import UIBase
from base.base_settings import TUNEAPP_NAME
from common.framework_params import INSTALLER
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all
from extentreport.report import Report

class LogiTuneInstall(UIBase):

    def test_001_VC_XXXXX_install_logi_tune(self):
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        try:
            disconnect_all()
            app = TunesUIInstall()
            if app.check_for_app_installed_win(TUNEAPP_NAME):
                app.uninstallApp()
            time.sleep(10)
            app.installApp(INSTALLER)
            services = app.verify_logi_tune_services_install()
            if services:
                Report.logPass("Successfully installed Logi Tune")
            else:
                Report.logFail("Logi Tune not installed Successfully")
        except Exception as e:
            Report.logException(str(e))

    def test_002_VC_XXXXX_uninstall_logi_tune(self):
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        try:
            # disconnect all devices
            Report.logInfo("Disconnect all devices")
            disconnect_all()
            Report.logInfo("Start uninstall process")
            app = TunesUIInstall()
            app.uninstallApp()
            services = app.verify_logi_tune_services_uninstall()
            if services:
                Report.logPass("Successfully uninstalled Logi Tune")
            else:
                Report.logFail("Logi Tune not uninstalled successfully")
        except Exception as e:
            Report.logException(str(e))

    def test_003_VC_XXXXX_update_production_app_to_latest_staging(self):
        if get_custom_platform() != "windows":
            Report.logSkip("Test Case only supported in Windows")
            raise SkipTest("Test Case only supported in Windows")
        try:
            app = TunesUIInstall()
            if app.check_for_app_installed_win(TUNEAPP_NAME):
                app.uninstallApp()
            disconnect_all()
            _version = app.download_production_tuneapp()
            app.installApp(_version)
            services = app.verify_logi_tune_services_install()
            if services:
                Report.logPass("Successfully uninstalled Logi Tune")
            else:
                Report.logFail("Logi Tune not uninstalled successfully")
            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()
            self.tunesApp.click_update_logitune_now()
            app = TunesUIInstall()

            if app.check_update_app_status():
                Report.logPass("Successfully uninstalled Logi Tune")
            else:
                Report.logFail("Logi Tune not uninstalled successfully")
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LogiTuneInstall)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
