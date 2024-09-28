import os
import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device
from extentreport.report import Report


class WebcamC930e(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for C930e webcam.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, c930e
        tune_env = c930e.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import tune_env, is_acroname_available, c930e

    device_name = c930e.device_name
    ota_api_product_name = c930e.ota_api_product_name
    baseline_device_version = c930e.baseline_device_version
    target_device_version = c930e.target_device_version
    repeats = c930e.repeats
    S3_FOLDER = 'Logitech_C930e'

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(WebcamC930e, cls).tearDownClass()

    def prepare_update_items(self):
        file_path = os.path.join(self.DIR_PATH, f'Thunder_Scorpio_User_{self.baseline_device_version}.bin')

        t_files = FirmwareDownloader()
        t_files.prepare_firmware_files_for_test(self.S3_FOLDER, file_path)

        fw_update = FirmwareUpdate(
            retry=1,
            test_entity=self,
            device_name=self.device_name,
            baseline_version_device=self.baseline_device_version,
            target_version_device=self.target_device_version,
            file_path_device=file_path,
            tune_env=self.tune_env,
            ota_api_product_name=self.ota_api_product_name
        )

        return fw_update, file_path

    def test_401_VC_58425_connect_webcam_c930e(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_402_VC_58435_update_firmware_webcam_c930e(self):
        try:
            fw_update, _ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_403_VC_58426_zoom_in_out_webcam_c930e(self):
        self.camera.tc_zoom_in_out()

    def test_404_VC_58427_pan_tilt_webcam_c930e(self):
        self.camera.tc_pan_tilt()

    def test_405_VC_58432_auto_focus_webcam_c930e(self):
        self.camera.tc_auto_focus()

    def test_406_VC_58428_color_filter_webcam_c930e(self):
        self.camera.tc_color_filter()

    def test_407_VC_58429_image_adjustments_webcam_c930e(self) -> None:
        self.tune_methods.tc_image_adjustments(device_name=self.device_name)

    def test_408_VC_70188_image_adjustments_change_one_by_one_webcam_c930e(
            self) -> None:
        self.camera.tc_image_settings()

    # def test_409_VC_70189_image_adjustments_change_all_params_webcam_c930e(
    #         self) -> None:
    #     self.tune_methods.tc_image_adjustments_change_all_params(
    #         device_name=self.device_name)

    def test_410_VC_58433_about_the_camera_webcam_c930e(self):
        self.camera.tc_about_camera()

    def test_411_VC_58434_anti_flicker_webcam_c930e(self):
        self.camera.tc_anti_flicker()

    def test_412_VC_70186_image_adjustments_restart_to_default_brio_c930e(self):
        self.camera.tc_restart_to_default()

    def test_413_VC_77506_parameters_persistency_after_reconnect_c930e(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_414_VC_58437_factory_reset_webcam_c930e(self):
        self.camera.tc_factory_reset()

    def test_415_VC_101078_parameters_persistency_after_fw_update_c930e(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)

        try:
            fw_update, file_path = self.prepare_update_items()
            Report.logInfo(f'Start camera downgrade.')

            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)
            self.tune_app.update_firmware_with_easter_egg(
                device_file_path=file_path,
                device_name=self.device_name,
                timeout=fw_update.timeout,
            )

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
