'''
:Module Name: **videosettingsrequest**

===============================

A library that implements the Video Settings protobuf API.
'''

import logging
import asyncio
from apis.sync_api.protobuf_helper import ProtobufUtils
from common.config import AntiFlickerConfig
from common.config import DeviceModelConfig
import video_settings_requests_pb2 as videosettingsrequest

log = logging.getLogger(__name__)


class VideosettingsRequest:
    """
    Methods that implement the Video Settings protobuf API.

    """

    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 10.0

    def __del__(self):
        del self.ws_dict

    def _create_set_right_sight_configuration_request(self, product_uuid, enabled, mode):
        """
        Method to create a SetRightSightConfigurationRequest request .
        :param id:
        :return:
        """
        try:
            # Create a video settings request object
            videosettings_req = videosettingsrequest.VideoSettingsRequest()

            # Create an anti flicker configuration request object
            set_rightsight_request_obj = videosettingsrequest.SetRightSightConfigurationRequest()

            set_rightsight_request_obj.product_uuid = str(product_uuid)
            set_rightsight_request_obj.product_model = DeviceModelConfig.model_meetup

            if enabled:
                set_rightsight_request_obj.enabled = True
                if mode == 'ON_CALL_START':
                    set_rightsight_request_obj.mode = 1

            videosettings_req.set_right_sight_configuration_request.CopyFrom(
                set_rightsight_request_obj
            )

            return videosettings_req

        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def _create_set_anti_flicker_configuration_request(self, product_uuid, anti_flicker_mode):
        """
        Method to create a SetAntiFlickerConfigurationRequest request .
        :param id:
        :return:
        """
        try:
            # Create a video settings request object
            videosettings_req = videosettingsrequest.VideoSettingsRequest()

            # Create an anti flicker configuration request object
            set_antiflicker_request_obj = videosettingsrequest.SetAntiFlickerConfigurationRequest()

            set_antiflicker_request_obj.product_uuid = str(product_uuid)
            set_antiflicker_request_obj.product_model = DeviceModelConfig.model_rally_bar
            # NTSC- 60 Hz - 0, PAL - 50 Hz

            if anti_flicker_mode == 'NTSC':
                set_antiflicker_request_obj.anti_flicker_mode = AntiFlickerConfig.ANTIFLICKER_NTSC_ENUMERATION

            elif anti_flicker_mode == 'PAL':
                set_antiflicker_request_obj.anti_flicker_mode = AntiFlickerConfig.ANTIFLICKER_PAL_ENUMERATION

            videosettings_req.set_anti_flicker_configuration_request.CopyFrom(
                set_antiflicker_request_obj
            )

            return videosettings_req

        except Exception as e:
            log.error('Failed to create the product request: {}'.format(e))
            raise e

    def create_set_right_sight_configuration_request(self, product_uuid, enabled=True, mode=0):
        """
        Method to create a protobuf request for SetRightSightConfigurationRequest
        mode = 0 for Dynamic setting of rightsight
        mode = 1 for on-call start setting of rightsight
        :return: response payload
        """

        try:
            log.debug(
                'Set the rightsight configuration request',
            )

            # Construct probuf request
            logisync_message = self.proto_buf.create_logisync_message_header

            _videosetting_req_obj = self._create_set_right_sight_configuration_request(product_uuid, enabled, mode)

            logisync_message.request.video_settings_request.CopyFrom(_videosetting_req_obj)
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

    def create_set_anti_flicker_configuration_request(self, product_uuid, anti_flicker_mode):
        """
        Method to create a protobuf request for SetAntiFlickerConfigurationRequest
        :return: response payload
        """

        try:
            log.debug(
                'Set the anti flicker configuration request',
            )

            # Construct probuf request
            logisync_message = self.proto_buf.create_logisync_message_header

            _videosetting_req_obj = self._create_set_anti_flicker_configuration_request(product_uuid, anti_flicker_mode)

            logisync_message.request.video_settings_request.CopyFrom(_videosetting_req_obj)
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
