import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaideAPIEndUsersGroups(UIBase):
    """
         Test to verify add API End Users Groups.
    """

    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaideAPIEndUsersGroups, cls).setUpClass()

        except Exception as e:
            log.error("Unable to raise the test-suite")

    @classmethod
    def tearDownClass(cls):
        super(RaideAPIEndUsersGroups, cls).tearDownClass()

    def setUp(self):
        super(RaideAPIEndUsersGroups, self).setUp()

    def tearDown(self):
        super(RaideAPIEndUsersGroups, self).tearDown()

    def test_701_VC_113973_Add_View_Update_Delete_EndUsersGroups(self):
        """Add/ View/ Update and Delete end users groups: Owner,OrgViewer, Third Party.
                                    Setup:
                                          1. Sign in to Sync Portal using valid owner credentials.
                                          (User can login with different roles OrgAdmin, Third Party, OrgViewer to the organization)

                                    Test:
                                         1. Add the end users group:
                                         2. View the end users group.
                                         3. Update the end users group.
                                         4. Delete the end users group.



                                """
        Report.logInfo('STEP 1: Add the end users group to the organization.')

        rolelist_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']

        for role_raiden in rolelist_raiden:
            cohort_id, end_user_group_name = self.syncportal_methods.tc_add_end_user_group(role=role_raiden)

            self.users_userid = cohort_id
            self.end_user_group_name = end_user_group_name
            end_user_group_name_to = self.end_user_group_name + "_updated"

            Report.logInfo('STEP 2: View the added end users groups.')

            self.syncportal_methods.tc_view_end_user_group(role=role_raiden,
                                                           cohort_id=self.users_userid)

            Report.logInfo('STEP 3: Update the added end user group.')

            self.syncportal_methods.tc_update_end_user_group(role=role_raiden, cohort_id=self.users_userid,
                                                             end_user_group_name_from=self.end_user_group_name,
                                                             end_user_group_name_to=end_user_group_name_to)

            Report.logInfo('STEP 4: Delete the added end user group.')
            self.syncportal_methods.tc_delete_end_user_group(role_raiden, cohort_id=self.users_userid)

    def test_702_VC_113973_Modify_EndUserGroup_OfAn_EndUser(self):
        """Modify end user group of an end user:: Owner, OrgViewer, Third Party.
                                    Setup:
                                          1. Sign in to Sync Portal using valid owner credentials.
                                          (User can login with different roles OrgAdmin, Third Party, OrgViewer to the organization)

                                    Test:
                                         1. Add a new end user group:
                                         2. Add a new end user :
                                         3. Change end user group of end user to the newly created end user group in step 1.
                                         4. View end user to check that end user group is modified.
                                         5. Delete end user.
                                         6. Delete end user group.


                                """
        Report.logInfo('STEP 1: Add a new end user group.')

        role_list_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']
        for role_raiden in role_list_raiden:
            cohort_id, end_user_group_name = self.syncportal_methods.tc_add_end_user_group(role=role_raiden)

            self.users_cohort_id = cohort_id
            self.end_user_group_name = end_user_group_name
            end_user_group_cohort_id = self.users_cohort_id

            Report.logInfo('STEP 2: Add a new end user.')

            end_user_id, email = self.syncportal_methods.tc_add_end_user(role=role_raiden)

            self.users_user_id = end_user_id
            self.users_email = email

            Report.logInfo('STEP 3: Change end user group of end user to the newly created end user group in step 1.')


            self.syncportal_methods.tc_update_end_user_group_with_new_group_name(role=role_raiden,
                                                                                 end_user_id=self.users_user_id,
                                                                                 end_user_group_name_from='Standard',
                                                                                 end_user_group_cohort_id=end_user_group_cohort_id)
            Report.logInfo('STEP 4: View end user to check that end user group is modified.')
            self.syncportal_methods.tc_view_end_user_and_group(role=role_raiden,
                                                               end_user_id=self.users_user_id,
                                                               new_end_user_group_id=end_user_group_cohort_id,
                                                               end_user_group_name=self.end_user_group_name)

            Report.logInfo('STEP 5: Delete end user')
            self.syncportal_methods.tc_delete_end_user(role_raiden, self.users_user_id)

            Report.logInfo('STEP 6: Delete the added end user group.')
            self.syncportal_methods.tc_delete_end_user_group(role_raiden, self.users_cohort_id)


if __name__ == "__main__":
    unittest.main()
