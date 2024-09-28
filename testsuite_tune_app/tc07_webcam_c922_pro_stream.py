import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_device


class WebcamC922ProStream(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for C922Pro webcam.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = "C922 Pro Stream Webcam"
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect_device(device_name=cls.device_name)
        super(WebcamC922ProStream, cls).tearDownClass()

    def test_701_VC_58402_connect_webcam_c922_pro_stream(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_702_VC_58403_zoom_in_out_webcam_c922_pro_stream(self):
        self.camera.tc_zoom_in_out()

    def test_703_VC_58404_pan_tilt_webcam_c922_pro_stream(self):
        self.camera.tc_pan_tilt()
    def test_704_VC_58408_auto_focus_webcam_c922_pro_stream(self):
        self.camera.tc_auto_focus()

    def test_705_VC_58405_color_filter_webcam_c922_pro_stream(self):
        self.camera.tc_color_filter()

    def test_707_VC_70198_image_adjustments_change_one_by_one_webcam_c922_pro_stream(self) -> None:
        self.camera.tc_image_settings()

    def test_709_VC_58409_about_the_camera_webcam_c922_pro_stream(self):
        self.camera.tc_about_camera()

    def test_710_VC_58410_anti_flicker_webcam_c922_pro_stream(self):
        self.camera.tc_anti_flicker()

    def test_711_VC_xxx_update_firmware_webcam_c922_pro_stream(self):
        raise unittest.SkipTest("Update not available")

    def test_712_VC_58411_factory_reset_webcam_c922_pro_stream(self):
        self.camera.tc_factory_reset()


if __name__ == "__main__":
    unittest.main()
