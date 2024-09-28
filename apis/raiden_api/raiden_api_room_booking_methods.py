import json
import logging
import os

from apis.raiden_api import raiden_helper, raiden_validation_methods

from base.base_ui import UIBase
from common import (
    raiden_config,
    jasmine_config,
    tap_scheduler_config as tps,
    framework_params as fp,
)
from common.usb_switch import *

from extentreport.report import Report

log = logging.getLogger(__name__)


class SyncPortalRoomBookingMethods(UIBase):
    org_id = None
    token = None

    def set_group_room_booking_settings_to_default(self, role):
        """
        Method to set group room booking settings to default

        :param role:

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            raiden_helper.set_group_room_booking_settings_to_default(jasmine_config.JASMINE_UI_GROUP_NAME,
                                                                     self.org_id, self.token)

        except Exception as e:
            Report.logException(f'{e}')

    def set_settings_pin_for_group(self, role, code='0000'):
        """
        Set Settings pin for group

        :param role:
        :param code:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            raiden_helper.set_settings_pin_for_group(jasmine_config.JASMINE_UI_GROUP_NAME,
                                                     self.org_id, self.token, code)

        except Exception as e:
            Report.logException(f'{e}')

    def provision_nintendo_to_an_existing_room(
        self, role, room_name, on_name_conflict="Fail", max_occupancy=6
    ):
        """
        Provision Tap Scheduler to an existing room
        :param role:
        :param room_name:
        :param on_name_conflict:
        :param max_occupancy:
        """
        try:
            Report.logInfo(f"{role} - Initiate appliance provisioning")
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(
                role, global_variables.config, self.token
            )
            room_id = raiden_helper.get_room_id_from_room_name(
                global_variables.config, self.org_id, room_name, self.token
            )
            appliance_init_prov_payload = {
                "serial": str(raiden_helper.random_string_generator()),
                "roomId": f"{room_id}",
                "onNameConflict": on_name_conflict,
                "occupancyMode": "Disabled",
                "maxOccupancy": max_occupancy,
                "ttl": 20,
            }
            init_prov_url = (
                global_variables.config.BASE_URL
                + raiden_config.ORG_ENDPNT
                + str(self.org_id)
                + "/appliance/prov"
            )
            Report.logInfo(f"Initiate Provisioning URL is: {init_prov_url}")
            response = raiden_helper.send_request(
                method="POST",
                url=init_prov_url,
                body=json.dumps(appliance_init_prov_payload),
                token=self.token,
            )
            Report.logInfo(
                f"{role}: Initiate Appliance Provisioning request with payload: {appliance_init_prov_payload}"
            )

            Report.logInfo(
                f"Response received after initiating provisioning: {response}"
            )

            # Step2: Complete Provisioning for an appliance
            provision_id = response["url"].split("/")[6]
            log.debug(
                f"Provisioning Id that is extracted from the response of initiate provisioning is {provision_id}"
            )
            device_type = "Nintendo"
            device_name = "Tap Scheduler"
            complete_prov_url = (
                global_variables.config.BASE_URL
                + "/api/appliance/prov/"
                + str(provision_id)
                + "/complete"
            )
            Report.logInfo(f"Complete provisioning URL: {complete_prov_url}")
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
                    "ip": fp.NINTENDO_IP,
                }
            }
            Report.logInfo(
                f" Complete Provisioning Request Payload {complete_prov_payload}"
            )
            response = raiden_helper.send_request(
                method="POST",
                url=complete_prov_url,
                body=json.dumps(complete_prov_payload),
            )
            Report.logInfo(f" Complete Provisioning Response is:  {response}")

            resp = response["appInfo"]["com.logitech.vc.jasmine"]
            device_id = response["deviceId"]

            # Get Certificate
            start_certificate = resp.find("-----BEGIN CERTIFICATE-----")
            end_certificate = resp.find('-----END CERTIFICATE-----"')
            certificate = (
                resp[start_certificate:end_certificate] + "-----END CERTIFICATE-----"
            )
            certificate = certificate.replace("\\n", "\n")
            Report.logInfo(f" Certificate Response is:  {certificate}")

            # Get Private Key
            start_privatekey = resp.find("-----BEGIN PRIVATE KEY-----")
            end_privatekey = resp.find('-----END PRIVATE KEY-----"')
            private_key = (
                resp[start_privatekey:end_privatekey] + "-----END PRIVATE KEY-----"
            )
            private_key = private_key.replace("\\n", "\n")
            Report.logInfo(
                f" Private key after completing provisioning is:  {private_key}"
            )

            Report.logInfo(f" Complete Provisioning Room Response:  {response['room']}")
            Report.logInfo("Complete Room Provisioning")
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            (
                provision_status,
                room_id,
            ) = raiden_validation_methods.validate_complete_provisioning_appliance(
                role,
                response,
                room_name,
                appliance_init_prov_payload["maxOccupancy"],
                on_name_conflict="Fail",
            )
            # Directory name
            directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            DIR_PATH = os.path.join(
                directory,
                "testsuite_jasmine_api",
                "meeting_rooms",
            )

            jasmine_cert_path = os.path.join(DIR_PATH, "jasmine_certificate.pem")
            jasmine_privatekey_path = os.path.join(DIR_PATH, "jasmine_privatekey.pem")

            file_names = [jasmine_cert_path, jasmine_privatekey_path]

            for name in file_names:
                with open(name, "w") as file:
                    if name == jasmine_cert_path:
                        file.write(certificate)
                    elif name == jasmine_privatekey_path:
                        file.write(private_key)
                    file.close()

            Report.logInfo(
                f" Certificate path is {jasmine_cert_path} private key path is:  {jasmine_privatekey_path}"
            )

            assert provision_status is True, "Error in status"
            return room_id, device_id, jasmine_cert_path, jasmine_privatekey_path

        except Exception as e:
            Report.logException(f"{e}")

    def deprovision_device(self, role: str, room_id: str, device_id: str):
        """Method to deprovision device.
        :param role:
        :param room_id:
        :param device_id:
        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(role, global_variables.config, self.token)

            raiden_helper.deprovision_device(role, self.token, self.org_id, room_id, device_id)

        except Exception as e:
            Report.logException(f'{e}')