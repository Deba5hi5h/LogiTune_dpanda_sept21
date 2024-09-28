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

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_950
    tune_env = zone_950.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, zone_950

REPEATS = zone_950.repeats
S3_HEADSET_FOLDER = "Cybermorph"
S3_DONGLE_FOLDER = "Quadrun"

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class UpdateZone950QuadrunDongle(FwuStressBase):
    """
    Suite class for Zone 950 connected via dongle FWU tests via EasterEgg and OTA.
    """

    file_path_dongle = None
    file_path_headset = None
    baseline_version_dongle = None
    baseline_version_headset = None
    device_name = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateZone950QuadrunDongle, cls).setUpClass()
        cls.device_name = zone_950.device_name
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        zone_950.is_initialized()
        cls.baseline_version_headset = zone_950.baseline_device_version
        cls.baseline_version_tahiti = zone_950.baseline_tahiti_version
        cls.target_version_headset = zone_950.target_device_version
        cls.target_version_tahiti = zone_950.target_tahiti_version
        cls.file_path_headset = os.path.join(
            DIR_PATH, f"cybermorph_v{cls.baseline_version_headset}_xxx_v{cls.baseline_version_tahiti}.bin"
        )
        cls.file_path_tahiti = os.path.join(
            DIR_PATH, f"tahiti_v{cls.baseline_version_headset}_xxx_v{cls.baseline_version_tahiti}.bin"
        )
        cls.baseline_version_dongle = zone_950.baseline_dongle_version
        cls.target_version_dongle = zone_950.target_dongle_version
        cls.file_path_dongle = os.path.join(
            DIR_PATH,
            f"Quadrun_PB1_Release_Version_{cls.baseline_version_dongle}_DFU_image.bin"
        )

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_HEADSET_FOLDER,
                                                cls.file_path_headset, cls.file_path_tahiti)
        t_files.prepare_firmware_files_for_test(S3_DONGLE_FOLDER,
                                                cls.file_path_dongle)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateZone950QuadrunDongle, cls).tearDownClass()

    @parameterized.expand([(x, ) for x in range(1, REPEATS + 1)])
    def test_215_VC_102798_update_firmware_zone_950_headset_and_dongle(self, retry):
        """
        Scenario:
        1. Downgrade Dongle via Easter Egg.
        Downgrade Headset via Easter Egg.
        2. Update Dongle and Headset via OTA.
        """
        Report.logInfo(f"Try number: {retry}")

        try:
            fw_update = FirmwareUpdate(
                retry=retry,
                test_entity=self,
                device_name=self.device_name,
                baseline_version_device=self.baseline_version_headset,
                baseline_version_tahiti=self.baseline_version_tahiti,
                baseline_version_receiver=self.baseline_version_dongle,
                target_version_device=self.target_version_headset,
                target_version_tahiti=self.target_version_tahiti,
                target_version_receiver=self.target_version_dongle,
                file_path_device=self.file_path_headset,
                file_path_tahiti=self.file_path_tahiti,
                file_path_receiver=self.file_path_dongle,
                tune_env=tune_env,
                save_pass_logs=True,
                timeout=2500,
                jenkins_configuration=JENKINS_FWU_CONFIG,
            )
            fw_update.update_cybermorph_components()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(
        UpdateZone950QuadrunDongle)
    unittest.TextTestRunner(verbosity=2).run(suite)
