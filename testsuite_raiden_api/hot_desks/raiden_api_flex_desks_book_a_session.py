from datetime import datetime
import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIFlexDeskSessionBooking(UIBase):
    """
        Test case to book a session for a desk
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()
    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskSessionBooking, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskSessionBooking, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskSessionBooking, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskSessionBooking, self).tearDown()

    def test_1101_VC_119816_flex_desks_session_booking(self):
        """
              Test case to book a session for a desk

                            Steps:
                                1. Sign in to Sync Portal using valid owner credentials.
                                2. Create a User and get User ID and Email ID
                                3. Create Desk for above User ID
                                4. Book session for the created desk
                                5. Delete Desk and User

        """

        rolelist_raiden = ['OrgAdmin', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Add the end users to the organization.')
            user_id, email = self.syncportal_methods.tc_add_end_user(role=role_raiden)

            Report.logInfo('STEP 2: Book a session for a desk')
            desk_id, site, reservation_id = self.syncportal_hotdesks_methods.tc_flex_desk_session_booking(
                role=role_raiden, desk_name=self.desk_name, user_id=user_id, email_id=email)

            Report.logInfo('STEP 3: Delete site and end user')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, site)
            self.syncportal_methods.tc_delete_end_user(role=role_raiden, user_id=user_id)


    def test_1102_VC_120488_flex_desks_modify_view_delete_reserved_desk(self):
        """
              Test case modify, view and delete reserved desk

                            Steps:
                                1. Sign in to Sync Portal using valid owner credentials.
                                2. Create a User and get User ID and Email ID
                                3. Create Desk for above User ID
                                4. Book session for the created desk
                                5. Modify the reserved desk
                                6. View the reserved desk
                                7. Delete the reserved desk
                                8. Delete Desk and User

                            Tests:
                                1. Modify reserved desk
                                2. View desk reservation
                                3. Delete desk reservation
        """

        rolelist_raiden = ['OrgAdmin', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Add the end users to the organization.')
            user_id, email = self.syncportal_methods.tc_add_end_user(role=role_raiden)

            Report.logInfo('STEP 2: Book a session for a desk')
            desk_id, site, reservation_id = self.syncportal_hotdesks_methods.tc_flex_desk_session_booking(
                role=role_raiden, desk_name=self.desk_name, user_id=user_id, email_id=email)

            Report.logInfo('STEP 3: Modify a desk reservation')
            self.syncportal_hotdesks_methods.tc_flex_desk_modify_desk_reservation(
                role=role_raiden, desk_id=desk_id, reservation_id=reservation_id)

            Report.logInfo('STEP 4: View reserved desk')
            self.syncportal_hotdesks_methods.tc_flex_desk_view_reserved_desk(
                role=role_raiden, desk_id=desk_id, desk_name=self.desk_name)

            Report.logInfo('STEP 5: Delete reserved desk')
            self.syncportal_hotdesks_methods.tc_flex_desk_delete_reserved_desk(
                role=role_raiden, desk_id=desk_id, reservation_id=reservation_id)

            Report.logInfo('STEP 6: Delete site and end user')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, site)
            self.syncportal_methods.tc_delete_end_user(role=role_raiden, user_id=user_id)



if __name__ == "__main__":
    unittest.main()
