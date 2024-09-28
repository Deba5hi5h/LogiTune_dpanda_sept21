import json
import logging
import os
import random

from apis.raiden_api import raiden_helper, raiden_validation_methods

import requests
from datetime import timedelta, date, datetime
from tzlocal import get_localzone
import pytz
from apis.raiden_api.raiden_api_hot_desks_helper import SyncPortalHotDesksMethods
from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from base.base_ui import UIBase
from common import raiden_config, jasmine_config, tap_scheduler_config as tps, framework_params as fp, jasmine_room_floor_map_config as jrm
from common.usb_switch import *
from apps.sync.sync_app_methods import SyncAppMethods

from extentreport.report import Report
from testsuite_sync_app.tc_methods import SyncTCMethods

log = logging.getLogger(__name__)


class SyncPortalJasmineRoomBookingTCMethods(UIBase):
    sync_app = SyncAppMethods()
    sync_portal_hot_desks = SyncPortalHotDesksMethods()
    sync_methods = SyncTCMethods()
    lna = LNASyncAppMethods()

    org_id = None
    token = None

    def tc_appliance_provisioning_nintendo_get_certificate_privatekey(self, role, room_name, on_name_conflict='Fail', max_occupancy=6):
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

            Report.logInfo(f'Response received after initiating provisioning: {response}')

            Report.logInfo('Initiate Room Provisioning')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))

            # Step2: Complete Provisioning for an appliance
            provision_id = response["url"].split('/')[6]
            log.debug(f'Provisioning Id that is extracted from the response of initiate provisioning is {provision_id}')
            device_type = "Nintendo"
            device_name = "Tap Scheduler"
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
                    "make": tps.TAP_SCHEDULER_MAKE,
                    "model": tps.TAP_SCHEDULER_MODEL,
                    "proc": tps.TAP_SCHEDULER_PROC,
                    "ram": tps.TAP_SCHEDULER_RAM,
                    "os": tps.TAP_SCHEDULER_OS,
                    "osv": tps.TAP_SCHEDULER_OSV,
                    "sw": tps.TAP_SCHEDULER_SW,
                    "ip": fp.NINTENDO_IP
                }
            }
            Report.logInfo(
                f" Complete Provisioning Request Payload {complete_prov_payload}")
            response = raiden_helper.send_request(
                method="POST", url=complete_prov_url, body=json.dumps(complete_prov_payload)
            )
            Report.logInfo(
                f" Complete Provisioning Response is:  {response}")

            resp = response['appInfo']['com.logitech.vc.jasmine']

            # Get Certificate
            start_certificate = resp.find('-----BEGIN CERTIFICATE-----')
            end_certificate = resp.find('-----END CERTIFICATE-----"')
            certificate = resp[start_certificate:end_certificate] + '-----END CERTIFICATE-----'
            certificate = certificate.replace('\\n', '\n')
            Report.logInfo(
                f" Certificate Response is:  {certificate}")

            # Get Private Key
            start_privatekey = resp.find('-----BEGIN PRIVATE KEY-----')
            end_privatekey = resp.find('-----END PRIVATE KEY-----"')
            private_key = resp[start_privatekey:end_privatekey] + '-----END PRIVATE KEY-----'
            private_key = private_key.replace('\\n', '\n')
            Report.logInfo(
                f" Private key after completing provisioning is:  {private_key}")

            Report.logInfo(
                f" Complete Provisioning Room Response:  {response['room']}")
            Report.logInfo('Complete Room Provisioning')
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            provision_status, room_id = raiden_validation_methods. \
                validate_complete_provisioning_appliance(role, response, appliance_init_prov_payload["room"],
                                                         appliance_init_prov_payload["maxOccupancy"],
                                                         on_name_conflict='Fail')
            # Directory name
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            DIR_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_jasmine_api","meeting_rooms")

            file_names = ["jasmine_certificate.pem",
                          "jasmine_privatekey.pem"]

            for name in file_names:
                with open(name, "w") as file:
                    if name == "jasmine_certificate.pem":
                       file.write(certificate)
                    elif name == "jasmine_privatekey.pem":
                       file.write(private_key)
                    file.close()

            jasmine_cert_path = os.path.join(DIR_PATH, "jasmine_certificate.pem")
            jasmine_privatekey_path = os.path.join(DIR_PATH, "jasmine_privatekey.pem")

            Report.logInfo(
                f" Certificate path is {jasmine_cert_path} private key path is:  {jasmine_privatekey_path}")

            assert provision_status is True, 'Error in status'
            return room_id, jasmine_cert_path, jasmine_privatekey_path

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_jasmine_room_agenda(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str):
        """Method to get room agenda.

            Test:
                 1. Query the API: To get room agenda
                 GET ~/org/{org-id}/room/{room_id}/agenda

        """
        try:
            self.banner(f'Get agenda for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get jasmine room agenda
            url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/agenda"

            response = requests.get(url, cert=(jasmine_cert_path, jasmine_privatekey_path))
            Report.logInfo(
                f" Get agenda api status code:  {response.status_code}")
            jasmine_agenda_json_response = response.json()
            Report.logInfo(
                f" Get agenda api json response:  {response.json()}")

            jasmine_agenda_details = jasmine_agenda_json_response['bookings']
            number_of_bookings = len(jasmine_agenda_details)

            if number_of_bookings > 0:
                for i in range(len(jasmine_agenda_details)):
                    booking_start_time = jasmine_agenda_details[i]["startTime"]
                    booking_start_time_str = (
                            booking_start_time[:10] + " " + booking_start_time[11:19]
                    )
                    booking_start_time_utc = datetime.strptime(
                        booking_start_time_str, "%Y-%m-%d %H:%M:%S"
                    )
                    local_timezone = get_localzone()
                    utc_zone = pytz.utc
                    booking_local_time = str(
                        booking_start_time_utc.replace(tzinfo=utc_zone).astimezone(
                            local_timezone
                        )
                    )
                    booking_date_local = booking_local_time[:10]
                    today = str(date.today())

                    # Validate if agenda created for current day
                    if today == booking_date_local:
                        Report.logPass(
                            f"Meeting for the current date is {jasmine_agenda_details}"
                        )
                        break
                    else:
                        Report.logFail(f'There is no meeting scheduled for the current date')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_jasmine_perform_adhoc_room_booking(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str):
        """ Method to perform adhoc room booking

            Test:
                 1. Query the API: To perform adhoc room booking
                 POST ~/org/{org-id}/room/{room_id}/agenda/booking

        """
        try:
            self.banner(f'Do adhoc room booking for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to perform adhoc room booking
            url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/agenda/booking"
            Report.logInfo(
                f" Adhoc room booking url is:  {url}")

            end_date_time = datetime.now() + timedelta(minutes=45)
            log.info(f'End time is {end_date_time}')
            booking_end_time = end_date_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            log.info(f'Booking end time is {booking_end_time}')

            adhoc_room_booking_payload = {
                    'endTime': booking_end_time
            }
            Report.logInfo(
                f" Adhoc room booking Payload is: {adhoc_room_booking_payload}")

            response = requests.post(url, cert=(jasmine_cert_path, jasmine_privatekey_path), json={'endTime': booking_end_time})
            json_adhoc_response = response.json()
            Report.logInfo(
                f" Adhoc room booking api status code:  {response.status_code}")
            Report.logInfo(
                f" Adhoc room booking api json response:  {json_adhoc_response}")

            booking_id = ""
            meeting_not_created = 0
            number_of_bookings = len(json_adhoc_response['bookings'])

            # Adhoc agenda details
            jasmine_adhoc_details = json_adhoc_response['bookings']
            if number_of_bookings > 0:
                for item in range(len(jasmine_adhoc_details)):
                    meeting_end_time = jasmine_adhoc_details[item]['endTime']
                    Report.logInfo(
                        f" Adhoc meeting end time is:  {meeting_end_time}")
                    meeting_end_time_16 = meeting_end_time[:16]
                    booking_end_time_16 = booking_end_time[:16]

                    # Validate if end date time with book end time
                    if meeting_end_time_16 == booking_end_time_16:
                        booking_id = json_adhoc_response['bookings'][item]['id']
                        if booking_id == None:
                            for i in range(5):
                                booking_id = json_adhoc_response['bookings'][item]['id']
                                time.sleep(5)
                        Report.logPass(f'Adhoc meeting request created successfully')
                        break
                    else:
                        meeting_not_created += 1
                        if meeting_not_created == number_of_bookings:
                            Report.logFail(f'There is no adhoc meeting request created')
                            Report.logInfo(
                            f"meeting end time: {meeting_end_time_16} and booking end time: {booking_end_time_16}")

                return booking_id

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_jasmine_certificate(self, jasmine_cert_path: str, jasmine_privatekey_path: str):
        """
            Method to delete jasmine certificate

        :param role:
        :param jasmine_cert_path:certificate file
        :param jasmine_privatekey_path:private key
        """
        try:
            # Delete jasmine certificate and private key

            os.remove(jasmine_cert_path)
            os.remove(jasmine_privatekey_path)

            # Validate if certificate exists in path
            if "jasmine_certificate.pem" in jasmine_cert_path or "jasmine_privatekey.pem" in jasmine_privatekey_path:
                Report.logPass(f'Deleted jasmine certificate and private key')
            else:
                Report.logFail(f'Failed to delete jasmine certificate and private key')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_jasmine_cancel_adhoc_room_booking(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str, bookingId: str):
        """ Method to cancel adhoc room booking

            Test:
                 1. Query the API: To cancel adhoc room booking
                 DELETE /bapi/org/{orgId}/room/{roomId}/agenda/booking/{bookingId}

        """
        try:
            self.banner(f'To cancel adhoc room booking for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to cancel adhoc room booking
            cancel_adhoc_booking_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/agenda/booking/{bookingId}"
            Report.logInfo(
                f" Cancel Adhoc room booking Url is: {cancel_adhoc_booking_url} for booking id {bookingId}")

            cancel_adhoc_booking_response = requests.delete(cancel_adhoc_booking_url, cert=(jasmine_cert_path, jasmine_privatekey_path), params={'force':True})

            json_cancel_adhoc_booking_response = cancel_adhoc_booking_response.json()
            Report.logInfo(
                f" Cancel Adhoc room booking api status code:  {cancel_adhoc_booking_response}")
            Report.logInfo(
                f" Cancel Adhoc room booking api json response is:  {json_cancel_adhoc_booking_response}")

            # Validate adhoc booking deleted
            current_booking_count = 0
            booking_count = len(json_cancel_adhoc_booking_response['bookings'])
            Report.logInfo(
                f" Count of bookings after delete is: {booking_count}")

            for i in range(len(json_cancel_adhoc_booking_response['bookings'])):
                if booking_count == 0 or bookingId != json_cancel_adhoc_booking_response['bookings'][i]['id']:
                    current_booking_count += 1

            if current_booking_count == booking_count:
                Report.logPass(f'Adhoc meeting deleted successfully')
            else:
                Report.logFail(f'Failed to delete Adhoc meetings')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_jasmine_update_adhoc_room_booking(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str, booking_id: str):
        """ Method to update adhoc room booking

            Test:
                 1. Query the API: To update the adhoc room booking
                 PUT /bapi/org/{orgId}/room/{roomId}/agenda/booking/{bookingId}

        """
        try:
            self.banner(f'Update adhoc room booking for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to update adhoc room booking
            update_adhoc_room_booking_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/agenda/booking/{booking_id}"
            Report.logInfo(
                f" Update Adhoc room booking url is: {update_adhoc_room_booking_url}")

            update_end_time = datetime.now()+ timedelta(hours=1) + timedelta(minutes=15) + timedelta(seconds=60)
            updated_booking_end_time = update_end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            log.info(f'Updated booking end time is {updated_booking_end_time}')

            update_adhoc_room_booking_payload = {
                    'endTime': updated_booking_end_time
            }
            Report.logInfo(
                f" Update Adhoc room booking Payload is: {update_adhoc_room_booking_payload}")

            response = requests.put(update_adhoc_room_booking_url, cert=(jasmine_cert_path, jasmine_privatekey_path), json = {'endTime': updated_booking_end_time})
            json_update_adhoc_response = response.json()
            Report.logInfo(
                f" Updated Adhoc room booking api status code:  {response.status_code}")
            Report.logInfo(
                f" Updated Adhoc room booking api json response:  {json_update_adhoc_response}")

            # Updated Adhoc agenda details
            number_of_bookings = len(json_update_adhoc_response['bookings'])
            end_time_not_matching_count = 0
            if number_of_bookings > 0:
                for i in range(len(json_update_adhoc_response['bookings'])):
                    meeting_end_time = json_update_adhoc_response['bookings'][i]['endTime']
                    Report.logInfo(
                    f"Updated Adhoc room booking end time is:  {meeting_end_time}")

                # Validate response end date time with updated booking end time
                    if meeting_end_time[:16] == updated_booking_end_time[:16]:
                        Report.logPass(f'Adhoc meeting request is updated successfully')
                        break
                    else:
                        end_time_not_matching_count += 1
                        if number_of_bookings == end_time_not_matching_count:
                            Report.logFail(f'Failed to update adhoc meeting request')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_room_booking_settings(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str):
        """
        Method to get room booking settings.

            Test:
                 1. Query the API: To get room booking settings
                 GET ~/org/{org-id}/room/{room_id}/booking-settings

        """
        try:
            self.banner(f'Get booking settings for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get room booking settings
            room_booking_setting_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/booking-settings"
            Report.logInfo(
                f" Get Room booking settings url is:  {room_booking_setting_url}")

            response = requests.get(room_booking_setting_url, cert=(jasmine_cert_path, jasmine_privatekey_path))
            Report.logInfo(
                f"Room booking settings status code:  {response.status_code}")
            room_booking_setting_json_response = response.json()
            Report.logInfo(
                f"Room booking settings json response:  {room_booking_setting_json_response}")

            room_booking_policy = room_booking_setting_json_response['bookingPolicy']

            # Get the room booking settings
            if len(room_booking_policy) > 0:
                Report.logPass(f'Room booking settings is {room_booking_policy}')
            else:
                Report.logFail(f'Room booking settings is empty')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_jasmine_room_agenda_snapshot(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id_list: list):
        """
        Method to get room agenda snapshot.

            Test:
                 1. Query the API: To get room agenda snapshot
                 POST /bapi/org/{orgId}/room/agenda/snapshot
                 Request body - { roomIds: Array<string> }

        """
        try:
            self.banner(f'Get agenda snapshot for rooms: {room_id_list}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get jasmine room agenda snapshot
            get_room_agenda_snapshot_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/agenda/snapshot"

            get_room_agenda_snapshot_payload = {
                'roomIds': room_id_list
            }

            response = requests.post(get_room_agenda_snapshot_url, cert=(jasmine_cert_path, jasmine_privatekey_path), json={'roomIds': room_id_list})
            Report.logInfo(
                f" Get room agenda snapshot api status code:  {response.status_code}")
            jasmine_get_agenda_snapshot = response.json()
            Report.logInfo(
                f" Get room agenda snapshot api json response:  {response.json()}")

            # Validate if room agenda snapshot is retrieved
            number_of_bookings = len(jasmine_get_agenda_snapshot)
            if number_of_bookings > 0:
                if(jasmine_get_agenda_snapshot[0]['id'] and jasmine_get_agenda_snapshot[1][
                        'id']) in room_id_list:
                    Report.logPass(f'Room agenda snapshot is retrieved successfully {jasmine_get_agenda_snapshot}')
                else:
                    Report.logFail(f'Failed to retrieve room agenda snapshot')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_jasmine_maps_list(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str,
                                 map_id: str):
        """Method to get room agenda.

            Test:
                 1. Query the API: To get maps list
                 GET /bapi/org/{orgId}/room/{roomId}/maps

        """
        try:
            self.banner(f'Get map list for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get jasmine map list
            map_list_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/maps"

            response_map_list = requests.get(map_list_url, cert=(jasmine_cert_path, jasmine_privatekey_path))
            Report.logInfo(
                f" Get jasmine map list  {response_map_list.status_code}")
            jasmine_map_list_response = response_map_list.json()
            Report.logInfo(
                f" Get jasmine map list api json response:  {response_map_list.json()}")

            jasmine_map_id = jasmine_map_list_response[0]['id']
            if jasmine_map_id == map_id:
                Report.logPass(f'Map retrived for room id {room_id}')
            else:
                Report.logFail(f'There is no meeting scheduled for the current date')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_map_content_by_id(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str, room_id: str,
                                 map_id: str):
        """Method to get map content by map id

            Test:
                 1. Query the API: To get map content by map id
                 GET /bapi/org/{orgId}/map/{mapId}

        """
        try:
            self.banner(f'Get map list for room id: {room_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get map content by map id
            map_content_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/map/{map_id}"

            response_map_content = requests.get(map_content_url, cert=(jasmine_cert_path, jasmine_privatekey_path))
            Report.logInfo(
                f" Get jasmine map content by map id  {response_map_content.status_code}")
            jasmine_map_content_response = response_map_content.json()
            Report.logInfo(
                f" Get jasmine map content api json response:  {response_map_content.json()}")

            jasmine_map_id = jasmine_map_content_response['id']
            jasmine_content = jasmine_map_content_response['content']
            if jasmine_map_id == map_id:
                Report.logPass(f'Successfully retrieved map content for map id {map_id} is {jasmine_content}')
            else:
                Report.logFail(f'Failed to retrieve map content')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_map_to_organization(self, role, map_name):
        """
        TC to add map to organization
        """
        try:
            Report.logInfo(f'Add maps to an organization')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # STEP 1: Configure data to add map to organization
            map_name = map_name
            data_image = jrm.map_data_image
            map_width = 1024
            map_height = 1024
            map_scale = 38

            # STEP 2: Add map to organization
            map_id, floor_path, self.token, self.org_id, org_identifier = self.sync_portal_hot_desks.add_map_to_organization(self.token,
                                                                                                    self.org_id,
                                                                                                    map_name,
                                                                                                    data_image,
                                                                                                    map_width,
                                                                                                    map_height,
                                                                                                    map_scale)

            return map_id, floor_path, self.token, self.org_id, org_identifier

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_flex_desk_session_booking_jasmine(self, role, desk_name, user_id, email_id,desk_device_name,building_timezone):
            """
            TC to book a session for a desk
            """
            try:
                Report.logInfo(f'Book a session for a desk')

                self.token = raiden_helper.signin_method(global_variables.config, role)
                self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

                Report.logInfo(f'{role} Get group provision code for site and provision Coily to Sync Portal')
                browser = BrowserClass()
                browser.close_all_browsers()

                # Step 1: Create Site, building, floor and area
                site = '/Test-' + str(int(random.random() * 10000))
                building = site + '//SVC'
                floor = site + '/SVC//Floor 1'
                area = site + '/SVC/Floor 1//QA'

                response_site = self.sync_portal_hot_desks.add_group(role=role, group_name=site)
                response_building = self.sync_portal_hot_desks.add_group_building(role=role, group_name=building,building_timezone=building_timezone)
                response_floor = self.sync_portal_hot_desks.add_group(role=role, group_name=floor)
                response_area = self.sync_portal_hot_desks.add_group(role=role, group_name=area)

                # Get location id's for site, building, floor
                site_location_id, building_location_id, floor_location_id = "", "", ""
                for i in response_site:
                    if i in site:
                        site_location_id = self.org_id + "-" + response_site[i]['$id']
                        building_location_id = self.org_id + "-" + response_building[i]['SVC']['$id']
                        floor_location_id = self.org_id + "-" + response_floor[i]['SVC']['Floor 1']['$id']
                        area_location_id = self.org_id + "-" + response_area[i]['SVC']['Floor 1']['QA']['$id']

                # Step 2: Create empty desk.
                provision_code, self.desk_id = self.sync_portal_hot_desks.create_empty_desk_and_get_provision_code(
                    role=role, desk_name=desk_name, area_name=area)
                # Remove the separator - from the provision code
                prov_code_without_separator = ''
                for char in provision_code:
                    if char != '-':
                        prov_code_without_separator += char

                # Step 3: Provision coily to sync portal
                self.sync_methods.lna_ip = fp.COILY_IP
                self.lna.login_to_local_network_access_and_connect_to_sync(ip_address=self.sync_methods.lna_ip,
                                                                           user_name=self.sync_methods.lna_user,
                                                                           password=self.sync_methods.lna_pass,
                                                                           provision_code=prov_code_without_separator,
                                                                           device_name=desk_device_name)

                # Step 4: Book session for desk created.
                reservation_id = self.sync_portal_hot_desks.session_booking_for_flex_desk(role, user_id,
                                                                                          email_id,
                                                                                          self.desk_id,
                                                                                          desk_name)

                return site, building, floor, self.desk_id, site_location_id, building_location_id, floor_location_id, area_location_id, reservation_id

            except Exception as e:
                Report.logException(f'{e}')
                raise e


    def tc_get_booking_status_of_desk_by_floorid(self, role: str, jasmine_cert_path: str, jasmine_privatekey_path: str,
                                                 desk_id: str, floor_id: str):
        """Method to fetch booking status of desks by floorId for hydrating map in Jasmine App

            Test:
                 1. Query the API: To get booking status of desks by floorId
                 GET /bapi/org/{orgId}/map/desks
                 Query - floorId

        """
        try:
            self.banner(
                f'Get booking status of desks by floorId for hydrating map in Jasmine App for desk id: {desk_id}')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get booking status of desks by floorId
            get_desk_booking_status_url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/map/desks?floorId={floor_id}"

            response_get_desk_booking_status = requests.get(get_desk_booking_status_url,
                                                            cert=(jasmine_cert_path, jasmine_privatekey_path))

            Report.logInfo(
                f" Response for getting booking status of desks by floorId  {response_get_desk_booking_status}")
            Report.logInfo(
                f" Get booking status of desks by floorId  {response_get_desk_booking_status.status_code}")
            jasmine_map_get_desk_booking_status = response_get_desk_booking_status.json()
            Report.logInfo(
                f" Get booking status of desks by floorId :  {response_get_desk_booking_status.json()}")

            response_status = response_get_desk_booking_status.status_code

            if jasmine_map_get_desk_booking_status[0]['id']  == desk_id:
                Report.logPass(f'Successfully retrieved booking status for desk')
            else:
                Report.logFail(f'Failed to retrieve booking status')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_add_maps(self, role, map_name):
        """
        TC to add maps to an organization under desk group
        """
        try:
            Report.logInfo(f'Add maps to an organization under desk group')

            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # Configure data to add map to organization under desk group
            map_name = map_name
            data_image = jrm.map_data_image
            map_width = 1024
            map_height = 1024
            map_scale = 38

            # STEP 2: Add map to organization
            map_id, floor_path, self.token, self.org_id, org_identifier = self.sync_portal_hot_desks.add_map_to_organization(self.token, self.org_id, map_name,
                data_image, map_width, map_height, map_scale)

            return map_id, floor_path, self.token, self.org_id, org_identifier

        except Exception as e:
            Report.logException(f'{e}')
            raise e

    def tc_upload_room_booking_image(self, role: str):
        """ Method to upload the room booking image

            Test:
                 1. Query the API: To upload the room booking image
                 POST ~/org/{org-id}/img/upload?imageType=RoomBookingBg

        """
        try:
            self.banner(f'Upload the room booking image')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to upload the room booking image
            upload_room_booking_image_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/img/upload?imageType=RoomBookingBg'

            # Image directory path
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            IMAGE_DIRECTORY_PATH = os.path.join(directory, "vc-cloud-apps-automation-e2e", "testsuite_jasmine_api",
                                                "room_booking_images")

            # Image path
            room_booking_image = os.path.join(IMAGE_DIRECTORY_PATH, "city.jpeg")

            upload_room_booking_image_payload = {
                "filename": room_booking_image,
                "md5": "1qyBXRi9rWfNiuGTpBmy8Q=="
            }

            response_upload_room_booking_image = raiden_helper.send_request(
                method="POST", url=upload_room_booking_image_url, body=json.dumps(upload_room_booking_image_payload),
                token=self.token
            )

            image_id = response_upload_room_booking_image['imgId']
            upload_Url = response_upload_room_booking_image['uploadUrl']

            if 'img-upload' in upload_Url and image_id != None:
                Report.logPass(f'Room booking image is uploaded successfully')
            else:
                Report.logFail(f'Failed to upload room booking image')

            return image_id

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_room_booking_image_details(self, role: str, image_id: str):
        """ Method to get the room booking image details

            Test:
                 1. Query the API: To get the room booking image details
                 Get ~/org/{org-id}/img/image_id?imageType=RoomBookingBg

        """
        try:
            self.banner(f'Get the room booking image details')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to get room booking image details
            get_room_booking_image_details_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/img/' + str(image_id) + '?imageType=RoomBookingBg'

            get_room_booking_image_details_payload = {
                "imageType": "RoomBookingBg"
            }

            response_get_room_booking_image_details = raiden_helper.send_request(
                method="GET", url=get_room_booking_image_details_url,
                body=json.dumps(get_room_booking_image_details_payload),
                token=self.token
            )

            room_booking_image_id = response_get_room_booking_image_details['imgId']

            if room_booking_image_id == image_id:
                Report.logPass(f'Room booking image is retrieved successfully')
            else:
                Report.logFail(f'Failed to retrieve room booking image')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_delete_room_booking_uploaded_image(self, role: str, image_id: str):
        """ Method to delete room booking uploaded image

            Test:
                 1. Query the API: To delete room booking uploaded image
                 Delete ~/org/{org-id}/img/image_id?imageType=RoomBookingBg

        """
        try:
            self.banner(f'Delete the room booking image details')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to delete room booking image
            delete_room_booking_image_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/img/' + str(image_id)

            response_delete_room_booking_uploaded_image = raiden_helper.send_request(
                method="DELETE", url=delete_room_booking_image_url,
                token=self.token
            )

            Report.logInfo(
                f" Response after deleting uploaded image:  {response_delete_room_booking_uploaded_image}")

            if len(response_delete_room_booking_uploaded_image) == 0:
                Report.logPass(f'Successfully deleted the uploaded room booking image')
            else:
                Report.logFail(f'Failed to delete the uploaded room booking image')

        except Exception as e:
            Report.logException(f'{e}')

    def tc_get_room_booking_images(self, role: str):
        """ Method to get all room booking images

            Test:
                 1. Query the API: To get all the room booking images
                 Get ~/org/{org-id}/img

        """
        try:
            self.banner(f'Get room booking images')
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            # URL to delete room booking image
            get_room_booking_images_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(
                self.org_id) + '/img/?imageType=RoomBookingBg'

            response_get_room_booking_images = raiden_helper.send_request(
                method="GET", url=get_room_booking_images_url,
                token=self.token
            )

            number_of_room_booking_images = len(response_get_room_booking_images['images'])

            Report.logInfo(
                f" Response getting room booking images:  {response_get_room_booking_images}")

            images_names = []
            if number_of_room_booking_images > 0:
                for i in range(len(response_get_room_booking_images['images'])):
                    images_names.append(response_get_room_booking_images['images'][i]['filename'])
                    if i == (number_of_room_booking_images - 1):
                        Report.logPass(f'Names of room booking images are {images_names}')
            else:
                Report.logFail(f'Failed to retrieve room booking images')

        except Exception as e:
            Report.logException(f'{e}')

