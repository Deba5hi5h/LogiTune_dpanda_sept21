import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from firmware_tunes.build_types import GauguinBuildType
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, gauguin

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_Gauguin"


class UpdateGauguinViaEasterEgg(FwuStressBase):
    """
    Suite class for Brio 505 FWU tests via EasterEgg.
    """

    file_path_target = None
    file_path_baseline = None
    baseline_version = None
    target_version = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateGauguinViaEasterEgg, cls).setUpClass()
        cls.device_name = gauguin.device_name
        build_type = GauguinBuildType.USER
        gauguin.is_initialized()
        cls.baseline_version = gauguin.baseline_device_version
        cls.target_version = gauguin.target_device_version

        global_variables.test_category = f'FW Update Stress {cls.device_name}'

        cls.file_path_baseline = os.path.join(
            DIR_PATH, f"{build_type.value}{cls.baseline_version}.bin"
        )
        cls.file_path_target = os.path.join(
            DIR_PATH, f"{build_type.value}{cls.target_version}.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            S3_FOLDER, cls.file_path_baseline, cls.file_path_target
        )

    @parameterized.expand([(x,) for x in range(1, gauguin.repeats + 1)])
    def test_105_VC_69919_update_gauguin(self, retry):
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
                baseline_version_device=self.baseline_version,
                target_version_device=self.target_version,
                file_path_device=self.file_path_baseline,
                file_path_target=self.file_path_target,
                easter_egg_on_second_update=True,
                tune_env=tune_env,
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateGauguinViaEasterEgg)
    unittest.TextTestRunner(verbosity=2).run(suite)
