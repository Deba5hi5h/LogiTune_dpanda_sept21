import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.device_parameters_utilities import TuneEnv
from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from common.framework_params import JENKINS_FWU_CONFIG, JENKINS_REPEATS
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_750

    tune_env = zone_750.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_750

S3_FOLDER = "Logitech_Zone_750"
log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = zone_750.repeats


class UpdateZone750(FwuStressBase):
    """
    Suite class for Zone 750 FWU tests via EasterEgg and OTA.
    """

    file_path = None
    device_name = zone_750.device_name
    ota_api_product_name = zone_750.ota_api_product_name
    baseline_device_version = zone_750.baseline_device_version
    target_device_version = zone_750.target_device_version
    conn_type = ConnectionType.dongle

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZone750, cls).setUpClass()
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_750.is_initialized()

        cls.file_path = os.path.join(
            DIR_PATH, f"zone750_headset_{cls.baseline_device_version}.rfw"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateZone750, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_101_VC_58894_update_firmware_zone750_headset(self, retry):
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZone750)
    unittest.TextTestRunner(verbosity=2).run(suite)
