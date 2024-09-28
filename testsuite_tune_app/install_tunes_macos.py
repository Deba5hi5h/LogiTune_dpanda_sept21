import platform
import time
import unittest

from unittest import SkipTest

from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS

from base.base_ui import UIBase
from common.framework_params import INSTALLER
from common.platform_helper import get_custom_platform
from extentreport.report import Report

class LogiTuneInstallMacOS(UIBase):


    def test_0011_VC_XXXXX_install_logi_tune_macos(self):
        if get_custom_platform() != "macos":
            Report.logSkip("Test Case only supported in MacOS")
            raise SkipTest("Test Case only supported in MacOS")
        try:
            app = TunesUIInstallMacOS()

            if app.check_tune_installed_macos():
                app.uninstallApp()
            time.sleep(5)
            app.installApp(INSTALLER)
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LogiTuneInstallMacOS)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
