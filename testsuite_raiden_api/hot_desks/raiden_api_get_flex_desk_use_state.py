import logging
import unittest
from datetime import datetime, timedelta

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIGetFlexDeskUseState(UIBase):
    """
            Test to verify flex desk use state.
    """
    syncportal_methods = SyncPortalTCMethods()
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    device_name = "Coily"
    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"
    data = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIGetFlexDeskUseState, cls).setUpClass()

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIGetFlexDeskUseState, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIGetFlexDeskUseState, self).setUp()

    def tearDown(self):
        super(RaidenAPIGetFlexDeskUseState, self).tearDown()

    def test_2101_VC_131135_Get_FlexDesk_Use_State(self):
        '''
              Create new site, building, floor, area and desks. Provision the desk and check use state for below states:
                2 - Available (Provisioned and USB not connected to Coily)
                10 - In Use (Provisioned and USB connected to Coily)
                -1 - Unknown/NA (Verifying Empty Desk status, don't Provision)

            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor and desk.
                2) Verify the use state for empty desk
                3) Provision Logi Dock Flex to Sync Portal and verify for Available status
                4) Provision Logi Dock Flex to Sync Portal and verify for In Use status
                5) Delete the desk and site

        '''

        usestate_list = ['Available', 'In Use', 'NA']

        Report.logInfo(
            'STEP 1: Get and verify use state of flex desk')
        for usestate in usestate_list:
            self.site, self.desk_id  = self.syncportal_hotdesks_methods.tc_get_flexdesk_use_state(desk_name=self.desk_name, role=self.role, device_name=self.device_name,usestate=usestate)

            Report.logInfo(
                'STEP 2: Delete the desk and site.')
            self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
            self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
    unittest.main()
