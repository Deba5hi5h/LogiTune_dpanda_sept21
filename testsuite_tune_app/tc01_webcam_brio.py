import os
import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device, connect_device
from extentreport.report import Report
from common.comparators import Comparator


class WebcamBrio(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for Brio.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, brio4k
        tune_env = brio4k.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import tune_env, is_acroname_available, brio4k

    device_name = brio4k.device_name
    ota_api_product_name = brio4k.ota_api_product_name
    baseline_device_version = brio4k.baseline_device_version
    target_device_version = brio4k.target_device_version
    baseline_eeprom_version = brio4k.baseline_eeprom_version
    target_eeprom_version = brio4k.target_eeprom_version
    repeats = brio4k.repeats
    S3_FOLDER = "Logitech_Brio"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DIR_PATH = os.path.join(directory, 'firmware_tunes', 'easterEgg')
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def check_if_built_in_mic_param_shall_be_available(cls):

        cls.camera._open_camera_settings()
        cls.tune_app.open_about_the_device()
        fw_version = cls.tune_app.get_firmware_version()
        cls.tune_app.click_back_button_to_device_settings()
        # Check if fw is greater or equal than current FW version
        compare_value = Comparator.compare_versions(fw_version, "2.0.64") != 2
        if compare_value:
            log_info = "Brio FW Version is greater or equal than 2.0.64 - built in mic present"
        else:
            log_info = "Brio FW Version is lower than 2.0.64 - built in mic not present"

        Report.logInfo(log_info)
        return Comparator.compare_versions(fw_version, "2.0.64") != 2

    @classmethod
    def setUpClass(cls) -> None:
        super(WebcamBrio, cls).setUpClass()
        camera_name = cls.camera.camera.name
        try:
            if cls.is_acroname_available:
                connect_device(camera_name)
        except Exception as e:
            Report.logFail(f"Connection with {camera_name} failed - reason: {e}")
        else:
            cls.built_in_mic_flag = cls.check_if_built_in_mic_param_shall_be_available()
            if cls.is_acroname_available:
                disconnect_device(camera_name)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(WebcamBrio, cls).tearDownClass()

    def prepare_update_items(self):
        camera_file_path = os.path.join(
            self.DIR_PATH, f'webcam_{self.baseline_device_version}_release.bin'
        )

        if len(self.baseline_eeprom_version.split('.')) < 3:
            self.baseline_eeprom_version += '.0'

        eeprom_file_path = os.path.join(
            self.DIR_PATH, f'eeprom_logitech_{self.baseline_eeprom_version}.s19'
        )

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, camera_file_path)
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, eeprom_file_path)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            baseline_version_eeprom=self.baseline_eeprom_version,
            target_version_eeprom=self.target_eeprom_version,
            file_path_device=camera_file_path,
            file_path_eeprom=eeprom_file_path,
            tune_env=self.tune_env,
            ota_api_product_name=self.ota_api_product_name
        )

        return fw_update, camera_file_path, eeprom_file_path

    def test_101_VC_58353_connect_webcam_brio(self) -> None:
        if not self.built_in_mic_flag:
            self.camera.camera.built_in_microphone = None
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_102_VC_108375_built_in_mic(self) -> None:
        if self.built_in_mic_flag:
            self.camera.tc_built_in_microphone()
        else:
            Report.logSkip("Built in microphone not present before 2.0.64")

    def test_103_VC_58364_update_firmware_webcam_brio(self) -> None:
        if not self.built_in_mic_flag or self.camera.change_built_in_microphone(mic_turned_on=True):
            try:
                fw_update, *_ = self.prepare_update_items()
                fw_update.update_camera_components(force_eeprom_update=False)
            except Exception as ex:
                Report.logException(str(ex))
        else:
            Report.logSkip('Skipping test, because Built-in microphone is disabled, which may '
                           'brick Brio camera when downgrading below FW 2.0.64')

    def test_104_VC_58354_zoom_in_out_webcam_brio(self) -> None:
        self.camera.tc_zoom_in_out()

    def test_105_VC_58355_pan_tilt_webcam_brio(self) -> None:
        self.camera.tc_pan_tilt()

    def test_106_VC_58356_field_of_view_webcam_brio(self) -> None:
        self.camera.tc_field_of_view()

    def test_107_VC_58360_auto_focus_webcam_brio(self) -> None:
        self.camera.tc_auto_focus()

    def test_108_VC_58357_color_filter_webcam_brio(self) -> None:
        self.camera.tc_color_filter()

    # def test_108_VC_58358_image_adjustments_webcam_brio(self) -> None:
    #     self.camera.tc_image_settings()

    def test_109_VC_70173_image_adjustments_change_one_by_one_webcam_brio(self) -> None:
        self.camera.tc_image_settings()

    def test_110_VC_58361_about_the_camera_webcam_brio(self) -> None:
        self.camera.tc_about_camera()

    def test_111_VC_58362_anti_flicker_webcam_brio(self) -> None:
        self.camera.tc_anti_flicker()

    def test_112_VC_58363_hdr_webcam_brio(self) -> None:
        self.camera.tc_hdr()

    def test_113_VC_70172_image_adjustments_restart_to_default_brio(self):
        self.camera.tc_restart_to_default()

    def test_114_VC_77498_parameters_persistency_after_reconnect_brio(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_115_VC_58366_factory_reset_webcam_brio(self) -> None:
        self.camera.tc_factory_reset()

    def test_116_VC_101079_parameters_persistency_after_fw_update_brio(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)

        try:
            fw_update, camera_file_path, eeprom_file_path,  = self.prepare_update_items()
            Report.logInfo(f'Start camera downgrade.')

            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)
            self.tune_app.update_firmware_with_easter_egg(
                device_file_path=camera_file_path,
                device_name=self.device_name,
                timeout=fw_update.timeout,
            )

            # Uncomment if EEPROM update is desired
            # self.tune_app.open_device_in_my_devices_tab(self.device_name)
            # self.tune_app.open_about_the_device(device_name=self.device_name)
            # self.tune_app.update_firmware_with_easter_egg(
            #     device_file_path=eeprom_file_path,
            #     device_name=self.device_name,
            #     timeout=fw_update.timeout,
            # )

            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.click_back_button_to_device_settings()

            Report.logInfo(f'Change camera settings.')
            cam_persist._set_random_camera_adjustments()

            self.tune_app.click_back_from_image_adjustments()
            self.tune_app.open_about_the_device(device_name=self.device_name)

            Report.logInfo(f'Start upgrade.')

            self.tune_app.start_update_from_device_tab(
                device_name=self.device_name,
                timeout=fw_update.timeout,
            )

            self.tune_app.open_device_in_my_devices_tab(self.device_name)

            Report.logInfo(f'Verify camera settings.')
            self.tune_app.click_back_button_to_device_settings()
            cam_persist._get_camera_adjustments()

        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    unittest.main()
