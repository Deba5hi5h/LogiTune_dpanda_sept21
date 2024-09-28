import logging
import unittest
import sys
import asyncio
import json
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
from apis.sync_api.roomrequest import RoomRequest
from apis.sync_api.websocketconnection import WebsocketConnection
import common.log_helper as log_helper
import time
from threading import Thread
from apis.sync_api.sync_eventhandler import EventHandler
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncRoomAPI(SyncBaseAPI):
    """
     Tests to verify Room API. Make sure the room is connected to an organization via Sync Portal and ensure that
     insights is enabled for the room.

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncRoomAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')
            cls.room_info = cls.get_init_room_info()
            cls.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.set_init_room_info(cls.room_info)
        super(LogiSyncRoomAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncRoomAPI, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncRoomAPI, self).tearDown()  # Extent Report
        del self.websocket_dict

    @classmethod
    def get_init_room_info(cls):
        """
        Get intial room information so that we can save initial configuration.
        :return:
        """
        try:
            log.debug('Get the initial Room information')
            room_request = RoomRequest()
            cls.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            cls.websocket_dict['msg_buffer'] = room_request.create_get_room_information_request()
            websocket_con = WebsocketConnection(cls.websocket_dict)

            room_data = cls.loop.run_until_complete(websocket_con.request_response_listener())
            room_info = room_data['response']['roomResponse']['getRoomInformationResponse']
            status = SyncHelper.validate_getInitRoomInfo(room_info)
            assert status is True, 'Error'
            return room_info

        except AssertionError as e:
            log.error('Unable to setup sync config in setUpClass')
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    @classmethod
    def set_init_room_info(cls, room_info):
        """
        Function to set the room information to the initial provided data.
        :param room_info:
        :return:
        """
        try:
            log.debug('Set the room information back to the initial room information')
            room_request = RoomRequest()
            room_information = room_info['roomInformation']
            room_info_dict = {0: str(room_information['roomName']), 1: str(room_information['maxOccupancy'])}
            cls.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            cls.websocket_dict['msg_buffer'] = room_request.create_bulk_set_room_information_request(
                room_info_dict)
            websocket_con = WebsocketConnection(cls.websocket_dict)
            room_data = cls.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - BulkSetRoomInformationResponse - Set the room data back to initial information : {}'.
                      format(json_formatted_room_data))

            # Validate the response
            room_data = room_data['response']['roomResponse']['bulkSetRoomInformationResponse']
            status = SyncHelper.validate_setInitRoomInfo(room_data, room_info_dict)
            assert status is True, 'Error'
            time.sleep(5)

        except AssertionError as e:
            log.error('Unable to restore sync config in tearDownClass')
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_001_VC_43035_getRoomInformationRequest(self):
        """Message: GetRoomInformationRequest
            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
            Test:
                 1. Create a protobuf API request: GetRoomInformationRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns GetRoomInformationResponse.
        """
        try:
            self.banner('Message: GetRoomInformationRequest')
            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_get_room_information_request()
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - GetRoomInformationRequest : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room_info = room_data['response']['roomResponse']['getRoomInformationResponse']
            status = SyncHelper.validate_getRoomInformationResponse(room_info)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43036_setRoomNameRequest(self):
        """Message: SetRoomNameRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: SetRoomNameRequest providing room_name as input.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRoomNameResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: SetRoomNameRequest')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Change the room name to Test-Room
            room_name = 'Test-Room'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_room_name_request(room_name)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - setRoomNameResponse : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room = room_data['response']['roomResponse']['setRoomNameResponse']
            status = SyncHelper.validate_setRoomNameResponse(room, room_name)

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43037_setRoomMaxOccupancyRequest(self):
        """Message: SetRoomMaxOccupancyRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: SetRoomMaxOccupancyRequest providing max_occupancy as input.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRoomMaxOccupancyResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: SetRoomMaxOccupancyRequest')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Change maximum occupancy to 4.
            max_occupancy = 4

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_max_occupancy_request(max_occupancy)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - setRoomMaxOccupancyResponse : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room = room_data['response']['roomResponse']['setRoomMaxOccupancyResponse']
            status = SyncHelper.validate_setMaxOccupancyResponse(room, max_occupancy)

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_43038_roomInformationChangedEvent(self):
        """Message: RoomInformationChangedEvent
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Set maximum occupancy of the room to 4.
                 2. Create a thread that listens to roomInformationChangedEvent.
                 3. Change the maximum occupancy from 4 to 6.
                 4. Validate the roomInformationChangedEvent response.
        """
        try:
            self.banner('Message: RoomInformationChangedEvent')

            # Step1: Set the max occupancy of room to 4.
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))
            self.websocket_dict['event_list'] = ['roomInformationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})

            # Set maximum occupancy to 4.
            max_occupancy = 4

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_max_occupancy_request(max_occupancy)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Create a thread that listens to roomInformationChangedEvent.
            _thread_get_room_information_changed_event = Thread(
                name='logisync_room_information_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_room_information_changed_event.start()
            time.sleep(2)

            # Step3: Change the room information by updating max occupancy from 4 to 6.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}

            max_occupancy_updated = 6

            # Generate the request message
            self.websocket_dict_changed_config['msg_buffer'] = room_request.create_set_max_occupancy_request\
                (max_occupancy_updated)

            # Send the generated request via websocket to proxy server.
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)

            # Get the response
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())
            time.sleep(2)

            _thread_get_room_information_changed_event.join()
            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            room_information_changed_event = self.websocket_dict["event_response"]['event']['roomEvent'][
                'roomInformationChangedEvent']
            status = SyncHelper.validate_roomInformationChangedEvent(room_information_changed_event)
            time.sleep(5)

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_005_VC_43039_setRoomOccupancyModeRequest(self):
        """Message: SetRoomOccupancyModeRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: SetRoomOccupancyModeRequest providing mode as input.
                    ROOM_OCCUPANCY_MODE_DISABLED -> 0 -> Room Occupancy feature disabled.
                    ROOM_OCCUPANCY_MODE_ALWAYS_ON -> 1 -> Room Occupancy counting enabled whether or not a meeting
                    is active.
                    ROOM_OCCUPANCY_MODE_MEETINGS_ONLY -> 2 -> Room Occupancy counting enabled only when a meeting
                    is active
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRoomOccupancyModeResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: SetRoomOccupancyModeRequest')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # ROOM_OCCUPANCY_MODE_DISABLED -> 0 -> Room Occupancy feature disabled.
            # ROOM_OCCUPANCY_MODE_ALWAYS_ON -> 1 -> Room Occupancy counting enabled whether or not a meeting is active.
            # ROOM_OCCUPANCY_MODE_MEETINGS_ONLY -> 2 -> Room Occupancy counting enabled only when a
            # meeting is active

            # Disable room occupancy
            mode = 0

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_room_occupancy_mode_request(mode)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(
                websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - setRoomMaxOccupancyResponse - Disable room occupancy feature : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room = room_data['response']['roomResponse']['setRoomOccupancyModeResponse']
            status_disable = SyncHelper.validate_setRoomOccupancyModeResponse(room, mode)

            # Enable room occupancy: ROOM_OCCUPANCY_MODE_ALWAYS_ON
            mode = 1

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_room_occupancy_mode_request(mode)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - setRoomMaxOccupancyResponse - Enable room occupancy feature: Always On : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room = room_data['response']['roomResponse']['setRoomOccupancyModeResponse']
            status_always_on = SyncHelper.validate_setRoomOccupancyModeResponse(room, mode)

            # Enable room occupancy: ROOM_OCCUPANCY_MODE_MEETINGS_ONLY
            mode = 2

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_set_room_occupancy_mode_request(mode)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - setRoomMaxOccupancyResponse- Enable room occupancy feature- Meetings Only : {}'.
                      format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room = room_data['response']['roomResponse']['setRoomOccupancyModeResponse']
            status_meetings_only = SyncHelper.validate_setRoomOccupancyModeResponse(room, mode)

            status = status_disable & status_always_on & status_meetings_only

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_006_VC_43040_bulkSetRoomInformationRequest(self):
        """Message: BulkSetRoomInformationRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: BulkSetRoomInformationRequest providing room_information map
                    as input.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the BulkSetRoomInformationResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: BulkSetRoomInformationRequest')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Provide the room_information with room name as Test-Room-Name-Updated, max occupancy as 10 and
            # occupancy mode as Meetings only.
            room_inf = {0: "Test-Room-Name-Updated", 1: "10", 2: "2"}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_bulk_set_room_information_request(room_inf)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - BulkSetRoomInformationResponse : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room_data = room_data['response']['roomResponse']['bulkSetRoomInformationResponse']
            status = SyncHelper.validate_bulkSetRoomInformationRequest(room_data, room_inf)
            assert status is True, 'Error'

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_007_VC_43041_bulkSetRoomInformationRequest_empty_room_info(self):
        """Message: BulkSetRoomInformationRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: BulkSetRoomInformationRequest providing empty room_information map
                    as input.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the BulkSetRoomInformationResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: BulkSetRoomInformationRequest: Empty room_information map')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Provide the room_information with room name as Test-Room-Name-Updated, max occupancy as 10 and
            # occupancy mode as Meetings only.
            room_inf = {}

            room_information = self.get_init_room_info()
            room_info_base = room_information['roomInformation']

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_bulk_set_room_information_request(room_inf)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - BulkSetRoomInformationResponse : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room_data = room_data['response']['roomResponse']['bulkSetRoomInformationResponse']
            status = SyncHelper.validate_bulkSetRoomInformationRequest(room_data, room_inf, room_info_base)
            assert status is True, 'Error'

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_008_VC_43042_bulkSetRoomInformationRequest_partial_room_info(self):
        """Message: BulkSetRoomInformationRequest
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
            Test:
                 1. Create a protobuf API request: BulkSetRoomInformationRequest providing partial room_information map
                    as input.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the BulkSetRoomInformationResponse.
                 4. Validate the response.
        """
        try:
            self.banner('Message: BulkSetRoomInformationRequest: Partial room_information map')

            # Create request object
            room_request = RoomRequest()
            log.debug('Room request {}'.format(room_request))

            # Provide the room_information with room name as Test-Name-Updated, max occupancy as 12
            room_inf = {0: "Test-Name-Updated", 1: "12"}

            room_information = self.get_init_room_info()
            room_info_base = room_information['roomInformation']

            # Generate the request message
            self.websocket_dict['msg_buffer'] = room_request.create_bulk_set_room_information_request(room_inf)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            room_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_room_data = json.dumps(room_data, indent=2)
            log.debug('Room - BulkSetRoomInformationResponse - Partial roomInformation : {}'.
                      format(json_formatted_room_data))
            Report.logResponse(format(json_formatted_room_data))
            time.sleep(5)

            # Validate the response
            room_data = room_data['response']['roomResponse']['bulkSetRoomInformationResponse']
            status = SyncHelper.validate_bulkSetRoomInformationRequest(room_data, room_inf, room_info_base)
            assert status is True, 'Error'

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncRoomAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")