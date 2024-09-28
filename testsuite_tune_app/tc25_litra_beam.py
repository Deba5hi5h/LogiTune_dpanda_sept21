import os
import unittest

import testsuite_tune_app.update_easteregg.device_parameters_jenkins as dpj
from apps.tune.base.base_testcase import TuneBaseTestCase
from apps.tune.streaming_light.streaming_light_ui_methods import TuneStreamingLightPersistency, TuneStreamingLightMethods
from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tc_scenarios.light_pages_scenarios import LightPagesScenarios
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType


class LitraBeam(TuneBaseTestCase, UIBase):
    """
    Test class containing UI tests scenarios for Litra Beam.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, litra_beam
        tune_env = litra_beam.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import tune_env, is_acroname_available, litra_beam

    device_name = litra_beam.device_name
    ota_api_product_name = litra_beam.ota_api_product_name
    baseline_device_version = litra_beam.baseline_device_version
    target_device_version = litra_beam.target_device_version
    repeats = litra_beam.repeats
    S3_FOLDER = "Logitech_Litra_Beam"
    conn_type = ConnectionType.usb_dock

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    streaming_light_methods = TuneStreamingLightMethods(device_name)
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    cameras_connected_flag = False
    _CAMERAS = (
        dpj.brio4k.device_name,
        dpj.cezanne.device_name,
        dpj.degas.device_name,
        dpj.gauguin.device_name,
        dpj.matisse.device_name,
    )

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=LightPagesScenarios)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
            cls._disconnect_cameras()
        super(LitraBeam, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(self.DIR_PATH, f"imola-nrf52820-firmware-{self.baseline_device_version}-signed.dfu")
        file_path_target = os.path.join(self.DIR_PATH, f"imola-nrf52820-firmware-{self.target_device_version}-signed.dfu")
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

    @classmethod
    def _connect_cameras(cls) -> None:
        if cls.is_acroname_available and not cls.cameras_connected_flag:
            for camera_name in cls._CAMERAS:
                connect_device(camera_name)
            cls.cameras_connected_flag = True

    @classmethod
    def _disconnect_cameras(cls) -> None:
        for camera_name in cls._CAMERAS:
            disconnect_device(camera_name)

    def test_2501_VC_88108_connect_webcam_litra_beam(self) -> None:
        self.streaming_light_methods.tc_connect_litra_beam(device_name=self.device_name,
                                                           acroname_automatic=self.is_acroname_available)

    def test_2502_VC_88109_update_firmware_webcam_litra_beam(self) -> None:
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2503_VC_88110_power_on_off_litra_beam(
            self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.streaming_light_methods.tc_power_on_off_litra_beam(device_name=self.device_name)

    def test_2504_VC_88112_device_name_litra_beam(self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 30
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_2505_VC_88111_about_litra_beam(self) -> None:
        self.tune_methods.tc_about_camera(device_name=self.device_name)

    def test_2506_VC_88114_factory_reset_litra_beam(self) -> None:
        self.streaming_light_methods.tc_litra_beam_factory_reset(device_name=self.device_name)

    def test_2507_VC_102124_presets(self) -> None:
        self.streaming_light_methods.tc_litra_presets_test()

    def test_2508_VC_110265_parameters_persistency_after_reconnect_litra_beam(self):
        device_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        device_persist.check_persistency(acroname_automatic=self.is_acroname_available)

    def test_2509_VC_110266_parameters_persistency_after_fw_update_litra_beam(self):
        device_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        fw_update, file_path_baseline, file_path_target = self.prepare_update_items()
        device_persist.check_parameters_persistency_after_fw_update(fw_update, file_path_baseline, file_path_target)

    def test_2510_VC_110267_parameters_persistency_after_tune_relaunching(self):
        device_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        device_persist.check_parameters_persistency_after_tune_relaunching()

    def test_2511_VC_110268_preset_persistency_after_litra_reconnection(self):
        preset_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        preset_persist.check_preset_persistency_after_litra_reconnection(acroname_automatic=self.is_acroname_available)

    def test_2512_VC_110269_preset_persistency_after_litra_fw_update(self):
        preset_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        fw_update, file_path_baseline, file_path_target = self.prepare_update_items()
        preset_persist.check_preset_persistency_after_litra_update( fw_update, file_path_baseline, file_path_target)

    def test_2513_VC_110270_preset_persistency_after_tune_relaunching(self):
        preset_persist = TuneStreamingLightPersistency(streaming_light_name=self.device_name, tune_app=self.tune_app)
        preset_persist.check_preset_persistency_after_tune_relaunching()

    def test_2514_VC_110271_responsiveness(self):
        self.streaming_light_methods.tc_litra_beam_responsiveness()

    def test_2515_VC_110277_change_preset_name_after_changing_slider(self):
        self.streaming_light_methods.tc_change_preset_name_after_changing_slider()

    def test_2516_VC_144621_smart_activation_for_any_camera(self):
        self._connect_cameras()
        self.scenario.tc_smart_activation_for_any_camera(self.device_name)

    def test_2517_VC_144622_smart_activation_disabled(self):
        self._connect_cameras()
        self.scenario.tc_smart_activation_disabled(self.device_name)

    def test_2518_VC_144623_smart_activation_for_chosen_cameras(self):
        self._connect_cameras()
        self.scenario.tc_smart_activation_for_chosen_cameras(self.device_name)


if __name__ == "__main__":
    unittest.main()
