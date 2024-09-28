import logging
import os
import unittest
import time

from apps.tune.TuneElectron import TuneElectron, disconnect_all, connect_device
from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_2_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWireless2PowerOnOffDongle(UIBase):
    """
    Detection for headset power cycle in Dongle mode
    """
    tune_method = TuneUIMethods()
    tune_app = TuneElectron()
    device_name = zone_wireless_2_api.name
    conn_type = ConnectionType.dongle


    def test_XXX_VC_117121_detect_power_on_off_zone_wireless_2(self):

        try:
            self.tune_method.tc_detect_power_on_off_dongle(device_name=self.device_name)
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWireless2PowerOnOffDongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
