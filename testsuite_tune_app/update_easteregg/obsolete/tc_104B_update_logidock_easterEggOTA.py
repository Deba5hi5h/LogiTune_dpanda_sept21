import logging
import os
import time
import unittest

from parameterized import parameterized

from base.fwu_stress_base import FwuStressBase
from extentreport.report import Report
from common.platform_helper import Device
from apps.tune.TuneElectron import TuneElectron, disconnect_all

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
directory, _ = os.path.split(directory)

DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg", "qbert")


class UpdateLogiDock(FwuStressBase):

    @parameterized.expand([(x,) for x in range(1, 8)])
    def test_104_VC_58907_update_logi_dock(self, retry):
        """
                Scenario:
                1. Downgrade Lodi Dock via Easter Egg.
                2. Update Logi Dock via OTA.
        """
        device_name = "Logi Dock"
        device = Device.DOCK
        Report.logInfo(f"Try number: {retry}")

        baseline_version = "1.0.94"
        target_version = "1.0.97"
        file_path = os.path.join(DIR_PATH, f"qbert-{baseline_version}.bin")

        try:
            disconnect_all()
            time.sleep(3)

            self.tunesApp = TuneElectron()
            modify_flag = True if retry == 1 else False
            self.tunesApp.open_tune_app(modify_json=modify_flag, clean_logs=True)
            self.tunesApp.open_device_in_my_devices_tab(device_name)
            self.tunesApp.open_about_the_device()

            if not self.tunesApp.is_same_version(device_name=device_name, device=baseline_version)[0]:
                Report.logInfo(f"Start LogiDock update via easterEgg to: {baseline_version}")
                version = self.tunesApp.update_firmware_with_easter_egg(
                    device_file_path=file_path,
                    device_name=device_name,
                    device=device,
                    timeout=500,
                )
                Report.logInfo(f"Logi Dock version after easterEgg: {version}", screenshot=True)
                assert baseline_version in version, Report.logFail(f"{baseline_version} not in {version}")
                Report.logPass("Downgrade via Easter Egg finished with success.")
                self.tunesApp.close_tune_app()

                time.sleep(5)
                self.tunesApp.open_tune_app(clean_logs=True)
                self.tunesApp.open_device_in_my_devices_tab(device_name)
                self.tunesApp.open_about_the_device()
            else:
                Report.logInfo(f"LogiDock already has correct version: {baseline_version}")
            Report.logInfo(f"Start update via OTA to: {target_version}", screenshot=True)
            updated_version = self.tunesApp.start_update_from_device_tab(
                device_name=device_name,
                device=device
            )
            Report.logInfo(f"Logi Dock version after OTA: {updated_version}", screenshot=True)
            assert target_version in updated_version, Report.logFail(f"{target_version} not in {updated_version}")
            Report.logPass("Update via OTA finished with success.")

        except Exception as e:
            self.tunesApp.save_logitune_logs_in_testlogs(testlogs_path=self.logdirectory,
                                                         test_name=unittest.TestCase.id(self))
            Report.logException(str(e))
        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateLogiDock)
    unittest.TextTestRunner(verbosity=2).run(suite)
