import json
import logging
import os
from datetime import datetime
from apis.raiden_api import raiden_helper
from base.base_ui import UIBase
from common import raiden_config
from common.usb_switch import *
from apps.sync.sync_app_methods import SyncAppMethods
from apps.browser_methods import BrowserClass
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from testsuite_sync_app.tc_methods import SyncTCMethods
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from apis.raiden_api.raiden_api_hot_desks_helper import SyncPortalHotDesksMethods
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from common import framework_params as fp
import random

log = logging.getLogger(__name__)


class SyncPortalTCMethodsHotDesks(UIBase):
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    sync_portal_hot_desks = SyncPortalHotDesksMethods()
    lna = LNASyncAppMethods()
    sync_app = SyncAppMethods()
    sync_portal_tc_methods = SyncPortalTCMethods()
    org_id = None
    token = None
    site = '/Test-' + str(int(random.random() * 10000))
    building = site + '//SVC'
    floor = site + '/SVC//Floor 1'
    area = site + '/SVC/Floor 1//QA'
    role = 'OrgAdmin'
    now = datetime.now()
    time_to_string = now.strftime("%Y%m%d%H%M%S")
    desk_name = f'{time_to_string}Auto-Desk'
    realm_desk = 'Desks'

    def tc_Provision_Coily_to_Sync_Portal(self, role, desk_name, device_name):
        """
        Provision Coily to Sync Portal
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            Report.logInfo(f'{role} Provision Coily to Sync Portal using Local Network Access')
            browser = BrowserClass()
            browser.close_all_browsers()
            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)
            # Create empty desk.
            provision_code, self.desk_id = self.sync_portal_hot_desks.create_empty_desk_and_get_provision_code(
                role=self.role, desk_name=desk_name, area_name=self.area)
            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in provision_code:
                if char != '-':
                    prov_code_without_separator += char
            self.sync_methods.lna_ip = fp.COILY_IP
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                       user_name=self.sync_methods.lna_user,
                                                                       password=self.sync_methods.lna_pass,
                                                                       provision_code=prov_code_without_separator,
                                                                       device_name=device_name)
            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_desk_information(self, desk_name):
        """
        Get desk information
        """
        try:
            self.banner(f'Get Desk information: {desk_name}')
            self.role_raiden = 'OrgAdmin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role_raiden)
            self.org_id = raiden_helper.get_org_id(self.role_raiden, global_variables.config, self.token)

            provision_code, desk_id = self.sync_portal_hot_desks. \
                create_empty_desk_and_get_provision_code(role='OrgAdmin', desk_name=desk_name, area_name=self.area)

            info_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/room/" + \
                       desk_id + '/info'
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

    def tc_get_list_of_all_desks_in_organization(self, role):
        """
        Get the list of all desks in the organization
        """
        try:
            list_of_desks = self.sync_portal_hot_desks.get_list_of_all_desks_in_organization(role)
            _num_of_desks = list_of_desks.__len__()
            self.assertNotEqual(
                _num_of_desks, 0, f'Count of Desks in the organization is {_num_of_desks}',
            )
            if _num_of_desks > 0:
                Report.logPass(f"Count of desks - {_num_of_desks}")
            else:
                Report.logFail('Error in getting count of desks')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_desk(self, role, desk_id):
        """
        Delete desk from Sync Portal
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.delete_desk(desk_id, self.org_id, self.token)
        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_site(self, role, site_name):
        """
        Delete Site from Sync Portal Flex Desks.
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            raiden_helper.delete_site(site_name, self.org_id, self.token)
        except Exception as e:
            Report.logException(f'{e}')

    def tc_flex_desks_add_channel(self, role: str):
        """
        Add update channel
        """
        try:
            Report.logInfo(f'Adding channel to flex desks: logging in as: {role}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            flex_desks_add_channel_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/channel'
            Report.logInfo(f'Url to add flex desk channel is {flex_desks_add_channel_url}')
            channel_id, channel_name = self.sync_portal_hot_desks.add_channel_for_flex_desks(role,
                                                                                             flex_desk_add_channel_url=flex_desks_add_channel_url,
                                                                                             token=self.token)
            return channel_id, channel_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_flex_desks_view_channel(self, role: str, channel_name: str, channel_id: str):
        """
        View created Channel for flex desks
        """
        try:
            Report.logInfo(f'View channel for flex desk')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            status_get_channel_details = self.sync_portal_hot_desks.get_channel_info_for_flex_desks(
                global_variables.config, self.org_id, self.token, channel_name, channel_id)

            assert status_get_channel_details is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_update_flex_desks_channel_name(self, role: str, channel_id: str, end_user_grp_name_from: str,
                                          channel_name: str):
        """
        Update flex desk's channel name to channel name created in Step 1
        """

        try:
            Report.logInfo(f'Update flex desk-s channel name from {end_user_grp_name_from} to - {channel_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # STEP 1. Add one empty desk and get desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 2. Update channel name for newly created desk
            update_channel_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/channel'
            Report.logInfo(f'Url to update channel name of desk  is: {update_channel_name_url}')

            status_update_flex_desk_channel_name = self.sync_portal_hot_desks.update_with_new_channel_name_for_flex_desk(
                global_variables.config,
                self.org_id, role, self.desk_name, self.desk_id,
                channel_id,
                channel_name,
                update_channel_name_url,
                self.token)

            assert status_update_flex_desk_channel_name is True, 'Error in status'

        except Exception as e:
            Report.logException(f'{e}')

    def tc_create_empty_desks(self, group_name: str):
        """
                Create empty flex desk
        """

        try:
            Report.logInfo(f'Create empty desk')
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.get_org_id(self.role, global_variables.config, self.token)

            # STEP 1. Add one empty desk and get desk id
            add_empty_desk_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/rooms'
            Report.logInfo(f'Url to add empty desk  is: {add_empty_desk_url}')

            room_name = 'Test_Desk'
            update_desk_channel_name_payload = {
                'group': f'{group_name}',
                'rooms': [{"name": f'{room_name}' + str(int(random.random() * 10000))}],
                'realm': self.realm_desk
            }

            response_create_empty_desk = raiden_helper.send_request(
                method='POST', url=add_empty_desk_url, body=json.dumps(update_desk_channel_name_payload),
                token=self.token
            )
            json_formatted_response = json.dumps(response_create_empty_desk, indent=2)
            Report.logInfo(f'Response for create empty desk {json_formatted_response}')
            Report.logResponse(json_formatted_response)
            Report.logInfo(f'Response for create empty desk - {json_formatted_response}')

            for item in response_create_empty_desk:
                desk_id = item['id']
                desk_name = item['name']
            return desk_id, desk_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_modify_channel_name_for_flex_desk(self, role: str, channel_id: str, channel_name: str):
        """
        Modify flex desk's channel name to channel name created in Step 1
        """
        try:
            Report.logInfo(f'Modify flex desks channel name')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # STEP 1. Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 2. Modify channel id for newly created room to channel_id
            modify_channel_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/channel/{channel_id}'
            Report.logInfo(f'Url to update channel name of room  is: {modify_channel_name_url}')

            modify_desk_channel_name_payload = {
                'name': channel_name
            }

            response_modify_desk_channel_name = raiden_helper.send_request(
                method='PUT', url=modify_channel_name_url, body=json.dumps(modify_desk_channel_name_payload),
                token=self.token
            )
            json_formatted_response = json.dumps(response_modify_desk_channel_name, indent=2)
            Report.logInfo(f'Response for create empty desk {json_formatted_response}')
            Report.logResponse(json_formatted_response)
            Report.logInfo(f'Response for create empty desk - {json_formatted_response}')

            # STEP 3. Validate that channel name is updated for the desk successfully.
            if response_modify_desk_channel_name['name'] == channel_name:
                Report.logPass(
                    f'For desk name {self.desk_name}, channel id is updated from $prod to {channel_name} successfully')
            else:
                Report.logFail(f'Failed to Update channel name for desk {self.desk_name}')
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_flex_desk_channel(self, role, channel_id):
        try:
            Report.logInfo(
                f'{role}-Delete flex desk channel: {channel_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)
            delete_flex_desk_channel_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/channel/{channel_id}'

            response_delete_flex_desk_channel = self.sync_portal_hot_desks.delete_flex_desk_channel(channel_id,
                                                                                                    delete_flex_desk_channel_url,
                                                                                                    self.token)

            json_formatted_response = json.dumps(response_delete_flex_desk_channel, indent=2)
            Report.logResponse(format(json_formatted_response))

            if response_delete_flex_desk_channel['id'] == channel_id:
                Report.logPass(f'Flex desk channel id {channel_id} is deleted successfully')
            else:
                Report.logFail(f'Failed to delete flex desk channel with id {channel_id}')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_hot_desk_hierarchy(self, role, desk_name):
        """
        TC to add hot desk hierarchy
        """
        try:
            Report.logInfo(f'{role} Add Hot Desk Hierarchy')

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            return self.desk_name, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_view_hot_desk_hierarchy(self, role, desk_name, desk_id):
        """
        TC to view hot desk hierarchy
        """
        try:
            Report.logInfo(f'{role} View Hot Desk Hierarchy')

            # View desk.
            response_desk_info = self.tc_get_desk_details(desk_name=desk_name, desk_id=desk_id)

            json_formatted_response = json.dumps(response_desk_info, indent=2)
            Report.logResponse(json_formatted_response)

            # Validate if Desk info is retrieved
            if response_desk_info['id'] == desk_id:
                Report.logPass(f'Flex desk details {desk_name} is retrieved successfully')
            else:
                Report.logFail(f'Failed to retrieve flex desk {desk_name} details')

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_modify_hot_desk_hierarchy(self, role, desk_name, desk_id):
        """
        TC to modify hot desk hierarchy
        """
        try:
            Report.logInfo(f'{role} Modify Hot Desk Hierarchy')

            site = '/Test-' + str(int(random.random() * 10000))
            building = site + '//SVC'
            floor = site + '/SVC//Floor 1'
            area = site + '/SVC/Floor 1//QA'

            site_updated = site + "_" + str(int(random.random() * 1000))
            building_updated = building + "_" + str(int(random.random() * 1000))
            floor_updated = floor + "_" + str(int(random.random() * 1000))
            area_updated = area + "_" + str(int(random.random() * 1000))
            update_desk_name_to = desk_name + "_" + str(int(random.random() * 1000))

            # Create Site, Building, Floor and Area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=area)

            # Modify Desk Name.
            self.sync_portal_hot_desks.modify_desk_name(role, desk_name, update_desk_name_to, desk_id)

            # Modify Area name
            self.sync_portal_hot_desks.modify_group(role=self.role, group_name=area, update_group_name_to=area_updated,
                                                    site=site)
            # Modify Floor name
            self.sync_portal_hot_desks.modify_group(role=self.role, group_name=floor,
                                                    update_group_name_to=floor_updated, site=site)

            # Modify Building name
            self.sync_portal_hot_desks.modify_group(role=self.role, group_name=building,
                                                    update_group_name_to=building_updated, site=site)

            # Modify Site name
            self.sync_portal_hot_desks.modify_group(role=self.role, group_name=site, update_group_name_to=site_updated,
                                                    site=site)


        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_delete_flex_desk_hierarchy(self, desk_id, role):
        try:
            Report.logInfo(
                f'{role} -Delete flex desk hierarchy')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            group_name = '/Test-' + str(int(random.random() * 10000))
            building = group_name + '//SVC'
            floor = group_name + '/SVC//Floor 1'
            area = group_name + '/SVC/Floor 1//QA'

            # Create Building, Floor and Area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=area)

            # Step 1: Delete desk
            self.tc_delete_flex_desk(role, desk_id)

            # Step 2: Delete area name
            self.sync_portal_hot_desks.delete_flex_desk_hierarchy(role=self.role, group_name=area)

            # Step 3: Delete floor name
            self.sync_portal_hot_desks.delete_flex_desk_hierarchy(role=self.role, group_name=floor)

            # Step 4: Delete building name
            self.sync_portal_hot_desks.delete_flex_desk_hierarchy(role=self.role, group_name=building)

            # Step 5: Delete site name
            self.sync_portal_hot_desks.delete_flex_desk_hierarchy(role=self.role, group_name=group_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_flex_desk(self, role, desk_id):
        try:
            Report.logInfo(
                f'{role} -Delete flex desk')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Delete desk
            delete_flex_desk_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/room/delete'

            delete_desk_payload = {
                "roomIds": [desk_id]
            }

            response_delete_flex_desk = raiden_helper.send_request(
                method='POST', url=delete_flex_desk_url, body=json.dumps(delete_desk_payload),
                token=self.token
            )

            json_formatted_response = json.dumps(response_delete_flex_desk, indent=2)
            Report.logResponse(format(json_formatted_response))

            if response_delete_flex_desk == {}:
                Report.logPass(f'Flex desk name is deleted successfully for {desk_id}')
            else:
                Report.logFail(f'Failed to delete flex desk with id {desk_id}')
        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_desk_details(self, desk_name, desk_id):
        """
        Get desk details
        """
        try:
            self.banner(f'Get Desk details: {desk_name}')
            self.role_raiden = 'OrgAdmin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role_raiden)
            self.org_id = raiden_helper.get_org_id(self.role_raiden, global_variables.config, self.token)
            #
            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # # Add one empty desk and get desk id
            # self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

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

    def tc_firmware_update_coily(self, desk_name, role, device_name):
        """
        Method to update firmware for coily and verify firmware update is successful

        :param desk_name:Desk name
        :param role:Signed-in user role
        :param device_name:Coily
        :return :
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.banner(f'Firmware Update: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, desk_name,
                                                                                            device_name)

            response_device_info = self.tc_get_coily_desk_information(desk_name, self.desk_id)

            self.device_id = response_device_info['devices'][0]['id']
            print(f'Coily device id is {self.device_id}')

            raiden_helper.set_update_channel_via_adb(device_name)

            update_status = self.sync_portal_hot_desks.firmware_update_availability_check_coily(org_id=self.org_id,
                                                                                                desk_id=self.desk_id,
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

                timer = 50
                while timer > 0:
                    timer -= 1
                    update_status = raiden_helper.check_update_status_of_device(org_id=self.org_id,
                                                                                room_id=self.desk_id,
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

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(str(e))

    def tc_Provision_Coily_to_Sync_Portal_Stay_Connected(self, role, desk_name, device_name):
        """
        Provision Coily to Sync Portal, stay connected to sync portal after provisioning desk
        """
        try:
            Report.logInfo(f'{role} Provision Coily to Sync Portal using Local Network Access')
            browser = BrowserClass()
            browser.close_all_browsers()
            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)
            # Create empty desk.
            provision_code, self.desk_id = self.sync_portal_hot_desks. \
                create_empty_desk_and_get_provision_code(role=self.role, desk_name=desk_name, area_name=self.area)
            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in provision_code:
                if char != '-':
                    prov_code_without_separator += char
            self.sync_methods.lna_ip = fp.COILY_IP

            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                       user_name=self.sync_methods.lna_user,
                                                                       password=self.sync_methods.lna_pass,
                                                                       provision_code=prov_code_without_separator,
                                                                       device_name=device_name)

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_coily_desk_information(self, desk_name, desk_id):
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

    def tc_move_hot_desk_to_a_group(self, role, desk_name):
        """
        TC to move hot desk to a group
        """
        try:
            Report.logInfo(f'{role} Move Hot Desk to a group')

            self.site_name, self.desk_id = self.tc_add_hot_desk_hierarchy(role, desk_name)

            # Create new group - Site, building, floor and area
            site = self.site
            building = site + '//SVC'
            floor = site + '/SVC//Floor 1'
            new_area = site + '/SVC/Floor 1/QA_New'

            self.sync_portal_hot_desks.add_group(role=self.role, group_name=site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=new_area)

            self.sync_portal_hot_desks.move_desk_to_different_group(role=self.role, group_name=self.area,
                                                                    new_group_name=new_area,
                                                                    desk_id=self.desk_id)

            # Validate desk is moved to new group.
            info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{self.desk_id}/info'

            response_desk_info = raiden_helper.send_request(
                method='GET', url=info_url, token=self.token
            )

            json_formatted_response = json.dumps(response_desk_info, indent=2)
            Report.logResponse(json_formatted_response)
            desk_id = response_desk_info['id']

            # Validate if Desk info is retrieved
            if response_desk_info['id'] == self.desk_id and new_area in response_desk_info['group']:
                Report.logPass(
                    f'Desk {desk_name} is moved to new group {new_area} successfully')
            else:
                Report.logFail(f'Failed to move desk {desk_name} to new {new_area} ')

            return desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_hot_desk_check_in_url(self, role, desk_name):
        """
        TC to get hot desk check in url
        """
        try:
            Report.logInfo(f'{role} Get Hot Desk Check-in Url')

            self.desk_name, self.desk_id = self.tc_add_hot_desk_hierarchy(role, desk_name)

            desk_check_in_url, response = self.sync_portal_hot_desks.get_desk_check_in_url(role=self.role,
                                                                                           desk_id=self.desk_id)
            desk_id = response['desks'][0]['id']
            # Validate response
            if response['desks'][0]['id'] == self.desk_id:
                Report.logPass(
                    f'Check in url for desk is {desk_check_in_url}')
            else:
                Report.logFail(f'Failed to retrieve check-in url for desk')

            return desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_edit_area_attributes(self, role):
        """
        TC to edit area attributes
        """
        try:
            Report.logInfo(f'Edit the area attributes')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            site = self.site
            site = site.replace("/", '%2F')
            area = site + '%2FSVC%2FFloor%201%2FQA%2F'
            location_path = f'{area}'

            # STEP 1. Edit the area attributes
            response_edit_area_attributes = self.sync_portal_hot_desks.edit_area_attributes(role, location_path)

            # Validate response
            if response_edit_area_attributes:
                Report.logPass(
                    f'Response for edit area attribute is {response_edit_area_attributes}')
            else:
                Report.logFail(f'Failed to edit area attributes')
            return self.site

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_edit_desk_attributes(self, role, desk_name):
        """
        TC to edit desk attributes
        """
        try:
            Report.logInfo(f'Edit the desk attributes')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # Create empty desk.
            provision_code, self.desk_id = self.sync_portal_hot_desks.create_empty_desk_and_get_provision_code(
                role=self.role, desk_name=desk_name, area_name=self.area)
            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in provision_code:
                if char != '-':
                    prov_code_without_separator += char

            # STEP 1. Edit the desk attributes
            response_edit_desk_attributes = self.sync_portal_hot_desks.edit_desk_attributes(role, self.desk_id,
                                                                                            desk_name)

            # Validate response
            if response_edit_desk_attributes:
                Report.logPass(
                    f'Response for edit desk attribute is {response_edit_desk_attributes}')
            else:
                Report.logFail(f'Failed to edit desk attributes')
            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_disable_desk_policy_reserve_remotely(self, role: str):
        """
            Modify flex desk's policy to disable to reserve desk remotely
        """
        try:
            Report.logInfo(f'Modify flex desk policy to disable to reserve desk remotely')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # Modify desk policy to disable to reserve desk remotely
            modify_desk_policy_reserve_remotely_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to reserve desk remotely is: {modify_desk_policy_reserve_remotely_url}')

            status_desk_policy_disable_reserve_remotely = self.sync_portal_hot_desks.desk_policy_disable_reserve_remotely(
                modify_desk_policy_reserve_remotely_url,
                self.token, self.area)

            if status_desk_policy_disable_reserve_remotely:
                self.sync_portal_hot_desks.desk_policy_enable_reserve_remotely(modify_desk_policy_reserve_remotely_url,
                self.token, self.area)

            return self.site, self.building, self.floor, self.area

        except Exception as e:
            Report.logException(f'{e}')

    def tc_modify_desk_policy_disable_reserve_remotely_enable_walkin_session(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable to reserve desk remotely and enable walk-in session
        """
        try:
            Report.logInfo(f' Modify flex desks policy to disable to reserve desk remotely and enable walk-in session')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to disable to reserve desk remotely and enable walk-in session
            desk_policy_disable_reserve_remotely_enable_walkin_session_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify desk policy to disable to reserve desk remotely and enable walk-in session is: {desk_policy_disable_reserve_remotely_enable_walkin_session_url}')

            status_disable_reserve_remotely_enable_walkin_session = self.sync_portal_hot_desks.desk_policy_disable_reserve_remotely_enable_walkin_session(
                desk_policy_disable_reserve_remotely_enable_walkin_session_url,
                self.token, area_name)

            if status_disable_reserve_remotely_enable_walkin_session:
                self.sync_portal_hot_desks.desk_policy_enable_reserve_remotely(desk_policy_disable_reserve_remotely_enable_walkin_session_url,
                self.token, area_name)
            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_set_max_7_days(self, role: str, area_name: str):
        """
            Modify flex desk's policy to set max days to advance to 7 days
        """
        try:
            Report.logInfo(f'Modify flex desks policy to set max days to advance to 7 days')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to set max days to advance to 7 days
            modify_desk_policy_set_max_days_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to set max days to advance to 7 days is: {modify_desk_policy_set_max_days_url}')

            status_desk_policy_set_max_7_days = self.sync_portal_hot_desks.modify_desk_policy_set_max_7_days(
                modify_desk_policy_set_max_days_url,
                self.token, area_name)

            if status_desk_policy_set_max_7_days:
                self.sync_portal_hot_desks.desk_policy_set_max_to_default_days(
                modify_desk_policy_set_max_days_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_modify_desk_policy_disable_reserved_spot_visible_to_others(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable reserved spot visible to others
        """
        try:
            Report.logInfo(f'Modify flex desks policy to disable reserved spot visible to others')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to disable reserved spot visible to others
            modify_desk_policy_reserved_spot_visible_to_others_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to disable reserved spot visible to others is: {modify_desk_policy_reserved_spot_visible_to_others_url}')

            status_disable_reserved_spot_visible_to_others = self.sync_portal_hot_desks.modify_desk_policy_disable_reserved_spot_visible_to_others(
                modify_desk_policy_reserved_spot_visible_to_others_url,
                self.token, area_name)

            if status_disable_reserved_spot_visible_to_others:
                self.sync_portal_hot_desks.desk_policy_enable_reserved_spot_visible_to_others(
                    modify_desk_policy_reserved_spot_visible_to_others_url,
                    self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_desk_policy_reserve_remotely(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable to reserve desk remotely
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable to reserve desk remotely')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to enable to reserve desk remotely
            desk_policy_enable_reserve_remotely_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to reserve desk remotely is: {desk_policy_enable_reserve_remotely_url}')

            self.sync_portal_hot_desks.desk_policy_enable_reserve_remotely(
                desk_policy_enable_reserve_remotely_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_set_max_14_days(self, role: str, area_name: str):
        """
            Modify flex desk's policy to set max days to advance to 14 days
        """
        try:
            Report.logInfo(f'Modify flex desks policy to set max days to advance to 14 days')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to set max days to advance to 14 days
            desk_policy_set_max_14_days_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to set max days to advance to 14 days is: {desk_policy_set_max_14_days_url}')

            self.sync_portal_hot_desks.desk_policy_set_max_to_default_days(
                desk_policy_set_max_14_days_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_set_reservation_time_limit_8_hours(self, role: str, area_name: str):
        """
            Modify flex desk's policy Enable reservation time limit to 8 hours
        """
        try:
            Report.logInfo(f' Modify flex desks policy Enable reservation time limit to 8 hours')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy Enable reservation time limit to 8 hours
            desk_policy_set_reservation_time_limit_8_hours_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to set reservation time limit to 8 hours is: {desk_policy_set_reservation_time_limit_8_hours_url}')

            status_enable_reservation_time_limit_8_hours = self.sync_portal_hot_desks.desk_policy_enable_reservation_time_limit_8_hours(
                desk_policy_set_reservation_time_limit_8_hours_url,
                self.token, area_name)

            if status_enable_reservation_time_limit_8_hours:
                self.sync_portal_hot_desks.desk_policy_enable_reservation_time_limit_1_hour(desk_policy_set_reservation_time_limit_8_hours_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_set_reservation_time_limit_1_hour(self, role: str, area_name: str):
        """
            Modify flex desk's policy Enable reservation time limit to 1 hour
        """
        try:
            Report.logInfo(f' Modify flex desks policy Enable reservation time limit to 1 hour')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy Enable reservation time limit to 1 hour
            set_reservation_time_limit_1_hour_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to set reservation time limit to 8 hours is: {set_reservation_time_limit_1_hour_url}')

            status_enable_reservation_time_limit_1_hour = self.sync_portal_hot_desks.desk_policy_enable_reservation_time_limit_1_hour(
                set_reservation_time_limit_1_hour_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_reserved_spot_visible_to_others(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable reserved spot visible to others
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable reserved spot visible to others')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to enable reserved spot visible to others
            desk_policy_enable_reserved_spot_visible_to_others_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify flex desks policy to enable reserved spot visible to others is: {desk_policy_enable_reserved_spot_visible_to_others_url}')

            status_enable_reserved_spot_visible_to_others = self.sync_portal_hot_desks.desk_policy_enable_reserved_spot_visible_to_others(
                desk_policy_enable_reserved_spot_visible_to_others_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')


    def tc_desk_policy_disable_walkin_session(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable walk-in session
        """
        try:
            Report.logInfo(f' Modify flex desks policy to disable walk-in session')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to disable walk-in session
            disable_walkin_session_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify desk policy to disable walk-in session is: {disable_walkin_session_url}')

            status_disable_walkin_session = self.sync_portal_hot_desks.desk_policy_disable_walkin_session(
                disable_walkin_session_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_walkin_session(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable walk-in session and set duration to 1 hour
        """
        try:
            Report.logInfo(f' Modify flex desks policy to ebable walk-in session duration to 1 hour')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to enable walk-in session duration to 1 hour
            enable_walkin_session_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(f'Url to modify desk policy to enable walk-in session duration to 1 hour is: {enable_walkin_session_url}')

            status_enable_walkin_session = self.sync_portal_hot_desks.desk_policy_enable_walkin_session_set_duration_1_hour(
                enable_walkin_session_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_session_time_limit(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable session time limit
        """
        try:
            Report.logInfo(f'Modify flex desks policy to disable session time limit')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to disable session time limit
            disable_session_time_limit_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy disable_session_time_limit is: {disable_session_time_limit_url}')

            self.sync_portal_hot_desks.desk_policy_disable_session_time_limit(
                disable_session_time_limit_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_disable_session_time_limit(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable session time limit
        """
        try:
            Report.logInfo(f'Modify flex desks policy to disable session time limit')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to disable session time limit
            disable_session_time_limit_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy disable_session_time_limit is: {disable_session_time_limit_url}')

            self.sync_portal_hot_desks.desk_policy_disable_session_time_limit(
                disable_session_time_limit_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_show_QR_code(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable show QR code
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable show QR code')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to enable show QR code
            enable_show_qr_code_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy policy to enable show QR code is: {enable_show_qr_code_url}')

            self.sync_portal_hot_desks.desk_policy_enable_show_qr_code(
                enable_show_qr_code_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_disable_show_QR_code(self, role: str, area_name: str):
        """
            Modify flex desk's policy to disable show QR code
        """
        try:
            Report.logInfo(f'Modify flex desks policy to disable show QR code')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to disable show QR code
            disable_show_qr_code_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy policy to disable show QR code is: {disable_show_qr_code_url}')

            self.sync_portal_hot_desks.desk_policy_disable_show_qr_code(
                disable_show_qr_code_url,
                self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')


    def tc_desk_policy_enable_reserve_remotely_checkin_vacancy_release_30_minutes(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30mins
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30mins')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30mins
            enable_reservable_checkin_set_vacancy_release_30_minutes_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable to reserve desk remotely, enable check-in required and set vacancy release to 30min is: {enable_reservable_checkin_set_vacancy_release_30_minutes_url}')

            self.sync_portal_hot_desks.desk_policy_enable_reserve_remotely_checkin_vacancy_release_30_minutes(
                enable_reservable_checkin_set_vacancy_release_30_minutes_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_reservable_disable_check_in(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable Reservable and disable Check-in required
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable Reservable and disable Check-in required')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to enable Reservable and disable Check-in required
            desk_policy_enable_reservable_disable_check_in_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable Reservable and disable Check-in required is: {desk_policy_enable_reservable_disable_check_in_url}')

            self.sync_portal_hot_desks.desk_policy_enable_reservable_disable_check_in(
                desk_policy_enable_reservable_disable_check_in_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')


    def tc_enable_walkin_default_session_duration_notify_desk_released(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes
            enable_walkin_default_session_duration_notify_desk_released_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to Modify flex desks policy to enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes is: {enable_walkin_default_session_duration_notify_desk_released_url}')

            self.sync_portal_hot_desks.enable_walkin_default_session_duration_notify_desk_released(
                enable_walkin_default_session_duration_notify_desk_released_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')


    def tc_desk_policy_disable_auto_extend_session_set_hardstop_10minutes(self, role: str, area_name: str):
        """
            Modify flex desk's policy - Disable Auto-extend session and set blocking user from re-using set to 10 minutes
        """
        try:
            Report.logInfo(f'Modify flex desks policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desks policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes
            disable_auto_extend_session_set_hardstop_10minutes_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify flex desks policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes is: {disable_auto_extend_session_set_hardstop_10minutes_url}')

            self.sync_portal_hot_desks.disable_auto_extend_session_set_hardstop_10minutes(
                disable_auto_extend_session_set_hardstop_10minutes_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_desk_policy_reserve_remotely(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable Auto-extend session
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable to reserve desk remotely')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to enable to reserve desk remotely
            desk_policy_enable_reserve_remotely_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to reserve desk remotely is: {desk_policy_enable_reserve_remotely_url}')

            self.sync_portal_hot_desks.desk_policy_enable_reserve_remotely(
                desk_policy_enable_reserve_remotely_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_desk_policy_enable_auto_extend_session(self, role: str, area_name: str):
        """
            Modify flex desk's policy to enable Auto-extend session
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable Auto-extend session')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desks policy to enable Auto-extend session
            desk_policy_enable_auto_extend_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable Auto-extend session is: {desk_policy_enable_auto_extend_url}')

            self.sync_portal_hot_desks.desk_policy_enable_auto_extend_session(
                desk_policy_enable_auto_extend_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_reservable_show_qr_code_check_in_20minutes(self, role: str, area_name: str):
        """
            Modify flex desk's policy to Enable Show QR code, Enable Reservable & set Check-in required to 20 minutes
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desks policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes
            enable_reservable_show_qr_code_check_in_20minutes_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable Show QR code, Enable Reservable & set Check-in required to 20 minutes is: {enable_reservable_show_qr_code_check_in_20minutes_url}')

            self.sync_portal_hot_desks.enable_reservable_show_qr_code_check_in_20minutes(
                enable_reservable_show_qr_code_check_in_20minutes_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_reservable_disable_qr_code_and_checkin_required(self, role: str, area_name: str):
        """
            Modify flex Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required
        """
        try:
            Report.logInfo(f'Modify flex Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required
            enable_reservable_disable_qr_code_and_checkin_required_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to Disable QR code reservation, Enable Reservable & disable Check-in required is: {enable_reservable_disable_qr_code_and_checkin_required_url}')

            self.sync_portal_hot_desks.enable_reservable_disable_qr_code_and_checkin_required(
                enable_reservable_disable_qr_code_and_checkin_required_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_walkin_session_disable_auto_extend_block_reserve_reuse(self, role: str, area_name: str):
        """
            Modify flex desk's policy to Enable walk-in session, disable auto-extend session
            and set Blocking user from re-using to 30 mins.
        """
        try:
            Report.logInfo(f'Modify flex desks policy to Enable walk-in session, disable auto-extend and block user from reusing 30mins')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desks policy to Enable walk-in session, disable auto-extend and block user from reusing 30mins
            enable_walkin_session_disable_auto_extend_block_reserve_reuse_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable_walkin_session_disable_auto_extend_block_reserve_reuse is: {enable_walkin_session_disable_auto_extend_block_reserve_reuse_url}')

            self.sync_portal_hot_desks.enable_walkin_session_disable_auto_extend_block_reserve_reuse(
                enable_walkin_session_disable_auto_extend_block_reserve_reuse_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_disable_walkin_session_and_checkin_enable_autoextend(self, role: str, area_name: str):
        """
            Modify flex desk's policy to Disable walk-in session, Disable Check-in required, enable auto-extend session
        """
        try:
            Report.logInfo(f'Modify flex desks policy to Disable walk-in session, Disable Check-in required, enable auto-extend session')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify flex desk's policy to Disable walk-in session, Disable Check-in required, enable auto-extend session
            disable_walkin_session_and_checkin_enable_autoextend_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to disable_walkin_session_and_checkin_enable_autoextend is: {disable_walkin_session_and_checkin_enable_autoextend_url}')

            self.sync_portal_hot_desks.disable_walkin_session_and_checkin_enable_autoextend(
                disable_walkin_session_and_checkin_enable_autoextend_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')


    def tc_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin(self, role: str, area_name: str):
        """
            Modify flex desk's policy to Enable Reservable, set max days in advance to 7 days and session time limit set to 12 hours
            and Show QR code enabled, Check-in required enabled
        """
        try:
            Report.logInfo(f' Modify flex desks policy to Enable Reservable, set max days in advance to 7 days and session time limit set to 12 houand Show QR code enabled, Check-in required enabled')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to enable to reserve desk remotely Modify flex desk's policy to Enable Reservable, set max days in advance to 7 days and session time limit set to 12 hours
            #             and Show QR code enabled, Check-in required enabled
            enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url is: {enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url}')

            self.sync_portal_hot_desks.enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin(
                enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_enable_reservable_set_maxdays_disable_session_time_show_qrcode(self, role: str, area_name: str):
        """
            Modify flex desk's policy to Enable Reservable, set max days in advance to 14 days,
            disable session time limt, disable Show QR code
        """
        try:
            Report.logInfo(f'Modify flex desks policy to enable_reservable_set_maxdays_disable_session_time_show_qrcode')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Modify desk policy to enable_reservable_set_maxdays_disable_session_time_show_qrcode
            enable_reservable_set_maxdays_disable_session_time_show_qrcode_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/desk-settings'
            Report.logInfo(
                f'Url to modify desk policy to enable_reservable_set_maxdays_disable_session_time_show_qrcode is: {enable_reservable_set_maxdays_disable_session_time_show_qrcode_url}')

            self.sync_portal_hot_desks.enable_reservable_set_maxdays_disable_session_time_show_qrcode(
                enable_reservable_set_maxdays_disable_session_time_show_qrcode_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')

    def tc_flex_desk_session_booking(self, role, desk_name, user_id, email_id):
            """
            TC to book a session for a desk
            """
            try:
                Report.logInfo(f'Book a session for a desk')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # Step 1: Create Site, building, floor and area
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

                # Step 2: Create empty desk.
                provision_code, self.desk_id = self.sync_portal_hot_desks.create_empty_desk_and_get_provision_code(
                    role=self.role, desk_name=desk_name, area_name=self.area)
                # Remove the separator - from the provision code
                prov_code_without_separator = ''
                for char in provision_code:
                    if char != '-':
                        prov_code_without_separator += char

                # STEP 3. Book a session for the above created desk
                reservation_id = self.sync_portal_hot_desks.session_booking_for_flex_desk(role, user_id, email_id, self.desk_id,
                                                                         desk_name)

                return self.desk_id, self.site, reservation_id

            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_desk_booking_setting_enable_show_meeting_disable_hide_meeting(self, role):
            """
                TC to desk Booking Settings- Enable show meeting agenda & disable hide meeting details
            """
            try:
                Report.logInfo(f'Desk booking to enable show meeting and disable hide meeting details')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # Step 1: Create Site, building, floor and area
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
                self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

                # Desk Booking Settings- Enable show meeting agenda & disable hide meeting details
                desk_booking_setting_enable_show_meeting_disable_hide_meeting_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
                Report.logInfo(
                    f'Url for desk Booking Settings- Enable show meeting agenda & disable hide meeting details is: {desk_booking_setting_enable_show_meeting_disable_hide_meeting_url}')

                # STEP: Desk booking to enable show meeting and disable hide meeting details')
                self.sync_portal_hot_desks.desk_booking_setting_enable_show_meeting_disable_hide_meeting(desk_booking_setting_enable_show_meeting_disable_hide_meeting_url, self.token, self.area)

                return self.site, self.area

            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_desk_booking_setting_enable_show_meeting_agenda_enable_hide_meeting(self, role,area_name):
        """
            TC to Desk Booking Settings- Enable show meeting agenda & enable hide meeting details
        """
        try:
            Report.logInfo(f'Desk Booking Settings- Enable show meeting agenda & enable hide meeting details')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings- Enable show meeting agenda & enable hide meeting details
            desk_booking_setting_enable_show_meeting_enable_hide_meeting_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings- Enable show meeting agenda & enable hide meeting details is: {desk_booking_setting_enable_show_meeting_enable_hide_meeting_url}')

            # STEP: Desk booking to enable show meeting agenda and enable hide meeting details')
            self.sync_portal_hot_desks.desk_booking_setting_enable_show_meeting_enable_hide_meeting(
                desk_booking_setting_enable_show_meeting_enable_hide_meeting_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_desk_booking_setting_disable_show_meeting_agenda(self, role, area_name):
            """
                TC to Desk Booking Settings - Disable show meeting agenda
            """
            try:
                Report.logInfo(f'Desk Booking Settings - Disable show meeting agenda')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # Desk Booking Settings- Enable show meeting agenda & disable hide meeting details
                desk_booking_setting_disable_show_meeting_agenda_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
                Report.logInfo(
                    f'Url for desk Booking Settings - disable show meeting agenda: {desk_booking_setting_disable_show_meeting_agenda_url}')

                # STEP: Desk booking to disable show meeting agenda')
                self.sync_portal_hot_desks.desk_booking_setting_disable_show_meeting_agenda(desk_booking_setting_disable_show_meeting_agenda_url, self.token, area_name)

            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_desk_booking_setting_screen_brightness_100(self, role, area_name):
        """
                TC to Desk Booking Settings - Set default brightness to 100
            """
        try:
            Report.logInfo(f'Desk Booking Settings - Set default brightness to 100')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings- Set default brightness to 100
            desk_booking_setting_screen_brightness_100_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings - Set default brightness to 100: {desk_booking_setting_screen_brightness_100_url}')

            # STEP: Desk booking to set default brightness to 100')
            self.sync_portal_hot_desks.desk_booking_setting_screen_brightness_100(
                desk_booking_setting_screen_brightness_100_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_desk_booking_setting_screen_brightness_250(self, role, area_name):
        """
                TC to Desk Booking Settings - Set default brightness to 250
            """
        try:
            Report.logInfo(f'Desk Booking Settings - Set default brightness to 250')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings- Set default brightness to 250
            desk_booking_setting_screen_brightness_250_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings - Set default brightness to 250: {desk_booking_setting_screen_brightness_250_url}')

            # STEP: Desk booking to set default brightness to 250')
            self.sync_portal_hot_desks.desk_booking_setting_screen_brightness_250(
                desk_booking_setting_screen_brightness_250_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_desk_booking_setting_default_langauge_english(self, role, area_name):
        """
                TC to Desk Booking Settings - Set default language to english
        """
        try:
            Report.logInfo(f'Desk Booking Settings - Set default language to english')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings- Set default language to english
            desk_booking_setting_default_language_english_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings - Set default language to english: {desk_booking_setting_default_language_english_url}')

            # STEP: Desk booking to set default language to english')
            self.sync_portal_hot_desks.desk_booking_setting_default_language_english(
                desk_booking_setting_default_language_english_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_desk_booking_setting_default_time_format_24_hour(self, role, area_name):
        """
                TC to Desk Booking Settings - Set default time format to 24 hour clock
        """
        try:
            Report.logInfo(f'Desk Booking Settings - Set default time format to 24 hour clock')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings - Set default time format to 24 hour clock
            desk_booking_setting_default_time_format_24_hour_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings - Set default time format to 24 hour clock: {desk_booking_setting_default_time_format_24_hour_url}')

            # STEP: Desk booking to default time format to 24-hour clock')
            self.sync_portal_hot_desks.desk_booking_setting_default_time_format_24_hour(
                desk_booking_setting_default_time_format_24_hour_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_desk_booking_setting_default_time_format_12_hour(self, role, area_name):
        """
                TC to Desk Booking Settings - Set default time format to 12 hour clock
        """
        try:
            Report.logInfo(f'Desk Booking Settings - Set default time format to 12 hour clock')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Desk Booking Settings - Set default time format to 12 hour clock
            desk_booking_setting_default_time_format_12_hour_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/policy/app-settings'
            Report.logInfo(
                f'Url for desk Booking Settings - Set default time format to 12 hour clock: {desk_booking_setting_default_time_format_12_hour_url}')

            # STEP: Desk booking to default time format to 12-hour clock')
            self.sync_portal_hot_desks.desk_booking_setting_default_time_format_12_hour(
                desk_booking_setting_default_time_format_12_hour_url, self.token, area_name)

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_modify_desk_reservation(self, role, desk_id, reservation_id):
            """
                TC to modify desk reservation
            """
            try:
                Report.logInfo(f'Modify a desk reservation')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # STEP 1. Modify existing desk reservation
                self.sync_portal_hot_desks.flex_desk_modify_desk_reservation(role, desk_id,
                                                                         reservation_id)

                return True

            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_flex_desk_view_reserved_desk(self, role, desk_id, desk_name):
            """
                TC to view reserved desk
            """
            try:
                Report.logInfo(f'View reserved desk')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # STEP 1. View reserved desk
                self.sync_portal_hot_desks.flex_desk_view_reserved_desk(role, desk_id,
                                                                         desk_name)

                return True

            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_flex_desk_delete_reserved_desk(self, role, desk_id, reservation_id):
            """
                TC to delete reserved desk
            """
            try:
                Report.logInfo(f'Delete reserved desk')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                # STEP 1. Delete reserved desk
                return self.sync_portal_hot_desks.flex_desk_delete_reserved_desk(self.token, self.org_id, desk_id,
                                                                          reservation_id)
            except Exception as e:
                Report.logException(f'{e}')
                raise e

    def tc_flex_desk_add_it_setting_pin_to_a_group(self, role, desk_it_pin, group_name):
        """
        TC to add IT Setting PIN for a group
        """
        try:
            Report.logInfo(f'Add IT Setting PIN for a group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Add IT Setting PIN for a group
            pin_id = self.sync_portal_hot_desks.flex_desk_add_it_setting_pin_to_a_group(role, desk_it_pin, group_name)

            return pin_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_edit_it_setting_pin_to_a_group(self, role, pin_id, modified_it_pin, group_name):
        """
        TC to edit IT Setting PIN for a group

        :param pin_id: id of desk IT pin
        :param modified_it_pin:modified pin of desk IT pin
        """
        try:
            Report.logInfo(f'Edit IT Setting PIN for a group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Edit IT Setting PIN for a group
            self.sync_portal_hot_desks.flex_desk_edit_it_setting_pin_to_a_group(role, pin_id, modified_it_pin,
                                                                                group_name)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_view_it_setting_pin_to_a_group(self, role, group_name, pin_id):
        """
            TC to view IT Setting PIN for a group
        """
        try:
            Report.logInfo(f'View IT Setting PIN for a group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: View IT Setting PIN for a group
            response_pin_id = self.sync_portal_hot_desks.flex_desk_view_it_setting_pin_to_a_group(role, group_name,
                                                                                                  pin_id)

            return response_pin_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_delete_it_setting_pin_to_a_group(self, role, group_name, pin_id):
        """
        TC to delete IT Setting PIN for a group
        """
        try:
            Report.logInfo(f'Delete IT Setting PIN for a group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            pin_id = self.flex_desk_verify_it_setting_pin_exists(role, group_name, pin_id)

            # STEP: Delete IT Setting PIN for a group
            if pin_id != None:
                self.sync_portal_hot_desks.flex_desk_delete_it_setting_pin_to_a_group(role, pin_id, group_name)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_add_different_pin_to_existing_pin(self, role, desk_it_pin, group_name):
        """
            TC to add a different PIN to the level with an existing PIN
        """
        try:
            Report.logInfo(f'Add a different PIN to the level with an existing PIN')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Add a different PIN to the level with an existing PIN
            response_code = self.sync_portal_hot_desks.flex_desk_add_different_pin_to_existing_pin(role, desk_it_pin,
                                                                                                   group_name)

            if response_code == 'PIN_EXISTS':
                return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_add_duplicatet_pin_to_existing_pin(self, role, duplicate_pin, group_name):
        """
            TC to add a duplicate PIN to the level with an existing PIN
        """
        try:
            Report.logInfo(f'Add a duplicate PIN to the level with an existing PIN')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Add a duplicate PIN to the level with an existing PIN
            response_code = self.sync_portal_hot_desks.flex_desk_add_duplicate_pin_to_existing_pin(role, duplicate_pin,
                                                                                                   group_name)

            if response_code == 'PIN_EXISTS':
                return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def flex_desk_verify_it_setting_pin_exists(self, role, group_name, pin_id):
        """
            Verify if IT Setting PIN already set at level
        """
        try:
            Report.logInfo(f'Verify if IT Setting PIN already set at level')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Verify if IT Setting PIN already set at level
            pin_id = self.sync_portal_hot_desks.flex_desk_view_it_setting_pin_to_a_group(role, group_name, pin_id)

            return pin_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(self, role, desk_it_pin, group_name):
        """
            TC to verify adding IT Setting PIN with wrong length to a group
        """
        try:
            Report.logInfo(f'Verify adding IT Setting PIN with wrong length to a group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Verify adding IT Setting PIN with wrong length to a group
            response_add_it_setting_pin = self.sync_portal_hot_desks.flex_desk_add_it_setting_pin_with_wrong_length_to_a_group(
                role, desk_it_pin, group_name)

            if response_add_it_setting_pin == 'Bad Request':
                Report.logInfo(f'Only 4 digits pin can be added to the group')
            else:
                Report.logInfo(f'Added IT Setting PIN for group with pin {desk_it_pin}')

            return response_add_it_setting_pin

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_device_setting_usb_3_priority(self, role,device_name,high_speed_usb):
        """
        TC to enable/disable USB 3.0 Priority
        """
        try:
            Report.logInfo(f'Enable/disable USB 3.0 Priority')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # STEP 3: Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 4: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                            device_name)
            # STEP 5: Get Device information
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            # STEP 6: USB 3.0 Priority Setting
            self.sync_portal_hot_desks.flex_desk_device_setting_usb_3_priority(self.token, self.org_id,
                                                                                       self.device_id, high_speed_usb,
                                                                                       self.desk_id)

            return self.desk_id, self.site

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_device_setting_disable_internet_time_set_ntp_server(self, role, device_name, ntp_server):
        """
        TC to Disable internet time and set NTP server
        """
        try:
            Report.logInfo(f'Disable internet time and set NTP server to {ntp_server}')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # STEP 3: Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 4: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)

            # STEP 5: Get Device information
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            # STEP 6: Disable internet time and set NTP server to time.android.com
            self.sync_portal_hot_desks.flex_desk_device_setting_disable_internet_time_set_ntp_server(self.token, self.org_id, self.device_id, ntp_server, self.desk_id)

            return self.desk_id, self.site

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_device_setting_local_area_network_status(self, role,device_name,local_area_network):
        """
        TC to enable/disable local area network
        """
        try:
            Report.logInfo(f'Enable/disable local area network')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.area)

            # STEP 3: Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 4: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)

            # STEP 5: Get Device information
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            # STEP 6: Local Area Network
            self.sync_portal_hot_desks.flex_desk_device_setting_local_area_network_status(self.token, self.org_id, self.device_id, local_area_network,self.desk_id)

            return self.desk_id, self.site

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_device_setting_local_area_network_change_password(self, role,device_name,local_area_network_password):
        """
        TC to change password of local area network
        """
        try:
            Report.logInfo(f'Change password of local area network')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.area)

            # STEP 3: Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 4: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)

            # STEP 5: Get Device information
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            # STEP 6: Local Area Network
            self.sync_portal_hot_desks.flex_desk_device_setting_local_area_network_change_password(self.token, self.org_id, self.device_id, local_area_network_password)

            return self.desk_id, self.site, self.token, self.org_id, self.device_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e


    def tc_flex_desk_device_setting_local_area_network_set_to_default_password(self,device_name,default_password,desk_id,token,org_id, device_id):
        """
        TC to change to default password for local area network
        """
        try:
            Report.logInfo(f'Change to default password for local area network')

            # STEP: Update Local Area Network password to default password
            self.sync_portal_hot_desks.flex_desk_device_setting_local_area_network_change_password(token, org_id, device_id, default_password)

            return self.desk_id, self.site

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_reboot_device(self, role, device_name):
        """
        TC to reboot the device
        """
        try:
            Report.logInfo(f'Flex desk - reboot device')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=role, group_name=self.area)

            # STEP 3: Create empty desk and get desk name and desk id
            self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            # STEP 4: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)

            # STEP 5: Get Device information
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            # STEP 6: Reboot the device
            response_reboot_device = self.sync_portal_hot_desks.flex_desk_reboot_device(self.token, self.org_id, self.desk_id, self.device_id)

            # Validate Response
            if response_reboot_device:
                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)
                reboot_device_id = response_device_info['devices'][0]['id']
                if reboot_device_id == self.device_id:
                    Report.logPass(f'Device with id, {self.desk_id} rebooted successfully')
                else:
                    Report.logFail(f'Failed to reboot the device with desk id, {self.desk_id}')

            return self.desk_id, self.site, self.device_id, self.token, self.org_id, self.desk_name

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_deprovision_device(self, device_id, desk_id, token, org_id, desk_name):
        """
            TC to Deprovision the device
        """
        try:
            Report.logInfo(f'Function to deprovision the device')

            # STEP: Deprovision the provisioned device
            self.sync_portal_hot_desks.flex_desk_deprovision_device(token, org_id, device_id, desk_id, desk_name)

            # Get Device information
            response_device_info = self.tc_get_coily_desk_information(desk_name, desk_id)
            devices_len = len(response_device_info['devices'])

            # Validate Response
            if devices_len == 0:
                Report.logPass(f'Device is successfully deprovisioned')
            else:
                Report.logFail(f'Failed to deprovision the device with id {device_id}')

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

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

    def tc_add_maps_to_organization(self, role, map_name):
        """
        TC to add maps to organization
        """
        try:
            Report.logInfo(f'Add maps to an organization')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            site_name = '/Test' + str(int(random.random() * 10000))
            building_name = site_name + '//SVC'
            floor_name = site_name + '/SVC//Floor 1'

            # STEP 1: Create Site, building, floor and area
            response_site = self.sync_portal_hot_desks.add_group(role=role, group_name=site_name)
            response_building = self.sync_portal_hot_desks.add_group(role=role, group_name=building_name)
            response_floor = self.sync_portal_hot_desks.add_group(role=role, group_name=floor_name)

            site = str(site_name).replace('/', '')

            # Get location id's for site, building, floor
            site_location_id, building_location_id, floor_location_id = "", "", ""
            if site in response_site:
                site_location_id = self.org_id + "-" + response_site[site]['$id']
                building_location_id = self.org_id + "-" + response_building[site]['SVC']['$id']
                floor_location_id = self.org_id + "-" + response_floor[site]['SVC']['Floor 1']['$id']

            # Configure data to add map to organization
            map_name = map_name
            data_image = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDI0IiBoZWlnaHQ9IjEwMjQiIHZpZXdCb3g9IjAgMCAxMDI0IDEwMjQiPgogIDxkZWZzPgogICAgPHN0eWxlPgogICAgICAuY2xzLTEgewogICAgICAgIGZpbGw6ICNmMmVjZjY7CiAgICAgIH0KCiAgICAgIC5jbHMtMiB7CiAgICAgICAgZmlsbDogIzgxNGVmYTsKICAgICAgfQoKICAgICAgLmNscy0zIHsKICAgICAgICBmaWxsOiBub25lOwogICAgICAgIHN0cm9rZTogIzAwMDsKICAgICAgICBzdHJva2UtbGluZWNhcDogcm91bmQ7CiAgICAgICAgc3Ryb2tlLWxpbmVqb2luOiByb3VuZDsKICAgICAgICBzdHJva2Utd2lkdGg6IDJweDsKICAgICAgfQogICAgPC9zdHlsZT4KICA8L2RlZnM+CiAgPGcgaWQ9ImZsb29yIj4KICAgIDxwb2x5Z29uIGNsYXNzPSJjbHMtMSIgcG9pbnRzPSI5LjIgOTU2LjggMTAxMS43IDk1Ni44IDEwMTEuNyAxMzIgNjY4LjUgMTMyIDY2OC41IDU5IDkuMiA1OS4yIDkuMiA0MTMuNiA5LjIgOTU2LjgiLz4KICA8L2c+CiAgPGcgaWQ9InJvb21zIj4KICA8L2c+CiAgPGcgaWQ9InBsYW4iPgogICAgPHBvbHlsaW5lIGNsYXNzPSJjbHMtMyIgcG9pbnRzPSI2NjguNSA3MS42IDY2OC41IDU5LjEgOS4yIDU5LjIgOS4yIDk1Ni44IDEwMTEuNyA5NTYuOCAxMDExLjcgMTMyIDY2OC41IDEzMiA2NjguNSAxMTkuOCIvPgogICAgPHBvbHlsaW5lIGNsYXNzPSJjbHMtMyIgcG9pbnRzPSIyODEuNyAyMTUuMiAyODEuNyAyNDAuNyA5LjIgMjQwLjciLz4KICAgIDxwb2x5bGluZSBjbGFzcz0iY2xzLTMiIHBvaW50cz0iMjM0LjkgNTkuMiAyMzQuOSAxMzYuOSAyODEuNyAxMzYuOSAyODEuNyA1OS41Ii8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI2My40IiB5MT0iMTIwLjIiIHgyPSI5OS42IiB5Mj0iMTIwLjIiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjkzLjciIHkxPSIxMjAuMiIgeDI9IjkzLjciIHkyPSI1OS4yIi8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSIxMzQuOCIgeTE9IjE3NS43IiB4Mj0iMTM0LjgiIHkyPSI1OS4yIi8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSIxMjguNiIgeTE9IjEyMC4yIiB4Mj0iMTM0LjgiIHkyPSIxMjAuMiIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iMTM5LjciIHkxPSIxMzYuOSIgeDI9IjEzNC44IiB5Mj0iMTM2LjkiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjE4NC45IiB5MT0iNjAuMiIgeDI9IjE4NC45IiB5Mj0iMTM2LjkiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjE2OS45IiB5MT0iMTM2LjkiIHgyPSIyMDAuMSIgeTI9IjEzNi45Ii8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSIxMzQuOCIgeTE9IjIxNS4xIiB4Mj0iMTM0LjgiIHkyPSIzMTcuNSIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iMTM0LjgiIHkxPSI0MTMuNiIgeDI9IjEzNC44IiB5Mj0iMzU3Ii8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI5LjIiIHkxPSI0MTMuNiIgeDI9IjEzNC44IiB5Mj0iNDEzLjYiLz4KICAgIDxwYXRoIGNsYXNzPSJjbHMtMyIgZD0iTTMxMy4yLDM1OS45YzAsNjEuNiwxMC44LDE5NS0yNy40LDIzOC4yLTYxLjcsNzAtMTIzLjYsNjAuNS0yNzYuNiw2MC41Ii8+CiAgICA8cG9seWxpbmUgY2xhc3M9ImNscy0zIiBwb2ludHM9IjM4My41IDMxNCAzODMuNSAyODAuNSA1MDYuNCAyODAuNSA1MDYuNCAzODUuNyIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iMzgzLjUiIHkxPSIzNDkuNSIgeDI9IjUwNi40IiB5Mj0iMzQ5LjUiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjM4My41IiB5MT0iMzQzIiB4Mj0iMzgzLjUiIHkyPSIzODUuNyIvPgogICAgPHBvbHlsaW5lIGNsYXNzPSJjbHMtMyIgcG9pbnRzPSI3NzQuNyAzMTAuNSA3NzQuNyAyODAuNSA2MDEuOSAyODAuNSA2MDEuOSA1OTkuMyA3NzQuNyA1OTkuMyA3NzQuNyA0OTQuNSIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iNzc0LjciIHkxPSI0NjMuMSIgeDI9Ijc3NC43IiB5Mj0iMzQyIi8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI2MDEuOSIgeTE9IjQzMi41IiB4Mj0iNzc0LjciIHkyPSI0MzIuNSIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iODQ5LjMiIHkxPSIxMzMuOSIgeDI9Ijg0OS4zIiB5Mj0iMjI1LjYiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9Ijg0OS4zIiB5MT0iMjYxLjUiIHgyPSIxMDEwLjIiIHkyPSIyNjEuNSIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iODQ5LjMiIHkxPSIyNTciIHgyPSI4NDkuMyIgeTI9IjMyMS4zIi8+CiAgICA8cG9seWxpbmUgY2xhc3M9ImNscy0zIiBwb2ludHM9IjEwMTAuMiAzNTcuMSA4NDkuMyAzNTcuMSA4NDkuMyAzNTIuNyIvPgogICAgPHBvbHlsaW5lIGNsYXNzPSJjbHMtMyIgcG9pbnRzPSI4NDkuMyA2MDguMSA4NDkuMyA1NDguMyAxMDEwIDU0OC4zIi8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI4NDkuMyIgeTE9IjY0NC40IiB4Mj0iMTAxMS43IiB5Mj0iNjQ0LjQiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9Ijg0OS4zIiB5MT0iNjM5LjUiIHgyPSI4NDkuMiIgeTI9IjcwNC44Ii8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI4NDkuMiIgeTE9IjczNi4yIiB4Mj0iODQ5LjMiIHkyPSI4OTYuMiIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iODQ5LjMiIHkxPSI3NDAuMyIgeDI9IjEwMDkuOSIgeTI9Ijc0MC4zIi8+CiAgICA8bGluZSBjbGFzcz0iY2xzLTMiIHgxPSI4NDkuMyIgeTE9IjkyNy42IiB4Mj0iODQ5LjMiIHkyPSI5NTYuOCIvPgogICAgPGxpbmUgY2xhc3M9ImNscy0zIiB4MT0iMjI5LjEiIHkxPSIxMzYuOSIgeDI9IjIzNC45IiB5Mj0iMTM2LjkiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjIzNC45IiB5MT0iMTM2LjkiIHgyPSIyNzkuNSIgeTI9IjU5LjIiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNjM5LjEiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNjQ5IiB5PSIxMzIiIHdpZHRoPSIxMCIgaGVpZ2h0PSI1OS45Ii8+CiAgICA8cmVjdCBjbGFzcz0iY2xzLTMiIHg9IjY1OSIgeT0iMTMyIiB3aWR0aD0iMTAiIGhlaWdodD0iNTkuOSIvPgogICAgPHJlY3QgY2xhc3M9ImNscy0zIiB4PSI2NjkiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNjc4LjkiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNjg4LjkiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNjk4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzA4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzE4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzI4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzM4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzQ4LjgiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzU4LjciIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzY4LjciIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzc4LjciIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzg4LjYiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iNzk4LjYiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iODA4LjUiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iODE4LjUiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iODI4LjUiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxyZWN0IGNsYXNzPSJjbHMtMyIgeD0iODM4LjkiIHk9IjEzMiIgd2lkdGg9IjEwIiBoZWlnaHQ9IjU5LjkiLz4KICAgIDxsaW5lIGNsYXNzPSJjbHMtMyIgeDE9IjYzOS4xIiB5MT0iMTYxLjkiIHgyPSI4NDguNCIgeTI9IjE2MS45Ii8+CiAgICA8cG9seWxpbmUgY2xhc3M9ImNscy0zIiBwb2ludHM9Ijg0MS4yIDE1NC44IDg0OC45IDE2MiA4NDEuMiAxNjkuMSIvPgogIDwvZz4KPC9zdmc+Cg=='
            map_width = 1024
            map_height = 1024
            map_scale = 38

            # STEP 2: Add map to organization
            map_id, floor_path, self.token, self.org_id, org_identifier = self.sync_portal_hot_desks.add_map_to_organization(self.token, self.org_id, map_name,
                                                                                    data_image, map_width, map_height, map_scale)


            return map_id, floor_path, self.token, self.org_id, site_name, site_location_id, building_location_id, floor_location_id, building_name, floor_name, org_identifier

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_maps_in_organization(self, token, org_id, map_id):
        """
        TC to get maps in organization
        """
        try:
            Report.logInfo(f'Get maps in organization')

            # STEP: Get maps details of organization
            self.sync_portal_hot_desks.get_organization_map_details(token, org_id, map_id)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_maps_under_unassigned_section(self, token, org_id):
        """
            TC to Get map(s) under unassigned section
        """
        try:
            Report.logInfo(f'Get maps under unassigned section')

            # STEP : Get maps under unassigned section
            response_message = self.sync_portal_hot_desks.get_maps_under_unassigned_section(token, org_id)
            Report.logInfo(f'{response_message}')

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_link_map_to_site_building_floor(self, token, org_id, map_id, site, site_location_id, building,
                                           building_location_id, floor, floor_location_id):
        """
            TC to Link the map to Site, building and Floor
        """
        try:
            Report.logInfo(f'Link the map to Site, building and Floor')

            # STEP 1: Capture the location path'
            location_path = f'{floor}'

            # STEP 2: Link the map to Site, building and Floor'
            response_message = self.sync_portal_hot_desks.link_map_to_site_building_floor(token, org_id, map_id,
                                                                                          site_location_id,
                                                                                          building_location_id,
                                                                                          floor_location_id,
                                                                                          location_path)
            Report.logInfo(f'{response_message}')

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_maps_associated_with_building(self, token, org_id, map_id, building_location_id):
        """
            TC to get maps associated with the building
        """
        try:
            Report.logInfo(f'Get maps associated with the building')

            # STEP : Get maps associated with the building'
            self.sync_portal_hot_desks.get_maps_associated_with_building(token, org_id, map_id, building_location_id)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_rename_map(self, token, org_id, map_id, map_name):
        """
            TC to rename map
        """
        try:
            Report.logInfo(f'Rename Map')

            # STEP : Rename Map'
            self.sync_portal_hot_desks.rename_map(token, org_id, map_id, map_name)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_delete_map(self, token, org_id, map_id):
        """
            Delete map created.
        """
        try:
            Report.logInfo(f'Delete Map')
            self.sync_portal_hot_desks.delete_map(token, org_id, map_id)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_reassign_map_to_another_floor(self, token, org_id, map_id, site, site_location_id, building_location_id,
                                         floor_location_id):
        """
            TC to re-assign map to another floor
        """
        try:
            Report.logInfo(f'Re-assign map to another floor')

            site = site.replace("/", '%2F')
            new_floor = site + '%2FSVC%2FFloor%202%2F'
            new_location_path = f'{new_floor}'

            # STEP: Re-assign map to another floor'
            self.sync_portal_hot_desks.reassign_map_to_another_floor(token, org_id, map_id,
                                                                     site_location_id,
                                                                     building_location_id,
                                                                     floor_location_id,
                                                                     new_location_path)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_change_map_status_hidden_to_visible(self, token, org_id, map_id):
        """
            TC to change the map status from hidden to visible
        """
        try:
            Report.logInfo(f'Change the map status from hidden to visible')

            # STEP : Change the map status from hidden to visible'
            published_at_time =  self.sync_portal_hot_desks.change_map_status_hidden_to_visible(token, org_id, map_id)

            return published_at_time

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_desk_activity_details(self, role, device_name):
        """
            TC to get desk activity details
        """
        try:
            Report.logInfo(f'Get desk activity details')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)
            # STEP 3: Get desk activity details
            self.sync_portal_hot_desks.get_desk_activity_details(self.token, self.org_id, self.desk_id)

            return self.desk_id, self.site
        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_peripheral_use_state(self, role, device_name):
        """
            TC to get the info associated with peripherals, their healthStatus,
            UpdateStatus and status (Use State)
        """
        try:
            Report.logInfo(f'Get the peripheral use state information')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, self.desk_name,
                                                                             device_name)
            # STEP 3: Get peripheral use state information
            self.sync_portal_hot_desks.get_peripheral_use_state(self.token, self.org_id, self.desk_id)
            return self.desk_id, self.site
        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_create_desk_provision_coily_get_desk_details(self, role, device_name):
        """
            Method to Create desk, provision coily and get desk details
        """
        try:
            Report.logInfo(f'Create desk, provision coily and get desk details')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Create Desk and Provision the Coily
            Report.logInfo(f'Create Desk and Provision the Coily')
            self.site, self.desk_id = self.provision_coily_to_sync_portal_existing_org_id(self.role, self.desk_name,
                                                                             device_name, self.token, self.org_id)
            # STEP 3: Get Device information
            response_device_info = self.get_coily_desk_information(self.desk_name, self.desk_id, token=self.token,
                                                                   org_id=self.org_id, role=self.role)

            for item in range(len(response_device_info['devices'])):
                device_type = response_device_info['devices'][item]['type']
                if device_type == 'Coily':
                    self.device_id = response_device_info['devices'][item]['id']
                    self.empty_desk_id = response_device_info['devices'][item]['room']['id']
                    print(f'Coily device id is {self.device_id} and desk id is {self.empty_desk_id}')
                    break

            return self.token, self.org_id, self.site, self.area, self.device_id, self.desk_id, self.empty_desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def get_coily_desk_information(self, desk_name, desk_id, token, org_id, role):
        """
            Get coily desk information
        """
        try:
            self.banner(f'Get Desk information: {desk_name}')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = org_id

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

    def tc_flex_desk_change_group_settings_of_area(self, token, org_id, role, desk_id, device_name, area, ntp_server, lna_password, default_password, empty_desk_id):
        """
            TC to change group settings of an area
        """
        try:
            Report.logInfo(f'Change group settings of an area')
            area_name = str(area).replace('//', '/') + '//'

            # STEP 1: Change group settings of an area
            status = self.sync_portal_hot_desks.flex_desk_change_group_settings_of_area(token, org_id, desk_id,
                                                                               area_name, ntp_server, lna_password,
                                                                               default_password, empty_desk_id)

            if status == True:
                browser = BrowserClass()
                browser.close_all_browsers()

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e


    def provision_coily_to_sync_portal_existing_org_id(self, role, desk_name, device_name, token, org_id):
        """
        Provision Coily to Sync Portal
        """
        try:

            Report.logInfo(f'{role} Provision Coily to Sync Portal using Local Network Access')
            browser = BrowserClass()
            browser.close_all_browsers()
            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)
            # Create empty desk.
            provision_code, self.desk_id = self.sync_portal_hot_desks.create_empty_desk_and_get_provision_code(
                role=role, desk_name=desk_name, area_name=self.area)
            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in provision_code:
                if char != '-':
                    prov_code_without_separator += char
            self.sync_methods.lna_ip = fp.COILY_IP
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                       user_name=self.sync_methods.lna_user,
                                                                       password=self.sync_methods.lna_pass,
                                                                       provision_code=prov_code_without_separator,
                                                                       device_name=device_name)
            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_set_local_area_network_password(self, token, org_id, default_password, area):
        """
        TC to set password for local area network
        """
        try:
            Report.logInfo(f'Set password for local area network')

            # STEP: Update Local Area Network password
            login_status = self.sync_portal_hot_desks.set_local_area_network_password(token, org_id, default_password, area)

            if login_status:
                browser = BrowserClass()
                browser.close_all_browsers()

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_coily_insight_information(self, role, desk_name, user_id, desk_id, site):
        """
            Get coily insight information
        """
        try:
            Report.logInfo(f'Get coily insight information for: {desk_name}')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP: Get coily insight information
            self.sync_portal_hot_desks.get_coily_insight_information(self.token, self.org_id, user_id, desk_id, site)

            return True

        except Exception as e:
            Report.logException(f'{e}')

    def tc_schedule_firmware_update_coily(self, desk_name, role, device_name):
        """
        Method to schedule firmware update for coily

        :param desk_name:Desk name
        :param role:Signed-in user role
        :param device_name:Coily
        :return :
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.banner(f'Schedule Firmware Update for: {device_name}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, desk_name,
                                                                                            device_name)
            # Get Device Info
            timer = 7
            while timer > 0:
                timer -= 1

                response_device_info = self.tc_get_coily_desk_information(self.desk_name, self.desk_id)

                if response_device_info['devices'] == []:
                    time.sleep(5)
                else:
                    self.device_id = response_device_info['devices'][0]['id']
                    print(f'Coily device id is {self.device_id}')
                    break

            raiden_helper.set_update_channel_via_adb(device_name)

            self.sync_portal_hot_desks.schedule_firmware_update_flexdesk(token=self.token, org_id=self.org_id,
                                                                         device_id=self.device_id,
                                                                         desk_name=desk_name,
                                                                         desk_id=self.desk_id)

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(str(e))


    def tc_get_flexdesk_use_state(self, desk_name, role, device_name, usestate):
        """
            TC to get the use state of flex desk
        """
        try:
            Report.logInfo(f'Get flex desk use state')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            if usestate == 'NA':
                # STEP 2: Create Site, building, floor and area
                self.sync_portal_hot_desks.add_group(role=role, group_name=self.site)
                self.sync_portal_hot_desks.add_group(role=role, group_name=self.building)
                self.sync_portal_hot_desks.add_group(role=role, group_name=self.floor)
                self.sync_portal_hot_desks.add_group(role=role, group_name=self.area)

                # STEP 3:Create empty desk and get desk name and desk id
                self.desk_id, self.desk_name = self.tc_create_empty_desks(group_name=self.area)

            elif usestate == 'Available' or usestate == 'In Use':
                # STEP 4: Provision the desk
                self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, desk_name,
                                                                             device_name)

            # STEP 5: Get flex desk use state information
            self.flexdesk_use_state = self.sync_portal_hot_desks.get_flexdesk_use_state(self.token, self.org_id, self.desk_id)

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_flexdesk_collabos_systemimage_version(self, desk_name, role, device_name):
        """
            TC to get flex desk collabos and system image version
        """
        try:
            Report.logInfo(f'Get flex desk collabos and system image version')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, desk_name,
                                                                         device_name)

            # STEP 3: Get flex desk collabos and system image version
            self.sync_portal_hot_desks.get_flexdesk_collabos_systemimage_version(self.token, self.org_id, self.desk_id)

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_edit_flexdesk_host_name(self, desk_name, role, device_name):
        """
            TC to edit flex desk host name
        """
        try:
            Report.logInfo(f'Edit flex desk host name')

            # STEP 1: Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 2: Provision the desk
            self.site, self.desk_id = self.tc_Provision_Coily_to_Sync_Portal(self.role, desk_name,
                                                                         device_name)
            desk_id = self.desk_id

            # STEP 3: Get flex desk Initial host name
            get_flexdesk_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{desk_id}/info'

            for i in range(20):
                response_get_flexdesk_host_name = raiden_helper.send_request(
                    method='GET', url=get_flexdesk_host_name_url,
                    token=self.token
                )

                time.sleep(5)

                if len(response_get_flexdesk_host_name['devices']) >= 1:
                    self.device_id = response_get_flexdesk_host_name['devices'][0]['id']
                    if 'systemSettings' in response_get_flexdesk_host_name['devices'][0]['state']['reported']:
                        self.flexdesk_host_name = \
                        response_get_flexdesk_host_name['devices'][0]['state']['reported']['systemSettings']['hostName']
                        Report.logInfo(f'Flex desk initial host name is: {self.flexdesk_host_name}')
                        break

            # STEP 4: Edit flex desk host name
            self.sync_portal_hot_desks.edit_flexdesk_host_name(self.token, self.org_id, desk_id, self.device_id, self.flexdesk_host_name, desk_name)

            return self.site, self.desk_id, self.device_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_get_site_group_provision_code_provision_coily_to_sync_portal(self, role, device_name):
        """
            Get site's group provision code and provision Coily to Sync Portal
        """
        try:
            # Override the raiden parameters of device based on the raiden environment
            raiden_helper.raiden_parameters_override(device=device_name, env=global_variables.SYNC_ENV)

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            Report.logInfo(f'{role} Get group provision code for site and provision Coily to Sync Portal')
            browser = BrowserClass()
            browser.close_all_browsers()

            # Create Site, building, floor and area
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.site)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.building)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.floor)
            self.sync_portal_hot_desks.add_group(role=self.role, group_name=self.area)

            # Get group provision code from site
            site_group_provision_code = self.sync_portal_hot_desks.get_group_provision_code_for_site(role=self.role, site_name=self.site, area_name=self.area)
            # Remove the separator - from the provision code
            prov_code_without_separator = ''
            for char in site_group_provision_code:
                if char != '-':
                    prov_code_without_separator += char
            self.sync_methods.lna_ip = fp.COILY_IP
            self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                       user_name=self.sync_methods.lna_user,
                                                                       password=self.sync_methods.lna_pass,
                                                                       provision_code=prov_code_without_separator,
                                                                       device_name=device_name)

            # Get desk name created
            retries = 20
            for retry in range(0, retries):
                desk_name = self.get_recently_created_deskname(role, self.site)
                if desk_name != None:
                    break
                else:
                    time.sleep(10)

            # Get desk_id from the above desk name
            get_desk_info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room?name={desk_name}'
            response_get_desk_info = raiden_helper.send_request(
                method='GET', url=get_desk_info_url,
                token=self.token
            )

            Report.logResponse(f'{response_get_desk_info}')
            self.desk_id = response_get_desk_info[0]['id']

            return self.site, self.desk_id

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def get_recently_created_deskname(self, role, site):
        """
        Get recently created desk name using role and site name
        """
        try:
            list_of_desks = self.sync_portal_hot_desks.get_list_of_all_desks_in_organization(role)
            _num_of_desks = list_of_desks.__len__()
            for i in range(_num_of_desks):
                site_name = list_of_desks[i]['_highlightResult']['groupLabel']['value']
                desk_name = None
                if site in site_name:
                    desk_name = list_of_desks[i]['_highlightResult']['name']['value']
                    Report.logInfo(f'Desk name is {desk_name}')
                    break

            return desk_name

        except Exception as e:
            Report.logException(f'{e}')

    def tc_assign_room_to_map(self, token, org_id, map_name, map_id, org_identifier, site, site_location_id,
                              building_location_id,
                              floor_location_id, room_name, room_id, published_at_time, location_path):
        """
            TC to assign room to map
        """
        try:
            Report.logInfo(f'Assign room to map')

            # STEP: Assign room to map
            self.sync_portal_hot_desks.assign_room_to_map(token, org_id, map_name, map_id, org_identifier,
                                                          site_location_id,
                                                          building_location_id,
                                                          floor_location_id,
                                                          room_name, room_id, published_at_time, location_path)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_assign_desk_to_map(self, token, org_id, map_name, map_id, org_identifier, site_location_id,
                              building_location_id,
                              floor_location_id, desk_name, desk_id, published_at_time, location_path, area_location_id):
        """
            TC to assign desk to map
        """
        try:
            Report.logInfo(f'Assign desk to map')

            # STEP: Assign desk to map
            self.sync_portal_hot_desks.assign_desk_to_map(token, org_id, map_name, map_id, org_identifier,
                                                          site_location_id,
                                                          building_location_id,
                                                          floor_location_id,
                                                          desk_name, desk_id, published_at_time, location_path, area_location_id)

            return True

        except Exception as e:
            Report.logException(f'{e}')
            raise e
































































