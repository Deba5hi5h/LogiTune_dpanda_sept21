import os
import unittest

from apps.tune.firmware_downloader import FirmwareDownloader
from apps.tune.firmware_update import FirmwareUpdate
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import JENKINS_FWU_CONFIG
from common.usb_switch import disconnect_device
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_qbert import QBERT_EQ_PROFILES


class LogiDock(UIBase):
    """
    Test class containing UI tests scenarios for Logi Dock.
    """
    if JENKINS_FWU_CONFIG:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import is_acroname_available, logi_dock
        tune_env = logi_dock.jenkins_tune_env
    else:
        from testsuite_tune_app.update_easteregg.device_parameters import tune_env, is_acroname_available, logi_dock

    device_name = logi_dock.device_name
    ota_api_product_name = logi_dock.ota_api_product_name
    baseline_device_version = logi_dock.baseline_device_version
    target_device_version = logi_dock.target_device_version
    repeats = logi_dock.repeats
    S3_FOLDER = "Logi_Dock"
    conn_type = ConnectionType.usb_dock

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    directory = os.path.dirname(os.path.dirname(__file__))
    DIR_PATH = os.path.join(directory, "firmware_tunes", "easterEgg")

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.is_acroname_available:
            disconnect_device(device_name=cls.device_name)
        super(LogiDock, cls).tearDownClass()

    def prepare_update_items(self):
        file_path_baseline = os.path.join(self.DIR_PATH, f"qbert-{self.baseline_device_version}.bin")
        file_path_target = os.path.join(self.DIR_PATH, f"qbert-{self.target_device_version}.bin")

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
            ota_api_product_name=self.ota_api_product_name,
            easter_egg_on_second_update=True
        )

        return fw_update, file_path_baseline, file_path_target

    def test_2201_VC_88116_connect_webcam_logi_dock(self) -> None:
        self.tune_methods.tc_connect_dock(device_name=self.device_name)

    def test_2202_VC_88117_update_firmware_logi_dock(self) -> None:
        try:
            fw_update, *_ = self.prepare_update_items()
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2203_VC_88118_mic_level_logi_dock(self) -> None:
        """
        Test method to modify parameters and verify Mic level feature.
        """
        self.tune_methods.tc_mic_level(device_name=self.device_name)

    def test_2204_VC_88119_equalizer_headset_logi_dock(self) -> None:
        """
        Test method to modify and verify and Equalizer feature.
        """
        self.tune_methods.tc_wireless_headset_equalizer(device_name=self.device_name,
                                                        conn_type=self.conn_type,
                                                        profiles=QBERT_EQ_PROFILES)

    def test_2205_VC_88120_device_name_logi_dock(self) -> None:
        """
        Test method to modify and verify Device Name feature.
        """
        name_max_len = 48
        self.tune_methods.tc_device_name(device_name=self.device_name,
                                         conn_type=self.conn_type,
                                         name_max_len=name_max_len)

    def test_2206_VC_88121_parameters_persistency_after_reconnect_logi_dock(self) -> None:
        self.tune_methods.tc_dock_parameters_persistency(device_name=self.device_name,
                                                         reconnect_timeout=5,
                                                         profiles=QBERT_EQ_PROFILES)

    def test_2207_VC_88122_about_the_dock_webcam_logi_dock(self) -> None:
        self.tune_methods.tc_about_camera(device_name=self.device_name)

    def test_2208_VC_88123_hi_speed_usb_3_0_logi_dock(self) -> None:
        self.tune_methods.tc_hi_speed_usb_3_0_logi_dock(device_name=self.device_name)

    def test_2209_VC_88124_meeting_alert_logi_dock(self) -> None:
        self.tune_methods.tc_meeting_alert(device_name=self.device_name)

    def test_2210_VC_88125_firmware_update_webcam_brio_30X_connected_to_logi_dock(self) -> None:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import degas

        file_path = os.path.join(
            self.DIR_PATH, f"Degas_{degas.baseline_device_version}.rfw"
        )

        try:
            t_files = FirmwareDownloader()
            t_files.prepare_firmware_files_for_test("Logitech_Degas", file_path)

            fw_update = FirmwareUpdate(
                retry=1,
                test_entity=self,
                device_name='Brio 305',
                baseline_version_device=degas.baseline_device_version,
                target_version_device=degas.target_device_version,
                file_path_device=file_path,
                tune_env=degas.jenkins_tune_env,
                ota_api_product_name=degas.ota_api_product_name,
                reconnect_after_fwu_failure=False
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2211_VC_88126_firmware_update_headset_zone_wired_earbuds_connected_to_logi_dock(self) -> None:
        from testsuite_tune_app.update_easteregg.device_parameters_jenkins import zone_wired_earbuds

        file_path = os.path.join(
            self.DIR_PATH, f"zonewiredearbuds_headset_{zone_wired_earbuds.baseline_device_version}.rfw"
        )

        try:
            t_files = FirmwareDownloader()
            t_files.prepare_firmware_files_for_test("Logitech_Zone_Wired_Earbuds", file_path)

            fw_update = FirmwareUpdate(
                retry=1,
                test_entity=self,
                device_name=zone_wired_earbuds.device_name,
                baseline_version_device=zone_wired_earbuds.baseline_device_version,
                target_version_device=zone_wired_earbuds.target_device_version,
                file_path_device=file_path,
                tune_env=zone_wired_earbuds.jenkins_tune_env,
                ota_api_product_name=zone_wired_earbuds.ota_api_product_name,
                reconnect_after_fwu_failure=False
            )
            fw_update.update()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2212_VC_88127_factory_reset_webcam_logi_dock(self) -> None:
        self.tune_methods.tc_dock_factory_reset(device_name=self.device_name,
                                                profiles=QBERT_EQ_PROFILES)


if __name__ == "__main__":
    unittest.main()
