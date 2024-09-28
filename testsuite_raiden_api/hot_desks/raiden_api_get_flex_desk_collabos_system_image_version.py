import logging
import unittest
from datetime import datetime, timedelta

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIGetFlexDeskCollabOSSystemImageVersion(UIBase):
    """
            Test to get flex desk CollabOS and System Image Version.
    """
    syncportal_methods = SyncPortalTCMethods()
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    device_name = "Coily"
    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIGetFlexDeskCollabOSSystemImageVersion, cls).setUpClass()

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIGetFlexDeskCollabOSSystemImageVersion, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIGetFlexDeskCollabOSSystemImageVersion, self).setUp()

    def tearDown(self):
        super(RaidenAPIGetFlexDeskCollabOSSystemImageVersion, self).tearDown()

    def test_2201_VC_131905_Get_FlexDesk_CollabOS_SystemImage_Version(self):
        '''
              Create new site, building, floor, area and desks.
              Provision the desk and get collabos and system image

            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor and desk.
                2) Provision Logi Dock Flex to Sync Portal
                3) Verify CollabOS and System Image
                4) Delete the desk and site

        '''

        Report.logInfo(
            'STEP 1: Get CollabOS and System Image version of coily')

        self.site, self.desk_id = self.syncportal_hotdesks_methods.tc_get_flexdesk_collabos_systemimage_version(desk_name=self.desk_name, role=self.role, device_name=self.device_name)

        Report.logInfo(
            'STEP 2: Delete the desk and site.')
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
    unittest.main()
