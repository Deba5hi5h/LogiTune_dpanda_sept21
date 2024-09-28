import logging
import os
import time
import unittest

from base.base_ui import UIBase
from common.framework_params import PROJECT
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wired_earbuds_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWiredEarbuds(UIBase):

    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    device_name = zone_wired_earbuds_api.name
    conn_type = ConnectionType.dongle

    def test_XXX_VC_103771_detect_zone_wired_earbuds(self):
        try:
            disconnect_all()
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()
            for i in range(1, 3):
                Report.logInfo(f"{self.device_name} detection. Try {i}")
                time.sleep(5)
                connect_device(self.device_name)
                time.sleep(5)
                self.tune_app.is_device_label_displayed("Zone Wired Earbuds")
                disconnect_device(self.device_name)
                time.sleep(5)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWiredEarbuds)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)




