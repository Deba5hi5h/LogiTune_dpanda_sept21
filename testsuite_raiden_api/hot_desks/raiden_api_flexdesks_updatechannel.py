import logging
import unittest
from datetime import datetime

from base.base_ui import UIBase
from testsuite_raiden_api.hot_desks.raiden_api_hot_desks import RaidenAPIHotDesks
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIUpdateChannelForFlexDesks(UIBase):
    """
           Test to verify update channel Add/View/Modify/Delete API for Flex Desks.
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIUpdateChannelForFlexDesks, cls).setUpClass()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaideAPIUpdateChannelForFlexDesks, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIUpdateChannelForFlexDesks, self).setUp()

    def tearDown(self):
        super(RaideAPIUpdateChannelForFlexDesks, self).tearDown()

    def test_901_VC_114935_Add_View_Modify_Delete_UpdateChannel(self):
        """Add/ View/ Modify and Delete Channel: Owner, Org Viewer, Third Party.
                                    Setup:
                                          1. Sign in to Sync Portal using valid owner credentials.

                                    Test:
                                         1. Add Channel: Owner, Org Viewer,Third Party to add channel to flex desk
                                         2. View Channel.
                                         3. Assign the update channel to a desk
                                         4. Modify Channel.
                                         5. Delete Channel.

                """

        rolelist_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Add Channel to Flex Desks')

            channel_id, channel_name = self.syncportal_hotdesks_methods.tc_flex_desks_add_channel(role=role_raiden)

            self.channel_id = channel_id
            self.channel_name = channel_name

            Report.logInfo(
                'STEP 2: View Channel created for Flex Desks')

            self.syncportal_hotdesks_methods.tc_flex_desks_view_channel(role=role_raiden,
                                                                        channel_name=self.channel_name,
                                                                        channel_id = self.channel_id)

            Report.logInfo('STEP 3: Assign the update channel to a desk')
            self.syncportal_hotdesks_methods.tc_update_flex_desks_channel_name(role=role_raiden, channel_id=self.channel_id, end_user_grp_name_from='$prod',
                                           channel_name=self.channel_name)

            Report.logInfo('STEP 4: Modify Channel')
            self.syncportal_hotdesks_methods.tc_modify_channel_name_for_flex_desk(role=role_raiden,
                                                                            channel_id=self.channel_id, channel_name=self.channel_name)

            Report.logInfo('STEP 5: Delete Channel')
            self.syncportal_hotdesks_methods.tc_delete_flex_desk_channel(role_raiden, channel_id=self.channel_id)


if __name__ == "__main__":
    unittest.main()
