import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods

log = logging.getLogger(__name__)


class RaidenAPIHostedRallyBarHuddleFWUpdate(UIBase):
    """
    Test to verify device APIs for Rally Bar Huddle in device mode.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "HostedTiny"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIHostedRallyBarHuddleFWUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHostedRallyBarHuddleFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHostedRallyBarHuddleFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPIHostedRallyBarHuddleFWUpdate, self).tearDown()

    def test_2201_VC_115008_firmware_update_rally_bar_huddle_in_device_mode(self):
        # Pre-requisite: Let the device has update available.
        RaidenAPIHostedRallyBarHuddleFWUpdate.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_firmware_update(room_name=self.room_name,
                                                   role=self.role,
                                                   device_name=self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarHuddleFWUpdate)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")

