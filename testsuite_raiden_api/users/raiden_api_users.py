import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIUser(UIBase):
    """
    Test to verify device APIs for Brio.
    """
    syncportal_methods = SyncPortalTCMethods()
    users_email = {}
    users_userid = {}

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIUser, cls).setUpClass()

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIUser, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIUser, self).setUp()

    def tearDown(self):
        super(RaidenAPIUser, self).tearDown()

    def test_201_VC_86203_add_view_update_delete_IT_users_by_owner(self):
        """Owner: Add/ View/ Update and Delete IT users: Owner, Admin, Read Only, Third Party, Installer, Device Admin
        and Device Manager.
        Setup:
              1. Sign in to Sync Portal using valid owner credentials.

        Test:
             1. Add the users: Owner, Admin, Read Only, Third Party, Installer, Device Admin and Device Manager to the
             organization.
             2. View the users.
             3. Update the role of users.
             4. Delete the users.

        """
        Report.logInfo(
            "STEP 1: Owner: Add the IT users: Owner, Admin, Read Only, Third Party, Installer, Device Admin and "
            "Device Manager to the organization."
        )
        role_raiden = "OrgAdmin"

        user_id_owner, email_owner = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgOwner"
        )
        user_id_admin, email_admin = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgMember"
        )
        user_id_readonly, email_readonly = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgViewer"
        )
        user_id_thirdparty, email_thirdparty = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgProxy"
        )
        user_id_installer, email_installer = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgInstaller"
        )
        user_id_device_admin, email_device_admin = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgDeviceAdmin"
        )
        user_id_device_manager, email_device_manager = self.syncportal_methods.tc_add_user(
            role=role_raiden, user="OrgDeviceManager"
        )

        self.users_email["OrgOwner"] = email_owner
        self.users_email["OrgMember"] = email_admin
        self.users_email["OrgViewer"] = email_readonly
        self.users_email["OrgProxy"] = email_thirdparty
        self.users_email["OrgInstaller"] = email_installer
        self.users_email["OrgDeviceAdmin"] = email_device_admin
        self.users_email["OrgDeviceManager"] = email_device_manager

        self.users_userid["OrgOwner"] = user_id_owner
        self.users_userid["OrgMember"] = user_id_admin
        self.users_userid["OrgViewer"] = user_id_readonly
        self.users_userid["OrgProxy"] = user_id_thirdparty
        self.users_userid["OrgInstaller"] = user_id_installer
        self.users_userid["OrgDeviceAdmin"] = user_id_device_admin
        self.users_userid["OrgDeviceManager"] = user_id_device_manager

        Report.logInfo("STEP 2: View the created IT users")
        for key, value in self.users_userid.items():
            self.syncportal_methods.tc_view_user(
                role=role_raiden, user=key, email_user=self.users_email[key]
            )

        Report.logInfo("STEP 3: Update the role of created IT users")
        for key, value in self.users_userid.items():
            if key != "OrgMember":
                self.syncportal_methods.tc_update_user(
                    role=role_raiden,
                    user=value,
                    usertype_from=key,
                    usertype_to="OrgMember"
                )
            else:
                self.syncportal_methods.tc_update_user(
                    role=role_raiden,
                    user=value,
                    usertype_from=key,
                    usertype_to="OrgOwner"
                )
        Report.logInfo("STEP 4: Delete the created IT users")
        for key, value in self.users_userid.items():
            self.syncportal_methods.tc_delete_user(role_raiden, key, value)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
