import os
import unittest

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.headset.headset_ui_methods import TuneHeadsetMethods, TuneHeadsetPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType


class BombermanStereo(UIBase):
    """
    Test class containing UI tests scenarios for Bomberman Stereo headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import bomberman_stereo, is_acroname_available
        tune_env = bomberman_stereo.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters \
            import tune_env, is_acroname_available, bomberman_stereo

    device_name = bomberman_stereo.device_name
    ota_api_product_name = bomberman_stereo.ota_api_product_name
    baseline_device_version = bomberman_stereo.baseline_device_version
    target_device_version = bomberman_stereo.target_device_version
    repeats = bomberman_stereo.repeats
    S3_FOLDER = "Bomberman/Stereo"
    conn_type = ConnectionType.dongle

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device = TuneHeadsetMethods(device_name, tune_app)
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(BombermanStereo, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(
            self.DIR_PATH, f"Bomberman_Stereo_V{self.baseline_device_version}.rfw"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path_baseline)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            file_path_device=file_path_baseline,
            tune_env=self.tune_env,
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_baseline

    def test_4301_VC_139090_connect_headset_bomberman_stereo(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name)

    def test_4302_VC_139091_firmware_update_headset_bomberman_stereo(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_4303_VC_139092_sidetone_headset_bomberman_stereo(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.tune_methods.tc_sidetone(device_name=self.device_name,
                                      conn_type=self.conn_type)

    def test_4304_VC_139088_mic_level_bomberman_stereo(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_4305_VC_139093_enable_voice_prompts_headset_bomberman_stereo(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(
            device_name=self.device_name, conn_type=self.conn_type)

    def test_4306_VC_139089_anti_startle_bomberman_stereo(self) -> None:
        """
        Test method to modify and verify Health and Safety feature.
        """
        self.tune_methods.tc_health_and_safety_anti_startle(device_name=self.device_name,
                                                            conn_type=self.conn_type,
                                                            is_dashboard_feature=True)

    def test_4307_VC_139094_about_the_headset_to_mute_headset_bomberman_stereo(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_4308_VC_139095_factory_reset_to_mute_headset_bomberman_stereo(
            self) -> None:
        """
        Test method to verify default values after factory reset.
        """
        self.tune_methods.tc_factory_reset_wired_headset(
            device_name=self.device_name)

    def test_4309_VC_139096_headset_diagnostics_bomberman_stereo(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_4310_VC_139097_parameters_persistency_after_reconnect_bomberman_stereo(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(
            headset_name=self.device_name, tune_app=self.tune_app, wired=True)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)

if __name__ == "__main__":
    unittest.main()
