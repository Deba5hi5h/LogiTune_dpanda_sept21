import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPITapSchedulerFWUpdate(UIBase):
    """
    Test to verify device APIs for Tap Scheduler.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Nintendo"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPITapSchedulerFWUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPITapSchedulerFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPITapSchedulerFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPITapSchedulerFWUpdate, self).tearDown()

    def test_2701_VC_129531_Provision_Tap_Scheduler_to_Sync_Portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_2702_VC_129535_FW_Update_Tap_Scheduler(self):
        # Pre-requisite: Let the device has update available.
        self.syncportal_methods.tc_firmware_update(room_name=self.room_name,
                                                   role=self.role,
                                                   device_name=self.device_name)

    def test_2703_VC_12815_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapSchedulerFWUpdate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
