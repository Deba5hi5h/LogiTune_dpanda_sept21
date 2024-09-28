import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_device


class WebcamC925e(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for C925e webcam.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = "C925e"
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect_device(device_name=cls.device_name)
        super(WebcamC925e, cls).tearDownClass()

    def test_301_VC_58412_connect_webcam_c925e(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_302_VC_58413_zoom_in_out_webcam_c925e(self):
        self.camera.tc_zoom_in_out()

    def test_303_VC_58414_pan_tilt_webcam_c925e(self):
        self.camera.tc_pan_tilt()

    def test_304_VC_58418_auto_focus_webcam_c925e(self):
        self.camera.tc_auto_focus()

    def test_305_VC_58415_color_filter_webcam_c925e(self):
        self.camera.tc_color_filter()

    def test_307_VC_70183_image_adjustments_change_one_by_one_webcam_c925e(self) -> None:
        self.camera.tc_image_settings()

    def test_309_VC_58419_about_the_camera_webcam_c925e(self):
        self.camera.tc_about_camera()

    def test_310_VC_58421_anti_flicker_webcam_c925e(self):
        self.camera.tc_anti_flicker()

    def test_311_VC_58424_factory_reset_webcam_c925e(self):
        self.camera.tc_factory_reset()

    def test_312_VC_58412_update_firmware_webcam_c925e(self):
        raise unittest.SkipTest("Update not available")


if __name__ == "__main__":
    unittest.main()
