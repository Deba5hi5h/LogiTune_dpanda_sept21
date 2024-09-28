import logging
import unittest
from datetime import datetime, timedelta

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIFlexDeskGroupProvisionCode(UIBase):
    """
            Test to provision flex desk using group provision code generated in Sync Portal
    """
    syncportal_methods = SyncPortalTCMethods()
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    device_name = "Coily"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIFlexDeskGroupProvisionCode, cls).setUpClass()

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskGroupProvisionCode, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskGroupProvisionCode, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskGroupProvisionCode, self).tearDown()

    def test_2301_VC_137033_Provision_FlexDesk_Using_GroupProvisionCode(self):
        '''
              Create new site, building, floor, area and desks.
              Provision the desk to portal using site's group provision code in sync portal

            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor, desk and get the group provision code for desk
                2) Provision Logi Dock Flex to Sync Portal using group provision code
                3) Delete the desk and site

        '''

        Report.logInfo(
            'STEP 1: Provision Flex Desk to Sync Portal using group provision code')
        self.site, self.desk_id  = \
        self.syncportal_hotdesks_methods.tc_get_site_group_provision_code_provision_coily_to_sync_portal(role=self.role, device_name=self.device_name)

        Report.logInfo(
            'STEP 2: Delete the desk and site.')
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
    unittest.main()
