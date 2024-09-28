import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wireless_plus

S3_FOLDER = "Logitech_Zone_Wireless_Plus"

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class UpdateZoneWirelessPlusBT(FwuStressBase):
    """
    Suite class for Zone Wireless Plus connected over direct BT FWU tests via EasterEgg and OTA.
    """

    file_path_headset = None
    baseline_version_headset = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneWirelessPlusBT, cls).setUpClass()
        cls.device_name = zone_wireless_plus.device_name
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_wireless_plus.is_initialized(skip_dongle=True)
        cls.baseline_version_headset = zone_wireless_plus.baseline_device_version
        cls.target_version_headset = zone_wireless_plus.target_device_version
        cls.file_path_headset = os.path.join(
            DIR_PATH, f"zonewirelessplus_headset_{cls.baseline_version_headset}.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path_headset)

    @parameterized.expand([(x,) for x in range(1, zone_wireless_plus.repeats + 1)])
    def test_205_VC_58898_update_zone_wireless_plus_directBT(self, retry):
        """
        Scenario:
        1. Downgrade Headset via Easter Egg.
        2. Update Headset via OTA.
        """
        Report.logInfo(f"Try number: {retry}")

        try:
            fw_update = FirmwareUpdate(
                retry=retry,
                test_entity=self,
                device_name=self.device_name,
                baseline_version_device=self.baseline_version_headset,
                target_version_device=self.target_version_headset,
                file_path_device=self.file_path_headset,
                tune_env=tune_env,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneWirelessPlusBT)
    unittest.TextTestRunner(verbosity=2).run(suite)
