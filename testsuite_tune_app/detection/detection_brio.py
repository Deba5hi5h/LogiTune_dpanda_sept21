import logging
import os
import time
import unittest

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all
from base.base_ui import UIBase
from common.framework_params import PROJECT
from extentreport.report import Report

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectBrio(UIBase):


    def test_XXX_VC_YYYYY_detect_brio(self):
        device_name = "Brio"

        try:
            disconnect_all()
            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()
            for i in range(1, 3):
                Report.logInfo(f"{device_name} detection. Try {i}")
                time.sleep(5)
                connect_device(device_name)
                time.sleep(5)
                self.tunesApp.is_device_label_displayed(device_name)
                disconnect_device(device_name)
                time.sleep(5)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectBrio)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)




