import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase

log = logging.getLogger(__name__)


class RaidenAPIITUserAccessControl(UIBase):
    """
    User API tests
    """
    syncportal_methods = SyncPortalTCMethods()
    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIITUserAccessControl, cls).setUpClass()
            cls.role = 'OrgAdmin'# Owner

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIITUserAccessControl, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIITUserAccessControl, self).setUp()

    def tearDown(self):
        super(RaidenAPIITUserAccessControl, self).tearDown()

    def test_301_VC_86205_IT_User_Access_Control_Restrict_Access_to_subgroups_by_Owner(self):
        self.syncportal_methods.tc_IT_User_Access_Control_Restrict_Access_to_subgroups_by_Owner(role=self.role)

    def test_302_VC_86210_IT_User_Access_Control_Restrict_access_to_subgroups_by_ThirdPartyUser(self):
        self.syncportal_methods.tc_IT_User_Access_Control_Restrict_access_to_subgroups_by_ThirdPartyUser()

    def test_303_VC_86212_IT_User_Access_Control_Rename_Room_Groups(self):
        self.syncportal_methods.tc_IT_User_Access_Control_Rename_Room_Groups(role=self.role)

    def test_304_VC_86214_IT_User_Access_Control_Delete_Room_Groups(self):
        self.syncportal_methods.tc_IT_User_Access_Control_Delete_Room_Groups(role=self.role)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIITUserAccessControl)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
