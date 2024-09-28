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
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_wired

    tune_env = zone_wired.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wired

S3_FOLDER = "Logitech_Zone_Wired"
log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = zone_wired.repeats

class UpdateZoneWired(FwuStressBase):
    """
    Suite class for Zone Wired FWU tests via EasterEgg and OTA.
    """

    file_path = None
    device_name = zone_wired.device_name
    ota_api_product_name = zone_wired.ota_api_product_name
    baseline_device_version = zone_wired.baseline_device_version
    target_device_version = zone_wired.target_device_version
    conn_type = ConnectionType.dongle

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneWired, cls).setUpClass()
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_wired.is_initialized()

        cls.file_path = os.path.join(
            DIR_PATH, f"zonewired_headset_{cls.baseline_device_version}.rfw"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateZoneWired, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_102_VC_58891_update_firmware_zone_wired_headset(self, retry):
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneWired)
    unittest.TextTestRunner(verbosity=2).run(suite)
