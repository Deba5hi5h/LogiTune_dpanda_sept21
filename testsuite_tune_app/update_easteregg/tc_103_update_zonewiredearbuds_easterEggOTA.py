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
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_wired_earbuds
    tune_env = zone_wired_earbuds.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_wired_earbuds

S3_FOLDER = "Logitech_Zone_Wired_Earbuds"
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
REPEATS = zone_wired_earbuds.repeats


class UpdateZoneWiredEarbuds(FwuStressBase):
    """
    Suite class for Zone Wired Earbuds FWU tests via EasterEgg and OTA.
    """

    device_name = zone_wired_earbuds.device_name
    ota_api_product_name = zone_wired_earbuds.ota_api_product_name
    baseline_device_version = zone_wired_earbuds.baseline_device_version
    target_device_version = zone_wired_earbuds.target_device_version
    conn_type = ConnectionType.dongle
    file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZoneWiredEarbuds, cls).setUpClass()

        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_wired_earbuds.is_initialized()

        cls.file_path = os.path.join(
            DIR_PATH, f"zonewiredearbuds_headset_{cls.baseline_device_version}.rfw"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateZoneWiredEarbuds, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_103_VC_58895_update_firmware_wired_earbuds(self, retry):
        """
        Scenario:
        1. Downgrade Earbuds via Easter Egg.
        2. Update Earbuds via OTA.
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateZoneWiredEarbuds)
    unittest.TextTestRunner(verbosity=2).run(suite)
