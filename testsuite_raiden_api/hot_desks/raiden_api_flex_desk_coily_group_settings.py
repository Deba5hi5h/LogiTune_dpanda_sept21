import logging
import unittest
import random

from apis.raiden_api.raiden_api_hot_desks_helper import SyncPortalHotDesksMethods
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIFlexDeskCoilyGroupSettings(UIBase):
    """
            Test case to modify coily group setting

                    Steps:
                        1. Create a site, building, floor, area, desk and provision coily
                        2. Change group settings of an area.
                        3. Change password associated with LNA, internet time to 0.us.pool.ntp.org and USB 3.0 priority to OFF.
                        4. Verify that the setting propagates to device.
                        5. Update Local Network Area password to default password
                        6. Delete created desk
                        7. Delete created site
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()
    sync_portal_hot_desks = SyncPortalHotDesksMethods()

    device = 'Coily'

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskCoilyGroupSettings, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskCoilyGroupSettings, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskCoilyGroupSettings, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskCoilyGroupSettings, self).tearDown()

    def test_1801_VC_125323_flex_desks_change_group_settings_of_area(self):

        rolelist_raiden = ['OrgAdmin']
        '''
                        1. Create a site, building, floor, area, desk and provision coily
                        2. Change group settings of an area.
                        3. Change password associated with LNA, internet time to 0.us.pool.ntp.org and USB 3.0 priority to OFF.
                        4. Verify that the setting propagates to device.                        
                        5. Update Local Network Area password to default password
                        6. Delete created desk
                        7. Delete created site
        '''

        ntp_server = '0.us.pool.ntp.org'  # time.android.com
        lna_password = 'Logi@1234'
        default_password = 'Logi@3456'

        for role in rolelist_raiden:
            Report.logInfo('STEP 1:Create desk, provision coily and get desk details')
            token, org_id, site, area, desk_id, device_id, empty_desk_id = self.syncportal_hotdesks_methods.tc_create_desk_provision_coily_get_desk_details(role=role, device_name=self.device)

            Report.logInfo('STEP 2:Change the group setting of an area')
            self.syncportal_hotdesks_methods.tc_flex_desk_change_group_settings_of_area(token=token, org_id=org_id, role=role, desk_id=desk_id, device_name=self.device, area=area, ntp_server=ntp_server, lna_password=lna_password, default_password=default_password, empty_desk_id=empty_desk_id)

            Report.logInfo('STEP 3: Set the local area network password')
            self.syncportal_hotdesks_methods.tc_set_local_area_network_password(token=token, org_id=org_id, default_password=default_password, area=area)

            Report.logInfo('STEP 4: Delete desk')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, empty_desk_id)

            Report.logInfo('STEP 5 : Delete the site')
            self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


if __name__ == "__main__":
    unittest.main()
