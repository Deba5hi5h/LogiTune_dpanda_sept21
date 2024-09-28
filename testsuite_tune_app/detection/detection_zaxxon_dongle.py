import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_true_wireless_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZaxxonDongle(UIBase):

    tune_app = TuneElectron()
    device_name = zone_true_wireless_api.name
    conn_type = ConnectionType.dongle

    def test_XXX_VC_103773_detect_zaxxon_dongle(self):
        """Verification of detecting Zaxxon through dongle connection
        This test powers off dongle which is plugged on USB hub and then powers on to check Zaxxon connection
        It will fail if the battery sign is not showed up in Zaxxon page on Tune
        """

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
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZaxxonDongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
