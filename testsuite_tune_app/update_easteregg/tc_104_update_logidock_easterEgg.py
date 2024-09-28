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
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import logi_dock
    tune_env = logi_dock.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, logi_dock

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logi_Dock"
REPEATS = logi_dock.repeats


class UpdateLogiDock(FwuStressBase):
    """
    Suite class for Logi Dock FWU tests via EasterEgg.
    """
    device_name = logi_dock.device_name
    ota_api_product_name = logi_dock.ota_api_product_name
    baseline_device_version = logi_dock.baseline_device_version
    target_device_version = logi_dock.target_device_version

    conn_type = ConnectionType.usb_dock
    file_path_target = None
    file_path_baseline = None


    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateLogiDock, cls).setUpClass()

        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        logi_dock.is_initialized()

        cls.file_path_baseline = os.path.join(DIR_PATH, f"qbert-{cls.baseline_device_version}.bin")
        cls.file_path_target = os.path.join(DIR_PATH, f"qbert-{cls.target_device_version}.bin")

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            S3_FOLDER, cls.file_path_baseline, cls.file_path_target
        )

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateLogiDock, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_104_VC_58907_update_firmware_logi_dock(self, retry):
        """
        Scenario:
        1. Downgrade Logi Dock  via Easter Egg.
        2. Update Logi Dock via OTA.
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
                file_path_target=self.file_path_target,
                easter_egg_on_second_update=True,
                tune_env=tune_env,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateLogiDock)
    unittest.main(warnings="ignore")
    unittest.TextTestRunner(verbosity=2).run(suite)
