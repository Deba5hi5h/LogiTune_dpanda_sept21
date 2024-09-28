import logging
import os
import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_vibe_125_api, zone_vibe_130_api, zone_vibe_wireless_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneVibePowerOnOffDongle(UIBase):
    """
    Headset detection test when headset power turn off before dongle connected
    """
    # used in tearDown to update test status on zephyr
    conn_type = ConnectionType.dongle

    tune_method = TuneUIMethods()
    tune_app = TuneElectron()

    def test_XXX_VC_103777_detect_power_on_off_zone_vibe_125(self):
        self.device_name = zone_vibe_125_api.name
        try:
            self.tune_method.tc_detect_power_on_off_dongle(zone_vibe_125_api.name)

        except Exception as e:
            Report.logException(str(e))

    def test_XXX_VC_103778_detect_power_on_off_zone_vibe_130(self):
        self.device_name = zone_vibe_130_api.name
        try:
            self.tune_method.tc_detect_power_on_off_dongle(zone_vibe_130_api.name)

        except Exception as e:
            Report.logException(str(e))

    def test_XXX_VC_103779_detect_power_on_off_zone_vibe_wireless(self):
        self.device_name = zone_vibe_wireless_api.name
        try:
            self.tune_method.tc_detect_power_on_off_dongle(zone_vibe_wireless_api.name)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneVibePowerOnOffDongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
