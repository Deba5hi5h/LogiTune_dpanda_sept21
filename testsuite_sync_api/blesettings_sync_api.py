import asyncio
import json
import logging
import sys
import unittest
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
from apis.sync_api.blesettings_request import BLESettingsRequest
from apis.sync_api.websocketconnection import WebsocketConnection
import common.log_helper as log_helper
from common import framework_params as fp
from extentreport.report import Report
import time

log = logging.getLogger(__name__)


class LogiSyncBLESettingsAPI(SyncBaseAPI):
    """
    Tests to verify the bluetooth settings protobuf API.
    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncBLESettingsAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()

            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError(' Sync Service not running')

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()
        super(LogiSyncBLESettingsAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncBLESettingsAPI, self).setUp() #Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncBLESettingsAPI, self).tearDown() #Extent Report

    def test_001_VC_43018_RallyBar_setBleConfigurationRequest_off(self, BLE_MODE='BLE_OFF'):
        """Change the BLE mode to off for the device connected to the host.
            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Rally Bar is connected to the system.

            Test:
                 1. Create a protobuf API request: BleSettingsRequest and create a thread to listen to BleConfigurationChangedEvent.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Rally Bar and validate the contents.

        """
        try:
            self.banner('Set BLE configuration for Rally Bar to OFF.')

            # Create a ble settings request object.
            blesettings_req = BLESettingsRequest()

            # Generate the request message.
            log.debug('BLE settings request {}'.format(blesettings_req))

            self.websocket_dict['msg_buffer'] = blesettings_req.create_set_ble_configuration_proto_request\
                (self.product_uuid['RALLY_BAR'], ble_mode=BLE_MODE)

            # Send the request to the proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response.
            ble_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())

            json_formatted_ble_settings_data = json.dumps(ble_settings_data, indent=2)
            log.debug('BLE Settings - setBleConfigurationResponse : {}'.
                      format(json_formatted_ble_settings_data))
            Report.logResponse(format(json_formatted_ble_settings_data))

            # Validate the response.
            response_data = ble_settings_data['response']['bleSettingsResponse']['setBleConfigurationResponse']

            if 'errors' not in response_data:
                status = SyncHelper.validate_setBleSettingsResponse(response_data, ble_mode=BLE_MODE)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the bluetooth setting.')
                status = SyncHelper.validate_error_bluetooth_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43019_RallyBar_setBleConfigurationRequest_on(self, BLE_MODE='BLE_ON'):
        """Change the BLE mode to on for the device connected to the host.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Rally Bar is connected to the system.

            Test:
                 1. Create a protobuf API request: BleSettingsRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Rally Bar and validate the contents.

        """
        try:
            self.banner('Set BLE configuration for Rally Bar to ON.')

            # Create a ble settings request object.
            blesettings_req = BLESettingsRequest()

            log.debug('BLE settings request {}'.format(blesettings_req))

            # Generate the request message.
            self.websocket_dict['msg_buffer'] = blesettings_req.create_set_ble_configuration_proto_request\
                (self.product_uuid['RALLY_BAR'], ble_mode=BLE_MODE )

            # Send the request to the proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            time.sleep(5)

            # Get the response.
            ble_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_ble_settings_data = json.dumps(ble_settings_data, indent=2)
            log.debug('BLE Settings - setBleConfigurationResponse : {}'.
                      format(json_formatted_ble_settings_data))
            Report.logResponse(format(json_formatted_ble_settings_data))

            # Validate the response.
            response_data = ble_settings_data['response']['bleSettingsResponse']['setBleConfigurationResponse']

            if 'errors' not in response_data:
                status = SyncHelper.validate_setBleSettingsResponse(response_data, ble_mode=BLE_MODE)
            else:
                log.info(
                    'Request got timed out. Sync Agent will re-send another request and update the bluetooth setting.')
                status = SyncHelper.validate_error_bluetooth_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_44075_RallyBarMini_setBleConfigurationRequest_off(self, BLE_MODE='BLE_OFF'):
        """Change the BLE mode to off for the device connected to the host.
            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Rally Bar Mini is connected to the system.

            Test:
                 1. Create a protobuf API request: BleSettingsRequest and create a thread to listen to BleConfigurationChangedEvent.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Rally Bar and validate the contents.

        """
        try:
            self.banner('Set BLE configuration for Rally Bar Mini to OFF.')

            # Create a ble settings request object.
            blesettings_req = BLESettingsRequest()

            # Generate the request message.
            log.debug('BLE settings request {}'.format(blesettings_req))

            self.websocket_dict['msg_buffer'] = blesettings_req.create_set_ble_configuration_proto_request\
                (self.product_uuid['RALLY_BAR_MINI'], ble_mode=BLE_MODE)

            # Send the request to the proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response.
            ble_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())

            json_formatted_ble_settings_data = json.dumps(ble_settings_data, indent=2)
            log.debug('BLE Settings - setBleConfigurationResponse : {}'.
                      format(json_formatted_ble_settings_data))
            Report.logResponse(format(json_formatted_ble_settings_data))

            # Validate the response.
            response_data = ble_settings_data['response']['bleSettingsResponse']['setBleConfigurationResponse']

            if 'errors' not in response_data:
                status = SyncHelper.validate_setBleSettingsResponse(response_data, ble_mode=BLE_MODE)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the bluetooth setting.')
                status = SyncHelper.validate_error_bluetooth_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_44077_RallyBarMini_setBleConfigurationRequest_on(self, BLE_MODE='BLE_ON'):
        """Change the BLE mode to on for the device connected to the host.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Rally Bar Mini is connected to the system.

            Test:
                 1. Create a protobuf API request: BleSettingsRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Rally Bar and validate the contents.

        """
        try:
            self.banner('Set BLE configuration for Rally Bar Mini to ON.')

            # Create a ble settings request object.
            blesettings_req = BLESettingsRequest()

            log.debug('BLE settings request {}'.format(blesettings_req))

            # Generate the request message.
            self.websocket_dict['msg_buffer'] = blesettings_req.create_set_ble_configuration_proto_request\
                (self.product_uuid['RALLY_BAR_MINI'], ble_mode=BLE_MODE)

            # Send the request to the proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            time.sleep(5)

            # Get the response.
            ble_settings_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_ble_settings_data = json.dumps(ble_settings_data, indent=2)
            log.debug('BLE Settings - setBleConfigurationResponse : {}'.
                      format(json_formatted_ble_settings_data))
            Report.logResponse(format(json_formatted_ble_settings_data))

            # Validate the response.
            response_data = ble_settings_data['response']['bleSettingsResponse']['setBleConfigurationResponse']

            if 'errors' not in response_data:
                status = SyncHelper.validate_setBleSettingsResponse(response_data, ble_mode=BLE_MODE)
            else:
                log.info(
                    'Request got timed out. Sync Agent will re-send another request and update the bluetooth setting.')
                status = SyncHelper.validate_error_bluetooth_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncBLESettingsAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")