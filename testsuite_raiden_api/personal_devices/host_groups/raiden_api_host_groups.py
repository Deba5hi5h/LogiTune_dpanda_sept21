import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIHostGroups(UIBase):
    """
         Test to verify add, view, update and delete host group.
    """

    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIHostGroups, cls).setUpClass()

        except Exception as e:
            log.error("Unable to raise the test-suite")

    @classmethod
    def tearDownClass(cls):
        super(RaideAPIHostGroups, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIHostGroups, self).setUp()

    def tearDown(self):
        super(RaideAPIHostGroups, self).tearDown()

    def test_2024_VC_116404_add_view_update_delete_host_computer_groups(self):
        """Personal Devices: Add, view, update and delete host computer groups: Owner,Admin and Third Party user
            Setup:
                  1. Sign in to Sync Portal using valid credentials of Owner/ Admin/ Third Party user.

            Test:
                 1. Add host group.
                 2. View the host group.
                 3. Update the host group.
                 4. Delete the host group.
        """
        roles_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']
        for role_raiden in roles_raiden:
            Report.logInfo('STEP 1: Add host computer group to the organization.')
            host_group_name = self.syncportal_methods.tc_add_host_group(role=role_raiden)

            Report.logInfo('STEP 2: View the added host computer group.')
            self.syncportal_methods.tc_view_host_group(role=role_raiden, host_group=host_group_name)

            Report.logInfo('STEP 3: Update the added host computer group')
            renamed_room_group = host_group_name + "-renamed"
            self.syncportal_methods.tc_update_host_group(role=role_raiden, existing_host_group=host_group_name,
                                                         renamed_host_group=renamed_room_group)

            Report.logInfo('STEP 4: Delete the added host computer group.')
            self.syncportal_methods.tc_delete_host_group(role_raiden, host_group=host_group_name)


if __name__ == "__main__":
    unittest.main()
