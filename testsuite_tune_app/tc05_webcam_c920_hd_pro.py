import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_device


class WebcamC920HdPro(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for C920HDPro webcam.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = "C920 HD Pro Webcam"
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect_device(device_name=cls.device_name)
        super(WebcamC920HdPro, cls).tearDownClass()

    def test_501_VC_58391_connect_webcam_c920_hd_pro(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_502_VC_58392_zoom_in_out_webcam_c920_hd_pro(self):
        self.camera.tc_zoom_in_out()

    def test_503_VC_58393_pan_tilt_webcam_c920_hd_pro(self):
        self.camera.tc_pan_tilt()

    def test_504_VC_58398_auto_focus_webcam_c920_hd_pro(self):
        self.camera.tc_auto_focus()

    def test_505_VC_58395_color_filter_webcam_c920_hd_pro(self):
        self.camera.tc_color_filter()

    def test_507_VC_70191_image_adjustments_change_one_by_one_webcam_c920_hd_pro(self) -> None:
        self.camera.tc_image_settings()

    def test_509_VC_58399_about_the_camera_webcam_c920_hd_pro(self):
        self.camera.tc_about_camera()

    def test_510_VC_58400_anti_flicker_webcam_c920_hd_pro(self):
        self.camera.tc_anti_flicker()

    def test_511_VC_58401_factory_reset_webcam_c920_hd_pro(self):
        self.camera.tc_factory_reset()

    def test_512_VC_58391_update_firmware_webcam_c920_hd_pro(self):
        raise unittest.SkipTest("Update not available")


if __name__ == "__main__":
    unittest.main()
