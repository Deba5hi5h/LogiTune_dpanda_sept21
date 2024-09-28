import logging
import os
import sys
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base import global_variables
from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from testsuite_tune_app.update_easteregg.device_parameters import tune_env, degas

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
DIR_UTILS_PATH = os.path.join(directory, "firmware_tunes", "utils", "degas")
S3_FOLDER = "Logitech_Degas"


class UpdateDegasViaEasterEgg(FwuStressBase):
    """
    Suite class for Brio 305 FWU tests via EasterEgg.
    """
    device_name = degas.device_name
    ota_api_product_name = degas.ota_api_product_name
    file_path_baseline = None
    file_path_target = None


    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateDegasViaEasterEgg, cls).setUpClass()
        _create_config_file_if_not_exists()
        degas.is_initialized()

        cls.baseline_version = degas.baseline_device_version
        cls.target_version = degas.target_device_version

        global_variables.test_category = f'FW Update Stress {cls.device_name}'

        cls.file_path_baseline = os.path.join(
            DIR_PATH, f"Degas_{cls.baseline_version}.rfw"
        )
        cls.file_path_target = os.path.join(
            DIR_PATH, f"Degas_{cls.target_version}.rfw"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            S3_FOLDER, cls.file_path_baseline, cls.file_path_target
        )

    @parameterized.expand([(x,) for x in range(1, degas.repeats + 1)])
    def test_106_VC_XXXXX_update_degas(self, retry):
        """
        Scenario:
        1. Downgrade Degas camera via Easter Egg.
        2. Update camera via Easter Egg.
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


def _create_config_file_if_not_exists():
    file = 'tune-features.cfg'
    if 'dar' in sys.platform:
        file_path = os.path.join(r'/Applications', file)

        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    file.write('local_update_enabled=true')
                Report.logInfo(f'Config file has been created!')
            except PermissionError as e:
                Report.logInfo(f'No permissions to create file in directory: {file_path}')
                raise e
    else:
        file_path = os.path.join(r'C:\Program Files (x86)', file)

        if not os.path.exists(file_path):
            _degas_util_script = os.path.join(DIR_UTILS_PATH, "config_file.bat")
            os.system(_degas_util_script)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateDegasViaEasterEgg)
    unittest.TextTestRunner(verbosity=2).run(suite)
