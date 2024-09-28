import asyncio
import logging
from apis.sync_api.protobuf_helper import ProtobufUtils
from common.config import DeviceModelConfig
import ble_settings_requests_pb2 as ble_proto

log = logging.getLogger(__name__)

class BLESettingsRequest:
    """
    Methods that implement the bluetooth settings protobuf API.

    """

    def __init__(self):
        self.protobuf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 30.0

    def __del__(self):
        del self.ws_dict

    def _create_set_ble_configuration_request(self, product_uuid, ble_mode):
        """
        Method to create a SetBleConfigurationRequest message.
        :return:
        """
        try:
            # Create a ble settings request object.
            blesettings_req = ble_proto.BleSettingsRequest()

            # Create a ble configuration request object.
            set_ble_config_request = ble_proto.SetBleConfigurationRequest()

            set_ble_config_request.product_uuid = str(product_uuid)
            set_ble_config_request.product_model = DeviceModelConfig.model_rally_bar

            # Toggle bluetooth on or off.
            if ble_mode == 'BLE_OFF':
                set_ble_config_request.ble_mode = 0
            elif ble_mode == 'BLE_OFF_redundant_test':
                set_ble_config_request.ble_mode = 0
            elif ble_mode == 'BLE_ON':
                set_ble_config_request.ble_mode = 1
            elif ble_mode == 'BLE_ON_redundant_test':
                set_ble_config_request.ble_mode = 1

            blesettings_req.set_ble_configuration_request.CopyFrom(
                set_ble_config_request
            )

            return blesettings_req

        except Exception as e:
            log.error('Failed to create the ble request: {}'.format(e))
            raise e

    def create_set_ble_configuration_proto_request(self, product_uuid, ble_mode):
        try:
            _ble_settings_req_obj = self._create_set_ble_configuration_request(product_uuid, ble_mode)
            logisync_message = self.protobuf.create_logisync_message_header
            logisync_message.request.ble_settings_request.CopyFrom(_ble_settings_req_obj)
            msg_buffer = self.protobuf.serialize_request(logisync_message)
            log.info(
                'Set BLE Configuration - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('Failed to create the BLE configuration request: {}'.format(e))
            raise e



