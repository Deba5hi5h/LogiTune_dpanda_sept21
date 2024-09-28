"""
:Module Name: **devicesettingsrequest**

==============================

A library that implements the FirmwareRequest protobuf API.
All methods that are part of this API class can be defined here.

"""
import asyncio
import logging

import device_settings_requests_pb2 as device_settings_request
from apis.sync_api.protobuf_helper import ProtobufUtils

log = logging.getLogger(__name__)


class DeviceSettingsRequest:
    """
        This class implements the DeviceSettingsRequest protobuf API such as
        SetDeviceDisplayConfigurationRequest
    """
    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 30.0

    def __del__(self):
        del self.ws_dict

    def _create_set_device_display_configuration_request(self, device_uuid, product_model, brightness):
        """
            Method to create a device display configuration request.
            It can handle protobuf APIs set_device_display_configuration_request
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetDeviceDisplayConfigurationRequest()
            _device_req_obj.device_uuid = str(device_uuid)
            _device_req_obj.product_model = product_model
            _device_req_obj.brightness = brightness
            device_request.set_device_display_configuration_request.CopyFrom(
                _device_req_obj,
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def create_set_device_display_configuration(self, device_uuid, product_model, brightness):
        """
            Method to create a protobuf request for SetDeviceDisplayConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get SetDeviceDisplayConfigurationRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_set_device_display_configuration_request(device_uuid, product_model, brightness)
            logisync_message.request.device_settings_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetDeviceDisplayConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetDeviceDisplayConfigurationRequest Failed {}'.format(e))
            raise e

    def _create_set_audio_noise_reduction_request(self, product_uuid, product_model, noise_reduction):
        """
            Method to create a device display configuration request.
            It can handle protobuf APIs SetAudioNoiseReductionRequest.
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetAudioNoiseReductionRequest()
            _device_req_obj.product_uuid = str(product_uuid)
            _device_req_obj.product_model = product_model
            if noise_reduction == 'DISABLE':
                audio_noise_reduction = 0
            else:
                audio_noise_reduction = 1
            _device_req_obj.noise_reduction = audio_noise_reduction
            device_request.set_audio_noise_reduction_request.CopyFrom(
                _device_req_obj
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def create_set_audio_noise_reduction_request(self, product_uuid, product_model, noise_reduction):
        """
            Method to create a protobuf request for SetAudioNoiseReductionRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get SetAudioNoiseReductionRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _audio_req_obj = self._create_set_audio_noise_reduction_request(product_uuid, product_model, noise_reduction)
            logisync_message.request.device_settings_request.CopyFrom(_audio_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetAudioNoiseReductionRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetAudioNoiseReductionRequest Failed {}'.format(e))
            raise e

    def _create_set_audio_speaker_boost_request(self, product_uuid, product_model, speaker_boost):
        """
            Method to create a device display configuration request.
            It can handle protobuf APIs SetAudioSpeakerBoostRequest
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetAudioSpeakerBoostRequest()
            _device_req_obj.product_uuid = str(product_uuid)
            _device_req_obj.product_model = product_model
            if speaker_boost == 'DISABLE':
                audio_speaker_boost = 0
            else:
                audio_speaker_boost = 1
            _device_req_obj.speaker_boost = audio_speaker_boost
            device_request.set_audio_speaker_boost_request.CopyFrom(
                _device_req_obj
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def create_set_audio_speaker_boost_request(self, product_uuid, product_model, speaker_boost):
        """
            Method to create a protobuf request for SetAudioSpeakerBoostRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get SetAudioSpeakerBoostRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _audio_req_obj = self._create_set_audio_speaker_boost_request(product_uuid, product_model, speaker_boost)
            logisync_message.request.device_settings_request.CopyFrom(_audio_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetAudioNoiseReductionRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetAudioSpeakerBoostRequest Failed {}'.format(e))
            raise e

    def _create_set_audio_reverb_mode_request(self, product_uuid, product_model, reverb_mode):
        """
            Method to create a device settings request.
            It can handle protobuf APIs SetAudioReverbModeRequest
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetAudioReverbModeRequest()
            _device_req_obj.product_uuid = str(product_uuid)
            _device_req_obj.product_model = product_model
            if reverb_mode == 'NORMAL':
                audio_reverb_mode = 2
            elif reverb_mode == 'AGGRESSIVE':
                audio_reverb_mode = 3
            else:
                audio_reverb_mode = 0
            _device_req_obj.reverb_mode = audio_reverb_mode
            device_request.set_audio_reverb_mode_request.CopyFrom(
                _device_req_obj
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def create_set_audio_reverb_mode_request(self, product_uuid, product_model, reverb_mode):
        """
            Method to create a protobuf request for SetAudioReverbModeRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get SetAudioReverbModeRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _audio_req_obj = self._create_set_audio_reverb_mode_request(product_uuid, product_model, reverb_mode)
            logisync_message.request.device_settings_request.CopyFrom(_audio_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetAudioNoiseReductionRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetAudioNoiseReductionRequest Failed {}'.format(e))
            raise e

    def _create_set_device_whiteboard_configuration_request(self, product_uuid, product_model, whiteboard_configuration):
        """
            Method to create a device settings request.
            It can handle protobuf APIs SetDeviceWhiteboardConfigurationRequest
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetDeviceWhiteboardConfigurationRequest()
            _device_req_obj.product_uuid = str(product_uuid)
            _device_req_obj.product_model = product_model
            _device_req_obj.whiteboard_configuration.image_enhancement = whiteboard_configuration['image_enhancement']
            _device_req_obj.whiteboard_configuration.ghosting = whiteboard_configuration['ghosting']
            device_request.set_device_whiteboard_configuration_request.CopyFrom(
                _device_req_obj
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def _create_set_device_whiteboard_edit_boundaries_request(self, product_uuid, product_model, enabled):
        """
            Method to create a device settings request.
            It can handle protobuf APIs SetDeviceWhiteboardEditBoundariesRequest
        """
        try:
            device_request = device_settings_request.DeviceSettingsRequest()
            _device_req_obj = device_settings_request.SetDeviceWhiteboardEditBoundariesRequest()
            _device_req_obj.product_uuid = str(product_uuid)
            _device_req_obj.product_model = product_model
            _device_req_obj.enabled = enabled
            device_request.set_device_whiteboard_edit_boundaries_request.CopyFrom(
                _device_req_obj
            )

            return device_request
        except Exception as e:
            log.error('Failed to create the device settings request: {}'.format(e))
            raise e

    def create_set_device_whiteboard_configuration_request(self, product_uuid, product_model, whiteboard_configuration):
        """
            Method to create a protobuf request for SetDeviceWhiteboardConfigurationRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'SetDeviceWhiteboardConfigurationRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _whiteboard_req_obj = self._create_set_device_whiteboard_configuration_request(product_uuid, product_model, whiteboard_configuration)
            logisync_message.request.device_settings_request.CopyFrom(_whiteboard_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetDeviceWhiteboardConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetDeviceWhiteboardConfigurationRequest Failed {}'.format(e))
            raise e

    def create_set_device_whiteboard_edit_boundaries_request(self, product_uuid, product_model, enabled):
        """
            Method to create a protobuf request for SetDeviceWhiteboardEditBoundariesRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'SetDeviceWhiteboardEditBoundariesRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _whiteboard_req_obj = self._create_set_device_whiteboard_edit_boundaries_request(product_uuid, product_model, enabled)
            logisync_message.request.device_settings_request.CopyFrom(_whiteboard_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetDeviceWhiteboardConfigurationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetDeviceWhiteboardConfigurationRequest Failed {}'.format(e))
            raise e

