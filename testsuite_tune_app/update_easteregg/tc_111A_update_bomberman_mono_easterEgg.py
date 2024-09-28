import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, bomberman_mono

S3_FOLDER = "Bomberman/Mono"

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")


class UpdateBombermanMono(FwuStressBase):
    """
    Suite class for Bomberman Mono connected over BT FWU tests via EasterEgg and OTA.
    """

    baseline_version_headset = None
    target_version_headset = None
    file_path_headset = None
    file_path_target = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateBombermanMono, cls).setUpClass()
        cls.device_name = bomberman_mono.device_name
        global_variables.test_category = f'FW Update Stress {cls.device_name}'
        bomberman_mono.is_initialized(skip_dongle=True)
        cls.baseline_version_headset = bomberman_mono.baseline_device_version
        cls.target_version_headset = bomberman_mono.target_device_version
        cls.file_path_headset = os.path.join(
            DIR_PATH, f"Bomberman_Mono_V{cls.baseline_version_headset}.rfw"
        )
        cls.file_path_target = os.path.join(
            DIR_PATH, f"Bomberman_Mono_V{cls.target_version_headset}.rfw"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path_headset, cls.file_path_target)

    @parameterized.expand([(x,) for x in range(1, bomberman_mono.repeats + 1)])
    def test_111A_VC_XXXXXX_update_bomberman_mono(self, retry):
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
                baseline_version_device=self.baseline_version_headset,
                target_version_device=self.target_version_headset,
                file_path_device=self.file_path_headset,
                file_path_target=self.file_path_target,
                easter_egg_on_second_update=True,
                tune_env=tune_env,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateBombermanMono)
    unittest.TextTestRunner(verbosity=2).run(suite)
