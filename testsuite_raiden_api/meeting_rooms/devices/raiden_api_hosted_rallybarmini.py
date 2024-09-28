import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIHostedRallyBarMini(UIBase):
    """
    Test to verify device APIs for Rally Bar.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "HostedDiddy"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIHostedRallyBarMini, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHostedRallyBarMini, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHostedRallyBarMini, self).setUp()

    def tearDown(self):
        super(RaidenAPIHostedRallyBarMini, self).tearDown()

    def test_1401_VC_102262_Get_Device_RallyBarMini_in_Device_mode(self):
        RaidenAPIHostedRallyBarMini.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1402_VC_102263_Change_RightSight2_Turn_Off_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_disable_rightsight(self.role, self.room_name, self.device_name)

    def test_1403_VC_102264_Set_RS2_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Slower_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1404_VC_102266_Set_RS2_GroupView_Framing_Speed_To_Default_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Default(self.role, self.room_name, self.device_name)

    def test_1405_VC_102267_Disable_AI_Noise_Suppression_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1406_VC_102268_Enable_AI_Noise_Suppression_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1407_VC_102270_Enable_Speaker_Boost_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1408_VC_102274_Disable_Speaker_Boost_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Disable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1409_VC_102460_Enable_Reverb_Control_Aggressive_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Aggressive(self.role, self.room_name, self.device_name)

    def test_1410_VC_102461_Enable_Reverb_Control_Normal_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_1411_VC_102462_Turn_Off_Bluetooth_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1412_VC_102463_Turn_On_Bluetooth_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1413_VC_102464_Microphone_EQ_Voice_Boost_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1414_VC_102465_Microphone_EQ_Normal_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1415_VC_102466_Speaker_EQ_Bass_Boost_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1416_VC_102467_Speaker_EQ_Normal_RallyBarMini_in_Device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarMini)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
