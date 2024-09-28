from datetime import datetime
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks


class RaidenAPIHotDesks(UIBase):
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    now = datetime.now()
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"
    desk_id = ''
    site_name = ''
    device_name = 'Coily'

    @classmethod
    def setUpClass(cls) -> None:
        super(RaidenAPIHotDesks, cls).setUpClass()
        cls.role = 'OrgAdmin'

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIHotDesks, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIHotDesks, self).setUp()

    def tearDown(self):
        super(RaidenAPIHotDesks, self).tearDown()

    def test_6101_VC_102225_provision_coily_to_sync_portal(self):
        RaidenAPIHotDesks.site_name, RaidenAPIHotDesks.desk_id = self.syncportal_hotdesks_methods.\
            tc_Provision_Coily_to_Sync_Portal(role=self.role, desk_name=self.desk_name, device_name=self.device_name)

    def test_6102_VC_102227_get_desk_information(self):
        self.syncportal_hotdesks_methods.tc_get_desk_information(desk_name=self.desk_name)

    def test_6103_VC_121135_get_list_of_all_desks_in_organization(self):
        self.syncportal_hotdesks_methods.tc_get_list_of_all_desks_in_organization(role=self.role)

    def test_6104_VC_102228_delete_desk(self):
        self.syncportal_hotdesks_methods.tc_delete_desk(self.role, self.desk_id)

    def test_6105_VC_106480_delete_site(self):
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, self.site_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHotDesks)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")