import logging
import unittest
import sys
import asyncio
import json
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
from apis.sync_api.videosettingsrequest import VideosettingsRequest
from apis.sync_api.websocketconnection import WebsocketConnection
import common.log_helper as log_helper
from common import framework_params as fp
from threading import Thread
from apis.sync_api.sync_eventhandler import EventHandler
import time

from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncVideoSettingAPI(SyncBaseAPI):
    """
     Tests to verify product API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncVideoSettingAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()

            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError(' Sync Service not running')

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(LogiSyncVideoSettingAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncVideoSettingAPI, self).setUp()
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncVideoSettingAPI, self).tearDown()

    def test_001_VC_43708_MeetUp_SetRightSightConfigurationRequest_on_call_start(self):
        """SetRightSightConfigurationRequest - MeetUp - Change the mode to On Call Start. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for MeetUp with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - MeetUp - Change the mode to On Call Start. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['MEETUP'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43709_MeetUp_SetRightSightConfigurationRequest_off(self):
        """SetRightSightConfigurationRequest - MeetUp - Turn off RightSight. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for MeetUp with
                 enabled as false.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - MeetUp - Turn off RightSight. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['MEETUP'], enabled=False)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43710_MeetUp_SetRightSightConfigurationRequest_dynamic(self):
        """SetRightSightConfigurationRequest - MeetUp - Change the mode to Dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for MeetUp with
                 enabled as true and mode as dynamic.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - MeetUp - Change the mode to Dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'DYNAMIC'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['MEETUP'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_43711_MeetUp_RightSightConfigurationChangedEvent_on_call_start_to_dynamic(self):
        """RightSightConfigurationChangedEvent - Change the mode from on call start to dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for MeetUp with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection. It returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration
                 5. Start the event listener.
                 6. Create a protobuf API request: SetRightSightConfigurationRequest for MeetUp with
                 enabled as true and mode as 'DYNAMIC'
                 7. Validate that the RightSightConfigurationChangedEvent is captured.

                """
        try:
            self.banner('RightSightConfigurationChangedEvent - Change the mode from on call start to dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Step1: Set the right sight configuration to on call start.
            # Create videosettings request object
            videosettings_req = VideosettingsRequest()
            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['MEETUP'], enabled=True, mode=MODE)
            # Set the event type as LogiSync to fetch rightSightConfigurationChangedEvent.
            self.websocket_dict['event_list'] = ['rightSightConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})
            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Start the event listener. Create thread to grab rightSightConfigurationChangedEvent event before
            # changing the mode from on-call-start to dynamic.
            _thread_get_right_sight_event = Thread(
                name='logisync_right_sight_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_right_sight_event.start()
            time.sleep(2)

            # Step3: Change the rightsight configuration to dynamic.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}
            MODE2 = 'DYNAMIC'
            self.websocket_dict_changed_config['msg_buffer']= videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['MEETUP'], enabled=True, mode=MODE2)
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)
            # Send the generated request via websocket to proxy server.
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())

            # Step4: Validate that the event response contains rightSightConfigurationChangedEvent.
            _thread_get_right_sight_event.join()
            time.sleep(2)
            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            right_sight_event = self.websocket_dict["event_response"]['event']['videoSettingsEvent']['rightSightConfigurationChangedEvent']
            status = SyncHelper.validate_rightSightConfigurationChangedEvent(right_sight_event)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_201_VC_44080_RallyBar_SetRightSightConfigurationRequest_on_call_start(self):
        """SetRightSightConfigurationRequest - Rally Bar - Change the mode to On Call Start. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - Rally Bar - Change the mode to On Call Start. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['RALLY_BAR'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_202_VC_44081_RallyBar_SetRightSightConfigurationRequest_off(self):
        """SetRightSightConfigurationRequest - Rally Bar - Turn off RightSight. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar with
                 enabled as false.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - MeetUp - Turn off RightSight. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['RALLY_BAR'], enabled=False)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_203_VC_44082_RallyBar_SetRightSightConfigurationRequest_dynamic(self):
        """SetRightSightConfigurationRequest - Rally Bar - Change the mode to Dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar with
                 enabled as true and mode as dynamic.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - Rally Bar - Change the mode to Dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'DYNAMIC'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request\
                (self.product_uuid['RALLY_BAR'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_204_VC_44083_RallyBar_RightSightConfigurationChangedEvent_on_call_start_to_dynamic(self):
        """RightSightConfigurationChangedEvent - Change the mode from on call start to dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection. It returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration
                 5. Start the event listener.
                 6. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar with
                 enabled as true and mode as 'DYNAMIC'
                 7. Validate that the RightSightConfigurationChangedEvent is captured.

                """
        try:
            self.banner('RightSightConfigurationChangedEvent - Change the mode from on call start to dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Step1: Set the right sight configuration to on call start.
            # Create videosettings request object
            videosettings_req = VideosettingsRequest()
            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR'], enabled=True, mode=MODE)
            # Set the event type as LogiSync to fetch rightSightConfigurationChangedEvent.
            self.websocket_dict['event_list'] = ['rightSightConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})
            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Start the event listener. Create thread to grab rightSightConfigurationChangedEvent event before
            # changing the mode from on-call-start to dynamic.
            _thread_get_right_sight_event = Thread(
                name='logisync_right_sight_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_right_sight_event.start()
            time.sleep(2)

            # Step3: Change the rightsight configuration to dynamic.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}
            MODE2 = 'DYNAMIC'
            self.websocket_dict_changed_config['msg_buffer']= videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR'], enabled=True, mode=MODE2)
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)
            # Send the generated request via websocket to proxy server.
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())

            # Step4: Validate that the event response contains rightSightConfigurationChangedEvent.
            _thread_get_right_sight_event.join()
            time.sleep(2)
            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            right_sight_event = self.websocket_dict["event_response"]['event']['videoSettingsEvent']['rightSightConfigurationChangedEvent']
            status = SyncHelper.validate_rightSightConfigurationChangedEvent(right_sight_event)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_301_VC_44084_RallyBarMini_SetRightSightConfigurationRequest_on_call_start(self):
        """SetRightSightConfigurationRequest - Rally Bar Mini- Change the mode to On Call Start. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar Mini with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - Rally Bar Mini- Change the mode to On Call Start. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_302_VC_44085_RallyBarMini_SetRightSightConfigurationRequest_off(self):
        """SetRightSightConfigurationRequest - Rally Bar Mini- Turn off RightSight. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar Mini with
                 enabled as false.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - Rally Bar Mini - Turn off RightSight. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], enabled=False)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_303_VC_44086_RallyBarMini_SetRightSightConfigurationRequest_dynamic(self):
        """SetRightSightConfigurationRequest - Rally Bar Mini - Change the mode to Dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar Mini with
                 enabled as true and mode as dynamic.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetRightSightConfigurationRequest - Rally Bar Mini - Change the mode to Dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'DYNAMIC'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], enabled=True, mode=MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setRightSightConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setRightSightConfigurationResponse']
            status = SyncHelper.validate_setRightSightConfigurationResponse(product, MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_304_VC_44088_RallyBarMini_RightSightConfigurationChangedEvent_on_call_start_to_dynamic(self):
        """RightSightConfigurationChangedEvent - Change the mode from on call start to dynamic. Data Structure: RightSightConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini to the host PC.

            Test:
                 1. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar Mini with
                 enabled as true and mode as 'ON_CALL_START'
                 2. Send this to the proxy server via a websocket connection. It returns the SetRightSightConfigurationResponse.
                 4. Validate the response: video_settings_configuration
                 5. Start the event listener.
                 6. Create a protobuf API request: SetRightSightConfigurationRequest for Rally Bar Mini with
                 enabled as true and mode as 'DYNAMIC'
                 7. Validate that the RightSightConfigurationChangedEvent is captured.

                """
        try:
            self.banner('RightSightConfigurationChangedEvent - Rally Bar Mini- Change the mode from on call start to dynamic. '
                        'Data Structure: RightSightConfiguration.')

            # Step1: Set the right sight configuration to on call start.
            # Create videosettings request object
            videosettings_req = VideosettingsRequest()
            log.debug('Video Settings request {}'.format(videosettings_req))
            MODE = 'ON_CALL_START'
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], enabled=True, mode=MODE)
            # Set the event type as LogiSync to fetch rightSightConfigurationChangedEvent.
            self.websocket_dict['event_list'] = ['rightSightConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})
            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Start the event listener. Create thread to grab rightSightConfigurationChangedEvent event before
            # changing the mode from on-call-start to dynamic.
            _thread_get_right_sight_event = Thread(
                name='logisync_right_sight_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_right_sight_event.start()
            time.sleep(2)

            # Step3: Change the rightsight configuration to dynamic.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}
            MODE2 = 'DYNAMIC'
            self.websocket_dict_changed_config[
                'msg_buffer'] = videosettings_req.create_set_right_sight_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], enabled=True, mode=MODE2)
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)
            # Send the generated request via websocket to proxy server.
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())

            # Step4: Validate that the event response contains rightSightConfigurationChangedEvent.
            _thread_get_right_sight_event.join()
            time.sleep(2)
            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            right_sight_event = self.websocket_dict["event_response"]['event']['videoSettingsEvent'][
                'rightSightConfigurationChangedEvent']
            status = SyncHelper.validate_rightSightConfigurationChangedEvent(right_sight_event)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_101_VC_43712_RallyBar_setAntiFlickerConfigurationRequest_to_NTSC(self):
        """SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration Request for Rally Bar with anti flicker mode as NTSC 60 Hz. Data Structure: VideoSettingsConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'NTSC'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetAntiFlickerConfigurationRequest : Set Anti Flicker Configuration to NTSC 60 Hz.'
                        'Data Structure: VideoSettingsConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            ANTI_FLICKER_MODE = 'NTSC'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setAntiFlickerConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setAntiFlickerConfigurationResponse']
            status = SyncHelper.validate_setAntiFlickerConfigurationResponse(product, ANTI_FLICKER_MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_102_VC_43713_RallyBar_setAntiFlickerConfigurationRequest_to_PAL(self):
        """SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration Request for Rally Bar with anti flicker mode as PAL 50 Hz. Data Structure: VideoSettingsConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'PAL'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Validate the response: video_settings_configuration

        """
        try:
            self.banner('SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration to PAL 50 Hz.'
                        'Data Structure: VideoSettingsConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))

            ANTI_FLICKER_MODE = 'PAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request\
                (self.product_uuid['RALLY_BAR'], ANTI_FLICKER_MODE)

            # Send the generated request to the proxy server via websocket
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())

            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setAntiFlickerConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setAntiFlickerConfigurationResponse']
            status = SyncHelper.validate_setAntiFlickerConfigurationResponse(product, ANTI_FLICKER_MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_103_VC_43715_RallyBar_videoSettingsConfigurationChangedEvent_PAL_to_NTSC(self):
        """VideoSettingsConfigurationChangedEvent: PAL to NTSC.
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'PAL'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Add the event listener.
                 5. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'NTSC'.Send it to proxy server via websocket connection
                 6. Validate that videoSettingsConfigurationChangedEvent appears.

        """
        try:
            self.banner('VideoSettingsConfigurationChangedEvent: PAL to NTSC.')
            # Step1: Set the anti flocker mode to PAL
            # Create videosettings request object
            videosettings_req = VideosettingsRequest()
            # Set the event type as LogiSync to fetch rightSightConfigurationChangedEvent.
            self.websocket_dict['event_list'] = ['videoSettingsConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})
            log.debug('Video Settings request {}'.format(videosettings_req))
            ANTI_FLICKER_MODE = 'PAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Start the event listener. Create thread to grab VideoSettingsConfigurationChangedEvent event before
            # changing the mode from PAL(50 HZ) to NTSC(60 Hz).
            _thread_get_video_settings_event = Thread(
                name='logisync_video_settings_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_video_settings_event.start()
            time.sleep(2)

            # Step3: Change the video settings configuration from PAL to NTSC.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}
            ANTI_FLICKER_MODE = 'NTSC'
            # Generate the request message
            self.websocket_dict_changed_config['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)

            # Get the response
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())

            time.sleep(2)
            # Step4: Validate that the event response contains rightSightConfigurationChangedEvent.
            _thread_get_video_settings_event.join()

            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            video_settings_event = self.websocket_dict["event_response"]['event']['videoSettingsEvent'][
                'videoSettingsConfigurationChangedEvent']
            status = SyncHelper.validate_videoSettingsConfigurationChangedEvent(video_settings_event)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_104_VC_44089_RallyBarMini_setAntiFlickerConfigurationRequest_to_NTSC(self):
        """SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration Request for Rally Bar Mini with anti flicker mode as NTSC 60 Hz. Data Structure: VideoSettingsConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar Mini with
                 anti-flicker mode as 'NTSC'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Validate the response: setAntiFlickerConfigurationResponse

        """
        try:
            self.banner('SetAntiFlickerConfigurationRequest : Set Anti Flicker Configuration to NTSC 60 Hz.'
                        'Data Structure: VideoSettingsConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))
            ANTI_FLICKER_MODE = 'NTSC'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setAntiFlickerConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setAntiFlickerConfigurationResponse']
            status = SyncHelper.validate_setAntiFlickerConfigurationResponse(product, ANTI_FLICKER_MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_105_VC_44090_RallyBarMini_setAntiFlickerConfigurationRequest_to_PAL(self):
        """SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration Request for Rally Bar with anti flicker mode as PAL 50 Hz. Data Structure: VideoSettingsConfiguration.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar Mini in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar Mini with
                 anti-flicker mode as 'PAL'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Validate the response: setAntiFlickerConfigurationResponse

        """
        try:
            self.banner('SetAntiFlickerConfigurationRequest: Set Anti Flicker Configuration to PAL 50 Hz.'
                        'Data Structure: VideoSettingsConfiguration.')

            # Create videosettings request object
            videosettings_req = VideosettingsRequest()

            log.debug('Video Settings request {}'.format(videosettings_req))

            ANTI_FLICKER_MODE = 'PAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request\
                (self.product_uuid['RALLY_BAR_MINI'], ANTI_FLICKER_MODE)

            # Send the generated request to the proxy server via websocket
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            video_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())

            json_formatted_video_settings_data = json.dumps(video_settings_data, indent=2)
            log.debug('Video Settings - setAntiFlickerConfigurationResponse : {}'.
                      format(json_formatted_video_settings_data))
            Report.logResponse(format(json_formatted_video_settings_data))

            # Validate the response
            product = video_settings_data['response']['videoSettingsResponse']['setAntiFlickerConfigurationResponse']
            status = SyncHelper.validate_setAntiFlickerConfigurationResponse(product, ANTI_FLICKER_MODE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_106_VC_44091_RallyBarMini_videoSettingsConfigurationChangedEvent_PAL_to_NTSC(self):
        """VideoSettingsConfigurationChangedEvent: PAL to NTSC.
            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally Bar in device mode to the host PC.

            Test:
                 1. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'PAL'.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetAntiFlickerConfigurationResponse.
                 4. Add the event listener.
                 5. Create a protobuf API request: SetAntiFlickerConfigurationRequest for Rally Bar with
                 anti-flicker mode as 'NTSC'.Send it to proxy server via websocket connection
                 6. Validate that videoSettingsConfigurationChangedEvent appears.

        """
        try:
            self.banner('VideoSettingsConfigurationChangedEvent: PAL to NTSC.')
            # Step1: Set the anti flocker mode to PAL
            # Create videosettings request object
            videosettings_req = VideosettingsRequest()
            # Set the event type as LogiSync to fetch rightSightConfigurationChangedEvent.
            self.websocket_dict['event_list'] = ['videoSettingsConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})
            log.debug('Video Settings request {}'.format(videosettings_req))
            ANTI_FLICKER_MODE = 'PAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Start the event listener. Create thread to grab VideoSettingsConfigurationChangedEvent event before
            # changing the mode from PAL(50 HZ) to NTSC(60 Hz).
            _thread_get_video_settings_event = Thread(
                name='logisync_video_settings_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_video_settings_event.start()
            time.sleep(2)

            # Step3: Change the video settings configuration from PAL to NTSC.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}
            ANTI_FLICKER_MODE = 'NTSC'
            # Generate the request message
            self.websocket_dict_changed_config['msg_buffer'] = videosettings_req.create_set_anti_flicker_configuration_request \
                (self.product_uuid['RALLY_BAR_MINI'], ANTI_FLICKER_MODE)

            # Send the generated request via websocket to proxy server.
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)

            # Get the response
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())

            time.sleep(2)
            # Step4: Validate that the event response contains rightSightConfigurationChangedEvent.
            _thread_get_video_settings_event.join()

            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            video_settings_event = self.websocket_dict["event_response"]['event']['videoSettingsEvent'][
                'videoSettingsConfigurationChangedEvent']
            status = SyncHelper.validate_videoSettingsConfigurationChangedEvent(video_settings_event)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncVideoSettingAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
