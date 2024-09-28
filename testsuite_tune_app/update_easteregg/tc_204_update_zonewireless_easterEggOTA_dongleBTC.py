import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import connect_device, disconnect_device
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from extentreport.report import Report

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_wireless

    tune_env = zone_wireless.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wireless

S3_FOLDER = "Logitech_Zone_Wireless"
log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = zone_wireless.repeats


class UpdateZoneWirelessDongle(FwuStressBase):
    """
    Suite class for Zone Wireless connected over BT dongle FWU tests via EasterEgg and OTA.
    """
    device_name = zone_wireless.device_name
    ota_api_product_name = zone_wireless.ota_api_product_name
    baseline_device_version = zone_wireless.baseline_device_version
    baseline_dongle_version = zone_wireless.baseline_dongle_version
    target_device_version = zone_wireless.target_device_version
    target_dongle_version = zone_wireless.target_dongle_version

    conn_type = ConnectionType.dongle
    file_path_dongle = None
    file_path_headset = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneWirelessDongle, cls).setUpClass()

        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_wireless.is_initialized()

        cls.file_path_headset = os.path.join(
            DIR_PATH, f"zonewireless_headset_{cls.baseline_device_version}.bin"
        )

        cls.file_path_dongle = os.path.join(
            DIR_PATH, f"zonewireless_dongle_btc_{cls.baseline_dongle_version}.dfu"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            S3_FOLDER, cls.file_path_headset, cls.file_path_dongle
        )

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateZoneWirelessDongle, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_204_VC_58897_update_firmware_zone_wireless_headset_headset_and_dongle(self, retry):
        """
        Scenario:
        1. Downgrade BTC Dongle via Easter Egg.
        Downgrade Headset via Easter Egg.
        2. Update BTC Dongle and Headset via OTA.
        """
        Report.logInfo(f"Try number: {retry}")

        try:
            fw_update = FirmwareUpdate(
                retry=retry,
                test_entity=self,
                device_name=self.device_name,
                baseline_version_device=self.baseline_device_version,
                baseline_version_receiver=self.baseline_dongle_version,
                target_version_device=self.target_device_version,
                target_version_receiver=self.target_dongle_version,
                file_path_device=self.file_path_headset,
                file_path_receiver=self.file_path_dongle,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneWirelessDongle)
    unittest.TextTestRunner(verbosity=2).run(suite)
