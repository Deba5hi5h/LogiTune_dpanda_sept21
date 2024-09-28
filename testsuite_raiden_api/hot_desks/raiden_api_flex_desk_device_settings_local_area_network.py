import logging
import unittest
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork(UIBase):
    """
            Tests to verify Device Settings- Local Area Network

            Tests:
                1.Disable Local Network Access
                2.Enable Local Network Access
                3.Change Password of Local Network Access to Logitech@123
                Negative test:
                4.Change Password of Local Network Access to Logi123
                5.Change Password of Local Network to ""
                6.Change Password of Local Network Access to Logi@3456
        """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()

    device_name = "Coily"
    role = "OrgAdmin"

    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork, self).tearDown()

    def test_1201_VC_122222_flex_desks_device_settings_local_area_network_disable(self):
        local_area_network = 0

        Report.logInfo('STEP 1: Disable Local Network Access')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_local_area_network_status(
            role=self.role, device_name=self.device_name, local_area_network=local_area_network)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1202_VC_122222_flex_desks_device_settings_local_area_network_enable(self):
        local_area_network = 1

        Report.logInfo('STEP 1: Enable Local Network Access')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_local_area_network_status(
            role=self.role, device_name=self.device_name, local_area_network=local_area_network)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1203_VC_122222_flex_desks_device_settings_local_area_network_change_password(self):

        default_password = 'Logi@3456'
        password_list = ['Logitech@123','Logi123',""]

        for password in password_list:
            Report.logInfo('STEP 1: Change Local Network Access Password')
            desk_id, site, token, org_id, device_id = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_local_area_network_change_password(
                role=self.role, device_name=self.device_name, local_area_network_password=password)

            Report.logInfo('STEP 2: Change back to default local area network password')
            self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_local_area_network_set_to_default_password(
                device_name=self.device_name, default_password=default_password, desk_id=desk_id, token=token, org_id=org_id, device_id = device_id)

            Report.logInfo('STEP 3: Delete desk')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

            Report.logInfo(
                'STEP 4 : Delete the site.')
            self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_2301_VC_132410_Edit_FlexDesk_Host_Name(self):
        '''
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a new site, building, area, floor and desk.
                2) Provision Logi Dock Flex to Sync Portal and get the host name of Coily
                3) Edit the flex desk host name
                4) Validate the updated host name
                5) Set the hostname of Coily back to its initial name.
                6) Delete the desk and site

        '''

        Report.logInfo(
            'STEP 1: Edit flex desk host name')

        self.site, self.desk_id, self.device_id = self.syncportal_hotdesks_methods.tc_edit_flexdesk_host_name(desk_name=self.desk_name, role=self.role, device_name=self.device_name)

        Report.logInfo(
            'STEP 2: Delete the desk and site.')
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site)


if __name__ == "__main__":
        unittest.main()