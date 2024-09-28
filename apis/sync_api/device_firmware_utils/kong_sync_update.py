import asyncio
import json
import logging
import time

from common.config import DeviceModelConfig
from apis.sync_api.firmwarerequest import FirmwareRequest
from apis.sync_api.device_firmware_utils.device import AndroidBase
from apis.sync_api.device_firmware_utils.utils import get_components_versions_by_manifest
from common.framework_params import IP_KONG_FIRMWARE_TEST
import apis.helper as helper
import apis.process_helper as process_helper
from apis.sync_helper import SyncHelper
from common import framework_params as fp
from apis.sync_api.websocketconnection import WebsocketConnection

log = logging.getLogger(__name__)



class KongSyncUpdate:

    def downgrade_kong_firmware(self):
        try:
            android, audio, pt, zf, hk, collabOS = get_components_versions_by_manifest("KONG_COLLAB_1_2.587")

            log.debug("Start adb server")
            process_helper.execute_command("adb start-server")
            time.sleep(5)

            platform = helper.get_name_of_os()
            kong = AndroidBase(platform, IP_KONG_FIRMWARE_TEST)

            # install android image if needed
            version_matches, installed = kong.install_android_image(android)
            assert version_matches is True

            if installed:
                # stop and start adb server to allow SYNC connection when device is being rebooted
                log.debug("Stop adb server")
                process_helper.execute_command("adb kill-server")
                time.sleep(120)
                log.debug("Start adb server")
                process_helper.execute_command("adb start-server")
                time.sleep(5)
                # establish adb connection after reboot
                kong = AndroidBase(platform, IP_KONG_FIRMWARE_TEST)

            # update component if needed
            log.debug("Installing components...")
            components = {"PT": pt, "HK": hk, "ZF": zf, "Audio": audio}
            # components = {"HK": hk, "Audio": audio} #diddy
            components_reinstalled = 0
            for key, value in components.items():
                comp_version_matches, comp_installed = kong.update_component_with_file(key, value)
                assert comp_version_matches is True, f"updated {key} does not match target version"
                if comp_installed:
                    components_reinstalled += 1
                    log.debug(f"{key} updated successfully to {value}")

            if components_reinstalled > 0:
                # reboot device if any component reinstalled to be sure all component are loaded
                # stop and start adb server to allow SYNC connection when device is being rebooted
                log.debug("Reboot device.")
                kong.device_reboot()
                log.debug("Stop adb server")
                process_helper.execute_command("adb kill-server")
                time.sleep(120)

            if platform == "windows":
                log.debug("Stop adb server")
                process_helper.execute_command("adb kill-server")
                time.sleep(5)

        except Exception as e:
            log.error('Unable to prepare Android components for upgrade tests.')
            raise e

    def reboot_device(self):
        log.debug("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(5)

        platform = helper.get_name_of_os()
        kong = AndroidBase(platform, IP_KONG_FIRMWARE_TEST)

        log.debug(f"Send command: adb -s {IP_KONG_FIRMWARE_TEST} reboot")
        kong.device_reboot()

        if platform == "windows":
            log.debug("Stop adb server")
            process_helper.execute_command("adb kill-server")
            time.sleep(5)

    def clean_schedule_firmware_update(self):
        try:
            # Generate the request message
            loop_schedule_update_request = asyncio.new_event_loop()
            firmware_request = FirmwareRequest()
            product_uuid = self.product_uuid['RALLY_BAR']
            product_model_id = DeviceModelConfig.model_rally_bar
            scheduled_update = None
            websocket_dict_update_scheduled_request = {'type': 'LogiSync', 'timeout': 120.0}
            websocket_dict_update_scheduled_request[
                'msg_buffer'] = firmware_request.create_set_firmware_update_schedule(
                product_uuid, product_model_id, scheduled_update)
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_scheduled_request))
            # Send request to proxy server via a web socket connection
            websocket_con_update_scheduled_request = WebsocketConnection(websocket_dict_update_scheduled_request)
            # Get the response
            firmware_update_data = loop_schedule_update_request.run_until_complete(
                websocket_con_update_scheduled_request.request_response_listener())
            json_formatted_firmware_update_data = json.dumps(firmware_update_data, indent=2)
            log.debug('TEAR DOWNFirmware API - GetLatestFirmwareByProductIdRequest : {}'.
                      format(json_formatted_firmware_update_data))
            # Validate the response
            fw_response = firmware_update_data['response']['firmwareResponse']['setFirmwareUpdateScheduleResponse']
            status = SyncHelper.validate_set_firmware_update_schedule_response(firmware_response=fw_response,
                                                                               product_uuid=product_uuid,
                                                                               scheduled_update=scheduled_update)
            assert status is True, 'Error'
        except Exception as e:
            log.error('Unable to clean scheduled update.')
            raise e

    def is_update_visible_by_sync(self, max_tries=15):

        tries = 0
        firmware_request = FirmwareRequest()
        log.debug('Product request {}'.format(firmware_request))
        loop = asyncio.get_event_loop()

        # Generate the request message
        product_uuid = self.product_uuid['RALLY_BAR']
        websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
        websocket_dict['msg_buffer'] = firmware_request.create_get_latest_firmware(product_uuid)
        log.debug('Web socket dictionary - {}'.format(websocket_dict))

        while tries < max_tries:
            tries += 1
            log.debug(f'Retry {tries}. Check for available update for Kong.')

            try:
                # Send request to proxy server via a web socket connection
                websocket_con = WebsocketConnection(websocket_dict)

                # Get the response
                product_data = loop.run_until_complete(websocket_con.request_response_listener())
                json_formatted_product_data = json.dumps(product_data, indent=2)
                log.debug('Firmware API - GetLatestFirmwareByProductIdRequest : {}'.
                          format(json_formatted_product_data))

                # Validate the response
                fw_response = product_data['response']['firmwareResponse']['getLatestFirmwareByProductIdResponse']

                # If update not found it should throw exception!
                log.debug(f"Update found. Target version is: {fw_response['latestFirmwarePackageVersion']}")

                return True

            except Exception as e:
                log.debug(f'Update not found.')

            time.sleep(15)

        return False

    def wait_until_any_ongoing_update_is_finished(self):

        is_ongoing_update = True
        retry_counter = 0

        while is_ongoing_update:
            try:
                retry_counter += 1
                firmware_request = FirmwareRequest()
                loop_error_event_resp = asyncio.get_event_loop()
                websocket_dict_error_event_resp = {'type': 'LogiSync', 'timeout': 30.0}
                websocket_dict_error_event_resp[
                    'msg_buffer'] = firmware_request.create_get_firmware_update_progress()
                log.debug('Web socket dictionary - {}'.format(websocket_dict_error_event_resp))

                # Send request to proxy server via a web socket connection
                websocket_con_update_progress_resp = WebsocketConnection(websocket_dict_error_event_resp)

                # Get the response
                get_update_progress_resp = loop_error_event_resp.run_until_complete(
                    websocket_con_update_progress_resp.request_response_listener())
                json_formatted_update_progress_resp = json.dumps(get_update_progress_resp, indent=2)
                log.debug('Firmware API - GetFirmwareUpdateProgressRequest : {}'.
                          format(json_formatted_update_progress_resp))

                fw_response = get_update_progress_resp['response']['firmwareResponse'][
                    'getFirmwareUpdateProgressResponse']

                # If update not found it should throw exception!
                log.debug(f"Ongoing update found: {fw_response['updates']}. Check again in 20 sec.")

                if retry_counter == 65:
                    # 65*20sec is more than 21 minutes (timeout for Sync installation)
                    assert False, "Problem with ongoing update blocking test execution."

                time.sleep(20)

            except Exception as e:
                is_ongoing_update = False
                log.debug(f'Update not found.')

        if retry_counter > 1:
            log.debug(f'Wait for Sync to close firmware process.')
            time.sleep(120)