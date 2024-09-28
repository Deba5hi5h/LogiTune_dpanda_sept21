import logging
import os
import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWirelessPowerOnOffDongle(UIBase):
    """
    Detection for headset power cycle in Dongle mode
    """
    tune_method = TuneUIMethods()
    tune_app = TuneElectron()

    def test_XXX_VC_117120_detect_power_on_off_zone_wireless(self):
        try:
            self.tune_method.tc_detect_power_on_off_dongle(zone_wireless_api.name)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWirelessPowerOnOffDongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
