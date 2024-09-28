import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidensApiCustomTags(UIBase):
    """
        Test to verify custom tags for meeting rooms.
    """
    syncportal_methods = SyncPortalTCMethods()
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    tag_name = now.strftime("%Y%m%d%H%M%S") + " tag"
    role = "OrgAdmin"

    def test_701_vc_147247_add_remove_custom_tags(self):
        '''
                     Test: To add and remove custom tags
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Create room


                    Test:
                        1.Add custom tag to the selected room
                        2.Remove custom tag from the above selected room
                        3.Delete created room
                        4.Delete created site
                '''

        Report.logInfo(
            'STEP 1: Create room')
        self.room_id = self.syncportal_methods.tc_create_empty_room(role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 2: Add room to group')
        site_name = self.syncportal_methods.tc_add_room_to_group(
            role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 3: Add custom tag to room')
        tag_name_added = self.syncportal_methods.tc_add_remove_custom_tags(self.role, self.room_id, self.tag_name, operation="add")

        Report.logInfo(
            'STEP 4: Remove custom tag from room')
        self.syncportal_methods.tc_add_remove_custom_tags(self.role, self.room_id, tag_name = tag_name_added, operation="remove")

        Report.logInfo(
            'STEP 5: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 6 : Delete the site.')
        self.syncportal_methods.tc_delete_site(self.role, site_name)


    def test_702_vc_147247_add_remove_custom_tags_from_room_details(self):
        '''
                     Test: To add and remove custom tags from room details page
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Create room


                    Test:
                        1.Add custom tag to the selected room from room details page
                        2.Remove custom tag to the selected room from room details page
                        3.Delete created room
                        4.Delete created site
                '''

        assets = "Video"

        Report.logInfo(
            'STEP 1: Create room')
        self.room_id = self.syncportal_methods.tc_create_empty_room(role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 2: Add room to group')
        site_name = self.syncportal_methods.tc_add_room_to_group(
            role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 3: Add custom tag to room details page')
        tag_name_added = self.syncportal_methods.tc_add_remove_custom_tags_from_details_page(self.role, self.room_name, self.room_id, assets, self.tag_name, operation="add")

        Report.logInfo(
            'STEP 4: Remove custom tag from room details page')
        self.syncportal_methods.tc_add_remove_custom_tags_from_details_page(self.role, self.room_name, self.room_id, assets, tag_name = tag_name_added, operation="remove")

        Report.logInfo(
            'STEP 5: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 6 : Delete the site.')
        self.syncportal_methods.tc_delete_site(self.role, site_name)


    def test_703_vc_147247_add_remove_custom_tags_to_multiple_rooms(self):
        '''
                     Test: To add and remove custom tags to multiple rooms
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Create multiple rooms


                    Test:
                        1.Add custom tag to to multiple rooms
                        2.Remove custom tag from multiple rooms
                        3.Delete created rooms
                '''

        Report.logInfo(
            'STEP 1: Create room')
        room_names, room_ids = self.syncportal_methods.tc_add_multiple_rooms(role=self.role)

        Report.logInfo(
            'STEP 2: Add custom tag to multiple rooms')
        tag_name_added = self.syncportal_methods.tc_add_remove_custom_to_multiple_rooms(self.role, room_ids, tag_name = self.tag_name, operation="add")

        Report.logInfo(
            'STEP 3: Remove custom tag from multiple room')
        self.syncportal_methods.tc_add_remove_custom_to_multiple_rooms(self.role, room_ids, tag_name = tag_name_added, operation="remove")

        Report.logInfo(
            'STEP 4: Delete all the created room')
        self.syncportal_methods.tc_delete_rooms(self.role, room_names)



    if __name__ == "__main__":
        unittest.main()