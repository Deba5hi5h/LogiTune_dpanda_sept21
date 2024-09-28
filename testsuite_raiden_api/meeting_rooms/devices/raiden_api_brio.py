import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase

log = logging.getLogger(__name__)


class RaidenAPIBrio(UIBase):
    """
    Test to verify device APIs for Brio.
    """
    syncportal_methods = SyncPortalTCMethods()
    sync_app = SyncAppMethods()
    device_name = "Brio"
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIBrio, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIBrio, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIBrio, self).setUp()

    def tearDown(self):
        super(RaidenAPIBrio, self).tearDown()

    def test_701_VC_53847_Get_Device_Brio(self):
        RaidenAPIBrio.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIBrio)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
