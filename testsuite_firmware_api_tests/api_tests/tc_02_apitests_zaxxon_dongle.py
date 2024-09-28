import time
import unittest

from base import global_variables
from base.base_ui import UIBase
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_true_wireless_api
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zaxxon import *


class ZaxxonApiDongleTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1KHmBVfWP5ZW5X2rYUDOkbDej6pd50I8OpiqrtQot4wY/edit#gid=2073661613
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(ZaxxonApiDongleTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_true_wireless_api.name,
                                          conn_type=ConnectionType.dongle)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_TRUE_WIRELESS"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    def test_201_VC_57349_get_protocol_version(self) -> None:
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_202_VC_57350_get_features(self) -> None:
        try:
            response = self.features.root_feature.get_features(FEATURES_ZAXXON)
            self.features.root_feature.verify_get_features_responses(
                response, FEATURES_ZAXXON)
        except Exception as e:
            Report.logException(str(e))

    def test_203_VC_57351_get_not_supported_feature(self) -> None:
        try:
            for feature in [[1, 12], [10, 13]]:
                response = self.features.root_feature.get_not_supported_feature(
                    [feature[0], feature[1]])
                self.features.root_feature.verify_not_supported_feature(
                    response)
        except Exception as e:
            Report.logException(str(e))

    def test_204_VC_57352_get_not_existing_feature(self) -> None:
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as e:
            Report.logException(str(e))

    def test_205_VC_57353_get_feature_count(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(
                response, len(FEATURES_ZAXXON))
        except Exception as e:
            Report.logException(str(e))

    def test_206_VC_57354_get_feature_id(self) -> None:
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(
                response, FEATURES_ZAXXON)
        except Exception as e:
            Report.logException(str(e))

    def test_207_VC_57355_get_connection_info(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_connection_info(
            )
            self.features.cent_pp_bridge_feature.verify_get_connection_info(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_208_VC_57356_get_protocol_version_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_protocol_version_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_protocol_version_from_secondary_earbud(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_209_VC_57357_get_features_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_features_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_features_from_secondary_earbud(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_210_VC_57358_get_feature_count_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_feature_count_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_feature_count_from_secondary_earbud(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_211_VC_57359_get_feature_id_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_feature_id_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_feature_id_from_secondary_earbud_dongle(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_212_VC_57360_get_serial_number_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_serial_number_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_serial_number_from_secondary_earbud_dongle(
                response, zone_true_wireless_api.secondary_serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_213_VC_57361_get_firmware_version_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_firmware_version_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_firmware_version_from_secondary_earbud(
                response, zone_true_wireless_api.firmware_version)
        except Exception as e:
            Report.logException(str(e))

    def test_214_VC_57362_get_hardware_info_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_hardware_info_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_hardware_info_from_secondary_earbud(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_215_VC_57363_get_battery_status_from_secondary_earbud(self) -> None:
        try:
            response = self.features.cent_pp_bridge_feature.get_battery_status_from_secondary_earbud(
            )
            self.features.cent_pp_bridge_feature.verify_get_battery_status_from_secondary_earbud(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_216_VC_57364_get_serial_number(self) -> None:
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(
                response, zone_true_wireless_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_217_VC_57365_get_firmware_version(self) -> None:
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(
                response, zone_true_wireless_api.firmware_version)
        except Exception as e:
            Report.logException(str(e))

    def test_218_VC_57366_get_hardware_info(self) -> None:
        try:
            hw_revision = '01'
            color_code = '0100' if zone_true_wireless_api.earbud_color == "ROSE" else '0000'
            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(
                response, zone_true_wireless_api.model_id, hw_revision, color_code)
        except Exception as e:
            Report.logException(str(e))

    def test_219_VC_57367_set_and_get_device_name(self) -> None:
        try:
            NAME = f"{zone_true_wireless_api.name} {random.randint(0, 100)}"
            self.features.device_name_feature.set_device_name(NAME)
            time.sleep(1)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 31)
        except Exception as e:
            Report.logException(str(e))

    def test_220_VC_57368_get_default_device_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_default_device_name(
            )
            self.features.device_name_feature.verify_default_name(
                response, zone_true_wireless_api.name)
        except Exception as e:
            Report.logException(str(e))

    def test_221_VC_57369_get_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(
                response, max_length=31)
        except Exception as e:
            Report.logException(str(e))

    def test_222_VC_57370_set_longer_than_max_length_name(self) -> None:
        try:
            response = self.features.device_name_feature.set_device_name(
                zone_true_wireless_api.name * 2)
            self.features.device_name_feature.verify_error_for_setting_too_long_name(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_223_VC_57371_set_get_eq(self) -> None:
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(
                    response, key, value)
                time.sleep(3)
        except Exception as e:
            Report.logException(str(e))

    def test_224_VC_57372_get_eq_modes(self) -> None:
        try:
            response = self.features.eqset_feature.get_eq_modes()
            self.features.eqset_feature.verify_get_eq_modes(response, EQ_MODES)
        except Exception as e:
            Report.logException(str(e))

    def test_225_VC_57373_get_band_info(self) -> None:
        try:
            response = self.features.eqset_feature.get_band_info()
            self.features.eqset_feature.verify_get_band_info(response)
        except Exception as e:
            Report.logException(str(e))

    def test_226_VC_57374_set_get_sleep_timer(self) -> None:
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(
                    response, t)
        except Exception as e:
            Report.logException(str(e))

    def test_227_VC_57376_disable_anc(self) -> None:
        try:
            tested_status = 0
            other_states = [1, 2]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                time.sleep(1)
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            time.sleep(2)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_228_VC_57377_enable_anc(self) -> None:
        try:
            tested_status = 1
            other_states = [0, 2]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                time.sleep(1)
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            time.sleep(1)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_229_VC_57378_enable_transparency_on(self) -> None:
        try:
            tested_status = 2
            other_states = [0, 1]
            if self.features.headset_audio_feature.get_current_anc_state(
            ) == f"{tested_status:02x}":
                time.sleep(1)
                self.features.headset_audio_feature.set_anc_state(
                    random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            time.sleep(1)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(
                response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_230a_VC_57379_anc_with_not_supported_value(self) -> None:
        try:
            response = self.features.headset_audio_feature.set_anc_state(
                random.randint(3, 255))
            self.features.headset_audio_feature.verify_not_supported_anc_state(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_230_VC_57382_set_get_sidetone_level(self) -> None:
        try:
            levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            level = random.choice(levels)

            res1 = self.features.headset_audio_feature.set_sidetone_level(
                level)
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(
                res1)
        except Exception as e:
            Report.logException(str(e))

    def test_231_VC_57383_get_connected_device_num(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_connected_device_number(
            )
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(
                response, CONNECTED_DEVICES)
        except Exception as e:
            Report.logException(str(e))

    def test_232_VC_57384_get_connected_device_info(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_connected_device_info(
                CONNECTED_DEVICES)
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_info(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_233_VC_57385_get_connected_device_name(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_name(
                zone_true_wireless_api.dongle_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(
                response, zone_true_wireless_api.receiver_name)
        except Exception as e:
            Report.logException(str(e))

    def test_234_VC_57386_get_connected_device_name_mobile(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_name(
                local_api_pc_configuration.mobile_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(
                response, local_api_pc_configuration.mobile_name.replace("_", " "))
        except Exception as e:
            Report.logException(str(e))

    def test_235_VC_57387_get_audio_active_device(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_audio_active_device(
            )
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(
                response, zone_true_wireless_api.dongle_bt_address, '00')
        except Exception as e:
            Report.logException(str(e))

    def test_236_VC_57388_get_dongle_fw_version(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_dongle_fw_version(
            )
            self.features.headset_bt_conn_info_feature.verify_error_message_on_get_driver_fw_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_237_VC_57389_connected_device_status(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_status(
                zone_true_wireless_api.dongle_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, CONNECTED)
        except Exception as e:
            Report.logException(str(e))

    def test_238_VC_57390_connected_device_status_for_fake_device(self) -> None:
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_status(
                local_api_pc_configuration.fake_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(
                response, NOT_CONNECTED)
        except Exception as e:
            Report.logException(str(e))

    def test_239_VC_57392_get_set_A2DP_mute_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(
                    zone_true_wireless_api.dongle_bt_address, status)
                response = self.features.headset_bt_conn_info_feature.get_A2DP_mute_status(
                    zone_true_wireless_api.dongle_bt_address)
                self.features.headset_bt_conn_info_feature.verify_get_A2DP_mute_status(
                    response, status)

                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_240_VC_57393_get_pdl_device_numbers_and_info(self) -> None:
        try:
            number_response = self.features.headset_bt_conn_info_feature.get_pdl_device_number(
            )
            pdl_length = self.features.headset_bt_conn_info_feature.get_length_of_pdl(
                number_response)
            info_response = self.features.headset_bt_conn_info_feature.get_pdl_devices_info(
                pdl_length)
            self.features.headset_bt_conn_info_feature.verify_pdl_devices_info(
                info_response)
        except Exception as e:
            Report.logException(str(e))

    def test_241_VC_57394_remove_device_from_pdl(self) -> None:
        Report.logSkip("ZAX-342")
        self.skipTest("ZAX-342")
        try:
            self.features.headset_bt_conn_info_feature.remove_device_from_pdl()
        except Exception as e:
            Report.logException(str(e))

    def test_242_VC_57395_set_get_do_not_disturb_mode(self) -> None:
        try:
            modes = [0, 1]
            for mode in modes:
                self.features.headset_misc_feature.set_do_not_disturb_mode(
                    mode)
                response = self.features.headset_misc_feature.get_do_not_disturb_mode(
                )
                self.features.headset_misc_feature.verify_get_do_not_disturb_mode(
                    response, mode)
        except Exception as e:
            Report.logException(str(e))

    def test_243_VC_57398_set_not_supported_do_not_disturb_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_do_not_disturb_mode(
                random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_do_not_disturb_mode_state(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_244_VC_57399_set_get_voice_notification_status(self) -> None:
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_voice_notification_status(
                    status)
                response = self.features.headset_misc_feature.get_voice_notification_status(
                )
                self.features.headset_misc_feature.verify_get_voice_notification_status(
                    response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_245_VC_57399_set_not_supported_voice_notification_value(self) -> None:
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(
                random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_246_VC_57401_factory_reset_device(self) -> None:
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as e:
            Report.logException(str(e))

    def test_247_VC_57402_set_get_button_general_settings(self) -> None:
        try:
            self.features.headset_misc_feature.get_button_general_settings()

            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items(
            ):
                long_press = random.choice(values[0])
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                self.features.headset_misc_feature.set_button_customization_settings(
                    button_index, long_press, short_press, tripple_press,
                    double_press)
                response = self.features.headset_misc_feature.get_button_general_settings(
                )
                self.features.headset_misc_feature.verify_get_button_general_settings(
                    response, button_index, long_press, short_press,
                    tripple_press, double_press)
        except Exception as e:
            Report.logException(str(e))

    def test_248_VC_57403_get_button_individual_capability(self) -> None:
        try:
            buttons = [0, 1]
            for button_index in buttons:
                response = self.features.headset_misc_feature.get_button_individual_capability(
                    button_index)
                self.features.headset_misc_feature.verify_get_button_individual_capability(
                    response, button_index, BUTTONS_CAPABILITIES)
        except Exception as e:
            Report.logException(str(e))

    def test_249_VC_55806_get_capability_for_not_existing_button(self) -> None:
        try:
            response = self.features.headset_misc_feature.get_button_individual_capability(
                random.randint(2, 255))
            self.features.headset_misc_feature.verify_response_for_capability_for_wrong_button(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_253_VC_57408_reset_button_customization_settings(self) -> None:
        try:
            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items(
            ):
                long_press = random.choice(values[0])
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                self.features.headset_misc_feature.set_button_customization_settings(
                    button_index, long_press, short_press, tripple_press,
                    double_press)
                response = self.features.headset_misc_feature.get_button_general_settings(
                )
                self.features.headset_misc_feature.verify_get_button_general_settings(
                    response, button_index, long_press, short_press,
                    tripple_press, double_press)

            self.features.headset_misc_feature.reset_button_customization_settings(
            )
            for button_index, values in DEFAULT_BUTTONS_GENERAL_SETTINGS.items(
            ):
                long_press = values[0]
                short_press = values[1]
                tripple_press = values[2]
                double_press = values[3]
                response = self.features.headset_misc_feature.get_button_general_settings(
                )
                self.features.headset_misc_feature.verify_get_button_general_settings(
                    response, button_index, long_press, short_press,
                    tripple_press, double_press)
        except Exception as e:
            Report.logException(str(e))

    def test_254_VC_57409_get_supported_language(self) -> None:
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as e:
            Report.logException(str(e))

    def test_255_VC_57410_set_not_supported_language(self) -> None:
        try:
            # Changing language is not supported yet
            not_supported_languages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(
                    n)
                self.features.earcon_feature.verify_set_not_supported_language(
                    response)
        except Exception as e:
            Report.logException(str(e))

    def test_256_VC_57411_get_language_capability(self) -> None:
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_257_VC_57412_set_get_earcon_state(self) -> None:
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(
                    response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_258_VC_57413_set_not_supported_earcon_state(self) -> None:
        try:
            response = self.features.earcon_feature.set_earcon_state(
                random.randint(2, 255))
            self.features.earcon_feature.verify_not_supported_earcon_value(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_259_VC_55816_get_battery_status(self) -> None:
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_260_VC_57416_get_buds_case_aes_key(self) -> None:
        try:
            response = self.features.zaxxon_bud_case_key_feature.get_buds_case_aes_key(
            )
            self.features.zaxxon_bud_case_key_feature.verify_get_buds_case_aes_key(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_261_VC_57417_get_role(self) -> None:
        try:
            response = self.features.tw_role_switching_feature.get_role()
            self.features.tw_role_switching_feature.verify_get_role(response)
        except Exception as e:
            Report.logException(str(e))

    def test_262_VC_57418_set_get_notification_state(self) -> None:
        try:
            states = [0, 1]
            for state in states:
                self.features.tw_role_switching_feature.set_notification_state(
                    state)
                time.sleep(1)
                response = self.features.tw_role_switching_feature.get_notification_state(
                )
                self.features.tw_role_switching_feature.verify_get_notification_state(
                    response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_263_VC_57419_set_not_supported_notification_state(self) -> None:
        try:
            response = self.features.tw_role_switching_feature.set_notification_state(
                random.randint(2, 255))
            self.features.tw_role_switching_feature.verify_not_supported_notification_status(
                response)
        except Exception as e:
            Report.logException(str(e))

    def test_264_VC_57420_set_get_ear_detection_state(self) -> None:
        try:
            states = [1, 0]
            for state in states:
                self.features.tw_in_ear_detection_feature.set_ear_detection_state(
                    state)
                time.sleep(1)
                response = self.features.tw_in_ear_detection_feature.get_ear_detection_state(
                )
                self.features.tw_in_ear_detection_feature.verify_get_ear_detection_state(
                    response, state)
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ZaxxonApiDongleTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
