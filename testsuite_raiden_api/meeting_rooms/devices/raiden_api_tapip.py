import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPITapIP(UIBase):
    """
    Test to verify device APIs for Tap.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Atari"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPITapIP, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPITapIP, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPITapIP, self).setUp()

    def tearDown(self):
        super(RaidenAPITapIP, self).tearDown()

    def test_1801_Provision_TapIP_to_sync_portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_1802_VC_102445_Get_Device_TapIP(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1803_VC_79953_Reboot_Device_TapIP(self):
        self.syncportal_methods.tc_Reboot_Device(self.role, self.room_name, self.device_name)

    def test_1804_VC_79955_Disable_Local_Network_Access_TapIP(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1805_VC_79954_Enable_Local_Network_Access_TapIP(self):
        min_version = float(910.169)
        self.syncportal_methods.tc_Enable_Local_Network_Access(self.role, self.room_name,
                                                               self.device_name, min_version)

    def test_1806_VC_79956_Change_Password_Local_Network_Access_TapIP(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name, min_version)

    def test_1807_VC_79957_Move_Device_TapIP(self):
        self.syncportal_methods.tc_Move_Device(self.role, self.room_name, self.device_name)

    def test_1808_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapIP)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")