import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIHostedRallyBarHuddle(UIBase):
    """
    Test to verify device APIs for Rally Bar Huddle in device mode.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "HostedTiny"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIHostedRallyBarHuddle, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHostedRallyBarHuddle, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHostedRallyBarHuddle, self).setUp()

    def tearDown(self):
        super(RaidenAPIHostedRallyBarHuddle, self).tearDown()

    def test_2501_VC_116707_get_rally_bar_huddle_in_device_mode(self):
        RaidenAPIHostedRallyBarHuddle.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_2502_VC_121288_change_rightsight_to_on_call_start_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Change_RS1_to_OnCallStart(self.role, self.room_name, self.device_name)

    def test_2503_VC_122687_change_rightsight_to_off_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_Turn_Off(self.role, self.room_name, self.device_name)

    def test_2504_VC_122688_change_rightsight_to_dynamic_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_to_Dynamic(self.role, self.room_name, self.device_name)

    def test_2505_VC_122689_disable_AI_noise_suppression_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_2506_VC_122690_enable_AI_noise_suppression_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_2507_VC_122691_enable_speaker_boost_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Enable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1408_VC_122692_disable_speaker_boost_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Disable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1409_VC_122693_enable_reverb_control_aggressive_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Aggressive(self.role, self.room_name, self.device_name)

    def test_1410_VC_122694_enable_reverb_control_normal_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_1411_VC_122695_turn_off_bluetooth_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1412_VC_122696_turn_on_bluetooth_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1413_VC_122697_microphone_EQ_voice_boost_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1414_VC_122698_microphone_EQ_normal_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1415_VC_122699_speaker_EQ_bass_boost_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1416_VC_122700_speaker_EQ_normal_rally_bar_huddle_in_device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarHuddle)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
