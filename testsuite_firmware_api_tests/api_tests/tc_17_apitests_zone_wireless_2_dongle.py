import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_wireless_2_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_wireless_2 import \
    FEATURES_ZONE_WIRELESS_2, MAX_LEN_NAME, EQ_MODES, CONNECTED_DEVICES, CONNECTED, NOT_CONNECTED


class ZoneWireles2ApiDongleTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(ZoneWireles2ApiDongleTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_wireless_2_api.name,
                                          conn_type=ConnectionType.dongle,
                                          com_port=local_api_pc_configuration.com_port)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_WIRELESS_2"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    @classmethod
    def tearDownClass(cls):
        cls.centurion.close_port()
        super(ZoneWireles2ApiDongleTests, cls).tearDownClass()
        
    def test_1701_VC_74320_get_protocol_version(self) -> None:
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1702_VC_74321_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_ZONE_WIRELESS_2)
            self.features.root_feature.verify_get_features_responses(
                response, FEATURES_ZONE_WIRELESS_2
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1703_VC_74322_get_not_supported_feature(self) -> None:
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature(
                    [feature[0], feature[1]]
                )
                self.features.root_feature.verify_not_supported_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1704_VC_74323_get_not_existing_feature(self) -> None:
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1705_VC_74324_get_feature_count(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(
                response, len(FEATURES_ZONE_WIRELESS_2.keys())
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1706_VC_74325_get_feature_id(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(
                response, FEATURES_ZONE_WIRELESS_2
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1707_VC_74335_get_serial_number(self) -> None:
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(
                response, zone_wireless_2_api.serial_number
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1708_VC_74336_get_firmware_version(self) -> None:
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(
                response, zone_wireless_2_api.firmware_version
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1709_VC_74337_get_hardware_info(self) -> None:
        try:
            model_id = zone_wireless_2_api.model_id
            hw_revision = "04"
            if zone_wireless_2_api.earbud_color == "ROSE":
                color_code = '0100'
            elif zone_wireless_2_api.earbud_color == "OFF-WHITE":
                color_code = '0200'
            else:
                color_code = '0000'

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(
                response, model_id, hw_revision, color_code
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1710_VC_74338_set_and_get_device_name(self) -> None:
        try:
            NAME = zone_wireless_2_api.name + " {}".format(random.randint(0, 10000))
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, MAX_LEN_NAME)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1711_VC_74339_get_default_device_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_default_device_name()
            self.features.device_name_feature.verify_default_name(
                response, zone_wireless_2_api.name
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1712_VC_74340_get_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(
                response, max_length=MAX_LEN_NAME
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1713_VC_74341_set_longer_than_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.set_device_name(
                zone_wireless_2_api.name * 5
            )
            self.features.device_name_feature.verify_error_for_setting_too_long_name(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1714_VC_74386_get_battery_status(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1715_VC_74387_get_voltage_info(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_voltage_status()
            self.features.battery_SOC_feature.verify_get_voltage_status(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1716_VC_74345_set_get_sleep_timer(self) -> None:
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(response, t)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1717_VC_74381_get_supported_language(self) -> None:
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1718_VC_74382_set_not_supported_language(self) -> None:
        try:
            not_supported_languages = [15]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(n)
                self.features.earcon_feature.verify_set_not_supported_language(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1719_VC_74383_get_language_capability(self) -> None:
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(response, device_name=zone_wireless_2_api.name)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1720_VC_74342_set_get_eq(self) -> None:
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(response, key, value)
                time.sleep(3)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1721_VC_74343_get_eq_modes(self) -> None:
        try:
            response = self.features.eqset_feature.get_eq_modes()
            self.features.eqset_feature.verify_get_eq_modes(response, EQ_MODES)
        except Exception as e:
            Report.logException(str(e))

    def test_1722_VC_74344_get_band_info(self) -> None:
        try:
            response = self.features.eqset_feature.get_band_info()
            self.features.eqset_feature.verify_get_band_info(response)
        except Exception as e:
            Report.logException(str(e))

    def test_1723_VC_74347_anc_off(self) -> None:
        try:
            tested_status = 0
            other_states = [1, 2, 3]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(5)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_1724_VC_74348_anc_on(self) -> None:
        try:
            tested_status = 1
            other_states = [0, 2, 3]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_1725_VC_74349_transparency_on(self) -> None:
        try:
            tested_status = 2
            other_states = [0, 1, 3]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_1726_VC_74350_anc_low(self) -> None:
        try:
            tested_status = 3
            other_states = [0, 1, 2]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_1727_VC_74351_anc_with_not_supported_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_anc_state(
                random.randint(4, 255))
            self.features.headset_audio_feature.verify_not_supported_anc_state(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_1728_VC_74346_set_get_mic_mute_state(self) -> None:
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

    def test_1729_VC_74352_set_not_supported_mic_mute_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_mic_mute(
                random.randint(2, 255)
            )
            self.features.headset_audio_feature.verify_not_supported_mic_mute_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1730_VC_74354_set_get_sidetone_level(self) -> None:
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

    def test_1731_VC_74353_set_not_supported_value_of_sidetone_level(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(
                random.randint(11, 255)
            )
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1732_VC_82081_set_get_anc_mode_customization(self) -> None:
        try:
            modes = [0x03, 0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
            # modes = [0x0b]
            for mode in modes:
                self.features.headset_audio_feature.set_anc_customization_mode(mode)
                response = self.features.headset_audio_feature.get_anc_customization_mode()
                self.features.headset_audio_feature.verify_get_anc_customization_mode(
                    response, mode
                )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1733_VC_82082_set_wrong_anc_customization_mode(self) -> None:
        try:
            modes = [0x00, 0x01, 0x02, 0x04, 0x08]
            for mode in modes:
                response = self.features.headset_audio_feature.set_anc_customization_mode(mode)
                self.features.headset_audio_feature.verify_set_wrong_anc_customization_mode(
                    response
                )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1734_VC_74355_get_connected_device_num(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_connected_device_number()
            )
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(
                response, CONNECTED_DEVICES
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1735_VC_74356_get_connected_device_info(self) -> None:
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

    def test_1736_VC_74357_get_connected_device_name(self) -> None:
        try:
            Report.logInfo(f"Name of connected device is: {local_api_pc_configuration.pc_host_name}")
            response = (
                self.features.headset_bt_conn_info_feature.get_device_connected_name(
                    zone_wireless_2_api.dongle_bt_address
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(
                response, zone_wireless_2_api.receiver_name
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1737_VC_74359_get_audio_active_device(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_audio_active_device()
            )
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(
                response, local_api_pc_configuration.pc_bt_address, "00"
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1738_VC_74361_connected_device_status(self) -> None:
        try:
            response = (
                self.features.headset_bt_conn_info_feature.get_device_connected_status(
                    zone_wireless_2_api.dongle_bt_address
                )
            )
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, CONNECTED
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1739_VC_74362_connected_device_status_for_fake_device(self) -> None:
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

    def test_1740_VC_74364_get_set_A2DP_mute_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                    local_api_pc_configuration.pc_bt_address, status
                )
                response = (
                    self.features.headset_bt_conn_info_feature.get_A2DP_mute_status(
                        local_api_pc_configuration.pc_bt_address
                    )
                )
                self.features.headset_bt_conn_info_feature.verify_get_A2DP_mute_status_cybermorh(
                    response
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1741_VC_74363_set_not_supported_A2DP_state(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                local_api_pc_configuration.pc_bt_address, random.randint(2, 255)
            )
            self.features.headset_bt_conn_info_feature.verify_not_supported_A2DP_mu_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1742_VC_74365_get_pdl_device_numbers_and_info(self) -> None:
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

    def test_1743_VC_74371_set_get_voice_notification_status(self) -> None:
        try:
            statuses = [0, 1, 2]
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

    def test_1744_VC_74372_set_not_supported_voice_notification_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(
                random.randint(3, 255)
            )
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1745_VC_74373_factory_reset_device(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_1746_VC_74368_set_get_mic_boom_status(self) -> None:
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

    def test_1747_VC_74369_set_not_supported_mic_boom_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_mic_boom_status(
                random.randint(2, 255)
            )
            self.features.headset_misc_feature.verify_not_supported_mic_boom_status(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1748_VC_79297_set_get_ai_reduction_state(self) -> None:
        try:
            statuses = [0, 1, 2, 3]
            for status in statuses:
                self.features.ai_noise_reduction.set_ai_noise_reduction_state(status)
                response = self.features.ai_noise_reduction.get_ai_noise_reduction_state()
                self.features.ai_noise_reduction.verify_get_ai_noise_reduction_state(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1749_VC_79300_set_not_supported_ai_noise_reduction_state(self) -> None:
        try:
            response = self.features.ai_noise_reduction.set_ai_noise_reduction_state(
                random.randint(4, 255)
            )
            self.features.ai_noise_reduction.verify_not_supported_ai_noise_reduction_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1750_VC_79299_set_get_anti_startle_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.anti_startle.set_anti_startle(status)
                response = self.features.anti_startle.get_anti_startle()
                self.features.anti_startle.verify_get_anti_startle(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1751_VC_79302_set_not_supported_anti_startle_state(self) -> None:
        try:
            response = self.features.anti_startle.set_anti_startle(
                random.randint(2, 255)
            )
            self.features.anti_startle.verify_not_supported_anti_startle_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1752_VC_79298_set_get_noise_exposure_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.noise_exposure.set_noise_exposure_state(status)
                response = self.features.noise_exposure.get_noise_exposure_state()
                self.features.noise_exposure.verify_get_noise_exposure_state(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1753_VC_79301_set_not_supported_noise_exposure_state(self) -> None:
        try:
            response_1 = self.features.noise_exposure.set_noise_exposure_state(2)
            self.features.noise_exposure.verify_not_supported_noise_exposure_value(
                response_1
            )

            response_2 = self.features.noise_exposure.set_noise_exposure_state(
                random.randint(3, 255)
            )
            self.features.noise_exposure.verify_not_supported_noise_exposure_value(
                response_2
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1754_VC_80432_set_get_ear_detection_state(self) -> None:
        try:
            self.features.tw_in_ear_detection_feature.get_ear_detection_state()
            states = [0, 1]
            for state in states:
                self.features.tw_in_ear_detection_feature.set_ear_detection_state(
                    state)
                response = self.features.tw_in_ear_detection_feature.get_ear_detection_state(
                )
                self.features.tw_in_ear_detection_feature.verify_get_ear_detection_state(
                    response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_1755_VC_80434_set_not_supported_notification_state(self) -> None:
        try:
            response = self.features.tw_in_ear_detection_feature.set_ear_detection_state(
                random.randint(2, 255))
            self.features.tw_in_ear_detection_feature.verify_not_supported_set_ear_detection_state(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_1756_VC_82083_set_get_auto_answer_on_call_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.auto_call_answer.set_auto_answer_on_call(status)
                response = self.features.auto_call_answer.get_auto_answer_on_call()
                self.features.auto_call_answer.verify_get_auto_answer_on_call(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1757_VC_82084_set_not_supported_auto_answer_on_call_state(self) -> None:
        try:
            response = self.features.auto_call_answer.set_auto_answer_on_call(
                random.randint(2, 255)
            )
            self.features.auto_call_answer.verify_not_supported_auto_answer_on_call_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1758_VC_82085_set_get_auto_mute_on_call_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.auto_mute_on_call.set_auto_mute_on_call(status)
                response = self.features.auto_mute_on_call.get_auto_mute_on_call()
                self.features.auto_mute_on_call.verify_get_auto_mute_on_call(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1759_VC_82086_set_not_supported_auto_mute_on_call_state(self) -> None:
        try:
            response = self.features.auto_mute_on_call.set_auto_mute_on_call(
                random.randint(2, 255)
            )
            self.features.auto_mute_on_call.verify_not_supported_auto_mute_on_call_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1760_VC_98853_set_get_touch_sensor_state(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.touch_sensor_state.set_touch_sensor_state(status)
                response = self.features.touch_sensor_state.get_touch_sensor_state()
                self.features.touch_sensor_state.verify_get_touch_sensor_state(
                    response, status
                )
                time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1761_VC_98854_set_not_supported_touch_sensor_state(self) -> None:
        try:
            response = self.features.touch_sensor_state.set_touch_sensor_state(
                random.randint(2, 255)
            )
            self.features.touch_sensor_state.verify_not_supported_touch_sensor_state(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))

    def test_1762_VC_98857_set_headset_active_eq(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                for key, value in EQ_MODES.items():
                    self.features.eqset_feature.set_eq_mode(key, value)
                    time.sleep(2)
                    self.features.headset_active_eq.set_headset_active_eq(status, key, value)
                    response = self.features.headset_active_eq.get_headset_active_eq()
                    self.features.headset_active_eq.verify_get_headset_active_eq(
                        response, status
                    )
                    time.sleep(5)
        except Exception as ex:
            Report.logException(str(ex))

    def test_1763_VC_98856_set_not_supported_headset_active_eq_state(self) -> None:
        try:
            response = self.features.headset_active_eq.set_headset_active_eq(
                random.randint(2, 255), -1, []
            )
            self.features.headset_active_eq.verify_not_supported_headset_active_eq(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(ZoneWireles2ApiDongleTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
