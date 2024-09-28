import time
import unittest
import random

from base import global_variables
from base.base_ui import UIBase
from testsuite_firmware_api_tests.api_tests.api_parameters import bomberman_mono_api
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_bomberman_mono import *


class BombermanMonoAPITests(UIBase):
    """
    COMMANDS COVERAGE: https://docs.google.com/spreadsheets/d/1ZGQUiclAQvlVjZeGs0mYRDiXt0ZMcrrWk1roVidefFU/edit#gid=1486963386
    errors: https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Protocol/Error_codes.md
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(BombermanMonoAPITests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=bomberman_mono_api.name,
                                          conn_type=ConnectionType.dongle)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "BOMBERMAN_MONO"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    def test_2301_VC_138717_get_protocol_version(self):
        try:
            response = self.features.root_feature.get_protocol_version()
            self.features.root_feature.verify_protocol_version(response)
        except Exception as e:
            Report.logException(str(e))

    def test_2302_VC_138716_get_features(self):
        try:
            response = self.features.root_feature.get_features(FEATURES_BOMBERMAN_MONO)
            self.features.root_feature.verify_get_features_responses(response, FEATURES_BOMBERMAN_MONO)
        except Exception as e:
            Report.logException(str(e))

    def test_2303_VC_138715_get_not_supported_feature(self):
        try:
            for feature in [[1, 12], [1, 13]]:
                response = self.features.root_feature.get_not_supported_feature([feature[0], feature[1]])
                self.features.root_feature.verify_not_supported_feature(response)
        except Exception as e:
            Report.logException(str(e))

    def test_2304_VC_138714_get_not_existing_feature(self):
        try:
            response = self.features.root_feature.get_not_existing_feature()
            self.features.root_feature.verify_not_existing_feature(response)
        except Exception as e:
            Report.logException(str(e))

    def test_2305_VC_138713_get_feature_count(self):
        try:
            response = self.features.feature_set_feature.get_feature_count()
            self.features.feature_set_feature.verify_feature_count(response, len(FEATURES_BOMBERMAN_MONO))
        except Exception as e:
            Report.logException(str(e))

    def test_2306_VC_138712_get_feature_id(self):
        try:
            response = self.features.feature_set_feature.get_feature_id()
            self.features.feature_set_feature.verify_get_feature_id(response, FEATURES_BOMBERMAN_MONO)
        except Exception as e:
            Report.logException(str(e))

    def test_2307_VC_138711_get_serial_number(self):
        try:
            response = self.features.device_info_feature.get_serial_number()
            self.features.device_info_feature.verify_serial_number(response, bomberman_mono_api.serial_number)
        except Exception as e:
            Report.logException(str(e))

    def test_2308_VC_138710_get_firmware_version(self):
        try:
            response = self.features.device_info_feature.get_firmware_version()
            self.features.device_info_feature.verify_firmware_version(response, bomberman_mono_api.firmware_version)
        except Exception as e:
            Report.logException(str(e))

    def test_2309_VC_138709_get_hardware_info(self):
        try:
            hw_revision = '00'

            response = self.features.device_info_feature.get_hardware_info()
            self.features.device_info_feature.verify_hardware_info(response, bomberman_mono_api.model_id, hw_revision)
        except Exception as e:
            Report.logException(str(e))

    def test_2310_VC_138709_set_get_mic_mute_state(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_audio_feature.set_mic_mute(status)
                response = self.features.headset_audio_feature.get_mic_mute_status()
                self.features.headset_audio_feature.verify_get_mic_mute_status(response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_2311_VC_138707_get_sidetone_level(self):
        try:
            response = self.features.headset_audio_feature.get_sidetone_level()
        except Exception as e:
            Report.logException(str(e))

    def test_2312_VC_138718_set_not_supported_value_of_sidetone_level(self):
        try:
            response = self.features.headset_audio_feature.set_sidetone_level(random.randint(11, 255))
            self.features.headset_audio_feature.verify_error_on_set_sidetone_level(response)
        except Exception as e:
            Report.logException(str(e))

    def test_2313_VC_138706_set_get_voice_notification_status(self):
        try:
            statuses = [0, 1]
            for status in statuses:
                self.features.headset_misc_feature.set_voice_notification_status(status)
                response = self.features.headset_misc_feature.get_voice_notification_status()
                self.features.headset_misc_feature.verify_get_voice_notification_status(response, status)
                time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def test_2314_VC_138704_factory_reset_device(self):
        try:
            self.features.headset_misc_feature.factory_reset_device()
        except Exception as e:
            Report.logException(str(e))

    def test_2315_VC_138703_set_get_anti_startle_state(self) -> None:
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

    def test_2316_VC_138702_set_not_supported_anti_startle_state(self) -> None:
        try:
            response = self.features.anti_startle.set_anti_startle(
                random.randint(2, 255)
            )
            self.features.anti_startle.verify_not_supported_anti_startle_value(
                response
            )
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BombermanMonoAPITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
