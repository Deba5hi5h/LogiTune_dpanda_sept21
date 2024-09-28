import asyncio
import logging
from threading import Thread
from apis.sync_api.device_firmware_utils.kong_sync_update import KongSyncUpdate
from apis.sync_api.firmwarerequest import FirmwareRequest
from base.sync_base_api import SyncBaseAPI
from apis.sync_api.sync_eventhandler import EventHandler
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
import common.log_helper as log_helper
from apis.sync_api.websocketconnection import WebsocketConnection
from extentreport.report import Report
import time
import json
import sys
from apis.raiden_api import raiden_helper
from apis.raiden_api import raiden_validation_methods
from common import raiden_config
import unittest
from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from base import global_variables

log = logging.getLogger(__name__)


class LogiSyncFirmwareAPIKongSyncAppPortal(UIBase, SyncBaseAPI):
    """
     Tests to verify product API

    """
    sync_app = SyncAppMethods()
    device_name = 'Rally Bar'
    room_name = None
    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncFirmwareAPIKongSyncAppPortal, cls).setUpClass()

            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(LogiSyncFirmwareAPIKongSyncAppPortal, cls).tearDownClass()

    def setUp(self):
        try:
            super(LogiSyncFirmwareAPIKongSyncAppPortal, self).setUp()  # Extent Report
            log.info('Starting {}'.format(self._testMethodName))

            self.sync_update = KongSyncUpdate()

            self.sync_update.wait_until_any_ongoing_update_is_finished()

            self.sync_update.downgrade_kong_firmware()

            if not self.sync_update.is_update_visible_by_sync():
                assert False, "There is no update available for tested device."

            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.get_org_id(self.role, global_variables.config, self.token)

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    def tearDown(self):
        self.sync_update.clean_schedule_firmware_update()
        time.sleep(10)  # to let SyncApp finish enumerating the device
        super(LogiSyncFirmwareAPIKongSyncAppPortal, self).tearDown()  # Extent Report

    def test_001_VC_55609_RallyBar_trigger_Firmware_Update_via_Sync_Portal_and_check_firmware_update_events(self):
        """Scenario covers triggering firmware update of Kong via Sync Portal and checking events during firmware update
        on Kong: GetFirmwareUpdateProgressRequest, firmwareUpdateStartedEvent, firmwareUpdateProgressEvent
        and firmwareUpdateCompletedEvent.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system
                  4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

            Test:
                 1. Add event listener for firmwareUpdateStartedEvent.
                 2. Trigger firmware update for Rally Bar via Sync Portal.
                 3. Add event listener for GetFirmwareUpdateProgressRequest.
                 4. Create a protobuf API request: GetFirmwareUpdateProgressRequest
                 and send this to the proxy server via a websocket connection.
                 5. Add event listener for firmwareUpdateCompletedEvent.
                 6. Validate that firmwareUpdateStartedEvent appears.
                 7. Validate the response: updateFirmwareByIdResponse.
                 8. Validate that firmwareUpdateProgressEvent appears.
                 9. Validate the response: getFirmwareUpdateProgressResponse.
                 10. Validate that firmwareUpdateCompletedEvent appears.
                 11. Validate the firmware version via GET Device Sync Portal API.

        """
        try:
            LogiSyncFirmwareAPIKongSyncAppPortal.room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.close()
            # Create configuration request object
            product_request = FirmwareRequest()
            log.debug('Product request {}'.format(product_request))

            # ###############################
            # 1. Start thread for Update Start event
            # ###############################
            log.debug('1. Start thread for Update Start event')
            loop_update_started = asyncio.get_event_loop()
            websocket_dict_update_start = {'type': 'LogiSync', 'timeout': 60.0}
            websocket_dict_update_start['event_list'] = ['firmwareUpdateStartedEvent']
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_start))

            # Send request to proxy server via a web socket connection
            websocket_conn_update_started = WebsocketConnection(websocket_dict_update_start)

            _thread_firmware_update_started_event = Thread(
                name='logisync_firmware_update_started_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_update_started, loop_update_started,
                                                                 websocket_dict_update_start))
            _thread_firmware_update_started_event.start()
            time.sleep(2)

            # ###############################
            # 2. Trigger Firmware update of Rally Bar via Sync Portal
            # ###############################
            log.debug('2. Trigger Firmware update of Rally Bar via Sync Portal')
            # Trigger firmware update
            firmware_update_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + \
                                  "/device/software"
            device_id_rally_bar = raiden_helper.get_device_id_from_room_name(global_variables.config, self.room_name,
                                                                             self.org_id, self.token, self.device_name)
            _data = {'deviceIds': [device_id_rally_bar], "updateNow": True}

            response = raiden_helper.send_request(
                method='POST', url=firmware_update_url, body=json.dumps(_data), token=self.token
            )
            time.sleep(30)
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response after triggering firmware update via Sync Portal- {}'.format(json_formatted_response))

            _thread_firmware_update_started_event.join()

            # ###############################
            # 3. Start thread for Update Progress event
            # ###############################
            log.debug('3. Start thread for Update Progress event')
            time.sleep(15)
            loop_update_progress = asyncio.get_event_loop()
            websocket_dict_update_progress = {'type': 'LogiSync', 'timeout': 90.0}
            websocket_dict_update_progress['event_list'] = ['firmwareUpdateProgressEvent']
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_progress))

            # Send request to proxy server via a web socket connection
            websocket_conn_update_progress = WebsocketConnection(websocket_dict_update_progress)

            _thread_firmware_update_progress_event = Thread(
                name='logisync_firmware_update_progress_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_update_progress, loop_update_progress,
                                                                 websocket_dict_update_progress))
            _thread_firmware_update_progress_event.start()
            time.sleep(2)
            _thread_firmware_update_progress_event.join()

            # ###############################
            # 4. Generate and send request message to get firmware update progress
            # ###############################
            log.debug('4. Generate and send request message to get firmware update progress')
            loop_update_progress_resp = asyncio.get_event_loop()
            product_uuid = self.product_uuid['RALLY_BAR']
            websocket_dict_update_progress_resp = {'type': 'LogiSync', 'timeout': 90.0}
            websocket_dict_update_progress_resp['msg_buffer'] = product_request.create_get_firmware_update_progress()
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_progress_resp))

            # Send request to proxy server via a web socket connection
            websocket_con_update_progress_resp = WebsocketConnection(websocket_dict_update_progress_resp)

            # Get the response
            get_update_progress_resp = loop_update_progress_resp.run_until_complete(websocket_con_update_progress_resp.request_response_listener())
            json_formatted_update_progress_resp = json.dumps(get_update_progress_resp, indent=2)
            log.debug('Firmware API - GetFirmwareUpdateProgressRequest : {}'.
                      format(json_formatted_update_progress_resp))
            Report.logResponse(format(json_formatted_update_progress_resp))

            fw_update_response = get_update_progress_resp['response']['firmwareResponse']['getFirmwareUpdateProgressResponse']['updates'][0]
            firmware_package_version = fw_update_response['firmwarePackageVersion']

            # ###############################
            # 5. Start thread for Update Completed event
            # ###############################
            log.debug('5. Start thread for Update Completed event')
            loop_update_completed = asyncio.get_event_loop()
            websocket_dict_update_completed = {'type': 'LogiSync', 'timeout': 1800.0}
            websocket_dict_update_completed['event_list'] = ['firmwareUpdateCompletedEvent']
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_completed))

            # Send request to proxy server via a web socket connection
            websocket_conn_update_completed = WebsocketConnection(websocket_dict_update_completed)

            _thread_firmware_update_completed_event = Thread(
                name='logisync_firmware_update_completed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_update_completed, loop_update_completed,
                                                                 websocket_dict_update_completed))
            _thread_firmware_update_completed_event.start()
            time.sleep(2)
            _thread_firmware_update_completed_event.join()

            # ###############################
            # 1.1 Validate the Update Started Event response
            # ###############################
            fw_update_started_event_status = websocket_dict_update_start["event_response"]['event']['firmwareEvent'][
                'firmwareUpdateStartedEvent']
            Report.logResponse(websocket_dict_update_start["event_response"])
            status_1_1 = SyncHelper.validate_firmware_update_started_Event(fw_update_started_event_status, product_uuid)
            assert status_1_1 is True, 'Error in Update Started Event response'

            # ###############################
            # 1.2 Validate the Update Progress Event response
            # ###############################
            fw_update_progress_event_status = \
            websocket_dict_update_progress["event_response"]['event']['firmwareEvent']['firmwareUpdateProgressEvent'][
                'progress']
            Report.logResponse(websocket_dict_update_progress["event_response"])
            status_1_2 = SyncHelper.validate_firmware_update_progress_Event(fw_update_progress_event_status, product_uuid)
            assert status_1_2 is True, 'Error in Update Progress Event response'

            # ###############################
            # 1.3 Validate the Get Update Progress response
            # ###############################
            update_get_progress_resp_status = get_update_progress_resp['response']['firmwareResponse'][
                'getFirmwareUpdateProgressResponse']['updates']
            status_1_3 = SyncHelper.validate_get_firmware_update_progress(update_get_progress_resp_status, product_uuid)
            assert status_1_3 is True, 'Error'

            # ###############################
            # 1.4 Validate the Update Completed Event response
            # ###############################
            fw_update_completed_event_status = \
            websocket_dict_update_completed["event_response"]['event']['firmwareEvent']['firmwareUpdateCompletedEvent']
            Report.logResponse(websocket_dict_update_completed["event_response"])
            # status_1_4 = SyncHelper.validate_firmware_update_completed_Event(fw_update_completed_event_status, product_uuid)
            status_1_4 = SyncHelper.validate_firmware_update_completed_Event_with_fw_package_version(
                fw_update_completed_event_status, product_uuid, firmware_package_version)
            assert status_1_4 is True, 'Error in Update Completed Event response'
            time.sleep(120)

            # ###############################
            # 1.4 Validate the firmware package version in Sync Portal
            # ###############################
            get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/device/" + \
                             device_id_rally_bar

            Report.logInfo('GET call')
            Report.logInfo(get_device_url)

            response = raiden_helper.send_request(
                method='GET', url=get_device_url, token=self.token
            )
            time.sleep(2)
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response for GET Device API- {}'.format(json_formatted_response))
            status_1_5 = raiden_validation_methods.validate_firmware_version(response, firmware_package_version)
            log_helper.test_result_logger(self.id(), status_1_5)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')



if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareAPIKongSyncAppPortal)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
