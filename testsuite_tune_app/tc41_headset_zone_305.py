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

class Zone305(UIBase):
    """
    Test class containing UI tests scenarios for Zone 305 headset.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import \
            is_acroname_available, zone_305
        tune_env = zone_305.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import \
            tune_env, is_acroname_available, zone_305

    device_name = zone_305.device_name
    ota_api_product_name = zone_305.ota_api_product_name
    baseline_device_version = zone_305.baseline_device_version
    baseline_dongle_version = zone_305.baseline_dongle_version
    target_device_version = zone_305.target_device_version
    target_dongle_version = zone_305.target_dongle_version
    dongle_address = zone_305.dongle_address
    repeats = zone_305.repeats
    S3_HEADSET_FOLDER = "Krull"
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
        super(Zone305, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_headset = os.path.join(
            self.DIR_PATH, f"Krull_{self.baseline_device_version}.img")
        file_path_dongle = os.path.join(
            self.DIR_PATH, f"Quadrun_PB1_Release_Version_{self.baseline_dongle_version}_DFU_image.bin")

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_HEADSET_FOLDER, file_path_headset)
        t_files.prepare_firmware_files_for_test(self.S3_DONGLE_FOLDER, file_path_dongle)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            baseline_version_receiver=self.baseline_dongle_version,
            target_version_device=self.target_device_version,
            target_version_receiver=self.target_dongle_version,
            file_path_device=file_path_headset,
            file_path_receiver=file_path_dongle,
            tune_env=self.tune_env,
            jenkins_configuration=JENKINS_FWU_CONFIG,
        )

        return fw_update, file_path_headset, file_path_dongle

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

    def test_4101_VC_138430_connect_headset_zone_305(self) -> None:
        """
        Test method to verify if all device feature are visible after
        reconnecting the device.
        """
        self.tune_methods.tc_connect_headset(device_name=self.device_name, is_wireless=True)

    def test_4102_VC_138429_firmware_update_headset_zone_305(self) -> None:
        """
        Test method to verify firmware update.
        """
        fw_update, *_ = self.prepare_update_items()

        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_4103_VC_138428_sidetone_headset_zone_305(self) -> None:
        """
        Test method to modify parameters and verify sidetone feature.
        """
        self.tune_methods.tc_sidetone(device_name=self.device_name,
                                      conn_type=self.conn_type)

    def test_4104_VC_138423_mic_level_zone_305(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_4105_VC_138422_check_default_presets_values_zone_305(self) -> None:
        """
        Test to verify default equalizer presets' values.
        """
        self.device.tc_equalizer_check_default_presets_values()

    def test_4106_VC_138414_add_and_delete_custom_presets_zone_305(self) -> None:
        """
        Test to verify if adding and deleting custom presets works correctly.
        """
        self.device.tc_equalizer_add_and_delete_custom_presets()

    def test_4107_VC_138415_check_max_presets_prompt_zone_305(self) -> None:
        """
        Test to verify if max presets prompt occurs.
        """
        self.device.tc_equalizer_check_max_custom_presets_prompt()

    def test_4108_VC_138412_max_preset_name_input_zone_305(self) -> None:
        """
        Test to verify maximum length of custom equalizer preset name.
        """
        self.device.tc_equalizer_max_preset_name_length()

    def test_4109_VC_138427_rotate_to_mute_headset_zone_305(self) -> None:
        """
        Test method to modify and verify Rotate to mute feature.
        """
        self.tune_methods.tc_rotate_to_mute(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_4110_VC_138426_enable_voice_prompts_to_mute_headset_zone_305(
            self) -> None:
        """
        Test method to modify and verify Enable Voice Prompts feature.
        """
        self.tune_methods.tc_voice_prompts(device_name=self.device_name,
                                           conn_type=self.conn_type)

    def test_4111_VC_138421_device_name_zone_305(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_4112_VC_138420_sleep_timeout_zone_305(
            self) -> None:
        """
        Test method to modify and verify Sleep timeout feature.
        """
        self.tune_methods.tc_sleep_settings(device_name=self.device_name,
                                            conn_type=self.conn_type)

    def test_4113_VC_138418_connected_devices_zone_305(
            self) -> None:
        """
        Test method to verify Connection priority feature.
        """
        receiver_name = "Zone Receiver"
        self.tune_methods.tc_connected_devices(device_name=self.device_name,
                                               conn_type=self.conn_type,
                                               receiver_name=receiver_name)

    def test_4114_VC_138417_headset_language_zone_305(
            self) -> None:
        """
        Test method change and verify headset language feature.
        """
        test_name = unittest.TestCase.id(self).split('.')[-1]
        self.tune_methods.tc_language_update(device_name=self.device_name, test_name=test_name)

    def test_4115_VC_138416_headset_diagnostics_zone_305(self) -> None:
        """
        Test method to modify and verify Headset Diagnostics feature.
        """
        self.tune_methods.tc_headset_diagnostics(device_name=self.device_name)

    def test_4116_VC_138425_about_the_headset_to_mute_headset_zone_305(
            self) -> None:
        """
        Test method to verify About the headset page.
        """
        self.tune_methods.tc_about_headset(device_name=self.device_name)

    def test_4117_VC_138415_parameters_persistency_after_reconnect_zone_305(self) -> None:
        """
        Test to verify parameters persistency after reconnecting headset.
        """
        head_persist = TuneHeadsetPersistency(headset_name=self.device_name, tune_app=self.tune_app)
        head_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_4118_VC_138424_factory_reset_zone_305(self) -> None:
        """
        Test to verify factory reset command on the headset.
        """
        Report.logSkip("Manual only")
        self.skipTest("Manual only")


if __name__ == "__main__":
    unittest.main()
