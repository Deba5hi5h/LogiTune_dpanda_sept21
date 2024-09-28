import asyncio
import json
import sys
import time
import unittest
import logging
from threading import Thread

from common.config import DeviceModelConfig
from apis.sync_api.device_firmware_utils.kong_sync_update import KongSyncUpdate
from apis.sync_api.firmwarerequest import FirmwareRequest
from base.sync_base_api import SyncBaseAPI
from apis.sync_api.sync_errormessages import SyncErrorMessages
from apis.sync_api.sync_eventhandler import EventHandler
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
import common.log_helper as log_helper
from common import framework_params as fp
from apis.sync_api.websocketconnection import WebsocketConnection
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncFirmwareErrorsAPIKong(SyncBaseAPI):
    """
     Tests to verify product API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncFirmwareErrorsAPIKong, cls).setUpClass()

            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(LogiSyncFirmwareErrorsAPIKong, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncFirmwareErrorsAPIKong, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.sync_update = KongSyncUpdate()

        self.sync_update.wait_until_any_ongoing_update_is_finished()

        self.sync_update.downgrade_kong_firmware()

        if not self.sync_update.is_update_visible_by_sync():
            assert False, "There is no update available for tested device."

    def tearDown(self):
        self.sync_update.clean_schedule_firmware_update()
        time.sleep(10) #to let SyncApp finish enumarating the device
        super(LogiSyncFirmwareErrorsAPIKong, self).tearDown()  # Extent Report

    def test_001_VC_43784_RallyBar_firmware_update_error_event_when_sending_image_to_device(self):
        """Scenario covers commands and events during firmware update on Kong: UpdateAllFirmwareRequest.

                Setup:
                    1. LogiSync Application should be running on the host
                    2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                    3. One or more monitored or managed devices have to be connected to system
                    4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

                Test:
                    1. Create a protobuf API request: UpdateFirmwareByIdRequest
                    and send this to the proxy server via a websocket connection.
                    2. Validate that UpdateFirmwareByIdRequest appears.
                    3. Reboot Device at the beginning of the update.
                    3. Add event listener for firmwareUpdateErrorEvent.
                    4. Validate that firmwareUpdateErrorEvent appears with correct error message.

        """
        try:

            log.debug('Get update error event when not possible to send image to device.')
            # Create configuration request object
            firmware_request = FirmwareRequest()
            log.debug('Product request {}'.format(firmware_request))

            # ###############################
            # 1. Generate the request message to start update
            # ###############################

            product_uuid = self.product_uuid['RALLY_BAR']
            loop_update_start = asyncio.new_event_loop()
            websocket_dic_update_start = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dic_update_start['msg_buffer'] = firmware_request.create_update_firmware_by_id(product_uuid, None)
            log.debug('Web socket dictionary - {}'.format(websocket_dic_update_start))

            websocket_conn_update_start = WebsocketConnection(websocket_dic_update_start)
            fw_data = loop_update_start.run_until_complete(websocket_conn_update_start.request_response_listener())

            json_formatted_product_data = json.dumps(fw_data, indent=2)
            log.debug('Firmware API - UpdateFirmwareByProductIdRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            fw_response = fw_data['response']['firmwareResponse']['updateFirmwareByIdResponse']['update']
            status_1 = SyncHelper.validate_update_firmware_by_id(fw_response, product_uuid)
            assert status_1 is True, 'Error in Update Started response'

            # ###############################
            # 2. Reboot device at the beginning of update process
            # ###############################
            time.sleep(10)
            self.sync_update.reboot_device()

            # ###############################
            # 3. Start thread for Update Progress event
            # ###############################
            loop_error_event = asyncio.new_event_loop()
            websocket_dict_error_event = {'type': 'LogiSync', 'timeout': 250.0}
            websocket_dict_error_event['event_list'] = ['firmwareUpdateErrorEvent']
            log.debug('Web socket dictionary - {}'.format(websocket_dict_error_event))

            # Send request to proxy server via a web socket connection
            websocket_conn_error_event = WebsocketConnection(websocket_dict_error_event)

            _thread_firmware_update_error_event = Thread(
                name='logisync_firmware_update_error_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_error_event, loop_error_event,
                                                                 websocket_dict_error_event))
            _thread_firmware_update_error_event.start()
            time.sleep(2)

            _thread_firmware_update_error_event.join()

            fw_update_error_event_status = websocket_dict_error_event["event_response"]['event']['firmwareEvent'][
                'firmwareUpdateErrorEvent']
            Report.logResponse(websocket_dict_error_event["event_response"])
            errors = SyncErrorMessages()
            status_2 = SyncHelper.validate_firmware_update_error_Event(fw_update_error_event_status, product_uuid, errors.error_messages[0]['FailedToSendImage'])

            assert status_2 is True, 'Error in Update Error Event response'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43786_RallyBar_error_during_firmware_update_schedule(self):
        """Scenario check response on wrong time setup during Firmware Update Schedule.

                    Setup:
                          1. LogiSync Application should be running on the host
                          2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                          3. One or more monitored or managed devices have to be connected to system
                          4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

                    Test:
                         1. Create a protobuf API request: SetFirmwareUpdateScheduleRequest with 'latest' time before 'earliest'
                         and send this to the proxy server via a websocket connection.
                         2. Validate the response: SetFirmwareUpdateScheduleRequest consist of correct error message.

        """
        try:
            # ###############################
            # 1. Generate and send request message to set firmware update schedule
            # ###############################
            loop_schedule_update_request = asyncio.new_event_loop()

            firmware_request = FirmwareRequest()

            product_uuid = self.product_uuid['RALLY_BAR']
            product_model_id = DeviceModelConfig.model_rally_bar
            current_time = int(time.time())
            scheduled_update = {
                'issued_time': current_time,
                'earliest_time': current_time + 21000,
                'latest_time': current_time + 21000 - 2 * 3600
            }

            websocket_dict_update_scheduled_request = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict_update_scheduled_request[
                'msg_buffer'] = firmware_request.create_set_firmware_update_schedule(product_uuid, product_model_id,
                                                                                     scheduled_update)
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_scheduled_request))

            # Send request to proxy server via a web socket connection
            websocket_con_update_scheduled_request = WebsocketConnection(websocket_dict_update_scheduled_request)

            # Get the response
            firmware_update_data = loop_schedule_update_request.run_until_complete(
                websocket_con_update_scheduled_request.request_response_listener())
            json_formatted_firmware_update_data = json.dumps(firmware_update_data, indent=2)
            log.debug('Firmware API - SetFirmwareUpdateScheduleRequest : {}'.
                      format(json_formatted_firmware_update_data))
            Report.logResponse(format(json_formatted_firmware_update_data))

            # ###############################
            # 2. Validate the Set Firmware Update Schedule response
            # ###############################
            fw_response = firmware_update_data['response']['firmwareResponse']['setFirmwareUpdateScheduleResponse']
            Report.logResponse(firmware_update_data["response"])
            errors = SyncErrorMessages()
            status = SyncHelper.validate_set_firmware_update_schedule_response(firmware_response=fw_response,
                                                                               product_uuid=product_uuid,
                                                                               scheduled_update=scheduled_update,
                                                                               error=errors.error_messages[0]['InvalidScheduleRequestData'])
            assert status is True, 'Error'

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareErrorsAPIKong)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
