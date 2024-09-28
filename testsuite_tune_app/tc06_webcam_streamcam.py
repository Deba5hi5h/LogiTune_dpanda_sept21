import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.usb_switch import disconnect_device


class WebcamStreamCam(UIBase):
    """
    Test class containing LogiTune UI tests scenarios for Streamcam.
    """

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    device_name = "StreamCam"
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        disconnect_device(device_name=cls.device_name)
        super(WebcamStreamCam, cls).tearDownClass()
        
    def test_601_VC_58367_connect_webcam_streamcam(self):
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_602_VC_58368_zoom_in_out_webcam_streamcam(self):
        self.camera.tc_zoom_in_out()

    def test_603_VC_58369_pan_tilt_webcam_streamcam(self):
        self.camera.tc_pan_tilt()
    def test_604_VC_58373_auto_focus_webcam_streamcam(self):
        self.camera.tc_auto_focus()

    def test_605_VC_58370_color_filter_webcam_streamcam(self):
        self.camera.tc_color_filter()

    # def test_606_VC_58371_image_adjustments_webcam_streamcam(self) -> None:
    #     self.tune_methods.tc_image_adjustments(device_name=self.device_name)

    def test_607_VC_70194_image_adjustments_change_one_by_one_webcam_streamcam(
            self) -> None:
        self.camera.tc_image_settings()

    # def test_608_VC_70195_image_adjustments_change_all_params_webcam_streamcam(
    #         self) -> None:
    #     self.tune_methods.tc_image_adjustments_change_all_params(
    #         device_name=self.device_name)

    def test_609_VC_58374_about_the_camera_webcam_streamcam(self):
        self.camera.tc_about_camera()

    def test_610_VC_58375_anti_flicker_webcam_streamcam(self):
        self.camera.tc_anti_flicker()

    def test_611_VC_58376_hdr_webcam_streamcam(self):
        self.camera.tc_hdr()

    def test_612_VC_70193_image_adjustments_restart_to_default_brio_streamcam(self):
        self.camera.tc_restart_to_default()

    def test_613_VC_58377_factory_reset_webcam_streamcam(self):
        self.camera.tc_factory_reset()

    def test_614_VC_77501_parameters_persistency_after_reconnect_streamcam(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency()


# def test_615_VC_58370_update_firmware_webcam_streamcam(self):
    #     raise unittest.SkipTest("Update not available")
        # self.tune_methods.tc_firmware_update(device_name=self.device_name)


if __name__ == "__main__":
    unittest.main()
