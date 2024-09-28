import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase
from extentreport.report import Report
from datetime import datetime

log = logging.getLogger(__name__)


class RaidenAPIOwner(UIBase):
    syncportal_methods = SyncPortalTCMethods()
    prov_list = dict()
    created_org_id = None
    room_name = ''

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIOwner, cls).setUpClass()
            cls.role = 'OrgAdmin'
            now = datetime.now()
            cls.room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Room1"

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIOwner, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIOwner, self).setUp()

    def tearDown(self):
        super(RaidenAPIOwner, self).tearDown()
        self.token = self.org_id = None

    def test_051_Owner_creates_new_Admin(self):
        try:
            user_role = 'OrgMember'
            user_id, email = self.syncportal_methods.tc_add_user(role=self.role, user=user_role)
            self.syncportal_methods.tc_delete_user(self.role, user_role, user_id)

        except Exception as e:
            Report.logException(f'{e}')

    def test_052_Owner_List_of_all_Org_Users(self):
        self.syncportal_methods.tc_Owner_List_of_all_Org_Users(role=self.role)

    def test_053_Owner_Provision_New_Room(self):
        self.syncportal_methods.tc_Provision_New_Room(self.role, self.room_name)

    def test_054_Owner_List_of_All_OrgRooms(self):
        self.syncportal_methods.tc_List_of_All_Org_Rooms(self.role)

    def test_055_Owner_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)


if __name__ == "__main__":
    unittest.main()
