import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_vibe_100_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_vibe_100 import (
    FEATURES_ZONE_VIBE_100, EQ_MODES, CONNECTED_DEVICES, CONNECTED, NOT_CONNECTED)


class ZoneVibe100ApiBtTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(ZoneVibe100ApiBtTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_vibe_100_api.name,
                                          conn_type=ConnectionType.bt,
                                          com_port=local_api_pc_configuration.com_port)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_VIBE_100"
        global_variables.firmware_api_device_conn = ConnectionType.bt

    @classmethod
    def tearDownClass(cls):
        cls.centurion.close_port()
        super(ZoneVibe100ApiBtTests, cls).tearDownClass()

    def test_1101_VC_57424_get_protocol_version(self) -> None:
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1102_VC_57425_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_ZONE_VIBE_100)
            self.features.root_feature.verify_get_features_responses(
                response, FEATURES_ZONE_VIBE_100
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1103_VC_57426_get_not_supported_feature(self) -> None:
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature(
                    [feature[0], feature[1]]
                )
                self.features.root_feature.verify_not_supported_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1104_VC_57427_get_not_existing_feature(self) -> None:
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1105_VC_57428_get_feature_count(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(
                response, len(FEATURES_ZONE_VIBE_100.keys())
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1106_VC_57429_get_feature_id(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(
                response, FEATURES_ZONE_VIBE_100
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1107_VC_57439_get_serial_number(self) -> None:
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(
                response, zone_vibe_100_api.serial_number
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1108_VC_57440_get_firmware_version(self) -> None:
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(
                response, zone_vibe_100_api.firmware_version
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1109_VC_57441_get_hardware_info(self) -> None:
        try:
            model_id = zone_vibe_100_api.model_id
            hw_revision = "00"

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(
                response, model_id, hw_revision
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1110_VC_57442_set_and_get_device_name(self) -> None:
        try:
            NAME = zone_vibe_100_api.name + " {}".format(random.randint(0, 10000))
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 30)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1111_VC_57443_get_default_device_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_default_device_name()
            self.features.device_name_feature.verify_default_name(
                response, zone_vibe_100_api.name
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1112_VC_57444_get_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(
                response, max_length=30
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1113_VC_57445_set_longer_than_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.set_device_name(
                zone_vibe_100_api.name * 5
            )
            self.features.device_name_feature.verify_error_for_setting_too_long_name(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1114_VC_55489_get_battery_status(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1115_VC_57490_get_voltage_info(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_voltage_status()
            self.features.battery_SOC_feature.verify_get_voltage_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1116_VC_57449_set_get_sleep_timer(self) -> None:
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(response, t)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1117_VC_57484_get_supported_language(self) -> None:
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1118_VC_57485_set_not_supported_language(self) -> None:
        try:
            not_supported_languages = [3]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(n)
                self.features.earcon_feature.verify_set_not_supported_language(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1119_VC_57486_get_language_capability(self) -> None:
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1120_VC_57487_set_get_earcon_state(self) -> None:
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(response, state)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1121_VC_57488_set_not_supported_earcon_state(self) -> None:
        try:
            response = self.features.earcon_feature.set_earcon_state(
                random.randint(2, 255)
            )
            self.features.earcon_feature.verify_not_supported_earcon_value(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1122_VC_57446_set_get_eq(self) -> None:
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(response, key, value)
                time.sleep(3)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1123_VC_57497_get_bt_state(self) -> None:
        try:
            response = self.features.bluetooth_crtl_feature.get_bt_state()
            self.features.bluetooth_crtl_feature.verify_get_bt_state(
                response, state=2
            )  # Connected
        except Exception as ex:
            Report.logException(str(ex))

    def test_1124_VC_57496_set_discoverable_state(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            response = self.features.bluetooth_crtl_feature.set_discoverable_state()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1125_VC_57450_set_get_mic_mute_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_audio_feature.set_mic_mute(status)
                response = self.features.headset_audio_feature.get_mic_mute_status()
                self.features.headset_audio_feature.verify_get_mic_mute_status(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1126_VC_57455_set_not_supported_mic_mute_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_mic_mute(
                random.randint(2, 255)
            )
            self.features.headset_audio_feature.verify_not_supported_mic_mute_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1127_VC_57457_set_get_sidetone_level(self) -> None:
        try:
            levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            for level in levels:
                self.features.headset_audio_feature.set_sidetone_level(level)
                response = self.features.headset_audio_feature.get_sidetone_level()
                self.features.headset_audio_feature.verify_get_sidetone_level(
                    response, level
                )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1128_VC_57456_set_not_supported_value_of_sidetone_level(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(
                random.randint(11, 255)
            )
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1129_VC_57458_get_connected_device_num(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_connected_device_number()
            )
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(
                response, CONNECTED_DEVICES
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1130_VC_57459_get_connected_device_info(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_connected_device_info(
                    CONNECTED_DEVICES
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_info(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1131_VC_57460_get_connected_device_name(self) -> None:
        try:
            Report.logInfo(f"Name of connected device is: {local_api_pc_configuration.pc_host_name}")
            response = (
                self.features.headset_bt_conn_info_feature.get_device_connected_name(
                    local_api_pc_configuration.pc_bt_address
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(
                response, local_api_pc_configuration.pc_host_name
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1132_VC_57462_get_audio_active_device(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_audio_active_device()
            )
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(
                response, local_api_pc_configuration.pc_bt_address, "00"
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1133_VC_57463_get_dongle_fw_version(self) -> None:
        Report.logSkip("Checking Dongle version is not available in BT mode")
        self.skipTest("Checking Dongle version is not available in BT mode")

    def test_1134_VC_57464_connected_device_status(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_device_connected_status(
                    local_api_pc_configuration.pc_bt_address
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, CONNECTED
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1135_VC_57465_connected_device_status_for_fake_device(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_device_connected_status(
                    local_api_pc_configuration.fake_bt_address
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, NOT_CONNECTED
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1136_VC_57467_get_set_A2DP_mute_status(self) -> None:
        try:
            statuses = [0]
            for status in statuses:
                self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                    local_api_pc_configuration.pc_bt_address, status
                )
                response = (
                    self.features.headset_bt_conn_info_feature.get_A2DP_mute_status(
                        local_api_pc_configuration.pc_bt_address
                    )
                )
                self.features.headset_bt_conn_info_feature.verify_get_A2DP_mute_status(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1137_VC_57466_set_not_supported_A2DP_state(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                local_api_pc_configuration.pc_bt_address, random.randint(2, 255)
            )
            self.features.headset_bt_conn_info_feature.verify_not_supported_A2DP_mu_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1138_VC_57468_get_pdl_device_numbers_and_info(self) -> None:
        try:
            number_response = (
                self.features.headset_bt_conn_info_feature.get_pdl_device_number()
            )
            pdl_length = self.features.headset_bt_conn_info_feature.get_length_of_pdl(
                number_response
            )
            info_response = (
                self.features.headset_bt_conn_info_feature.get_pdl_devices_info(
                    pdl_length
                )
            )
            self.features.headset_bt_conn_info_feature.verify_pdl_devices_info(
                info_response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1139_VC_57474_set_get_voice_notification_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_voice_notification_status(status)
                response = (
                    self.features.headset_misc_feature.get_voice_notification_status()
                )
                self.features.headset_misc_feature.verify_get_voice_notification_status(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1140_VC_57475_set_not_supported_voice_notification_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(
                random.randint(2, 255)
            )
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1141_VC_57476_factory_reset_device(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1142_VC_57471_set_get_mic_boom_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_mic_boom_status(status)
                response = self.features.headset_misc_feature.get_mic_boom_status()
                self.features.headset_misc_feature.verify_mic_boom_status(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1143_VC_57472_set_not_supported_mic_boom_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_mic_boom_status(
                random.randint(2, 255)
            )
            self.features.headset_misc_feature.verify_not_supported_mic_boom_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ZoneVibe100ApiBtTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
