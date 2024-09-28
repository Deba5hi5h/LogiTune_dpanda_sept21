import logging
import os
import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_900_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZone900PowerOnOffDongle(UIBase):
    """
    Detection for headset power cycle in Dongle mode
    """
    # used in tearDown to update test status on zephyr
    device_name = zone_900_api.name
    conn_type = ConnectionType.dongle

    tune_method = TuneUIMethods()
    tune_app = TuneElectron()

    def test_XXX_VC_117119_detect_power_on_off_zone_900(self):
        try:
            self.tune_method.tc_detect_power_on_off_dongle(zone_900_api.name)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZone900PowerOnOffDongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
