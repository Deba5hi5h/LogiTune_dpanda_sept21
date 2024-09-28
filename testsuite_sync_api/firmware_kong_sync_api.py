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
from apis.sync_api.sync_eventhandler import EventHandler
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
import common.log_helper as log_helper
from common import framework_params as fp
from apis.sync_api.websocketconnection import WebsocketConnection
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncFirmwareAPIKong(SyncBaseAPI):
    """
     Tests to verify product API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncFirmwareAPIKong, cls).setUpClass()

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
        super(LogiSyncFirmwareAPIKong, cls).tearDownClass()

    def setUp(self):
        try:
            super(LogiSyncFirmwareAPIKong, self).setUp()  # Extent Report
            log.info('Starting {}'.format(self._testMethodName))

            self.sync_update = KongSyncUpdate()

            self.sync_update.wait_until_any_ongoing_update_is_finished()

            self.sync_update.downgrade_kong_firmware()

            if not self.sync_update.is_update_visible_by_sync():
                assert False, "There is no update available for tested device."
        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    def tearDown(self):
        self.sync_update.clean_schedule_firmware_update()
        time.sleep(10)  # to let SyncApp finish enumerating the device
        super(LogiSyncFirmwareAPIKong, self).tearDown()  # Extent Report

    def test_001_VC_43781_RallyBar_update_firmware_by_id_to_latest_version_and_check_firmware_update_events(self):
        """Scenario covers commands and events during firmware update on Kong: UpdateFirmwareByProductIdRequest,
        GetFirmwareUpdateProgressRequest, firmwareUpdateStartedEvent, firmwareUpdateProgressEvent
        and firmwareUpdateCompletedEvent.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system
                  4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

            Test:
                 1. Add event listener for firmwareUpdateStartedEvent.
                 2. Create a protobuf API request: UpdateFirmwareByProductIdRequest
                 and send this to the proxy server via a websocket connection.
                 3. Add event listener for GetFirmwareUpdateProgressRequest.
                 4. Create a protobuf API request: GetFirmwareUpdateProgressRequest
                 and send this to the proxy server via a websocket connection.
                 5. Add event listener for firmwareUpdateCompletedEvent.
                 6. Validate that firmwareUpdateStartedEvent appears.
                 7. Validate the response: updateFirmwareByIdResponse.
                 8. Validate that firmwareUpdateProgressEvent appears.
                 9. Validate the response: getFirmwareUpdateProgressResponse.
                 10. Validate that firmwareUpdateCompletedEvent appears.

        """
        try:

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
            # 2. Generate the request message to start update
            # ###############################
            log.debug('2. Generate the request message to start update')
            product_uuid = self.product_uuid['RALLY_BAR']
            loop_start_update = asyncio.new_event_loop()
            websocket_dict_start_update = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict_start_update['msg_buffer'] = product_request.create_update_firmware_by_id(product_uuid, None)
            log.debug('Web socket dictionary - {}'.format(websocket_dict_start_update))

            websocket_conn_v2 = WebsocketConnection(websocket_dict_start_update)
            fw_data = loop_start_update.run_until_complete(websocket_conn_v2.request_response_listener())

            json_formatted_product_data = json.dumps(fw_data, indent=2)
            log.debug('Firmware API - UpdateFirmwareByProductIdRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

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
            # 1.2 Validate the Update Started response
            # ###############################
            fw_response = fw_data['response']['firmwareResponse']['updateFirmwareByIdResponse']['update']
            status_1_2 = SyncHelper.validate_update_firmware_by_id(fw_response, product_uuid)
            assert status_1_2 is True, 'Error in Update Started response'

            # ###############################
            # 1.3 Validate the Update Progress Event response
            # ###############################
            fw_update_progress_event_status = \
            websocket_dict_update_progress["event_response"]['event']['firmwareEvent']['firmwareUpdateProgressEvent'][
                'progress']
            Report.logResponse(websocket_dict_update_progress["event_response"])
            status_1_3 = SyncHelper.validate_firmware_update_progress_Event(fw_update_progress_event_status, product_uuid)
            assert status_1_3 is True, 'Error in Update Progress Event response'

            # ###############################
            # 1.4 Validate the Get Update Progress response
            # ###############################
            update_get_progress_resp_status = get_update_progress_resp['response']['firmwareResponse'][
                'getFirmwareUpdateProgressResponse']['updates']
            status_1_4 = SyncHelper.validate_get_firmware_update_progress(update_get_progress_resp_status, product_uuid)
            assert status_1_4 is True, 'Error'

            # ###############################
            # 1.5 Validate the Update Completed Event response
            # ###############################
            fw_update_completed_event_status = \
            websocket_dict_update_completed["event_response"]['event']['firmwareEvent']['firmwareUpdateCompletedEvent']
            Report.logResponse(websocket_dict_update_completed["event_response"])
            # status_1_5 = SyncHelper.validate_firmware_update_completed_Event(fw_update_completed_event_status, product_uuid)
            status_1_5 = SyncHelper.validate_firmware_update_completed_Event_with_fw_package_version(
                fw_update_completed_event_status, product_uuid, firmware_package_version)
            assert status_1_5 is True, 'Error in Update Completed Event response'

            log_helper.test_result_logger(self.id(), status_1_5)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43782_RallyBar_schedule_firmware_update_by_id_to_latest_version_and_verify_update_scheduling_events(self):
        """Scenario covers commands and events during firmware update on Kong: SetFirmwareUpdateScheduleRequest.

                    Setup:
                          1. LogiSync Application should be running on the host
                          2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                          3. One or more monitored or managed devices have to be connected to system
                          4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

                    Test:
                         1. Add event listener for firmwareUpdateSchedulingEvent.
                         2. Create a protobuf API request: SetFirmwareUpdateScheduleRequest
                         and send this to the proxy server via a websocket connection.
                         3. Validate that firmwareUpdateSchedulingEvent appears.
                         4. Validate the response: SetFirmwareUpdateScheduleRequest.

                """
        try:
            # ###############################
            # 1. Start thread for Firmware Update Schedule event
            # ###############################
            loop_update_scheduled = asyncio.new_event_loop()
            websocket_dict_update_scheduled = {'type': 'LogiSync', 'timeout': 60.0}
            websocket_dict_update_scheduled['event_list'] = ['firmwareUpdateSchedulingEvent']
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_scheduled))

            # Send request to proxy server via a web socket connection
            websocket_conn_update_scheduled = WebsocketConnection(websocket_dict_update_scheduled)

            _thread_firmware_update_scheduled_event = Thread(
                name='logisync_firmware_update_started_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_update_scheduled, loop_update_scheduled,
                                                                 websocket_dict_update_scheduled))
            _thread_firmware_update_scheduled_event.start()
            time.sleep(2)

            # ###############################
            # 2. Generate and send request message to set firmware update schedule
            # ###############################
            loop_schedule_update_request = asyncio.new_event_loop()

            firmware_request = FirmwareRequest()

            product_uuid = self.product_uuid['RALLY_BAR']
            product_model_id = DeviceModelConfig.model_rally_bar
            current_time = int(time.time())
            scheduled_update = {
                'issued_time': current_time,
                'earliest_time': current_time + 21000,
                'latest_time': current_time + 21000 + 2*3600
            }

            websocket_dict_update_scheduled_request = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict_update_scheduled_request['msg_buffer'] = firmware_request.create_set_firmware_update_schedule(product_uuid, product_model_id, scheduled_update)
            log.debug('Web socket dictionary - {}'.format(websocket_dict_update_scheduled_request))

            # Send request to proxy server via a web socket connection
            websocket_con_update_scheduled_request = WebsocketConnection(websocket_dict_update_scheduled_request)

            # Get the response
            firmware_update_data = loop_schedule_update_request.run_until_complete(websocket_con_update_scheduled_request.request_response_listener())
            json_formatted_firmware_update_data = json.dumps(firmware_update_data, indent=2)
            log.debug('Firmware API - SetFirmwareUpdateScheduleRequest : {}'.
                      format(json_formatted_firmware_update_data))
            Report.logResponse(format(json_formatted_firmware_update_data))

            _thread_firmware_update_scheduled_event.join()

            # ###############################
            # 3. Validate the Firmware Update Scheduled Event response
            # ###############################
            event_response = websocket_dict_update_scheduled["event_response"]['event']['firmwareEvent']['firmwareUpdateSchedulingEvent']
            Report.logResponse(websocket_dict_update_scheduled["event_response"])
            status = SyncHelper.validate_set_firmware_update_schedule_response(firmware_response=event_response,
                                                                               product_uuid=product_uuid,
                                                                               scheduled_update=scheduled_update)
            assert status is True, 'Error'

            # ###############################
            # 4. Validate the Set Firmware Update Schedule response
            # ###############################
            fw_response = firmware_update_data['response']['firmwareResponse']['setFirmwareUpdateScheduleResponse']
            status = SyncHelper.validate_set_firmware_update_schedule_response(firmware_response=fw_response,
                                                                               product_uuid=product_uuid,
                                                                               scheduled_update=scheduled_update)
            assert status is True, 'Error'

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43783_RallyBar_update_all_firmware_request(self):
        """Scenario covers commands and events during firmware update on Kong: UpdateAllFirmwareRequest.

                            Setup:
                                  1. LogiSync Application should be running on the host
                                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                                  3. One or more monitored or managed devices have to be connected to system
                                  4. Downgrade device components (Android/Audio/STM/PT/HK) to match specified baseline if needed.

                            Test:
                                 1. Create a protobuf API request: UpdateAllFirmwareRequest
                                 and send this to the proxy server via a websocket connection.
                                 2. Validate that UpdateAllFirmwareRequest appears.
                                 3. Add event listener for firmwareUpdateCompletedEvent.
                                 4. Validate that firmwareUpdateCompletedEvent appears.

                        """
        try:
            # ###############################
            # 1. Generate and send request message to update all firmware
            # ###############################

            firmware_request = FirmwareRequest()
            product_uuid = self.product_uuid['RALLY_BAR']
            loop = asyncio.new_event_loop()
            websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict['msg_buffer'] = firmware_request.create_update_all_firmware()
            log.debug('Web socket dictionary - {}'.format(websocket_dict))

            websocket_conn_v2 = WebsocketConnection(websocket_dict)
            fw_data = loop.run_until_complete(websocket_conn_v2.request_response_listener())

            json_formatted_product_data = json.dumps(fw_data, indent=2)
            log.debug('Firmware API - UpdateAllFirmwareRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # ###############################
            # 2 Validate the Update All Firmware response
            # ###############################

            fw_response = fw_data['response']['firmwareResponse']['updateAllFirmwareResponse']['updates']
            status_2 = SyncHelper.validate_update_all_firmware(fw_response)
            assert status_2 is True, 'Error in Update All Firmware response'

            # ###############################
            # 3. Start thread for Update Completed event and wait until update is finished
            # ###############################
            loop_update_completed = asyncio.new_event_loop()
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
            # 4. Validate the Update Completed Event response
            # ###############################
            fw_update_completed_event_status = \
                websocket_dict_update_completed["event_response"]['event']['firmwareEvent']['firmwareUpdateCompletedEvent']
            Report.logResponse(websocket_dict_update_completed["event_response"])
            status_4 = SyncHelper.validate_firmware_update_completed_Event(fw_update_completed_event_status, product_uuid)
            assert status_4 is True, 'Error in Update Completed Event response'

            log_helper.test_result_logger(self.id(), status_4)

        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareAPIKong)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
