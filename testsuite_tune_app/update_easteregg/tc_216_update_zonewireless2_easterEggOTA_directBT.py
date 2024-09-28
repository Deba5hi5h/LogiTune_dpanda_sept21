import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wireless_2

S3_HEADSET_FOLDER = "Cybermorph"

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class UpdateZoneWireless2(FwuStressBase):
    """
    Suite class for Zone Wireless 2 connected over BT FWU tests via EasterEgg and OTA.
    """

    baseline_version_headset = None
    file_path_headset = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneWireless2, cls).setUpClass()
        cls.device_name = zone_wireless_2.device_name
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_wireless_2.is_initialized(skip_dongle=True)
        cls.baseline_version_headset = zone_wireless_2.baseline_device_version
        cls.baseline_version_tahiti = zone_wireless_2.baseline_tahiti_version
        cls.target_version_headset = zone_wireless_2.target_device_version
        cls.target_version_tahiti = zone_wireless_2.target_tahiti_version
        cls.file_path_headset = os.path.join(
            DIR_PATH, f"cybermorph_v{cls.baseline_version_headset}_xxx_v{cls.baseline_version_tahiti}.bin"
        )
        cls.file_path_tahiti = os.path.join(
            DIR_PATH, f"tahiti_v{cls.baseline_version_headset}_xxx_v{cls.baseline_version_tahiti}.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_HEADSET_FOLDER, cls.file_path_headset, cls.file_path_tahiti)

    @parameterized.expand([(x,) for x in range(1, zone_wireless_2.repeats + 1)])
    def test_216_VC_74092_update_zone_wireless_2_directBT(self, retry):
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
                baseline_version_tahiti=self.baseline_version_tahiti,
                target_version_device=self.target_version_headset,
                target_version_tahiti=self.target_version_tahiti,
                file_path_device=self.file_path_headset,
                file_path_tahiti=self.file_path_tahiti,
                tune_env=tune_env,
                timeout=2500,
                save_pass_logs=True
            )
            fw_update.update_cybermorph_components()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneWireless2)
    unittest.TextTestRunner(verbosity=2).run(suite)
