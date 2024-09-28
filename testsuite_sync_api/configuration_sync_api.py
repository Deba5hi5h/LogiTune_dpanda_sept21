import asyncio
import json
import logging
import sys
import unittest

from apis import process_helper
import common.log_helper as log_helper
from apis.sync_api.configurationrequest import ConfigurationRequest
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
from apis.sync_api.websocketconnection import WebsocketConnection
from threading import Thread
from apis.sync_api.sync_eventhandler import EventHandler
import time
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncConfigurationAPI(SyncBaseAPI):
    """
        Tests to verify configuration API
    """
    base_config = ""

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncConfigurationAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')
            cls.base_config = cls._get_sync_config()

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.base_config != "":
                cls._restore_sync_config(cls.base_config)
            super(LogiSyncConfigurationAPI, cls).tearDownClass()
        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    def setUp(self):
        super(LogiSyncConfigurationAPI, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncConfigurationAPI, self).tearDown() #Extent Report

    def test_001_VC_43020_getLogiSyncConfigurationRequest(self):
        """Get current configuration that has been set by the Sync

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: GetLogiSyncConfigurationRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Get configuration parameters and validate the response.

        """
        try:

            # Create configuration request object
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_logi_sync_configuration_request()
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            configuration_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_configuration_data = json.dumps(configuration_data, indent=2)
            log.debug('getLogiSyncConfigurationRequest : {}'.
                      format(json_formatted_configuration_data))
            Report.logResponse(format(json_formatted_configuration_data))

            # Validate the response
            products = configuration_data['response']['configurationResponse']['getLogiSyncConfigurationResponse']['configuration']['configuration']
            status = SyncHelper.validate_get_configuration_response(products)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43022_setLogiSyncConfigurationRequest_fullConfig(self):
        """Sets the configuration on the Sync service.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetLogiSyncConfigurationRequest with full configuration
                 2. Send this to the proxy server via a websocket connection.
                 3. Get configuration parameters and validate the response.

        """
        try:

            # Create configuration request object
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))
            configuration_base = {1: "true", 2: "TestName", 3: "false", 4: "TestOrgName"}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                configuration_base)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            configuration_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_configuration_data = json.dumps(configuration_data, indent=2)
            log.debug('setLogiSyncConfigurationRequest : {}'.
                      format(json_formatted_configuration_data))
            Report.logResponse(format(json_formatted_configuration_data))

            # Validate the response
            configuration_data = configuration_data['response']['configurationResponse']['setLogiSyncConfigurationResponse']['configuration']
            status = SyncHelper.validate_set_configuration_response(configuration_base, configuration_data['configuration'])
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43023_logiSyncConfigurationChangedEvent(self):
        """Message: LogiSyncConfigurationChangedEvent

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running

            Test:
                 1. Set a Logi sync configuration.
                 2. Create a thread that listens to LogiSyncConfigurationChangedEvent
                 3. Change the logisync configuration and capture the LogiSyncConfigurationChangedEvent.

        """
        try:

            # Step1: Set a Logisync configuration.
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))
            self.websocket_dict['event_list'] = ['logiSyncConfigurationChangedEvent']
            self.websocket_dict.update({'type': 'LogiSync', 'timeout': 60.0})

            configuration_base = {1: "true", 2: "TestName", 3: "false", 4: "TestOrgName"}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                configuration_base)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            self.loop.run_until_complete(websocket_conn.request_response_listener())

            # Step2: Create a thread that listens to LogiSyncConfigurationChangedEvent.
            _thread_get_logisync_configuration_changed_event = Thread(
                name='logisync_configuration_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn, self.loop,
                                                                 self.websocket_dict))
            _thread_get_logisync_configuration_changed_event.start()
            time.sleep(2)

            # Step3: Change the logisync configuration and capture the LogiSyncConfigurationChangedEvent.
            self.loop_changed_config = asyncio.new_event_loop()
            self.websocket_dict_changed_config = {'type': 'LogiSync', 'timeout': 30.0}

            configuration_base_updated = {1: "true", 2: "TestName-updated", 3: "false", 4: "TestOrgName"}

            # Generate the request message
            self.websocket_dict_changed_config['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                configuration_base_updated)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict_changed_config))

            # Send request to proxy server via a web socket connection
            websocket_conn_changed_config = WebsocketConnection(self.websocket_dict_changed_config)

            # Get the response
            self.loop_changed_config.run_until_complete(websocket_conn_changed_config.request_response_listener())
            time.sleep(2)

            _thread_get_logisync_configuration_changed_event.join()
            log.info(f'Event Response - {self.websocket_dict["event_response"]}')
            Report.logResponse(self.websocket_dict["event_response"])
            logisync_configuration_changed_event = self.websocket_dict["event_response"]['event']['configurationEvent'][
                'logiSyncConfigurationChangedEvent']
            status = SyncHelper.logisync_configuration_changed_event(logisync_configuration_changed_event,
                                                                     configuration_base_updated)

            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_43026_setLogiSyncConfigurationRequest_emptyConfig(self):
        """Sets the configuration on the Sync service.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetLogiSyncConfigurationRequest with empty configuration
                 2. Send this to the proxy server via a websocket connection.
                 3. Get configuration parameters and validate the response.

        """
        try:

            # Create configuration request object
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))
            configuration_base = {}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                configuration_base)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            configuration_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_configuration_data = json.dumps(configuration_data, indent=2)
            log.debug('setLogiSyncConfigurationRequest : {}'.
                      format(json_formatted_configuration_data))
            Report.logResponse(format(json_formatted_configuration_data))

            # Validate the response
            configuration_data = configuration_data['response']['configurationResponse']['setLogiSyncConfigurationResponse']['configuration']
            status = SyncHelper.validate_set_configuration_response(configuration_base, configuration_data)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_005_VC_43029_setLogiSyncConfigurationRequest_partialConfig(self):
        """Sets the configuration on the Sync service.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetLogiSyncConfigurationRequest with partial configuration
                 2. Send this to the proxy server via a websocket connection.
                 3. Get configuration parameters and validate the response.

        """
        try:

            # Create configuration request object
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))
            configuration_base = {3: "true"}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                configuration_base)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            configuration_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_configuration_data = json.dumps(configuration_data, indent=2)
            log.debug('setLogiSyncConfigurationRequest : {}'.
                      format(json_formatted_configuration_data))
            Report.logResponse(format(json_formatted_configuration_data))

            # Validate the response
            configuration_data = configuration_data['response']['configurationResponse']['setLogiSyncConfigurationResponse']['configuration']
            status = SyncHelper.validate_set_configuration_response(configuration_base, configuration_data['configuration'])
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_100_VC_43030_getHostInformationRequest(self):
        """Get information about the host machine running the Sync service.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: GetHostInformationRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Get configuration parameters and validate the response.

        """
        try:

            # Create configuration request object
            configuration_request = ConfigurationRequest()
            log.debug('Host Information request {}'.format(configuration_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = configuration_request.create_host_information_request()
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            configuration_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_configuration_data = json.dumps(configuration_data, indent=2)
            log.debug('getHostInformationRequest : {}'.
                      format(json_formatted_configuration_data))
            Report.logResponse(format(json_formatted_configuration_data))

            # Validate the response
            host_information = configuration_data['response']['configurationResponse']['getHostInformationResponse']['information']
            status = SyncHelper.validate_get_host_information_response(host_information)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    @classmethod
    def _get_sync_config(cls):
        try:
            log.debug('Get Sync Configuration for a setUpClass.')
            configuration_request = ConfigurationRequest()
            websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict['msg_buffer'] = configuration_request.create_logi_sync_configuration_request()
            websocket_con = WebsocketConnection(websocket_dict)

            config_data = cls.loop.run_until_complete(websocket_con.request_response_listener())

            return config_data['response']['configurationResponse']['getLogiSyncConfigurationResponse']['configuration'][
                'configuration']
        except AssertionError as e:
            log.error('Unable to setup sync config in setUpClass')
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    @classmethod
    def _restore_sync_config(cls, config):
        try:
            log.debug('Restore Sync Configuration with config got in setUpClass.')
            configuration_request = ConfigurationRequest()
            websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}
            websocket_dict['msg_buffer'] = configuration_request.create_set_logi_sync_configuration_request(
                config)
            websocket_con = WebsocketConnection(websocket_dict)
            configuration_data = cls.loop.run_until_complete(websocket_con.request_response_listener())
            configuration_data = \
            configuration_data['response']['configurationResponse']['setLogiSyncConfigurationResponse']['configuration']
            status = SyncHelper.validate_restore_configuration_response(config,
                                                                    configuration_data['configuration'])
            assert status is True, 'Error'
        except AssertionError as e:
            log.error('Unable to restore sync config in tearDownClass')
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncConfigurationAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
