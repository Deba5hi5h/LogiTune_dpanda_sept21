import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPIRallyBarFWUpdate(UIBase):
    """
    Test to verify Rally Bar Firmware update.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Kong"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRallyBarFWUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRallyBarFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRallyBarFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPIRallyBarFWUpdate, self).tearDown()

    def test_2101_VC_132007_provision_rally_bar_in_appliance_mode_to_sync_portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_2102_VC_132008_firmware_update_via_update_now_rally_bar_in_appliance_mode(self):
        # Pre-requisite: Let the device has update available.
        self.syncportal_methods.tc_firmware_update(room_name=self.room_name,
                                                   role=self.role,
                                                   device_name=self.device_name)

    def test_2103_VC_132009_delete_room_rally_bar_in_appliance_mode(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarFWUpdate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")