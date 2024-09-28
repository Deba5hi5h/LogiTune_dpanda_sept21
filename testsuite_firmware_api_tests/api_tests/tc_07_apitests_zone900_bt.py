import time
import unittest

from base import global_variables
from base.base_ui import UIBase
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, zone_900_api
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone900 import *

class Zone900APITestsBT(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(Zone900APITestsBT, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_900_api.name,
                                          conn_type=ConnectionType.bt,
                                          com_port=local_api_pc_configuration.com_port)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_900"
        global_variables.firmware_api_device_conn = ConnectionType.bt

    def test_701_VC_57572_get_protocol_version(self):
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_702_VC_57573_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_ZONE900)
            self.features.root_feature.verify_get_features_responses(response, FEATURES_ZONE900)
        except Exception as e:
            Report.logException(str(e))

    def test_703_VC_57574_get_not_supported_feature(self):
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature([feature[0], feature[1]])
                self.features.root_feature.verify_not_supported_feature(response)
        except Exception as e:
            Report.logException(str(e))

    def test_704_VC_57575_get_not_existing_feature(self):
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as e:
            Report.logException(str(e))

    def test_705_VC_57576_get_feature_count(self):
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(response, len(FEATURES_ZONE900))
        except Exception as e:
            Report.logException(str(e))

    def test_706_VC_57577_get_feature_id(self):
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(response, FEATURES_ZONE900)
        except Exception as e:
            Report.logException(str(e))

    def test_707_VC_57587_get_serial_number(self):
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(response, zone_900_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_708_VC_57588_get_firmware_version(self):
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(response, zone_900_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_709_VC_57589_get_hardware_info(self):
        try:
            hw_revision = '02'

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(response, zone_900_api.model_id, hw_revision)
        except Exception as e:
            Report.logException(str(e))

    def test_710_VC_57590_set_and_get_device_name(self):
        try:
            NAME = f"{zone_900_api.name} {random.randint(0, 100)}"
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 30)
        except Exception as e:
            Report.logException(str(e))

    def test_711_VC_57591_get_default_device_name(self):
        try:
            response = self.features.device_name_feature.get_default_device_name()
            self.features.device_name_feature.verify_default_name(response, zone_900_api.name)
        except Exception as e:
            Report.logException(str(e))

    def test_712_VC_57592_get_max_length_name(self):
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(response, max_length=30)
        except Exception as e:
            Report.logException(str(e))

    def test_713_VC_57593_set_longer_than_max_length_name(self):
        try:
            response = self.features.device_name_feature.set_device_name(zone_900_api.name * 3)
            self.features.device_name_feature.verify_error_for_setting_too_long_name(response)
        except Exception as e:
            Report.logException(str(e))

    def test_714_VC_57594_set_get_eq(self):
        Report.logSkip("EQ values needs to be defined")
        self.skipTest("EQ values needs to be defined")
        try:
            for key, value in EQ_MODES.items():
                self.features.eqset_feature.set_eq_mode(key, value)
                response = self.features.eqset_feature.get_eq_mode()
                self.features.eqset_feature.verify_get_eq_mode(response, key, value)
                time.sleep(3)
        except Exception as e:
            Report.logException(str(e))

    def test_715_VC_57597_set_get_sleep_timer(self):
        try:
            timers = [0, 5, 10, 15, 30, 60, 120, 240]

            for t in timers:
                self.features.auto_sleep_feature.set_sleep_timer(t)
                response = self.features.auto_sleep_feature.get_sleep_timer()
                self.features.auto_sleep_feature.verify_sleep_timer(response, t)
        except Exception as e:
            Report.logException(str(e))

    def test_716_VC_57646_get_bt_state(self):
        try:
            response = self.features.bluetooth_crtl_feature.get_bt_state()
            self.features.bluetooth_crtl_feature.verify_get_bt_state(response, state=2)
        except Exception as e:
            Report.logException(str(e))

    def test_717_VC_57645_set_discoverable_state(self):
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            response = self.features.bluetooth_crtl_feature.set_discoverable_state()
        except Exception as e:
            Report.logException(str(e))

    def test_718_VC_57598_set_get_mic_mute_state(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_audio_feature.set_mic_mute(status)
                response = self.features.headset_audio_feature.get_mic_mute_status()
                self.features.headset_audio_feature.verify_get_mic_mute_status(response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_719_VC_57603_set_not_supported_mic_mute_value(self):
        try:
            response = self.features.headset_audio_feature.set_mic_mute(random.randint(2, 255))
            self.features.headset_audio_feature.verify_not_supported_mic_mute_value(response)
        except Exception as e:
            Report.logException(str(e))

    def test_720_VC_57599_disable_anc(self):
        try:
            tested_status = 0
            other_states = [1, 2]
            if self.features.headset_audio_feature.get_current_anc_state() == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(random.choice(other_states))
                time.sleep(5)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_721_VC_57600_enable_anc(self):
        try:
            tested_status = 1
            other_states = [0, 2]
            if self.features.headset_audio_feature.get_current_anc_state() == f"{tested_status:02x}":
                self.features.headset_audio_feature.set_anc_state(random.choice(other_states))
                time.sleep(3)
            self.features.headset_audio_feature.set_anc_state(tested_status)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(response, tested_status)
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_722_VC_57602_anc_with_not_supported_value(self):
        try:
            response = self.features.headset_audio_feature.set_anc_state(random.randint(3, 255))
            self.features.headset_audio_feature.verify_not_supported_anc_state(response)
        except Exception as e:
            Report.logException(str(e))

    def test_723_VC_57606_set_get_sidetone_level(self):
        try:
            levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            for level in levels:
                self.features.headset_audio_feature.set_sidetone_level(level)
                response = self.features.headset_audio_feature.get_sidetone_level()
                self.features.headset_audio_feature.verify_get_sidetone_level(response, level)
        except Exception as e:
            Report.logException(str(e))

    def test_724_VC_57605_set_not_supported_value_of_sidetone_level(self):
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(random.randint(11, 255))
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(response)
        except Exception as e:
            Report.logException(str(e))

    def test_725_VC_57607_get_connected_device_num(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_connected_device_number()
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_number(response, CONNECTED_DEVICES)
        except Exception as e:
            Report.logException(str(e))

    def test_726_VC_57608_get_connected_device_info(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_connected_device_info(CONNECTED_DEVICES)
            self.features.headset_bt_conn_info_feature.verify_get_connected_device_info(response)
        except Exception as e:
            Report.logException(str(e))

    def test_727_VC_57609_get_connected_device_name(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_name(local_api_pc_configuration.pc_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(response, local_api_pc_configuration.pc_host_name)
        except Exception as e:
            Report.logException(str(e))

    def test_728_VC_57611_get_audio_active_device(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_audio_active_device()
            self.features.headset_bt_conn_info_feature.verify_get_audio_active_device(response, local_api_pc_configuration.pc_bt_address, '00')
        except Exception as e:
            Report.logException(str(e))

    def test_730_VC_57613_connected_device_status(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_status(local_api_pc_configuration.pc_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(response, CONNECTED)
        except Exception as e:
            Report.logException(str(e))

    def test_731_VC_57614_connected_device_status_for_fake_device(self):
        try:
            response = self.features.headset_bt_conn_info_feature.get_device_connected_status(local_api_pc_configuration.fake_bt_address)
            self.features.headset_bt_conn_info_feature.verify_get_device_connected_status(response, NOT_CONNECTED)
        except Exception as e:
            Report.logException(str(e))

    def test_732_VC_57616_get_set_A2DP_mute_status(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(local_api_pc_configuration.pc_bt_address, status)
                response = self.features.headset_bt_conn_info_feature.get_A2DP_mute_status(local_api_pc_configuration.pc_bt_address)
                self.features.headset_bt_conn_info_feature.verify_get_A2DP_mute_status(response, status)

                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_733_VC_57615_set_not_supported_A2DP_state(self):
        try:
            response = self.features.headset_bt_conn_info_feature.set_A2DP_mute_status(local_api_pc_configuration.pc_bt_address,
                                                                                       random.randint(2, 255))
            self.features.headset_bt_conn_info_feature.verify_not_supported_A2DP_mu_status(response)
        except Exception as e:
            Report.logException(str(e))

    def test_734_VC_57617_get_pdl_device_numbers_and_info(self):
        try:
            number_response = self.features.headset_bt_conn_info_feature.get_pdl_device_number()
            pdl_length = self.features.headset_bt_conn_info_feature.get_length_of_pdl(number_response)
            info_response = self.features.headset_bt_conn_info_feature.get_pdl_devices_info(pdl_length)
            self.features.headset_bt_conn_info_feature.verify_pdl_devices_info(info_response)
        except Exception as e:
            Report.logException(str(e))

    def test_735_VC_57623_set_get_voice_notification_status(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_voice_notification_status(status)
                response = self.features.headset_misc_feature.get_voice_notification_status()
                self.features.headset_misc_feature.verify_get_voice_notification_status(response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_736_VC_57624_set_not_supported_voice_notification_value(self):
        try:
            response = self.features.headset_misc_feature.set_voice_notification_status(random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_voice_notification_status(response)
        except Exception as e:
            Report.logException(str(e))

    def test_737_VC_57625_factory_reset_device(self):
        Report.logSkip("manual")
        self.skipTest("manual")
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as e:
            Report.logException(str(e))

    def test_738_VC_57620_set_get_mic_boom_status(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_mic_boom_status(status)
                response = self.features.headset_misc_feature.get_mic_boom_status()
                self.features.headset_misc_feature.verify_mic_boom_status(response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_739_VC_57621_set_not_supported_mic_boom_value(self):
        try:
            response = self.features.headset_misc_feature.set_mic_boom_status(random.randint(2, 255))
            self.features.headset_misc_feature.verify_not_supported_mic_boom_status(response)
        except Exception as e:
            Report.logException(str(e))

    def test_740_VC_57626_set_get_button_general_settings(self):
        try:
            self.features.headset_misc_feature.get_button_general_settings()

            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items():
                long_press = random.choice(values[0])
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                self.features.headset_misc_feature.set_button_customization_settings(button_index, long_press, short_press, tripple_press, double_press)
                time.sleep(1)
                response = self.features.headset_misc_feature.get_button_general_settings()
                self.features.headset_misc_feature.verify_get_button_general_settings(response, button_index, long_press, short_press, tripple_press, double_press)
        except Exception as e:
            Report.logException(str(e))

    def test_741_VC_57627_get_button_individual_capability(self):
        try:
            buttons = [0, 1]
            for button_index in buttons:
                response = self.features.headset_misc_feature.get_button_individual_capability(button_index)
                self.features.headset_misc_feature.verify_get_button_individual_capability(response, button_index, BUTTONS_CAPABILITIES)
        except Exception as e:
            Report.logException(str(e))

    def test_742_VC_57632_reset_button_customization_settings(self):
        try:
            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items():
                long_press = random.choice(values[0])
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                self.features.headset_misc_feature.set_button_customization_settings(button_index, long_press, short_press, tripple_press,
                                                                 double_press)
                response = self.features.headset_misc_feature.get_button_general_settings()
                self.features.headset_misc_feature.verify_get_button_general_settings(response, button_index, long_press, short_press,
                                                                  tripple_press, double_press)

            self.features.headset_misc_feature.reset_button_customization_settings()
            for button_index, values in DEFAULT_BUTTONS_GENERAL_SETTINGS.items():
                long_press = values[0]
                short_press = values[1]
                tripple_press = values[2]
                double_press = values[3]
                response = self.features.headset_misc_feature.get_button_general_settings()
                self.features.headset_misc_feature.verify_get_button_general_settings(response, button_index, long_press, short_press,
                                                                  tripple_press, double_press)
        except Exception as e:
            Report.logException(str(e))

    def test_743_VC_57628_get_capability_for_not_existing_button(self):
        try:
            response = self.features.headset_misc_feature.get_button_individual_capability(random.randint(2, 255))
            self.features.headset_misc_feature.verify_response_for_capability_for_wrong_button(response)
        except Exception as e:
            Report.logException(str(e))

    def test_744_VC_57629_set_not_supported_capablity_for_long_press_buttons(self):
        try:
            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items():
                long_press = random.randint(6, 15)
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                response = self.features.headset_misc_feature.set_button_customization_settings(button_index, long_press, short_press,
                                                                            tripple_press, double_press)
                self.features.headset_misc_feature.verify_error_for_setting_wrong_capablity_to_the_button(response)
        except Exception as e:
            Report.logException(str(e))

    def test_745_VC_57630_set_not_supported_capablity_for_short_press_buttons(self):
        try:
            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items():
                long_press = random.choice(values[0])
                short_press = random.randint(6, 15)
                tripple_press = random.choice(values[2])
                double_press = random.choice(values[3])

                response = self.features.headset_misc_feature.set_button_customization_settings(button_index, long_press, short_press,
                                                                            tripple_press, double_press)
                self.features.headset_misc_feature.verify_error_for_setting_wrong_capablity_to_the_button(response)
        except Exception as e:
            Report.logException(str(e))

    def test_746_VC_57631_set_not_supported_capability_for_double_press_buttons(self):
        try:
            for button_index, values in BUTTONS_CAPABILITIES_BY_FUNCTIONS.items():
                long_press = random.choice(values[0])
                short_press = random.choice(values[1])
                tripple_press = random.choice(values[2])
                double_press = random.randint(6, 15)

                response = self.features.headset_misc_feature.set_button_customization_settings(button_index, long_press, short_press,
                                                                            tripple_press, double_press)
                self.features.headset_misc_feature.verify_error_for_setting_wrong_capablity_to_the_button(response)
        except Exception as e:
            Report.logException(str(e))

    def test_747_VC_57633_get_supported_language(self):
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as e:
            Report.logException(str(e))

    def test_748_VC_57634_set_not_supported_language(self):
        Report.logSkip("language")
        self.skipTest("language")
        try:
            not_supported_languages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, random.randint(11, 255)]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(n)
                self.features.earcon_feature.verify_set_not_supported_language(response)
        except Exception as e:
            Report.logException(str(e))

    def test_749_VC_57635_get_language_capability(self):
        Report.logSkip("language")
        self.skipTest("language")
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(response)
        except Exception as e:
            Report.logException(str(e))

    def test_750_VC_57636_set_get_earcon_state(self):
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_751_VC_57637_set_not_supported_earcon_state(self):
        try:
            response = self.features.earcon_feature.set_earcon_state(random.randint(2, 255))
            self.features.earcon_feature.verify_not_supported_earcon_value(response)
        except Exception as e:
            Report.logException(str(e))

    def test_752_VC_57638_get_battery_status(self):
        try:
            response = self.features.battery_SOC_feature.get_battery_status()
            self.features.battery_SOC_feature.verify_get_battery_status(response)
        except Exception as e:
            Report.logException(str(e))

    def test_753_VC_57639_get_voltage_info(self):
        try:
            response = self.features.battery_SOC_feature.get_voltage_status()
            self.features.battery_SOC_feature.verify_get_voltage_status(response)
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Zone900APITestsBT)
    unittest.TextTestRunner(verbosity=2).run(suite)
