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
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import bomberman_mono

    tune_env = bomberman_mono.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, bomberman_mono

S3_FOLDER = "Bomberman/Mono"
log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = bomberman_mono.repeats

class UpdateBombermanMono(FwuStressBase):
    """
    Suite class for Bomberman Mono FWU tests via EasterEgg and OTA.
    """

    file_path = None
    device_name = bomberman_mono.device_name
    ota_api_product_name = bomberman_mono.ota_api_product_name
    baseline_device_version = bomberman_mono.baseline_device_version
    target_device_version = bomberman_mono.target_device_version
    conn_type = ConnectionType.dongle

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateBombermanMono, cls).setUpClass()
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        bomberman_mono.is_initialized()

        cls.file_path = os.path.join(
            DIR_PATH, f"Bomberman_Mono_V{cls.baseline_device_version}.rfw"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateBombermanMono, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, bomberman_mono.repeats + 1)])
    def test_111_VC_138720_update_firmware_bomberman_mono_headset(self, retry):
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
                baseline_version_device=self.baseline_device_version,
                target_version_device=self.target_device_version,
                file_path_device=self.file_path,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateBombermanMono)
    unittest.TextTestRunner(verbosity=2).run(suite)
