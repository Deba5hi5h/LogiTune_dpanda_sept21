import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIUpdateChannel(UIBase):
    """
        Test to verify update channel Add/View/Modify/Delete API for Meeting Rooms.
    """

    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIUpdateChannel, cls).setUpClass()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaideAPIUpdateChannel, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIUpdateChannel, self).setUp()

    def tearDown(self):
        super(RaideAPIUpdateChannel, self).tearDown()

    def test_801_VC_114564_Add_View_Modify_Delete_UpdateChannel(self):
        """Add/ View/ Modify and Delete Channel: Owner, Org Viewer, Third Party.
                            Setup:
                                  1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                 1. Add Channel: Owner, Org Viewer,Third Party to add meeting room channel
                                 2. View Channel.
                                 3. Assign the update channel to a room
                                 4. Modify Channel.
                                 5. Delete Channel.

        """

        rolelist_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Add Channel.')

            channel_id, channel_name = self.syncportal_methods.tc_rooms_add_channel(role=role_raiden)

            self.channel_id = channel_id
            self.channel_name = channel_name

            Report.logInfo('STEP 2: View the Channel created')

            self.syncportal_methods.tc_view_channel(role=role_raiden)

            Report.logInfo('STEP 3: Change channel of meeting room to newly created channel in step 1.')

            self.syncportal_methods.tc_update_meeting_rooms_channel_name(role=role_raiden,
                                                                         channel_id=self.channel_id,
                                                                         end_user_grp_name_from='prod',
                                                                         channel_name=self.channel_name)

            Report.logInfo('STEP 4: Modify the channel name')

            self.syncportal_methods.tc_modify_channel_name_for_meeting_room(role=role_raiden,
                                                                            channel_id=self.channel_id)

            Report.logInfo('STEP 5: Delete meeting room Channel')
            self.syncportal_methods.tc_delete_meeting_room_channel(role_raiden, channel_id=self.channel_id)


if __name__ == "__main__":
    unittest.main()
