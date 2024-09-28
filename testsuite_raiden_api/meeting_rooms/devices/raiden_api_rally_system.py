import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIRallySystem(UIBase):
    """
    Test to verify device APIs for Rally System.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "Rally"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallySystem, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallySystem, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallySystem, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallySystem, self).tearDown()

    def test_1001_VC_53862_Get_Device_RallySystem(self):
        RaidenAPIRallySystem.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1002_VC_53865_Change_RightSight_to_OnCallStart_RallySystem(self):
        self.syncportal_methods.tc_Change_RS1_to_OnCallStart(self.role, self.room_name, self.device_name)

    def test_1003_VC_53864_Change_RightSight_Turn_Off_RallySystem(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_Turn_Off(self.role, self.room_name, self.device_name)

    def test_1004_VC_53866_Change_RightSight_to_Dynamic_RallySystem(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_to_Dynamic(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallySystem)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
