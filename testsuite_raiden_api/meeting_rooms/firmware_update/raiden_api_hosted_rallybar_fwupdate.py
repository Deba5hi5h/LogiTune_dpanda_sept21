import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIHostedRallyBarFWUpdate(UIBase):
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
            super(RaidenAPIHostedRallyBarFWUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHostedRallyBarFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHostedRallyBarFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPIHostedRallyBarFWUpdate, self).tearDown()

    def test_2001_VC_112839_FW_Update_RallyBar_in_Device_mode(self):
        # Pre-requisite: Let the device has update available.
        RaidenAPIHostedRallyBarFWUpdate.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_firmware_update(room_name=self.room_name,
                                                   role=self.role,
                                                   device_name=self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarFWUpdate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
