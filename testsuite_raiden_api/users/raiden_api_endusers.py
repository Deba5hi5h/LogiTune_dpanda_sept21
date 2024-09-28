import logging
import unittest
import sys

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIEndUsers(UIBase):
    """
     Test to verify add API End Users.
     """
    syncportal_methods = SyncPortalTCMethods()
    users_email = ""
    users_userid = ""

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIEndUsers, cls).setUpClass()

        except Exception as e:
            log.error("Unable to raise the test-suite")
            raise e

    @classmethod
    def tearDownClass(cls) -> None:
        super(RaideAPIEndUsers, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIEndUsers, self).setUp()

    def tearDown(self):
        super(RaideAPIEndUsers, self).tearDown()


    def test_601_VC_113976_Add_View_Delete_EndUsers(self):
        """Add/ View/ Update and Delete end users: Owner, Third Party.
                            Setup:
                                  1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                 1. Add the users: Owner, Third Party to the organization
                                 2. View the users.
                                 3. Delete the users.

                        """
        Report.logInfo(
            'STEP 1: Add the end users to the organization.')

        rolelist_raiden = ['ThirdParty', 'OrgAdmin']

        for role_raiden in rolelist_raiden:
            user, email = self.syncportal_methods.tc_add_end_user(role=role_raiden)

            self.users_user_id = user
            self.users_email = email

            Report.logInfo('STEP 2: View the created end users')

            self.syncportal_methods.tc_view_end_user(role=role_raiden,
                                                    user_id=self.users_user_id,
                                                    email_id=self.users_email)

            Report.logInfo('STEP 3: Delete the created end users')
            self.syncportal_methods.tc_delete_end_user(role_raiden, self.users_user_id)


if __name__ == "__main__":
    unittest.main()
