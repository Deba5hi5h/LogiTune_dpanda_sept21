import logging
import os
import unittest

from parameterized import parameterized

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from base.fwu_stress_base import FwuStressBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

if JENKINS_FWU_CONFIG:
    from testsuite_tune_app.update_easteregg.device_parameters_jenkins import litra_beam
    tune_env = litra_beam.jenkins_tune_env
else:
    from testsuite_tune_app.update_easteregg.device_parameters import tune_env, litra_beam

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
S3_FOLDER = "Logitech_Litra_Beam"
REPEATS = litra_beam.repeats


class UpdateLitraBeam(FwuStressBase):
    """
    Suite class for Litra Beam FWU tests via EasterEgg and OTA.
    """
    device_name = litra_beam.device_name
    ota_api_product_name = litra_beam.ota_api_product_name
    baseline_device_version = litra_beam.baseline_device_version
    target_device_version = litra_beam.target_device_version
    conn_type = ConnectionType.usb_dock
    file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateLitraBeam, cls).setUpClass()
        cls.device_name = litra_beam.device_name

        litra_beam.is_initialized()

        if JENKINS_FWU_CONFIG:
            connect_device(device_name=cls.device_name)

        cls.file_path = os.path.join(
            DIR_PATH, f"imola-nrf52820-firmware-{cls.baseline_device_version}-signed.dfu"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(S3_FOLDER, cls.file_path)

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            disconnect_device(device_name=cls.device_name)
        super(UpdateLitraBeam, cls).tearDownClass()

    @parameterized.expand([(x,) for x in range(1, REPEATS + 1)])
    def test_108A_VC_100789_update_firmware_litra_beam(self, retry):
        """
        Scenario:
        1. Downgrade Litra Beam via Easter Egg.
        2. Update Litra Beam via OTA.
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
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateLitraBeam)
    unittest.TextTestRunner(verbosity=2).run(suite)
