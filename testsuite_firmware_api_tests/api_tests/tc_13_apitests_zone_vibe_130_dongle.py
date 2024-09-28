import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_vibe_130_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_vibe_130 import (
    FEATURES_ZONE_VIBE_130, EQ_MODES, CONNECTED_DEVICES, CONNECTED,
    NOT_CONNECTED)


class ZoneVibe130ApiDongleTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(ZoneVibe130ApiDongleTests, cls).setUpClass()
        cls.centurion = CenturionCommands(
            device_name=zone_vibe_130_api.name,
            conn_type=ConnectionType.dongle)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_VIBE_130"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    def test_1501_VC_80449_get_protocol_version(self) -> None:
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1502_VC_80450_get_features(self) -> None:
        try:
            response = self.features.root_feature.get_features(
                FEATURES_ZONE_VIBE_130)
            self.features.root_feature.verify_get_features_responses(
                response, FEATURES_ZONE_VIBE_130)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1503_VC_80451_get_not_supported_feature(self) -> None:
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature(
                    [feature[0], feature[1]])
                self.features.root_feature.verify_not_supported_feature(
                    response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1504_VC_80452_get_not_existing_feature(self) -> None:
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1505_VC_80453_get_feature_count(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(
                response, len(FEATURES_ZONE_VIBE_130.keys()))
        except Exception as ex:
            Report.logException(str(ex))

    def test_1506_VC_80454_get_feature_id(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(
                response, FEATURES_ZONE_VIBE_130)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1507_VC_80455_get_serial_number(self) -> None:
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(
                response, zone_vibe_130_api.serial_number)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1508_VC_80456_get_firmware_version(self) -> None:
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(
                response, zone_vibe_130_api.firmware_version)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1509_VC_80457_get_hardware_info(self) -> None:
        try:
            model_id = zone_vibe_130_api.model_id
            hw_revision = "00"

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(
                response, model_id, hw_revision)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1510_VC_80458_set_and_get_device_name(self) -> None:
        try:
            NAME = f"{zone_vibe_130_api.name} {random.randint(0, 1000000)}"
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 30)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1511_VC_80459_get_default_device_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_default_device_name(
            )
            self.features.device_name_feature.verify_default_name(
                response, zone_vibe_130_api.name)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1512_VC_80460_get_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(
                response, max_length=30)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1513_VC_80461_set_longer_than_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.set_device_name(
                zone_vibe_130_api.name * 5)
            self.features.device_name_feature.verify_error_for_setting_too_long_name(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1514_VC_80462_get_battery_status(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1515_VC_80463_get_voltage_info(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_voltage_status()
            self.features.battery_SOC_feature.verify_get_voltage_status(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1516_VC_80464_set_get_sleep_timer(self) -> None:
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(
                    response, t)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1517_VC_80465_get_supported_language(self) -> None:
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1518_VC_80466_set_not_supported_language(self) -> None:
        try:
            not_supported_languages = [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                random.randint(11, 255),
            ]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(
                    n)
                self.features.earcon_feature.verify_set_not_supported_language(
                    response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1519_VC_80467_get_language_capability(self) -> None:
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1520_VC_80468_set_get_earcon_state(self) -> None:
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(
                    response, state)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1521_VC_80469_set_not_supported_earcon_state(self) -> None:
        try:
            response = self.features.earcon_feature.set_earcon_state(
                random.randint(2, 255))
            self.features.earcon_feature.verify_not_supported_earcon_value(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1522_VC_80470_set_get_eq(self) -> None:
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(
                    response, key, value)
                time.sleep(3)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1523_VC_80471_get_bt_state(self) -> None:
        try:
            response = self.features.bluetooth_crtl_feature.get_bt_state()
            self.features.bluetooth_crtl_feature.verify_get_bt_state(
                response, state=2)  # Connected
        except Exception as ex:
            Report.logException(str(ex))

    def test_1524_VC_80472_set_discoverable_state(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")

        try:
            response = self.features.bluetooth_crtl_feature.set_discoverable_state(
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1525_VC_80473_set_get_mic_mute_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_audio_feature.set_mic_mute(status)
                response = self.features.headset_audio_feature.get_mic_mute_status(
                )
                self.features.headset_audio_feature.verify_get_mic_mute_status(
                    response, status)
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1526_VC_80474_set_not_supported_mic_mute_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_mic_mute(
                random.randint(2, 255))
            self.features.headset_audio_feature.verify_not_supported_mic_mute_value(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1527_VC_80475_set_get_sidetone_level(self) -> None:
        try:
            levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            for level in levels:
                self.features.headset_audio_feature.set_sidetone_level(level)
                response = self.features.headset_audio_feature.get_sidetone_level(
                )
                self.features.headset_audio_feature.verify_get_sidetone_level(
                    response, level)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1528_VC_80476_set_not_supported_value_of_sidetone_level(
            self) -> None:
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(
                random.randint(11, 255))
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1529_VC_80477_get_connected_device_num(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_connected_device_number())
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(
                response, CONNECTED_DEVICES)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1530_VC_80478_get_connected_device_info(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_connected_device_info(CONNECTED_DEVICES))
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_info(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1531_VC_80479_get_connected_device_name(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_device_connected_name(
                            zone_vibe_130_api.dongle_bt_address))
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(
                response, zone_vibe_130_api.receiver_name)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1532_VC_80481_get_audio_active_device(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_audio_active_device())
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(
                response, zone_vibe_130_api.dongle_bt_address, "00")
        except Exception as ex:
            Report.logException(str(ex))

    def test_1533_VC_80482_get_dongle_fw_version(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_dongle_fw_version())
            self.features.headset_bt_conn_info_feature.verify_get_dongle_fw_version(
                response, zone_vibe_130_api.dongle_firmware_version)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1534_VC_80483_connected_device_status(self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_device_connected_status(
                            zone_vibe_130_api.dongle_bt_address))
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, CONNECTED)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1535_VC_80484_connected_device_status_for_fake_device(
            self) -> None:
        try:
            response = (self.features.headset_bt_conn_info_feature.
                        get_device_connected_status(
                            local_api_pc_configuration.fake_bt_address))
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, NOT_CONNECTED)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1536_VC_80485_get_set_A2DP_mute_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                    zone_vibe_130_api.dongle_bt_address, status)
                response = (self.features.headset_bt_conn_info_feature.
                            get_A2DP_mute_status(
                                zone_vibe_130_api.dongle_bt_address))
                self.features.headset_bt_conn_info_feature.verify_get_A2DP_mute_status(
                    response, status)
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1537_VC_80492_set_not_supported_A2DP_state(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                zone_vibe_130_api.dongle_bt_address,
                random.randint(2, 255))
            self.features.headset_bt_conn_info_feature.verify_not_supported_A2DP_mu_status(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1538_VC_80486_get_pdl_device_numbers_and_info(self) -> None:
        try:
            number_response = (self.features.headset_bt_conn_info_feature.
                               get_pdl_device_number())
            pdl_length = self.features.headset_bt_conn_info_feature.get_length_of_pdl(
                number_response)
            info_response = (self.features.headset_bt_conn_info_feature.
                             get_pdl_devices_info(pdl_length))
            self.features.headset_bt_conn_info_feature.verify_pdl_devices_info(
                info_response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1539_VC_80487_set_get_voice_notification_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_voice_notification_status(
                    status)
                response = (self.features.headset_misc_feature.
                            get_voice_notification_status())
                self.features.headset_misc_feature.verify_get_voice_notification_status(
                    response, status)
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1540_VC_80488_set_not_supported_voice_notification_value(
            self) -> None:
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(
                random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(
                response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1541_VC_80489_factory_reset_device(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1542_VC_80490_set_get_mic_boom_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_mic_boom_status(status)
                response = self.features.headset_misc_feature.get_mic_boom_status(
                )
                self.features.headset_misc_feature.verify_mic_boom_status(
                    response, status)
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1543_VC_80491_set_not_supported_mic_boom_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_mic_boom_status(
                random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_mic_boom_status(
                response)
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(
        ZoneVibe130ApiDongleTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
