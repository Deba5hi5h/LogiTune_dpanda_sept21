import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPISystemAdmin(UIBase):
    syncportal_methods = SyncPortalTCMethods()
    prov_list = dict()
    created_org_id = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPISystemAdmin, cls).setUpClass()
            cls.role = 'SysAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPISystemAdmin, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPISystemAdmin, self).setUp()

    def tearDown(self):
        super(RaidenAPISystemAdmin, self).tearDown()
        self.token = self.org_id = None

    def test_001_VC_11056_SystemAdmin_Create_New_Org(self):
        try:
            response, status = self.syncportal_methods.tc_create_new_org(role=self.role)
            RaidenAPISystemAdmin.created_org_id = response['id']

        except Exception as e:
            Report.logException(f'{e}')

    def test_002_VC_11060_SystemAdmin_Update_Org(self):
        self.syncportal_methods.tc_update_org(role=self.role, org_id=self.created_org_id)

    def test_003_SystemAdmin_Add_Owner(self):
        try:
            user_role = 'OrgOwner'
            user_id, email = self.syncportal_methods.tc_add_user(role=self.role, user=user_role)
            self.syncportal_methods.tc_delete_user(self.role, user_role, user_id)

        except Exception as e:
            Report.logException(f'{e}')

    def test_004_Sysadmin_Gets_List_Of_All_Orgs(self):
        self.syncportal_methods.tc_get_count_of_all_orgs(role=self.role)

    def test_005_VC_11058_Sysadmin_Gets_List_Of_All_Orgs_Using_Raiden_Api(self):
        self.syncportal_methods.tc_get_count_of_all_orgs_using_raiden_api(role=self.role)

    def test_006_VC_11061_Sysadmin_Delete_Org(self):
        self.syncportal_methods.tc_delete_org(role=self.role, org_id= self.created_org_id)


if __name__ == "__main__":
    unittest.main()
