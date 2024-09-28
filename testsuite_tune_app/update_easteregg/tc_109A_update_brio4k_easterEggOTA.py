import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base.fwu_stress_base import FwuStressBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import brio4k

    tune_env = brio4k.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, brio4k

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_Brio"
REPEATS = brio4k.repeats


class UpdateBrio4K(FwuStressBase):
    """
    Suite class for Brio 4K FWU tests via EasterEgg and OTA.
    Applied from LogiTune 3.2.X
    """
    device_name = brio4k.device_name
    ota_api_product_name = brio4k.ota_api_product_name
    baseline_device_version = brio4k.baseline_device_version
    target_device_version = brio4k.target_device_version
    baseline_eeprom_version = brio4k.baseline_eeprom_version
    target_eeprom_version = brio4k.target_eeprom_version
    camera_file_path = None
    eeprom_file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateBrio4K, cls).setUpClass()

        brio4k.is_initialized()

        cls.camera_file_path = os.path.join(
            DIR_PATH, f"webcam_{cls.baseline_device_version}_release.bin"
        )

        if len(cls.baseline_eeprom_version.split('.')) < 3:
            cls.baseline_eeprom_version += '.0'

        cls.eeprom_file_path = os.path.join(
            DIR_PATH, f'eeprom_logitech_{cls.baseline_eeprom_version}.s19'
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.camera_file_path)
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.eeprom_file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateBrio4K, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_105_VC_58888_update_firmware_brio4k_webcam(self, retry):
        """
        Scenario:
        1. Downgrade Brio 4K camera via Easter Egg.
        2. Update camera via OTA.
        """
        Report.logInfo(f"Try number: {retry}")

        try:
            fw_update = FirmwareUpdate(
                retry=retry,
                test_entity=self,
                device_name=self.device_name,
                baseline_version_device=self.baseline_device_version,
                target_version_device=self.target_device_version,
                baseline_version_eeprom=self.baseline_eeprom_version,
                target_version_eeprom=self.target_eeprom_version,
                file_path_device=self.camera_file_path,
                file_path_eeprom=self.eeprom_file_path,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update_camera_components()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateBrio4K)
    unittest.TextTestRunner(verbosity=2).run(suite)
