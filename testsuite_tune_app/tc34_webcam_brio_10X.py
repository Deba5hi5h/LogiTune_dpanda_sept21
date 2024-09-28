import unittest

from apps.tune.camera.camera_ui_methods import TuneCameraMethods, TuneCameraPersistency
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device

class WebcamBrio10X(UIBase):
    """
    Test class containing UI tests scenarios for Brio 10X.
    """

    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, cezanne
        tune_env = cezanne.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import is_acroname_available, cezanne

    device_name = cezanne.device_name

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    camera = TuneCameraMethods(camera_name=device_name, tune_app=tune_app)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(WebcamBrio10X, cls).tearDownClass()

    def test_3301_VC_103786_connect_webcam_brio_10X(self) -> None:
        self.camera.tc_connect_webcam_and_verify_parameters()

    def test_3302_VC_103787_color_filter_webcam_brio_10X(self) -> None:
        self.camera.tc_color_filter()

    def test_3303_VC_103789_image_adjustments_change_one_by_one_webcam_brio_10X(
            self) -> None:
        self.camera.tc_image_settings()

    def test_3304_VC_103790_about_the_camera_webcam_brio_10X(self) -> None:
        self.camera.tc_about_camera()

    def test_3305_VC_103791_anti_flicker_webcam_brio_10X(self) -> None:
        self.camera.tc_anti_flicker()

    def test_3306_VC_103788_image_adjustments_reset_to_default_brio_10X(self):
        self.camera.tc_restart_to_default()

    def test_3307_VC_103792_parameters_persistency_after_reconnect_brio_10X(self) -> None:
        cam_persist = TuneCameraPersistency(camera_name=self.device_name, tune_app=self.tune_app)
        cam_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_3308_VC_103793_factory_reset_webcam_brio_10X(self) -> None:
        self.camera.tc_factory_reset()


if __name__ == "__main__":
    unittest.main()
