"""
:Module Name: **configurationrequest**

==============================

A library that implements the ConfigurationRequest protobuf API.
All methods that are part of this API class can be defined here.

"""
import asyncio
import logging

import configuration_requests_pb2 as configuration_request
from apis.sync_api.protobuf_helper import ProtobufUtils

log = logging.getLogger(__name__)

class ConfigurationRequest:
    '''
    This class implements the ConfigurationRequest protobuf API such as
    GetLogiSyncConfigurationRequest, GetHostInformationRequest,
    SetLogiSyncConfigurationRequest

    '''

    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 10.0

    def __del__(self):
        del self.ws_dict

    def _create_get_host_information_request(self):
        """
            Method to create a host information request.
            It can handle protobuf APIs get_host_information_request
        """
        try:
            conf_request = configuration_request.LogiSyncConfigurationRequest()
            _host_inf_req_obj = configuration_request.GetHostInformationRequest()
            conf_request.get_host_information_request.CopyFrom(
                _host_inf_req_obj,
            )

            return conf_request
        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_host_information_request(self):
        """
            Method to create a protobuf request for GetHostInformationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get GetLogiSyncConfigurationRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _conf_req_obj = self._create_get_host_information_request()
            logisync_message.request.configuration_request.CopyFrom(_conf_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetHostInformationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetHostInformationRequest Failed {}'.format(e))
            raise e

    def _create_get_logi_sync_configuration_request(self):
        """
            Method to create a GetLogiSyncConfigurationRequest message.
        """
        try:
            conf_request = configuration_request.LogiSyncConfigurationRequest()
            _conf_req_obj = configuration_request.GetLogiSyncConfigurationRequest()
            conf_request.get_logi_sync_configuration_request.CopyFrom(
                _conf_req_obj,
            )

            return conf_request
        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_logi_sync_configuration_request(self):
        """
            Method to create a protobuf request for GetLogiSyncConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get GetLogiSyncConfigurationRequest',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _conf_req_obj = self._create_get_logi_sync_configuration_request()
            logisync_message.request.configuration_request.CopyFrom(_conf_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetLogiSyncConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetLogiSyncConfigurationRequest Failed {}'.format(e))
            raise e

    def _create_set_logi_sync_configuration_request(self, configuration_base):
        """
            Method to create a SetLogiSyncConfigurationRequest message.
        """
        try:
            conf_request = configuration_request.LogiSyncConfigurationRequest()

            _conf_req_obj = configuration_request.SetLogiSyncConfigurationRequest()
            _config = {}

            for key, value in configuration_base.items():
                _conf_req_obj.configuration.configuration[int(key)] = value

            conf_request.set_logi_sync_configuration_request.CopyFrom(
                _conf_req_obj
            )

            return conf_request

        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_set_logi_sync_configuration_request(self, configuration_base):
        """
            Method to create a protobuf request for SetLogiSyncConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Set SetLogiSyncConfigurationRequest',
            )

            # Construct probuf request
            logisync_message = self.proto_buf.create_logisync_message_header

            _set_conf_req_obj = self._create_set_logi_sync_configuration_request(configuration_base)

            logisync_message.request.configuration_request.CopyFrom(_set_conf_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetLogiSyncConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetProductByIdRequest Failed {}'.format(e))
            raise e