import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_300_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_300 import (
    FEATURES_ZONE_300, EQ_MODES, CONNECTED_DEVICES, CONNECTED, NOT_CONNECTED)


class Zone300ApiBtTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(Zone300ApiBtTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_300_api.name,
                                          conn_type=ConnectionType.bt,
                                          com_port=local_api_pc_configuration.com_port)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_300"
        global_variables.firmware_api_device_conn = ConnectionType.bt

    @classmethod
    def tearDownClass(cls):
        cls.centurion.close_port()
        super(Zone300ApiBtTests, cls).tearDownClass()

    def test_2201_VC_121867_get_protocol_version(self) -> None:
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2202_VC_121868_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_ZONE_300)
            self.features.root_feature.verify_get_features_responses(
                response, FEATURES_ZONE_300
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2203_VC_121869_get_not_supported_feature(self) -> None:
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature(
                    [feature[0], feature[1]]
                )
                self.features.root_feature.verify_not_supported_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2204_VC_121870_get_not_existing_feature(self) -> None:
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2205_VC_121871_get_feature_count(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(
                response, len(FEATURES_ZONE_300.keys())
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2206_VC_121872_get_feature_id(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(
                response, FEATURES_ZONE_300
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2207_VC_121873_get_serial_number(self) -> None:
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(
                response, zone_300_api.serial_number
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2208_VC_121874_get_firmware_version(self) -> None:
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(
                response, zone_300_api.firmware_version
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2209_VC_121875_get_hardware_info(self) -> None:
        try:
            model_id = zone_300_api.model_id
            hw_revision = "02"

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(
                response, model_id, hw_revision
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2210_VC_121877_set_and_get_device_name(self) -> None:
        try:
            NAME = zone_300_api.name + " {}".format(random.randint(0, 10000))
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 30)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2211_VC_121879_get_default_device_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_default_device_name()
            self.features.device_name_feature.verify_default_name(
                response, zone_300_api.name
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2212_VC_121880_get_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(
                response, max_length=30
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2213_VC_121881_set_longer_than_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.set_device_name(
                zone_300_api.name * 5
            )
            self.features.device_name_feature.verify_error_for_setting_too_long_name(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2214_VC_121882_get_battery_status(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2215_VC_121883_get_voltage_info(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_voltage_status()
            self.features.battery_SOC_feature.verify_get_voltage_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2216_VC_121884_set_get_sleep_timer(self) -> None:
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(response, t)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2217_VC_121885_get_supported_language(self) -> None:
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2218_VC_121886_set_not_supported_language(self) -> None:
        try:
            not_supported_languages = [3]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(n)
                self.features.earcon_feature.verify_set_not_supported_language(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2219_VC_121887_get_language_capability(self) -> None:
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2220_VC_121888_set_get_earcon_state(self) -> None:
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(response, state)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2221_VC_121890_set_not_supported_earcon_state(self) -> None:
        try:
            response = self.features.earcon_feature.set_earcon_state(
                random.randint(2, 255)
            )
            self.features.earcon_feature.verify_not_supported_earcon_value(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2222_VC_121891_set_get_eq(self) -> None:
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(response, key, value)
                time.sleep(3)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2223_VC_121892_get_bt_state(self) -> None:
        try:
            response = self.features.bluetooth_crtl_feature.get_bt_state()
            self.features.bluetooth_crtl_feature.verify_get_bt_state(
                response, state=2
            )  # Connected
        except Exception as ex:
            Report.logException(str(ex))

    def test_2224_VC_121893_set_discoverable_state(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            response = self.features.bluetooth_crtl_feature.set_discoverable_state()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2225_VC_121894_set_get_mic_mute_state(self) -> None:
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

    def test_2226_VC_121895_set_not_supported_mic_mute_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_mic_mute(
                random.randint(2, 255)
            )
            self.features.headset_audio_feature.verify_not_supported_mic_mute_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2227_VC_121896_set_get_sidetone_level(self) -> None:
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

    def test_2228_VC_121897_set_not_supported_value_of_sidetone_level(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(
                random.randint(11, 255)
            )
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2229_VC_121898_get_connected_device_num(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_connected_device_number()
            )
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(
                response, CONNECTED_DEVICES
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2230_VC_121899_get_connected_device_info(self) -> None:
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

    def test_2231_VC_121900_get_connected_device_name(self) -> None:
        try:
            Report.logInfo(f"Name of connectd device is: {local_api_pc_configuration.pc_host_name}")
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

    def test_2232_VC_121901_get_audio_active_device(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_audio_active_device()
            )
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(
                response, local_api_pc_configuration.pc_bt_address, "00"
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2233_VC_121902_get_dongle_fw_version(self) -> None:
        Report.logSkip("Checking Dongle version is not available in BT mode")
        self.skipTest("Checking Dongle version is not available in BT mode")

    def test_2234_VC_121903_connected_device_status(self) -> None:
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

    def test_2235_VC_121906_connected_device_status_for_fake_device(self) -> None:
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

    def test_2236_VC_121907_get_set_A2DP_mute_status(self) -> None:
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

    def test_2237_VC_121908_set_not_supported_A2DP_state(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                local_api_pc_configuration.pc_bt_address, random.randint(2, 255)
            )
            self.features.headset_bt_conn_info_feature.verify_not_supported_A2DP_mu_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2238_VC_121909_get_pdl_device_numbers_and_info(self) -> None:
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

    def test_2239_VC_121910_set_get_voice_notification_status(self) -> None:
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

    def test_2240_VC_121911_set_not_supported_voice_notification_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(
                random.randint(2, 255)
            )
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_2241_VC_121912_factory_reset_device(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2242_VC_121913_set_get_mic_boom_status(self) -> None:
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

    def test_2243_VC_121914_set_not_supported_mic_boom_value(self) -> None:
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
    suite = unittest.TestLoader().loadTestsFromTestCase(Zone300ApiBtTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
