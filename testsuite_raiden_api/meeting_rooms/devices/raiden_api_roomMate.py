import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPIRoomMate(UIBase):
    """
    Test to verify device APIs for Tap.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Sega"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRoomMate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRoomMate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRoomMate, self).setUp()

    def tearDown(self):
        super(RaidenAPIRoomMate, self).tearDown()

    def test_1701_Provision_RoomMate_to_sync_portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_1702_VC_102444_Get_Device_RoomMate(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1703_VC_79948_Reboot_Device_RoomMate(self):
        self.syncportal_methods.tc_Reboot_Device(self.role, self.room_name, self.device_name)

    def test_1704_VC_79951_Disable_Local_Network_Access_RoomMate(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1705_VC_79950_Enable_Local_Network_Access_RoomMate(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Enable_Local_Network_Access(self.role, self.room_name,
                                                               self.device_name, min_version)

    def test_1706_VC_79952_Change_Password_Local_Network_Access_RoomMate(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name, min_version)

    def test_1707_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomMate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")