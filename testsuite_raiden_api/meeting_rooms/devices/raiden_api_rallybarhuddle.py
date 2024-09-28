import logging
import unittest
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIRallyBarHuddle(UIBase):
    """
    Test to verify device APIs for Rally Bar Huddle in appliance mode.
    """

    syncportal_methods = SyncPortalTCMethods()
    device_name = "Tiny"
    now = datetime.now()
    time_to_string = now.strftime("%Y%m%d%H%M%S")
    room_name = f"{time_to_string} Auto-EmptyRoom"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallyBarHuddle, cls).setUpClass()
            cls.role = "OrgAdmin"

        except Exception as e:
            Report.logException("Unable to setup the test suite")
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallyBarHuddle, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallyBarHuddle, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallyBarHuddle, self).tearDown()

    def test_2001_VC_116691_provision_rally_bar_huddle_in_appliance_mode_to_sync_portal(self):
        self.syncportal_methods.tc_provision_device_in_appliance_mode_to_sync_portal(
            self.role, self.device_name, self.room_name, global_variables.SYNC_ENV
        )

    def test_2002_VC_116698_get_device_information_rally_bar_huddle_in_appliance_mode(self):
        self.syncportal_methods.tc_get_device(
            room_name=self.room_name, role=self.role, device_name=self.device_name
        )

    def test_2003_VC_116699_change_rightsight_to_on_call_start_rally_bar_huddle(self):
        self.syncportal_methods.tc_Change_RS1_to_OnCallStart(self.role, self.room_name, self.device_name)

    def test_2004_VC_116700_change_rightsight_to_off_rally_bar_huddle(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_Turn_Off(self.role, self.room_name, self.device_name)

    def test_2005_VC_16701_change_rightsight_to_dynamic_rally_bar_huddle(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_to_Dynamic(self.role, self.room_name, self.device_name)

    def test_2006_VC_116721_disable_AI_noise_suppression_rally_bar_huddle(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_2007_VC_116722_enable_AI_noise_suppression_rally_bar_huddle(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_2008_VC_116724_disable_reverb_control_rally_bar_huddle(self):
        self.syncportal_methods.tc_Disable_Reverb_Control(self.role, self.room_name, self.device_name)

    def test_2009_VC_116725_enable_reverb_control_aggressive_rally_bar_huddle(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Aggressive(self.role, self.room_name, self.device_name)

    def test_2010_VC_116726_enable_reverb_control_normal_rally_bar_huddle(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_2011_VC_116746_turn_off_bluetooth_rally_bar_huddle(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_2012_VC_116747_turn_on_bluetooth_rally_bar_huddle(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_2013_VC_116748_microphone_EQ_bass_boost_rally_bar_huddle(self):
        self.syncportal_methods.tc_Microphone_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_2014_VC_116749_microphone_EQ_voice_boost_rally_bar_huddle(self):
        self.syncportal_methods.tc_Microphone_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_2015_VC_116750_microphone_EQ_normal_rally_bar_huddle(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_2016_VC_116751_speaker_EQ_bass_boost_rally_bar_huddle(self):
        self.syncportal_methods.tc_Speaker_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_2017_VC_116752_speaker_EQ_voice_boost_rally_bar_huddle(self):
        self.syncportal_methods.tc_Speaker_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_2018_VC_116753_speaker_EQ_normal_rally_bar_huddle(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_2019_VC_116742_disable_local_network_access_rally_bar_huddle(self):
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name)

    def test_2020_VC_116743_enable_local_network_access_rally_bar_huddle(self):
        self.syncportal_methods.tc_Enable_Local_Network_Access(self.role, self.room_name, self.device_name)

    def test_2021_VC_116744_change_password_local_network_access_rally_bar_huddle(self):
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name)

    def test_2022_VC_116745_delete_room_rally_bar_huddle_in_appliance_mode(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    unittest.main()
