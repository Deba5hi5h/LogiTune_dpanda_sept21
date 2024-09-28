import asyncio
import json
import sys
import unittest
import logging

from common.config import DeviceModelConfig
from apis.sync_api.firmwarerequest import FirmwareRequest
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
import common.log_helper as log_helper
from common import framework_params as fp
from apis.sync_api.websocketconnection import WebsocketConnection
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncFirmwareAPI(SyncBaseAPI):
    """
     Tests to verify product API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncFirmwareAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(LogiSyncFirmwareAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncFirmwareAPI, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncFirmwareAPI, self).tearDown() #Extent Report

    def test_001_VC_43716_RallySystem_getLatestFirmwareByProductIdRequest(self):
        """Requests that the Sync service retrieve the latest available firmware for a specific product.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: GetLatestFirmwareByProductIdRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Get all products and validate the response.

        """
        try:
            self.banner('GetLatestFirmwareByProductIdRequest')
            # Create configuration request object
            product_request = FirmwareRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            product_uuid = self.product_uuid['RALLY']
            product_model_id = DeviceModelConfig.model_rally
            self.websocket_dict['msg_buffer'] = product_request.create_get_latest_firmware(product_uuid)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_firmware_data = json.dumps(product_data, indent=2)
            log.debug('Firmware API - GetLatestFirmwareByProductIdRequest : {}'.
                      format(json_formatted_firmware_data))
            Report.logResponse(format(json_formatted_firmware_data))

            # Validate the response
            fw_response = product_data['response']['firmwareResponse']['getLatestFirmwareByProductIdResponse']
            status = SyncHelper.validate_get_latest_firmware(firmware_response=fw_response,
                                                             device_type=product_model_id,
                                                             product_uuid=product_uuid)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')



if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")