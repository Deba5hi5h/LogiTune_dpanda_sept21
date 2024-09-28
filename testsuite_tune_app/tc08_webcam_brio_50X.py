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
from firmware_tunes.build_types import GauguinBuildType


class WebcamBrio50X(UIBase):
    """
    Test class containing UI tests scenarios for Brio 50x.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, gauguin
        tune_env = gauguin.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import tune_env, is_acroname_available, gauguin

    device_name = gauguin.device_name
    ota_api_product_name = gauguin.ota_api_product_name
    baseline_device_version = gauguin.baseline_device_version
    target_device_version = gauguin.target_device_version
    repeats = gauguin.repeats
    S3_FOLDER = 'Logitech_Gauguin'
    build_type = GauguinBuildType.USER

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, 'firmware_tunes', 'easterEgg')
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(WebcamBrio50X, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(self.DIR_PATH, f'{self.build_type.value}{self.baseline_device_version}.bin')
        file_path_target = os.path.join(self.DIR_PATH, f'{self.build_type.value}{self.target_device_version}.bin')

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
            ota_api_product_name=self.ota_api_product_name
        )

        return fw_update, file_path_baseline, file_path_target

    def test_801_VC_69975_connect_webcam_brio_50X(self) -> None:
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_802_VC_108378_built_in_mic_webcam_brio_50X(self) -> None:
        self.camera.tc_built_in_microphone()

    def test_803_VC_69986_update_firmware_webcam_brio_50X(self) -> None:
        fw_update, file_path_base, _ = self.prepare_update_items()
        try:
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))
        finally:
            self.tune_app.open_tune_app()
            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)
            self.tune_app.update_firmware_with_easter_egg(
                device_file_path=file_path_base,
                device_name=self.device_name,
                timeout=fw_update.timeout,
            )

    def test_804_VC_69976_zoom_in_out_webcam_brio_50X(self) -> None:
        self.camera.tc_zoom_in_out()

    def test_805_VC_69977_pan_tilt_webcam_brio_50X(self) -> None:
        self.camera.tc_pan_tilt()

    def test_806_VC_69978_field_of_view_webcam_brio_50X(self) -> None:
        self.camera.tc_field_of_view()

    def test_807_VC_69982_auto_focus_webcam_brio_50X(self) -> None:
        self.camera.tc_auto_focus()

    def test_808_VC_69979_color_filter_webcam_brio_50X(self) -> None:
        self.camera.tc_color_filter()

    def test_809_VC_70176_image_adjustments_change_one_by_one_webcam_brio_505(
            self) -> None:
        self.camera.tc_image_settings()

    def test_810_VC_69985_hdr_webcam_brio_50X(self) -> None:
        self.camera.tc_hdr()

    def test_811_VC_69984_anti_flicker_webcam_brio_50X(self) -> None:
        self.camera.tc_anti_flicker()

    def test_812_VC_70175_image_adjustments_restart_to_default_brio_50X(self):
        self.camera.tc_restart_to_default()

    def test_813_VC_74756_parameters_persistency_after_reconnect_brio_50X(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_814_VC_69983_about_the_camera_webcam_brio_50X(self) -> None:
        self.camera.tc_about_camera()

    def test_815_VC_69987_factory_reset_webcam_brio_50X(self) -> None:
        self.camera.tc_factory_reset()

    def test_816_VC_101082_parameters_persistency_after_fw_update_brio_50X(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)

        try:
            fw_update, file_path, _ = self.prepare_update_items()
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
