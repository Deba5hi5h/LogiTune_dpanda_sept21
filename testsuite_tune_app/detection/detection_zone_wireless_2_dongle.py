import logging
import os
import time
import unittest

from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all
from locators.tunes_ui_locators import TunesAppLocators
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_2_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWireless2Dongle(UIBase):
    # used in tearDown to update test status on zephyr
    device_name = zone_wireless_2_api.name
    conn_type = ConnectionType.dongle

    def test_XXX_VC_YYYYY_detect_Zone_wireless_2_dongle(self):
        """Verification of detecting Zone Wireless 2 through dongle connection
        This test powers off dongle which is plugged on USB hub and then powers on to check Zone Wireless connection
        It will fail if the battery sign is not showed up in Zone Wireless page on Tune
        """

        try:
            disconnect_all()
            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()
            for i in range(1, 3):
                Report.logInfo(f"{self.device_name} detection. Try {i}")
                connect_device(self.device_name)
                self.tunesApp.verify_element(TunesAppLocators.DEVICE, param=self.device_name, wait_for_visibility=True)
                self.tunesApp.is_device_battery_displayed(self.device_name)
                disconnect_device(self.device_name)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWireless2Dongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
