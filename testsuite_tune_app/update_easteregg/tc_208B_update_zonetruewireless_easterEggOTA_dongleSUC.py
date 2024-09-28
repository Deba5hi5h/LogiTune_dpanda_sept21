import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_true_wireless

S3_FOLDER = "Logitech_Zaxxon/files"

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class UpdateZoneTrueWirelessDongleSUCConnection(FwuStressBase):
    """
    Suite class for Zone True Wireless connected over SU dongle FWU tests via EasterEgg and OTA.
    """

    file_path_dongle = None
    file_path_headset = None
    baseline_version_dongle = None
    baseline_version_headset = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneTrueWirelessDongleSUCConnection, cls).setUpClass()
        cls.device_name = f'{zone_true_wireless.device_name} Plus'
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_true_wireless.is_initialized()
        cls.baseline_version_headset = zone_true_wireless.baseline_device_version
        cls.target_version_headset = zone_true_wireless.target_device_version
        cls.file_path_headset = os.path.join(
            DIR_PATH, f"Zaxxon_v00.00.0{cls.baseline_version_headset}_encrypted_ota.bin"
        )
        cls.baseline_version_dongle = zone_true_wireless.baseline_dongle_version
        cls.target_version_dongle = zone_true_wireless.target_dongle_version
        cls.file_path_dongle = os.path.join(
            DIR_PATH, f"ZAXXON_SUC_{cls.baseline_version_dongle}.dfu"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            S3_FOLDER, cls.file_path_headset, cls.file_path_dongle
        )

    @parameterized.expand([(x,) for x in range(1, zone_true_wireless.repeats + 1)])
    def test_208_VC_58903_upgrade_downgrade_zonetruewireless_firmware_dongleSUC_connection(
        self, retry
    ):
        """
        Scenario:
        1. Downgrade BTC Dongle via Easter Egg.
        Downgrade Earbuds via Easter Egg.
        2. Update BTC Dongle and Earbuds via OTA.
        """
        Report.logInfo(f"Try number: {retry}")

        try:
            fw_update = FirmwareUpdate(
                retry=retry,
                test_entity=self,
                device_name=self.device_name,
                baseline_version_device=self.baseline_version_headset,
                baseline_version_receiver=self.baseline_version_dongle,
                target_version_device=self.target_version_headset,
                target_version_receiver=self.target_version_dongle,
                file_path_device=self.file_path_headset,
                file_path_receiver=self.file_path_dongle,
                tune_env=tune_env,
                timeout=2000,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(
        UpdateZoneTrueWirelessDongleSUCConnection
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
