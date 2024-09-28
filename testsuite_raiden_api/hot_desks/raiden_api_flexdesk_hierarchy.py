import logging
import unittest
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from extentreport.report import Report


class RaidenAPITestsForFlexDeskHierarchy(UIBase):
    """
              Test to verify Add/View/Modify/Delete API for Site, Building, Floor, Area, Flex Desks.
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()

    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPITestsForFlexDeskHierarchy, cls).setUpClass()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPITestsForFlexDeskHierarchy, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPITestsForFlexDeskHierarchy, self).setUp()

    def tearDown(self):
        super(RaidenAPITestsForFlexDeskHierarchy, self).tearDown()

    def test_701_VC_116894_Add_View_Modify_Delete_DeskHierarchy(self):
        """Add/ View/ Modify and Delete Site, Building, Floor, Area, Flex Desks: Owner, Org Viewer, Third Party.
                                          Setup:
                                                1. Sign in to Sync Portal using valid owner credentials.

                                          Test:
                                               1. Add a new site, building, floor, area and empty desk.
                                               2. View site, building, floor, area and empty desk.
                                               3. Rename desk, area, floor, building and site
                                               4. Delete desk, area, floor, building and site.


        """

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in role_list_raiden:
            Report.logInfo(
                'STEP 1: Add a new site, building, floor, area and empty desk.')

            RaidenAPITestsForFlexDeskHierarchy.site_name, RaidenAPITestsForFlexDeskHierarchy.desk_id = self.syncportal_hotdesks_methods.tc_add_hot_desk_hierarchy(
                role=role_raiden, desk_name=self.desk_name)

            self.desk_id = RaidenAPITestsForFlexDeskHierarchy.desk_id

            Report.logInfo(
                'STEP 2: View site, building, floor, area and empty desk.')

            self.syncportal_hotdesks_methods.tc_view_hot_desk_hierarchy(
                role=role_raiden, desk_name=self.desk_name, desk_id=self.desk_id)

            Report.logInfo(
                'STEP 3: Rename site, building, floor, area and empty desk.')

            self.syncportal_hotdesks_methods.tc_modify_hot_desk_hierarchy(
                role=role_raiden, desk_name=self.desk_name, desk_id=self.desk_id)

            Report.logInfo('STEP 4: Delete Desk Hierarchy')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk_hierarchy(role=role_raiden, desk_id=self.desk_id)

if __name__ == "__main__":
    unittest.main()