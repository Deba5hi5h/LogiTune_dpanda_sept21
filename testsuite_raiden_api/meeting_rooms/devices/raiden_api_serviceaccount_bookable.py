import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIServiceAccountBookable(UIBase):
    """
        Test to verify service account bookable APIs for Tap Scheduler.
        """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Nintendo"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}
    role = "OrgAdmin"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIServiceAccountBookable, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIServiceAccountBookable, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIServiceAccountBookable, self).setUp()

    def tearDown(self):
        super(RaidenAPIServiceAccountBookable, self).tearDown()

    def test_2201_VC_140615_Link_Unlink_Room_To_Bookable(self):
        '''
             Test: To Link and Unlink room to bookables
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Add new room
                2) Link above created room to bookable
                3) Unlink room to bookable
                4) Delete the room
        '''

        bookable_id = "m365_logi_qa_room_7@logivcqa1.onmicrosoft.com"

        Report.logInfo('STEP 1: Create empty room')
        self.room_id = self.syncportal_methods.tc_create_empty_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room from bookables.')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, self.room_id, bookable_id)

        Report.logInfo(
            'STEP 3: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 4: Delete the room.')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


    def test_2202_VC_140615_Create_Rooms_From_Bookables(self):
        '''
            Test: To create rooms from bookables
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create rooms from bookables
                2) Unlink room to bookable
        '''

        bookable_id = "m365_logi_qa_room_21@logivcqa1.onmicrosoft.com"
        Report.logInfo(
            'STEP 1: Create rooms from bookables.')
        self.syncportal_methods.tc_create_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 2: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)


    def test_2203_VC_140615_Delete_Bookables(self):
        '''
             Test: To delete bookables and later import them back for next automation run
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Delete bookables
                2) Import bookables
        '''

        bookable_id = "m365_logi_qa_room_22@logivcqa1.onmicrosoft.com"
        admin_email_id = "admin@logivcqa1.onmicrosoft.com"

        Report.logInfo(
            'STEP 1: Delete rooms bookables.')
        self.syncportal_methods.tc_delete_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 2: Import bookables.')
        self.syncportal_methods.tc_import_bookables(self.role, admin_email_id)

if __name__ == "__main__":
        unittest.main()

