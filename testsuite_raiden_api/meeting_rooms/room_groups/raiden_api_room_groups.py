import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIRoomGroups(UIBase):
    """
         Test to verify add, view, update and delete room group.
    """

    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIRoomGroups, cls).setUpClass()

        except Exception as e:
            log.error("Unable to raise the test-suite")

    @classmethod
    def tearDownClass(cls):
        super(RaideAPIRoomGroups, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIRoomGroups, self).setUp()

    def tearDown(self):
        super(RaideAPIRoomGroups, self).tearDown()

    def test_2023_VC_116403_add_view_update_delete_room_groups(self):
        """Add, view, update and delete room groups: Owner,Admin and Third Party user
            Setup:
                  1. Sign in to Sync Portal using valid credentials of Owner/ Admin/ Third Party user.

            Test:
                 1. Add room group.
                 2. View the room group.
                 3. Update the room group.
                 4. Delete the room group.
        """
        roles_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']
        for role_raiden in roles_raiden:
            Report.logInfo('STEP 1: Add room group to the organization.')
            room_group_name = self.syncportal_methods.tc_add_room_group(role=role_raiden)

            Report.logInfo('STEP 2: View the added room group.')
            self.syncportal_methods.tc_view_room_group(role=role_raiden, room_group=room_group_name)

            Report.logInfo('STEP 3: Update the added room group')
            renamed_room_group = room_group_name + "-renamed"
            self.syncportal_methods.tc_update_room_group(role=role_raiden, existing_room_group=room_group_name,
                                                         renamed_room_group=renamed_room_group)

            Report.logInfo('STEP 4: Delete the added room group.')
            self.syncportal_methods.tc_delete_room_group(role_raiden, room_group=room_group_name)


if __name__ == "__main__":
    unittest.main()
