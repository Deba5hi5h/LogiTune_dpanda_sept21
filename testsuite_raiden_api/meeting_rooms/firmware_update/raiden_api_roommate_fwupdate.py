import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPIRoomMateFWUpdate(UIBase):
    """
    Test to verify device APIs for RoomMate.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Sega"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRoomMateFWUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRoomMateFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRoomMateFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPIRoomMateFWUpdate, self).tearDown()

    def test_2401_VC_129529_Provision_RoomMate_to_Sync_Portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_2402_VC_129533_FW_Update_RoomMate(self):
        # Pre-requisite: Let the device has update available.
        self.syncportal_methods.tc_firmware_update(room_name=self.room_name,
                                                   role=self.role,
                                                   device_name=self.device_name)

    def test_2403_VC_12815_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomMateFWUpdate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
