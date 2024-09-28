import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPIRallyBar(UIBase):
    """
    Test to verify device APIs for Rally Bar.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Kong"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallyBar, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallyBar, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallyBar, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallyBar, self).tearDown()

    def test_1501_Provision_Rally_Bar_to_Sync_Portal(self):
        """
        Provision Rally Bar to Sync Portal using LNA.
        """
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_1502_VC_53873_Get_Device_RallyBar(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1503_VC_53875_Change_RightSight_Group_view_set_to_OnCallStart_RallyBar(self):
        self.syncportal_methods.tc_change_rightSight_to_group_view_oncallstart(self.role, self.room_name,
                                                                               self.device_name)

    def test_1504_VC_53876_Change_RightSight_Turn_Off_RallyBar(self):
        self.syncportal_methods.tc_disable_rightsight(self.role, self.room_name, self.device_name)

    def test_1505_VC_60998_Change_RightSight2_Speaker_tracking_mode_Speaker_View_Picture_in_Picture_enabled_RallyBar(self):
        self.syncportal_methods.\
            tc_Change_RightSight2_Speaker_tracking_mode_Speaker_View_Picture_in_Picture_enabled(self.role,
                                                                                                self.room_name,
                                                                                                self.device_name)

    def test_1506_VC_60999_Change_RS2_Speaker_tracking_mode_Speaker_View_Picture_in_picture_disabled_RallyBar(self):
        self.syncportal_methods.\
            tc_Change_RS2_Speaker_tracking_mode_Speaker_View_Picture_in_picture_disabled(self.role,
                                                                                         self.room_name,
                                                                                         self.device_name)

    def test_1507_VC_53878_Change_RightSight_Group_view_set_to_Dynamic_RallyBar(self):
        self.syncportal_methods.tc_Change_RightSight_Group_view_set_to_Dynamic(self.role,
                                                                               self.room_name,
                                                                               self.device_name)

    def test_1508_VC_53879_Disable_AI_Noise_Suppression_RallyBar(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1509_VC_53880_Enable_AI_Noise_Suppression_RallyBar(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1510_VC_53881_Enable_Speaker_Boost_RallyBar(self):
        self.syncportal_methods.tc_Enable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1511_VC_53896_Disable_Speaker_Boost_RallyBar(self):
        self.syncportal_methods.tc_Disable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1512_VC_53882_Disable_Reverb_Control_RallyBar(self):
        self.syncportal_methods.tc_Disable_Reverb_Control(self.role, self.room_name, self.device_name)

    def test_1513_VC_53883_Enable_Reverb_Control_Aggressive_RallyBar(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Aggressive(self.role, self.room_name, self.device_name)

    def test_1514_VC_53885_Enable_Reverb_Control_Normal_RallyBar(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_1515_VC_53886_Turn_Off_Bluetooth_RallyBar(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1516_VC_53887_Turn_On_Bluetooth_RallyBar(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1517_VC_69046_Microphone_EQ_Bass_Boost_RallyBar(self):
        self.syncportal_methods.tc_Microphone_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1518_VC_69047_Microphone_EQ_Voice_Boost_RallyBar(self):
        self.syncportal_methods.tc_Microphone_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1519_VC_69048_Microphone_EQ_Normal_RallyBar(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1520_VC_69049_Speaker_EQ_Bass_Boost_RallyBar(self):
        self.syncportal_methods.tc_Speaker_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1521_VC_69050_Speaker_EQ_Voice_Boost_RallyBar(self):
        self.syncportal_methods.tc_Speaker_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1522_VC_69051_Speaker_EQ_Normal_RallyBar(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1523_VC_69052_Set_GroupView_Framing_Speed_To_Slower_RallyBar(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Slower(self.role, self.room_name, self.device_name)

    def test_1524_VC_69053_Set_GroupView_Framing_Speed_To_Default_RallyBar(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Default(self.role, self.room_name, self.device_name)

    def test_1525_VC_69055_Set_GroupView_Framing_Speed_To_Faster_RallyBar(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Faster(self.role, self.room_name, self.device_name)

    def test_1526_VC_69056_Switch_from_Group_View_Framing_Speed_Slower_To_Speaker_View_Framing_Speed_Default(self):
        self.syncportal_methods.tc_Switch_from_Group_View_Framing_Speed_Slower_To_Speaker_View_Framing_Speed_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1527_VC_69057_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Slower_RallyBar(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1528_VC_69058_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Faster_RallyBar(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Faster(
            self.role, self.room_name, self.device_name
        )

    def test_1529_VC_69059_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Slower_RallyBar(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1530_VC_69060_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Default_RallyBar(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1531_VC_69061_Set_SpeakerView_Framing_Speed_To_Faster_Speaker_Detection_To_Faster_RallyBar(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Faster_Speaker_Detection_To_Faster(
            self.role, self.room_name, self.device_name
        )

    def test_1532_VC_69062_Disable_Enable_RightSight_Verify_Group_View_Framing_Speed_Default(self):
        self.syncportal_methods.tc_Disable_Enable_RightSight_Verify_Group_View_Framing_Speed_Default(
            self.role, self.room_name, self.device_name
        )

    def test_1533_VC_69064_Disable_Local_Network_Access_RallyBar(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1534_VC_69063_Enable_Local_Network_Access_RallyBar(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Enable_Local_Network_Access(self.role, self.room_name, self.device_name, min_version)

    def test_1535_VC_69065_Change_Password_Local_Network_Access_RallyBar(self):
        min_version = float(914.223)
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name, min_version)

    def test_1536_VC_79944_RightSight_Preservation_Of_Settings_RS_Off_On_RallyBar(self):
        self.syncportal_methods.tc_RightSight_Preservation_Of_Settings_RS_Off_On(self.role, self.room_name,
                                                                                 self.device_name)

    def test_1537_VC_79945_RightSight_Preservation_Of_Settings_RS_Switch_between_Group_view_and_Speaker_view_RallyBar(self):
        self.syncportal_methods.tc_RightSight_Preservation_Of_Settings_RS_Switch_between_Group_view_and_Speaker_view(
            self.role,
            self.room_name,
            self.device_name)

    def test_1538_VC_58911_Change_BYOD_Screen_to_Swytch_tutorial_via_Sync_Portal_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Swytch_tutorial_via_Sync_Portal(self.role, self.room_name,
                                                                                         self.device_name)

    def test_1539_VC_58912_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_Sync_Portal_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_Sync_Portal(self.role,
                                                                                             self.room_name,
                                                                                             self.device_name)

    def test_1540_VC_58913_Change_BYOD_Screen_to_Custom_via_Sync_Portal_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Custom_via_Sync_Portal(self.role, self.room_name,
                                                                                self.device_name)

    def test_1541_VC_58914_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_Sync_Portal_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_Sync_Portal(self.role,
                                                                                             self.room_name,
                                                                                             self.device_name)

    def test_1542_VC_58915_Change_BYOD_Screen_to_Swytch_tutorial_via_device_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_Swytch_tutorial_via_device(self.role, self.room_name,
                                                                                    self.device_name)

    def test_1543_VC_58918_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_device_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_device(self.role, self.room_name,
                                                                                        self.device_name)

    def test_1544_VC_58919_Change_BYOD_Screen_to_custom_wallpaper_uploaded_using_sync_portal_via_device_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_custom_wallpaper_uploaded_using_sync_portal_via_device(
            self.role, self.room_name, self.device_name)

    def test_1545_VC_58920_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_device_RallyBar(self):
        self.syncportal_methods.tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_device(self.role, self.room_name,
                                                                                        self.device_name)

    def test_1546_VC_69044_Group_Settings(self):
        self.syncportal_methods.tc_Group_Settings(self.role, self.room_name, self.device_name)

    def test_1547_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBar)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
