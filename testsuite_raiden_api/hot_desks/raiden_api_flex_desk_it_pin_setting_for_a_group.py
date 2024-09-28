import logging
import unittest
import random

from apis.raiden_api.raiden_api_hot_desks_helper import SyncPortalHotDesksMethods
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIFlexDeskITPinSettingForGroup(UIBase):
    """
            Test case to set IT pin setting for a group

                    Test:
                        1. Add IT setting PIN for a group
                        2. View IT settings PIN of a group
                        3. Edit IT setting PIN for a group
                        4. Add a different PIN to the level with an existing PIN
                        5. Add a duplicate PIN to the level
                        6. Delete IT setting PIN of a group
                        7. Add a PIN with 3 digits
                        8. Add a PIN with 5 characters
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()
    sync_portal_hot_desks = SyncPortalHotDesksMethods()

    desk_it_pin = str(random.randint(1000, 5000))
    modified_it_pin = str(random.randint(6000, 9999))
    duplicate_pin = desk_it_pin
    three_digit_it_pin = str(random.randint(100, 999))
    five_digit_it_pin = str(random.randint(10000, 99999))
    zero_digit_it_pin = 0

    # Creating Site group
    site_name = '/Test_' + str(int(random.random() * 10000))

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskITPinSettingForGroup, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskITPinSettingForGroup, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskITPinSettingForGroup, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskITPinSettingForGroup, self).tearDown()

    def test_1101_VC_120753_flex_desks_it_pin_setting_for_a_group(self):

        rolelist_raiden = ['OrgAdmin', 'ThirdParty']

        for role in rolelist_raiden:
            Report.logInfo('Creating site group')
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.site_name)

            Report.logInfo('STEP 1: Add IT setting PIN for a group')
            pin_id = self.syncportal_hotdesks_methods.tc_flex_desk_add_it_setting_pin_to_a_group(
                role=role, desk_it_pin=self.desk_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 2: View IT setting PIN for a group')
            response_pin_id = self.syncportal_hotdesks_methods.tc_flex_desk_view_it_setting_pin_to_a_group(
                role=role, group_name=self.site_name, pin_id=pin_id)

            Report.logInfo('STEP 3: Edit IT setting PIN for a group')
            self.syncportal_hotdesks_methods.tc_flex_desk_edit_it_setting_pin_to_a_group(
                role=role, pin_id=response_pin_id, modified_it_pin=self.modified_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 4: Delete IT setting PIN for a group')
            self.syncportal_hotdesks_methods.tc_flex_desk_delete_it_setting_pin_to_a_group(
                role=role, group_name=self.site_name, pin_id=response_pin_id)


    def test_1102_VC_120753_flex_desks_it_pin_setting_negative_scenario(self):

        rolelist_raiden = ['OrgAdmin', 'ThirdParty']

        for role in rolelist_raiden:
            Report.logInfo('Creating site group')
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.site_name)

            Report.logInfo('STEP 1: Add IT setting PIN for a group')
            pin_id = self.syncportal_hotdesks_methods.tc_flex_desk_add_it_setting_pin_to_a_group(
                role=role, desk_it_pin=self.desk_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 2: Add a different PIN to the level with an existing PIN')
            self.syncportal_hotdesks_methods.tc_flex_desk_add_different_pin_to_existing_pin(
                role=role, desk_it_pin=self.modified_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 3: Add a duplicate PIN to the level')
            self.syncportal_hotdesks_methods.tc_flex_desk_add_duplicatet_pin_to_existing_pin(
                role=role, duplicate_pin=self.duplicate_pin, group_name=self.site_name)

            Report.logInfo('STEP 4: Delete IT setting PIN for a group')
            self.syncportal_hotdesks_methods.tc_flex_desk_delete_it_setting_pin_to_a_group(
                role=role, group_name=self.site_name, pin_id=pin_id)

            Report.logInfo('STEP 5: Add PIN with 3 digits')
            self.syncportal_hotdesks_methods.tc_flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(
                role=role, desk_it_pin=self.three_digit_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 6: Add PIN with 5 digits')
            self.syncportal_hotdesks_methods.tc_flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(
                role=role, desk_it_pin=self.five_digit_it_pin, group_name=self.site_name)

            Report.logInfo('STEP 7: Verify for PIN with 0 digit')
            self.syncportal_hotdesks_methods.tc_flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(
                role=role, desk_it_pin=self.zero_digit_it_pin, group_name=self.site_name)


if __name__ == "__main__":
    unittest.main()
