import json
import time
from datetime import timedelta
import datetime

from apis.raiden_api import raiden_helper, raiden_validation_methods, raiden_api_user_helper
from apis.raiden_api.raiden_helper import check_health_status_of_device, check_fw_update_availability
from apps.raiden.sync_portal_home import SyncPortalHome
from common import raiden_config, jasmine_room_floor_map_config as jrm
from base.raiden_base_api import RaidenBaseAPI
from base import global_variables
from extentreport.report import Report
from apis.raiden_api.raiden_algolia import RaidenAlgolia
from tzlocal import get_localzone

from apps.local_network_access.lna_methods import LNAMethods
from testsuite_sync_app.tc_methods import SyncTCMethods
from common import framework_params as fp

class SyncPortalHotDesksMethods(RaidenBaseAPI):
    """
    Sync Portal Hot Desks methods
    """
    lna = LNAMethods()
    sync_app = SyncTCMethods()
    sync_portal_home = SyncPortalHome()

    def get_list_of_all_desks_in_organization(self, role):
        """
        Get the list of all desks in the organization
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            session_context = raiden_helper.get_session_context_filter_by_orgid(
                global_variables.config, self.token, self.org_id,
            )
            alg_obj = RaidenAlgolia(session_context['search'])
            list_of_desks = alg_obj.algolia_get_list_of_desks
            json_formatted_list_of_desks = json.dumps(list_of_desks, indent=2)
            Report.logInfo('List of desks in organization')
            Report.logResponse(json_formatted_list_of_desks)
            return list_of_desks

        except Exception as e:
            Report.logException(f'{e}')

    def add_group(self, role, group_name):
        """
        Method to create area

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
                "realm": "Desks"
            }

            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Add group - {group_name}')
            Report.logResponse(format(json_formatted_response))
            return response

        except Exception as e:
            Report.logException(f'{e}')

    def create_empty_desk_and_get_provision_code(self, role, desk_name, area_name):
        """
        Method to create empty desk and get provision code

        :param role:
        :param desk_name:
        :param area_name:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            # Create empty desk
            desk_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/rooms/"
            payload = {
                "realm": "Desks",
                "group": area_name,
                "rooms": [
                    {
                        "name": desk_name
                    }
                ]
            }

            response = raiden_helper.send_request(
                method='POST', url=desk_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo('Create an empty Desk')
            Report.logResponse(format(json_formatted_response))
            desk_obj = response[0]
            status = self._validate_desk_created(desk_obj, desk_name)
            assert status is True, 'Error in creation of desk'

            # Get provision code
            desk_id = desk_obj['id']
            desk_prov_code_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{desk_id}/prov-code'
            response_prov_code = raiden_helper.send_request(
                method='GET', url=desk_prov_code_url, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo('Create an empty Desk')
            Report.logResponse(format(json_formatted_response))
            status_prov_code = self._validate_get_prov_code(response_prov_code)
            assert status_prov_code is True, 'Error in getting prov code'
            return response_prov_code['code'], desk_id

        except Exception as e:
            Report.logException(f'{e}')

    def _validate_desk_created(self, response: dict, desk_name):
        """
        Validate that the desk is created successfully.
        """
        try:
            if response['name'] == desk_name:
                Report.logPass(f'Desk got created successfully. Received response- {response}')
                return True
            else:
                Report.logFail('Error in response')

        except Exception as e:
            Report.logException('Exception occurred- {}'.format(e))

    def _validate_get_prov_code(self, response: dict):
        """
        Validate get prov code.
        """
        try:
            if response['code']:
                Report.logPass(f'Got the code. Received response- {response}')
                return True
            else:
                Report.logFail('Error in response')

        except Exception as e:
            Report.logException(f'Exception occurred - {e}')

    def add_channel_for_flex_desks(self, role: str, flex_desk_add_channel_url: str, token: str) -> tuple:
        """
            Create new channel.

            :param role: Role of logged in user
            :param flex_desk_add_channel_url: API URL to add new channel.
            :param token: Token related to signed in user.
            :return:
            """
        try:
            # Channel name
            new_channel_name = raiden_helper.create_new_channel_name(
                role)

            channel_name = new_channel_name['name'][0]

            # Add New Channel
            add_new_channel_payload = {
                'realm': 'Desks',
                'name': channel_name
            }

            response_add_channel = raiden_helper.send_request(
                method='POST', url=flex_desk_add_channel_url, body=json.dumps(add_new_channel_payload), token=token
            )
            json_formatted_response = json.dumps(response_add_channel, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(f'Response- Added channel for role {role} - {json_formatted_response}')

            # Validate that channel is added successfully.
            data_dict = json.loads(json_formatted_response)

            if channel_name == response_add_channel['name']:
                Report.logPass(f'Channel name {channel_name} is added successfully')
            else:
                Report.logFail(f'Channel name {channel_name} is not added successfully')
            return data_dict['id'], channel_name

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def get_channel_info_for_flex_desks(self, config: dict, org_id: str, token: str, channel_name: str,
                                        channel_id: str):
        """
        Get desk channel info

        :param config: config containing the users' credentials in the organization.
        :param org_id: Organization ID
        :param token: Token related to signed in user.
        :param channel_name: newly created channel name.
        """
        try:
            # Get Channel
            get_channel_url = f'{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/channel?realm=Desks'
            Report.logInfo(f'- Channel url {get_channel_url}')
            response_get_channel = raiden_helper.send_request(
                method='GET', url=get_channel_url, token=token
            )

            # Validate that channel is added successfully.
            if (item['name'] == channel_name & item['id'] == channel_id for item in response_get_channel):
                json_formatted_response = json.dumps(response_get_channel, indent=2)
                Report.logResponse(json_formatted_response)
                Report.logInfo(f'- Response: Get channel - {json_formatted_response}')
                Report.logPass(f'Channel id {channel_name} is retrieved successfully')
            else:
                Report.logFail(f'Channel id could not be retrieved')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def update_with_new_channel_name_for_flex_desk(self, config: dict, org_id: str, role: str, desk_name: str,
                                                   desk_id: str, channel_id: str, channel_name: str,
                                                   update_channel_name_url: str, token: str):
        """
            Update channel name for desk.

            :param desk_id: Desk id for which channel name to be updated
            :param channel_id: Desk to be modified to Channel id
            :param update_channel_name_url: API URL to update room's channel name
            :param token: Token related to signed in user.
            """
        try:
            # Update desk's channel name
            update_desk_channel_name_payload = {
                'roomIds': [desk_id],
                'channelId': channel_id,
                'realm': 'Desks'
            }

            response_update_room_channel_name = raiden_helper.send_request(
                method='POST', url=update_channel_name_url, body=json.dumps(update_desk_channel_name_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_update_room_channel_name, indent=2)
            Report.logResponse(format(json_formatted_response))
            Report.logInfo(
                f'Response- for update channel name is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_update_room_channel_name}")

            # Validate that channel name is updated for the desk successfully.
            is_channel_updated = self.get_channel_info_for_flex_desks(
                global_variables.config, org_id, token, channel_name, channel_id)

            assert is_channel_updated is True, 'Error in status'

            if is_channel_updated:
                Report.logPass(
                    f'For desk name {desk_name}, channel id is updated from $prod to {channel_id} successfully')
            else:
                Report.logFail(f'Failed to Update channel name for desk {desk_name}')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def delete_flex_desk_channel(self, channel_id: str, delete_flex_desk_channel_url: str, token: str):
        """
        Delete flex desk channel
        """
        try:

            Report.logInfo('DELETE Call')
            Report.logInfo(delete_flex_desk_channel_url)

            response = raiden_helper.send_request(
                method='DELETE', url=delete_flex_desk_channel_url,
                token=token
            )
            return response

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def view_group(self, role, group_name):
        """
        Method to view flex desk hierarchy

        :param role:
        :param group_name:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            view_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id

            response = raiden_helper.send_request(
                method='GET', url=view_groups_url, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'View group - {group_name}')
            Report.logResponse(format(json_formatted_response))

        except Exception as e:
            Report.logException(f'{e}')

    def modify_group(self, role, group_name, update_group_name_to, site):
        """
        Method to modify flex desk hierarchy

        :param role:
        :param group_name:
        :param update_group_name_to:modify to new group name
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            modify_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + '/update-groups'

            modify_desk_hierarchy_payload = {
                "operation": "Move",
                "source": group_name + "/",
                "target": update_group_name_to + "/",
                "realm": "Desks"
            }
            response = raiden_helper.send_request(
                method='POST', url=modify_groups_url, body=json.dumps(modify_desk_hierarchy_payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Modify group from - {group_name} to {update_group_name_to}')
            Report.logResponse(format(json_formatted_response))

            list_group_name = update_group_name_to.split('//')
            modified_group_name = list_group_name[-1]
            if '/' in modified_group_name:
                list_group_name_second = modified_group_name.split('/')
                modified_group_name = list_group_name_second[-1]

            site = site.split('/')

            # Validate if group-name is updated
            if response[site[-1]]['SVC']['Floor 1']['QA']['$label'] == modified_group_name:
                Report.logPass(
                    f'Area is updated from {group_name} to {update_group_name_to} successfully')
            elif response[site[-1]]['SVC']['Floor 1']['$label'] == modified_group_name:
                Report.logPass(
                    f'Floor is updated from {group_name} to {update_group_name_to} successfully')
            elif response[site[-1]]['SVC']['$label'] == modified_group_name:
                Report.logPass(
                    f'Building is updated from {group_name} to {update_group_name_to} successfully')
            elif response[site[-1]]['$label'] == modified_group_name:
                Report.logPass(
                    f'Site is updated from {group_name} to {update_group_name_to} successfully')
            else:
                Report.logFail(f'Failed to Update group name from {group_name} to {update_group_name_to} ')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def modify_desk_name(self, role, desk_name, update_desk_name_to, desk_id):
        """
        Method to modify flex desk name

        :param role:
        :param desk_name:
        :param update_desk_name_to
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            modify_desk_name_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + '/room/' + desk_id

            modify_desk_name_payload = {
                "id": desk_id,
                "name": update_desk_name_to,
                "tags": []
            }

            response = raiden_helper.send_request(
                method='PUT', url=modify_desk_name_url, body=json.dumps(modify_desk_name_payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Modify desk from - {desk_name} to {update_desk_name_to}')
            Report.logResponse(format(json_formatted_response))

            # Validate if desk-name is updated
            if update_desk_name_to == response['name']:
                Report.logPass(
                    f'Desk name {desk_name}, is updated to {update_desk_name_to} successfully')
            else:
                Report.logFail(f'Failed to update desk name {desk_name}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def delete_flex_desk_hierarchy(self, role, group_name):
        try:
            Report.logInfo(
                f'{role} -Delete flex desk hierarchy')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Delete desk group name
            delete_site_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/update-groups'

            delete_group_name_payload = {

                "operation": "Remove",
                "target": "/" + group_name,
                "realm": "Desks"
            }

            response_delete_flex_desk_hierarchy = raiden_helper.send_request(
                method='POST', url=delete_site_url, body=json.dumps(delete_group_name_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_delete_flex_desk_hierarchy, indent=2)
            Report.logResponse(format(json_formatted_response))

            if group_name not in response_delete_flex_desk_hierarchy:
                Report.logPass(f'Flex desk group name {group_name} is deleted successfully')
            else:
                Report.logFail(f'Failed to delete flex desk with id {group_name}')

        except Exception as e:
            Report.logException(f'{e}')

    def firmware_update_availability_check_coily(self, org_id, desk_id, device_id, device_type, token):
        """
        Firmware update availability check
        """
        try:
            Report.logInfo(f'Firmware update availability check for {device_type}')
            # Step 1: Verify that device is online
            retries = 30
            # Health Status -1 Unknown, 0 No Issues, 1 Warning, 2 Error.
            for r in range(retries):
                health_status = self.check_health_status_of_desk(org_id, desk_id, device_type, token)
                if health_status == 0 or health_status == 1:
                    break
                else:
                    time.sleep(10)

            # Step 2: Check for firmware update availability.
            update_status = check_fw_update_availability(org_id, desk_id, device_id, device_type, token)
            for _ in range(retries):
                if update_status == 1 or update_status == 8:
                    break
                else:
                    update_status = check_fw_update_availability(org_id, desk_id, device_id, device_type, token)
                    time.sleep(10)
            return update_status

        except Exception as e:
            Report.logException(f'{e}')

    def check_health_status_of_desk(self, org_id, desk_id, device_type, token):
        """
        Check health status of device
        """
        try:
            room_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{desk_id}/info'
            Report.logInfo('GET Call')
            Report.logInfo(room_url)

            response = raiden_helper.send_request(
                method='GET', url=room_url, token=token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(f'Response for GET Desk Info - {json_formatted_response}')
            devices = response['devices']
            device_obj = dict()
            for device in devices:
                if device['type'] == device_type:
                    device_obj = device
                    break
            health_status = device_obj['state']['reported']['healthStatus']
            return health_status

        except Exception as e:
            Report.logInfo.error("{}".format(e))
            raise e

    def move_desk_to_different_group(self, role, group_name, new_group_name, desk_id):
        """
        Method to move desk to different group

        :param role:
        :param group_name:
        :param new_group_name:move desk to new_group_name
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            move_group_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/group'

            modify_desk_hierarchy_payload = {
                "roomIds": [desk_id],
                "target": new_group_name + "/",
                "realm": "Desks"
            }
            response = raiden_helper.send_request(
                method='POST', url=move_group_url, body=json.dumps(modify_desk_hierarchy_payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Move hot desk from - {group_name} to {new_group_name}')
            Report.logResponse(json_formatted_response)

            # Validate response
            if response == {}:
                Report.logPass(
                    f'Desk is moved from {group_name} to {new_group_name} successfully')
            else:
                Report.logFail(f'Failed to move desk from {group_name} to {new_group_name} ')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def get_desk_check_in_url(self, role, desk_id):
        """
        Method to get desk check in url

        :param role:role of logged in user
        :param desk_id:desk id
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            time.sleep(5)
            get_desk_checkin_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/desk/get-checkin-urls'

            get_desk_checkin_payload = {
                "roomIds": [desk_id]
            }
            response = raiden_helper.send_request(
                method='POST', url=get_desk_checkin_url, body=json.dumps(get_desk_checkin_payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Get check-in url for hot desk id - {desk_id}')
            Report.logResponse(json_formatted_response)
            desk_check_in_url = response['desks'][0]['checkinUrl']

            return desk_check_in_url, response

        except Exception as e:
            Report.logException(f'{e}')

    def edit_area_attributes(self, role, location_path):
        """
        Method to edit area attributes

        :param role:role of logged in user
        :param area:area hierarchy
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            edit_area_attributes_payload = {
                "tags": ['Standard', 'Solo', 'SilentZone']
            }

            edit_area_attributes_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/location/{location_path}'
            Report.logInfo(f'Url to edit area attributes  is: {edit_area_attributes_url}')

            response = raiden_helper.send_request(
                method='PUT', url=edit_area_attributes_url, body=json.dumps(edit_area_attributes_payload),
                token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Edit attributes for area - {location_path}')
            Report.logResponse(json_formatted_response)
            tag_list = response['tags']

            # Validate Response
            if tag_list == ['SilentZone', 'Solo', 'Standard']:
                Report.logPass(f'Desk attributes is updated successfully')
            else:
                Report.logFail(f'Failed to edit desk attributes')

            return response

        except Exception as e:
            Report.logException(f'{e}')

    def edit_desk_attributes(self, role, desk_id, desk_name):
        """
        Method to edit desk attributes

        :param role:role of logged in user
        :param area:area hierarchy
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            edit_desk_attributes_payload = {
                'id': desk_id,
                'name': desk_name,
                'tags': ['Keyboard', 'Mouse', 'Screen']
            }

            edit_desk_attributes_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{desk_id}'
            Report.logInfo(f'Url to edit desk attributes  is: {edit_desk_attributes_url}')

            response = raiden_helper.send_request(
                method='PUT', url=edit_desk_attributes_url, body=json.dumps(edit_desk_attributes_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Edit attributes for desk - {desk_name}')
            Report.logResponse(json_formatted_response)
            tag_list = response['tags']

            # Validate Response
            if tag_list == ['Keyboard', 'Mouse', 'Screen']:
                Report.logPass(f'Attributes for desk is updated successfully')
            else:
                Report.logFail(f'Failed to edit desk attributes')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def desk_policy_enable_reserve_remotely(self, modify_desk_policy_reserve_remotely_url: str, token: str,
                                            area_name: str):
        """
            Modify desk policy to enable to reserve desk remotely.

            :param modify_desk_policy_reserve_remotely_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable to reserve desk remotely
            desk_policy_enable_reserve_remotely_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_desk_policy_reserve_remotely = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_reserve_remotely_url,
                body=json.dumps(desk_policy_enable_reserve_remotely_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_desk_policy_reserve_remotely, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify_desk_policy_reserve_remotely is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_desk_policy_reserve_remotely}")

            # Validate that reserve remotely desk policy is modified successfully.
            is_reserve_remotely_enabled = response_enable_desk_policy_reserve_remotely['policy']['reservationPolicy'][
                'reserveRemotely']

            assert is_reserve_remotely_enabled is True, 'Error in status'

            if is_reserve_remotely_enabled:
                Report.logPass(
                    f'Reserve remotely desk policy is enabled successfully')
            else:
                Report.logFail(f'Failed to enable reserve remotely desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_disable_reserve_remotely_enable_walkin_session(self,
                                                                   desk_policy_disable_reserve_remotely_enable_walkin_session_url: str,
                                                                   token: str, area_name: str):
        """
            Modify desk policy to disable to reserve desk remotely and enable walk-in session.

            :param desk_policy_disable_reserve_remotely_enable_walkin_session_url: API URL to modify desk policy to disable to reserve desk remotely and enable walk-in session
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable to reserve desk remotely and enable walk-in session
            desk_policy_disable_reserve_remotely_enable_walkin_session_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': False,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_disable_reserve_remotely_enable_walkin_session = raiden_helper.send_request(
                method='POST', url=desk_policy_disable_reserve_remotely_enable_walkin_session_url,
                body=json.dumps(desk_policy_disable_reserve_remotely_enable_walkin_session_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_disable_reserve_remotely_enable_walkin_session,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for disable reserve remotely and enable walk-in session is: {json_formatted_response}')

            Report.logInfo(f'Response is {response_desk_policy_disable_reserve_remotely_enable_walkin_session}')

            # Validate that reserve remotely is disabled and walk-in enabled successfully.
            is_disable_reserve_remotely = \
                response_desk_policy_disable_reserve_remotely_enable_walkin_session['policy']['reservationPolicy'][
                    'reserveRemotely']
            is_enable_walkin_session = \
                response_desk_policy_disable_reserve_remotely_enable_walkin_session['policy']['coilySettings'][
                    'walkInSessionDefaultDuration']

            assert is_disable_reserve_remotely is False and is_enable_walkin_session == 1, 'Error in status'

            if is_disable_reserve_remotely is False and is_enable_walkin_session == 1:
                Report.logPass(
                    f'Reserve remotely is disabled and walk-in enabled successfully')
            else:
                Report.logFail(f'Failed to disable reserve remotely and enable walk-in session')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def modify_desk_policy_set_max_7_days(self, modify_desk_policy_set_max_days_url: str, token: str,
                                          area_name: str):
        """
            Modify desk policy to set max days advance to 7 days.

            :param modify_desk_policy_set_max_days_url: API URL to set max days advance to 7 days
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to set max days advance to 7 days
            modify_desk_policy_set_max_days_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 7,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_modify_desk_policy_set_max_days = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_set_max_days_url,
                body=json.dumps(modify_desk_policy_set_max_days_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_modify_desk_policy_set_max_days, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for set max days advance to 7 days is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_modify_desk_policy_set_max_days}")

            # Validate that desk policy, set max days advance to 7 days is successfully applied.
            set_max_days_response = response_modify_desk_policy_set_max_days['policy']['reservationPolicy'][
                'maxDaysInAdvance']

            assert set_max_days_response == 7, 'Error in status'

            if set_max_days_response == 7:
                Report.logPass(
                    f'Set max days in advance desk policy is modified successfully')
            else:
                Report.logFail(f'Failed to modify set max days in advance desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def modify_desk_policy_disable_reserved_spot_visible_to_others(self,
                                                                   modify_desk_policy_reserved_spot_visible_to_others_url: str,
                                                                   token: str,
                                                                   area_name: str):
        """
            Desk policy to modify reserved spot visible to others

            :param modify_desk_policy_disable_reserved_spot_visible_to_others_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy disable reserved spot visible to others
            desk_policy_disable_reserved_spot_visible_to_others_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': False},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_disable_reserved_spot_visible_to_others = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_reserved_spot_visible_to_others_url,
                body=json.dumps(desk_policy_disable_reserved_spot_visible_to_others_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_disable_reserved_spot_visible_to_others, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for disabling reserved Spot Visible to others is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_disable_reserved_spot_visible_to_others}")

            # Validate that reserved spot visible to others is disabled.
            reserved_spot_visible_to_others_response = \
                response_desk_policy_disable_reserved_spot_visible_to_others['policy']['reservationPolicy'][
                    'reservedSpotVisibleToOthers']

            assert reserved_spot_visible_to_others_response is False, 'Error in status'

            if not reserved_spot_visible_to_others_response:
                Report.logPass(
                    f'Disabled the reserved spot visible to others successfully')
            else:
                Report.logFail(f'Failed to disable the reserved spot visible to others')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_disable_reserve_remotely(self, modify_desk_policy_reserve_remotely_url: str, token: str,
                                             area_name: str):
        """
            Modify desk policy to disable to reserve desk remotely.

            :param modify_desk_policy_reserve_remotely_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable to reserve desk remotely
            desk_policy_disable_reserve_remotely_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': False,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_disable_desk_policy_reserve_remotely = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_reserve_remotely_url,
                body=json.dumps(desk_policy_disable_reserve_remotely_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_disable_desk_policy_reserve_remotely, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify_desk_policy_reserve_remotely is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_disable_desk_policy_reserve_remotely}")

            # Validate that reserve remotely desk policy is modified successfully.
            is_reserve_remotely_updated = response_disable_desk_policy_reserve_remotely['policy']['reservationPolicy'][
                'reserveRemotely']

            assert is_reserve_remotely_updated is False, 'Error in status'

            if not is_reserve_remotely_updated:
                Report.logPass(
                    f'Reserve remotely desk policy is disabled successfully')
            else:
                Report.logFail(f'Failed to disable reserve remotely desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_set_max_to_default_days(self, modify_desk_policy_set_max_days_url: str, token: str,
                                            area_name: str):
        """
            Modify desk policy to set max days advance to default 14 days.

            :param modify_desk_policy_set_max_days_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to set max days advance to default 14 days
            desk_policy_set_max_14_days_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_set_max_14_days = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_set_max_days_url,
                body=json.dumps(desk_policy_set_max_14_days_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_set_max_14_days, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for set max days advance to 14 days is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_set_max_14_days}")

            # Validate that desk policy, set max days advance to 14 days is successfully applied.
            set_max_days_response = response_desk_policy_set_max_14_days['policy']['reservationPolicy'][
                'maxDaysInAdvance']

            assert set_max_days_response == 14, 'Error in status'

            if set_max_days_response == 14:
                Report.logPass(
                    f'Max days in advance desk policy is set to default 14 days')
            else:
                Report.logFail(f'Failed to set max days in advance desk policy to default 14 days')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_reserved_spot_visible_to_others(self,
                                                           modify_desk_policy_reserved_spot_visible_to_others_url: str,
                                                           token: str,
                                                           area_name: str):
        """
            Desk policy to modify reserved spot visible to others

            :param modify_desk_policy_reserved_spot_visible_to_others_url: API URL to modify Desk Policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy enable reserved spot visible to others
            desk_policy_enable_reserved_spot_visible_to_others_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_enable_reserved_spot_visible_to_others = raiden_helper.send_request(
                method='POST', url=modify_desk_policy_reserved_spot_visible_to_others_url,
                body=json.dumps(desk_policy_enable_reserved_spot_visible_to_others_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_enable_reserved_spot_visible_to_others, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for disabling reserved Spot Visible to others is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_enable_reserved_spot_visible_to_others}")

            # Validate that reserved spot visible to others is disabled.
            reserved_spot_visible_to_others_response = \
                response_desk_policy_enable_reserved_spot_visible_to_others['policy']['reservationPolicy'][
                    'reservedSpotVisibleToOthers']

            assert reserved_spot_visible_to_others_response is True, 'Error in status'

            if reserved_spot_visible_to_others_response:
                Report.logPass(
                    f'Enabled the reserved spot visible to others successfully')
            else:
                Report.logFail(f'Failed to enable the reserved spot visible to others')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_reservation_time_limit_8_hours(self, desk_policy_set_reservation_time_limit_8_hours_url: str,
                                                          token: str,
                                                          area_name: str):
        """
            Desk policy to modify reservation time limit to 8 hours

            :param desk_policy_set_reservation_time_limit_8_hours_url: API URL to modify Desk Policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy enable reservation time limit to 8 hours
            desk_policy_enable_reservation_time_limit_to_8_hours_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 8,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_enable_reservation_time_limit_8_hours = raiden_helper.send_request(
                method='POST', url=desk_policy_set_reservation_time_limit_8_hours_url,
                body=json.dumps(desk_policy_enable_reservation_time_limit_to_8_hours_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_enable_reservation_time_limit_8_hours, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for enabling reservation time limit to 8 hours is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_enable_reservation_time_limit_8_hours}")

            # Validate that reservation time limit is set to 8 hours
            reservation_time_limit_8_hours = \
                response_desk_policy_enable_reservation_time_limit_8_hours['policy']['reservationPolicy'][
                    'reservedSessionDefaultDuration']

            assert reservation_time_limit_8_hours == 8, 'Error in status'

            if reservation_time_limit_8_hours:
                Report.logPass(
                    f'Enabled the reservation time limit to 8 hours successfully')
            else:
                Report.logFail(f'Failed to enable the reservation time limit to 8 hours')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_reservation_time_limit_1_hour(self, desk_policy_set_reservation_time_limit_1_hour_url: str,
                                                         token: str,
                                                         area_name: str):
        """
            Desk policy to modify reservation time limit to 1 hour

            :param desk_policy_set_reservation_time_limit_1_hour_url: API URL to modify Desk Policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy enable reservation time limit to 1 hour
            enable_reservation_time_limit_to_1_hour_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservation_time_limit_1_hour = raiden_helper.send_request(
                method='POST', url=desk_policy_set_reservation_time_limit_1_hour_url,
                body=json.dumps(enable_reservation_time_limit_to_1_hour_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_reservation_time_limit_1_hour, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for enabling reservation time limit to 1 hour is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservation_time_limit_1_hour}")

            # Validate that reservation time limit is set to 1 hour
            reservation_time_limit_1_hour = \
                response_enable_reservation_time_limit_1_hour['policy']['reservationPolicy'][
                    'reservedSessionDefaultDuration']

            assert reservation_time_limit_1_hour == 1, 'Error in status'

            if reservation_time_limit_1_hour:
                Report.logPass(
                    f'Enabled the reservation time limit to 1 hour successfully')
            else:
                Report.logFail(f'Failed to enable the reservation time limit to 1 hour')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_disable_walkin_session(self, disable_walkin_session_url: str, token: str,
                                           area_name: str):
        """
            Modify desk policy to disable walk-in session.

            :param disable_walkin_session_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable walk-in session
            desk_policy_disable_walkin_session_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': None,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_disable_walkin_session = raiden_helper.send_request(
                method='POST', url=disable_walkin_session_url,
                body=json.dumps(desk_policy_disable_walkin_session_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_disable_walkin_session, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify desk policy to disable walk-in session is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_disable_walkin_session}")

            # Validate that desk policy to disable walk-in session.
            is_walkin_session_disabled = response_desk_policy_disable_walkin_session['policy']['coilySettings'][
                'walkInSessionDefaultDuration']

            assert is_walkin_session_disabled == None, 'Error in status'

            if is_walkin_session_disabled == None:
                Report.logPass(
                    f'Walk-in session is disabled successfully')
            else:
                Report.logFail(f'Failed to disable walk-in session for desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_walkin_session_set_duration_1_hour(self, enable_walkin_session_url: str, token: str,
                                                              area_name: str):
        """
            Modify desk policy to enable walk-in session and set default session duration to 1 hour

            :param enable_walkin_session_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable walk-in session and set default session duration to 1 hour
            desk_policy_enable_walkin_session_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_desk_policy_enable_walkin_session = raiden_helper.send_request(
                method='POST', url=enable_walkin_session_url,
                body=json.dumps(desk_policy_enable_walkin_session_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_policy_enable_walkin_session
                                                 , indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify desk policy to enable walk-in session and set duration to 1 hour is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_policy_enable_walkin_session}")

            # Validate that desk policy to enable walk-in session and set duration to 1 hour.
            is_walkin_session_enabled = response_desk_policy_enable_walkin_session['policy']['coilySettings'][
                'walkInSessionDefaultDuration']

            assert is_walkin_session_enabled == 1, 'Error in status'

            if is_walkin_session_enabled:
                Report.logPass(
                    f'Walk-in session is enabled successfully')
            else:
                Report.logFail(f'Failed to enable walk-in session for desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_disable_session_time_limit(self, disable_session_time_limit_url: str, token: str,
                                               area_name: str):
        """
            Modify desk policy to disable session time limit.

            :param disable_session_time_limit_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable session time limit
            disable_session_time_limit_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_disable_session_time_limit = raiden_helper.send_request(
                method='POST', url=disable_session_time_limit_url,
                body=json.dumps(disable_session_time_limit_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_disable_session_time_limit, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify desk policy to disable session time limit is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_disable_session_time_limit}")

            # Validate to modify desk policy to disable session time limit.
            is_reserve_remotely_disabled = response_disable_session_time_limit['policy']['reservationPolicy'][
                'reservationTimeLimit']

            assert is_reserve_remotely_disabled is None, 'Error in status'

            if is_reserve_remotely_disabled is None:
                Report.logPass(
                    f'Session time limit is disabled successfully')
            else:
                Report.logFail(f'Failed to disable session time limit for desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_show_qr_code(self, enable_show_qr_code_url: str, token: str,
                                        area_name: str):
        """
            Modify desk policy to enable to reserve desk remotely.

            :param enable_show_qr_code_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable to show qr code
            desk_policy_enable_show_qr_code_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': True,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_show_qr_code = raiden_helper.send_request(
                method='POST', url=enable_show_qr_code_url,
                body=json.dumps(desk_policy_enable_show_qr_code_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_show_qr_code, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for  is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_show_qr_code}")

            # Validate show qr code is enabled.
            is_show_qr_code_enabled = response_enable_show_qr_code['policy']['reservationPolicy'][
                'qrCodeReservation']

            assert is_show_qr_code_enabled is True, 'Error in status'

            if is_show_qr_code_enabled:
                Report.logPass(
                    f'Show QR code is enabled successfully')
            else:
                Report.logFail(f'Failed to enable show qr code')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_disable_show_qr_code(self, enable_show_qr_code_url: str, token: str,
                                         area_name: str):
        """
            Modify desk policy to enable to reserve desk remotely.

            :param enable_show_qr_code_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable to show qr code
            desk_policy_disable_show_qr_code_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_disable_show_qr_code = raiden_helper.send_request(
                method='POST', url=enable_show_qr_code_url,
                body=json.dumps(desk_policy_disable_show_qr_code_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_disable_show_qr_code, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for  is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_disable_show_qr_code}")

            # Validate show qr code is enabled.
            is_show_qr_code_disabled = response_disable_show_qr_code['policy']['reservationPolicy'][
                'qrCodeReservation']

            assert is_show_qr_code_disabled is False, 'Error in status'

            if not is_show_qr_code_disabled:
                Report.logPass(
                    f'Show QR code is disabled successfully')
            else:
                Report.logFail(f'Failed to disable show qr code')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_reserve_remotely_checkin_vacancy_release_30_minutes(self,
                                                                               enable_reservable_checkin_set_vacancy_release_30_minutes_url: str,
                                                                               token: str,
                                                                               area_name: str):
        """
            Modify flex desk's policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30mins

            :param enable_reservable_checkin_set_vacancy_release_30_minutes_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to Modify flex desk's policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30mins
            enable_reserve_remotely_checkin_vacancy_release_30_minutes_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': 1800,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_checkin_set_vacancy_release_30_minutes = raiden_helper.send_request(
                method='POST', url=enable_reservable_checkin_set_vacancy_release_30_minutes_url,
                body=json.dumps(enable_reserve_remotely_checkin_vacancy_release_30_minutes_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_reservable_checkin_set_vacancy_release_30_minutes,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify_desk_policy_reserve_remotely, enable check-in required and set vacancy release to 30 mins is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservable_checkin_set_vacancy_release_30_minutes}")

            # Validate that reserve remotely desk policy is modified successfully.
            is_reserve_remotely_enabled = \
                response_enable_reservable_checkin_set_vacancy_release_30_minutes['policy']['reservationPolicy'][
                    'reserveRemotely']
            vacancy_release_value = \
                response_enable_reservable_checkin_set_vacancy_release_30_minutes['policy']['coilySettings'][
                    'enforceCheckInTimeLimit']

            assert is_reserve_remotely_enabled is True and vacancy_release_value == 1800, 'Error in status'

            if is_reserve_remotely_enabled is True and vacancy_release_value == 1800:
                Report.logPass(
                    f'Reserve remotely desk policy is enabled and vacancy release is set to 30 minutes')
            else:
                Report.logFail(f'Failed to enable reserve remotely and set vacancy release to 30 minutes')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_reservable_disable_check_in(self, desk_policy_enable_reservable_disable_check_in_url: str,
                                                       token: str,
                                                       area_name: str):
        """
            Modify flex desk's policy to enable Reservable and disable Check-in required

            :param desk_policy_enable_reservable_disable_check_in_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify flex desk's policy to enable Reservable and disable Check-in required
            enable_reservable_disable_check_in_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_disable_check_in = raiden_helper.send_request(
                method='POST', url=desk_policy_enable_reservable_disable_check_in_url,
                body=json.dumps(enable_reservable_disable_check_in_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_reservable_disable_check_in, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for desk policy enable reservable, disable check-in is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservable_disable_check_in}")

            # Validate that enable reservable, disable check in desk policy is modified successfully.
            is_reservable_enabled = response_enable_reservable_disable_check_in['policy']['reservationPolicy'][
                'reserveRemotely']

            is_check_in_disabled = response_enable_reservable_disable_check_in['policy']['coilySettings'][
                'enforceCheckInTimeLimit']

            assert is_reservable_enabled is True and is_check_in_disabled == None, 'Error in status'

            if is_reservable_enabled is True and is_check_in_disabled == None:
                Report.logPass(
                    f'Desk policy Reserved is enabled and check-in is disabled successfully')
            else:
                Report.logFail(f'Failed to enable reserve remotely and disable check-in desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_walkin_default_session_duration_notify_desk_released(self,
                                                                    enable_walkin_default_session_duration_notify_desk_released_url: str,
                                                                    token: str,
                                                                    area_name: str):
        """
            Modify desk policy to enable walk-in with default session duration set to 1 hour and notify user before desk released to 5 minutes

            :param enable_walkin_default_session_duration_notify_desk_released_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable walk-in with default session duration set to 1 hour and notify user before desk released to 5 minutes
            enable_walkin_default_session_duration_notify_desk_released_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_walkin_default_session_duration_notify_desk_released = raiden_helper.send_request(
                method='POST', url=enable_walkin_default_session_duration_notify_desk_released_url,
                body=json.dumps(enable_walkin_default_session_duration_notify_desk_released_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_walkin_default_session_duration_notify_desk_released,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify desk policy to enable walk-in with default session duration set to 1 hour and notify user before desk released to 5 minutes is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_walkin_default_session_duration_notify_desk_released}")

            # Validate walk-in is enabled with default session duration set to 1 hour and notify user before desk released to 5 minutes successfully.
            is_walkin_with_default_session_duration = \
                response_enable_walkin_default_session_duration_notify_desk_released['policy']['coilySettings'][
                    'walkInSessionDefaultDuration']

            is_notify_user_before_desk_released = \
                response_enable_walkin_default_session_duration_notify_desk_released['policy']['coilySettings'][
                    'notifyUserBeforeDeskReleased']

            assert is_walkin_with_default_session_duration == 1 and is_notify_user_before_desk_released == 300, 'Error in status'

            if is_walkin_with_default_session_duration == 1 and is_notify_user_before_desk_released == 300:
                Report.logPass(
                    f'Response - Desk policy walk-in is enabled with default session duration set to 1 hour and notify user before desk released to 5 minutes successfully')
            else:
                Report.logFail(
                    f'Failed to enable walk-in with default duration and notify user 5 mins before desk released')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def disable_auto_extend_session_set_hardstop_10minutes(self,
                                                           disable_auto_extend_session_set_hardstop_10minutes_url: str,
                                                           token: str,
                                                           area_name: str):
        """
            Modify flex desks policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes

            :param disable_auto_extend_session_set_hardstop_10minutes_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to Modify flex desks policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes
            disable_auto_extend_session_set_hardstop_10minutes_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': 600,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_disable_auto_extend_session_set_hardstop_10minutes = raiden_helper.send_request(
                method='POST', url=disable_auto_extend_session_set_hardstop_10minutes_url,
                body=json.dumps(disable_auto_extend_session_set_hardstop_10minutes_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_disable_auto_extend_session_set_hardstop_10minutes, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify desk policy disable auto extend session set hardstop to 10minutes is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_disable_auto_extend_session_set_hardstop_10minutes}")

            # Validate desk policy disable auto extend session set hardstop to 10minutes is modified successfully.
            is_hardstop_set_10mins = \
                response_disable_auto_extend_session_set_hardstop_10minutes['policy']['coilySettings'][
                    'hardStopBlockFromReusing']

            assert is_hardstop_set_10mins == 600, 'Error in status'

            if is_hardstop_set_10mins:
                Report.logPass(
                    f'Auto extend session is disabled and set hardstop to 10minutes successfully')
            else:
                Report.logFail(f'Failed to disable auto extend session and set hardstop to 10minutes')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_policy_enable_auto_extend_session(self, desk_policy_enable_auto_extend_url: str, token: str,
                                               area_name: str):
        """
            Modify desk policy to enable to reserve desk remotely.

            :param desk_policy_enable_auto_extend_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable auto extend session
            desk_policy_enable_auto_extend_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_auto_extend = raiden_helper.send_request(
                method='POST', url=desk_policy_enable_auto_extend_url,
                body=json.dumps(desk_policy_enable_auto_extend_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_auto_extend, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- Desk policy to enable auto extend session: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_auto_extend}")

            # Validate that auto extend session is enabled in Desk policy .
            is_auto_extend_enabled = response_enable_auto_extend['policy']['coilySettings'][
                'hardStopBlockFromReusing']

            assert is_auto_extend_enabled is None, 'Error in status'

            if is_auto_extend_enabled is None:
                Report.logPass(
                    f'Desk policy auto extend session is enabled successfully')
            else:
                Report.logFail(f'Failed to enable auto extend session in desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_reservable_show_qr_code_check_in_20minutes(self,
                                                          enable_reservable_show_qr_code_check_in_20minutes_url: str,
                                                          token: str,
                                                          area_name: str):
        """
            Modify flex desks policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes

            :param enable_reservable_show_qr_code_check_in_20minutes_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify flex desks policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes
            enable_reservable_show_qr_code_check_in_20minutes_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': 1200,
                                      'qrCodeReservation': True,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_show_qr_code_check_in_20minutes = raiden_helper.send_request(
                method='POST', url=enable_reservable_show_qr_code_check_in_20minutes_url,
                body=json.dumps(enable_reservable_show_qr_code_check_in_20minutes_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_reservable_show_qr_code_check_in_20minutes, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- modify flex desks policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservable_show_qr_code_check_in_20minutes}")

            # Validate that Show QR code is enabled, Reservable is enabled & set Check-in required to 20 minutes successfully modified.
            is_reserve_remotely_enabled = \
                response_enable_reservable_show_qr_code_check_in_20minutes['policy']['reservationPolicy'][
                    'reserveRemotely']

            is_show_qr_code_enabled = \
                response_enable_reservable_show_qr_code_check_in_20minutes['policy']['reservationPolicy'][
                    'qrCodeReservation']

            is_checkin_limit = \
                response_enable_reservable_show_qr_code_check_in_20minutes['policy']['reservationPolicy'][
                    'qrCheckInRequiredTimeLimit']

            assert is_reserve_remotely_enabled is True and is_show_qr_code_enabled is True and is_checkin_limit == 1200, 'Error in status'

            if is_reserve_remotely_enabled and is_show_qr_code_enabled is True and is_checkin_limit == 1200:
                Report.logPass(
                    f'Reservable is enabled, show qr code is enabled and set Check-in required to 20 minutes is successful')
            else:
                Report.logFail(
                    f'Failed to enable Reservable, enable show qr code and set check-in required time to 20minutes')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_reservable_disable_qr_code_and_checkin_required(self,
                                                               enable_reservable_disable_qr_code_and_checkin_required_url: str,
                                                               token: str,
                                                               area_name: str):
        """
            Modify flex Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required

            :param enable_reservable_disable_qr_code_and_checkin_required_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable QR code reservation, Enable Reservable & disable Check-in required
            enable_reservable_disable_qr_code_and_checkin_required_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_disable_qr_code_and_checkin_required = raiden_helper.send_request(
                method='POST', url=enable_reservable_disable_qr_code_and_checkin_required_url,
                body=json.dumps(enable_reservable_disable_qr_code_and_checkin_required_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_reservable_disable_qr_code_and_checkin_required,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- to modify flex Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservable_disable_qr_code_and_checkin_required}")

            # Validate that reserve remotely desk policy is modified successfully.
            is_reserve_remotely_enabled = \
                response_enable_reservable_disable_qr_code_and_checkin_required['policy']['reservationPolicy'][
                    'reserveRemotely']
            checkin_required_disabled = \
                response_enable_reservable_disable_qr_code_and_checkin_required['policy']['reservationPolicy'][
                    'qrCheckInRequiredTimeLimit']
            qrcode_reservation_disabled = \
                response_enable_reservable_disable_qr_code_and_checkin_required['policy']['reservationPolicy'][
                    'qrCodeReservation']

            assert checkin_required_disabled is None and qrcode_reservation_disabled is False, 'Error in status'

            if checkin_required_disabled is None and qrcode_reservation_disabled is False:
                Report.logPass(
                    f'Reserve remotely desk policy is enabled and disabled checkin_required and qrcode_reservation successfully')
            else:
                Report.logFail(
                    f'Failed to enable reserve remotely desk policy and disabled checkin_required and qrcode_reservation ')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_walkin_session_disable_auto_extend_block_reserve_reuse(self,
                                                                      enable_walkin_session_disable_auto_extend_block_reserve_reuse_url: str,
                                                                      token: str,
                                                                      area_name: str):
        """
            Modify flex desk's policy to Enable walk-in session, disable auto-extend session
            and set Blocking user from re-using to 30 mins.

            :param enable_walkin_session_disable_auto_extend_block_reserve_reuse_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to Modify flex desk's policy to Enable walk-in session, disable auto-extend session
            #             and set Blocking user from re-using to 30 mins.
            enable_walkin_session_disable_auto_extend_block_reserve_reuse_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': 1800,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_walkin_session_disable_auto_extend_block_reserve_reuse = raiden_helper.send_request(
                method='POST', url=enable_walkin_session_disable_auto_extend_block_reserve_reuse_url,
                body=json.dumps(enable_walkin_session_disable_auto_extend_block_reserve_reuse_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_enable_walkin_session_disable_auto_extend_block_reserve_reuse,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for enable_walkin_session_disable_auto_extend_block_reserve_reuse is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_walkin_session_disable_auto_extend_block_reserve_reuse}")

            # Validate that enable_walkin_session_disable_auto_extend_block_reserve_reuse.
            walkin_session_enabled = \
                response_enable_walkin_session_disable_auto_extend_block_reserve_reuse['policy']['coilySettings'][
                    'walkInSessionDefaultDuration']
            hardStopBlockFromReusing_time = \
                response_enable_walkin_session_disable_auto_extend_block_reserve_reuse['policy']['coilySettings'][
                    'hardStopBlockFromReusing']

            assert walkin_session_enabled == 1 and hardStopBlockFromReusing_time == 1800, 'Error in status'

            if walkin_session_enabled == 1 and hardStopBlockFromReusing_time == 1800:
                Report.logPass(
                    f'Desk policy enable_walkin_session_disable_auto_extend_block_reserve_reuse_payload is done successfully')
            else:
                Report.logFail(
                    f'Failed to enable_walkin_session_disable_auto_extend_block_reserve_reuse_payload desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def disable_walkin_session_and_checkin_enable_autoextend(self,
                                                             disable_walkin_session_and_checkin_enable_autoextend_url: str,
                                                             token: str,
                                                             area_name: str):
        """
            Modify flex desk's policy to Disable walk-in session, Disable Check-in required, enable auto-extend session

            :param disable_walkin_session_and_checkin_enable_autoextend_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to disable_walkin_session_and_checkin_enable_autoextend
            disable_walkin_session_and_checkin_enable_autoextend_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': True,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': None,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_disable_walkin_session_and_checkin_enable_autoextend = raiden_helper.send_request(
                method='POST', url=disable_walkin_session_and_checkin_enable_autoextend_url,
                body=json.dumps(disable_walkin_session_and_checkin_enable_autoextend_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_disable_walkin_session_and_checkin_enable_autoextend,
                                                 indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for modify_desk_policy_reserve_remotely is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_disable_walkin_session_and_checkin_enable_autoextend}")

            # Validate that disable_walkin_session_and_checkin_enable_autoextend desk policy is modified successfully.
            is_checkin_enabled = \
                response_disable_walkin_session_and_checkin_enable_autoextend['policy']['reservationPolicy'][
                    'qrCodeReservation']

            is_walkin_disabled = \
                response_disable_walkin_session_and_checkin_enable_autoextend['policy']['coilySettings'][
                    'walkInSessionDefaultDuration']

            is_auto_extend_enabled = \
                response_disable_walkin_session_and_checkin_enable_autoextend['policy']['coilySettings'][
                    'hardStopBlockFromReusing']

            assert is_checkin_enabled is True and is_walkin_disabled is None and is_auto_extend_enabled is None, 'Error in status'

            if is_checkin_enabled is True and is_walkin_disabled is None and is_auto_extend_enabled is None:
                Report.logPass(
                    f'disable_walkin_session_and_checkin_enable_autoextend desk policy is modified successfully')
            else:
                Report.logFail(f'Failed to disable_walkin_session_and_checkin_enable_autoextend desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin(self,
                                                                             enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url: str,
                                                                             token: str,
                                                                             area_name: str):
        """
             Modify flex desk's policy to Enable Reservable, set max days in advance to 7 days and session time limit set to 12 hours
            and Show QR code enabled, Check-in required enabled

            :param enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin
            enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': 1200,
                                      'qrCodeReservation': True,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 7,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 12,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin = raiden_helper.send_request(
                method='POST', url=enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url,
                body=json.dumps(enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin is: {json_formatted_response}')

            Report.logInfo(
                f"Response is {response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin}")

            # Validate that enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin is modified successfully.
            is_reserve_remotely_enabled = \
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin['policy'][
                    'reservationPolicy'][
                    'reserveRemotely']

            max_days_in_advance = \
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin['policy'][
                    'reservationPolicy'][
                    'maxDaysInAdvance']

            reserved_session_default_duration = \
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin['policy'][
                    'reservationPolicy'][
                    'reservedSessionDefaultDuration']

            qr_code_reservation_enabled = \
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin['policy'][
                    'reservationPolicy'][
                    'qrCodeReservation']

            qr_checkin_required_time_limit = \
                response_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin['policy'][
                    'reservationPolicy'][
                    'qrCheckInRequiredTimeLimit']

            if qr_code_reservation_enabled and max_days_in_advance == 7 and reserved_session_default_duration == 12 and qr_checkin_required_time_limit == 1200:
                Report.logPass(
                    f'Enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin is modified successfully')
            else:
                Report.logFail(
                    f'Failed to enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def enable_reservable_set_maxdays_disable_session_time_show_qrcode(self,
                                                                       enable_reservable_set_maxdays_disable_session_time_show_qrcode_url: str,
                                                                       token: str,
                                                                       area_name: str):
        """
            Modify desk policy to enable_reservable_set_maxdays_disable_session_time_show_qrcode

            :param enable_reservable_set_maxdays_disable_session_time_show_qrcode_url: API URL to modify desk policy
            :param token: Token related to signed in user.
            :param area_name: Area group hierarchy
        """
        try:
            # Payload to modify desk policy to enable_reservable_set_maxdays_disable_session_time_show_qrcode
            enable_reservable_set_maxdays_disable_session_time_show_qrcode_payload = {
                'group': area_name,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': False,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': 14,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 1,
                                      'reserveRemotely': True,
                                      'reservationTimeLimit': None,
                                      'reservedSpotVisibleToOthers': True},
                'coilySettings': {
                    'walkInSessionDefaultDuration': 1,
                    'notifyUserBeforeDeskReleased': 300,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': None,
                    'enforceCheckInTimeLimit': None,
                    'requireCleaning': False
                }
            }

            response_enable_reservable_set_maxdays_disable_session_time_show_qrcode = raiden_helper.send_request(
                method='POST', url=enable_reservable_set_maxdays_disable_session_time_show_qrcode_url,
                body=json.dumps(enable_reservable_set_maxdays_disable_session_time_show_qrcode_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_enable_reservable_set_maxdays_disable_session_time_show_qrcode, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- to enable_reservable_set_maxdays_disable_session_time_show_qrcode is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_enable_reservable_set_maxdays_disable_session_time_show_qrcode}")

            # Validate that enable_reservable_set_maxdays_disable_session_time_show_qrcodedesk policy is modified successfully.
            is_reserve_remotely_enabled = \
                response_enable_reservable_set_maxdays_disable_session_time_show_qrcode['policy'][
                    'reservationPolicy'][
                    'reserveRemotely']

            max_days_in_advance = response_enable_reservable_set_maxdays_disable_session_time_show_qrcode['policy'][
                'reservationPolicy'][
                'maxDaysInAdvance']

            reservation_time_limit = response_enable_reservable_set_maxdays_disable_session_time_show_qrcode['policy'][
                'reservationPolicy'][
                'reservationTimeLimit']

            qr_code_reservation_enabled = \
                response_enable_reservable_set_maxdays_disable_session_time_show_qrcode['policy'][
                    'reservationPolicy'][
                    'qrCodeReservation']

            if is_reserve_remotely_enabled and max_days_in_advance == 14 and reservation_time_limit is None and qr_code_reservation_enabled is False:
                Report.logPass(
                    f'Enable_reservable_set_maxdays_disable_session_time_show_qrcode desk policy is enabled successfully')
            else:
                Report.logFail(
                    f'Failed to response_enable_reservable_set_maxdays_disable_session_time_show_qrcode desk policy')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def session_booking_for_flex_desk(self, role, user_id, email_id, desk_id, desk_name):
        """
        Method to book a session for desk

        :param role:role of logged in user
        :param desk_id:desk id for which session is booked
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            start_date_time = datetime.datetime.now() + timedelta(days=5) + timedelta(hours=18) + timedelta(
                minutes=22) + timedelta(seconds=30)
            session_start_date = start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            end_date_time = datetime.datetime.now() + timedelta(days=5) + timedelta(hours=19) + timedelta(
                minutes=19) + timedelta(seconds=30)
            session_end_date = end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            flex_desk_session_booking_payload = {
                'title': 'Sync Admin Reservation',
                'start': session_start_date,
                'stop': session_end_date,
                'tz': 'Universal',
                'user': {
                    'identifier': user_id,
                    'email': email_id,
                    'name': email_id
                }
            }

            flex_desk_session_booking_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/desk/{desk_id}/reservation'
            Report.logInfo(f'Url to book a session for desk is: {flex_desk_session_booking_url}')

            response_flex_desk_session_booking = raiden_helper.send_request(
                method='POST', url=flex_desk_session_booking_url, body=json.dumps(flex_desk_session_booking_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_session_booking, indent=2)
            Report.logInfo(f'Booking session for desk - {desk_name}')
            Report.logResponse(json_formatted_response)
            response_user_id = response_flex_desk_session_booking['reservations'][0]['organizer']['identifier']
            response_starts_at = response_flex_desk_session_booking['reservations'][0]['starts_at']
            response_ends_at = response_flex_desk_session_booking['reservations'][0]['ends_at']
            response_reservation_id = response_flex_desk_session_booking['reservations'][0]['identifier']

            # Validate Response
            if response_user_id == user_id and response_starts_at[0:16] in session_start_date and response_ends_at[
                                                                                                  0:16] in session_end_date:
                Report.logPass(f'Session booked for desk {desk_name} with email {email_id} successfully')
            else:
                Report.logFail(f'Failed to book session for desk {desk_name} with email {email_id}')

            return response_reservation_id

        except Exception as e:
            Report.logException(f'{e}')

    def desk_booking_setting_enable_show_meeting_disable_hide_meeting(self,
                                                                      desk_booking_setting_enable_show_meeting_disable_hide_meeting_url: str,
                                                                      token: str, area_name: str):
        """
            Desk Booking Settings - Enable show meeting agenda & disable hide meeting details

            :param desk_booking_enable_show_meeting_disable_hide_meeting_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Enable show meeting agenda & disable hide meeting details
            desk_booking_setting_enable_show_meeting_disable_hide_meeting_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_enable_show_meeting_disable_hide_meeting = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_enable_show_meeting_disable_hide_meeting_url,
                body=json.dumps(desk_booking_setting_enable_show_meeting_disable_hide_meeting_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_enable_show_meeting_disable_hide_meeting, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Enable show meeting agenda & disable hide meeting details is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_enable_show_meeting_disable_hide_meeting}")

            # Validate that Desk Booking Settings - Enable show meeting agenda & disable hide meeting details is modified successfully.
            is_desk_booking_setting_enable_show_meeting_disable_hide_meeting = \
                response_desk_booking_setting_enable_show_meeting_disable_hide_meeting['policy'][
                    'scheduler'][
                    'agendaEnabled']

            if is_desk_booking_setting_enable_show_meeting_disable_hide_meeting:
                Report.logPass(
                    f'Desk Booking Settings - Enable show meeting agenda & disable hide meeting details is done successfully')
            else:
                Report.logFail(
                    f'Failed to Enable show meeting agenda & disable hide meeting details')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_enable_show_meeting_enable_hide_meeting(self,
                                                                     desk_booking_setting_enable_show_meeting_enable_hide_meeting_url: str,
                                                                     token: str, area_name: str):
        """
            Desk Booking Settings - Enable show meeting agenda & enable hide meeting details

            :param desk_booking_setting_enable_show_meeting_enable_hide_meeting_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Enable show meeting agenda & enable hide meeting details
            desk_booking_setting_enable_show_meeting_enable_hide_meeting_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': True,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_enable_show_meeting_enable_hide_meeting = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_enable_show_meeting_enable_hide_meeting_url,
                body=json.dumps(desk_booking_setting_enable_show_meeting_enable_hide_meeting_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_enable_show_meeting_enable_hide_meeting, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Enable show meeting agenda & disable hide meeting details is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_enable_show_meeting_enable_hide_meeting}")

            # Validate that Desk Booking Settings - Enable show meeting agenda & enable hide meeting details is modified successfully.
            is_desk_booking_setting_enable_show_meeting_agenda = \
                response_desk_booking_setting_enable_show_meeting_enable_hide_meeting['policy'][
                    'scheduler'][
                    'agendaEnabled']

            is_desk_booking_setting_enable_hide_meeting = \
                response_desk_booking_setting_enable_show_meeting_enable_hide_meeting['policy'][
                    'scheduler'][
                    'privacyModeEnabled']

            if is_desk_booking_setting_enable_show_meeting_agenda and is_desk_booking_setting_enable_hide_meeting:
                Report.logPass(
                    f'Desk Booking Settings - Enable show meeting agenda & enable hide meeting details is done successfully')
            else:
                Report.logFail(
                    f'Failed to Enable show meeting agenda & enable hide meeting details')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_disable_show_meeting_agenda(self,
                                                         desk_booking_setting_disable_show_meeting_agenda_url: str,
                                                         token: str, area_name: str):
        """
            Desk Booking Settings - Enable show meeting agenda & disable hide meeting details

            :param desk_booking_setting_disable_show_meeting_agenda_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Disable show meeting agenda
            desk_booking_setting_disable_show_meeting_agenda_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': False,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_disable_show_meeting_agenda = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_disable_show_meeting_agenda_url,
                body=json.dumps(desk_booking_setting_disable_show_meeting_agenda_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_disable_show_meeting_agenda, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Disable show meeting agenda is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_disable_show_meeting_agenda}")

            # Validate that Desk Booking Settings - Disable show meeting agenda is modified successfully.
            is_desk_booking_setting_disable_show_meeting_agenda = \
                response_desk_booking_setting_disable_show_meeting_agenda['policy'][
                    'scheduler'][
                    'agendaEnabled']

            if not is_desk_booking_setting_disable_show_meeting_agenda:
                Report.logPass(
                    f'Desk Booking Settings - Disable show meeting agenda is done successfully')
            else:
                Report.logFail(
                    f'Failed to Disable show meeting agenda')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_screen_brightness_100(self, desk_booking_setting_screen_brightness_100_url: str,
                                                   token: str, area_name: str):
        """
            Desk Booking Settings - Set default brightness to 100

            :param desk_booking_setting_screen_brightness_100_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Set default brightness to 100
            desk_booking_setting_screen_brightness_100_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 100,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_screen_brightness_100 = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_screen_brightness_100_url,
                body=json.dumps(desk_booking_setting_screen_brightness_100_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_screen_brightness_100, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Set default brightness to 100 is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_screen_brightness_100}")

            # Validate that Desk Booking Settings - Set default brightness to 100.
            is_desk_booking_setting_screen_brightness_100 = \
                response_desk_booking_setting_screen_brightness_100['policy'][
                    'scheduler'][
                    'screenBrightness']

            if is_desk_booking_setting_screen_brightness_100 == 100:
                Report.logPass(
                    f'Desk Booking Settings - default brightness was set to 100')
            else:
                Report.logFail(
                    f'Failed to set default brightness to 100')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_screen_brightness_250(self, desk_booking_setting_screen_brightness_250_url: str,
                                                   token: str, area_name: str):
        """
            Desk Booking Settings - Set default brightness to 250

            :param desk_booking_setting_screen_brightness_250_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Set default brightness to 250
            desk_booking_setting_screen_brightness_250_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 250,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_screen_brightness_250 = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_screen_brightness_250_url,
                body=json.dumps(desk_booking_setting_screen_brightness_250_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_screen_brightness_250, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Set default brightness to 250 is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_screen_brightness_250}")

            # Validate that Desk Booking Settings - Set default brightness to 250.
            is_desk_booking_setting_screen_brightness_250 = \
                response_desk_booking_setting_screen_brightness_250['policy'][
                    'scheduler'][
                    'screenBrightness']

            if is_desk_booking_setting_screen_brightness_250 == 250:
                Report.logPass(
                    f'Desk Booking Settings - default brightness was set to 250')
            else:
                Report.logFail(
                    f'Failed to set default brightness to 250')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_default_language_english(self, desk_booking_setting_default_language_english_url: str,
                                                      token: str, area_name: str):
        """
            Desk Booking Settings - Set default language to english

            :param desk_booking_setting_default_language_english_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Set default language to english
            desk_booking_setting_default_language_english_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_default_language_english = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_default_language_english_url,
                body=json.dumps(desk_booking_setting_default_language_english_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_default_language_english, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Set default language to english is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_default_language_english}")

            # Validate that Desk Booking Settings - Set default language to english.
            is_desk_booking_setting_default_language_english = \
                response_desk_booking_setting_default_language_english['policy'][
                    'scheduler'][
                    'locale']

            if is_desk_booking_setting_default_language_english == 'en_US':
                Report.logPass(
                    f'Desk Booking Settings - default language was set to english')
            else:
                Report.logFail(
                    f'Failed to set default language to english')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_default_time_format_24_hour(self,
                                                         desk_booking_setting_default_time_format_24_hour_url: str,
                                                         token: str, area_name: str):
        """
            Desk Booking Settings - Set default time format to 24 hour clock

            :param desk_booking_setting_default_time_format_24_hour_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Set default time format to 24 hour clock
            desk_booking_setting_default_time_format_24_hour_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '24'
                                }
                        }
                }

            response_desk_booking_setting_default_time_format_24_hour = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_default_time_format_24_hour_url,
                body=json.dumps(desk_booking_setting_default_time_format_24_hour_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_default_time_format_24_hour, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Set default time format to 24 hour clock is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_default_time_format_24_hour}")

            # Validate that Desk Booking Settings - Set default time format to 24 hour clock
            is_desk_booking_setting_default_time_format_24_hour = \
                response_desk_booking_setting_default_time_format_24_hour['policy'][
                    'scheduler'][
                    'timeFormat']

            if is_desk_booking_setting_default_time_format_24_hour == '24':
                Report.logPass(
                    f'Desk Booking Settings - default timeFormat was set to 24')
            else:
                Report.logFail(
                    f'Failed to set default timeFormat to 24')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def desk_booking_setting_default_time_format_12_hour(self,
                                                         desk_booking_setting_default_time_format_12_hour_url: str,
                                                         token: str, area_name: str):
        """
            Desk Booking Settings - Set default time format to 12 hour clock

            :param desk_booking_setting_default_time_format_12_hour_url: API URL to modify desk settings
            :param token: Token related to signed in user.
            :param area_name: Group Area name
        """
        try:
            # Payload to modify Desk Booking Settings - Set default time format to 12 hour clock
            desk_booking_setting_default_time_format_12_hour_payload = \
                {
                    'group': area_name,
                    'appSettings':
                        {
                            'scheduler':
                                {
                                    'agendaEnabled': True,
                                    'privacyModeEnabled': False,
                                    'screenBrightness': 255,
                                    'locale': 'en_US',
                                    'timeFormat': '12'
                                }
                        }
                }

            response_desk_booking_setting_default_time_format_12_hour = raiden_helper.send_request(
                method='POST', url=desk_booking_setting_default_time_format_12_hour_url,
                body=json.dumps(desk_booking_setting_default_time_format_12_hour_payload),
                token=token
            )
            json_formatted_response = json.dumps(
                response_desk_booking_setting_default_time_format_12_hour, indent=2)
            Report.logResponse(json_formatted_response)
            Report.logInfo(
                f'Response- for Desk Booking Settings - Set default time format to 12 hour clock is: {json_formatted_response}')

            Report.logInfo(f"Response is {response_desk_booking_setting_default_time_format_12_hour}")

            # Validate that Desk Booking Settings - Set default time format to 12 hour clock
            is_desk_booking_setting_default_time_format_12_hour = \
                response_desk_booking_setting_default_time_format_12_hour['policy'][
                    'scheduler'][
                    'timeFormat']

            if is_desk_booking_setting_default_time_format_12_hour == '12':
                Report.logPass(
                    f'Desk Booking Settings - default timeFormat was set to 12')
            else:
                Report.logFail(
                    f'Failed to set default timeFormat to 12')
            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def flex_desk_modify_desk_reservation(self, role, desk_id, reservation_id):
        """
        Method to modify desk reservation

        :param role:role of logged in user
        :param desk_id:desk id for which session is booked
        :param reservation_id:id for the reserved desk
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            updated_start_date_time = datetime.datetime.now() + timedelta(days=5) + timedelta(hours=19) + timedelta(
                minutes=32) + timedelta(seconds=30)
            updated_session_start_date = updated_start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            updated_end_date_time = datetime.datetime.now() + timedelta(days=5) + timedelta(hours=20) + timedelta(
                minutes=45) + timedelta(seconds=30)
            updated_session_end_date = updated_end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            flex_desk_modify_desk_reservation_payload = {
                'title': 'Reservation',
                'start': updated_session_start_date,
                'stop': updated_session_end_date,
                'tz': 'Universal',
                'resourceId': desk_id
            }

            flex_desk_modify_desk_reservation_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/desk/{desk_id}/reservation/{reservation_id}'
            Report.logInfo(f'Url to modify reserved desk is: {flex_desk_modify_desk_reservation_url}')

            response_flex_desk_session_booking = raiden_helper.send_request(
                method='PUT', url=flex_desk_modify_desk_reservation_url,
                body=json.dumps(flex_desk_modify_desk_reservation_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_session_booking, indent=2)
            Report.logInfo(f'Modifying reserved desk for desk id - {desk_id}')
            Report.logResponse(json_formatted_response)

            response_starts_at = response_flex_desk_session_booking['reservations'][0]['starts_at']
            response_ends_at = response_flex_desk_session_booking['reservations'][0]['ends_at']
            response_reservation_id = response_flex_desk_session_booking['reservations'][0]['identifier']

            # Validate Response
            if response_reservation_id == reservation_id and response_starts_at[
                                                             0:16] in updated_session_start_date and response_ends_at[
                                                                                                     0:16] in updated_session_end_date:
                Report.logPass(f'Desk reservation modified successfully for desk id {desk_id}')
            else:
                Report.logFail(f'Failed to modify reserved desk for desk id {desk_id}')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_view_reserved_desk(self, role, desk_id, desk_name):
        """
        Method to view reserved desk

        :param role:role of logged in user
        :param desk_id:desk id for which session is booked
        :param desk_name:name of the reserved desk
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_view_reserved_desk_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{desk_id}/info'
            Report.logInfo(f'Url to view reserved desk is: {flex_desk_view_reserved_desk_url}')

            response_flex_desk_view_reserved_desk = raiden_helper.send_request(
                method='GET', url=flex_desk_view_reserved_desk_url, token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_view_reserved_desk, indent=2)
            Report.logInfo(f'View reserved desk for desk id - {desk_id}')
            Report.logResponse(json_formatted_response)

            response_desk_id = response_flex_desk_view_reserved_desk['id']
            response_desk_name = response_flex_desk_view_reserved_desk['name']

            # Validate Response
            if response_desk_name == desk_name and response_desk_id == desk_id:
                Report.logPass(f'Successfully retrieved details of reserved desk id {desk_id}')
            else:
                Report.logFail(f'Failed to retrieve details of reserved desk id {desk_id}')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_delete_reserved_desk(self, token, org_id, desk_id, reservation_id):
        """
        Method to view reserved desk

        :param token:sign-in token
        :param org_id: id of organization
        :param desk_id:desk id for which session is booked
        :param reservation_id:id for the reserved desk
        """
        try:
            flex_desk_delete_reserved_desk_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/desk/{desk_id}/reservation/{reservation_id}'
            Report.logInfo(f'Url to delete reserved desk is: {flex_desk_delete_reserved_desk_url}')

            response_flex_desk_delete_reserved_desk = raiden_helper.send_request(
                method='DELETE', url=flex_desk_delete_reserved_desk_url, token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_delete_reserved_desk, indent=2)
            Report.logInfo(f'Delete reserved desk for desk id - {desk_id}')
            Report.logResponse(json_formatted_response)

            # Validate Response
            if response_flex_desk_delete_reserved_desk == True:
                Report.logPass(f'Successfully deleted reserved desk {desk_id}')
                return True
            else:
                Report.logFail(f'Failed to delete reserved desk {desk_id}')
                return False

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_add_it_setting_pin_to_a_group(self, role, desk_it_pin, group_name):
        """
            Method to add it setting pin to a group

            :param role:role of logged in user
            :param desk_it_pin: random pin generated for desk it pin setting
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_add_it_setting_pin_to_a_group_payload = {
                "group": group_name,
                "pin": desk_it_pin,
                "label": "sync_it_pin",
                "type": "settings",
                "realm": "Desks"
            }

            flex_desk_add_it_setting_pin_to_a_group_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin'
            Report.logInfo(f'Url to add it setting pin to a group is: {flex_desk_add_it_setting_pin_to_a_group_url}')

            response_flex_desk_add_it_setting_pin_to_a_group = raiden_helper.send_request(
                    method='PUT', url=flex_desk_add_it_setting_pin_to_a_group_url,
                    body=json.dumps(flex_desk_add_it_setting_pin_to_a_group_payload),
                    token=self.token)

            json_formatted_response = json.dumps(response_flex_desk_add_it_setting_pin_to_a_group, indent=2)
            Report.logInfo(f'Add IT setting pin to a group')
            Report.logResponse(json_formatted_response)
            response_pin_id = response_flex_desk_add_it_setting_pin_to_a_group[0]['id']
            response_pin = response_flex_desk_add_it_setting_pin_to_a_group[0]['pin']

            # Validate Response
            if response_pin == desk_it_pin:
                Report.logPass(f'Added IT setting pin successfully to a group')
            else:
                Report.logFail(f'Failed to add IT setting pin')
                response_pin_id = None


            return response_pin_id

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_edit_it_setting_pin_to_a_group(self, role, pin_id, modified_it_pin, group_name):
        """
            Method to edit it setting pin to a group

            :param role:role of logged in user
            param modified_it_pin:modified IT pin of desk
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_edit_it_setting_pin_to_a_group_payload = {
                "group": group_name,
                "pin": modified_it_pin,
                "label": "sync_it_pin",
                "type": "settings",
                "realm": "Desks"
            }

            flex_desk_edit_it_setting_pin_to_a_group_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin/{pin_id}'
            Report.logInfo(f'Url to edit it setting pin to a group is: {flex_desk_edit_it_setting_pin_to_a_group_url}')

            response_flex_desk_edit_it_setting_pin_to_a_group = raiden_helper.send_request(
                method='POST', url=flex_desk_edit_it_setting_pin_to_a_group_url,
                body=json.dumps(flex_desk_edit_it_setting_pin_to_a_group_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_edit_it_setting_pin_to_a_group, indent=2)
            Report.logInfo(f'Edit IT setting pin to a group')
            Report.logResponse(json_formatted_response)
            response_pin_id = response_flex_desk_edit_it_setting_pin_to_a_group[0]['id']
            response_pin = response_flex_desk_edit_it_setting_pin_to_a_group[0]['pin']

            # Validate Response
            if response_pin == modified_it_pin:
                Report.logPass(f'Edited IT setting pin successfully to a group')
            else:
                Report.logFail(f'Failed to edit IT setting pin')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_view_it_setting_pin_to_a_group(self, role, group_name, pin_id):
        """
        Method to view it setting pin to a group

        :param role:role of logged in user
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_view_it_setting_pin_to_a_group_payload = {
                'group': group_name+'%2F&type=settings&realm=Desks'
            }

            flex_desk_view_it_setting_pin_to_a_group_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin?group={group_name}%2F&type=settings&realm=Desks'
            Report.logInfo(f'Url to view it setting pin to a group is: {flex_desk_view_it_setting_pin_to_a_group_url}')

            response_flex_desk_view_it_setting_pin_to_a_group = raiden_helper.send_request(
                method='GET', url=flex_desk_view_it_setting_pin_to_a_group_url,
                body=json.dumps(flex_desk_view_it_setting_pin_to_a_group_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_view_it_setting_pin_to_a_group, indent=2)
            Report.logInfo(f'View IT setting pin to a group')
            Report.logResponse(json_formatted_response)
            if response_flex_desk_view_it_setting_pin_to_a_group != []:
                response_pin_id = response_flex_desk_view_it_setting_pin_to_a_group[0]['id']
                response_pin = response_flex_desk_view_it_setting_pin_to_a_group[0]['pin']

                # Validate Response
                if response_pin_id == pin_id:
                    Report.logPass(f'Viewed IT setting pin successfully to a group')
                else:
                    Report.logFail(f'Failed to view IT setting pin')

                return response_pin_id

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_delete_it_setting_pin_to_a_group(self, role, pin_id, group_name):
        """
        Method to delete it setting pin to a group

        :param role:role of logged in user
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            if pin_id != None:
                flex_desk_delete_it_setting_pin_to_a_group_payload = {
                    'group': group_name+'%2F&type=settings&realm=Desks'
                }

                flex_desk_delete_it_setting_pin_to_a_group_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin/{pin_id}?group={group_name}%2F&type=settings&realm=Desks'
                Report.logInfo(
                    f'Url to delete it setting pin to a group is: {flex_desk_delete_it_setting_pin_to_a_group_url}')

                response_flex_desk_delete_it_setting_pin_to_a_group = raiden_helper.send_request(
                    method='DELETE', url=flex_desk_delete_it_setting_pin_to_a_group_url,
                    body=json.dumps(flex_desk_delete_it_setting_pin_to_a_group_payload),
                    token=self.token
                )

                json_formatted_response = json.dumps(response_flex_desk_delete_it_setting_pin_to_a_group, indent=2)
                Report.logInfo(f'Delete IT setting pin to a group')
                Report.logResponse(json_formatted_response)

                # Validate Response
                if response_flex_desk_delete_it_setting_pin_to_a_group == []:
                    Report.logPass(f'Deleted IT setting pin successfully to a group')
                else:
                    Report.logFail(f'Failed to delete IT setting pin')
            else:
                Report.logInfo(f'Pin id is Null')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_add_different_pin_to_existing_pin(self, role, desk_it_pin, group_name):
        """
            Method to add a different PIN to the level with an existing PIN

            :param role:role of logged in user
            :param desk_it_pin: random pin generated for desk it pin setting
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_add_different_pin_to_existing_pin_payload = {
                "group": group_name,
                "pin": desk_it_pin,
                "label": "sync_it_pin",
                "type": "settings",
                "realm": "Desks"
            }

            flex_desk_add_different_pin_to_existing_pin_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin'
            Report.logInfo(
                f'Url to add different pin to the level with an existing PIN is: {flex_desk_add_different_pin_to_existing_pin_url}')

            response_flex_desk_add_different_pin_to_existing_pin = raiden_helper.send_request(
                method='PUT', url=flex_desk_add_different_pin_to_existing_pin_url,
                body=json.dumps(flex_desk_add_different_pin_to_existing_pin_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_add_different_pin_to_existing_pin, indent=2)
            Report.logInfo(f'Add different pin to the level with an existing PIN')
            Report.logResponse(json_formatted_response)

            response_name = response_flex_desk_add_different_pin_to_existing_pin['name']
            response_message = response_flex_desk_add_different_pin_to_existing_pin['message']

            # Validate Response
            if response_name == 'ConflictError' and response_message == 'PIN already set at this level':
                Report.logPass(f'Already IT setting pin set at this level')
            else:
                Report.logFail(f'Added new IT setting pin')

            return response_name

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_add_duplicate_pin_to_existing_pin(self, role, duplicate_pin, group_name):
        """
            Method to add a duplicate PIN to the level with an existing PIN

            :param role:role of logged in user
            :param duplicate_pin: existing pin generated for desk it pin setting
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_add_duplicate_pin_to_existing_pin_payload = {
                "group": group_name,
                "pin": duplicate_pin,
                "label": "sync_it_pin",
                "type": "settings",
                "realm": "Desks"
            }

            flex_desk_add_duplicate_pin_to_existing_pin_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin'
            Report.logInfo(
                f'Url to add duplicate pin to the level with an existing PIN is: {flex_desk_add_duplicate_pin_to_existing_pin_url}')

            response_flex_desk_add_duplicate_pin_to_existing_pin = raiden_helper.send_request(
                method='PUT', url=flex_desk_add_duplicate_pin_to_existing_pin_url,
                body=json.dumps(flex_desk_add_duplicate_pin_to_existing_pin_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_add_duplicate_pin_to_existing_pin, indent=2)
            Report.logInfo(f'Add duplicate pin to the level with an existing PIN')
            Report.logResponse(json_formatted_response)

            response_code = response_flex_desk_add_duplicate_pin_to_existing_pin['code']
            response_message = response_flex_desk_add_duplicate_pin_to_existing_pin['message']

            # Validate Response
            if response_code == 'PIN_EXISTS' and response_message == 'PIN Already Exists':
                Report.logPass(f'Already IT setting pin exists')
            else:
                Report.logFail(f'Response Status code and message didnot match')

            return response_code

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(self, role, desk_it_pin, group_name):
        """
            Method to verify adding IT Setting PIN with wrong length to a group

            :param role:role of logged in user
            :param desk_it_pin: random pin generated for desk it pin setting
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            flex_desk_add_it_setting_pin_payload = {
                "group": group_name,
                "pin": desk_it_pin,
                "label": "sync_it_pin",
                "type": "settings",
                "realm": "Desks"
            }

            flex_desk_add_it_setting_pin_payload_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/pin'
            Report.logInfo(
                f'Url to verify adding IT Setting PIN with wrong length to a group is: {flex_desk_add_it_setting_pin_payload}')

            response_flex_desk_add_it_setting_pin = raiden_helper.send_request(
                method='PUT', url=flex_desk_add_it_setting_pin_payload_url,
                body=json.dumps(flex_desk_add_it_setting_pin_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_flex_desk_add_it_setting_pin, indent=2)
            Report.logInfo(f'Verify to add IT setting pin to a group with different digits pin combination ')
            Report.logResponse(json_formatted_response)
            response_add_it_setting_pin = response_flex_desk_add_it_setting_pin['message']

            # Validate Response
            if response_add_it_setting_pin == 'Bad Request':
                Report.logPass(f'IT setting pin should be equal to 4 digits only')
            else:
                Report.logFail(f'Added IT setting pin successfully to a group')
                response_add_it_setting_pin = response_flex_desk_add_it_setting_pin[0]['id']

            return response_add_it_setting_pin

        except Exception as e:
            Report.logException(f'{e}')

    def get_desk_id_by_desk_name_in_organization(self, token: str, org_id: str, site: str, building: str, floor: str,
                                                 area: str, desk_name: str) -> str:
        """
        Get the desk od by desk name in the organization

        :param token:Sign in token
        :param org_id:
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        """
        try:
            session_context = raiden_helper.get_session_context_filter_by_orgid(
                global_variables.config, token, org_id,
            )
            alg_obj = RaidenAlgolia(session_context['search'])
            list_of_desks = alg_obj.algolia_get_list_of_desks
            desk_location = f"/{site}/{building}/{floor}/{area}/"
            for desk in list_of_desks:
                if str(desk['_highlightResult']['groupLabel']['value']).lower() == desk_location.lower():
                    if str(desk['_highlightResult']['name']['value']).lower() == desk_name.lower():
                        return desk['objectID']
            raise Exception("Desk not found")
        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def session_booking_for_existing_desk(self, token: str, org_id: str, email_id: str, site: str, building: str,
                                          floor: str, area: str,
                                          desk_name: str, start: str, end: str, day: int = 0):
        """
        Method to book a session for an existing desk

        :param token:Sign in token
        :param org_id:
        :param email_id:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param time_zone: Local Time Zone - Example 'America/Los_Angeles'
        :param day: 0 for current date, 1 for next day and so on
        """
        try:
            get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate'
            user_id = raiden_api_user_helper.get_end_user_id_from_email(email_id,
                                                                        get_users_url,
                                                                        token)
            user_name = raiden_api_user_helper.get_end_user_name_from_email(email_id,
                                                                            get_users_url,
                                                                            token)
            desk_id = self.get_desk_id_by_desk_name_in_organization(token, org_id, site,
                                                                    building, floor, area, desk_name)
            date = datetime.datetime.now().date() + timedelta(days=day)
            timezone = datetime.datetime.utcnow() - datetime.datetime.now()
            start_date_time = datetime.datetime.strptime(f"{date} {str(start).replace(' ', '')}", '%Y-%m-%d %I:%M%p') \
                              + timezone + timedelta(seconds=32)
            end_date_time = datetime.datetime.strptime(f"{date} {str(end).replace(' ', '')}", '%Y-%m-%d %I:%M%p') \
                            + timezone + timedelta(seconds=32)
            session_start_date = start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            session_end_date = end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            local_timezone = str(get_localzone())

            flex_desk_session_booking_payload = {
                'title': 'Sync Admin Reservation',
                'start': session_start_date,
                'stop': session_end_date,
                'tz': local_timezone,
                'user': {
                    'identifier': user_id,
                    'email': email_id,
                    'name': user_name
                }
            }

            flex_desk_session_booking_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/desk/{desk_id}/reservation'
            Report.logInfo(f'Url to book a session for desk is: {flex_desk_session_booking_url}')

            response_flex_desk_session_booking = raiden_helper.send_request(
                method='POST', url=flex_desk_session_booking_url, body=json.dumps(flex_desk_session_booking_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_session_booking, indent=2)
            Report.logInfo(f'Booking session for desk - {desk_name}')
            Report.logResponse(json_formatted_response)
            response_user_id = response_flex_desk_session_booking['reservations'][0]['organizer']['identifier']
            response_starts_at = response_flex_desk_session_booking['reservations'][0]['starts_at']
            response_ends_at = response_flex_desk_session_booking['reservations'][0]['ends_at']
            response_reservation_id = response_flex_desk_session_booking['reservations'][0]['identifier']

            # Validate Response
            if response_user_id == user_id and response_starts_at[0:16] in session_start_date and response_ends_at[
                                                                                                  0:16] in session_end_date:
                Report.logPass(f'Session booked for desk {desk_name} with email {email_id} successfully')
            else:
                Report.logFail(f'Failed to book session for desk {desk_name} with email {email_id}')

            return response_reservation_id

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_device_setting_usb_3_priority(self, token, org_id, device_id, high_speed_usb, desk_id):
        """
            Method to enable/disable USB 3.0 Priority

            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param high_speed_usb:setting to enable or disable USB 3.0 priority
            :param desk_id:Id for the desk created
        """
        try:

            flex_desk_device_setting_usb_3_priority_payload = {
                'coilyUsbSettings':
                    {
                        'highSpeedUsb': high_speed_usb
                    }
            }

            flex_desk_device_setting_usb_3_priority_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(f'Url to enable/disable USB 3.0 priority is: {flex_desk_device_setting_usb_3_priority_url}')

            response_flex_desk_device_setting_usb_3_priority = raiden_helper.send_request(
                method='PUT', url=flex_desk_device_setting_usb_3_priority_url,
                body=json.dumps(flex_desk_device_setting_usb_3_priority_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_device_setting_usb_3_priority, indent=2)
            Report.logInfo(f'Enable/Disable USB 3.0 priority is')
            Report.logResponse(json_formatted_response)

            # Get device details to fetch coily_high_speed_usb
            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{desk_id}/info'


            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = raiden_helper.send_request(
                    method='GET', url=info_url, token=token
                )

                if len(response_device_info['devices']) > 0:
                    coily_high_speed_usb = response_device_info['devices'][0]['state']['reported']['coilyUsbSettings'][
                    'highSpeedUsb']
                    print(f'Coily high_speed_usb is {coily_high_speed_usb}')
                    break
                else:
                    time.sleep(5)

            # Validate Response
            if coily_high_speed_usb == high_speed_usb and coily_high_speed_usb == 1:
                Report.logPass(f'USB 3.0 priority is successfully enabled')
            elif coily_high_speed_usb == high_speed_usb and coily_high_speed_usb == 0:
                Report.logPass(f'USB 3.0 priority is successfully disabled')
            else:
                Report.logFail(f'Failed to set the USB 3.0 priority settings to {high_speed_usb}')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_device_setting_disable_internet_time_set_ntp_server(self, token, org_id, device_id, ntp_server,
                                                                      desk_id):
        """
            Method to Disable internet time and set NTP server

            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param ntp_server:ntp server details
            :param desk_id:Id for the desk created
        """
        try:

            flex_desk_device_setting_disable_internet_time_set_ntp_server_payload = {
                'regionalSettings': {
                    'ntpServer': ntp_server
                }
            }

            flex_desk_device_setting_disable_internet_time_set_ntp_server_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(
                f'Url to Disable internet time and set NTP server is: {flex_desk_device_setting_disable_internet_time_set_ntp_server_url}')

            response_flex_desk_device_setting_disable_internet_time_set_ntp_server = raiden_helper.send_request(
                method='PUT', url=flex_desk_device_setting_disable_internet_time_set_ntp_server_url,
                body=json.dumps(flex_desk_device_setting_disable_internet_time_set_ntp_server_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_device_setting_disable_internet_time_set_ntp_server,
                                                 indent=2)
            Report.logInfo(f'Disable internet time and set NTP server is')
            Report.logResponse(json_formatted_response)

            # Get device details from coily
            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{desk_id}/info'

            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = raiden_helper.send_request(
                    method='GET', url=info_url, token=token
                )

                if len(response_device_info) > 0:
                    if ntp_server == 'time.android.com' or ntp_server == '0.us.pool.ntp.org' or ntp_server == 'time@android.com' or ntp_server == "":
                        ntp_server_url = response_device_info['devices'][0]['state']['reported']['regionalSettings'][
                            'ntpServer']
                        print(f'NTP server url is {ntp_server_url}')

                    if ntp_server == 'time@android.com':
                        response_message = response_flex_desk_device_setting_disable_internet_time_set_ntp_server[
                                'message']
                    else:
                        response_message = None
                    break
                else:
                    time.sleep(5)

            # Validate Response
            if ntp_server_url == ntp_server and ntp_server == 'time.android.com':
                Report.logPass(f'Internet time is successfully disabled and NTP server is set to {ntp_server}')
            elif ntp_server_url == ntp_server and ntp_server == '0.us.pool.ntp.org':
                Report.logPass(f'Internet time is successfully disabled and NTP server is set to {ntp_server}')
            elif ntp_server_url == ntp_server and ntp_server is "":
                Report.logPass(f'Enabled Auto - Configuration of internet time')
            elif ntp_server_url != ntp_server and response_message == 'Bad Request':
                Report.logPass(f'BadRequestError is shown in response for NTP server {ntp_server} which is expected behavior')
            else:
                Report.logFail(f'Failed to set Internet time and NTP server to {ntp_server}')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def update_booking_session(self, token: str, org_id: str, desk_id: str, reservation_id: str,
                               start: str, end: str, day: int = 0):
        """
        Method to update booking session

        :param reservation_id:
        :param token:Sign in token
        :param org_id:
        :param desk_id:
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param day: 0 for current date, 1 for next day and so on
        """
        try:

            date = datetime.datetime.now().date() + timedelta(days=day)
            timezone = datetime.datetime.utcnow() - datetime.datetime.now() + timedelta(seconds=32)
            start_date_time = datetime.datetime.strptime(f"{date} {str(start).replace(' ', '')}", '%Y-%m-%d %I:%M%p') \
                              + timezone
            end_date_time = datetime.datetime.strptime(f"{date} {str(end).replace(' ', '')}", '%Y-%m-%d %I:%M%p') \
                            + timezone
            session_start_date = start_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            session_end_date = end_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            local_timezone = str(get_localzone())

            flex_desk_modify_desk_reservation_payload = {
                'title': 'Reservation',
                'start': session_start_date,
                'stop': session_end_date,
                'tz': local_timezone,
                'resourceId': desk_id
            }

            update_session_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/desk/{desk_id}/reservation/{reservation_id}'

            response_flex_desk_session_booking = raiden_helper.send_request(
                method='PUT', url=update_session_url,
                body=json.dumps(flex_desk_modify_desk_reservation_payload),
                token=token
            )

            response_starts_at = response_flex_desk_session_booking['reservations'][0]['starts_at']
            response_ends_at = response_flex_desk_session_booking['reservations'][0]['ends_at']
            response_reservation_id = response_flex_desk_session_booking['reservations'][0]['identifier']

            # Validate Response
            if response_reservation_id == reservation_id and response_starts_at[
                                                             0:16] in session_start_date and response_ends_at[
                                                                                             0:16] in session_end_date:
                Report.logPass(f'Desk reservation modified successfully for desk id {desk_id}')
            else:
                Report.logFail(f'Failed to modify reserved desk for desk id {desk_id}')
        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_device_setting_local_area_network_status(self, token, org_id, device_id, local_area_network,
                                                           desk_id):
        """
            Method to enable/disable Local Area Network

            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param local_area_network:local area network status
            :param desk_id:Id for the desk created
        """
        try:

            flex_desk_device_setting_local_area_network_payload = {
                'lnaSettings':
                    {
                        'on': local_area_network,
                        'version': 2
                    }
            }

            flex_desk_device_setting_local_area_network_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(
                f'Url to enable/disable Local Area Network is: {flex_desk_device_setting_local_area_network_url}')

            response_flex_desk_device_setting_local_area_network = raiden_helper.send_request(
                method='PUT', url=flex_desk_device_setting_local_area_network_url,
                body=json.dumps(flex_desk_device_setting_local_area_network_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_device_setting_local_area_network, indent=2)
            Report.logInfo(f'Enable/Disable Local Area Network is')
            Report.logResponse(json_formatted_response)

            # Get coily's local area network status
            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{desk_id}/info'

            timer = 7
            while timer > 0:
                timer -= 1
                response_device_info = raiden_helper.send_request(
                    method='GET', url=info_url, token=token
                )

                if len(response_device_info) > 0:
                    coily_local_area_network = response_device_info['devices'][0]['state']['reported']['lnaSettings'][
                        'on']
                    print(f'Coily local area network status is {coily_local_area_network}')
                    break
                else:
                    time.sleep(5)

            # Validate Response
            if coily_local_area_network == local_area_network and coily_local_area_network == 1:
                Report.logPass(f'Local area network status is successfully enabled')
            elif coily_local_area_network == local_area_network and coily_local_area_network == 0:
                Report.logPass(f'Local area network status is successfully disabled')
            else:
                Report.logFail(f'Failed to set the local area network status to {local_area_network}')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_device_setting_local_area_network_change_password(self, token, org_id, device_id,
                                                                    local_area_network_password):
        """
            Method to change password of local area network

            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param local_area_network_password:Changing the password of local area network
        """
        try:

            flex_desk_local_area_network_password_change_payload = \
                {
                    'lnaSettings':
                        {
                            'on': 1,
                            'password': local_area_network_password,
                            "version": 2
                        }
                }

            flex_desk_local_area_network_password_change_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(
                f'Url to to change password of local area network is: {flex_desk_local_area_network_password_change_url}')

            response_flex_desk_local_area_network_password_change = raiden_helper.send_request(
                method='PUT', url=flex_desk_local_area_network_password_change_url,
                body=json.dumps(flex_desk_local_area_network_password_change_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_local_area_network_password_change, indent=2)
            Report.logInfo(f'Response to change password of local area network is')
            Report.logResponse(json_formatted_response)

            if local_area_network_password == "" or len(local_area_network_password) < 8:
                response_message = response_flex_desk_local_area_network_password_change['message']
            else:
                response_message = response_flex_desk_local_area_network_password_change

            # Validate Response, logging to sync app with updated password
            if response_flex_desk_local_area_network_password_change == {}:
                sync_page = self.lna.login_to_local_network_access(ip_address=fp.COILY_IP,
                                                                   user_name=self.sync_app.lna_user,
                                                                   password=local_area_network_password).click_sync()
                sync_page.verify_disconnect_from_sync_button_displayed()
                if local_area_network_password != 'Logi@3456':
                    Report.logPass(f'Local area network changed successfully to {local_area_network_password}')
                else:
                    Report.logPass(f'Local area network password changed to default password successfully')
            elif response_message == 'Bad Request':
                Report.logResponse(
                    f'Cannot change local area network password as entered password doesnot match allowed types')
            else:
                Report.logFail(f'Failed to change the local area network password to {local_area_network_password}')

            return True

        except Exception as e:
            Report.logException(f'{e}')


    def get_active_sessions_for_user(self, token: str, org_id: str, email_id: str) -> list:
        """
        Method to get all active sessions for user until next 30 days (Max 30 days user can book desk)

        :param token:Sign in token
        :param org_id:
        :param email_id: Email ID of user
        :return active_reservations: List of active reservations Desk Id, Reservation ID
        """
        try:

            get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate'
            user_id = raiden_api_user_helper.get_end_user_id_from_email(email_id,
                                                                        get_users_url,
                                                                        token)
            current_utc = datetime.datetime.utcnow()
            future_utc = current_utc + timedelta(days=30)
            start = current_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            end = future_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            url = f"{global_variables.config.BASE_URL}api/org/{org_id}/associate/{user_id}/reservation?start={start}&stop={end}&include=session_type"

            response_get = raiden_helper.send_request(
                method='GET', url=url, token=token,
            )

            active_reservations = []
            for reservation in response_get['reservations']:
                active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))
            return active_reservations
        except Exception as e:
            Report.logException(f'{e}')

    def delete_all_sessions_for_user(self, token: str, org_id: str, email_id: str):
        """
        Method to all active sessions for the user

        :param token:Sign in token
        :param org_id:
        :param email_id: Email ID of user
        :return :
        """
        try:
            active_reservations = self.get_active_sessions_for_user(token=token, org_id=org_id, email_id=email_id)
            for reservation in active_reservations:
                self.flex_desk_delete_reserved_desk(token=token, org_id=org_id, desk_id=reservation[0],
                                                    reservation_id=reservation[1])
        except Exception as e:
            Report.logException(f'{e}')


    def flex_desk_reboot_device(self, token, org_id, desk_id, device_id):
        """
            Method to reboot the device

            :param token:token to authenticate user
            :param org_id:Organization id
            :param desk_id: Id for the desk created
            :param device_id: Coily device id
        """
        try:

            flex_desk_reboot_device_payload = \
                {
                    'deviceIds': [device_id],
                    'strategy': 2

                }

            flex_desk_reboot_device_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/reboot'
            Report.logInfo(
                f'Url to reboot the device is: {flex_desk_reboot_device_url}')

            response_flex_desk_reboot_device = raiden_helper.send_request(
                method='POST', url=flex_desk_reboot_device_url,
                body=json.dumps(flex_desk_reboot_device_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_reboot_device, indent=2)
            Report.logInfo(f'Response to reboot the device is')
            Report.logResponse(json_formatted_response)

            if response_flex_desk_reboot_device == {}:
                Report.logInfo(f'Rebooted the device')
            else:
                Report.logInfo(f'Failed to reboot the device')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def flex_desk_deprovision_device(self, token, org_id, device_id, desk_id, desk_name):
        """
            Method to deprovision the device

            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param desk_id:Id of the created desk
        """
        try:

            flex_desk_deprovision_device_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/device/{device_id}'
            Report.logInfo(
                f'Url to deprovision the device is: {flex_desk_deprovision_device_url}')

            response_flex_desk_deprovision_device = raiden_helper.send_request(
                method='DELETE', url=flex_desk_deprovision_device_url, token=token
            )

            json_formatted_response = json.dumps(response_flex_desk_deprovision_device, indent=2)
            Report.logInfo(f'Response to deprovision the device is')
            Report.logResponse(json_formatted_response)

            return response_flex_desk_deprovision_device

        except Exception as e:
            Report.logException(f'{e}')

    def get_desk_activity_details(self, token, org_id, desk_id):
        """
            Method to get desk activity details
            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id: Coily device id
            :param desk_id:Id for the desk created
        """
        try:
            desk_activity_details_payload = {
                'length': 50,
                'categories': [],
                'triggers': []
            }
            desk_activity_details_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/events/search'
            Report.logInfo(f'Url to get desk activity details is: {desk_activity_details_url}')
            response_desk_activity_details = raiden_helper.send_request(
                method='POST', url=desk_activity_details_url,
                body=json.dumps(desk_activity_details_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_desk_activity_details, indent=2)
            Report.logInfo(f'Get desk activity details is below:')
            Report.logResponse(json_formatted_response)
            # Validate Response
            for item in range(len(response_desk_activity_details['events'])):
                res_dict = response_desk_activity_details['events'][item]
                if res_dict['eventType'] == 'DeviceConnected' or res_dict['eventType']  == 'RoomProvisionedPortal':
                    Report.logPass(f'Desk Activity is retrieved successfully')
                else:
                    Report.logFail(f'Failed to retrieve desk activity')
                return True
        except Exception as e:
            Report.logException(f'{e}')

    def add_map_to_organization(self, token, org_id,map_name, data_image, map_width, map_height, map_scale):
        """
            Method to add map to organization

            :param token:token to authenticate user
            :param org_id:Organization id
        """
        try:

            add_maps_to_organization_payload = {
                'name': map_name,
                'data': data_image,
                'width': map_width,
                'height': map_height,
                'scale': map_scale
            }

            add_maps_to_organization_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map'
            Report.logInfo(
                f'Url to add maps to organization is: {add_maps_to_organization_url}')

            response_add_maps_to_organization = raiden_helper.send_request(
                method='POST', url=add_maps_to_organization_url,
                body=json.dumps(add_maps_to_organization_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_add_maps_to_organization, indent=2)
            Report.logInfo(f'Response to add maps to organization is')
            Report.logResponse(json_formatted_response)
            map_id = response_add_maps_to_organization['id']
            floor_path = response_add_maps_to_organization['content']['floor']['paths'][0]
            org_identifier = response_add_maps_to_organization['org_identifier']

            if response_add_maps_to_organization['name'] == map_name:
                Report.logInfo(f'Maps added successfully to organization')
            else:
                Report.logInfo(f'Failed to add map to organization')
            return map_id, floor_path, token, org_id, org_identifier

        except Exception as e:
            Report.logException(f'{e}')

    def get_organization_map_details(self, token, org_id, map_id):
        """
            Method to get map details of organization

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
        """
        try:

            get_organization_map_details_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map'
            Report.logInfo(
                f'Url to get maps details of organization is: {get_organization_map_details_url}')

            response_get_organization_map_details = raiden_helper.send_request(
                method='GET', url=get_organization_map_details_url,
                token=token
            )

            json_formatted_response = json.dumps(response_get_organization_map_details, indent=2)
            Report.logInfo(f'Response to get maps details of organization is')
            Report.logResponse(json_formatted_response)


            # for item in response_get_organization_map_details:
            #     if item['id'] in response_get_organization_map_details:
            for item in response_get_organization_map_details:
                if map_id in item['id']:
                    if map_id == item['id']:
                        Report.logInfo(f'Organization Maps details are retrieved successfully')
                        break
                    else:
                        Report.logInfo(f'Failed to retrieve maps details of organization')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def get_maps_under_unassigned_section(self, token, org_id):
        """
            Method to Get map(s) under unassigned section

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
        """
        try:

            get_unassigned_maps_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/unassigned'
            Report.logInfo(
                f'Url to get map(s) under unassigned section is: {get_unassigned_maps_url}')

            response_get_unassigned_maps = raiden_helper.send_request(
                method='GET', url=get_unassigned_maps_url,
                token=token
            )

            json_formatted_response = json.dumps(response_get_unassigned_maps, indent=2)
            Report.logInfo(f'Response to get map(s) under unassigned section is')
            Report.logResponse(json_formatted_response)

            for item in response_get_unassigned_maps:
                if len(response_get_unassigned_maps) > 0:
                    map_name = item['name']
                    Report.logInfo(f'Unassigned map name is {map_name} ')
                else:
                    Report.logInfo(f'Failed to retrieve unassigned maps details of organization')
            return "Unassigned map details are retrieved successfully"

        except Exception as e:
            Report.logException(f'{e}')

    def link_map_to_site_building_floor(self, token, org_id, map_id, site_location_id, building_location_id, floor_location_id, location_path):
        """
            Method to link map to site, building, floor

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
            :param site_location_id:Location Id for the site group
            :param building_location_id:Location Id for the building group
            :param floor_location_id:Location Id for the floor group
            :param location_path:Path till the floor group

        """
        try:

            link_map_to_site_building_floor_payload = {
                 'site': site_location_id,
                 'building': building_location_id,
                 'floor': floor_location_id,
                 'path': location_path
                }

            link_map_to_site_building_floor_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}/location'
            Report.logInfo(
                f'Url to link map to site building floor is: {link_map_to_site_building_floor_url}')

            response_link_map_to_site_building_floor = raiden_helper.send_request(
                method='PUT', url=link_map_to_site_building_floor_url, body=json.dumps(link_map_to_site_building_floor_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_link_map_to_site_building_floor, indent=2)
            Report.logInfo(f'Response to link map to site building floor is')
            Report.logResponse(json_formatted_response)

            if response_link_map_to_site_building_floor['location']['floor'] == floor_location_id:
                Report.logInfo(f' Successfully linked map id {map_id} to site building floor {location_path} ')
            else:
                Report.logInfo(f'Failed to link map to path {location_path}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def get_maps_associated_with_building(self, token, org_id, map_id, building_location_id):
        """
            Method to get map associated with building

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
            :param building_location_id:Location Id for the building group

        """
        try:

            get_maps_associated_with_building_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/building/{building_location_id}/map'
            Report.logInfo(
                f'Url to get map associated with building is: {get_maps_associated_with_building_url}')

            response_get_maps_associated_with_building = raiden_helper.send_request(
                method='GET', url=get_maps_associated_with_building_url, token=token
            )

            json_formatted_response = json.dumps(response_get_maps_associated_with_building, indent=2)
            Report.logInfo(f'Response to get map associated with building is')
            Report.logResponse(json_formatted_response)

            for item in response_get_maps_associated_with_building:
                if response_get_maps_associated_with_building[0]['location']['building'] == building_location_id:
                    response_map_id = response_get_maps_associated_with_building[0]['id']
                    response_map_name = response_get_maps_associated_with_building[0]['name']
                    if response_map_id == map_id:
                        Report.logInfo(f' Successfully retrieved map name {response_map_name} for the building {building_location_id}')
                    else:
                        Report.logInfo(f'Failed to get maps associated with building {building_location_id}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def rename_map(self, token, org_id, map_id, map_name):
        """
            Method to rename the map
            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
            :param map_name: Map name created
        """
        try:
            renamed_map = map_name + "_renamed"
            rename_map_payload = {
                'name': renamed_map,
            }

            rename_map_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}/name'
            Report.logInfo(
                f'Url to rename map is: {rename_map_url}')

            response_rename_map = raiden_helper.send_request(
                method='PUT', url=rename_map_url, body=json.dumps(rename_map_payload), token=token
            )

            json_formatted_response = json.dumps(response_rename_map, indent=2)
            Report.logInfo(f'Response to rename map is')
            Report.logResponse(json_formatted_response)

            if renamed_map in response_rename_map['name']:
                    Report.logInfo(f'Map is renamed successfully')
            else:
                    Report.logInfo(f'Failed to rename map')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def delete_map(self, token, org_id, map_id):
        """
            Delete Map created

        :param map_id: Id of the map created
        :param org_id:Org id under which map is created
        :param token:
        """
        try:
            Report.logInfo(f'Delete map under org id - {org_id}')

            delete_map_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}'
            Report.logInfo(
                f'Url to delete map is: {delete_map_url}')

            response_delete_map = raiden_helper.send_request(
                method='DELETE', url=delete_map_url, token=token
            )

            json_formatted_response = json.dumps(response_delete_map, indent=2)
            Report.logInfo(f'Response to delete map is')
            Report.logResponse(json_formatted_response)

            if response_delete_map['deleted'] == map_id:
                Report.logPass(f'Successfully deleted map {map_id}')
            else:
                Report.logFail(f'Failed to delete of map {map_id}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def reassign_map_to_another_floor(self, token, org_id, map_id, site_location_id, building_location_id, floor_location_id, new_location_path):
        """
            Method to re-assign map to another floor

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
            :param site_location_id:Location Id for the site group
            :param building_location_id:Location Id for the building group
            :param floor_location_id:Location Id for the floor group
            :param new_location_path:Path to the new floor group

        """
        try:

            reassign_map_to_another_floor_payload = {
                 'site': site_location_id,
                 'building': building_location_id,
                 'floor': floor_location_id,
                 'path': new_location_path
                }

            reassign_map_to_another_floor_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}/location'
            Report.logInfo(
                f'Url to re-assign map to another floor is: {reassign_map_to_another_floor_url}')

            response_reassign_map_to_another_floor = raiden_helper.send_request(
                method='PUT', url=reassign_map_to_another_floor_url, body=json.dumps(reassign_map_to_another_floor_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_reassign_map_to_another_floor, indent=2)
            Report.logInfo(f'Response to re-assign map to another floor is')
            Report.logResponse(json_formatted_response)

            if new_location_path in response_reassign_map_to_another_floor['location']['path']:
                Report.logInfo(f' Successfully re-assigned map to another floor location {new_location_path} ')
            else:
                Report.logInfo(f'Failed to re-assign map to another floor {new_location_path}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def change_map_status_hidden_to_visible(self, token, org_id, map_id):
        """
            Method to change the map status from hidden to visible
            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_id:Id for map created in organization
        """
        try:
            map_status_hidden_to_visible_payload = {
                'published': True,
            }

            map_status_hidden_to_visible_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}/status'
            Report.logInfo(
                f'Url to change the map status from hidden to visible is: {map_status_hidden_to_visible_url}')

            response_map_status_hidden_to_visible = raiden_helper.send_request(
                method='PUT', url=map_status_hidden_to_visible_url, body=json.dumps(map_status_hidden_to_visible_payload), token=token
            )

            json_formatted_response = json.dumps(response_map_status_hidden_to_visible, indent=2)
            Report.logInfo(f'Response change the map status from hidden to visible is')
            Report.logResponse(json_formatted_response)

            now = datetime.datetime.now(datetime.timezone.utc)
            published_at_time = now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:4] + 'Z'

            if published_at_time[0:17] in response_map_status_hidden_to_visible['published_at']:
                    Report.logInfo(f'Changed the map status from hidden to visible successfully')
            else:
                    Report.logInfo(f'Failed to change the map status from hidden to visible')
            return published_at_time

        except Exception as e:
            Report.logException(f'{e}')

    def get_peripheral_use_state(self, token, org_id, desk_id):
        """
            Method to get peripheral use state information
            :param token:token to authenticate user
            :param org_id:Organization id
            :param desk_id:Id for the desk created
        """
        try:
            get_peripheral_use_state_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/info'
            Report.logInfo(f'Url to get peripheral use state information is: {get_peripheral_use_state_url}')

            response_peripheral_use_state = raiden_helper.send_request(
                method='GET', url=get_peripheral_use_state_url,
                token=token
            )
            json_formatted_response = json.dumps(response_peripheral_use_state, indent=2)
            Report.logInfo(f'Get peripheral use state information is below:')
            Report.logResponse(json_formatted_response)

            # Validate Response
            for item in range(len(response_peripheral_use_state['devices'])):
                peripheral_health_status = response_peripheral_use_state['devices'][item]['state']['reported']['healthStatus']
                peripheral_update_status = response_peripheral_use_state['devices'][item]['state']['reported']['updateStatus']
                peripheral_status = response_peripheral_use_state['devices'][item]['state']['reported']['status']
                Report.logInfo(
                    f'Peripheral health status is {peripheral_health_status}, update status is {peripheral_update_status}')
                if peripheral_health_status == 0 or peripheral_health_status == 1 or peripheral_update_status == 0 or peripheral_update_status == 1:
                    Report.logPass(f'Peripheral health and update status is retrieved successfully')
                    Report.logPass(f'Peripheral status is {peripheral_status}')
                else:
                    Report.logFail(f'Failed to retrieve peripheral use state')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def get_active_sessions_for_desk(self, token: str, org_id: str, site: str, building:str, floor: str,
                                     area: str, desk_name: str) -> list:
        """
        Method to get all active sessions for desk next 30 days (Max 30 days user can book desk)

        :param token:Sign in token
        :param org_id:
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :return active_reservations: List of active reservations Desk Id, Reservation ID
        """
        try:

            desk_id = self.get_desk_id_by_desk_name_in_organization(token=token, org_id=org_id, site=site,
                                                                    building=building, floor=floor, area=area,
                                                                    desk_name=desk_name)
            current_utc = datetime.datetime.utcnow()
            future_utc = current_utc + timedelta(days=30)
            start = current_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            end = future_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            url = f"{global_variables.config.BASE_URL}api/org/{org_id}/desk/{desk_id}/reservation?start={start}&stop={end}&include=session_type"

            response_get = raiden_helper.send_request(
                method='GET', url=url, token=token,
            )

            active_reservations = []
            for reservation in response_get['reservations']:
                active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))
            return active_reservations
        except Exception as e:
            Report.logException(f'{e}')

    def delete_all_bookings_for_desk(self, token: str, org_id: str, site: str, building:str, floor: str,
                                     area: str, desk_name: str):
        """
        Method to get all active sessions for desk next 30 days (Max 30 days user can book desk)

        :param token:Sign in token
        :param org_id:
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :return active_reservations: List of active reservations Desk Id, Reservation ID
        """
        try:
            active_reservations = self.get_active_sessions_for_desk(token=token, org_id=org_id, site=site,
                                                                    building=building, floor=floor, area=area,
                                                                    desk_name=desk_name)
            for reservation in active_reservations:
                self.flex_desk_delete_reserved_desk(token=token, org_id=org_id, desk_id=reservation[0],
                                                    reservation_id=reservation[1])
        except Exception as e:
            Report.logException(f'{e}')

    def update_desk_policy_settings(self, token: str, org_id: str, group_path: str,
                                    reserve_remotely: bool = True,
                                    max_days_in_advance: int = 14,
                                    check_in_time_limit: int = 600,
                                    walk_in_session_duration: int = 1,
                                    walk_in_notify_duration: int = 300,
                                    session_time_limit: int = None,
                                    hardstop_from_reusing: int = None,
                                    reserved_spot_visible: bool = True,
                                    show_qr_code: bool = True
                                    ) -> bool:
        """
        Method to update desk policy settings and validate correct values are set

        :param show_qr_code: bool
        :param reserved_spot_visible: bool
        :param hardstop_from_reusing: Time in Seconds. If passed None, Auto extend session will be turned ON
        :param session_time_limit: Time in Hours. If passed None, Session time limit will be turned off
        :param walk_in_notify_duration: Time in seconds
        :param walk_in_session_durtion: Time in Hours. If passed None, walk-in will be turned off
        :param check_in_time_limit: Time in Seconds. If passed None, Check-in required will be turned off
        :param max_days_in_advance: days 1 to 30
        :param reserve_remotely: bool
        :param org_id:
        :param token:
        :param group_path: Path of area, floor, building or site
                            e.g. /site/building/floor/area (setting at area level)
                            /site/building/floor (setting at floor level)
                            /site/building (setting at building level)
                            /site (setting at site level)
        :return bool:
        """
        try:
            desk_policy_payload = {
                'group': group_path,
                'reservationPolicy': {'qrCheckInRequiredTimeLimit': None,
                                      'qrCodeReservation': show_qr_code,
                                      'officeStartHours': None,
                                      'maxDaysInAdvance': max_days_in_advance,
                                      'officeEndHours': None,
                                      'reservedSessionDefaultDuration': 5,
                                      'reserveRemotely': reserve_remotely,
                                      'reservationTimeLimit': session_time_limit,
                                      'reservedSpotVisibleToOthers': reserved_spot_visible},
                'coilySettings': {
                    'walkInSessionDefaultDuration': walk_in_session_duration,
                    'notifyUserBeforeDeskReleased': walk_in_notify_duration,
                    'generateLongOccupancyAlertThreshold': None,
                    'hardStopBlockFromReusing': hardstop_from_reusing,
                    'enforceCheckInTimeLimit': check_in_time_limit,
                    'requireCleaning': False
                }
            }
            desk_policy_settings_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/policy/desk-settings'
            response = raiden_helper.send_request(
                method='POST', url=desk_policy_settings_url, body=json.dumps(desk_policy_payload), token=token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(json_formatted_response)

            flag = True
            if desk_policy_payload['reservationPolicy'] == response['policy']['reservationPolicy']:
                Report.logPass("Correct values are set for Reservation Policy")
            else:
                flag = False
                Report.logFail("Incorrect values are set for Reservation Policy")
                Report.logResponse(f"Expected Values\n{desk_policy_payload['reservationPolicy']}\n"
                                   f"Actual Values\n{response['policy']['reservationPolicy']}")
            if desk_policy_payload['coilySettings'] == response['policy']['coilySettings']:
                Report.logPass("Correct values are set for Coily Settings")
            else:
                flag = False
                Report.logFail("Incorrect values are set for Coily Settings")
                Report.logResponse(f"Expected Values\n{desk_policy_payload['coilySettings']}\n"
                                   f"Actual Values\n{response['policy']['coilySettings']}")

            return flag

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def flex_desk_change_group_settings_of_area(self, token, org_id, desk_id, area, ntp_server, lna_password,
                                                default_password, empty_desk_id):
        """
            Method to change group settings of an area

            :param token:token to authenticate user
            :param org_id:Organization id
        """
        try:

            change_group_settings_of_area_payload = {
                'regionalSettings':
                    {
                        'ntpServer': ntp_server,
                    },
                'lnaSettings':
                    {
                        'on': 1,
                        'password': lna_password,
                        'version': 2
                    },
                'coilyUsbSettings':
                    {
                        'highSpeedUsb': 0
                    },
                'realm': 'Desks',
                'group': area
            }

            change_group_settings_of_area_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/policy/device-settings/Coily'
            Report.logInfo(
                f'Url to change group settings of an area is: {change_group_settings_of_area_url}')

            response_change_group_settings_of_area = raiden_helper.send_request(
                method='POST', url=change_group_settings_of_area_url,
                body=json.dumps(change_group_settings_of_area_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_change_group_settings_of_area, indent=2)
            Report.logInfo(f'Change group settings of an area is')
            Report.logResponse(json_formatted_response)

            time.sleep(50)

            # Get the device information to fetch the internet time, LNA settings and high speed USB setting
            device_information_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{empty_desk_id}/info'

            response_device_information = raiden_helper.send_request(
                method='GET', url=device_information_url, token=token
            )

            for list_item in range(len(response_device_information['devices'])):
                device_type = response_device_information['devices'][list_item]['type']
                if device_type == 'Coily':
                    devices_state_reported = {}
                    devices_state_reported = response_device_information['devices'][list_item]['state']['reported']
                    for dict_item in devices_state_reported:
                        if dict_item == 'coilyUsbSettings':
                            if devices_state_reported[dict_item]['highSpeedUsb'] == 0:
                                Report.logInfo(f'Coily Usb Settings, highSpeedUsb is updated successfully')
                            else:
                                Report.logInfo(f'Coily Usb Settings, highSpeedUsb is not updated')
                        elif dict_item == 'lnaSettings':
                            if devices_state_reported[dict_item]['on'] == 1:
                                Report.logInfo(f'LNA Settings is updated successfully')
                            else:
                                Report.logInfo(f'LNA Settings is not updated')
                        elif dict_item == 'regionalSettings':
                            if devices_state_reported[dict_item]['ntpServer'] == ntp_server:
                                Report.logInfo(f'Regional Settings ntp server is updated successfully')
                            else:
                                Report.logInfo(f'Regional Settings, highSpeedUsb is not updated')

            # Validate for updated password by logging to sync app with updated password
            sync_page = self.lna.login_to_local_network_access(ip_address=fp.COILY_IP,
                                                                       user_name=self.sync_app.lna_user,
                                                                       password=lna_password).click_sync()
            if sync_page.verify_disconnect_from_sync_button_displayed():
                Report.logPass(f'Local area network password updated successfully')
            else:
                Report.logPass(f'Local area network password is not updated')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def set_local_area_network_password(self, token, org_id, lna_password, area):
        """
            Method to set the local area network password
            :param token:token to authenticate user
            :param org_id:Organization id
            :param device_id:Device id of Coily
            :param lna_password: password of local area network which has to be set
            :param area: group name
        """
        try:

            set_local_area_network_password_payload = {
                'lnaSettings':
                    {
                        'on': 1,
                        'password': lna_password,
                        'version': 2
                    },
                'realm': 'Desks',
                'group': area
            }

            set_local_area_network_password_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/policy/device-settings/Coily'
            Report.logInfo(
                f'Url to set the local area network password is: {set_local_area_network_password_url}')

            response_set_local_area_network_password = raiden_helper.send_request(
                method='POST', url=set_local_area_network_password_url,
                body=json.dumps(set_local_area_network_password_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_set_local_area_network_password, indent=2)
            Report.logInfo(f'Response to set the local network area password is')
            Report.logResponse(json_formatted_response)

            # Validate for updated password by logging to sync app with updated password
            sync_page = self.lna.login_to_local_network_access(ip_address=fp.COILY_IP,
                                                               user_name=self.sync_app.lna_user,
                                                               password=lna_password).click_sync()
            if sync_page.verify_disconnect_from_sync_button_displayed():
                Report.logPass(f'Local area network password updated successfully')
            else:
                Report.logPass(f'Local area network password is not updated')

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def get_coily_insight_information(self, token, org_id, user_id, desk_id, site):
        """
            Method to get coily insight information
            :param token:token to authenticate user
            :param org_id:Organization id
            :param user_id: user id of the end user created
            :param desk_id:Id for the desk created
        """
        try:

            # Get insights data associated with end user
            session_start_date = datetime.datetime.today() + datetime.timedelta(-30)
            start_date = session_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            Report.logInfo(f'session_start_date is {start_date}')

            session_end_date = datetime.datetime.today()
            end_date = session_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            Report.logInfo(f'session_end_date is {end_date}')

            get_user_insight_data_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/associate/{user_id}/insights?start={start_date}&stop={end_date}'

            Report.logInfo(f'Url to get insights data associated with end user is: {get_user_insight_data_url}')

            response_user_insight_data = raiden_helper.send_request(
                method='GET', url=get_user_insight_data_url,
                token=token
            )
            json_formatted_response = json.dumps(response_user_insight_data, indent=2)
            Report.logInfo(f'Get insights data associated with end user is below:')
            Report.logResponse(json_formatted_response)

            # Get Insights data associated with desk
            session_start_date = datetime.datetime.today() + datetime.timedelta(-7)
            start_date = session_start_date.strftime("%Y-%m-%d")
            Report.logInfo(f'session_start_date is {start_date}')

            session_end_date = datetime.datetime.today()
            end_date = session_end_date.strftime("%Y-%m-%d")
            Report.logInfo(f'session_end_date is {end_date}')

            get_desk_insight_data_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/desk/{desk_id}/insights?start={start_date}&stop={end_date}'

            Report.logInfo(f'Url to get insights data associated with desk is: {get_desk_insight_data_url}')

            response_desk_insight_data = raiden_helper.send_request(
                method='GET', url=get_desk_insight_data_url,
                token=token
            )
            json_formatted_response = json.dumps(response_desk_insight_data, indent=2)
            Report.logInfo(f'Get insights data associated with desk is below:')
            Report.logResponse(json_formatted_response)

            # Get Insights data- site level

            get_site_level_insight_data_payload = {

                'group' : site,
                'start' : start_date,
                'stop' : end_date

            }

            get_site_level_insight_data_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/desk/insights?group=%2Fsite%2F&start={start_date}&stop={end_date}'

            Report.logInfo(f'Url to get site level insight data is: {get_site_level_insight_data_url}')

            response_site_level_insight_data = raiden_helper.send_request(
                method='GET', url=get_site_level_insight_data_url,
                body=json.dumps(get_site_level_insight_data_payload),
                token=token
            )
            json_formatted_response = json.dumps(response_site_level_insight_data, indent=2)
            Report.logInfo(f'Get site level insights data is below:')
            Report.logResponse(json_formatted_response)

            # Validate Response
            for item in response_site_level_insight_data['desks']:
                if desk_id == item['id']:
                    Report.logPass(f'Site level insight data retrieved successfully')
                else:
                    Report.logFail(f'Failed to retrieve site level insight data')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def schedule_firmware_update_flexdesk(self, token, org_id, device_id, desk_name, desk_id):
        """
            Schedule firmware update for flex desk

            :param token: token key generated to authenticate user
            :param org_id:Org id under which map is created
            :param device_id: Flex desk device id
            :param desk_name:Name of the created desk
            :param desk_id: Id of the created desk
        """

        try:
            Report.logInfo(f'Schedule firmware update for flex desk under org id - {org_id}')

            # Get the latest firmware version
            response_device_info = self.get_coily_desk_information(desk_name, desk_id)

            collabos_available_software = response_device_info['devices'][0]['asw']
            collabos_available_software_timestamp = response_device_info['devices'][0]['aswts']
            collabos_nextManifest = response_device_info['devices'][0]['nextManifest']

            current_utc = datetime.datetime.utcnow()
            nearest_schedule_time = current_utc + (datetime.datetime.min - current_utc) % timedelta(minutes=30)
            future_utc = nearest_schedule_time + timedelta(hours=2)
            time_from = nearest_schedule_time.strftime("%Y-%m-%dT%H:%M:%S")
            time_to = future_utc.strftime("%Y-%m-%dT%H:%M:%S")
            Report.logInfo(f'Firmware update is scheduled from time {time_from} to {time_to}')

            schedule_fw_update_flexdesk_payload = {
                  'deviceIds': [
                    device_id
                  ],
                  'schedule': {
                    'sw': collabos_available_software,
                    'swts': collabos_available_software_timestamp,
                    'when': {
                        'from': time_from,
                        'to': time_to
                    },
                    'manifest': collabos_nextManifest
                  }
                }

            schedule_fw_update_flexdesk_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/software'
            Report.logInfo(
                f'Url to schedule firmware update to flexdesk is: {schedule_fw_update_flexdesk_url}')

            response_schedule_fw_update_flexdesk = raiden_helper.send_request(
                method='POST', url=schedule_fw_update_flexdesk_url, body=json.dumps(schedule_fw_update_flexdesk_payload), token=token
            )

            json_formatted_response = json.dumps(response_schedule_fw_update_flexdesk, indent=2)
            Report.logInfo(f'Response to schedule firmware update to flexdesk is')
            Report.logResponse(json_formatted_response)

            # Validate if scheduled firmware update completed successfully
            timer = 50
            while timer > 0:
                timer -= 1

                # Get the firmware version and status after triggering the scheduled update
                response_device_info = self.get_coily_desk_information(desk_name, desk_id)
                collabos_update_status = response_device_info['state']['reported']['updateStatus']
                collabos_software_version = response_device_info['sw']

                # Update Status is 1 when update is available, 2 when update is in pending state,
                # 4 when update is in downloading state, 6 when update is in progress,
                # 8 when update is failed and 0 when up-to-date.
                # More details related to Update Status is available in
                # https://docs.google.com/document/d/1CsTIuCDEu1eiddFXLFBPI1VH2FHqs547CZAwRpeeSLw/edit#heading=h.x8kk2wprgnen

                if collabos_update_status == 1 or collabos_update_status == 8:
                    Report.logInfo("Firmware update is available.")
                    time.sleep(60)
                    update_status = 1
                elif collabos_update_status == 4:
                    Report.logInfo("Firmware update is downloading.")
                elif collabos_update_status == 6:
                    Report.logInfo("Firmware update is in progress.")
                elif collabos_update_status == 0:
                    Report.logPass("Firmware update scheduled is completed successfully.")
                    Report.logInfo(f'Firmware software version is: {collabos_software_version}')
                    update_status = 0
                    break

            return update_status

        except Exception as e:
            Report.logException(f'{e}')

    def get_coily_desk_information(self, desk_name, desk_id):
        """
        Get coily desk information
        """
        try:
            self.banner(f'Get Desk information: {desk_name}')
            self.role_raiden = 'OrgAdmin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role_raiden)
            self.org_id = raiden_helper.get_org_id(self.role_raiden, global_variables.config, self.token)

            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{desk_id}/info'
            response = raiden_helper.send_request(
                method='GET', url=info_url, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Response for GET info API for {desk_name}')
            Report.logResponse(json_formatted_response)
            Report.logInfo(f'Response for GET info API for {desk_name}- {json_formatted_response}')

            return response

        except Exception as e:
            Report.logException(f'{e}')

    def get_flexdesk_use_state(self, token, org_id, desk_id):
        """
            Method to get flex desk use state information
            :param token:token to authenticate user
            :param org_id:Organization id
            :param desk_id:Id for the desk created
        """
        try:
            get_flexdesk_use_state_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/info'
            Report.logInfo(f'Url to get flex desk use state information is: {get_flexdesk_use_state_url}')

            response_flexdesk_use_state = raiden_helper.send_request(
                method='GET', url=get_flexdesk_use_state_url,
                token=token
            )
            json_formatted_response = json.dumps(response_flexdesk_use_state, indent=2)
            Report.logInfo(f'Get flex desk use state information is:')
            Report.logResponse(json_formatted_response)

            # Validate Response
            flexdesk_use_state = response_flexdesk_use_state['state']['reported']['status']
            Report.logInfo(f'Flex desk use status is {flexdesk_use_state}')

            if flexdesk_use_state == 2:
                Report.logPass(f'Flex desk status is Available')
            elif flexdesk_use_state == 10:
                Report.logPass(f'Flex desk status is In Use')
            elif flexdesk_use_state == 0:
                Report.logPass(f'Flex desk status is Offline')
            elif flexdesk_use_state == -1:
                Report.logPass(f'Flex desk status is NA')
            else:
                Report.logFail(f'Failed to retrieve flex desk use state')

            return flexdesk_use_state

        except Exception as e:
            Report.logException(f'{e}')

    def get_flexdesk_collabos_systemimage_version(self, token, org_id, desk_id):
        """
            Method to get flex desk CollabOS and SystemImage version
            :param token:token to authenticate user
            :param org_id:Organization id
            :param desk_id:Id for the desk created
        """
        try:
            get_flexdesk_use_state_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/info'
            Report.logInfo(f'Url to get flex desk CollabOS and SystemImage version is: {get_flexdesk_use_state_url}')

            response_flexdesk_collabos_systemimage_version = raiden_helper.send_request(
                method='GET', url=get_flexdesk_use_state_url,
                token=token
            )

            json_formatted_response = json.dumps(response_flexdesk_collabos_systemimage_version, indent=2)
            Report.logInfo(f'Get flex desk desk CollabOS and SystemImage version is:')
            Report.logResponse(json_formatted_response)

            # Validate Response
            flexdesk_collabos_version = response_flexdesk_collabos_systemimage_version['devices'][0]['sw']
            flexdesk_systemimage_version = response_flexdesk_collabos_systemimage_version['devices'][0]['osv']

            Report.logInfo(f'Flex desk CollabOS version is {flexdesk_collabos_version}')
            Report.logInfo(f'Flex desk System Image version is {flexdesk_systemimage_version}')

            return True

        except Exception as e:
            Report.logException(f'{e}')


    def edit_flexdesk_host_name(self, token, org_id, desk_id, device_id, flexdesk_host_name, desk_name):
        """
            Method to edit flex desk user name
            :param token:token to authenticate user
            :param org_id:Organization id
            :param desk_id:Id for the desk created
            :param device_id: Device id of Coily
            :param flexdesk_host_name: initial host name of Coily device
        """
        try:

            updated_host_name = flexdesk_host_name + '-test'
            Report.logInfo(f'Flex desk host name will be updated to: {updated_host_name}')

            edit_flexdesk_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(f'Url to edit flex desk host name is: {edit_flexdesk_host_name_url}')

            edit_flexdesk_host_name_payload = {
                'systemSettings':{
                    'hostName': updated_host_name
                                }
            }

            response_edit_flexdesk_host_name = raiden_helper.send_request(
                method='PUT', url=edit_flexdesk_host_name_url, body=json.dumps(edit_flexdesk_host_name_payload),
                token=token
            )

            Report.logInfo('Device is rebooting after editing the host name')

            retries = 30
            for retry in range(0, retries):

                response_get_device_status = self.get_coily_desk_information(desk_name, desk_id)
                bootStatus_after_hostname_edit = response_get_device_status['devices'][0]['state']['reported'][
                    'bootStatus']

                if bootStatus_after_hostname_edit == 0:
                    break
                else:
                    time.sleep(10)

            json_formatted_response = json.dumps(response_edit_flexdesk_host_name, indent=2)
            Report.logInfo(f'Edit flex desk host name:')
            Report.logResponse(json_formatted_response)

            # Validate Response
            for i in range(20):
                get_flexdesk_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{desk_id}/info'

                response_get_flexdesk_updated_host_name = raiden_helper.send_request(
                    method='GET', url=get_flexdesk_host_name_url,
                    token=token
                )

                time.sleep(5)

                if len(response_get_flexdesk_updated_host_name['devices']) >= 1:
                    if 'systemSettings' in response_get_flexdesk_updated_host_name['devices'][0]['state']['reported']:
                        flexdesk_updated_host_name = response_get_flexdesk_updated_host_name['devices'][0]['state']['reported']['systemSettings']['hostName']
                        Report.logInfo(f'Flex desk updated host name is: {flexdesk_updated_host_name}')
                        break


            if flexdesk_updated_host_name == updated_host_name:
                Report.logPass(f'Flex desk host name is updated successfully')
            else:
                Report.logFail(f'Flex desk host name didnot update')

            # Set the hostname of Coily back to its initial name.
            if flexdesk_updated_host_name == updated_host_name:

                reset_flexdesk_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
                Report.logInfo(f'Url to reset flex desk host name is: {reset_flexdesk_host_name_url}')

                reset_flexdesk_host_name_payload = {
                    'systemSettings': {
                        'hostName': flexdesk_host_name
                    }
                }

                response_reset_flexdesk_host_name = raiden_helper.send_request(
                    method='PUT', url=reset_flexdesk_host_name_url, body=json.dumps(reset_flexdesk_host_name_payload),
                    token=token
                )

                Report.logInfo('Device is rebooting after reseting the host name')

                retries = 30
                for retry in range(0, retries):

                    response_get_device_status = self.get_coily_desk_information(desk_name, desk_id)
                    bootStatus_after_hostname_reset = response_get_device_status['devices'][0]['state']['reported'][
                        'bootStatus']

                    if bootStatus_after_hostname_reset == 0:
                        break
                    else:
                        time.sleep(10)

            # Get Flex Desk initial Host Name details
            get_flexdesk_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{desk_id}/info'

            for i in range(20):
                response_get_flexdesk_reseted_host_name = raiden_helper.send_request(
                    method='GET', url=get_flexdesk_host_name_url,
                    token=self.token
                )

                time.sleep(5)

                flexdesk_reseted_host_name = response_get_flexdesk_reseted_host_name['hostName']

                if flexdesk_host_name == flexdesk_reseted_host_name:
                    Report.logPass(f'Flex desk host name is set back to initial host name successfully')
                else:
                    Report.logFail(f'Flex desk host name didnot set back to initial name')

            return updated_host_name

        except Exception as e:
            Report.logException(f'{e}')


    def get_ip_address_of_coily_device(self, token: str, org_id: str, site: str, building:str, floor: str,
                                       area: str, desk_name: str) -> str:
        """
        Method to get IP Address of Coily device associated with Desk

        :param token:Sign in token
        :param org_id:
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :return ip_address:
        """
        try:
            desk_id = self.get_desk_id_by_desk_name_in_organization(token, org_id, site, building,
                                                                    floor, area, desk_name)
            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/room/{desk_id}/info'
            info_response = raiden_helper.send_request(method='GET', url=info_url, token=token)
            return info_response['devices'][0]['ip']
        except Exception as e:
            Report.logException(f'{e}')
            return ""

    def get_group_provision_code_for_site(self, role, site_name, area_name):
        """
        Method to get group provision code from site

        :param role:
        :param desk_name:
        :param area_name:
        :param site_name:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Get group provision code for site
            site_group_prov_code_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/prov-code'

            site_name = site_name + "/"
            payload_site_group_prov_code = {
                "group": site_name,
                "realm": "Desks",
                "generate":True
            }

            response_site_group_prov_code = raiden_helper.send_request(
                method='POST', url=site_group_prov_code_url, body=json.dumps(payload_site_group_prov_code), token=self.token
            )

            json_formatted_response_site_group_prov_code = json.dumps(response_site_group_prov_code, indent=2)
            Report.logResponse(format(json_formatted_response_site_group_prov_code))
            site_group_provision_code = response_site_group_prov_code['code']
            status_group_prov_code = self._validate_get_prov_code(response_site_group_prov_code)
            assert status_group_prov_code is True, 'Error in getting group provision code for site for'
            return site_group_provision_code

        except Exception as e:
            Report.logException(f'{e}')


    def assign_room_to_map(self, token, org_id, map_name, map_id, org_identifier, site_location_id, building_location_id, floor_location_id, room_name, room_id, published_at_time, location_path):
        """
            Method to assign room to map

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_name:Name of the map
            :param map_id:Id for map created in organization
            :param org_identifier:org_identifier from meetio
            :param site_location_id:Location Id for the site group
            :param building_location_id:Location Id for the building group
            :param floor_location_id:Location Id for the floor group
            :param room_name:Name of the room created
            :param room_id:id of the room created
            :param published_at_time:Map published time
            :param location_path:Path where map was located


        """
        try:

            assign_room_to_map_payload = {
                "content":{
                    "rooms":[
                        {
                         "paths":jrm.jasmine_room_path,
                         "id":room_id,
                         "name":room_name
                        }
                    ],
                     "segas":[],
                     "width":1024,
                     "scale":39,
                     "areas":[],
                     "desks":[],
                     "nintendos":[],
                     "floor":
                             {
                                 "paths":jrm.jasmine_room_floor_path
                             },
                     "pois":[],
                     "plan":
                     {
                         "paths":jrm.map_plan_paths

                    },
                    "height":1024
                },
                "location":{
                    "path":location_path,
                    "site":site_location_id,
                    "floor":floor_location_id,
                    "building":building_location_id
                },
                "updated_at":published_at_time,
                "org_id":org_id,
                "org_identifier":org_identifier,
                "id":map_id,
                "name":map_name
            }

            assign_room_to_map_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}'
            Report.logInfo(
                f'Url to assign room to map is: {assign_room_to_map_url}')

            response_assign_room_to_map = raiden_helper.send_request(
                method='PUT', url=assign_room_to_map_url, body=json.dumps(assign_room_to_map_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_assign_room_to_map, indent=2)
            Report.logInfo(f'Response for assign room to map is')
            Report.logResponse(json_formatted_response)

            if response_assign_room_to_map['content']['rooms'][0]['id'] == room_id:
                Report.logInfo(f' Successfully room is assigned to map')
                return True
            else:
                Report.logInfo(f'Failed to assign room to map')

        except Exception as e:
            Report.logException(f'{e}')

    def add_group_building(self, role, group_name,building_timezone):
        """
        Method to add building group

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
                "realm": "Desks",
                "attributes": {
                    "location": {
                        "timezone": building_timezone
                    }
                }
            }

            response = raiden_helper.send_request(
                method='POST', url=update_groups_url, body=json.dumps(payload), token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Add group - {group_name}')
            Report.logResponse(format(json_formatted_response))
            return response

        except Exception as e:
            Report.logException(f'{e}')


    def assign_desk_to_map(self, token, org_id, map_name, map_id, org_identifier, site_location_id, building_location_id, floor_location_id, desk_name, desk_id, published_at_time, location_path, area_location_id):
        """
            Method to assign room to map

            :param token:token to authenticate user
            :param org_id:Organization id
            :param map_name:Name of the map
            :param map_id:Id for map created in organization
            :param org_identifier:org_identifier from meetio
            :param site_location_id:Location Id for the site group
            :param building_location_id:Location Id for the building group
            :param floor_location_id:Location Id for the floor group
            :param desk_name:Name of the room created
            :param desk_id:id of the room created
            :param published_at_time:Map published time
            :param location_path:Path where map was located
            :param area_location_id:Location Id for the area group

        """
        try:

            assign_desk_to_map_payload = {
                "content":{
                    "rooms":[],
                     "segas":[],
                     "width":1024,
                     "scale":39,
                     "areas": [
                                {"id": area_location_id}
                    ],
                    "desks": [
                        {
                         "id": desk_id,
                         "type": "desks",
                         "x": 448.1341576621214,
                         "y": 564.4719434162112,
                         "name": desk_name,
                         "areaId": area_location_id
                        }],
                     "nintendos":[],
                     "floor":
                             {
                                 "paths":["M9.2 956.8h1002.5V132H668.5V59l-659.3.2v897.6z"]
                             },
                     "pois":[],
                     "plan":
                     {
                         "paths":jrm.map_plan_paths

                    },
                    "height":1024
                },
                "location":{
                    "path":location_path,
                    "site":site_location_id,
                    "floor":floor_location_id,
                    "building":building_location_id
                },
                "updated_at":published_at_time,
                "org_id":org_id,
                "org_identifier":org_identifier,
                "id":map_id,
                "name":map_name
            }

            assign_desk_to_map_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/map/{map_id}'
            Report.logInfo(
                f'Url to assign desk to map is: {assign_desk_to_map_url}')

            response_assign_desk_to_map = raiden_helper.send_request(
                method='PUT', url=assign_desk_to_map_url, body=json.dumps(assign_desk_to_map_payload),
                token=token
            )

            json_formatted_response = json.dumps(response_assign_desk_to_map, indent=2)
            Report.logInfo(f'Response for assign desk to map is')
            Report.logResponse(json_formatted_response)

            # Validate desk id retrieved is matching with booking desk id
            if response_assign_desk_to_map['content']['desks'][0]['id'] == desk_id:
                Report.logInfo(f' Successfully desk is assigned to map')
                return True
            else:
                Report.logInfo(f'Failed to assign desk to map')

        except Exception as e:
            Report.logException(f'{e}')






