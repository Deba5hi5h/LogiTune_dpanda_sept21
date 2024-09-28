import logging
import os
import time
import unittest

from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase
from common.usb_switch import disconnect_device
from testsuite_firmware_api_tests.api_tests.api_parameters import logi_dock_api, zone_wireless_2_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWireless2DockPairing(UIBase):

    dock_name = logi_dock_api.name
    device_name = zone_wireless_2_api.name
    receiver_name = zone_wireless_2_api.receiver_name
    tune_method = TuneUIMethods()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_method.tc_logi_dock_unpair_headset()
        time.sleep(3)
        disconnect_device(cls.dock_name)
        cls.tune_method.tc_pair_headset_with_dongle(device_name=cls.device_name, receiver_name=cls.receiver_name)
        disconnect_device(cls.device_name)

    def test_XXX_VC_YYYYY_detect_zone_wireless_2_dock_pairing(self):
        """Verification of detecting headset pairing through logi dock via logi tune
        It will fail when headset features not showing in tune app
        """

        self.tune_method.tc_detect_logi_dock_pairing_headsets(self.dock_name, device_name=self.device_name)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWireless2DockPairing)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
