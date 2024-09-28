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


class ZoneWiredEarbuds(UIBase):
    """
    Test class containing UI tests scenarios for Zone Wired Earbuds headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import \
            is_acroname_available, zone_wired_earbuds
        tune_env = zone_wired_earbuds.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import \
            tune_env, is_acroname_available, zone_wired_earbuds

    device_name = zone_wired_earbuds.device_name
    ota_api_product_name = zone_wired_earbuds.ota_api_product_name
    baseline_device_version = zone_wired_earbuds.baseline_device_version
    target_device_version = zone_wired_earbuds.target_device_version
    repeats = zone_wired_earbuds.repeats
    S3_FOLDER = "Logitech_Zone_Wired_Earbuds"
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
        super(ZoneWiredEarbuds, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(self.DIR_PATH, f"zonewiredearbuds_headset_{self.baseline_device_version}.rfw")
        file_path_target = os.path.join(self.DIR_PATH, f"zonewiredearbuds_headset_{self.target_device_version}.rfw")

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path_baseline, file_path_target)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            file_path_device=file_path_baseline,
            file_path_target=file_path_target,
            tune_env=self.tune_env,
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_baseline, file_path_target

    def test_1101_VC_70910_connect_headset_zone_wired_earbuds(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name)

    def test_1102_VC_70911_firmware_update_headset_zone_wired_earbuds(self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1103_VC_70912_sidetone_headset_zone_wired_earbuds(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.device.tc_sidetone(self.conn_type)

    def test_1104_VC_103453_check_default_presets_values_zone_wired_earbuds(self) -> None:
        """
        Test to verify default equalizer preset's values.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_check_default_presets_values()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1105_VC_112777_add_and_delete_custom_presets_zone_wired_earbuds(self) -> None:
        """
        Test to verify if adding and deleting custom presets works correctly.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_add_and_delete_custom_presets()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1106_VC_112778_check_max_presets_prompt_zone_wired_earbuds(self) -> None:
        """
        Test to verify if max presets prompt occurs.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_check_max_custom_presets_prompt()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1107_VC_112779_max_preset_name_input_zone_wired_earbuds(self):
        """
        Test to verify maximum length of custom equalizer preset name.
        """
        if get_custom_platform() == "windows":
            self.device.tc_equalizer_max_preset_name_length()
        else:
            Report.logSkip('Equalizer not available on MacOS')
            raise unittest.SkipTest("Equalizer not available on MacOS")

    def test_1108_VC_70914_enable_voice_prompts_to_mute_headset_zone_wired_earbuds(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(
            device_name=self.device_name, conn_type=self.conn_type)

    def test_1109_VC_70915_about_the_headset_to_mute_headset_zone_wired_earbuds(
            self) -> None:
        """
        Test method to verify About the headset page
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_1110_VC_70916_factory_reset_to_mute_headset_zone_wired_earbuds(
            self) -> None:
        """
        Test method to verify default values after factory reset.
        """
        self.tune_methods.tc_factory_reset_wired_headset(
            device_name=self.device_name)

    def test_1111_VC_103456_headset_diagnostics_zone_wired_earbuds(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_1112_VC_112535_parameters_persistency_after_reconnect_zone_wired_earbuds(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(
            headset_name=self.device_name, tune_app=self.tune_app, wired=True)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)


if __name__ == "__main__":
    unittest.main()
