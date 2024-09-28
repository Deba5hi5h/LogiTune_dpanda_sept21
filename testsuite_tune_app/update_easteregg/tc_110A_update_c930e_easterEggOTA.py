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
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import c930e
    tune_env = c930e.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, c930e

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_C930e"
REPEATS = c930e.repeats


class UpdateC930e(FwuStressBase):
    """
    Suite class for C930e FWU tests via EasterEgg and OTA.
    Applied from LogiTune 3.2.X
    """
    device_name = c930e.device_name
    ota_api_product_name = c930e.ota_api_product_name
    baseline_device_version = c930e.baseline_device_version
    target_device_version = c930e.target_device_version
    camera_file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateC930e, cls).setUpClass()

        c930e.is_initialized()

        cls.camera_file_path = os.path.join(
            DIR_PATH, f"Thunder_Scorpio_User_{cls.baseline_device_version}.bin"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.camera_file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateC930e, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_105_VC_58889_update_firmware_c930e_webcam(self, retry):
        """
        Scenario:
        1. Downgrade C930e camera via Easter Egg.
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
                file_path_device=self.camera_file_path,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateC930e)
    unittest.TextTestRunner(verbosity=2).run(suite)
