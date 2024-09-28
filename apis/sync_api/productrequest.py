"""
:Module Name: **productrequest**

==============================

A library that implements the ProductRequest protobuf API.
All methods that are part of this API class can be defined here.
For ex: get list of all products

"""
import asyncio
import logging

import product_state_requests_pb2 as product_request
from apis.sync_api.protobuf_helper import ProtobufUtils
from apis.sync_api.websocketconnection import WebsocketConnection

log = logging.getLogger(__name__)


class ProductRequest:
    '''
    This class implements the ProductRequest protobuf API such as
    GetAllProductsRequest, GetProductByIdRequest,
    GetProductConfigurationRequest, SetProductConfigurationRequest,
    ClearProductConfigurationRequest

    '''

    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 10.0

    def __del__(self):
        del self.ws_dict

    def _create_get_product_request(self, id):
        """
        Method to create a product request .
        It can handle two protobuf APIs , get_all_product_request or
        get_product_by_id_requests based on id value

        :param id:
        :return:
        """
        try:
            prod_request = product_request.ProductRequest()
            # If id is None call get_all_products_requests
            if not id:
                _product_req_obj = product_request.GetAllProductsRequest()
                prod_request.get_all_products_request.CopyFrom(
                    _product_req_obj,
                )
            else:
                # creates the request if id is provided
                _product_req_obj = product_request.GetProductByIdRequest()
                _product_req_obj.product_uuid = str(id)
                prod_request.get_product_by_id_request.CopyFrom(
                    _product_req_obj,
                )

            return prod_request
        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_product_request(self, id=None):
        """
        Method to create a protobuf request for get all product information
        or get product information by product uuid
        :return: response payload
        """

        try:
            log.debug(
                'Preparing to get product and its firmware information',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_req_obj = self._create_get_product_request(id)

            logisync_message.request.product_request.CopyFrom(_product_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetProductByIdRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetProductByIdRequest Failed {}'.format(e))
            raise e

    def _create_product_reboot_request(self, product_uuid):
        """
        Method to send product reboot request.

        :param id:
        :return:
        """
        try:
            prod_request = product_request.ProductRequest()

            # creates the request if id is provided
            _product_req_obj = product_request.SendProductRebootRequest()
            _product_req_obj.product_uuid = str(product_uuid)
            prod_request.send_product_reboot_request.CopyFrom(
                _product_req_obj,
            )
            return prod_request

        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_product_reboot_request(self, product_uuid):
        """
        Method to create a protobuf request for product reboot
        :return: response payload
        """

        try:
            log.debug(
                'Product Reboot request',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_req_obj = self._create_product_reboot_request(product_uuid)

            logisync_message.request.product_request.CopyFrom(_product_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SendProductRebootRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetProductByIdRequest Failed {}'.format(e))
            raise e

    def get_product_uuid(self):
        """
        Function to get product uuid value for the connected device ,
        it return an error if no devices are connected

        :return: ``product_uuid``
        :rtype:  ``string``
        """
        try:
            # Generate the Product request message
            self.ws_dict['msg_buffer'] = self.create_product_request()

            # Send request to proxy server via a websocket connection
            ws_conn = WebsocketConnection(self.ws_dict)

            # Collect the parsed response. It is guaranteed not to be a Pong message.
            product_data = self.loop.run_until_complete(
                ws_conn.request_response_listener(),
            )

            # Validate the response
            if 'response' not in product_data:
                raise AssertionError(
                    'Failed to get response in '
                    'get_product_uuid',
                )
            products = product_data['response']['productResponse'][
                'getAllProductsResponse'
            ]
            # Check if product is not empty
            if bool(products):
                if products['products'][0]['connectionState'] == 'SYNC_CONNECTION_STATE_OFFLINE':
                    raise AssertionError(
                        'Device connection state is offline, '
                        'Check if device is connected',
                    )
                else:
                    product_uuid = products['products'][0]['uuid']
            else:
                raise AssertionError(
                    'Failed to get the product uuid, '
                    'Check if device is connected',
                )
            return product_uuid

        except KeyError as key_error:
            log.error('Unable to Get the UUID {}'.format(key_error))
            raise key_error

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except Exception as err:
            log.error('{}'.format(err))
            raise err

    def _create_get_product_configuration_request(self, product_uuid):
        """
        Method to create a GetProductConfigurationRequest message.

        :param id:
        :return:
        """
        try:
            prod_request = product_request.ProductRequest()
            _product_req_obj = product_request.GetProductConfigurationRequest()
            _product_req_obj.product_uuid = str(product_uuid)
            prod_request.get_product_configuration_request.CopyFrom(
                _product_req_obj,
            )
            return prod_request
        except Exception as e:
            log.error('Failed to create the GetProductConfigurationRequest: {}'.format(e))
            raise e

    def create_get_product_configuration_request(self, product_uuid):
        """
        Method to create a protobuf request for GetProductConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Create a message for GetProductConfigurationRequest ',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_req_obj = self._create_get_product_configuration_request(product_uuid)

            logisync_message.request.product_request.CopyFrom(_product_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetProductConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('GetProductConfigurationRequest Failed {}'.format(e))
            raise e

    def _create_set_product_configuration_request(self, product_uuid, configuration_base):
        """
            Method to create a SetProductConfigurationRequest message.
        """
        try:
            prod_conf_request = product_request.ProductRequest()
            _product_conf_req_obj = product_request.SetProductConfigurationRequest()
            _product_conf_req_obj.product_uuid = str(product_uuid)

            if len(configuration_base) > 0:
                for key, value in configuration_base.items():
                    _product_conf_req_obj.expected_device_count[key] = value

            prod_conf_request.set_product_configuration_request.CopyFrom(
                _product_conf_req_obj,
            )
            return prod_conf_request
        except Exception as e:
            log.error('Failed to create the SetProductConfigurationRequest: {}'.format(e))
            raise e

    def create_set_product_configuration_request(self, product_uuid, configuration_base):
        """
            Method to create a protobuf request for SetProductConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Create a message for GetProductConfigurationRequest ',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_conf_req_obj = self._create_set_product_configuration_request(product_uuid, configuration_base)

            logisync_message.request.product_request.CopyFrom(_product_conf_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetProductConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('SetProductConfigurationRequest Failed {}'.format(e))
            raise e

    def _create_clear_product_configuration_request(self, product_uuid):
        """
            Method to create a ClearProductConfigurationRequest message.
        """
        try:
            prod_conf_request = product_request.ProductRequest()
            _product_conf_req_obj = product_request.ClearProductConfigurationRequest()
            _product_conf_req_obj.product_uuid = str(product_uuid)

            prod_conf_request.clear_product_configuration_request.CopyFrom(
                _product_conf_req_obj,
            )
            return prod_conf_request
        except Exception as e:
            log.error('Failed to create the ClearProductConfigurationRequest: {}'.format(e))
            raise e

    def create_clear_product_configuration_request(self, product_uuid):
        """
            Method to create a protobuf request for ClearProductConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Create a message for ClearProductConfigurationRequest ',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_conf_req_obj = self._create_clear_product_configuration_request(product_uuid)

            logisync_message.request.product_request.CopyFrom(_product_conf_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'ClearProductConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('ClearProductConfigurationRequest Failed {}'.format(e))
            raise e

    def _create_forget_product_request(self, product_uuid, product_model, device_uuids):
        """
            Method to create a ForgetProductRequest message.
        """
        try:
            prod_conf_request = product_request.ProductRequest()
            _product_conf_req_obj = product_request.ForgetDeviceRequest()
            _product_conf_req_obj.product_uuid = str(product_uuid)
            _product_conf_req_obj.product_model = product_model

            if device_uuids:
                for device in device_uuids:
                    _product_conf_req_obj.device_uuids.append(device)

            prod_conf_request.forget_device_request.CopyFrom(
                _product_conf_req_obj,
            )
            return prod_conf_request
        except Exception as e:
            log.error('Failed to create the ForgetDeviceRequest: {}'.format(e))
            raise e

    def create_forget_product_request(self, product_uuid, product_model, device_uuids=None):
        """
            Method to create a protobuf request for ForgetDeviceRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Create a message for ForgetDeviceRequest ',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _product_conf_req_obj = self._create_forget_product_request(product_uuid, product_model, device_uuids)

            logisync_message.request.product_request.CopyFrom(_product_conf_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'ForgetDeviceRequest - Message Request - {}'.format(
                    msg_buffer,
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('ForgetDeviceRequest Failed {}'.format(e))
            raise e