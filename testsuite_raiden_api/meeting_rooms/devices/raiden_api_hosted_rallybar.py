import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIHostedRallyBar(UIBase):
    """
    Test to verify device APIs for Rally Bar in device mode.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "HostedKong"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIHostedRallyBar, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHostedRallyBar, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHostedRallyBar, self).setUp()

    def tearDown(self):
        super(RaidenAPIHostedRallyBar, self).tearDown()

    def test_1301_VC_102254_Get_Device_RallyBar_in_Device_mode(self):
        RaidenAPIHostedRallyBar.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1302_VC_102255_Change_RightSight2_Turn_Off_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_disable_rightsight(self.role, self.room_name, self.device_name)

    def test_1303_VC_102257_Set_RS2_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Slower_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower(
            self.role, self.room_name, self.device_name
        )

    def test_1304_VC_102258_Set_RS2_GroupView_Framing_Speed_To_Default_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Set_GroupView_Framing_Speed_To_Default(self.role, self.room_name, self.device_name)

    def test_1305_VC_102259_Disable_AI_Noise_Suppression_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Disable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1306_VC_102261_Enable_AI_Noise_Suppression_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_AI_Noise_Suppression(self.role, self.room_name, self.device_name)

    def test_1307_VC_102269_Enable_Speaker_Boost_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1308_VC_102274_Disable_Speaker_Boost_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Disable_Speaker_Boost(self.role, self.room_name, self.device_name)

    def test_1309_VC_102451_Disable_Reverb_Control_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Disable_Reverb_Control(self.role, self.room_name, self.device_name)

    def test_1310_VC_102452_Enable_Reverb_Control_Normal_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Enable_Reverb_Control_Normal(self.role, self.room_name, self.device_name)

    def test_1311_VC_102454_Turn_Off_Bluetooth_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Turn_Off_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1312_VC_102455_Turn_On_Bluetooth_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Turn_On_Bluetooth(self.role, self.room_name, self.device_name)

    def test_1313_VC_102456_Microphone_EQ_Bass_Boost_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Bass_Boost(self.role, self.room_name, self.device_name)

    def test_1314_VC_102457_Microphone_EQ_Normal_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Microphone_EQ_Normal(self.role, self.room_name, self.device_name)

    def test_1315_VC_102458_Speaker_EQ_Voice_Boost_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Voice_Boost(self.role, self.room_name, self.device_name)

    def test_1316_VC_102459_Speaker_EQ_Normal_RallyBar_in_Device_mode(self):
        self.syncportal_methods.tc_Speaker_EQ_Normal(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBar)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
