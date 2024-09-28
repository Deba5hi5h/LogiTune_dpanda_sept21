import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime

log = logging.getLogger(__name__)


class RaidenAPIProvisioning(UIBase):
    """
    Test to verify add, update and delete of empty rooms.
    """
    syncportal_methods = SyncPortalTCMethods()
    room_names = list()
    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIProvisioning, cls).setUpClass()
            cls.role = 'OrgAdmin'
            now = datetime.now()
            cls.room_name_1 = now.strftime("%Y%m%d%H%M%S") + " Auto-Room1"
            cls.room_name_2 = now.strftime("%Y%m%d%H%M%S") + " Auto-Room2"

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIProvisioning, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIProvisioning, self).setUp()

    def tearDown(self):
        super(RaidenAPIProvisioning, self).tearDown()

    def test_401_VC_11108_PC_Provisioning(self):
        room_name = self.syncportal_methods.tc_Provision_New_Room(self.role, self.room_name_1)
        RaidenAPIProvisioning.room_names.append(room_name)

    def test_402_VC_102447_Appliance_Provisioning(self):
        room_name = self.syncportal_methods.tc_Appliance_Provisioning(self.role, self.room_name_2)
        RaidenAPIProvisioning.room_names.append(room_name)

    def test_403_VC_12860_Delete_rooms(self):
        for room_name in self.room_names:
            self.syncportal_methods.tc_delete_room(self.role, room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")