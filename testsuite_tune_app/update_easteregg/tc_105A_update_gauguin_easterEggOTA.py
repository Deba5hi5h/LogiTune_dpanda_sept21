import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.device_parameters_utilities import TuneEnv
from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base.fwu_stress_base import FwuStressBase
from common.framework_params import JENKINS_FWU_CONFIG, JENKINS_REPEATS
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from firmware_tunes.build_types import GauguinBuildType

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import gauguin

    tune_env = gauguin.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, gauguin

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_Gauguin"


class UpdateGauguin(FwuStressBase):
    """
    Suite class for Brio 505 FWU tests via EasterEgg and OTA.
    """
    device_name = gauguin.device_name
    ota_api_product_name = gauguin.ota_api_product_name
    baseline_device_version = gauguin.baseline_device_version
    target_device_version = gauguin.target_device_version
    repeats = gauguin.repeats
    build_type = GauguinBuildType.USER
    file_path_baseline = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateGauguin, cls).setUpClass()

        build_type = GauguinBuildType.USER

        gauguin.is_initialized()

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        cls.file_path_baseline = os.path.join(
            DIR_PATH, f"{build_type.value}{cls.baseline_device_version}.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path_baseline)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateGauguin, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, repeats + 1)])
    def test_105_VC_69919_update_firmware_gauguin_webcam(self, retry):
        """
        Scenario:
        1. Downgrade Gauguin camera via Easter Egg.
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
                file_path_device=self.file_path_baseline,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateGauguin)
    unittest.TextTestRunner(verbosity=2).run(suite)
