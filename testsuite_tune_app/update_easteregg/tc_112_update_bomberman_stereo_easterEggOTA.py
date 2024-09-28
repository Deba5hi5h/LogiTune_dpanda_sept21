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
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import bomberman_stereo

    tune_env = bomberman_stereo.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, bomberman_stereo

S3_FOLDER = "Bomberman/Stereo"
log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = bomberman_stereo.repeats

class UpdateBombermanStereo(FwuStressBase):
    """
    Suite class for Bomberman Stereo FWU tests via EasterEgg and OTA.
    """

    file_path = None
    device_name = bomberman_stereo.device_name
    ota_api_product_name = bomberman_stereo.ota_api_product_name
    baseline_device_version = bomberman_stereo.baseline_device_version
    target_device_version = bomberman_stereo.target_device_version
    conn_type = ConnectionType.dongle

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateBombermanStereo, cls).setUpClass()
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        bomberman_stereo.is_initialized()

        cls.file_path = os.path.join(
            DIR_PATH, f"Bomberman_Stereo_V{cls.baseline_device_version}.rfw"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateBombermanStereo, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, bomberman_stereo.repeats + 1)])
    def test_112_VC_138721_update_firmware_bomberman_stereo_headset(self, retry):
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateBombermanStereo)
    unittest.TextTestRunner(verbosity=2).run(suite)
