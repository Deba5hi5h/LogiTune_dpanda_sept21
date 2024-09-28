import logging
import unittest
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime

log = logging.getLogger(__name__)

class RaidenAPIServiceAccountsBooker(UIBase):
    """
        Test to verify service account/booker APIs for Tap Scheduler.
        """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Nintendo"
    now = datetime.now()
    role = "OrgAdmin"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIServiceAccountsBooker, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIServiceAccountsBooker, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIServiceAccountsBooker, self).setUp()

    def tearDown(self):
        super(RaidenAPIServiceAccountsBooker, self).tearDown()

    def test_2001_VC_137906_Get_And_Import_Bookables_For_Organization_Bookers(self):
        '''
            Test: To get and import bookables for Organization bookers

            Steps:
            1. Get Org Bookers
            2. Import Bookables for a Booker
        '''
        booker_id = self.syncportal_methods.tc_get_organization_bookers(
                                              role=self.role,
                                              device_name=self.device_name)

        self.syncportal_methods.tc_import_bookables_for_bookers(
            role=self.role,
            device_name=self.device_name, booker_id=booker_id)


if __name__ == "__main__":
        unittest.main()

