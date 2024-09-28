import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_device


class WebcamC920e(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for C920e webcam.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = "C920e"
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect_device(device_name=cls.device_name)
        super(WebcamC920e, cls).tearDownClass()

    def test_201_VC_58378_connect_webcam_c920e(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_202_VC_58389_built_in_mic_webcam_c920e(self) -> None:
        self.camera.tc_built_in_microphone()

    def test_203_VC_58380_zoom_in_out_webcam_c920e(self):
        self.camera.tc_zoom_in_out()

    def test_204_VC_58382_pan_tilt_webcam_c920e(self):
        self.camera.tc_pan_tilt()

    def test_205_VC_58386_auto_focus_webcam_c920e(self):
        self.camera.tc_auto_focus()

    def test_206_VC_58383_color_filter_webcam_c920e(self):
        self.camera.tc_color_filter()

    def test_207_VC_70180_image_adjustments_change_one_by_one_webcam_c925e(self) -> None:
        self.camera.tc_image_settings()

    def test_208_VC_58387_about_the_camera_webcam_c920e(self):
        self.camera.tc_about_camera()

    def test_209_VC_58388_anti_flicker_webcam_c920e(self):
        self.camera.tc_anti_flicker()

    def test_210_VC_70179_image_adjustments_restart_to_default_brio_c920e(self):
        self.camera.tc_restart_to_default()

    def test_211_VC_77502_parameters_persistency_after_reconnect_c920e(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency()

    def test_212_VC_58390_factory_reset_webcam_c920e(self):
        self.camera.tc_factory_reset()


if __name__ == "__main__":
    unittest.main()
