import logging
import unittest
import sys
import asyncio
import json
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
from apis.sync_api.productrequest import ProductRequest
from apis.sync_api.websocketconnection import WebsocketConnection
import common.log_helper as log_helper
from common.config import DeviceModelConfig
from common import framework_params as fp
from random import randint
# from common.ipswitch_helper import IPSwitchHelper
from apis.sync_api.protobuf_helper import ProtobufUtils
from threading import Thread
from apis.sync_api.sync_eventhandler import EventHandler
from common.usb_switch import *
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncProductAPI(SyncBaseAPI):
    """
     Tests to verify product API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncProductAPI, cls).setUpClass()
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
        super(LogiSyncProductAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncProductAPI, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 30.0}

    def tearDown(self):
        super(LogiSyncProductAPI, self).tearDown() #Extent Report

    def test_001_VC_43409_getAllProductsRequest(self):
        """Get all products attached to host via sync.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. One or more monitored or managed devices have to be connected to system.

            Test:
                 1. Create a protobuf API request: GetAllProductsRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get all products and validate the response.

        """
        try:
            self.banner('Get all products attached to host via Sync App.')
            # Create configuration request object
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_product_request()
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Video Settings - getAllProductsRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            products = product_data['response']['productResponse']['getAllProductsResponse']
            status = SyncHelper.validate_get_all_products_response(products)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43412_MeetUp_getProductByIdRequest(self):
        """Get Product details of MeetUp that is attached to host via sync.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. MeetUp is connected to the system.

            Test:
                 1. Create a protobuf API request: GetProductByIdRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for MeetUp.

        """
        try:
            self.banner('Get product by ID attached to host via Sync App.')
            # Create configuration request object
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Device: MeetUp.
            DEVICE_TYPE = 'MEETUP'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_product_request(self.product_uuid['MEETUP'])
            print('Web socket dict - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Collect the parsed response.
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product Request - getProductByIdRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['getProductByIdResponse']['product']
            status = SyncHelper.validate_response_product_by_id(product, DEVICE_TYPE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43927_RallyCamera_getProductByIdRequest(self):
        """Get Product details of Rally Camera that is attached to host via sync.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Rally Camera is connected to the system.

            Test:
                 1. Create a protobuf API request: GetProductByIdRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Rally Camera.

        """
        try:
            self.banner('Get product by ID attached to host via Sync App.')
            # Create configuration request object
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Device: MeetUp.
            DEVICE_TYPE = 'RALLYCAMERA'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_product_request(self.product_uuid['RALLY_CAMERA'])
            print('Web socket dict - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Collect the parsed response.
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product Request - getProductByIdRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['getProductByIdResponse']['product']
            status = SyncHelper.validate_response_product_by_id(product, DEVICE_TYPE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_43961_Brio_getProductByIdRequest(self):
        """Get Product details of Brio that is attached to host via sync.

            Setup:
                  1. LogiSync Application should be running on the host.
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running.
                  3. Brio is connected to the system.

            Test:
                 1. Create a protobuf API request: GetProductByIdRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Get product response for Brio.

        """
        try:
            self.banner('Get product by ID attached to host via Sync App.')
            # Create configuration request object
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Device: MeetUp.
            DEVICE_TYPE = 'BRIO'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_product_request(self.product_uuid['BRIO'])
            print('Web socket dict - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection.
            websocket_con = WebsocketConnection(self.websocket_dict)

            # Collect the parsed response.
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product Request - getProductByIdRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['getProductByIdResponse']['product']
            status = SyncHelper.validate_response_product_by_id(product, DEVICE_TYPE)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_101_VC_43413_RallySystem_getProductConfigurationRequest(self):
        """GetProductConfigurationRequest for Rally System.

            Setup:
                  1. Install Sync Application on Host PC.
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect Rally System to the host PC.

            Test:
                 1. Create a protobuf API request: GetProductConfigurationRequest for Rally System providing the product uuid.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the GetProductConfigurationResponse.
                 4. Validate the response.

        """
        try:
            self.banner('Get Product Configuration request returns Get Product Configuration Response for Rally System.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_get_product_configuration_request\
                (self.product_uuid['RALLY'])

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - GetProductConfigurationResponse : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['getProductConfigurationResponse']
            status = SyncHelper.validate_getProductConfigurationResponse(product)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_102_VC_43414_RallySystem_setProductConfigurationRequest_fullConfig(self):
        """SetProductConfigurationRequest for Rally System.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect Rally System to the host PC.

            Test:
                 1. Create a protobuf API request: SetProductConfigurationRequest for Rally System providing the product uuid.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the SetProductConfigurationResponse.
                 4. Validate the response.

        """
        try:
            self.banner('Get Product Configuration request returns Get Product Configuration Response for Rally.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            configuration_base = {20: randint(0, 5),
                                  21: randint(0, 5),
                                  22: randint(0, 5),
                                  23: randint(0, 5),
                                  25: randint(0, 5)}

            # Generate the request message
            product_uuid = self.product_uuid['RALLY']
            self.websocket_dict['msg_buffer'] = product_request.create_set_product_configuration_request(product_uuid, configuration_base)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - SetProductConfigurationResponse : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['setProductConfigurationResponse']
            status = SyncHelper.validate_setProductConfigurationResponse(product, product_uuid, configuration_base)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_201_VC_43415_RallySystem_clearProductConfigurationRequest(self):
        """ClearProductConfigurationRequest for Rally System.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect Rally System to the host PC.

            Test:
                 1. Create a protobuf API request: ClearProductConfigurationRequest for Rally System providing the product uuid.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the ClearProductConfigurationResponse.
                 4. Validate the response.

        """
        try:
            self.banner('Clear Product Configuration request returns Clear Product Configuration Response for Rally.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            product_uuid = self.product_uuid['RALLY']
            self.websocket_dict['msg_buffer'] = product_request.create_clear_product_configuration_request(product_uuid)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - ClearProductConfigurationResponse : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['clearProductConfigurationResponse']
            status = SyncHelper.validate_clearProductConfigurationResponse(product, product_uuid)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_202_VC_43416_RallySystem_forgetDeviceRequest(self):
        """ForgetDeviceRequest for Rally System.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect Rally System to the host PC.

            Test:
                 1. Create a protobuf API request: ForgetDeviceRequest for Rally System providing the product uuid.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the ForgetDeviceResponse.
                 4. Validate the response.

        """
        try:
            self.banner('Forget Device request returns Forget Device Response for Rally.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            product_uuid = self.product_uuid['RALLY']
            self.websocket_dict['msg_buffer'] = product_request.create_forget_product_request(product_uuid, DeviceModelConfig.model_rally)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - ForgetDeviceRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['forgetDeviceResponse']
            status = SyncHelper.validate_forget_device_response(product, product_uuid)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_203_VC_43417_RallySystem_forgetDeviceRequest_rallyComponents(self):
        """ForgetDeviceRequest for Rally System.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Create a protobuf API request: ForgetDeviceRequest for Rally System providing the product uuid
                 and connected devices uuids.
                 2. Send this to the proxy server via a websocket connection.
                 3. Returns the ForgetDeviceResponse.
                 4. Validate the response.

        """
        try:
            self.banner('Forget Device request returns Forget Device Response for Rally.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            product_uuid = self.product_uuid['RALLY']
            product_model_id = DeviceModelConfig.model_rally
            self.websocket_dict['msg_buffer'] = product_request.create_product_request(product_uuid)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_response = self.loop.run_until_complete(websocket_conn.request_response_listener())
            device_uuids = []
            for sub_prod in product_response['response']['productResponse']['getProductByIdResponse']['product']['devices']:
                device_uuids.append(sub_prod['uuid'])

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_forget_product_request(product_uuid,
                                                                                              product_model_id,
                                                                                              device_uuids)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - ForgetDeviceRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product = product_data['response']['productResponse']['forgetDeviceResponse']
            status = SyncHelper.validate_forget_device_response(product, product_uuid, device_uuids)
            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_204_VC_43536_RallySystem_productStateChangedEvent(self):
        """Product State Changed Event for Rally.

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect Rally System to the host PC.

            Test:
                 1. Start a thread for Product State Changed Event.
                 2. Create a protobuf API request: ForgetDeviceRequest for Rally System providing the product uuid.
                 3. Validate the API: ForgetDeviceResponse and product state changed event response.

        """
        try:
            self.banner('Product State Changed Event')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Start thread for Product State Changed event
            loop_event = asyncio.new_event_loop()
            websocket_dict_event = {'type': 'LogiSync', 'timeout': 60.0}
            websocket_dict_event['event_list'] = ['productStateChangedEvent']
            # Send request to proxy server via a web socket connection
            websocket_conn_event = WebsocketConnection(websocket_dict_event)

            _thread_product_state_changed_event = Thread(
                name='logisync_product_state_changed_event_thread',
                target=EventHandler.event_listener_method, args=(websocket_conn_event, loop_event,
                                                                 websocket_dict_event))
            _thread_product_state_changed_event.start()
            time.sleep(2)

            # Generate the request message for forget_product_request
            product_uuid = self.product_uuid['RALLY']
            self.websocket_dict['msg_buffer'] = product_request.create_forget_product_request(product_uuid,
                                                                                              DeviceModelConfig.model_rally)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)
            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Get the response
            product_data = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_data, indent=2)
            log.debug('Product - ForgetDeviceRequest : {}'.
                      format(json_formatted_product_data))

            _thread_product_state_changed_event.join()
            # Validate the product response
            product = product_data['response']['productResponse']['forgetDeviceResponse']
            status_product_response = SyncHelper.validate_forget_device_response(product, product_uuid)

            # Validate the product event response
            product_event = websocket_dict_event["event_response"]['event']['productEvent']['productStateChangedEvent']
            Report.logResponse(product_event)
            status_product_event = SyncHelper.validate_product_state_changed_event(product_event)
            status = status_product_response & status_product_event

            assert status is True, 'Error'
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_205_VC_43538_sendProductRebootRequest(self):
        """Send Product Reboot Request to Rally Bar.

            Setup:
                  1. Install Sync Application on Host PC.
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect Rally to the host PC.

            Test:
                 1. Create a protobuf API request: SendProductRebootRequest for Rally Bar providing the product uuid.
                 3. Validate the response: sendProductRebootResponse.

        """
        try:
            self.banner('Send Product Reboot request to Rally Bar.')

            # Create Product Request
            product_request = ProductRequest()
            log.debug('Product request {}'.format(product_request))

            # Generate the request message
            product_uuid = self.product_uuid['RALLY_BAR']
            product_model_id = DeviceModelConfig.model_rally_bar
            self.websocket_dict['msg_buffer'] = product_request.create_product_reboot_request(product_uuid)

            # Send the generated request via websocket to proxy server.
            websocket_conn = WebsocketConnection(self.websocket_dict)

            # Get the response
            product_response = self.loop.run_until_complete(websocket_conn.request_response_listener())
            json_formatted_product_data = json.dumps(product_response, indent=2)
            log.debug('Product - ForgetDeviceRequest : {}'.
                      format(json_formatted_product_data))
            Report.logResponse(format(json_formatted_product_data))

            # Validate the response
            product_data = product_response['response']['productResponse']['sendProductRebootResponse']
            status = SyncHelper.validate_send_product_reboot_response(product_data, product_uuid)
            assert status is True, 'Error'
            time.sleep(10)
            log_helper.test_result_logger(self.id(), status)

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_301_VC_43540_MeetUp_productUnavailableEvent(self):
        '''ProductUnavailableEvent for MeetUp.

            Setup:
                  1. Install Sync Application on Host PC.
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running.
                  3. Connect MeetUp to the host PC via USB.

            Test:
                 1. Disconnect the MeetUp using the IPSwitch.
                 2. Validate that the event contains required fields for productUnavailableEvent.
        '''
        try:
            # _switch_util = IPSwitchHelper()
            # _device = 'meetup'
            # # Switching OFF the Camera using IP Switch.
            # _switch_util.switch_off(_device)
            device_name = 'MeetUp'

            # Add the productUnavailableEvent event to event_list.
            self.websocket_dict['event_list'] = ['productUnavailableEvent']

            # Switching OFF MeetUp using IP Switch.
            disconnect_device(device_name)

            websocket_conn = WebsocketConnection(self.websocket_dict)
            event_response = self.loop.run_until_complete(
                websocket_conn.event_listener()
            )

            # Parse the response
            products = event_response['event']['productEvent']['productUnavailableEvent']
            Report.logResponse(products)

            # Validate the response
            _status = ProtobufUtils.validate_disconnect_event(products)
            log_helper.test_result_logger(self.id(), _status)

        except Exception as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_302_VC_43541_MeetUp_ProductAvailableEvent(self):
        '''ProductAvailableEvent

            Setup:
                  1. Install Sync Application on Host PC
                  2. Make sure that the services: LogisyncMiddleware, LogisyncProxy, LogisyncHandler are running
                  3. Connect MeetUp to the host PC.

            Test:
                 1. Connect MeetUp using the IPSwitch.
                 2. Get and validate that the event contains required fields for productAvailableEvent.
        '''
        try:

            # Switching ON the Camera
            # _switch_util = IPSwitchHelper()
            # _device = 'meetup'
            # _switch_util.switch_on(_device)
            device_name = 'MeetUp'

            # Add the productAvailableEvent to event_list.
            self.websocket_dict['event_list'] = ['productAvailableEvent']

            connect_device(device_name)
            time.sleep(2)

            websocket_conn = WebsocketConnection(self.websocket_dict)
            event_response = self.loop.run_until_complete(
                websocket_conn.event_listener(),
            )

            # Parse the response
            products = event_response['event']['productEvent']['productAvailableEvent']
            Report.logResponse(products)

            # Validate the response
            _status = ProtobufUtils.validate_connect_event(products)
            log_helper.test_result_logger(self.id(), _status)
        except Exception as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncProductAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
