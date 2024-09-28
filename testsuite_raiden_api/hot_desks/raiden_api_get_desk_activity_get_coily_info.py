from datetime import datetime
import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report


log = logging.getLogger(__name__)

class RaidenAPIGetDeskActivityGetCoilyInfo(UIBase):
    """
        Test case to get desk activity/event details and
        information related to peripherals connected to coily

    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()
    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"
    device_name = "Coily"

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIGetDeskActivityGetCoilyInfo, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIGetDeskActivityGetCoilyInfo, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIGetDeskActivityGetCoilyInfo, self).setUp()

    def tearDown(self):
        super(RaidenAPIGetDeskActivityGetCoilyInfo, self).tearDown()

    def test_1701_VC_124632_get_desk_activity_details(self):
        """
              Test case to get desk activity details

                            Steps:
                                1. Sign in to Sync Portal using valid owner credentials.
                                2. Create an empty desk in Sync Portal.
                                3. Provision Coily to Sync Portal.
                                4. Get Desk Activity

        """

        rolelist_raiden = ['OrgAdmin', 'ThirdParty']
        
        for role_raiden in rolelist_raiden:

            Report.logInfo('STEP 1: Get desk activity')
            desk_id, site = self.syncportal_hotdesks_methods.tc_get_desk_activity_details(
                role=role_raiden, device_name=self.device_name)

            Report.logInfo('STEP 2: Delete desk')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

            Report.logInfo(
                'STEP 3 : Delete the site.')
            self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1702_VC_124632_get_peripheral_information(self):
        """
              Test case to get peripheral information
                            Steps:
                                1. Connect Brio 105 (Cezanne) and Zone Vibe Wireless(Enduro) to Coily's rear port peripherals.
                                2. Sign in to Sync Portal using valid owner credentials.
                                3. Create an empty desk in Sync Portal and Provision Coily.
                                4. Get the info associated with peripherals, their healthStatus, UpdateStatus and status (Use State).
        """
        rolelist_raiden = ['OrgAdmin', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Get the info associated with peripherals, their healthStatus, UpdateStatus and status (Use State).')
            desk_id, site = self.syncportal_hotdesks_methods.tc_get_peripheral_use_state(
                role=role_raiden, device_name=self.device_name)

            Report.logInfo('STEP 2: Delete desk')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

            Report.logInfo(
                'STEP 3 : Delete the site.')
            self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


if __name__ == "__main__":
    unittest.main()