import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIRallyCamera(UIBase):
    """
    Test to verify device APIs for Rally Camera
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "RallyCamera"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallyCamera, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallyCamera, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallyCamera, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallyCamera, self).tearDown()

    def test_901_VC_53858_Get_Device_Rally_Camera(self):
        RaidenAPIRallyCamera.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_902_VC_53859_Change_RightSight_to_OnCallStart_Rally_Camera(self):
        self.syncportal_methods.tc_Change_RS1_to_OnCallStart(self.role, self.room_name, self.device_name)

    def test_903_VC_53860_Change_RightSight_Turn_Off_Rally_Camera(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_Turn_Off(self.role, self.room_name, self.device_name)

    def test_904_VC_53861_Change_RightSight_to_Dynamic_Rally_Camera(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_to_Dynamic(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyCamera)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
