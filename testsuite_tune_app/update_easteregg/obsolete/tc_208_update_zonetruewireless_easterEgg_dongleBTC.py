import logging
import os
import time
import unittest

from parameterized import parameterized

from base.base_ui import UIBase
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "Logitech_Zaxxon", "files")


BASELINE_VERSION = "03.19"
TARGET_VERSION = "03.20"

file_path_baseline = os.path.join(DIR_PATH, f"Zaxxon_v00.00.{BASELINE_VERSION}_encrypted_ota.bin")
file_path_target = os.path.join(DIR_PATH, f"Zaxxon_v00.00.{TARGET_VERSION}_encrypted_ota.bin")
BASE = (BASELINE_VERSION, file_path_baseline, 0)
TARGET = (TARGET_VERSION, file_path_target, 1)


class UpdateZoneTrueWirelessDongleConnection(FwuStressBase):

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneTrueWirelessDongleConnection, cls).setUpClass()
        cls.tunesApp = TuneElectron()

    @parameterized.expand([(loop, ver) for loop in range(1, 15) for ver in [BASE, TARGET]])
    def test_208_VC_58903_upgrade_downgrade_zonetruewireless_firmware_dongle_connection(self, loop_no, ver):
        """
        Scenario:
        1. Downgrade BTC Dongle via Easter Egg.
        Downgrade Earbuds via Easter Egg.
        2. Update BTC Dongle via Easter Egg.
        Update Earbuds via Easter Egg.

        """
        device_name = "Zone True Wireless"

        Report.logInfo(f"Loop no: {loop_no}")
        if ver[2] == 0:
            Report.logInfo(f" DOWNGRADE TO {ver[0]}")
        else:
            Report.logInfo(f" UPGRADE TO {ver[0]}")

        try:
            time.sleep(1)
            Report.logInfo("Beginning of the test", screenshot=True)
            self.tunesApp.connect_tune_app()
            self.tunesApp.open_device_in_my_devices_tab(device_name)
            Report.logInfo("Before going to easteregg", screenshot=True)
            # Use easterEgg option to make Zaxxon upgrade-/downgrade
            self.tunesApp.update_firmware_with_easter_egg(file_path=ver[1],
                                                          is_headset=True,
                                                          is_zaxxon=True,
                                                          is_dongle=True,
                                                          timeout=500)

            time.sleep(5)

            # Check Zaxxon version after the update
            version = self.tunesApp.check_firmware_version(device_name=device_name,
                                                           is_headset=True,
                                                           is_dongle=True)
            assert ver[0][1:0] in version, f"{ver[0]} not in {version}"
            Report.logInfo("After checking the version", screenshot=True)
            time.sleep(30)
            Report.logInfo("After 30 sec after the test", screenshot=True)

        except Exception as e:
            Report.get_screenshot()
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneTrueWirelessDongleConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)
