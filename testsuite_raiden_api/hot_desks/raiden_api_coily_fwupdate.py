import logging
import unittest
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPICoilyFWUpdate(UIBase):
    """
        Test to check for firmware update for Coily device and update firmware through APIs.
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    device_name = "Coily"
    now = datetime.now()
    time_now = now.strftime("%Y%m%d%H%M%S")
    desk_name = f'{time_now}Auto-EmptyDesk'
    data = {}

    @classmethod
    def setUp(cls):
        try:
            super(RaidenAPICoilyFWUpdate, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPICoilyFWUpdate, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPICoilyFWUpdate, self).setUp()

    def tearDown(self):
        super(RaidenAPICoilyFWUpdate, self).tearDown()

    def test_1001_VC_119808_FW_Update_LogiDockFlex(self):
        # Pre-requisite: Let the device has update available.
        '''
            Create new site, building, floor, area and desks. Provision the desk and check for
            firmware update.
            Update Firmware and validate if firmware is updated successfully.

                                          Setup:
                                                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor and desk. Provision Logi Dock Flex to Sync Portal.
                2) Check for the availability of update.
                3) Trigger update via Sync Portal- Update now.
                4) Check the update status and verify that the update is completed successfully.
                5) Delete the desk and site

        '''

        Report.logInfo(
            'STEP 1: Check for the availability of firmware update. Trigger update via Sync Portal- Update now. '
            'Check the update status and verify that the update is completed successfully')
        self.site, self.desk_id = self.syncportal_hotdesks_methods.tc_firmware_update_coily(desk_name=self.desk_name,
                                                                  role=self.role,
                                                                  device_name=self.device_name)

        Report.logInfo(
            'STEP 2: Delete the desk and site.')
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
    unittest.main()
