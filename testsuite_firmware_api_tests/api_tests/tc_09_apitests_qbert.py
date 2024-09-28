import unittest

from base import global_variables
from base.base_ui import UIBase
from testsuite_firmware_api_tests.api_tests.api_parameters import logi_dock_api
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_qbert import *


class QbertAPIDongleTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(QbertAPIDongleTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=logi_dock_api.name,
                                          conn_type=ConnectionType.usb_dock)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "LOGI_DOCK"
        global_variables.firmware_api_device_conn = ConnectionType.usb_dock

    def test_901_VC_xy_get_protocol_version(self):
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_902_VC_xy_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_QBERT)
            self.features.root_feature.verify_get_features_responses(response, FEATURES_QBERT)
        except Exception as e:
            Report.logException(str(e))

    def test_903_VC_xy_get_feature_count(self):
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(response, len(FEATURES_QBERT.keys()))
        except Exception as e:
            Report.logException(str(e))

    def test_904_VC_xy_get_feature_id(self):
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(response, FEATURES_QBERT)
        except Exception as e:
            Report.logException(str(e))

    def test_905_VC_xyz_get_serial_number(self):
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(response, logi_dock_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_906_VC_xyz_get_firmware_version(self):
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(response, logi_dock_api.firmware_version)
        except Exception as e:
            Report.logException(str(e))

    def test_907_VC_xyz_get_hardware_info(self):
        try:
            hw_revision = '04'

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(response, logi_dock_api.model_id, hw_revision)
        except Exception as e:
            Report.logException(str(e))

    def test_908_VC_xyz_set_and_get_device_name(self):
        try:
            NAME = f"{logi_dock_api.name} {random.randint(0, 1000000)}"
            self.features.device_name_feature.set_device_name(NAME)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, NAME, 48)
        except Exception as e:
            Report.logException(str(e))

    def test_909_VC_xyz_get_default_device_name(self):
        try:
            response = self.features.device_name_feature.get_default_device_name()
            self.features.device_name_feature.verify_default_name(response, logi_dock_api.name)
        except Exception as e:
            Report.logException(str(e))

    def test_910_VC_xyz_get_max_length_name(self):
        try:
            response = self.features.device_name_feature.get_max_name_length()
            self.features.device_name_feature.verify_device_name_max_lenght(response, max_length=48)
        except Exception as e:
            Report.logException(str(e))

    def test_911_VC_xyz_set_max_len_name(self):
        try:
            self.features.device_name_feature.set_device_name("A" * 48)
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, "A" * 48, 48)
        except Exception as e:
            Report.logException(str(e))

    def test_912_VC_xyz_set_longer_than_max_length_name(self):
        try:
            response = self.features.device_name_feature.set_device_name("B" * 49)
            self.features.device_name_feature.verify_error_for_setting_too_long_name(response)
        except Exception as e:
            Report.logException(str(e))

    def test_013_VC_xzy_prepare(self):
        assert 1 == 0, "Not implemented yet"

    def test_914_VC_xzy_get_status_thermal_sensors(self):
        try:
            response = self.features.thermal_sensors.get_status_thermal_sensors()
            self.features.thermal_sensors.verify_get_status_thermal_sensors(response)
        except Exception as e:
            Report.logException(str(e))

    def test_915_VC_xzy_iCentPPBridge(self):
        assert 1 == 0, "Not implemented yet"

    def test_916_VC_xzy_set_get_hdmi_mode(self):
        try:
            self.features.usb_control.get_hdmi_state()
            states = [0]
            for state in states:
                self.features.usb_control.set_hdmi_state(state)
                response = self.features.usb_control.get_hdmi_state()
                self.features.usb_control.verify_get_hdmi_state(response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_917_VC_xzy_get_port_info(self):
        try:
            response = self.features.usb_control.get_port_info()
            self.features.usb_control.verify_get_port_info(response)
        except Exception as e:
            Report.logException(str(e))

    def test_918_VC_xzy_get_port_status(self):
        try:
            response = self.features.usb_control.get_port_status()
            assert 1 == 0, "Check if this metod is supported and how it works"
        except Exception as e:
            Report.logException(str(e))

    def test_919_VC_xzy_enable_event(self):
        assert 1 == 0, "Check if this metod is supported and how it works"
        # try:
        #     states = [0, 1]
        #     for state in states:
        #         response = self.features.usb_control.set_enable_event(state)
        # except Exception as e:
        #     Report.logException(str(e))

    def test_920_VC_set_port_power(self):
        assert 1 == 0, "Check if this metod is supported and how it works"
        # try:
        #     response = self.features.usb_control.set_port_power()
        # except Exception as e:
        #     Report.logException(str(e))

    def test_921_VC_xyz_set_get_eq(self):
        assert 1 == 0, "Implementation not finished yet"
        # try:
        #     for key, value in EQ_MODES.items():
        #         self.features.eqset_feature.set_eq_mode(key, value)
        #         response = self.features.eqset_feature.get_eq_mode()
        #         self.features.eqset_feature.verify_get_eq_mode(response, key, value)
        #         time.sleep(3)
        #     assert 1 == 0, "Implementation not finished yet"
        # except Exception as e:
        #     Report.logException(str(e))

    def test_922_VC_xzy_set_get_unmute_mode(self):
        try:
            response = self.features.video_mute.get_unmute_mode()
        except Exception as e:
            Report.logException(str(e))

    def test_923_VC_xzy_get_registered_apps_ids(self):
        try:
            response = self.features.video_mute.get_registered_app_ids()
        except Exception as e:
            Report.logException(str(e))

    def test_924_VC_xzy_get_video_mute_state(self):
        try:
            response = self.features.video_mute.get_video_mute_state()
        except Exception as e:
            Report.logException(str(e))

    def test_976_VC_xyz_start_and_cancel_ambient_led(self):
        try:
            response = self.features.ambient_led.set_start_ambient_led()
            self.features.ambient_led.set_cancel_ambient_led(response[-1])
        except Exception as e:
            Report.logException(str(e))

    def test_926_VC_xyz_start_custom_and_cancel_ambient_led(self):
        try:
            response = self.features.ambient_led.set_start_custom_ambient_led()
            response = self.features.ambient_led.set_cancel_ambient_led()
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_get_speakerphone_info(self):
        try:
            response = self.features.speaker_phone.get_speakerphone_info()
            self.features.speaker_phone.verify_get_speakerphone_info()
        except Exception as e:
            Report.logException(str(e))


    def test_925a_VC_xyz_get_audio_state(self):
        try:
            response = self.features.speaker_phone.get_audio_state()
            self.features.speaker_phone.verify_get_audio_state(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925b_VC_xyz_get_connection_state(self):
        try:
            response = self.features.speaker_phone.get_connection_state()
            self.features.speaker_phone.verify_get_connection_state(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925c_VC_xyz_get_pairing_state(self):
        try:
            response = self.features.speaker_phone.get_pairing_state()
            self.features.speaker_phone.verify_get_pairing_state(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925d_VC_xyz_get_paired_devices_info(self):
        try:
            response = self.features.speaker_phone.get_paired_device_info()
            self.features.speaker_phone.verify_get_paired_device_info(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_set_get_led_state(self):
        try:
            states = [0, 1, 2]
            for state in states:
                self.features.one_touch_join.set_led_state(state)
                response = self.features.one_touch_join.get_led_state()
                self.features.one_touch_join.verify_get_led_state(response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_get_supported_language(self):
        try:
            response = self.features.earcon_feature.get_language()
            self.features.earcon_feature.verify_get_language(response, 0)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_set_not_supported_language(self):
        try:
            not_supported_languages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, random.randint(11, 255)]
            for n in not_supported_languages:
                response = self.features.earcon_feature.set_not_supported_language(n)
                self.features.earcon_feature.verify_set_not_supported_language(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_get_language_capability(self):
        try:
            response = self.features.earcon_feature.get_language_capability()
            self.features.earcon_feature.verify_get_language_capability(response)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_set_get_earcon_state(self):
        try:
            states = [0, 1]
            for state in states:
                self.features.earcon_feature.set_earcon_state(state)
                response = self.features.earcon_feature.get_earcon_state()
                self.features.earcon_feature.verify_get_earcon_state(response, state)
        except Exception as e:
            Report.logException(str(e))

    def test_925_VC_xyz_set_not_supported_earcon_state(self):
        try:
            response = self.features.earcon_feature.set_earcon_state(random.randint(2, 255))
            self.features.earcon_feature.verify_not_supported_earcon_value(response)
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(QbertAPIDongleTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
