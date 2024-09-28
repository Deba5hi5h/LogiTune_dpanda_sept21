import logging
import unittest
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIMoveDeskToGroup(UIBase):
    """
               Test case to move and verify if flex desk moved to new group .
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()

    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIMoveDeskToGroup,cls).setUpClass()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIMoveDeskToGroup, cls).tearDownClass()


    def setUp(self):
        super(RaidenAPIMoveDeskToGroup, self).setUp()

    def tearDown(self):
        super(RaidenAPIMoveDeskToGroup, self).tearDown()

    def test_801_VC_119792_Move_Desk_To_Group(self):
        """
                       Test to move desk to new group .
        """

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in role_list_raiden:
            Report.logInfo('STEP 1: Move desk to new group created')

            desk_id = self.syncportal_hotdesks_methods.tc_move_hot_desk_to_a_group(
                role=role_raiden, desk_name=self.desk_name)
            self.desk_id = desk_id

            Report.logInfo(
                'STEP 2: Delete the desk')
            self.syncportal_hotdesks_methods.tc_delete_desk(role=role_raiden, desk_id=self.desk_id)

    def test_802_VC_119796_Get_Desk_Check_In_Url(self):
        """
                       Get check-in URL of a desk.
                       Steps:
                       1.Create an empty desk under an area.
                       2.Get check-in URL of a desk.
                       3.Delete the empty desk.
        """

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in role_list_raiden:
            Report.logInfo('STEP 1: Get desk check-in url')

            desk_id = self.syncportal_hotdesks_methods.tc_get_hot_desk_check_in_url(
                role=role_raiden, desk_name=self.desk_name)
            self.desk_id = desk_id

            Report.logInfo(
                'STEP 2: Delete the desk')
            self.syncportal_hotdesks_methods.tc_delete_desk(role_raiden, self.desk_id)

    def test_803_VC_119793_Edit_Desk_Attributes(self):
        """
                       Edit Desk Attributes
                       Steps:
                       1.Create empty desk.
                       2.Edit desk attributes.
                       3.Delete the site and desk.
        """

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in role_list_raiden:
            Report.logInfo('STEP 1: Edit desk attributes')

            site_name, desk_id = self.syncportal_hotdesks_methods.tc_edit_desk_attributes(
                role=role_raiden, desk_name=self.desk_name)

            self.desk_id = desk_id
            self.site = site_name

            Report.logInfo(
                'STEP 2: Delete the desk and site.')
            self.syncportal_hotdesks_methods.tc_delete_desk(role_raiden, self.desk_id)
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, self.site)

    def test_804_VC_119795_Edit_Area_Attributes(self):
        """
                       Edit Area Attributes
                       Steps:
                       1.Create empty Area.
                       2.Edit Area attributes.
                       3.Delete the site.
        """

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in role_list_raiden:
            Report.logInfo('STEP 1: Edit area attributes')

            site_name = self.syncportal_hotdesks_methods.tc_edit_area_attributes(
                role=role_raiden)
            self.site_name = site_name

            Report.logInfo(
                'STEP 2: Delete the site')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, self.site_name)


if __name__ == "__main__":
    unittest.main()
