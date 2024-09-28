import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_vibe_125_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneVibe125Dongle(UIBase):
    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    device_name = zone_vibe_125_api.name
    conn_type = ConnectionType.dongle

    def test_XXX_VC_103774_detect_zone_vibe_125_dongle(self):
        try:
            disconnect_all()
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()
            for i in range(1, 3):
                Report.logInfo(f"{self.device_name} detection. Try {i}")
                connect_device(self.device_name)
                self.tune_app.is_device_battery_displayed(self.device_name)
                disconnect_device(self.device_name)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneVibe125Dongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
