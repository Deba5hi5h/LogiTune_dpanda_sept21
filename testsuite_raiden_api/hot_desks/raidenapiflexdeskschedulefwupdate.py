import logging
import unittest
import sys
from datetime import datetime, timedelta

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIFlexDeskScheduleFirmwareUpdate(UIBase):
    """
        Test to verify flex desk schedule firmware update.
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
            super(RaidenAPIFlexDeskScheduleFirmwareUpdate, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskScheduleFirmwareUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskScheduleFirmwareUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskScheduleFirmwareUpdate, self).tearDown()

    def test_2001_VC_131010_Schedule_FW_Update_LogiDockFlex(self):
        # Pre-requisite: Let the device be in Update Available state.
        '''
            Create new site, building, floor, area and desks. Provision the desk and check for
            firmware update.
            Schedule Firmware Update and validate if firmware is updated successfully at the scheduled time period.

            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor and desk. Provision Logi Dock Flex to Sync Portal.
                2) Check for the availability of update.
                3) Schedule the firmware update via Sync Portal-Schedule Now.
                4) Check the update status and verify that the update is completed successfully.
                5) Delete the desk and site

        '''

        role_raiden = 'OrgAdmin'

        Report.logInfo(
            'STEP 1: Check for the availability of firmware update. Schedule update via Sync Portal- Schedule Now. '
            'Check the update status and verify that the update is completed successfully')
        self.site, self.desk_id = self.syncportal_hotdesks_methods.tc_schedule_firmware_update_coily(desk_name=self.desk_name,
                                                                                            role=role_raiden, device_name=self.device_name)


        Report.logInfo(
            'STEP 2: Delete the desk and site.')
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
    unittest.main()