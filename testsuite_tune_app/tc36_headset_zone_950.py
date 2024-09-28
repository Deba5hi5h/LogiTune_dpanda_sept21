import os
import time
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
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_950 import \
    MAX_LEN_NAME


class Zone950(UIBase):
    """
    Test class containing UI tests scenarios for Zone 950 headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import \
            is_acroname_available, zone_950
        tune_env = zone_950.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import \
            tune_env, is_acroname_available, zone_950

    device_name = zone_950.device_name
    ota_api_product_name = zone_950.ota_api_product_name
    baseline_device_version = zone_950.baseline_device_version
    baseline_tahiti_version = zone_950.baseline_tahiti_version
    baseline_dongle_version = zone_950.baseline_dongle_version
    target_device_version = zone_950.target_device_version
    target_tahiti_version = zone_950.target_tahiti_version
    target_dongle_version = zone_950.target_dongle_version
    repeats = zone_950.repeats
    S3_FOLDER = "Cybermorph"
    S3_DONGLE_FOLDER = "Quadrun"
    conn_type = ConnectionType.dongle

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device = TuneHeadsetMethods(device_name, tune_app)
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def tearDownClass(cls) -> None:
        if JENKINS_FWU_CONFIG:
            cls.tune_methods.set_never_sleep_timer(product_string=cls.device_name, conn_type=cls.conn_type)
            time.sleep(3)
            cls.tune_methods.set_device_name_over_api(product_string=cls.device_name, conn_type=cls.conn_type)
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(Zone950, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"cybermorph_v{self.baseline_device_version}_xxx_v{self.baseline_tahiti_version}.bin"
        )
        file_path_tahiti = os.path.join(
            self.DIR_PATH, f"tahiti_v{self.baseline_device_version}_xxx_v{self.baseline_tahiti_version}.bin"
        )
        file_path_dongle = os.path.join(
            self.DIR_PATH,
            f"Quadrun_PB1_Release_Version_{self.baseline_dongle_version}_DFU_image.bin"
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path_headset, file_path_tahiti)
        t_files.prepare_firmware_files_for_test(self.S3_DONGLE_FOLDER, file_path_dongle)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            baseline_version_tahiti=self.baseline_tahiti_version,
            baseline_version_receiver=self.baseline_dongle_version,
            target_version_device=self.target_device_version,
            target_version_tahiti=self.target_tahiti_version,
            target_version_receiver=self.target_dongle_version,
            file_path_device=file_path_headset,
            file_path_tahiti=file_path_tahiti,
            file_path_receiver=file_path_dongle,
            tune_env=self.tune_env,
            timeout=2500,
            save_pass_logs=True,
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_headset, file_path_tahiti, file_path_dongle

    def _back_button_universal_click(self) -> None:
        """
        Method that checks what back button is used in current view and click
        """
        if self.tune_app.verify_back_button_cybermorph():
            self.tune_app.click_back_button_cybermorph()
        elif self.tune_app.verify_back_to_device():
            self.tune_app.click_back_to_device()
        elif self.tune_app.verify_button_functions_back():
            self.tune_app.click_button_functions_back()

    def test_3601_VC_102102_connect_headset_zone_950(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_3602_VC_102103_firmware_update_headset_zone_950(self) -> None:
        """
        Test method to verify firmware update.
        """
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update_cybermorph_components()
        except Exception as ex:
            Report.logException(str(ex))

    def test_3603_VC_103032_anc_levels_zone_950(self) -> None:
        """
        Test method to modify parameters and verify ANC feature.
        """
        self.tune_methods.tc_anc_buttons(device_name=self.device_name,
                                         conn_type=self.conn_type)

    def test_3604_VC_102104_sidetone_headset_zone_950(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.device.tc_sidetone(self.conn_type)

    def test_3605_VC_102105_mic_level_zone_950(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.device.tc_mic_level()

    def test_3606_VC_102106_advanced_call_clarity_zone_950(
            self) -> None:
        """
        Test method to modify and verify Advanced Call Clarity feature.
        """
        self.tune_methods.tc_advanced_call_clarity(device_name=self.device_name,
                                                   conn_type=self.conn_type)

    def test_3607_VC_102107_personal_eq_value_check(self) -> None:
        Report.logSkip("Feature not ready.")
        self.skipTest("Feature not ready.")

    def test_3608_VC_102108_check_default_presets_values_zone_950(self) -> None:
        """
        Test to verify default equalizer preset's values.
        """
        self.device.tc_equalizer_check_default_presets_values()

    def test_3609_VC_112801_add_and_delete_custom_presets_zone_950(self) -> None:
        """
        Test to verify if adding and deleting custom presets works correctly.
        """
        self.device.tc_equalizer_add_and_delete_custom_presets()

    def test_3610_VC_112802_check_max_presets_prompt_zone_950(self) -> None:
        """
        Test to verify if max presets prompt occurs.
        """
        self.device.tc_equalizer_check_max_custom_presets_prompt()

    def test_3611_VC_112803_max_preset_name_input_zone_950(self):
        """
        Test to verify maximum length of custom equalizer preset name.
        """
        self.device.tc_equalizer_max_preset_name_length()

    def test_3612_VC_102109_health_and_safety_anti_startle_zone_950(self) -> None:
        """
        Test method to modify and verify Health and Safety feature.
        """
        self.tune_methods.tc_health_and_safety_anti_startle(device_name=self.device_name,
                                                            conn_type=self.conn_type)

    def test_3613_VC_102110_health_and_safety_noise_exposure_zone_950(self) -> None:
        """
        Test method to modify and verify Health and Safety feature.
        """
        self.tune_methods.tc_health_and_safety_noise_exposure(device_name=self.device_name,
                                                              conn_type=self.conn_type)

    def test_3614_VC_102111_device_name_zone_950(self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = MAX_LEN_NAME
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_3615_VC_102112_sleep_timeout_zone_950(self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_sleep_settings(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_3616_VC_102113_rotate_to_mute_headset_zone_950(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_rotate_to_mute(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_3617_VC_102114_anc_button_options_zone_950(self) -> None:
        """
        Test method to modify and verify ANC button options feature.
        """
        self.tune_methods.tc_anc_button_options(device_name=self.device_name,
                                                conn_type=self.conn_type)

    def test_3618_VC_102115_on_head_detection_auto_mute_zone_950(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto Mute feature.
        """
        self.tune_methods.tc_on_head_detection_auto_mute(device_name=self.device_name,
                                                         conn_type=self.conn_type)

    def test_3619_VC_102116_on_head_detection_auto_answer_zone_950(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto Answer feature.
        """
        self.tune_methods.tc_on_head_detection_auto_answer(device_name=self.device_name,
                                                           conn_type=self.conn_type)

    def test_3620_VC_102117_on_head_detection_auto_pause_zone_950(self) -> None:
        """
        Test method to modify and verify On Head detection: Auto pause feature.
        """
        self.tune_methods.tc_on_head_detection_auto_pause(device_name=self.device_name,
                                                          conn_type=self.conn_type)

    def test_3621_VC_102119_voice_prompts_headset_zone_950(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts_3_levels(device_name=self.device_name,
                                                    conn_type=self.conn_type)

    def test_3622_VC_102121_connected_devices_zone_950(self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        receiver_name = "Zone Receiver"
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_3623_VC_102118_touch_button_zone_950(self) -> None:
        """
        Test method change and verify touch button feature.
        """
        self.tune_methods.tc_touch_pad(device_name=self.device_name,
                                       conn_type=self.conn_type)

    def test_3624_VC_102120_headset_language_zone_950(self) -> None:
        """
        Test method change and verify headset language feature.
        """
        self.tune_methods.tc_cybermorph_language_selection(device_name=self.device_name)

    def test_3625_VC_103739_headset_diagnostics_zone_950(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_3626_VC_102122_about_the_headset_to_mute_headset_zone_950(self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_3627_VC_102123_factory_reset_to_mute_zone_950(self) -> None:
        """
        Test method to verify Factory Reset feature.
        """
        Report.logSkip("TBD")
        self.skipTest("TBD")
        self.tune_methods.tc_factory_reset_wireless_headset(device_name=self.device_name)

    def test_3628_VC_112543_parameters_persistency_after_reconnect_zone_950(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(headset_name=self.device_name, tune_app=self.tune_app)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)


if __name__ == "__main__":
    unittest.main()
