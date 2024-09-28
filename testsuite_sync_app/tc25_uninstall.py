import unittest
from datetime import datetime
from unittest import SkipTest

from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_sync_app.tc_methods import SyncTCMethods


class Uninstall(UIBase):
    sync_app = SyncAppMethods()
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    lna = LNASyncAppMethods()

    def test_251_VC_39960_disconnect_from_sync_app(self):
        room_name = self.sync_app.open_and_get_room_name()
        Report.logInfo(f"Current Room Name: {room_name}")
        self.sync_app.disconnect_room_from_sync_portal(global_variables.config, global_variables.SYNC_ROLE).close()
        # Check Room is deleted from Portal
        if self.sync_portal.login_to_sync_portal_and_verify_provisioned_room(config=global_variables.config,
                                                                             role=global_variables.SYNC_ROLE,
                                                                             room_name=room_name, delete_status=True):
            Report.logPass(f"Room {room_name} is deleted from Sync Portal", True)
        else:
            Report.logFail(f"Room {room_name} is still provisioned in Sync Portal")
        self.sync_portal.browser.close_browser()

    def test_252_VC_40002_disconnect_from_sync_portal(self):
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        room_name = self.sync_app.open().get_room_name()
        self.sync_app.connect_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE, org_name).close()
        # Delete room from Sync Portal
        self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                              role=global_variables.SYNC_ROLE,
                                                              room_name=room_name)
        if self.sync_app.open().click_room().verify_room_disconnected():
            Report.logPass(f"Room {room_name} is disconnected from Sync App", True)
        else:
            Report.logFail(f"Room {room_name} is not disconnected from Sync App")
        self.sync_app.close()

    def test_253_VC_40075_multitenancy_readonly(self):
        # Readonly - Read-only Org
        """
        Test Case to Multi Tenancy - User with Read Only and Admin
        1. Login with User with Read-only
        2. Validate Read-only Organization is disabled and cannot be selected
        """
        email = global_variables.config.ROLES["Readonly"]['signin_payload']['email']
        pwd = global_variables.config.ROLES["Readonly"]['signin_payload']['password']
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        if not self.sync_app.open().click_room().click_connect_to_sync_portal().click_email_and_password() \
                .type_in_user_name(email).type_in_password(pwd).click_connect_room().select_org_name(org_name) \
                .verify_org_name_selected(org_name=org_name):
            Report.logPass("Unable to select Read-only Organization", True)
        else:
            Report.logFail("Able to select Read-only Organization")
        self.sync_app.close()

    def test_254_VC_40077_multitenancy_admin_readonly(self):
        # OrgAdmin - Owner and Read-only
        """
        Test Case to Multi Tenancy - User with Read Only and Admin
        1. Login with User having two organizations. One with Read-only and another Admin
        2. Validate Read-only Organization is disabled and cannot be selected
        3. Validate User can provision to Organization with Admin role
        """
        email = global_variables.config.ROLES["OrgAdmin"]['signin_payload']['email']
        pwd = global_variables.config.ROLES["OrgAdmin"]['signin_payload']['password']
        read_only_org = global_variables.SYNC_ROOM_READONLY[global_variables.SYNC_ENV]
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        if not self.sync_app.open().click_room().click_connect_to_sync_portal().click_email_and_password() \
                .type_in_user_name(email).type_in_password(pwd).click_connect_room().select_org_name(read_only_org) \
                .verify_org_name_selected(org_name=read_only_org):
            Report.logPass("Unable to select Read-only Organization", True)
        else:
            Report.logFail("Able to select Read-only Organization")
        if self.sync_app.room.select_org_name(org_name=org_name).click_join().verify_room_connected():
            Report.logPass("Room connected to Sync Portal successfully", True)
        else:
            Report.logFail("Room connect to Sync Portal Failed")
        room_name = self.sync_app.home.get_room_name()
        self.sync_app.close()
        if self.sync_portal.login_to_sync_portal_and_verify_provisioned_room(config=global_variables.config,
                                                                             role=global_variables.SYNC_ROLE,
                                                                             room_name=room_name):
            Report.logPass(f"Room {room_name} provisioned in Sync Portal", True)
        else:
            Report.logFail(f"Room {room_name} not provisioned in Sync Portal")
        self.sync_portal.delete_room(room_name=room_name)
        self.sync_portal.browser.close_browser()

    def test_255_VC_40079_multitenancy_permission_change(self):
        # Readonly - Read-only Org
        """
        Test Case to Multi Tenancy - User with Read Only and Admin
        1. Login with User with Admin Role
        2. Provision Room
        3. Change the User Role to Read Only
        4. Disconnect Room
        5. Validate Error message displays for permission
        """
        email = global_variables.config.ROLES['Readonly']['signin_payload']['email']
        pwd = global_variables.config.ROLES["Readonly"]['signin_payload']['password']
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        try:
            self.sync_portal.change_org_and_change_user_role(org_name=org_name, org_role="OrgAdmin",
                                                             user=email, role="Admin")
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.connect_to_sync_portal(global_variables.config, "Readonly", org_name).close()
            self.sync_portal.change_org_and_change_user_role(org_name=org_name, org_role="OrgAdmin",
                                                             user=email, role="Read Only")
            if self.sync_app.open().click_room().click_disconnect_room().type_in_user_name(email) \
                    .type_in_password(pwd).click_disconnect_room().verify_no_permission_to_disconnect():
                Report.logPass("Error message displayed for permission", True)
                self.sync_app.room.click_ok()
            else:
                Report.logFail("Error message not displayed for insufficeint permission")
            self.sync_app.close()
            self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                                  role=global_variables.SYNC_ROLE, room_name=room_name)
        except Exception as e:
            Report.logException(str(e))
            self.sync_portal.change_org_and_change_user_role(org_name=org_name, org_role="OrgAdmin",
                                                             user=email, role="Read Only")

    def test_256_VC_40078_multitenancy_no_org(self):
        # Readonly - Read-only Org
        """
        Test Case to Multi Tenancy - User with no organization associated
        1. Login with User with no organization associated
        2. Validate error message displayed for no organization associated
        """
        email = "sveerbhadrappa+0org@logitech.com"
        pwd = global_variables.config.ROLES["OrgViewer"]['signin_payload']['password']
        if self.sync_app.open().click_room().click_connect_to_sync_portal().click_email_and_password() \
                .type_in_user_name(email).type_in_password(pwd).click_connect_room().verify_no_org_name_associated():
            Report.logPass("Error message displayed - No affiliated organization found", True)
            self.sync_app.room.click_ok()
        else:
            Report.logFail("Error message not displayed - No affiliated organization found")
        self.sync_app.close()

    def test_257_VC_40076_multitenancy_3party(self):
        """
        Test Case to Multi Tenancy - User with Third Party permission
        1. Login with User with Third Party permission
        2. Validate user can provision room
        3. Validate user can deprovision room
        """
        email = global_variables.config.ROLES["ThirdParty"]['signin_payload']['email']
        pwd = global_variables.config.ROLES["ThirdParty"]['signin_payload']['password']
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        if self.sync_app.open().click_room().click_connect_to_sync_portal().click_email_and_password() \
                .type_in_user_name(email).type_in_password(pwd).click_connect_room().verify_third_party_permission():
            Report.logPass("Third Party role displayed", True)
        else:
            Report.logFail("Third Party role displayed not displayed")
        if self.sync_app.room.select_org_name(org_name=org_name).click_join().verify_room_connected():
            Report.logPass("Room connected to Sync Portal successfully", True)
        else:
            Report.logFail("Room connect to Sync Portal Failed")
        self.sync_app.disconnect_room_from_sync_portal(global_variables.config, "ThirdParty").close()

    def test_258_VC_39961_uninstall_sync_app(self):
        try:
            # Check the Room Name
            room_name = self.sync_app.open_and_get_room_name()
            Report.logInfo(f"Current Room Name: {room_name}")
            self.sync_app.close()
            self.sync_methods.tc_uninstall_sync_app()
            if self.sync_portal.login_to_sync_portal_and_verify_provisioned_room(config=global_variables.config,
                                                                                 role=global_variables.SYNC_ROLE,
                                                                                 room_name=room_name,
                                                                                 delete_status=True):
                Report.logPass(f"Room {room_name} is deleted from Sync Portal", True)
            else:
                Report.logFail(f"Room {room_name} is still provisioned in Sync Portal")
            self.sync_portal.browser.close_browser()
        except Exception as e:
            Report.logException(str(e))

    def test_259_VC_80210_uninstall_sync_app_provision_code(self):
        """
        VC_80210 :
        1. Create a sync portal room with secondary devices like Tap IP or Tap Scheduler
        2. Use the provision code to connect sync app
        3. Connect a device to sync app
        4. Uninstall sync app
        5. Devices associated with the sync app are removed from the sync portal
        6. Secondary devices present in the room continue to show online.
        7. cleanup : Delete the sync app room
        Expected:
        Removes sync app related devices from the portal but not the secondary devices present in the room
        """
        if global_variables.SYNC_ENV != "raiden-prod":
            Report.logSkip("Test Case only supported in Sync Prod")
            raise SkipTest("Test Case only supported in Sync Prod")
        try:
            self.sync_methods.tc_install_sync_app()
            device_name = "Tap Scheduler"
            now = datetime.now()
            room_name = f"{now.strftime('%Y%m%d%H%M%S')} Auto- {get_custom_platform()}"
            provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=room_name)
            self.sync_methods.lna_ip = "172.28.78.159"
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                       user_name=self.sync_methods.lna_user,
                                                                       password=self.sync_methods.lna_pass,
                                                                       provision_code=provision_code, seat_count=10)
            self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name)
            sync_app_device_name = "MeetUp"
            self.sync_app.open()
            self.sync_app.connect_to_sync_portal_using_provision_code(provision_code=provision_code).close()
            self.sync_methods.tc_add_device(device_name=sync_app_device_name)

            self.sync_methods.tc_uninstall_sync_app()
            self.sync_portal.verify_device_deleted_in_sync_portal(device_name=sync_app_device_name, room_name=room_name)
            self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name)
            self.sync_portal.login_to_sync_portal_and_delete_room(config=global_variables.config,
                                                                  role=global_variables.SYNC_ROLE,
                                                                  room_name=room_name)
        except Exception as e:
            Report.logException(str(e))


if __name__ == "__main__":
    unittest.main()
