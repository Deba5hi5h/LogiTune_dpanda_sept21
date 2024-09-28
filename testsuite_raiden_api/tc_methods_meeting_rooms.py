import json
import logging
import os

import traceback

from apis.raiden_api import raiden_helper, raiden_validation_methods
from apis.raiden_api.raiden_api_user_helper import get_meeting_room_channel_info, get_channel_info_for_meeting_room

import requests

from base.base_ui import UIBase
from common import raiden_config
from common.usb_switch import *
from apps.sync.sync_app_methods import SyncAppMethods
from apis.raiden_api import raiden_api_user_helper as raiden_user_helper
from apis.raiden_api import raiden_api_rightsight_helper as raiden_righsight_helper
from apis.raiden_api.raiden_algolia import RaidenAlgolia
from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from common import framework_params as fp

from datetime import datetime
from extentreport.report import Report
import random

log = logging.getLogger(__name__)


class SyncPortalTCMethods(UIBase):
    sync_app = SyncAppMethods()
    org_id = None
    token = None

    def tc_raiden_backend_version(self):
        """
        Get raiden backend version
        """
        try:
            self.banner(f'Get raiden backend version')
            raiden_backend_version = raiden_helper.get_raiden_backend_version(global_variables.config)
            Report.logInfo(f'Sync Portal API version is {raiden_backend_version}')
            assert raiden_backend_version is not None, 'Error in backend version'
            return raiden_backend_version

        except Exception as e:
            Report.logException(str(e))

    def tc_sign_in(self, role: str):
        """
        Sign in to Sync Portal using the provided role
        """
        try:
            self.banner(f'Sign in with role: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            assert self.token is not None, 'Error in token'

        except Exception as e:
            Report.logException(str(e))

    def tc_create_new_org(self, role):
        """Create new organization

            Setup:
                Sign in with valid system admin credentials.

            Test:
                1. Test case to create new organization by SysAdmin.
                2. Validate that the org is created by making POST call to the organization by SysAdmin
                and validate that other users should get forbidden error
                3. Create New Org
                POST ~/org
                4. Validate that the org is created by sysadmin
                by making GET call
                GET ~/org/{id}
                5. Validate that other org roles get forbidden error
                as response.

        """
        try:
            self.banner(f'Create new organization: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            response, org_name = raiden_helper.create_org(global_variables.config, role)
            Report.logInfo(f'Created organization {org_name}')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status = raiden_validation_methods.validate_org_response(
                response, role, org_name
            )
            assert status is True, 'Error in status'
            return response, status

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_org(self, role, org_id):
        """Update an organization

            Setup:
                Sign in with valid system admin credentials.

            Test:
                1. Validate that the super admin can update an organization.
                2. Validate that org admin and org member cannot update the organization.
                3. Create New Org
                POST ~/org
                4. Validate that Super Admin can update the org.
                GET ~/org/{id}
                5. Validate that other org roles get forbidden error.

        """
        try:
            self.banner(f'Update the name of organization: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            response, updated_org_name = raiden_helper.update_org(global_variables.config, role, org_id)
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status = raiden_validation_methods.validate_org_response(
                response, role, updated_org_name
            )
            assert status is True, 'Error in status'
            return response, status

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_org(self, role, org_id):
        """
        Delete organization
        """
        try:
            self.banner(f'Delete organization: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            response = raiden_helper.delete_org(global_variables.config, self.token, org_id)
            status = raiden_validation_methods.validate_empty_response(response)
            assert status is True, 'Error in status'
            return response, status

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_count_of_all_orgs(self, role):
        """Get count of all organizations.

            Setup:
                Sign in with valid system admin credentials.

            Test:
                Test Case to get count of all organizations using the Algolia API.

        """
        try:
            self.banner(f'Get count of orgs using algolia- {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            session_context = raiden_helper.get_session_context(
                global_variables.config, self.token
            )
            Report.logInfo(f'Getting the Session Context {session_context}')
            alg_obj = RaidenAlgolia(session_context['search'])
            _num_of_orgs = alg_obj.algolia_list_of_orgs
            self.assertNotEqual(
                _num_of_orgs, 0, f'Number of orgs: {_num_of_orgs}',
            )
            if _num_of_orgs > 0:
                Report.logPass(f"Number of orgs - {_num_of_orgs}")
            else:
                Report.logFail('Error in getting count of orgs')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_count_of_all_orgs_using_raiden_api(self, role):
        """Get Count of all organizations using raiden API.

            Setup:
                Sign in with valid system admin credentials.

            Test:
                Test Case to get count of all orgs using Raiden API.

        """
        try:
            self.banner(f'Get count of orgs using raiden api- {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            response = raiden_helper.get_orgs(global_variables.config, role)
            status = raiden_validation_methods.validate_valid_get_orgs_response(response)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_user(self, role: str, user: str):
        """
        Add user
        """
        try:
            Report.logInfo(f'Add user: {user} logging in as: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            adduser_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(self.org_id) + '/role'
            user_id, email = raiden_user_helper.add_user(role=role, usertype=user,
                                                         adduser_url=adduser_url,
                                                         token=self.token)
            return user_id, email

        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_user(self, role: str, user: str, email_user: str):
        """
        Add user
        """
        try:
            Report.logInfo(f'{role}-View the user {user}')
            self.token = raiden_helper.signin_method(global_variables.config, 'OrgAdmin')
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_get_user = raiden_user_helper.get_user(global_variables.config, email_user,
                                                          self.org_id, self.token, role, user)
            assert status_get_user is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_user(self, role: str, user: str, usertype_from, usertype_to):
        """
        Update user
        """
        try:
            Report.logInfo(f'{role}-Update the role of user-{user}')
            self.token = raiden_helper.signin_method(global_variables.config, 'OrgAdmin')
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            updateuser_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/role/update'
            status_update_user = raiden_user_helper.update_user_role(usertype_from, usertype_to, updateuser_url,
                                                                     user, self.token)
            assert status_update_user is True, 'Error in status'
        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_user(self, role, user_role, user_id):
        try:
            Report.logInfo(
                f'{role}-Delete the user {user_role} with user id: {user_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            delete_user_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + "/role/delete"
            response_delete_user = raiden_user_helper.delete_user_role(user_id, delete_user_url, self.token)
            json_formatted_response = json.dumps(response_delete_user, indent=2)
            Report.logResponse(format(json_formatted_response))

            for obj in response_delete_user:
                user_id = obj['userId']
                if obj['userId'] == user_id:
                    Report.logPass(f'User with user id {user_id} is deleted successfully')
                else:
                    Report.logFail('Something went wrong with the delete users')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_Provision_New_Room(self, role, room_name):
        try:
            Report.logInfo(f'{role} -  Provisioning a new room')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            _initprov_url = (
                    global_variables.config.BASE_URL
                    + raiden_config.ORG_ENDPNT
                    + str(self.org_id)
                    + '/prov'
            )
            init_prov_payload = {'room': room_name}
            response = raiden_helper.send_request(
                method='POST', url=_initprov_url, body=init_prov_payload, token=self.token)
            Report.logInfo(f'{role} - Initiate Room Provisioning request with Name: {room_name}')
            Report.logInfo('Response- Initiate Room Provisioning')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))

            init_prov_response = response['completion']
            _complete_prov_url = init_prov_response['url']
            complete_prov_payload = {
                'completion': init_prov_response,
                'device': {
                    "type": "Computer",
                    "name": room_name,
                    "make": "Apple",
                    "model": "Apple Mac mini",
                    "proc": "Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz",
                    "ram": "16 GB",
                    "os": "macOS",
                    "osv": "Version 10.16 (Build 20D91)",
                    "sw": "2.4.356",
                    "ip": "10.0.1.23"
                }
            }
            Report.logInfo(f'{role}: Complete Provisioning Request {complete_prov_payload}')
            complete_prov_response = raiden_helper.send_request(
                method='POST', url=_complete_prov_url, body=json.dumps(complete_prov_payload), token=self.token,
            )
            Report.logInfo('Complete Room Provisioning')
            json_formatted_response = json.dumps(complete_prov_response, indent=2)
            Report.logResponse(format(json_formatted_response))

            status, room_id = raiden_validation_methods.validate_prov_new_room(
                role, complete_prov_response, room_name,
            )
            assert status is True, 'Error in status'
            return room_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Appliance_Provisioning(self, role, room_name, on_name_conflict='Fail', max_occupancy=6):
        try:
            Report.logInfo(f'{role} - Initiate appliance provisioning')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            appliance_init_prov_payload = {
                "serial": str(raiden_helper.random_string_generator()),
                "room": room_name,
                "onNameConflict": on_name_conflict,
                "occupancyMode": "Disabled",
                "maxOccupancy": max_occupancy,
                "ttl": 20
            }
            init_prov_url = (
                    global_variables.config.BASE_URL
                    + raiden_config.ORG_ENDPNT
                    + str(self.org_id)
                    + "/appliance/prov"
            )
            Report.logInfo(f'Initiate Provisioning URL is: {init_prov_url}')
            response = raiden_helper.send_request(
                method="POST", url=init_prov_url, body=json.dumps(appliance_init_prov_payload), token=self.token
            )
            Report.logInfo(
                f'{role}: Initiate Appliance Provisioning request with payload: {appliance_init_prov_payload}')

            Report.logInfo(f'{role} - Response received after initiating provisioning: {response}')

            Report.logInfo('Initiate Room Provisioning')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))

            # Step2: Complete Provisioning for an appliance
            provision_id = response["url"].split('/')[6]
            log.debug(f'Provisioning Id that is extracted from the response of initiate provisioning is {provision_id}')
            device_type = "Kong"
            device_name = "Rally Bar"
            complete_prov_url = (
                    global_variables.config.BASE_URL
                    + "/api/appliance/prov/"
                    + str(provision_id)
                    + "/complete"
            )
            Report.logInfo(f'Complete provisioning URL: {complete_prov_url}')
            complete_prov_payload = {
                "device": {
                    "type": str(device_type),
                    "name": str(device_name),
                    "make": "Logitech",
                    "model": "Kong 1.0",
                    "proc": "Snapdragon",
                    "ram": "32 GB",
                    "os": "Android",
                    "osv": "10.0.138",
                    "sw": "10.0.138",
                    "ip": "10.0.1.23"
                }
            }
            Report.logInfo(
                f"{role}: Complete Provisioning Request Payload {complete_prov_payload}")
            response = raiden_helper.send_request(
                method="POST", url=complete_prov_url, body=json.dumps(complete_prov_payload)
            )
            Report.logInfo(
                f"{role} Complete Provisioning Response:  {response['room']}")
            Report.logInfo('Complete Room Provisioning')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status, room_id = raiden_validation_methods. \
                validate_complete_provisioning_appliance(role, response, appliance_init_prov_payload["room"],
                                                         appliance_init_prov_payload["maxOccupancy"],
                                                         on_name_conflict='Fail')
            assert status is True, 'Error in status'
            return room_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_List_of_All_Org_Rooms(self, role):
        """List all rooms in organization.

            Setup:
                Sign in with valid org admin credentials.

            Test:
                Test Case to Org Admin Getting a list of All Orgs Rooms using the Algolia API.

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            session_context = raiden_helper.get_session_context_filter_by_orgid(
                global_variables.config, self.token, self.org_id,
            )
            Report.logInfo(f'Getting the Session Context {session_context}')
            alg_obj = RaidenAlgolia(session_context['search'])
            _num_of_rooms = alg_obj.algolia_list_of_rooms.__len__()
            self.assertNotEqual(
                _num_of_rooms, 0, f'Num of Rooms in Orgs is {_num_of_rooms}',
            )
            if _num_of_rooms > 0:
                Report.logPass(f"Count of rooms - {_num_of_rooms}")
            else:
                Report.logFail('Error in getting count of rooms')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Owner_List_of_all_Org_Users(self, role):
        """Org Admin: List all organization users

            Setup:
                Sign in with valid org admin credentials.

            Test:
                Test Case to Org Admin Getting a list of All Org Users using the Algolia API.

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            # getting the session context for getting algolia related data
            session_context = raiden_helper.get_session_context_filter_by_orgid(
                global_variables.config, self.token, self.org_id
            )
            Report.logInfo(f'Getting the Session Context {session_context}')
            alg_obj = RaidenAlgolia(session_context['search'])
            _num_of_roles = alg_obj.algolia_list_of_users.__len__()
            self.assertNotEqual(
                _num_of_roles, 0, f'Num of Users in Orgs is {_num_of_roles}',
            )
            if _num_of_roles > 0:
                Report.logPass(f"Count of rooms - {_num_of_roles}")
            else:
                Report.logFail('Error in getting count of users')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_empty_room(self, role, room_name):
        """
        Add empty room
        """
        try:
            Report.logInfo(f'Adding empty room with room name {room_name}')
            self.token = raiden_helper.signin_method(global_variables.config, 'OrgAdmin')
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.add_empty_room(room_name, 6, self.org_id, self.token)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_empty_room(self, role, room_name):
        """
        Delete empty room
        """
        try:
            Report.logInfo(f'Adding empty room with room name {room_name}')
            self.token = raiden_helper.signin_method(global_variables.config, 'OrgAdmin')
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.delete_room(room_name, self.org_id, self.token)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_device(self, role: str, room_name: str, device_name: str):
        """Method to get information associated with device.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Brio is connected to Sync Portal organization

            Test:
                 1. Query the API: Get Device
                 GET ~/org/{org-id}/room/{room-id}/device/{device-id}
                 2. Device details should appear and the health should be No Issues.

        """
        try:
            self.banner(f'Get Device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            response_get_device = raiden_helper.get_device(self.org_id, device_name, self.device_id, self.token)
            status = raiden_validation_methods.validate_get_device(response_get_device)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_firmware_update(self, room_name, role, device_name):
        """
        Method to update firmware for device and verify firmware update is successful

        :param room_name:
        :param role:
        :param device_name:
        :return :
        """
        try:
            self.banner(f'Firmware Update: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id, room_name,
                                                               self.token)
            retries = 18
            for _ in range(retries):
                if self.device_id is None:
                    time.sleep(10)
                    self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                                self.org_id, self.token, device_name)
                else:
                    break
            if device_name in ('Kong', 'Diddy', 'Atari', 'Nintendo', 'Sega', 'Tiny'):
                raiden_helper.set_update_channel_via_adb(device_name)

            update_status = raiden_helper.firmware_update_availability_check(org_id=self.org_id, room_id=room_id,
                                                                             device_id=self.device_id,
                                                                             device_type=device_name,
                                                                             token=self.token)

            # Update Status is 1 when update is available, 2 when update is in pending state,
            # 4 when update is in downloading state, 6 when update is in progress,
            # 8 when update is failed and 0 when up-to-date.
            # More details related to Update Status is available in
            # https://docs.google.com/document/d/1CsTIuCDEu1eiddFXLFBPI1VH2FHqs547CZAwRpeeSLw/edit#heading=h.x8kk2wprgnen
            if update_status == 1 or update_status == 8:
                Report.logPass("Firmware update is available.")
                # Trigger firmware update
                raiden_helper.trigger_firmware_update_via_sync_portal(org_id=self.org_id, device_id=self.device_id,
                                                                      device_type=device_name, token=self.token)

                timer = 100 if device_name in (
                    'Kong', 'HostedKong', 'Diddy', 'HostedDiddy', 'Sega', 'Atari', 'Nintendo',
                    'Tiny', 'HostedTiny', 'Sentinel') else 50
                while timer > 0:
                    timer -= 1
                    update_status = raiden_helper.check_update_status_of_device(org_id=self.org_id, room_id=room_id,
                                                                                device_type=device_name,
                                                                                token=self.token)
                    if update_status == 0:
                        Report.logPass("Firmware Update is complete")
                        break
                    elif update_status == 8:
                        Report.logFail('Firmware update failed')
                        break
                    time.sleep(36)
                if update_status == 1:
                    Report.logFail('Update is still in available state')
                elif update_status == 2:
                    Report.logFail('Update is still in pending state')
            else:
                Report.logFail("Firmware Update is not available")

        except Exception as e:
            Report.logException(str(e))

    def tc_add_room_note(self, role: str, room_name: str, room_note: str):
        """Add Room note.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Auto-EmptyRoom room is available in the organization.

            Test:
                 1. Query the API to add room note providing data.
                 POST ~/org/{org-id}/room/{room-id}/note
                 2. Room note should get added to the room.

        """
        try:
            self.banner('Add Room Note')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id, room_name,
                                                               self.token)
            response = raiden_helper.post_room_note(self.org_id, room_id, room_note, self.token)
            status = raiden_validation_methods.validate_room_note_is_present(response, room_note)
            assert status is True, 'Error in status'
            return room_note

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_room_note(self, role: str, room_name: str, room_note: str):
        """Update Room note.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Auto-EmptyRoom room is available in the organization: VC-AUTOINFRA.

            Test:
                 1. Query the API to update room note providing data.
                 POST ~/org/{org-id}/room/{room-id}/note
                 2. Room note should get updated.

        """
        try:
            self.banner('Update Room Note')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id, room_name,
                                                               self.token)
            response = raiden_helper.post_room_note(self.org_id, room_id, room_note, self.token)
            status = raiden_validation_methods.validate_room_note_is_present(response, room_note)
            assert status is True, 'Error in status'
            return room_note

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_room_note(self, role: str, room_name: str):
        """Delete Room note.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Auto-EmptyRoom room is available in the organization

            Test:
                 1. Query the API to update room note providing data.
                 Delete ~/org/{org-id}/room/{room-id}/note
                 2. Room note should get deleted.

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id, room_name,
                                                               self.token)
            response = raiden_helper.delete_room_note(org_id=self.org_id, room_id=room_id, token=self.token)
            status = raiden_validation_methods.validate_room_note_is_deleted(response)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_provision_device_in_appliance_mode_to_sync_portal(self, role, device_name, room_name, env):
        """
        Provision device in appliance mode to Sync portal via Local Network Access
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=env)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            self.lna = LNASyncAppMethods()

            browser = BrowserClass()
            browser.close_all_browsers()
            prov_code, room_id = raiden_helper.add_empty_room(room_name, 6, self.org_id, self.token)
            lna_ip = ''
            if device_name == 'Kong':
                lna_ip = fp.KONG_IP
            elif device_name == 'Diddy':
                lna_ip = fp.DIDDY_IP
            elif device_name == 'Sega':
                lna_ip = fp.SEGA_IP
            elif device_name == 'Atari':
                lna_ip = fp.ATARI_IP
            elif device_name == 'Nintendo':
                lna_ip = fp.NINTENDO_IP
            elif device_name == 'Tiny':
                lna_ip = fp.TINY_IP
            provision_code = ''
            for char in prov_code:
                if char != '-':
                    provision_code += char
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=lna_ip,
                                                                       user_name=fp.LNA_USERNAME,
                                                                       password=fp.LNA_PASSWORD,
                                                                       provision_code=provision_code)
            time.sleep(30)
            return room_id

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_room(self, role, room_name):
        """
        Delete meeting room from Sync Portal
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.delete_room(room_name, self.org_id, self.token)
        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_RS1_to_OnCallStart(self, role, room_name, device_name):
        """Change RightSight to on call start
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to the organization.

            Test:
                  Change the rightsight to on call start.

        """
        try:
            self.banner(f'Change RightSight to On Call Start: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            rs_setting = str('at-call-start')
            self.data = {'rightSight': {'on': 1, 'mode': 1}}
            status = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_setting, self.data,
                                                             self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_RS1_Change_RightSight_Turn_Off(self, role, room_name, device_name):
        """Turn Off RightSight: Rally Camera
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to the organization.

            Test:
                 Turn Off rightsight.

        """
        try:
            self.banner(f'Turn Off RightSight: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            rs_setting = str('disabled')
            self.data = {'rightSight': {'on': 0}}
            status = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_setting, self.data,
                                                             self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_RS1_Change_RightSight_to_Dynamic(self, role, room_name, device_name):
        """Change rightsight to Dynamic: Rally Camera.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to the organization.

            Test:
                 Change the rightsight to dynamic

        """
        try:
            self.banner(f'Change RightSight to dynamic: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            rs_setting = str('dynamic')
            self.data = {'rightSight': {'on': 1, 'mode': 0}}
            status = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_setting, self.data,
                                                             self.token)
            assert status is True, 'Error in status'

        except AssertionError as e:
            Report.logException(f'{e}')

    def tc_change_rightSight_to_group_view_oncallstart(self, role, room_name, device_name):
        """Change rightsight to on call start.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to the organization.

            Test:
                 1. Change rightsight to on call start abd verify that the change is propagated to the device.
                 3. Verify that the change made to the setting persists after reboot.

        """
        try:
            self.banner(f'Change RightSight to On Call Start: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            rs_mode = str('at-call-start')
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.data = raiden_righsight_helper.get_payload_to_set_group_view_on_call_start(self.system_image_version)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_mode, self.data,
                                                                  self.token)

            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.aicv.rs-mode',
                setting_set_via_portal=rs_mode,
                device=device_name
            )

            # Reboot device.
            raiden_helper.reboot_device(global_variables.config, self.org_id, self.token, device=device_name,
                                        device_id=self.device_id)

            # Validate that the option applied persists after reboot.
            status_reboot = raiden_helper.validate_rs_mode_option_group_view_persistence_after_reboot \
                (self.org_id, self.token, self.data['rightSight'],
                 self.system_image_version, device_name, self.device_id)
            status = status_sync & status_device & status_reboot
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_disable_rightsight(self, role, room_name, device_name):
        """Turn Off RightSight
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to the organization.

            Test:
                  Turn off rightsight and verify that the change is propagated to the device.

        """
        try:
            self.banner(f'Turn Off RightSight: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            rs_mode = str('disabled')
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.data = raiden_righsight_helper.get_payload_to_disable_rightsight(self.system_image_version)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_mode, self.data,
                                                                  self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.aicv.rs-mode',
                setting_set_via_portal=rs_mode,
                device=device_name
            )
            status = status_sync and status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_RightSight2_Speaker_tracking_mode_Speaker_View_Picture_in_Picture_enabled(self, role, room_name,
                                                                                            device_name):
        """Change rightsight 2 Speaker tracking mode to Speaker View.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to sync portal.

            Test:
                 Change RightSight 2 Speaker Tracking Mode to Speaker View and enable Picture in picture.

        """
        try:
            self.banner(f'Change RightSight 2 Speaker Tracking Mode to Speaker View: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            rs_mode = str('speaker-tracking-pip')

            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)

            if self.system_image_version >= float(912.97):
                if self.system_image_version < float(914.303):
                    self.data = {'rightSight': {'on': 1, 'pip': True, 'trackingMode': 1, 'version': 2}}
                else:
                    self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "groupFramingSpeed": 1,
                                                "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 4}}

                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_sync = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_mode, self.data,
                                                                      self.token)
                status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.rs-mode',
                    setting_set_via_portal=rs_mode,
                    device=device_name
                )
                status = status_sync & status_device
                assert status is True, 'Error in status'

            else:
                Report.logPass('System Image is less than 0.912.97. '
                               'So, the speaker tracking mode: Speaker View is not available.')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_RS2_Speaker_tracking_mode_Speaker_View_Picture_in_picture_disabled(self, role, room_name,
                                                                                     device_name):
        """Change rightsight 2 Speaker tracking mode to Speaker View and turn off Picture in picture.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to sync portal.

            Test:
                 Change the speaker tracking mode to Speaker View and turn off picture in picture.

        """
        try:
            self.banner(f'Change RightSight 2 Speaker Tracking Mode to Speaker View & turn off Picture in picture: '
                        f'{device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            rs_mode = str('speaker-tracking-pip')

            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)

            if self.system_image_version >= float(912.97):
                if self.system_image_version < float(914.303):
                    self.data = {'rightSight': {'on': 1, 'pip': False, 'trackingMode': 1, 'version': 2}}
                else:
                    self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": False, "groupFramingSpeed": 1,
                                                "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 4}}

                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_sync = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_mode, self.data,
                                                                      self.token)
                status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.rs-mode',
                    setting_set_via_portal=rs_mode,
                    device=device_name
                )
                status = status_sync & status_device
                assert status is True, 'Error in status'

            else:
                Report.logPass('System Image is less than 0.912.97. '
                               'So, the speaker tracking mode: Speaker View is not available.')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_RightSight_Group_view_set_to_Dynamic(self, role, room_name, device_name):
        """Change rightsight to Dynamic.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to sync portal.

            Test:
                Change the rightsight to dynamic.

        """
        try:
            self.banner(f'Change RightSight to dynamic: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            rs_mode = str('dynamic')
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)

            if self.system_image_version < float(912.97):
                self.data = {'rightSight': {'on': 1, 'mode': 0}}
            elif self.system_image_version < float(914.303):
                self.data = {'rightSight': {'on': 1, 'mode': 0, 'trackingMode': 0, 'version': 2}}
            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "groupFramingSpeed": 1,
                                            "speakerFramingSpeed": 1,
                                            "speakerDetectionSpeed": 1, "version": 4}}

            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_rightsight_setting(self.org_id, self.device_id, rs_mode, self.data,
                                                                  self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.aicv.rs-mode',
                setting_set_via_portal=rs_mode,
                device=device_name
            )
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Disable_AI_Noise_Suppression(self, role, room_name, device_name):
        """Disable AI noise suppression.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to sync portal.

            Test:
                 Disable AI Noise Suppression.

        """
        try:
            self.banner(f'Disable AI Noise Suppression of {device_name}')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 0, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.noise-reduction', setting_set_via_portal='0', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Enable_AI_Noise_Suppression(self, role, room_name, device_name):
        """Enable AI noise suppression.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Enable AI Noise Suppression.

        """
        try:
            self.banner(f'Enable AI Noise Suppression for {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.noise-reduction', setting_set_via_portal='1', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Enable_Speaker_Boost(self, role, room_name, device_name):
        """Enable AI noise suppression
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Enable Speaker Boost.

        """
        try:
            self.banner(f'Enable Speaker Boost for {device_name}')
            self.data = {'audioSettings': {'speakerBoost': 1, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.speaker-boost', setting_set_via_portal='1', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Disable_Speaker_Boost(self, role, room_name, device_name):
        """Disable Speaker Boost
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Disable Speaker Boost.
        """
        try:
            self.banner(f'Disable Speaker Boost for {device_name}')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.speaker-boost', setting_set_via_portal='0', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Disable_Reverb_Control(self, role, room_name, device_name):
        """Disable Reverb Control
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Disable Reverb Control.

        """
        try:
            self.banner(f'Disable Reverb control for {device_name}')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 0, 'micEQ': 1,
                                           'speakerEQ': 1}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_reverb_mode = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.reverb-reduction',
                setting_set_via_portal='DISABLED',
                device=device_name
            )
            status = status_sync & status_reverb_mode
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Enable_Reverb_Control_Aggressive(self, role, room_name, device_name):
        """Enable Reverb Control to Aggressive.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Enable reverb control to aggressive.
        """
        try:
            self.banner(f'Enable Reverb control to Aggressive for {device_name}')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 3, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_reverb_mode = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.reverb-reduction',
                setting_set_via_portal='AGGRESSIVE',
                device=device_name
            )
            status = status_sync & status_reverb_mode
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Enable_Reverb_Control_Normal(self, role, room_name, device_name):
        """Enable Reverb Control to Normal.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Enable reverb control to Normal.

        """
        try:
            self.banner(f'Enable Reverb control to Normal for {device_name}')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_reverb_mode = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.reverb-reduction',
                setting_set_via_portal='NORMAL',
                device=device_name
            )
            status = status_sync & status_reverb_mode
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Turn_Off_Bluetooth(self, role, room_name, device_name):
        """Turn Off Bluetooth
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Turn Off Bluetooth.

        """
        try:
            self.banner(f'Turn Off Bluetooth: {device_name}')
            self.data = {'bt': {'on': 0}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status = raiden_helper.change_bluetooth_setting(self.org_id, self.device_id, self.data, self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Turn_On_Bluetooth(self, role, room_name, device_name):
        """Turn on Bluetooth
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Turn On Bluetooth.

        """
        try:
            self.banner(f'Turn On Bluetooth: {device_name}')
            self.data = {'bt': {'on': 1}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status = raiden_helper.change_bluetooth_setting(self.org_id, self.device_id, self.data, self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Microphone_EQ_Bass_Boost(self, role, room_name, device_name):
        """Set Microphone EQ to Bass Boost.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Microphone EQ to Bass boost.

        """
        try:
            self.banner(f'Set Microphone EQ of {device_name} to Bass Boost.')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 0,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.mic-eq-preset', setting_set_via_portal='0', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Microphone_EQ_Voice_Boost(self, role, room_name, device_name):
        """Set Microphone EQ to Voice Boost.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Microphone EQ to Voice boost.

        """
        try:
            self.banner(f'Set Microphone EQ of {device_name} to Voice Boost.')
            micEq = 2
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': micEq,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_mic_eq = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.mic-eq-preset',
                setting_set_via_portal=micEq,
                device=device_name
            )
            status = status_sync & status_mic_eq
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Microphone_EQ_Normal(self, role, room_name, device_name):
        """Set Microphone EQ to Normal.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Microphone EQ to Normal.

        """
        try:
            self.banner(f'Set Microphone EQ of {device_name} to Normal.')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.mic-eq-preset', setting_set_via_portal='1', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Speaker_EQ_Bass_Boost(self, role, room_name, device_name):
        """Set Speaker EQ to Bass Boost.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Speaker EQ to Bass boost.

        """
        try:
            self.banner(f'Set Speaker EQ of {device_name} to Bass Boost.')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 0}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.speaker-eq-preset', setting_set_via_portal='0', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Speaker_EQ_Voice_Boost(self, role, room_name, device_name):
        """Set Speaker EQ to Voice Boost.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Speaker EQ to Voice boost.

        """
        try:
            self.banner(f'Set Speaker EQ of {device_name} to Voice Boost.')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 2}}
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.speaker-eq-preset', setting_set_via_portal='2', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Speaker_EQ_Normal(self, role, room_name, device_name):
        """Set Speaker EQ to Normal.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Speaker EQ to Normal.

        """
        try:
            self.banner(f'Set Speaker EQ of {device_name} to Normal.')
            self.data = {'audioSettings': {'speakerBoost': 0, 'noiseReduction': 1, 'deReverbMode': 2, 'micEQ': 1,
                                           'speakerEQ': 1}}

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            status_sync = raiden_helper.change_audio_settings(self.org_id, self.device_id, self.data, self.token)
            status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.speaker-eq-preset', setting_set_via_portal='1', device=device_name)
            status = status_sync & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_GroupView_Framing_Speed_To_Slower(self, role, room_name, device_name):
        """Change Group View Framing speed to Slower.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set Group View framing speed to Slower.
                 2. Validate that the setting is applied to the device.
                 3. Validate the persistence of setting after reboot.

        """
        try:
            self.banner(f'Change Group View Framing speed of {device_name} to Slower.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            setting_name = 'Group View - Framing Speed'
            setting_value = 'slower'
            if self.system_image_version < float(914.260):
                log.info('Framing speed option is not available for system image version- {}'.format(
                    self.system_image_version))
                status = True

            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 1, "version": 4}}

                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_sync = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)
                status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.reaction-speed', setting_set_via_portal='slower', device=device_name)
                raiden_helper.reboot_device(global_variables.config, self.org_id, self.token, device=device_name,
                                            device_id=self.device_id)
                status_persistence = raiden_helper.validate_setting_preservation_after_reboot(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='groupFramingSpeed', expected_setting=0)
                status = status_sync & status_device & status_persistence
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_GroupView_Framing_Speed_To_Default(self, role, room_name, device_name):
        """Change Group View Framing speed to Default.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Group view framing to default and verify that the setting is propagated to device.

        """
        try:
            self.banner(f'Change Group View Framing speed of {device_name} to Default.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            setting_name = 'Group View - Framing Speed'
            setting_value = 'default'
            if self.system_image_version < float(914.260):
                log.info('Framing speed option is not available for system image version- {}'.format(
                    self.system_image_version))
                status = True

            else:
                self.data = raiden_righsight_helper.get_payload_to_set_group_view_and_framing_speed_to_default(
                    self.system_image_version)

                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_sync = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)
                status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.reaction-speed', setting_set_via_portal='default', device=device_name)

                status = status_sync and status_device

            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_GroupView_Framing_Speed_To_Faster(self, role, room_name, device_name):
        """Change Group View Framing speed to Faster.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set Group view framing to Faster and verify that the setting is propagated to device.

        """
        try:
            self.banner(f'Set the Group View Framing Speed to Faster: {device_name}')
            setting_name = 'Group View - Framing Speed'
            setting_value = 'faster'
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            if self.system_image_version < float(914.260):
                log.info('Framing speed option is not available for system image version- {}'.format(
                    self.system_image_version))
                status = True

            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                            "groupFramingSpeed": 2, "speakerFramingSpeed": 1, "version": 4}}

                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_sync = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)
                # Validate that the framing speed got applied to the device
                status_device = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.reaction-speed', setting_set_via_portal='faster', device=device_name)

                status = status_sync & status_device

            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Switch_from_Group_View_Framing_Speed_Slower_To_Speaker_View_Framing_Speed_Default(self, role, room_name,
                                                                                             device_name):
        """When switching from group view with framing speed as slower to speaker view, framing speed should set back to
        default
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set the speaker tracking mode to Group View and framing speed to Slower.
                 2. Switch from group view to speaker view.
                 3. Verify that speaker tracking mode is set to Speaker view and Framing speed is set to Default in
                 Sync portal.

        """
        try:
            self.banner('When switching from group view with framing speed as slower to speaker view, framing speed '
                        f'should set back to default: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            if self.system_image_version < float(914.260):
                log.info('Framing speed & speaker detection options are not available for system image version- {}'.
                         format(self.system_image_version))
                status = True

            else:
                # Set the speaker tracking mode to group view and framing speed to Slow.
                rs_setting = 'Group View with framing speed-Slow'
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "speakerDetectionSpeed": 1,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 1, "version": 4}}
                status_response_group_view = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Set the speaker tracking mode to speaker view.
                rs_setting = 'Speaker View'
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 1,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 1, "version": 4}}
                status_response_speaker_view = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                status_default_values_speaker_tracking_mode = raiden_helper. \
                    validate_expected_setting_rightsight(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='trackingMode', expected_setting=1)
                status_default_values_framingspeed = raiden_helper. \
                    validate_expected_setting_rightsight(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='speakerFramingSpeed', expected_setting=1)
                status = status_response_group_view & status_response_speaker_view & \
                         status_default_values_speaker_tracking_mode & \
                         status_default_values_framingspeed
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Slower(self, role, room_name,
                                                                                device_name):
        """Change Speaker View Framing speed to Default and speaker detection to Slower.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set speaker tracking mode to Speaker VIew, Framing speed to Default and
                 Speaker Detection to Slower.

        """
        try:
            self.banner(f'Change Speaker View Framing speed to Default and speaker '
                        f'detection to Slower- {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            if self.system_image_version < float(914.260):
                log.info('Framing speed & speaker detection options are not available for system image version- {}'.
                         format(self.system_image_version))
                status = True

            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 0,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 1, "version": 4}}
                # Speaker View, Framing Speed - Default and Speaker Detection - Slower
                rs_setting = 'Speaker View, Framing Speed - Default & Speaker Detection - Slower'
                self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                            self.org_id, self.token, device_name)
                status_response = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                # Validate that the framing speed and speaker detection got applied to the device
                status_device_framing_speed = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed', setting_set_via_portal='default',
                    device=device_name)
                status_device_speaker_detection = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed', setting_set_via_portal='slower',
                    device=device_name)
                status_device = status_device_framing_speed & status_device_speaker_detection
                # Reboot device.
                raiden_helper.reboot_device(global_variables.config, self.org_id, self.token, device=device_name,
                                            device_id=self.device_id)

                # Validate that the option applied persists after reboot.
                status_persistence_framingSpeed = raiden_helper. \
                    validate_setting_preservation_after_reboot(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='speakerFramingSpeed',
                    expected_setting=1)
                status_persistence_speaker_detection = raiden_helper. \
                    validate_setting_preservation_after_reboot(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='speakerDetectionSpeed',
                    expected_setting=0)
                status_persistence = status_persistence_framingSpeed & status_persistence_speaker_detection
                status = status_response & status_device & status_persistence
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_SpeakerView_Framing_Speed_To_Default_Speaker_Detection_To_Faster(self, role, room_name,
                                                                                device_name):
        """Change Speaker View Framing speed to Default and speaker detection to Faster.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set speaker tracking mode to Speaker VIew, Framing speed to Default and Speaker Detection to Faster.

        """
        try:
            self.banner(f'Change Speaker View Framing speed of {device_name} to Default and speaker detection to '
                        f'Faster.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            if self.system_image_version < float(914.260):
                log.info(
                    'Framing speed & speaker detection options are not available for system image version- {}'.format(
                        self.system_image_version))
                status = True

            else:
                rs_setting = 'Speaker view, framing speed to Default and speaker detection to Faster'
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 2,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 1, "version": 4}}
                status_response = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                # Validate that the framing speed and speaker detection got applied to the device
                status_device_framing_speed = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed', setting_set_via_portal='default',
                    device=device_name)
                status_device_speaker_detection = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed', setting_set_via_portal='faster',
                    device=device_name)
                status_device = status_device_framing_speed & status_device_speaker_detection
                status = status_response & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_SpeakerView_Framing_Speed_To_Slow_Speaker_Detection_To_Slower(self, role, room_name,
                                                                             device_name):
        """Change Speaker View Framing speed to Slower and speaker detection to Slower.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set speaker tracking mode to Speaker VIew, Framing speed to Slow and Speaker Detection to Slow.

        """
        try:
            self.banner(f'Change Speaker View Framing speed of {device_name} to Slow and speaker detection to Slower.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            if self.system_image_version < float(914.260):
                log.info('Framing speed option is not available for system image version- {}'.format(
                    self.system_image_version))
                status = True

            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 0,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 0, "version": 4}}
                rs_setting = 'Speaker view, framing speed to Slower and speaker detection to Slower'
                status_response = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Validate that the framing speed and speaker detection got applied to the device
                status_device_framing_speed = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed', setting_set_via_portal='slower',
                    device=device_name)
                status_device_speaker_detection = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed', setting_set_via_portal='slower',
                    device=device_name)
                status_device = status_device_framing_speed & status_device_speaker_detection
                status = status_response & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_SpeakerView_Framing_Speed_To_Slower_Speaker_Detection_To_Default(self, role, room_name,
                                                                                device_name):
        """Change Speaker View Framing speed to Slower and speaker detection to Default.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set speaker tracking mode to Speaker View, Framing speed to Slow and Speaker Detection to Slower.

        """
        try:
            self.banner(
                f'Change Speaker View Framing speed of {device_name} to Slower and speaker detection to Default.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            if self.system_image_version < float(914.260):
                Report.logInfo(
                    'Framing speed & speaker detection options are not available for system image version- {}'.format(
                        self.system_image_version))
                status = True

            else:
                self.data = raiden_righsight_helper.\
                    get_payload_to_set_speaker_view_framing_speed_to_slower_speaker_detection_to_default\
                    (self.system_image_version)

                rs_setting = 'Speaker view framing speed to Default and speaker detection to Faster'
                status_response = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                # Validate that the framing speed and speaker detection got applied to the device
                status_device_framing_speed = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed', setting_set_via_portal='slower',
                    device=device_name)
                status_device_speaker_detection = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed', setting_set_via_portal='default',
                    device=device_name)
                status_device = status_device_framing_speed & status_device_speaker_detection
                status = status_response and status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Set_SpeakerView_Framing_Speed_To_Faster_Speaker_Detection_To_Faster(self, role, room_name,
                                                                               device_name):
        """Change Speaker View Framing speed to Faster and speaker detection to Faster.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Set speaker tracking mode to Speaker VIew, Framing speed to Faster and Speaker Detection to Faster.

        """
        try:
            self.banner(
                f'Change Speaker View Framing speed of {device_name} to Faster and speaker detection to Faster.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            if self.system_image_version < float(914.260):
                log.info(
                    'Framing speed & speaker detection options are not available for system image version- {}'.format(
                        self.system_image_version))
                status = True

            else:
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "pip": True, "speakerDetectionSpeed": 2,
                                            "groupFramingSpeed": 0, "speakerFramingSpeed": 2, "version": 4}}
                rs_setting = 'Speaker view framing speed to Default and speaker detection to Faster'
                status_response = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                # Validate that the framing speed and speaker detection got applied to the device
                status_device_framing_speed = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed', setting_set_via_portal='faster',
                    device=device_name)
                status_device_speaker_detection = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed', setting_set_via_portal='faster',
                    device=device_name)
                status_device = status_device_framing_speed & status_device_speaker_detection
                status = status_response & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Disable_Enable_RightSight_Verify_Group_View_Framing_Speed_Default(self, role, room_name,
                                                                             device_name):
        """Disable and enable the RightSight2 and verify that the speaker tracking mode is Group View &
        Framing speed is set to Default
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Turn off rightsight.
                 2. Turn on rightsight.
                 3. Verify that speaker tracking mode is set to Group View and Framing speed is set to Default.

        """
        try:
            self.banner('Disable and enable the RightSight2 and verify that the speaker tracking mode is Group View & '
                        f'Framing speed is set to Default: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)

            if self.system_image_version < float(914.260):
                Report.logInfo(
                    'Framing speed & speaker detection options are not available for system image version- {}'.format(
                        self.system_image_version))
                status = True

            else:
                # Disable RightSight
                self.data = raiden_righsight_helper.get_payload_to_disable_rightsight(self.system_image_version)
                rs_setting = 'Disabled'
                status_response_off = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Enable Rightsight
                self.data = raiden_righsight_helper.\
                    get_payload_to_set_group_view_and_framing_speed_to_default(self.system_image_version)
                rs_setting = 'Enabled'
                status_response_on = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                status_response = status_response_off & status_response_on
                # Validate that the speaker tracking mode is group view and framing speed is set to Default in
                # Sync Portal.
                status_default_values_speaker_tracking_mode = raiden_helper.validate_expected_setting_rightsight(
                    global_variables.config, self.org_id, self.token, self.device_id, name_of_setting='trackingMode',
                    expected_setting=0)
                status_default_values_framingspeed = raiden_helper.validate_expected_setting_rightsight(
                    global_variables.config, self.org_id, self.token, self.device_id,
                    name_of_setting='groupFramingSpeed',
                    expected_setting=1)
                status = status_response and status_default_values_speaker_tracking_mode and \
                         status_default_values_framingspeed
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Disable_Local_Network_Access(self, role, room_name, device_name, min_version=None):
        """Disable Local Network Access
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Disable local network access.
        """
        try:
            self.banner(f'Disable Local Network Access- {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            setting_name = 'Local Network Access'
            setting_value = 'Disabled'

            # if self.system_image_version < float(914.223):
            if min_version is not None and self.system_image_version < min_version:
                Report.logInfo(f'Disabling Local Network Access via Sync Portal is not available for '
                               f'system image version- {self.system_image_version}')
                status = True
            else:
                # Disable LNA settings.
                self.data = {"lnaSettings": {"on": 0}}
                status = raiden_helper.change_setting(setting_name, setting_value,
                                                      self.org_id, self.device_id, self.data, self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Enable_Local_Network_Access(self, role, room_name, device_name, min_version=None):
        """Enable Local Network Access
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Enable local network access.

        """
        try:
            self.banner(f'Enable Local Network Access- {device_name}')
            setting_name = 'Local Network Access'
            setting_value = 'Enabled'
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            # if self.system_image_version < float(914.223):
            if min_version is not None and self.system_image_version < min_version:
                log.info('Enabling Local Network Access via Sync Portal is not available for system image version- {}'
                         .format(self.system_image_version))
                status = True

            else:
                # Enable LNA settings.
                self.data = {"lnaSettings": {"on": 1}}
                status = raiden_helper.change_setting(setting_name, setting_value,
                                                      self.org_id, self.device_id, self.data, self.token)
            assert status is True, 'Error in status'

        except Exception as e: \
                Report.logException(f'{e}')

    def tc_Change_Password_Local_Network_Access(self, role, room_name, device_name, min_version=None):
        """Change Password of Local Network Access
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 Change password

        """
        try:
            self.banner(f'Change Password of Local Network Access: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)

            if min_version is not None and self.system_image_version < min_version:
                log.info('Disabling Local Network Access via Sync Portal is not available for system image version- {}'
                         .format(self.system_image_version))
                status = True

            else:
                # Change Password
                self.data = {"password": "Logi@3456"}
                status = raiden_helper.change_lna_password(self.org_id, self.device_id, self.data, self.token)

            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_RightSight_Preservation_Of_Settings_RS_Off_On(self, role, room_name, device_name):
        """Rightsight preservation of settings when rightsight is turned off and on
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set the rightsight speaker tracking mode to Speaker view, PIP disabled,speaker detection faster
                 and framing speed as slower.
                 2. Turn off the Rightsight and Turn it on.
                 3. Verify that RS settings are preserved.

        """
        try:
            self.banner(f'Rightsight preservation of settings when rightsight is turned off and on- {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)

            if self.system_image_version < float(915.192):
                log.info('Rightsight preservation of settings feature is not available for '
                         'system image version- {}'.format(self.system_image_version))
                status = True

            else:
                # Set the rightsight speaker tracking mode to Speaker view, PIP disabled,
                # speaker detection faster and framing speed as slower
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "mode": 0, "pip": False,
                                            "groupFramingSpeed": 1, "speakerFramingSpeed": 0,
                                            "speakerDetectionSpeed": 2, "version": 5}}
                rs_setting = 'Speaker view, PIP disabled,speaker detection faster and framing speed as slower'
                status_rs = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Turn off Rightsight
                self.data = {"rightSight": {"on": 0, "trackingMode": 1, "mode": 0, "pip": False, "groupFramingSpeed": 1,
                                            "speakerFramingSpeed": 0, "speakerDetectionSpeed": 2, "version": 5}}
                self.data = {"rightSight": {"on": 0, "groupFramingSpeed": 1, "speakerFramingSpeed": 2,
                                            "speakerDetectionSpeed": 2, "version": 4}}
                rs_setting = 'Disabled'
                status_rs_off = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Turn on rightsight
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "mode": 0, "pip": False,
                                            "groupFramingSpeed": 1, "speakerFramingSpeed": 0,
                                            "speakerDetectionSpeed": 2, "version": 5}}
                rs_setting = 'Enabled'
                status_rs_on = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                time.sleep(45)

                # Validate that the settings are preserved in Sync Portal.
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id, name_of_setting='trackingMode',
                                                                   expected_setting=1)
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id, name_of_setting='pip',
                                                                   expected_setting=False)
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id,
                                                                   name_of_setting='speakerDetectionSpeed',
                                                                   expected_setting=2)

                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id,
                                                                   name_of_setting='groupFramingSpeed',
                                                                   expected_setting=1)

                # Validate that the settings apply to device.
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(name_of_setting='logi.aicv.rs-mode',
                                                                                   setting_set_via_portal='speaker-tracking-pip',
                                                                                   device=device_name)
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(name_of_setting='logi.aicv.pip-mode',
                                                                                   setting_set_via_portal='disabled',
                                                                                   device=device_name)
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.catch-speed',
                    setting_set_via_portal='faster',
                    device=device_name)
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.speaker-tracking-pip.release-speed',
                    setting_set_via_portal='slower',
                    device=device_name)

                # Restore back to default
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "pip": False,
                                            "groupFramingSpeed": 1, "speakerFramingSpeed": 0,
                                            "speakerDetectionSpeed": 2, "version": 5}}

                rs_setting = 'Group View with Dynamic mode and framing speed set to default'
                status_rs_default = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                status = status_rs & status_rs_off & status_rs_on & status_rs_default

            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_RightSight_Preservation_Of_Settings_RS_Switch_between_Group_view_and_Speaker_view(self, role,
                                                                                             room_name, device_name):
        """Rightsight preservation of settings- Switch between group view and speaker view
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set the speaker tracking mode to group view. Set the group view framing to On Call Start and
                 framing speed to faster.
                 2. Switch to speaker view with pip on, speaker detection and framing speed set to default.
                 3. Switch to group view.
                 4. Verify that the group view settings are preserved.
                 5. Reset to default values by setting the group view framing to Dynamic and framing speed
                 to default.

        """
        try:
            self.banner(
                f'Rightsight preservation of settings- Switch between group view and speaker view- {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.system_image_version = raiden_helper.get_system_image_version(org_id=self.org_id,
                                                                               device_name=device_name,
                                                                               room_name=room_name,
                                                                               token=self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)

            if self.system_image_version < float(915.192):
                log.info('Rightsight preservation of settings feature is not available for '
                         'system image version- {}'.format(self.system_image_version))
                status = True

            else:
                # Set the group view framing to On Call Start and framing speed to faster
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "pip": False,
                                            "groupFramingSpeed": 2, "speakerFramingSpeed": 0,
                                            "speakerDetectionSpeed": 2, "version": 5}}

                rs_setting = 'Group view framing to On Call Start and framing speed to faster'
                status_rs = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Switch to speaker view with pip on, speaker detection and framing speed set to default.
                self.data = {"rightSight": {"on": 1, "trackingMode": 1, "mode": 1, "pip": False,
                                            "groupFramingSpeed": 2, "speakerFramingSpeed": 1,
                                            "speakerDetectionSpeed": 1, "version": 5}}
                rs_setting = 'Speaker view with pip on, speaker detection and framing speed set to default'
                status_rs_switch_speaker_view = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)

                # Switch to group view. Verify that the group view settings are preserved.
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 1, "pip": True, "groupFramingSpeed": 2,
                                            "speakerFramingSpeed": 1, "speakerDetectionSpeed": 1, "version": 5}}
                rs_setting = 'Group view'
                status_rs_switch_group_view = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                time.sleep(30)

                # Validate that the settings are preserved in Sync Portal.
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id, name_of_setting='trackingMode',
                                                                   expected_setting=0)
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id, name_of_setting='mode',
                                                                   expected_setting=1)
                raiden_helper.validate_expected_setting_rightsight(global_variables.config, self.org_id, self.token,
                                                                   self.device_id,
                                                                   name_of_setting='groupFramingSpeed',
                                                                   expected_setting=2)

                # Validate that the settings apply to device.
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(name_of_setting='logi.aicv.rs-mode',
                                                                                   setting_set_via_portal='at-call-start',
                                                                                   device=device_name)
                raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                    name_of_setting='logi.aicv.reaction-speed',
                    setting_set_via_portal='faster',
                    device=device_name)

                # Restore back to default
                self.data = {"rightSight": {"on": 1, "trackingMode": 0, "mode": 0, "pip": False,
                                            "groupFramingSpeed": 1, "speakerFramingSpeed": 0,
                                            "speakerDetectionSpeed": 2, "version": 5}}
                rs_setting = 'Group View with Dynamic mode and framing speed set to default'
                status_rs_default = raiden_helper.change_rightsight_setting \
                    (self.org_id, self.device_id, rs_setting, self.data, self.token)
                status = status_rs & status_rs_switch_group_view & status_rs_switch_speaker_view & status_rs_default
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_Swytch_tutorial_via_Sync_Portal(self, role, room_name, device_name):
        """Change BYOD screen to Swytch tutorial
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Change the BYOD screen to Swytch Tutorial.
                 2. Validate that the setting is applied to the device.
                 3. Reboot device.
                 4. Check that the selected option persists after the device reboot.

        """
        try:
            self.banner(f'Change BYOD wallpaper option to Swytch tutorial: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            swytch_tutorial_wallpaper = 2
            self.data = {'byodSettings': {'wallpaper': swytch_tutorial_wallpaper}}

            setting_name = 'BYOD default screen'
            setting_value = 'Swytch tutorial'
            status_response = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)

            # Validate that the setting got applied to the device
            status_device = raiden_helper.validate_device_wallpaper(swytch_tutorial_wallpaper, device=device_name)

            # Reboot device.
            raiden_helper.reboot_device(global_variables.config, self.org_id, self.token, device_name, self.device_id)

            # Validate that the option applied persists.
            status_persistence = raiden_helper. \
                validate_wallpaper_option_persistence_after_reboot(global_variables.config, self.org_id,
                                                                   self.token, swytch_tutorial_wallpaper,
                                                                   device_id=self.device_id)

            status = status_response & status_device & status_persistence
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_Sync_Portal(self, role, room_name, device_name):
        """Change BYOD screen to HDMI & USB-C tutorial
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Change the BYOD screen to HDMI & USB-C tutorial
                 2. Validate that the setting is applied to the device.

        """
        try:
            self.banner(f'Change BYOD wallpaper option to HDMI & USB-C tutorial: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            hdmi_usb_c_wallpaper = 1
            self.data = {'byodSettings': {'wallpaper': hdmi_usb_c_wallpaper}}

            setting_name = 'BYOD default screen'
            setting_value = 'HDMI & USB-C tutorial'
            status_response = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)
            # Validate that the setting got applied to the device
            status_device = raiden_helper.validate_device_wallpaper(hdmi_usb_c_wallpaper, device=device_name)
            status = status_response & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_Custom_via_Sync_Portal(self, role, room_name, device_name):
        """Change BYOD screen to custom
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Change the BYOD screen to Custom
                 2. Validate that the setting is applied to the device.

        """
        try:
            self.banner(f'Change BYOD wallpaper option to Custom: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            custom_wallpaper = 3
            self.data = {'byodSettings': {'wallpaper': custom_wallpaper}}
            setting_name = 'BYOD default screen'
            setting_value = 'Custom'
            status = raiden_helper.change_setting(setting_name, setting_value,
                                                  self.org_id, self.device_id,
                                                  self.data, self.token)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_Sync_Portal(self, role, room_name, device_name):
        """Change BYOD screen to HDMI & USB-A tutorial
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Change the BYOD screen to HDMI & USB-A tutorial
                 2. Validate that the setting is applied to the device.

        """
        try:
            self.banner(f'Change BYOD wallpaper option to HDMI & USB-A tutorial: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            hdmi_usb_a_wallpaper = 0
            self.data = {'byodSettings': {'wallpaper': hdmi_usb_a_wallpaper}}
            setting_name = 'BYOD default screen'
            setting_value = 'HDMI & USB-A tutorial'
            status_response = raiden_helper.change_setting(setting_name, setting_value,
                                                           self.org_id, self.device_id,
                                                           self.data, self.token)

            # Validate that the setting got applied to the device
            status_device = raiden_helper.validate_device_wallpaper(hdmi_usb_a_wallpaper, device=device_name)
            status = status_response & status_device
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_Swytch_tutorial_via_device(self, role, room_name, device_name):
        """Change BYOD screen to Swytch tutorial via device
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set the BYOD wallpaper as Swytch Tutorial via device.
                 2. Check in Sync Portal that the change made is propagate from device to Sync Portal
        """
        try:
            self.banner(f'Change BYOD wallpaper option to Swytch tutorial directly via device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            swytch_tutorial_wallpaper = 2
            # Set the BYOD wallpaper as Swytch Tutorial via device.
            raiden_helper.set_the_wallpaper_via_device(swytch_tutorial_wallpaper, device=device_name)

            # Check in Sync Portal that the change made is propagate from device to Sync Portal
            response = raiden_helper.get_device(self.org_id, device_name, self.device_id, self.token)
            wallpaper_option = int(response['state']['reported']['byodSettings']['wallpaper'])
            status = raiden_helper.validate_byod_wallpaper_option_sync_portal(wallpaper_option,
                                                                              swytch_tutorial_wallpaper)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_HDMI_USB_C_tutorial_via_device(self, role, room_name, device_name):
        """Change BYOD screen to HDMI & USB-C tutorial via device
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1.Set the BYOD wallpaper as HDMI & USB-C tutorial via device.
                 2. Check in Sync Portal that the change made is propagate from device to Sync Portal

        """
        try:
            self.banner(f'Change BYOD wallpaper option to HDMI & USB-C tutorial directly via device:{device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            hdmi_usb_c_tutorial_wallpaper = 1

            # Set the BYOD wallpaper as HDMI & USB-C tutorial via device.
            raiden_helper.set_the_wallpaper_via_device(hdmi_usb_c_tutorial_wallpaper, device=device_name)

            # Check in Sync Portal that the change made is propagate from device to Sync Portal
            response = raiden_helper.get_device(self.org_id, device_name, self.device_id, self.token)
            wallpaper_option = int(response['state']['reported']['byodSettings']['wallpaper'])
            status = raiden_helper.validate_byod_wallpaper_option_sync_portal(wallpaper_option,
                                                                              hdmi_usb_c_tutorial_wallpaper)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_custom_wallpaper_uploaded_using_sync_portal_via_device(self, role, room_name,
                                                                                        device_name):
        """Change BYOD screen to custom wallpaper uploaded via Sync Portal using device
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Send ADB command to the device: adb shell settings put secure byod_mode_preview 3 to change the
                    BYOD screen to custom wallpaper uploaded via Sync Portal.
                 2. Check in Sync Portal that the change made is propagate from device to Sync Portal
                 3. Reboot device.
                 4. Check that the selected option persists after the device reboot.

        """
        try:
            self.banner(f'Change BYOD wallpaper option to custom using device:{device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            custom = 3
            # Set the BYOD wallpaper as HDMI & USB-C tutorial via device.
            raiden_helper.set_the_wallpaper_via_device(custom, device=device_name)

            # Check in Sync Portal that the change made is propagate from device to Sync Portal
            response = raiden_helper.get_device(self.org_id, device_name, self.device_id, self.token)
            wallpaper_option = int(response['state']['reported']['byodSettings']['wallpaper'])
            status = raiden_helper.validate_byod_wallpaper_option_sync_portal(wallpaper_option,
                                                                              custom)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Change_BYOD_Screen_to_HDMI_USB_A_tutorial_via_device(self, role, room_name, device_name):
        """Change BYOD screen to HDMI & USB-A tutorial via device
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is provisioned to Sync Portal.

            Test:
                 1. Set the BYOD wallpaper as HDMI & USB-C tutorial via device.
                 2. Check in Sync Portal that the change made is propagate from device to Sync Portal

        """
        try:
            self.banner(f'Change BYOD wallpaper option to HDMI & USB-A tutorial directly via device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            hdmi_usb_a_tutorial_wallpaper = 1

            # Set the BYOD wallpaper as HDMI & USB-C tutorial via device.
            raiden_helper.set_the_wallpaper_via_device(hdmi_usb_a_tutorial_wallpaper, device=device_name)

            # Check in Sync Portal that the change made is propagate from device to Sync Portal
            response = raiden_helper.get_device(self.org_id, device_name, self.device_id, self.token)
            wallpaper_option = int(response['state']['reported']['byodSettings']['wallpaper'])
            status_response = raiden_helper.validate_byod_wallpaper_option_sync_portal(wallpaper_option,
                                                                                       hdmi_usb_a_tutorial_wallpaper)

            # Reboot device.
            raiden_helper.reboot_device(global_variables.config, self.org_id, self.token,
                                        device=device_name, device_id=self.device_id)

            # Validate option applied persists in the device.
            status_device = raiden_helper.validate_device_wallpaper(hdmi_usb_a_tutorial_wallpaper,
                                                                    device=device_name)

            # Validate that the option applied persists in sync portal.
            status_persistence = raiden_helper. \
                validate_wallpaper_option_persistence_after_reboot(global_variables.config, self.org_id,
                                                                   self.token, hdmi_usb_a_tutorial_wallpaper,
                                                                   self.device_id)

            status = status_response & status_device & status_persistence
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Reboot_Device(self, role, room_name, device_name):
        """Reboot Device
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that device is connected to Sync Portal.

            Test:
                 Reboot the device.

        """
        try:
            self.banner(f'Reboot Device - {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            # Reboot device.
            status = raiden_helper.reboot_device(global_variables.config, self.org_id, self.token,
                                                 device_name, self.device_id)
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_empty_rooms(self, role, room_name1, room_name2):
        """Add, Read, Update and Delete empty rooms.
            Setup:
                  Sign in to Sync Portal organization using valid owner credentials.

            Test:
                 1. Add 2 empty rooms.
                 2. Check the details of provisioned empty Rooms.
                 3. Update the names of empty rooms
                 4. Delete the rooms from organization.
        """
        try:
            self.banner(f'{role}-Add, read, update and delete empty rooms.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 1. Add two empty rooms.
            Report.logInfo('STEP 1. Add two empty rooms')
            rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/rooms/"
            room_names = list()
            room_names.append(room_name1)
            room_names.append(room_name2)
            payload = {
                "realm": "Rooms",
                "group": "/",
                "rooms": [
                    {
                        "name": room_names[0],
                        "seatCount": 4
                    },
                    {
                        "name": room_names[1],
                        "seatCount": 6
                    }
                ]
            }
            response = raiden_helper.send_request(
                method='POST', url=rooms_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_1 = raiden_validation_methods.validate_rooms_created(response, room_names)

            # STEP 2: Check both rooms are present in the list of rooms in the
            # organization.
            Report.logInfo(
                'STEP 2: Check rooms are present in the list of rooms '
                'in the organization..')
            rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/"
            response = raiden_helper.send_request(
                method='GET', url=rooms_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            room_ids = {}
            rooms_presence = 0
            for object in response:
                if object['name'] == room_names[0]:
                    room_ids[room_names[0]] = str(object['id'])
                    rooms_presence += 1
                if object['name'] == room_names[1]:
                    room_ids[room_names[1]] = str(object['id'])
                    rooms_presence += 1
                if rooms_presence == 2:
                    break
            assert rooms_presence == 2, 'Created rooms are not present in the list of rooms'
            if rooms_presence == 2:
                status_2 = True
                Report.logPass('Created rooms are present in the list of rooms')
            else:
                status_2 = False
                Report.logFail('Crated rooms are not present in the list of rooms')
            room_id1 = room_ids[room_names[0]]
            room_id2 = room_ids[room_names[1]]

            # STEP 3. Update the name & seat count of rooms.
            updated_roomname1 = room_name1 + " Updated"
            updated_roomname2 = room_name2 + " Updated"
            Report.logInfo('STEP 3. Update the room names')
            update_rooms_url_room_1 = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                      "/room/" + room_id1

            payload = {
                "id": room_id1,
                "name": updated_roomname1,
                "maxOccupancy": 4
            }
            response = raiden_helper.send_request(
                method='PUT', url=update_rooms_url_room_1, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_3_room_1 = raiden_validation_methods.validate_room_name_updated(response, updated_roomname1)

            update_rooms_url_room_2 = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                      "/room/" + room_id2
            payload = {
                "id": room_id2,
                "name": updated_roomname2,
                "maxOccupancy": 6
            }

            response = raiden_helper.send_request(
                method='PUT', url=update_rooms_url_room_2, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_3_room_2 = raiden_validation_methods.validate_room_name_updated(response,
                                                                                   updated_roomname2)
            status_3 = status_3_room_1 & status_3_room_2

            # STEP 4: Delete the rooms from organization.
            Report.logInfo(
                'STEP 4: Delete the rooms from organization.')
            delete_room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/delete/"
            payload = {
                "roomIds": [
                    str(room_id1),
                    str(room_id2)
                ]
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_room_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_4 = raiden_validation_methods.validate_empty_response(response)

            status = status_1 & status_2 & status_3 & status_4
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Group_Settings(self, role, room_name, device_name):
        """Group Settings
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Let a room containing Rally Bar is provisioned to the organization.

            Test:
                 1. Add the group: AUTO PARENT GROUP to All groups.
                 2. Add a sub group: AUTO SUBGROUP to AUTO PARENT GROUP.
                 3. Move the room containing Rally Bar to AUTO PARENT GROUP/AUTO SUBGROUP.
                 4. Change the setting- Microphone EQ to Voice Boost in AUTO PARENT GROUP Settings.
                 5. Verify that change should reflect in the policies of AUTO SUBGROUP settings.
                 6. Verify that change should reflect in settings of individual room level.
                 7. Update the name of AUTO SUBGROUP to AUTO SUBGROUP UPDATED
                 8. Verify that the settings of AUTO SUBGROUP UPDATED DOES NOT CHANGE AND THEY PERSIST.
                 9. Change the setting Reverb Control from Normal to Disabled of AUTO SUBGROUP.
                 10. Check that device's audio settings: Microphone EQ and Reverb mode are updated for the device
                 in logi settings.
                 11. Delete AUTO SUBGROUP.
                 12. Check that the individual room level settings align with AUTO PARENT GROUP Settings.
                 13. Delete AUTO PARENT GROUP.

        """
        try:
            self.banner('Group Settings')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, room_name,
                                                                        self.org_id, self.token, device_name)
            # 1. Add the group: AUTO PARENT GROUP to All groups.
            Report.logInfo('STEP 1: Add the group: AUTO PARENT GROUP to All groups')
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                "/update-groups/"
            group_name = 'AUTO PARENT GROUP'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': "sync"}
            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_1 = raiden_validation_methods.validate_group_is_available(response, group_name)

            # 2. Add a sub group: AUTO SUBGROUP to AUTO PARENT GROUP.
            Report.logInfo('STEP 2: Add the group: AUTO  SUBGROUP to AUTO PARENT GROUP')
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                "/update-groups/"
            subgroup_name = 'AUTO SUBGROUP'
            payload = {'operation': "Add", 'target': "/" + group_name + '//' + subgroup_name, 'realm': "sync"}
            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_2 = raiden_validation_methods.validate_subgroup_is_added(response, subgroup_name, group_name)

            # 3. Move the room containing Rally Bar to AUTO PARENT GROUP/AUTO SUBGROUP.
            Report.logInfo('STEP 3: Move the room containing Rally Bar to AUTO PARENT GROUP/AUTO SUBGROUP')
            room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id,
                                                               room_name, self.token)
            move_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/group"
            payload = {
                'roomIds': [
                    room_id
                ],
                'target': "/" + group_name + "/" + subgroup_name + "//"
            }
            response = raiden_helper.send_request(
                method='POST', url=move_group_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_3 = raiden_validation_methods.validate_empty_response(response)

            # 4. Change the setting- Microphone EQ to Voice Boost in AUTO PARENT GROUP Settings.
            Report.logInfo('STEP 4: Change the setting- Microphone EQ to Voice Boost in AUTO PARENT GROUP Settings.')
            settings_policy_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + \
                                  self.org_id + "/Kong/settings-policy/"
            parameter = 'micEQ'
            micEq = 2  # enum for Voice boost
            payload = {
                "rightSight": {
                    "trackingMode": 0,
                    "mode": 0,
                    "version": 2,
                    "on": 1
                },
                "videoSettings": {
                    "antiFlickerMode": 1
                },
                "audioSettings": {
                    "speakerBoost": 0,
                    "noiseReduction": 1,
                    "deReverbMode": 2,
                    "micEQ": micEq,
                    "speakerEQ": 1
                },
                "bt": {
                    "on": 1
                },
                "group": "/AUTO PARENT GROUP/"
            }
            response = raiden_helper.send_request(
                method='POST', url=settings_policy_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_4 = raiden_validation_methods.validate_response_settings_policy(response, parameter, micEq)

            # STEP 5: Verify that change should reflect in the policies of AUTO SUBGROUP settings.
            Report.logInfo('STEP 5: Verify that change should reflect in the policies of AUTO SUBGROUP settings.')
            get_settings_policy_url = global_variables.config.BASE_URL + \
                                      raiden_config.ORG_ENDPNT + self.org_id \
                                      + "/Kong/settings-policy/?group=%2FAUTO%20PARENT%20GROUP%2FAUTO%20SUBGROUP%2F%2F"
            response = raiden_helper.send_request(
                method='GET', url=get_settings_policy_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_5 = raiden_validation_methods.validate_response_settings_policy(response, parameter, micEq)

            # STEP 6. Verify that change should reflect in settings of individual room level.
            Report.logInfo('STEP 6: Verify that change should reflect in settings of individual room level.')
            get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/device/" + \
                             self.device_id

            response = raiden_helper.send_request(
                method='GET', url=get_device_url, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_6 = raiden_validation_methods.validate_device_info_response_room_level(response, parameter, micEq)

            # 7. Update the name of AUTO SUBGROUP to AUTO SUBGROUP UPDATED
            Report.logInfo('STEP 7: Update the name of AUTO SUBGROUP to AUTO SUBGROUP UPDATED')
            update_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                               "/update-groups"
            payload = {
                "operation": "Move",
                "target": "/AUTO PARENT GROUP/AUTO SUBGROUP UPDATED/",
                "source": "/AUTO PARENT GROUP/AUTO SUBGROUP/",
                "realm": "sync"
            }
            response = raiden_helper.send_request(
                method='POST', url=update_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            subgroup_name_new = 'AUTO SUBGROUP UPDATED'
            status_7 = raiden_validation_methods.validate_subgroup_name_is_modified(response, subgroup_name,
                                                                                    subgroup_name_new, group_name)

            # STEP 8. Verify that the settings of AUTO SUBGROUP UPDATED DOES NOT CHANGE AND THEY PERSIST.
            Report.logInfo('STEP 8: Verify that change persist in AUTO SUBGROUP UPDATED policy settings.')
            get_settings_policy_url = global_variables.config.BASE_URL + \
                                      raiden_config.ORG_ENDPNT + self.org_id \
                                      + "/Kong/settings-policy/?group=%2FAUTO%20PARENT%20GROUP%2FAUTO%20SUBGROUP%2F%2F"
            response = raiden_helper.send_request(
                method='GET', url=get_settings_policy_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_8 = raiden_validation_methods.validate_response_settings_policy(response, parameter, micEq)

            # STEP 9. Change the setting Reverb Control from Normal to Disabled of AUTO SUBGROUP.
            Report.logInfo('STEP 9. Change the setting Reverb Control from Normal to Disabled of AUTO SUBGROUP.')
            settings_policy_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                  "/Kong/settings-policy/"
            parameter = 'deReverbMode'
            deReverbMode = 0  # enum for disabled
            payload = {
                "rightSight": {
                    "trackingMode": 0,
                    "mode": 0,
                    "version": 2,
                    "on": 1
                },
                "videoSettings": {
                    "antiFlickerMode": 1
                },
                "audioSettings": {
                    "speakerBoost": 0,
                    "noiseReduction": 1,
                    "deReverbMode": deReverbMode,
                    "micEQ": 2,
                    "speakerEQ": 1
                },
                "bt": {
                    "on": 1
                },
                "group": "/AUTO PARENT GROUP/AUTO SUBGROUP//"
            }

            response = raiden_helper.send_request(
                method='POST', url=settings_policy_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_9 = raiden_validation_methods.validate_response_settings_policy(response, parameter, deReverbMode)

            # STEP 10. Check that device's audio settings: Microphone EQ and Reverb mode are updated.
            Report.logInfo('STEP 10. Check that device audio settings: Microphone EQ and Reverb mode are updated.')
            status_mic_eq = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.mic-eq-preset',
                setting_set_via_portal=micEq,
                device=device_name
            )
            status_reverb_mode = raiden_helper.validate_change_made_in_setting_is_applied_to_device(
                name_of_setting='logi.audio.reverb-reduction',
                setting_set_via_portal='DISABLED',
                device=device_name
            )
            status_10 = status_mic_eq & status_reverb_mode

            # STEP 11. Delete AUTO SUBGROUP.
            Report.logInfo('STEP 11. Delete AUTO SUBGROUP.')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/AUTO PARENT GROUP/AUTO SUBGROUP//",
                "realm": "sync"
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_11 = raiden_validation_methods.validate_subgroup_is_deleted(response, subgroup_name,
                                                                               group_name)

            # 12. Check that the individual room level settings align with AUTO PARENT GROUP Settings
            # i.e. Reverb control changes from Disabled to Normal.
            Report.logInfo(
                'STEP 12:Check that the individual room level settings align with AUTO PARENT GROUP Settings')
            get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/device/" + self.device_id

            response = raiden_helper.send_request(
                method='GET', url=get_device_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_12 = raiden_validation_methods.validate_device_info_response_room_level(response,
                                                                                           parameter='deReverbMode',
                                                                                           attribute=0)
            # STEP 13. Delete AUTO PARENT GROUP.
            Report.logInfo('STEP 13. Delete AUTO PARENT GROUP.')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/AUTO PARENT GROUP//",
                "realm": "sync"
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_13 = raiden_validation_methods.validate_group_is_deleted(response,
                                                                            group_name)
            status = status_1 & status_2 & status_3 & status_4 & status_5 & status_6 & status_7 & status_8 & status_9 \
                     & status_10 & status_11 & status_12 & status_13
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_Move_Device(self, role, room_name, device_name):
        """Move an online Tap IP/Tap Scheduler from one room to another.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Tap IP/ Tap Scheduler is connected to the source room in the organization.

            Test:
                 1. Add a new destination room.
                 2. Check that the newly created room is in the list of rooms in the organization.
                 3. Get Room ID of source room
                 4. Move Tap IP from source room to destination room and verify in Sync Portal
                 and device using adb.
                 5. Move Tap IP back from destination room to source room.
                 6. Delete the destination room from the organization.

        """
        try:
            self.banner(f'Move Device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            # STEP 1. Add a new destination room.
            rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/rooms/"
            now = datetime.now()
            destination_room_name = now.strftime("%Y%m%d%H%M%S") + f" Destination- {device_name}"
            seat_count_room = 4
            Report.logInfo(f'STEP 1. Add the room {destination_room_name} with'
                           f' seat count {seat_count_room}.')
            payload = {
                "realm": "Rooms",
                "group": "/",
                "rooms": [{
                    "name": destination_room_name,
                    "seatCount": seat_count_room
                }]
            }

            response = raiden_helper.send_request(
                method='POST', url=rooms_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            time.sleep(30)

            # STEP 2: Check that the newly created room is in the list of rooms in the organization.
            Report.logInfo(
                'STEP 2: Check newly created room is present in the list of rooms '
                'in the organization..')
            rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/"
            response = raiden_helper.send_request(
                method='GET', url=rooms_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            room_id = None
            for object in response:
                if object['name'] == destination_room_name:
                    room_id = str(object['id'])
                    break
            if room_id:
                status_destination_room = True
                Report.logPass(f'{destination_room_name} is present in the list of rooms')
            else:
                status_destination_room = False
                Report.logFail(f'{destination_room_name} is not present in the list of rooms')

            # STEP 3: Get Room ID of source room
            Report.logInfo(
                f'STEP 3: Get the Room ID of {room_name}')
            source_room_id = raiden_helper.get_room_id_from_room_name(global_variables.config, self.org_id,
                                                                      room_name, self.token)
            # Get the device IP
            device_ip = raiden_helper.get_device_ip(device_name=device_name)

            # STEP 4: Move Tap IP from source room to destination room
            Report.logInfo(f'STEP 4: Move Tap IP from {room_name} to {destination_room_name}')
            move_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/" + \
                       source_room_id + '/device/' + self.device_id + '/move'
            payload = {
                'destRoomId': room_id,
                'deleteRoom': False
            }
            response = raiden_helper.send_request(
                method='POST', url=move_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_move_from_source_to_destination_room = raiden_validation_methods.validate_empty_response(response)
            time.sleep(60)
            # Verify that the Tap IP's room is set to Destination - Tap IP via adb.
            status_move_device_adb = raiden_helper.validate_move_device(destination_room_name, seat_count_room,
                                                                        device=device_name, device_ip=device_ip)

            # STEP 5: Move Tap IP back from destination room to source room.
            move_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/" + room_id + \
                       '/device/' + self.device_id + '/move'
            payload = {
                'destRoomId': source_room_id,
                'deleteRoom': False
            }
            response = raiden_helper.send_request(
                method='POST', url=move_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_move_from_destination_to_source_room = raiden_validation_methods.validate_empty_response(response)
            time.sleep(60)

            # STEP 6: Delete the room: Destination- Tap IP from the organization.
            Report.logInfo(
                'STEP 6: Delete destination room from the organization.')
            delete_room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/delete/"
            payload = {
                "roomIds": [
                    str(room_id)
                ]
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_room_url, body=json.dumps(payload), token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            status_delete_room = raiden_validation_methods.validate_empty_response(response)
            status = status_destination_room & status_move_from_source_to_destination_room & \
                     status_move_device_adb & status_move_from_destination_to_source_room & \
                     status_delete_room
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_IT_User_Access_Control_Restrict_Access_to_subgroups_by_Owner(self, role):
        """IT User Access control- Restrict access of roles: Admin, Read Only User and Installer to sub-groups by Owner
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                1. Add a room group to All groups of meeting rooms.
                2. Add a room group  to All groups of Personal devices.
                3. Allow the Admin, Read Only User and Installer only to the newly added room group in meeting rooms
                & personal devices.
                4. Verify that Admin, Read Only User and Installer can only view newly added room group in meeting rooms
                 & personal devices.
                5. Update the access to Admin, Read Only User and Installer back to All Groups in meeting rooms &
                personal devices.
                6. Delete created room group from the meeting rooms in organization
                7. Delete created room group from the meeting rooms in organization

        """
        try:
            self.banner('IT User Access control by Owner')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                "/update-groups/"
            group_name = 'AUTO GROUP ' + str(int(random.random() * 10000))

            # STEP 1: Owner: Add a room group to All groups of meeting rooms.
            Report.logInfo(f'STEP 1: Owner: Add room group named {group_name} to All groups of meeting rooms.')
            Report.logInfo(f'Role: {role}')
            realm_name_sync = 'sync'
            realm_name_rooms = 'Rooms'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_sync}
            response_sync = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )

            json_formatted_response_sync = json.dumps(response_sync, indent=2)
            Report.logResponse(format(json_formatted_response_sync))
            log.info(f'Response- {json_formatted_response_sync}')
            status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                               group_name)

            # STEP 2: Owner:  Add a room group  to All groups of Personal devices.
            Report.logInfo(f'STEP 2: Owner: Add room group named {group_name} to All groups of personal devices')
            realm_name_personal = 'Personal'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_personal}
            response_personal = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )

            json_formatted_response_personal = json.dumps(response_personal, indent=2)
            Report.logResponse(format(json_formatted_response_personal))
            log.info(f'Response-{json_formatted_response_personal}')
            status_add_room_group_personal = raiden_validation_methods.validate_group_is_available(
                response_sync, group_name)

            # STEP 3: Owner: Allow the Admin, Read Only User and Installer only to the newly added room group in meeting rooms
            # & personal devices.
            Report.logInfo(f'STEP 3: Owner: Allow the Admin, Read Only User and Installer only to {group_name} in '
                           'meeting rooms & personal devices.')
            get_users_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/role"
            role_update_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/role/update"

            # Admin
            user_id_admin = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'OrgViewer',
                                                                          get_users_url,
                                                                          self.token)
            response_user_access_admin = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_admin, self.token, group_name)

            json_formatted_response = json.dumps(response_user_access_admin, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Admin to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Read Only
            user_id_readonly = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'Readonly',
                                                                             get_users_url,
                                                                             self.token)
            response_user_access_readonly = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_readonly, self.token, group_name)

            json_formatted_response = json.dumps(response_user_access_readonly, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Read Only user to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Installer
            user_id_installer = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'Installer',
                                                                              get_users_url,
                                                                              self.token)
            response_user_access_installer = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_installer, self.token, group_name)

            json_formatted_response = json.dumps(response_user_access_installer, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Installer to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # STEP 4: Owner: Verify that Admin, Read Only User and Installer can only view newly created room group in
            # meeting rooms & personal devices.
            Report.logInfo(f'STEP 4: Owner: Verify that Admin, Read Only User and Installer can only view {group_name} '
                           'room group in meeting rooms & personal devices.')
            # Admin
            status_admin = raiden_user_helper.check_allowed_group('OrgViewer', global_variables.config, self.org_id,
                                                                  group_name)
            status_readonly = raiden_user_helper.check_allowed_group('Readonly', global_variables.config, self.org_id,
                                                                     group_name)
            status_installer = raiden_user_helper.check_allowed_group('Installer', global_variables.config, self.org_id,
                                                                      group_name)

            status_roles = status_admin & status_readonly & status_installer

            # STEP 5: Owner: Update the access to Admin, Read Only User and Installer back to All Groups in
            # meeting rooms &  personal devices.
            Report.logInfo('STEP 5: Owner: Update the access to Admin, Read Only User and Installer back to '
                           'All Groups in meeting rooms & personal devices.')
            # Admin
            response_user_access_admin = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_admin, self.token)

            json_formatted_response = json.dumps(response_user_access_admin, indent=2)
            Report.logInfo('Allow access of Admin to all groups in meeting rooms and personal devices.')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Admin to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Read Only User
            response_user_access_readonly = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_readonly, self.token)

            json_formatted_response = json.dumps(response_user_access_readonly, indent=2)
            Report.logInfo('Allow access of Read only user to all groups in meeting rooms and personal devices.')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Read Only user to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Installer
            response_user_access_installer = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_installer, self.token)

            json_formatted_response = json.dumps(response_user_access_installer, indent=2)
            Report.logInfo('Allow access of Admin to all groups in meeting rooms and personal devices..')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Admin to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # STEP 6: Owner: Delete newly created room group from the meeting rooms in organization
            Report.logInfo(f'STEP 6: Owner: Delete room group {group_name} from the meeting rooms in organization')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_rooms
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {group_name} from meeting rooms..- {json_formatted_response}')

            # STEP 7: Owner: Delete newly created group from the personal devices in organization
            Report.logInfo(f'STEP 7: Owner: Delete room group {group_name} from the personal devices in organization')
            payload_personal = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_personal
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload_personal), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {group_name} from personal devices..- {json_formatted_response}')

            status = status_add_room_group_sync & status_add_room_group_personal & status_roles
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_IT_User_Access_Control_Restrict_access_to_subgroups_by_ThirdPartyUser(self):
        """IT User Access control- Restrict access of roles: Admin, Read Only User and Installer by Third Party User
            Setup:
                  Sign in to Sync Portal using valid Third Party User credentials.

            Test:
                1. Add a room group to All groups of meeting rooms.
                2. Add a room group  to All groups of Personal devices.
                3. Allow the Admin, Read Only User and Installer only to the newly added room group in meeting rooms
                & personal devices.
                4. Verify that Admin, Read Only User and Installer can only view newly added room group in meeting rooms
                 & personal devices.
                5. Update the access to Admin, Read Only User and Installer back to All Groups in meeting rooms &
                personal devices.
                6. Delete created room group from the meeting rooms in organization
                7. Delete created room group from the meeting rooms in organization
        """
        try:
            self.banner('IT User Access control by Third Party User')
            role = 'ThirdParty'
            token_thirdpartyuser = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, token_thirdpartyuser)

            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups/"
            group_name = 'AUTO GROUP ' + str(int(random.random() * 10000))

            # STEP 1: Third Party User: Add a room group to All groups of meeting rooms.
            Report.logInfo(
                f'STEP 1: Third Party User: Add room group named {group_name} to All groups of meeting rooms.')
            Report.logInfo(f'Role: {role}')
            realm_name_sync = 'sync'
            realm_name_rooms = 'Rooms'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_sync}
            response_sync = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=token_thirdpartyuser
            )

            json_formatted_response_sync = json.dumps(response_sync, indent=2)
            Report.logResponse(format(json_formatted_response_sync))
            log.info(f'Response- {json_formatted_response_sync}')
            status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                               group_name)

            # STEP 2: Third Party User: Add a room group to All groups of Personal devices.
            Report.logInfo(
                f'STEP 2: Third Party User: Add room group named {group_name} to All groups of personal devices')
            realm_name_personal = 'Personal'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_personal}
            response_personal = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=token_thirdpartyuser
            )

            json_formatted_response_personal = json.dumps(response_personal, indent=2)
            Report.logResponse(format(json_formatted_response_personal))
            log.info(f'Response-{json_formatted_response_personal}')
            status_add_room_group_personal = raiden_validation_methods.validate_group_is_available(
                response_sync, group_name)

            # STEP 3: Third Party User: Allow the Admin, Read Only User and Installer only to newly created group in
            # meeting rooms & personal devices.
            Report.logInfo(f'STEP 3: Third Party User: Allow the Admin, Read Only User and Installer only to '
                           f'{group_name} in meeting rooms & personal devices.')
            get_users_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/role"
            role_update_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/role/update"

            # Admin
            user_id_admin = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'OrgViewer',
                                                                          get_users_url, token_thirdpartyuser)
            response_user_access_admin = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_admin, token_thirdpartyuser, group_name)

            json_formatted_response = json.dumps(response_user_access_admin, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Admin to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Read Only
            user_id_readonly = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'Readonly',
                                                                             get_users_url,
                                                                             token_thirdpartyuser)
            response_user_access_readonly = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_readonly, token_thirdpartyuser, group_name)

            json_formatted_response = json.dumps(response_user_access_readonly, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Read Only user to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Installer
            user_id_installer = raiden_user_helper.get_user_id_from_user_name(global_variables.config, 'Installer',
                                                                              get_users_url,
                                                                              token_thirdpartyuser)
            response_user_access_installer = raiden_user_helper.configure_user_access_to_one_group(
                role_update_url, user_id_installer, token_thirdpartyuser, group_name)

            json_formatted_response = json.dumps(response_user_access_installer, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Restrict access of Installer to the {group_name} in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # STEP 4: Verify that Admin, Read Only User and Installer can only view newly created room group in
            # meeting rooms & personal devices.
            Report.logInfo(f'STEP 4: Verify that Admin, Read Only User and Installer can only view {group_name} '
                           'room group in meeting rooms & personal devices.')
            # Admin
            status_admin = raiden_user_helper.check_allowed_group('OrgViewer', global_variables.config, self.org_id,
                                                                  group_name)
            status_readonly = raiden_user_helper.check_allowed_group('Readonly', global_variables.config, self.org_id,
                                                                     group_name)
            status_installer = raiden_user_helper.check_allowed_group('Installer', global_variables.config, self.org_id,
                                                                      group_name)

            status_roles = status_admin & status_readonly & status_installer

            # STEP 5: Update the access to Admin, Read Only User and Installer back to All Groups in meeting rooms &
            # personal devices.
            Report.logInfo('STEP 5: Update the access to Admin, Read Only User and Installer back to '
                           'All Groups in meeting rooms & personal devices.')
            # Admin
            response_user_access_admin = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_admin, token_thirdpartyuser)

            json_formatted_response = json.dumps(response_user_access_admin, indent=2)
            Report.logInfo('Allow access of Admin to all groups in meeting rooms and personal devices.')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Admin to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Read Only User
            response_user_access_readonly = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_readonly, token_thirdpartyuser)

            json_formatted_response = json.dumps(response_user_access_readonly, indent=2)
            Report.logInfo('Allow access of Read only user to all groups in meeting rooms and personal devices.')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Read Only user to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # Installer
            response_user_access_installer = raiden_user_helper.configure_user_access_to_all_groups(
                role_update_url, user_id_installer, token_thirdpartyuser)

            json_formatted_response = json.dumps(response_user_access_installer, indent=2)
            Report.logInfo('Allow access of Admin to all groups in meeting rooms and personal devices..')
            Report.logResponse(format(json_formatted_response))
            log.info(f'{role} -Allow access of Admin to all groups in meeting rooms and '
                     f'personal devices-Response.- {json_formatted_response}')

            # STEP 6: Delete newly created room group from the meeting rooms in organization
            Report.logInfo(f'STEP 6: Delete room group {group_name} from the meeting rooms in organization')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_rooms
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=token_thirdpartyuser
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {group_name} from meeting rooms..- {json_formatted_response}')

            # STEP 7: Delete newly created room group from the personal devices in organization
            Report.logInfo(f'STEP 7: Delete room group {group_name} from the personal devices in organization')
            payload_personal = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_personal
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload_personal), token=token_thirdpartyuser
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {group_name} from personal devices.- {json_formatted_response}')

            status = status_add_room_group_sync & status_add_room_group_personal & status_roles
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_IT_User_Access_Control_Rename_Room_Groups(self, role):
        """IT User Access control- Rename Room groups.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                1. Add a room group named to All groups of meeting rooms.
                2. Add a room group named  to All groups of Personal devices.
                3. Rename the newly created room group in meeting rooms
                4. Rename he newly created room group in personal devices.
                5. Verify that Admin, Read Only User, Third Party user and Installer can view the renamed room group in
                meeting rooms and Personal devices.
                6. Owner: Delete the room group from the meeting rooms in organization
                7. Owner: Delete the room group from the personal devices in organization.

        """
        try:
            self.banner('IT User Access control- Rename Room groups by Owner')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups/"
            group_name = 'AUTO GROUP ' + str(int(random.random() * 10000))

            # STEP 1: Owner: Add a room group named to All groups of meeting rooms.
            Report.logInfo(f'STEP 1: Owner: Add room group named {group_name} to All groups of meeting rooms.')
            Report.logInfo(f'Role: {role}')
            realm_name_sync = 'sync'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_sync}
            response_sync = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )

            json_formatted_response_sync = json.dumps(response_sync, indent=2)
            Report.logResponse(format(json_formatted_response_sync))
            log.info(f'Response- {json_formatted_response_sync}')
            status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                               group_name)

            # STEP 2: Owner: Add a room group to All groups of Personal devices.
            Report.logInfo(f'STEP 2: Owner: Add room group named {group_name} to All groups of personal devices')
            realm_name_personal = 'Personal'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_personal}
            response_personal = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response_personal = json.dumps(response_personal, indent=2)
            Report.logResponse(format(json_formatted_response_personal))
            log.info(f'Response-{json_formatted_response_personal}')
            status_add_room_group_personal = raiden_validation_methods.validate_group_is_available(
                response_sync, group_name)

            # STEP 3: Owner: Rename room group in meeting rooms
            renamed_group_name = group_name + "-Renamed"
            Report.logInfo(f'Owner: Rename room group {group_name} in meeting rooms to {renamed_group_name}')
            payload = {"operation": "Move", "target": "/" + renamed_group_name + "/", "source": "/" + group_name + "/",
                       "realm": "Rooms"}
            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Response- {json_formatted_response}')
            status_add_room_group_renamed_sync = raiden_validation_methods.validate_group_name_is_modified(
                response, group_name, renamed_group_name)

            # STEP 4: Owner: Rename room group in personal devices
            Report.logInfo(f'STEP 4: Owner: Rename room group {group_name} in personal devices to {renamed_group_name}')
            payload = {"operation": "Move", "target": "/" + renamed_group_name + "/", "source": "/" + group_name + "/",
                       "realm": "Personal"}
            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Response- {json_formatted_response}')
            status_add_room_group_renamed_personal_devices = raiden_validation_methods. \
                validate_group_name_is_modified(response, group_name, renamed_group_name)

            # STEP 5: Verify that Admin, Read Only User, Third Party user and Installer can view
            # renamed group name in meeting rooms and Personal devices.
            Report.logInfo('STEP 5: Verify that Admin, Read Only User, Third Party user and Installer can view '
                           f'{renamed_group_name} in meeting rooms and {renamed_group_name} in Personal devices.')

            # Admin
            status_renamed_group_admin = raiden_user_helper.check_group_is_renamed(role='OrgViewer',
                                                                                   config=global_variables.config,
                                                                                   org_id=self.org_id,
                                                                                   group_name=group_name,
                                                                                   group_name_new=renamed_group_name)

            # Read Only
            status_renamed_group_readonly = raiden_user_helper.check_group_is_renamed(role='Readonly',
                                                                                      config=global_variables.config,
                                                                                      org_id=self.org_id,
                                                                                      group_name=group_name,
                                                                                      group_name_new=renamed_group_name)

            # Installer
            status_renamed_group_installer = raiden_user_helper.check_group_is_renamed(role='Installer',
                                                                                       config=global_variables.config,
                                                                                       org_id=self.org_id,
                                                                                       group_name=group_name,
                                                                                       group_name_new=renamed_group_name)

            # Third Party User
            status_renamed_group_thirdparty = raiden_user_helper.check_group_is_renamed(role='ThirdParty',
                                                                                        config=global_variables.config,
                                                                                        org_id=self.org_id,
                                                                                        group_name=group_name,
                                                                                        group_name_new=renamed_group_name)

            status_renamed_group = status_renamed_group_admin & status_renamed_group_readonly & \
                                   status_renamed_group_installer & status_renamed_group_thirdparty

            # STEP 6: Owner: Delete room group from the meeting rooms in organization
            Report.logInfo(
                f'STEP 6: Owner: Delete room group {renamed_group_name} from the meeting rooms in organization')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": "Rooms"
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {renamed_group_name} from meeting rooms..- {json_formatted_response}')

            # STEP 7: Owner: Delete room group from the personal devices in organization
            Report.logInfo(
                f'STEP 7: Owner: Delete room group {renamed_group_name} from the personal devices in organization')
            payload_personal = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_personal
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload_personal), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {renamed_group_name} from personal devices..- {json_formatted_response}')

            status = status_add_room_group_sync & status_add_room_group_personal & status_add_room_group_renamed_sync \
                     & status_add_room_group_renamed_personal_devices & status_renamed_group
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_IT_User_Access_Control_Delete_Room_Groups(self, role):
        """IT User Access control- Delete Room groups.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                1. Add room group to All groups of meeting rooms.
                2. Add room group to All groups of Personal devices.
                3. Delete room group in meeting rooms
                4. Delete room group in personal devices.
                5. Verify that Admin, Read Only User, Third Party user and Installer can no longer view
                deleted room group in meeting rooms and Personal devices.

        """
        try:
            self.banner('IT User Access control- Delete Room groups by Owner')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups/"
            group_name = 'AUTO GROUP ' + str(int(random.random() * 10000))

            # STEP 1: Owner: Add room group to All groups of meeting rooms.
            Report.logInfo(f'STEP 1: Owner: Add room group named {group_name} to All groups of meeting rooms.')
            Report.logInfo(f'Role: {role}')
            realm_name_sync = 'sync'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_sync}
            response_sync = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )

            json_formatted_response_sync = json.dumps(response_sync, indent=2)
            Report.logResponse(format(json_formatted_response_sync))
            log.info(f'Response- {json_formatted_response_sync}')
            status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                               group_name)

            # STEP 2: Owner: Add room group to All groups of Personal devices.
            Report.logInfo(f'STEP 2: Owner: Add room group named {group_name} to All groups of personal devices')
            realm_name_personal = 'Personal'
            payload = {'operation': "Add", 'target': "/" + group_name, 'realm': realm_name_personal}
            response_personal = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=payload, token=self.token
            )
            json_formatted_response_personal = json.dumps(response_personal, indent=2)
            Report.logResponse(format(json_formatted_response_personal))
            log.info(f'Response-{json_formatted_response_personal}')
            status_add_room_group_personal = raiden_validation_methods.validate_group_is_available(
                response_sync, group_name)

            # STEP 3: Delete room group  from the meeting rooms in organization
            Report.logInfo(f'STEP 6: Delete room group {group_name} from the meeting rooms in organization')
            delete_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/update-groups"
            payload = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": "Rooms"
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete {group_name} from meeting rooms..- {json_formatted_response}')

            # STEP 4: Delete room group from the personal devices in organization
            Report.logInfo(f'STEP 7: Delete room group {group_name} from the personal devices in organization')
            payload_personal = {
                "operation": "Remove",
                "target": "/" + group_name + "//",
                "realm": realm_name_personal
            }
            response = raiden_helper.send_request(
                method='POST', url=delete_group_url, body=json.dumps(payload_personal), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info(f'Delete AUTO GROUP from personal devices.- {json_formatted_response}')

            # STEP 5: Verify that Admin, Read Only User, Third Party user and Installer can no longer view
            # the newly created room group in meeting rooms and AUTO GROUP in Personal devices.
            Report.logInfo('STEP 5: Verify that Admin, Read Only User, Third Party user and Installer can no longer '
                           f'view {group_name} in meeting rooms and AUTO GROUP in Personal devices.')

            # Admin
            status_deleted_group_admin = raiden_user_helper.check_group_is_not_available(role='OrgViewer',
                                                                                         config=global_variables.config,
                                                                                         org_id=self.org_id,
                                                                                         group_name=group_name)

            # Read Only
            status_deleted_group_readonly = raiden_user_helper.check_group_is_not_available(role='Readonly',
                                                                                            config=global_variables.config,
                                                                                            org_id=self.org_id,
                                                                                            group_name=group_name)

            # Installer
            status_deleted_group_installer = raiden_user_helper.check_group_is_not_available(role='Installer',
                                                                                             config=global_variables.config,
                                                                                             org_id=self.org_id,
                                                                                             group_name=group_name)

            # Third Party User
            status_deleted_group_thirdparty = raiden_user_helper.check_group_is_not_available(role='ThirdParty',
                                                                                              config=global_variables.config,
                                                                                              org_id=self.org_id,
                                                                                              group_name=group_name)

            status_deleted_group = status_deleted_group_admin & status_deleted_group_readonly & \
                                   status_deleted_group_installer & status_deleted_group_thirdparty

            status = status_add_room_group_sync & status_add_room_group_personal & status_deleted_group
            assert status is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_end_user(self, role: str):
        """
        Add end user
        """
        try:
            Report.logInfo(f'Adding end user: logging in as: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            add_user_url =f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/associate'
            print("adduser_url is:", add_user_url)
            user_id, email = raiden_user_helper.add_enduser(role=role,
                                                            adduser_url=add_user_url,
                                                            token=self.token)
            return user_id, email

        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_end_user(self, role: str, user_id: str, email_id: str):
        """
        View end user
        """
        try:
            Report.logInfo(f'{role}-View end user with email-id {email_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            status_get_user = raiden_user_helper.get_enduser(global_variables.config, user_id, self.org_id, self.token,
                                                             role, email_id)

            assert status_get_user is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_end_user(self, role, user_id):
        try:
            Report.logInfo(
                f'{role}-Delete the end user with user id: {user_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            delete_user_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/associate'
            response_delete_user = raiden_user_helper.delete_enduser_role(user_id, delete_user_url, self.token)

            json_formatted_response = json.dumps(response_delete_user, indent=2)
            Report.logResponse(format(json_formatted_response))

            for obj in response_delete_user:
                if obj == 'result':
                    res_user_id = response_delete_user[obj][0]['userId']
                    if res_user_id == user_id:
                        Report.logPass(f'User with user id {user_id} is deleted successfully')
                    else:
                        Report.logFail('Something went wrong with the delete users')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_end_user_group(self, role: str):
        """
            Add end users group
        """

        try:
            Report.logInfo(f'Adding end users group by logging in with role {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            add_end_user_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/associate/cohort'
            print(f' Add End User Group Url is: {add_end_user_group_url}')
            user_id, enduser_grpname = raiden_user_helper.add_end_user_group(role=role,
                                                           add_end_user_group_url=add_end_user_group_url,
                                                           token=self.token)
            return user_id, enduser_grpname

        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_end_user_group(self, role: str, cohort_id: str):
        """
        View end user groups
        """
        try:
            Report.logInfo(f'{role}-View end user group with user-id {cohort_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            status_get_end_user_group = raiden_user_helper.get_end_user_group(global_variables.config, cohort_id,
                                                                           self.org_id, self.token,
                                                                           role)

            assert status_get_end_user_group is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_end_user_group(self, role: str, cohort_id: str, end_user_group_name_from: str, end_user_group_name_to: str):
        """
        Update end user group name
        """
        try:
            Report.logInfo(f'Update end user group from {end_user_group_name_from} to- {end_user_group_name_to}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_end_user_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/associate/cohort/' + cohort_id
            Report.logInfo(f'Url to update end user group  is: {update_end_user_group_url}')
            status_update_end_user_group = raiden_user_helper.update_end_user_group(end_user_group_name_from, end_user_group_name_to,
                                                                               update_end_user_group_url,
                                                                               cohort_id, self.token)
            assert status_update_end_user_group is True, 'Error in status'
        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_end_user_group(self, role, cohort_id):
        try:
            Report.logInfo(
                f'{role}-Delete the end user group with cohort id: {cohort_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            delete_end_user_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + "/associate/cohort/" + cohort_id

            response_delete_end_user_group = raiden_user_helper.delete_end_user_group(cohort_id, delete_end_user_group_url,
                                                                                 self.token)

            json_formatted_response = json.dumps(response_delete_end_user_group, indent=2)
            Report.logResponse(format(json_formatted_response))

            if response_delete_end_user_group == {}:
                Report.logPass(f'End User Group with user id {cohort_id} is deleted successfully')
            else:
                Report.logFail('Something went wrong with the delete users')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_end_user_and_group(self, role: str, end_user_id: str, new_end_user_group_id: str, end_user_group_name: str):
        """
        View end user and validate it is mapped to updated group
        """
        try:
            Report.logInfo(f'{role}-View end user with user-id {end_user_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_get_end_user_group = raiden_user_helper.get_end_user_validate_end_user_group(global_variables.config,
                                                                                           end_user_id, self.org_id,
                                                                                           self.token,
                                                                                           role, end_user_group_name)

            assert status_get_end_user_group is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_end_user_group_with_new_group_name(self, role: str, end_user_id: str, end_user_group_name_from: str,
                                                  end_user_group_cohort_id: str):
        """
        Update end user group name
        Change end user group of end user to the newly created end user group in step 1.
        """
        try:
            Report.logInfo(f'Update end user group from {end_user_group_name_from} to - {end_user_group_cohort_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_end_user_group_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/associate'
            Report.logInfo(f'Url to update end user group  is: {update_end_user_group_url}')
            status_update_end_user_group = raiden_user_helper.update_with_new_group_name_for_end_user(end_user_group_name_from,
                                                                                              end_user_group_cohort_id,
                                                                                              update_end_user_group_url,
                                                                                              end_user_id, self.token)
            assert status_update_end_user_group is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_rooms_add_channel(self, role: str):
        """
        Add rooms channel
        """
        try:
            Report.logInfo(f'Adding channel: logging in as: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            add_channel_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/channel'
            Report.logInfo(f'Url to Add Channel is {add_channel_url}')
            channel_id, channel_name = raiden_user_helper.add_rooms_channel(role=role,
                                                                            add_channel_url=add_channel_url,
                                                                            token=self.token)
            return channel_id, channel_name
        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_channel(self, role: str):
        """
        View created Channel for meeting rooms
        """
        try:
            Report.logInfo(f'View channel')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            status_get_channel_details, meeting_room_channel_id = raiden_user_helper.get_channel_info_for_meeting_room(
                global_variables.config,
                self.org_id, self.token)

            assert status_get_channel_details is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_meeting_rooms_channel_name(self, role: str, channel_id: str, end_user_grp_name_from: str,
                                           channel_name: str):
        """
        Update meeting room's channel name to channel name created in Step 1
        """
        try:
            Report.logInfo(f'Update room channel name from {end_user_grp_name_from} to - {channel_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 1. Add one empty room and get room id
            room_name, room_id = self.add_single_empty_room(self.org_id, self.token)

            # STEP 2. Get Channel-id for newly created room
            meeting_room_channel_id = raiden_user_helper.get_meeting_room_channel_info(global_variables.config, room_id, self.org_id,
                                                        self.token, role, room_name)

            update_channel_name_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/room/channel'
            Report.logInfo(f'Url to update channel name of room  is: {update_channel_name_url}')
            # STEP 3. Update Channel-id for newly created room and Validate
            status_update_meeting_room_channel = raiden_user_helper.update_with_new_channel_name_for_meeting_room(
                global_variables.config,
                self.org_id, role, room_id,
                channel_id,
                update_channel_name_url,
                self.token, room_name, meeting_room_channel_id)
            assert status_update_meeting_room_channel is True, 'Error in status'
        except Exception as e:
            Report.logException(f'{e}')

    def add_single_empty_room(self, org_id: str, token: str):
        """
            Add one empty room
        """

        try:
            # STEP 1. Add one empty room.
            Report.logInfo('STEP 1. Add one empty room')
            rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/rooms/"
            room_names = list()
            now = datetime.now()
            room_name_1 = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom1"
            Report.logInfo(f'Room name is {room_name_1}')
            room_names.append(room_name_1)
            payload = {
                "realm": "Rooms",
                "group": "/",
                "rooms": [
                    {
                        "name": room_name_1,
                        "seatCount": 7
                    }
                ]
            }
            response = raiden_helper.send_request(
                method='POST', url=rooms_url, body=json.dumps(payload), token=token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(json_formatted_response)
            room_created_status = raiden_validation_methods.validate_rooms_created(response, room_names)

            assert room_created_status is True, 'Error in status'
            # STEP 2. Get room id
            if room_created_status:
                room_id = response[0]['id']
                Report.logInfo(f'For room {room_name_1} room id is {room_id}')
                return room_name_1, room_id

        except Exception as e:
            Report.logException(f'{e}')

    def tc_modify_channel_name_for_meeting_room(self, role: str, channel_id: str):
        """
        Modify meeting room's channel name to channel name created in Step 1
        """
        try:
            Report.logInfo(f'Modify meeting room channel name')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 1. Create empty room and get roomName and roomId
            room_name, room_id = self.add_single_empty_room(self.org_id, self.token)

            # STEP 2. Get channel-id for newly created room
            status, meeting_room_channel_id = get_channel_info_for_meeting_room(global_variables.config, self.org_id,
                                                                    self.token)

            # STEP 3. Modify channel-id for newly created room from meeting_room_channel_id to channel_id
            modify_channel_name_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/room/channel'
            Report.logInfo(f'Url to update channel name of room  is: {modify_channel_name_url}')

            meeting_room_updated_channel_id = raiden_user_helper.modify_with_new_channel_name_for_meeting_room(
                global_variables.config,
                self.org_id, role, room_id,
                channel_id,
                modify_channel_name_url,
                self.token, room_name)

            if meeting_room_updated_channel_id == channel_id:
                Report.logPass(f'Channel name updated from {meeting_room_channel_id} to {meeting_room_updated_channel_id}')
            else:
                Report.logFail(f'Failed to updated Channel id')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_room_group(self, role: str):
        """
            Add room group
        """

        try:
            now = datetime.now()
            time_to_string = now.strftime("%Y%m%d%H%M%S")
            # Name of a group can have at most 32 characters
            group_name = f"GROUP {time_to_string}"
            Report.logInfo(f'{role} - Add room group named {group_name} to All groups of meeting rooms.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_add_room_group_sync = raiden_helper.add_room_group(role=role, token=self.token,
                                                                      org_id=self.org_id, room_group=group_name)
            assert status_add_room_group_sync is True, 'Error in adding room group'
            return group_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_room_group(self, role: str, room_group: str):
        """
        View room group
        """
        try:
            Report.logInfo(f'{role}-View room group - {room_group}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_get_room_group = raiden_helper.view_room_group(role=role, token=self.token,
                                                                  org_id=self.org_id, room_group=room_group)
            assert status_get_room_group is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')
    def tc_delete_meeting_room_channel(self, role, channel_id):
        try:
            Report.logInfo(
                f'{role}-Delete meeting room channel: {channel_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            delete_meeting_room_channel_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/channel/{channel_id}'

            response_delete_meeting_room_channel = raiden_user_helper.delete_meeting_room_channel(channel_id,
                                                                                                delete_meeting_room_channel_url,
                                                                                                self.token)

            json_formatted_response = json.dumps(response_delete_meeting_room_channel, indent=2)
            Report.logResponse(json_formatted_response)

            if response_delete_meeting_room_channel['id'] == channel_id:
                Report.logPass(f'Meeting room channel id {channel_id} is deleted successfully')
            else:
                Report.logFail(f'Failed to delete meeting room channel with id {channel_id}')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_room_group(self, role: str, existing_room_group: str, renamed_room_group: str):
        """
        Update the name of room group
        """
        try:
            Report.logInfo(f'{role}- Update name of room group from {existing_room_group} to- {renamed_room_group}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_renamed_room_group = raiden_helper.rename_room_group(role=role, token=self.token,
                                                                        org_id=self.org_id,
                                                                        existing_room_group=existing_room_group,
                                                                        renamed_room_group=renamed_room_group)
            assert status_renamed_room_group is True, 'Error in renaming room group'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_room_group(self, role, room_group):
        try:
            Report.logInfo(f'{role} - Delete room group {room_group} from the meeting rooms in organization')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_delete_room_group = raiden_helper.delete_room_group(role=role, token=self.token,
                                                                       org_id=self.org_id, room_group=room_group)
            assert status_delete_room_group is True, 'Error in deleting room group'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_host_group(self, role: str):
        """
            Add room group
        """

        try:
            now = datetime.now()
            time_to_string = now.strftime("%Y%m%d%H%M%S")
            # Name of a group can have at most 32 characters
            group_name = f"GROUP {time_to_string}"
            Report.logInfo(f'{role} - Add host computer group named {group_name} to All groups of Personal Devices.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_add_room_group_sync = raiden_helper.add_host_group(role=role, token=self.token,
                                                                      org_id=self.org_id, host_group=group_name)
            assert status_add_room_group_sync is True, 'Error in adding room group'
            return group_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_view_host_group(self, role: str, host_group: str):
        """
        View room group
        """
        try:
            Report.logInfo(f'{role}-View room group - {host_group}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_get_room_group = raiden_helper.view_host_group(role=role, token=self.token,
                                                                  org_id=self.org_id, host_group=host_group)
            assert status_get_room_group is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_host_group(self, role: str, existing_host_group: str, renamed_host_group: str):
        """
        Update the name of room group
        """
        try:
            Report.logInfo(f'{role}- Update name of room group from {existing_host_group} to- {renamed_host_group}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_renamed_room_group = raiden_helper.rename_host_group(role=role, token=self.token,
                                                                        org_id=self.org_id,
                                                                        existing_host_group=existing_host_group,
                                                                        renamed_host_group=renamed_host_group)
            assert status_renamed_room_group is True, 'Error in renaming room group'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_host_group(self, role, host_group):
        try:
            Report.logInfo(f'{role} - Delete room group {host_group} from the meeting rooms in organization')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            status_delete_room_group = raiden_helper.delete_host_group(role=role, token=self.token,
                                                                       org_id=self.org_id, host_group=host_group)
            assert status_delete_room_group is True, 'Error in deleting room group'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_edit_tapscheduler_host_name(self, room_name, role, device_name):
        """
            TC to edit tap scheduler host name
        """
        try:
            Report.logInfo(f'Edit tap scheduler host name')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Provision the room
            env = global_variables.SYNC_ENV
            self.room_id = self.tc_provision_device_in_appliance_mode_to_sync_portal(role, device_name, room_name, env)

            # STEP 3: Get tap scheduler Initial host name
            get_tapscheduler_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{self.room_id}/info'

            self.room_name = room_name
            for i in range(20):
                response_get_tapscheduler_host_name = raiden_helper.send_request(
                    method='GET', url=get_tapscheduler_host_name_url,
                    token=self.token
                )

                time.sleep(5)

                if len(response_get_tapscheduler_host_name['devices']) >= 1:
                    self.device_id = response_get_tapscheduler_host_name['devices'][0]['id']
                    if 'systemSettings' in response_get_tapscheduler_host_name['devices'][0]['state']['reported']:
                        self.tapscheduler_host_name = \
                        response_get_tapscheduler_host_name['devices'][0]['state']['reported']['systemSettings']['hostName']
                        Report.logInfo(f'Tap Scheduler initial host name is: {self.tapscheduler_host_name}')
                        break

            # STEP 4: Edit tap scheduler host name
            raiden_helper.edit_tapscheduler_host_name(self,room_name=self.room_name, room_id=self.room_id, token=self.token, org_id=self.org_id, device_id=self.device_id, tapscheduler_host_name=self.tapscheduler_host_name)

            return self.room_id, self.device_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_group_provision_code_for_roomgroup(self, role, room_group_name):
        """
        Method to get group provision code for room group

        :param role:
        :param roomgroup_group_name: name of the group name
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Get group provision code for room group
            roomgroup_group_prov_code_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/prov-code'

            room_group_name = "/" + room_group_name + "//"
            payload_roomgroup_group_prov_code = {
                "group": room_group_name,
                "realm": "Rooms",
                "generate":True
            }

            response_roomgroup_group_prov_code = raiden_helper.send_request(
                method='POST', url=roomgroup_group_prov_code_url, body=json.dumps(payload_roomgroup_group_prov_code), token=self.token
            )

            json_formatted_response_roomgroup_group_prov_code = json.dumps(response_roomgroup_group_prov_code, indent=2)
            Report.logResponse(format(json_formatted_response_roomgroup_group_prov_code))
            roomgroup_group_provision_code = response_roomgroup_group_prov_code['code']
            return roomgroup_group_provision_code

        except Exception as e:
            Report.logException(f'{e}')

    def tc_provision_nintendo_to_sync_portal(self, role, device_name, room_group_name, roomgroup_group_provision_code):
        """
            Provision Nintendo to Sync Portal using room group provision code
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            Report.logInfo(f'{role} Provision Nintendo to Sync Portal using room group provision code')
            browser = BrowserClass()
            browser.close_all_browsers()

            self.lna = LNASyncAppMethods()
            lna_ip = ""

            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in roomgroup_group_provision_code:
                if char != '-':
                    prov_code_without_separator += char
                    lna_ip = fp.NINTENDO_IP

            # Provision Nintendo to Sync Portal using room group provision code
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=lna_ip,
                                                                       user_name=fp.LNA_USERNAME,
                                                                       password=fp.LNA_PASSWORD,
                                                                       provision_code=prov_code_without_separator)

            # Get room name created
            retries = 20
            for retry in range(0, retries):
                room_name = self.get_recently_created_roomname(role, room_group_name)
                if room_name != None:
                    break
                else:
                    time.sleep(10)

            return room_name

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def get_recently_created_roomname(self, role, room_group_name):
        """
        Get recently created room name using room group name
        """
        try:
            list_of_rooms = self.get_list_of_all_rooms_in_organization(role)
            _num_of_rooms = list_of_rooms.__len__()
            for i in range(_num_of_rooms):
                roomgroup_name = list_of_rooms[i]['_highlightResult']['groupLabel']['value']
                room_name = None
                if room_group_name in roomgroup_name:
                    room_name = list_of_rooms[i]['_highlightResult']['name']['value']
                    Report.logInfo(f'Room name is {room_name}')
                    break

            return room_name

        except Exception as e:
            Report.logException(f'{e}')

    def get_list_of_all_rooms_in_organization(self, role):
        """
        Get the list of all rooms in the organization
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            session_context = raiden_helper.get_session_context_filter_by_orgid(
                global_variables.config, self.token, self.org_id,
            )
            alg_obj = RaidenAlgolia(session_context['search'])
            list_of_rooms = alg_obj.algolia_list_of_rooms
            json_formatted_list_of_rooms = json.dumps(list_of_rooms, indent=2)
            Report.logInfo('List of rooms in organization')
            Report.logResponse(json_formatted_list_of_rooms)
            return list_of_rooms

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_organization_bookers(self, role: str, device_name: str):
        """Method to get organization bookers information.

            Test:
                 1. Query the API: Get Booker details
                 GET ~/org/{org-id}/booker
                 2. Get the booker id from the response

        """
        try:
            self.banner(f'Get Device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            response_get_organization_bookers_info = raiden_helper.get_organization_bookers(self, self.org_id, self.token)
            Report.logResponse(response_get_organization_bookers_info)
            booker_id = response_get_organization_bookers_info['bookers'][0]['id']

            return booker_id

        except Exception as e:
            Report.logException(f'{e}')


    def tc_import_bookables_for_bookers(self, role: str, device_name: str, booker_id: str):
        """Method to import bookables for bookers.

            Test:
                 1. Query the API: Import bookables for bookers
                 GET ~/org/{org-id}/booker/{bookerId}/import-bookable

        """
        try:
            self.banner(f'Get Device: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            response_import_bookables_for_bookers = raiden_helper.import_bookables_for_bookers(self, self.org_id,
                                                                                            self.token, booker_id)
            Report.logResponse(response_import_bookables_for_bookers)


        except Exception as e:
            Report.logException(f'{e}')

    def tc_create_empty_room(self, role: str, room_name: str):
        """
            Create empty room
        """

        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            room_id = raiden_helper.create_empty_room(room_name=room_name, seat_count=7, org_id=self.org_id, token=self.token)
            return room_id


        except Exception as e:
            Report.logException(f'{e}')

    def tc_link_room_to_bookable(self, role, room_id, bookable_id):
        """
            Method to link room to bookable

        :param role:
        :param room_id: id of the created room
         :param bookable_id:bookable id for which resource has to be linked
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Link room to bookable
            link_room_to_bookable_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{room_id}/bookable/{bookable_id}'

            response_link_room_to_bookable = raiden_helper.send_request(
                method='POST', url=link_room_to_bookable_url, token=self.token
            )

            json_formatted_response_link_room_to_bookable = json.dumps(response_link_room_to_bookable, indent=2)
            Report.logResponse(format(json_formatted_response_link_room_to_bookable))
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_unlink_rooms_from_bookables(self, role, bookable_id):
        """
            Method to unlink rooms from bookables

        :param role:
        :param bookable_id:bookable id for which resource has to be unlinked
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # UnLink rooms from bookables
            unlink_rooms_from_bookables_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/bookable/unlink'

            payload_unlink_rooms_from_bookable = {
                "bookableIds": [bookable_id]
            }

            response_link_room_to_bookable = raiden_helper.send_request(
                method='POST', url=unlink_rooms_from_bookables_url, body=json.dumps(payload_unlink_rooms_from_bookable), token=self.token
            )

            json_formatted_response_link_room_to_bookable = json.dumps(response_link_room_to_bookable, indent=2)
            Report.logResponse(format(json_formatted_response_link_room_to_bookable))
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_create_rooms_from_bookables(self, role, bookable_id):
        """
            Method to create rooms from bookables

        :param role:
        :param bookable_id:bookable id from which room will be created
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create rooms from bookables
            create_rooms_from_bookables_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/bookable/create-rooms'

            payload_create_rooms_from_bookables = {
                "bookableIds": [bookable_id]
            }

            response_create_rooms_from_bookables = raiden_helper.send_request(
                method='POST', url=create_rooms_from_bookables_url, body=json.dumps(payload_create_rooms_from_bookables), token=self.token
            )

            json_formatted_response_create_rooms_from_bookables = json.dumps(response_create_rooms_from_bookables, indent=2)
            Report.logResponse(format(json_formatted_response_create_rooms_from_bookables))

            for key in response_create_rooms_from_bookables:
                if key == bookable_id:
                    Report.logPass('Rooms created successfully from resource')
                else:
                    Report.logFail('Failed to create rooms')
            return True

        except Exception as e:
            Report.logException(f'{e}')


    def tc_delete_bookables(self, role, bookable_id):
        """
            Method to delete bookables

        :param role:
        :param bookable_id:bookable id which has to be deleted
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Delete bookables
            delete_bookables_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/bookable/delete'

            payload_delete_bookables = {
                "bookableIds": [bookable_id]
            }

            response_delete_bookables = raiden_helper.send_request(
                method='POST', url=delete_bookables_url, body=json.dumps(payload_delete_bookables), token=self.token
            )

            json_formatted_response_delete_bookables = json.dumps(response_delete_bookables, indent=2)
            Report.logResponse(format(json_formatted_response_delete_bookables))
            return True

        except Exception as e:
            Report.logException(f'{e}')


    def tc_import_bookables(self, role, admin_email_id):
        """
            Method to import bookables

        :param role:
        :param bookable_id:bookable id which has to be imported
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Import bookables
            import_bookables_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/booker/{admin_email_id}/import-bookables'

            response_import_bookables = raiden_helper.send_request(
                method='POST', url=import_bookables_url, token=self.token
            )

            json_formatted_response_import_bookables = json.dumps(response_import_bookables, indent=2)
            Report.logResponse(format(json_formatted_response_import_bookables))

            if response_import_bookables['id'] == admin_email_id:
                Report.logPass('Resource imported successfully')
            else:
                Report.logFail('Resource import failed')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_org_details_without_continuation_with_limit_parameter(self, role: str):
        """
            To get organization details for customers with select, sync plus and essential licenses without continuation string
        """

        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            client_certificate_id = self.tc_generate_client_certificate(role)

            if client_certificate_id != None:
                # Client certificate directory path
                directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                CLIENT_CERTIFICATE_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_raiden_api")

                # Certificate and Key placed in below path
                CERT_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'certificate.pem')
                KEY_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'privateKey.pem')

                # Capture response by passing limit query parameter and get continuation string
                cloud_api_url = f'{global_variables.config.PUBLIC_API_BASE_URL}{raiden_config.PUBLICAPI_V1_ORG_ENDPNT}{self.org_id}/place?limit=7'
                log.info(f'URL to get organization rooms, desks, devices details is - {cloud_api_url}')

                response_status = requests.get(cloud_api_url, cert=(CERT_PATH, KEY_PATH))
                json_formatted_response = json.dumps(response_status.json(), indent=2)
                log.info(f'Cloud API response passing limit parameter is - {json_formatted_response}')

                cloud_api_data = json.loads(json_formatted_response)
                Report.logInfo(
                    f"json formatted response removing new line character is: {cloud_api_data}")
                places = cloud_api_data['places']
                continuation_string = cloud_api_data['continuation']

                if len(places) == 0 or continuation_string != None:
                    Report.logPass(f'There is no places details for Organization with premium customers')
                    Report.logPass(f'Cloud API response with continuation string is {continuation_string}')
                    return continuation_string, client_certificate_id
                elif len(places) != 0:
                    Report.logPass(f'Organizations places details for premium customers is {places}')
                elif len(places) == 0 and continuation_string == None:
                    Report.logFail(f'There are no details of places in Organizations for premium customers')
                    Report.logFail(f'There is no continuation string in cloud API response')
                    return cloud_api_data, client_certificate_id

            else:
                Report.logFail(f'Client certificate creation failed')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_org_details_with_continuation_parameter(self, role: str, continuation_string: str):
        """
            To get organization details for customers with select, sync plus and essential licenses with continuation string
        """

        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Client certificate directory path
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            CLIENT_CERTIFICATE_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_raiden_api")

            # Certificate and Key placed in below path
            CERT_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'certificate.pem')
            KEY_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'privateKey.pem')

            # Capture response by passing continuation string
            if continuation_string != None:
                cloud_api_with_continuation_url = f'{global_variables.config.PUBLIC_API_BASE_URL}{raiden_config.PUBLICAPI_V1_ORG_ENDPNT}{self.org_id}/place?continuation={continuation_string}'
                log.info(f'URL to get organization rooms, desks, devices details is - {cloud_api_with_continuation_url}')

                response_with_continuation = requests.get(cloud_api_with_continuation_url, cert=(CERT_PATH, KEY_PATH))
                response_cloud_api_with_continuation = response_with_continuation.json()
                Report.logInfo(f'Cloud API response with continuation parameter is - {response_cloud_api_with_continuation}')

                places = response_cloud_api_with_continuation['places']
                len_places = len(places)

                if len_places > 0:
                    Report.logPass(f'Organizations places details for premium customers is {response_cloud_api_with_continuation}')
                else:
                    Report.logFail(f'There are no details of places in Organizations for premium customers')

                return response_cloud_api_with_continuation
            else:
                cloud_api_without_continuation_url = f'{global_variables.config.PUBLIC_API_BASE_URL}{raiden_config.PUBLICAPI_V1_ORG_ENDPNT}{self.org_id}/place'
                log.info(
                    f'URL to get organization rooms, desks, devices details is - {cloud_api_without_continuation_url}')

                response_without_continuation = requests.get(cloud_api_without_continuation_url, cert=(CERT_PATH, KEY_PATH))
                response_cloud_api_without_continuation = response_without_continuation.json()
                Report.logInfo(
                    f'Cloud API response without continuation parameter is - {response_cloud_api_without_continuation}')

                places = response_cloud_api_without_continuation['places']

                if places:
                    Report.logPass(
                        f'Organizations places details for premium customers is {places}')
                else:
                    Report.logFail(f'There are no details of places in Organizations for premium customers')

                return response_cloud_api_without_continuation

        except Exception as e:
            Report.logException(f'{e}')

    def tc_test_cloud_api_with_deactivated_certificate(self, role: str):
        """
            To test cloud api with org having de-activated client certificate
        """

        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Generate the client certificate
            client_certificate_id = self.tc_generate_client_certificate(role)

            if client_certificate_id != None:
                # Deactivate the client certificate
                response_deactivate_client_certificate = self.tc_deactivate_client_certificate(role, client_certificate_id, False)

                # Client certificate directory path
                directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                CLIENT_CERTIFICATE_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_raiden_api")

                # Certificate and Key placed in below path
                CERT_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'certificate.pem')
                KEY_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'privateKey.pem')

                # Capture response for cloud api
                cloud_api_url = f'{global_variables.config.PUBLIC_API_BASE_URL}{raiden_config.PUBLICAPI_V1_ORG_ENDPNT}{self.org_id}/place'
                log.info(f'Cloud API url for deactivated client certificate is - {cloud_api_url}')

                response = requests.get(cloud_api_url, cert=(CERT_PATH, KEY_PATH))
                response_cloud_api = response.json()
                log.info(f'Cloud API response for deactivated client certificate is - {response_cloud_api}')

                if response_cloud_api['statusCode'] == 403 and response_cloud_api['name'] == 'ForbiddenError':
                    Report.logPass('Valid response received for deactivated certificate')
                else:
                    Report.logFail('Incorrect response received for deactivated certificate')

                return client_certificate_id, response_cloud_api

            else:
                Report.logFail(f'Client certificate creation failed')

        except Exception as e:
            Report.logException(f'{e}')


    def tc_cloud_api_send_too_many_requests(self, role: str):
        """
            Send cloud api by making more than 10 requests in a minute
        """

        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Generate the client certificate
            client_certificate_id = self.tc_generate_client_certificate(role)

            if client_certificate_id != None:
                # Client certificate directory path
                directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                CLIENT_CERTIFICATE_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_raiden_api")

                # Certificate and Key placed in below path
                CERT_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'certificate.pem')
                KEY_PATH = os.path.join(CLIENT_CERTIFICATE_PATH, 'privateKey.pem')

                # Capture response for cloud api
                cloud_api_url = f'{global_variables.config.PUBLIC_API_BASE_URL}{raiden_config.PUBLICAPI_V1_ORG_ENDPNT}{self.org_id}/place'
                log.info(f'URL to get organization rooms, desks, devices details is - {cloud_api_url}')

                for j in range(60):
                    response_status_code = requests.get(cloud_api_url, cert=(CERT_PATH, KEY_PATH))
                    response_cloud_api = response_status_code.json()
                    log.info(f'Cloud API status {response_status_code} with json response - {response_cloud_api}{j}')

                    if j > 10:
                        Report.logInfo(f'Too many requests - {response_status_code}')

                    if response_status_code == 429:
                        Report.logPass('Too many requests message is shown by making more than 10 requests in a minute')
                    else:
                        Report.logFail('Too many requests message is not shown by making more than 10 requests in a minute')

                return client_certificate_id, response_status_code

            else:
                Report.logFail(f'Client certificate creation failed')

        except Exception as e:
            Report.logException(f'{e}{sys.exc_info()[0]}')
            traceback.print_exc()
            raise

    def tc_generate_client_certificate(self, role):
        """
            Method to generate client certificate

        :param role:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Get client certificate
            client_certificate_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/public-api/certificate'
            log.info(f'URL to generate client certificate is - {client_certificate_url}')

            response_get_client_certificate = raiden_helper.send_request(
                method='POST', url=client_certificate_url, token=self.token
            )

            if response_get_client_certificate['id'] != None or response_get_client_certificate['statusCode'] != 403 or response_get_client_certificate['name'] != 'ForbiddenError':
                Report.logPass('Cloud API client certificate is - {response_get_client_certificate}')
                client_certificate_id = response_get_client_certificate['id']
                certificate = response_get_client_certificate['certificate']
                privateKey = response_get_client_certificate['privateKey']

                Report.logResponse(f'Certificate id is {client_certificate_id}')
                Report.logResponse(f'Certificate is {certificate}')
                Report.logResponse(f'Private key is {privateKey}')

                certificate_file = open('certificate.pem', 'w')
                privateKey_file = open('privateKey.pem', 'w')

                certificate_file.writelines(certificate)
                privateKey_file.writelines(privateKey)

                certificate_file.close()
                privateKey_file.close()

                return client_certificate_id

            else:
                Report.logFail('Certificate creation failed.Maximum of two certificates (active or inactive) can be created at a time. Please delete the existing certificate')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_deactivate_client_certificate(self, role, client_certificate_id, client_certificate_status):
        """
            Method to deactivate client certificate

        :param role:
        :param client_certificate_id:Id of Client certificate
        :param client_certificate_status: Bool value to activate/deactivate the client certificate
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Deactivate client certificate
            deactivate_client_certificate_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/public-api/certificate/{client_certificate_id}'
            log.info(f'Url to deactivate client certificate is - {deactivate_client_certificate_url}')

            deactivate_client_certificate_payload = {'active': client_certificate_status}

            response_deactivate_client_certificate = raiden_helper.send_request(
                method='POST', url=deactivate_client_certificate_url, body=deactivate_client_certificate_payload, token=self.token)

            log.info(f'Client certificate status is - {response_deactivate_client_certificate}')

            if len(response_deactivate_client_certificate) == 0:
                Report.logPass(f'Sucessfully de-activated certificate with id {client_certificate_id}')
            else:
                Report.logFail(f'Certificate {client_certificate_id} is in active state')

            return response_deactivate_client_certificate

        except Exception as e:
            Report.logException(f'{e}')


    def tc_delete_client_certificate(self, role, client_certificate_id):
        """
            Method to delete client certificate

        :param role:
        :param client_certificate_id:Id of Client certificate

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Delete client certificate
            delete_client_certificate_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/public-api/certificate/{client_certificate_id}'
            log.info(f'URL to delete client certificate is - {delete_client_certificate_url}')

            response_delete_client_certificate = raiden_helper.send_request(
                method='DELETE', url=delete_client_certificate_url, token=self.token
            )

            log.info(f'Client certificate delete response is - {response_delete_client_certificate}')

            if len(response_delete_client_certificate) == 0:
                Report.logPass(f'Sucessfully deleted certificate with id {client_certificate_id}')
            else:
                Report.logFail(f'Failed to delete certificate with id {client_certificate_id}')

            return response_delete_client_certificate

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_room_to_group(self, role, room_name):
        """
        TC to add room to a group
        """
        try:
            Report.logInfo(f'{role} Add room to group')

            site_name = self.tc_add_room_hierarchy(role, room_name)

            return site_name

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_add_room_hierarchy(self, role, room_name):
        """
        TC to add room hierarchy
        """
        try:
            Report.logInfo(f'{role} Add room Hierarchy')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            site_name = '/Test' + str(int(random.random() * 10000))
            building_name = site_name + '//SVC'
            floor_name = site_name + '/SVC//Floor 1'
            area_name = site_name + '/SVC/Floor 1//QA'

            # STEP 1: Create Site, building, floor and area
            response_site = self.add_group(role=role, group_name=site_name)
            response_building = self.add_group(role=role, group_name=building_name)
            response_floor = self.add_group(role=role, group_name=floor_name)
            response_area = self.add_group(role=role, group_name=area_name)

            if (response_site and response_building and response_floor and response_area) != None:
                Report.logPass(f'Group added successfully')
                site_name = str(site_name).replace('/', '')
                return site_name
            else:
                Report.logFail(f'Failed to add group')

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def add_group(self, role, group_name):
        """
        Method to to add group

        :param role:
        :param group_name:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                "/update-groups"
            payload = {
                "operation": "Add",
                "target": group_name,
                "realm": "Rooms"
            }

            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Add group - {group_name}')
            Report.logResponse(format(json_formatted_response))

            for item in response:
                number_of_groups = len(response)
                count_groups = 0
                if item in group_name:
                    Report.logPass(f'Group name added successfully')
                    break
                else:
                    count_groups += 1
                    if count_groups == number_of_groups:
                        Report.logFail(f'Failed to create group')

            return response

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_remove_custom_tags(self, role: str, room_id: str,
                                  tag_name: str, operation: str):
        """ Method to add/remove custom tag

            Test:
                 1. Query the API: To add/remove custom tags
                 POST /org/{orgId}/room/tags

        """
        try:
            self.banner(f'Add/Remove custom tag for room with id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to add/remove custom tag for room
            add_remove_custom_tags_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/tags"
            log.info(f'URL to add/remove custom tag from room is - {add_remove_custom_tags_url}')

            if operation == "add":
                add_remove_custom_tags_payload = {
                    "roomIds": [room_id],
                    "add": [tag_name],
                    "remove": []
                }
            elif operation == "remove":
                add_remove_custom_tags_payload = {
                    "roomIds": [room_id],
                    "add": [],
                    "remove": [tag_name]
                }

            response_add_remove_custom_tags = raiden_helper.send_request(
                method='POST', url=add_remove_custom_tags_url, body=json.dumps(add_remove_custom_tags_payload),
                token=self.token
            )

            Report.logResponse(f'{response_add_remove_custom_tags}')
            json_formatted_response_add_remove_custom_tags = json.dumps(response_add_remove_custom_tags, indent=2)
            Report.logInfo(
                f" Add or remove custom tag json response:  {json_formatted_response_add_remove_custom_tags}")

            # Validate if custom tag added/removed
            get_room_info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{room_id}/info'

            response_get_room_info = raiden_helper.send_request(method='GET', url=get_room_info_url,
                                                                token=self.token)

            tag_name_added = ""
            length_tag_list = len(response_get_room_info['tags'])
            if operation == "add" and response_get_room_info['tags'][0] == tag_name:
                Report.logPass(f'Custom tags are added to room with room id {room_id}')
                tag_name_added = tag_name
                return tag_name_added
            elif operation == "remove" and length_tag_list == 0:
                Report.logPass(f'Custom tags are removed from room with room id {room_id}')
            else:
                Report.logFail(f'Failed to {operation} custom tags for room with room id {room_id}')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_site(self, role, site_name):
        """
        Delete Site from Sync Portal Meeting rooms
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.delete_site(site_name, self.org_id, self.token)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_remove_custom_tags_from_details_page(self, role: str, room_name: str, room_id: str, assets: str,
                                                    tag_name: str, operation: str):
        """ Method to add/remove custom tag from room details page

            Test:
                 1. Query the API: To add/remove custom tags from room details page
                 PUT /org/{orgId}/room/{room_id}

        """
        try:
            self.banner(f'Add/Remove custom tag for room with id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to add/remove custom tag from room details page
            add_remove_custom_tags_from_room_details_page_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{room_id}"
            log.info(
                f'URL to add/remove custom tag from room details page is - {add_remove_custom_tags_from_room_details_page_url}')

            if operation == "add":
                add_remove_custom_tags_from_room_details_page_payload = {
                    "id": room_id,
                    "name": room_name,
                    "alias": None,
                    "maxOccupancy": 6,
                    "assets": [assets],
                    "tags": [tag_name]
                }
            elif operation == "remove":
                add_remove_custom_tags_from_room_details_page_payload = {
                    "id": room_id,
                    "name": room_name,
                    "alias": None,
                    "maxOccupancy": 6,
                    "assets": [],
                    "tags": []
                }

            response_add_remove_custom_tags_from_room_details_page = raiden_helper.send_request(
                method='PUT', url=add_remove_custom_tags_from_room_details_page_url,
                body=json.dumps(add_remove_custom_tags_from_room_details_page_payload),
                token=self.token
            )

            Report.logResponse(f'{response_add_remove_custom_tags_from_room_details_page}')
            json_formatted_response_add_remove_custom_tags_from_room_details_page = json.dumps(
                response_add_remove_custom_tags_from_room_details_page, indent=2)
            Report.logInfo(
                f" Add or remove custom tag from room details page, json response:  {json_formatted_response_add_remove_custom_tags_from_room_details_page}")

            # Validate if custom tag added/removed from room details page
            tag_name_added = ""
            length_tag_list = len(response_add_remove_custom_tags_from_room_details_page['tags'])
            length_assest_list = len(response_add_remove_custom_tags_from_room_details_page['assets'])
            if operation == "add" and response_add_remove_custom_tags_from_room_details_page['tags'][0] == tag_name and response_add_remove_custom_tags_from_room_details_page['assets'][0] == assets :
                Report.logPass(f'Custom tags are added to room with room id {room_id}')
                tag_name_added = tag_name
            elif operation == "remove" and length_tag_list == 0 and length_assest_list == 0:
                Report.logPass(f'Custom tags are removed from room details with room id {room_id}')
            else:
                Report.logFail(f'Failed to {operation} custom tags from room details with room id {room_id}')

            return tag_name_added

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_multiple_rooms(self, role):
        """ Add multiple empty rooms.
            Setup:
                  Sign in to Sync Portal organization using valid owner credentials.

            Test:
                 1. Add 5 empty rooms.
        """
        try:
            self.banner(f'{role}-Add multiple empty rooms.')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            room_names = list()
            room_ids = list()

            for i in range(5):
                now = datetime.now()
                room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom" + str(i+1)
                room_names.append(room_name)

                # STEP 1. Add empty rooms
                Report.logInfo('STEP 1. Add empty rooms')
                room_id = self.tc_create_empty_room(role, room_name)
                room_ids.append(room_id)

            return room_names, room_ids
        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_remove_custom_to_multiple_rooms(self, role: str, room_ids: list,
                                                    tag_name: str, operation: str):
        """ Method to add/remove custom tag to multiple rooms

            Test:
                 1. Query the API: To add/remove custom tags from room details page
                 POST /org/{orgId}/room/tags

        """
        try:
            self.banner(f'Add/Remove custom tag for multiple rooms: {room_ids}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to add/remove custom tag for multiple rooms
            add_remove_custom_tags_for_multiple_rooms_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/tags"
            log.info(
                f'URL to add/remove custom tag for multiple rooms is - {add_remove_custom_tags_for_multiple_rooms_url}')

            if operation == "add":
                add_remove_custom_tags_for_multiple_rooms_payload = {
                    "roomIds": room_ids,
                    "add": [tag_name],
                    "remove":[]
                }
            elif operation == "remove":
                add_remove_custom_tags_for_multiple_rooms_payload = {
                     "roomIds": room_ids,
                     "add": [],
                     "remove":[tag_name]
                }

            response_add_remove_custom_tags_for_multiple_rooms = raiden_helper.send_request(
                method='POST', url=add_remove_custom_tags_for_multiple_rooms_url,
                body=json.dumps(add_remove_custom_tags_for_multiple_rooms_payload),
                token=self.token
            )

            Report.logResponse(f'{response_add_remove_custom_tags_for_multiple_rooms}')
            json_formatted_response_add_remove_custom_tags_for_multiple_rooms = json.dumps(
                response_add_remove_custom_tags_for_multiple_rooms, indent=2)
            Report.logInfo(
                f" Add or remove custom tag for multiple rooms, json response:  {json_formatted_response_add_remove_custom_tags_for_multiple_rooms}")

            room1_id = room_ids[0]

            # Validate if custom tag added/removed to/from multiple rooms
            get_room_info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{room1_id}/info'

            response_get_room_info = raiden_helper.send_request(method='GET', url=get_room_info_url,
                                                                token=self.token)

            tag_name_added = ""
            length_tag_list = len(response_get_room_info['tags'])
            if operation == "add" and response_get_room_info['tags'][0] == tag_name:
                Report.logPass(f'Custom tags are added to room with room ids {room_ids}')
                tag_name_added = tag_name
            elif operation == "remove" and length_tag_list == 0:
                Report.logPass(f'Custom tags are removed from room with room ids {room_ids}')
            else:
                Report.logFail(f'Failed to {operation} custom tags for room with room ids {room_ids}')
            return tag_name_added

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_rooms(self, role, room_names):
        """
        Delete meeting room from Sync Portal

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            for room_name in room_names:
                raiden_helper.delete_room(room_name, self.org_id, self.token)

        except Exception as e:
            Report.logException(f'{e}')
