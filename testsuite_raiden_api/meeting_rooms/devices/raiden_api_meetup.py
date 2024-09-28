import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIMeetup(UIBase):
    """
    Test to verify device APIs for Meetup.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "MeetUp"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIMeetup, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIMeetup, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIMeetup, self).setUp()

    def tearDown(self):
        super(RaidenAPIMeetup, self).tearDown()

    def test_801_VC_53852_Get_Device_Meetup(self):
        RaidenAPIMeetup.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_802_VC_53853_Change_RightSight_to_OnCallStart_MeetUp(self):
        self.syncportal_methods.tc_Change_RS1_to_OnCallStart(self.role, self.room_name, self.device_name)

    def test_803_VC_53855_Change_RightSight_Turn_Off_MeetUp(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_Turn_Off(self.role, self.room_name, self.device_name)

    def test_804_VC_53856_Change_RightSight_to_Dynamic_MeetUp(self):
        self.syncportal_methods.tc_RS1_Change_RightSight_to_Dynamic(self.role, self.room_name, self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetup)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")