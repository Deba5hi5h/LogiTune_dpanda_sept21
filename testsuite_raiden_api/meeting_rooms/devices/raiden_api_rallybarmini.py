import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPIRallyBarMini(UIBase):
    """
    Test to verify device APIs for Rally Bar Mini.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Diddy"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallyBarMini, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallyBarMini, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallyBarMini, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallyBarMini, self).tearDown()

    def test_1601_Provision_RallyBarMini_to_Sync_Portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_1602_VC_53889_Get_Device_RallyBarMini(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1603_VC_53890_Change_RightSight_Group_view_set_to_OnCallStart_RallyBarMini(self):
        self.syncportal_methods.tc_change_rightSight_to_group_view_oncallstart(self.role, self.room_name,
                                                                               self.device_name)

    def test_1604_VC_53891_Change_RightSight_Turn_Off_RallyBarMini(self):
        self.syncportal_methods.tc_disable_rightsight(self.role, self.room_name, self.device_name)

    def test_1605_VC_61000_Change_RightSight2_Speaker_tracking_mode_Speaker_View_Picture_in_Picture_enabled_RallyBarMini(self):
        self.syncportal_methods.\
            tc_Change_RightSight2_Speaker_tracking_mode_Speaker_View_Picture_in_Picture_enabled(self.role,
                                                                                                self.room_name,
                                                                                                self.device_name)

    def test_1606_VC_61001_Change_RS2_Speaker_tracking_mode_Speaker_View_Picture_in_picture_disabled_RallyBarMini(self):
        self.syncportal_methods.\
            tc_Change_RS2_Speaker_tracking_mode_Speaker_View_Picture_in_picture_disabled(self.role,
                                                                                         self.room_name,
                                                                                         self.device_name)

    def test_1607_VC_53892_Change_RightSight_Group_view_set_to_Dynamic_RallyBarMini(self):
        self.syncportal_methods.tc_Change_RightSight_Group_view_set_to_Dynamic(self.role, self.room_name,
                                                                               self.device_name)

    def test_1608_VC_53893_Disable_AI_Noise_Suppression_RallyBarMini(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1609_VC_53894_Enable_AI_Noise_Suppression_RallyBarMini(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1610_VC_53895_Enable_Speaker_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Enable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1611_VC_53898_Disable_Speaker_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Disable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1612_VC_53900_Disable_Reverb_Control_RallyBarMini(self):
        self.syncportal_methods.tc_Disable_Reverb_Control(self.role, self.room_name, self.device_name)

    def test_1613_VC_53901_Enable_Reverb_Control_Aggressive_RallyBarMini(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Aggressive(self.role, self.room_name, self.device_name)

    def test_1614_VC_53902_Enable_Reverb_Control_Normal_RallyBarMini(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_1615_VC_53903_Turn_Off_Bluetooth_RallyBarMini(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1616_VC_53904_Turn_On_Bluetooth_RallyBarMini(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1617_VC_69066_Microphone_EQ_Bass_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Microphone_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1618_VC_69067_Microphone_EQ_Voice_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Microphone_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1619_VC_69068_Microphone_EQ_Normal_RallyBarMini(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1620_VC_69069_Speaker_EQ_Bass_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Speaker_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1621_VC_69070_Speaker_EQ_Voice_Boost_RallyBarMini(self):
        self.syncportal_methods.tc_Speaker_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1622_VC_69071_Speaker_EQ_Normal_RallyBarMini(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1623_VC_69072_Set_GroupView_Framing_Speed_To_Slower_RallyBarMini(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Slower(self.role, self.room_name, self.device_name)

    def test_1624_VC_69073_Set_GroupView_Framing_Speed_To_Default_RallyBarMini(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Default(self.role, self.room_name, self.device_name)

    def test_1625_VC_69074_Set_GroupView_Framing_Speed_To_Faster_RallyBarMini(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Faster(self.role, self.room_name, self.device_name)

    def test_1626_VC_69075_Switch_from_Group_View_Framing_Speed_Slower_To_Speaker_View_Framing_Speed_Default_RallyBarMini(self):
        self.syncportal_methods.tc_Switch_from_Group_View_Framing_Speed_Slower_To_Speaker_View_Framing_Speed_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1627_VC_69077_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Slower_RallyBarMini(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1628_VC_69079_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Faster_RallyBarMini(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Faster(
            self.role, self.room_name, self.device_name
        )

    def test_1629_VC_69080_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower_RallyBarMini(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1630_VC_69082_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Default_RallyBarMini(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1631_VC_69083_Set_SpeakerView_Framing_Speed_To_Faster_Speaker_Detection_To_Faster_RallyBarMini(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Faster_Speaker_Detection_To_Faster(
            self.role, self.room_name, self.device_name
        )

    def test_1632_VC_69084_Disable_Enable_RightSight_Verify_Group_View_Framing_Speed_Default_RallyBarMini(self):
        self.syncportal_methods.tc_Disable_Enable_RightSight_Verify_Group_View_Framing_Speed_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1633_VC_69086_Disable_Local_Network_Access_RallyBarMini(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1634_VC_69085_Enable_Local_Network_Access_RallyBarMini(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Enable_Local_Network_Access(self.role, self.room_name, self.device_name, min_version)

    def test_1635_VC_69087_Change_Password_Local_Network_Access_RallyBarMini(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name, min_version)

    def test_1636_VC_79946_RightSight_Preservation_Of_Settings_RS_Off_On_RallyBarMini(self):
        self.syncportal_methods.tc_RightSight_Preservation_Of_Settings_RS_Off_On(self.role, self.room_name,
                                                                                 self.device_name)

    def test_1637_VC_79947_RightSight_Preservation_Of_Settings_RS_Switch_between_Group_view_and_Speaker_view_RallyBarMini(self):
        self.syncportal_methods.tc_RightSight_Preservation_Of_Settings_RS_Switch_between_Group_view_and_Speaker_view(
                                                                                                  self.role,
                                                                                                  self.room_name,
                                                                                                  self.device_name)

    def test_1638_VC_58921_Change_BYOD_Screen_to_Swytch_tutorial_via_Sync_Portal_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Swytch_tutorial_via_Sync_Portal(self.role, self.room_name,
                                                                                         self.device_name)

    def test_1639_VC_58922_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_Sync_Portal_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_Sync_Portal(self.role,
                                                                                             self.room_name,
                                                                                             self.device_name)

    def test_1640_VC_58923_Change_BYOD_Screen_to_Custom_via_Sync_Portal_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Custom_via_Sync_Portal(self.role, self.room_name,
                                                                                 self.device_name)

    def test_1641_VC_58924_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_Sync_Portal_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_Sync_Portal(self.role,
                                                                                             self.room_name,
                                                                                             self.device_name)

    def test_1642_VC_58926_Change_Change_BYOD_Screen_to_Swytch_tutorial_via_device_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Swytch_tutorial_via_device(self.role, self.room_name,
                                                                                    self.device_name)

    def test_1643_VC_58928_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_device_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_device(self.role, self.room_name,
                                                                                        self.device_name)

    def test_1644_VC_58929_Change_BYOD_Screen_to_custom_wallpaper_uploaded_using_sync_portal_via_device_RallyBarMini(
            self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_custom_wallpaper_uploaded_using_sync_portal_via_device(
            self.role, self.room_name, self.device_name)

    def test_1645_VC_58930_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_device_RallyBarMini(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_device(self.role, self.room_name,
                                                                                        self.device_name)

    def test_1646_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarMini)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
