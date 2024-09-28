import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wired_api
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_wired import *


class ZoneWiredAPIDongleTests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(ZoneWiredAPIDongleTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=zone_wired_api.name,
                                          conn_type=ConnectionType.dongle)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "ZONE_WIRED"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    def test_701_VC_57572_get_protocol_version(self):
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_702_VC_57573_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_ZWIRED)
            self.features.root_feature.verify_get_features_responses(response, FEATURES_ZWIRED)
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
            self.features.feature_set_feature.verify_feature_count(response, len(FEATURES_ZWIRED))
        except Exception as e:
            Report.logException(str(e))

    def test_706_VC_57577_get_feature_id(self):
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(response, FEATURES_ZWIRED)
        except Exception as e:
            Report.logException(str(e))

    def test_707_VC_57587_get_serial_number(self):
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(response, zone_wired_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_708_VC_57588_get_firmware_version(self):
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(response, zone_wired_api.firmware_version)
        except Exception as e:
            Report.logException(str(e))

    def test_709_VC_57589_get_hardware_info(self):
        try:
            hw_revision = '00'

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(response, zone_wired_api.model_id, hw_revision)
        except Exception as e:
            Report.logException(str(e))

    def test_710_VC_57590_get_device_name(self):
        try:
            response = self.features.device_name_feature.get_device_name()
            self.features.device_name_feature.verify_name(response, zone_wired_api.name, 10)
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

    def test_723_VC_57606_get_sidetone_level(self):
        try:
            response = self.features.headset_audio_feature.get_sidetone_level()
        except Exception as e:
            Report.logException(str(e))

    def test_724_VC_57605_set_not_supported_value_of_sidetone_level(self):
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(random.randint(11, 255))
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(response)
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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ZoneWiredAPIDongleTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
