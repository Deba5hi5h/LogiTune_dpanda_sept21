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
from firmware_tunes.build_types import MatisseBuildType

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import matisse
    tune_env = matisse.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, matisse

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_Matisse"
REPEATS = matisse.repeats


class UpdateMatisse(FwuStressBase):
    """
    Suite class for Brio Pro 70X FWU tests via EasterEgg and OTA.
    """
    device_name = matisse.device_name
    ota_api_product_name = matisse.ota_api_product_name
    baseline_device_version = matisse.baseline_device_version
    target_device_version = matisse.target_device_version

    build_type = MatisseBuildType.USER
    file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateMatisse, cls).setUpClass()

        matisse.is_initialized()

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        cls.file_path = os.path.join(
            DIR_PATH, f"{cls.build_type.value}{cls.baseline_device_version}.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateMatisse, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_107A_VC_100788_update_firmware_matisse_webcam(self, retry):
        """
        Scenario:
        1. Downgrade Matisse camera via Easter Egg.
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
                file_path_device=self.file_path,
                tune_env=tune_env,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateMatisse)
    unittest.TextTestRunner(verbosity=2).run(suite)
