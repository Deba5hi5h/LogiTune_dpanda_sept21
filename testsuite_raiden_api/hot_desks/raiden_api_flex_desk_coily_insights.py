import logging
import unittest
import sys
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPICoilyInsights(UIBase):
    """
         Test to verify flex desk coily insights functionality
    """

    syncportal_methods = SyncPortalTCMethods()
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()

    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPICoilyInsights, cls).setUpClass()

        except Exception as e:
            log.error("Unable to raise the test-suite")
            raise e

    @classmethod
    def tearDownClass(cls) -> None:
        super(RaideAPICoilyInsights, cls).tearDownClass()

    def setUp(self):
        super(RaideAPICoilyInsights, self).setUp()

    def tearDown(self):
        super(RaideAPICoilyInsights, self).tearDown()

    def test_1901_VC_128781_Coily_Insights(self):
        """Get insight data associated with end user, site and desk
                            Setup:
                                  1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                 1. Add an end user: OrgAdmin to the organization
                                 2. Add a site, building, floor, area and a desk
                                 3. Book a session by IT admin for the added end user and desk
                                 4. Get Insights data associated with end user
                                 5. Get Insights data associated with site
                                 6. Get Insights data associated with desk
                                 7. Delete the users, site and desk

                        """

        rolelist_raiden = ['OrgAdmin']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Add the end users to the organization.')
            user, email = self.syncportal_methods.tc_add_end_user(role=role_raiden)

            self.user_id = user
            self.user_email = email

            Report.logInfo('STEP 2: Book a session for a desk')
            desk_id, site, reservation_id = self.syncportal_hotdesks_methods.tc_flex_desk_session_booking(
                role=role_raiden, desk_name=self.desk_name, user_id=self.user_id, email_id=self.user_email)

            Report.logInfo('STEP 3: Get Coily Insight Information')
            self.syncportal_hotdesks_methods.tc_get_coily_insight_information(
                role=role_raiden, desk_name=self.desk_name, user_id=self.user_id, desk_id=desk_id, site=site)

            Report.logInfo('STEP 4: Delete site and end user')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, site)
            self.syncportal_methods.tc_delete_end_user(role=role_raiden, user_id=self.user_id)



if __name__ == "__main__":
    unittest.main()
