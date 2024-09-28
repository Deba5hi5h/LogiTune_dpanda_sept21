import os
import unittest

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.headset.headset_ui_methods import TuneHeadsetMethods, TuneHeadsetPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType


class Zone750(UIBase):
    """
    Test class containing UI tests scenarios for Zone 750 headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins \
            import is_acroname_available, zone_750
        tune_env = zone_750.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters \
            import tune_env, is_acroname_available, zone_750

    device_name = zone_750.device_name
    ota_api_product_name = zone_750.ota_api_product_name
    baseline_device_version = zone_750.baseline_device_version
    target_device_version = zone_750.target_device_version
    repeats = zone_750.repeats
    S3_FOLDER = "Logitech_Zone_750"
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
        super(Zone750, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(
            self.DIR_PATH, f'zone750_headset_{self.baseline_device_version}.rfw'
        )
        file_path_target = os.path.join(
            self.DIR_PATH, f'zone750_headset_{self.target_device_version}.rfw'
        )
        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(
            self.S3_FOLDER, file_path_baseline, file_path_target)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            file_path_device=file_path_baseline,
            file_path_target=file_path_target,
            tune_env=self.tune_env,
            ota_api_product_name=self.ota_api_product_name
        )

        return fw_update, file_path_baseline, file_path_target

    def test_1001_VC_70903_connect_headset_zone_750(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name)

    def test_1002_VC_70904_firmware_update_headset_zone_750(
            self) -> None:
        """
        Test method to verify firmware update.
        """
        fw_update, *_ = self.prepare_update_items()
        fw_update.update()

    def test_1003_VC_70905_sidetone_headset_zone_750(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.device.tc_sidetone(self.conn_type)

    def test_1004_VC_103452_check_default_presets_values_zone_750(self) -> None:
        """
        Test to verify default equalizer preset's values.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_check_default_presets_values()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1005_VC_112771_add_and_delete_custom_presets_zone_750(self) -> None:
        """
        Test to verify if adding and deleting custom presets works correctly.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_add_and_delete_custom_presets()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1006_VC_112772_check_max_presets_prompt_zone_750(self) -> None:
        """
        Test to verify if max presets prompt occurs.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_check_max_custom_presets_prompt()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1007_VC_112773_max_preset_name_input_zone_750(self):
        """
        Test to verify maximum length of custom equalizer preset name.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_max_preset_name_length()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1008_VC_70906_rotate_to_mute_headset_zone_750(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_rotate_to_mute(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_1009_VC_70907_enable_voice_prompts_to_mute_headset_zone_750(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(
            device_name=self.device_name, conn_type=self.conn_type)

    def test_1010_VC_70908_about_the_headset_to_mute_headset_zone_750(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_1011_VC_70909_factory_reset_to_mute_headset_zone_750(self) -> None:
        """
        Test method to verify default values after factory reset.
        """
        self.tune_methods.tc_factory_reset_wired_headset(
            device_name=self.device_name)

    def test_1012_VC_103455_headset_diagnostics_zone_750(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_1013_VC_112533_parameters_persistency_after_reconnect_zone_750(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(
            headset_name=self.device_name, tune_app=self.tune_app, wired=True)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)


if __name__ == "__main__":
    unittest.main()
