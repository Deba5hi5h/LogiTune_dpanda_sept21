"""
:Module Name: **firmwarerequest**

==============================

A library that implements the FirmwareRequest protobuf API.
All methods that are part of this API class can be defined here.

"""
import asyncio
import logging

import firmware_requests_pb2 as firmware_request
from apis.sync_api.protobuf_helper import ProtobufUtils

log = logging.getLogger(__name__)

class FirmwareRequest:
    """
        This class implements the ConfigurationRequest protobuf API such as
        GetLatestFirmwareByProductIdRequest
    """
    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 10.0

    def __del__(self):
        del self.ws_dict

    def _create_get_latest_firmware(self, product_uuid):
        """
            Method to create a get latest firmware request.
            It can handle protobuf APIs get_latest_firmware_by_product_id_request
        """
        try:
            fw_request = firmware_request.FirmwareRequest()
            _fw_req_obj = firmware_request.GetLatestFirmwareByProductIdRequest()
            _fw_req_obj.product_uuid = str(product_uuid)
            fw_request.get_latest_firmware_by_product_id_request.CopyFrom(
                _fw_req_obj,
            )

            return fw_request
        except Exception as e:
            log.error('Failed to create the firmware request: {}'.format(e))
            raise e

    def create_get_latest_firmware(self, product_uuid):
        """
            Method to create a protobuf request for GetLatestFirmwareByProductIdRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get GetLatestFirmwareByProductIdRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_get_latest_firmware(product_uuid=product_uuid)
            logisync_message.request.firmware_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetLatestFirmwareByProductIdRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetLatestFirmwareByProductIdRequest Failed {}'.format(e))
            raise e

    def _create_update_firmware_by_id(self, product_uuid, package_version=None):
        """
            Method to create a update firmware by id request.
            It can handle protobuf APIs update_firmware_by_id_request
        """
        try:
            fw_request = firmware_request.FirmwareRequest()
            _fw_req_obj = firmware_request.UpdateFirmwareByProductIdRequest()
            _fw_req_obj.product_uuid = str(product_uuid)
            if package_version:
                _fw_req_obj.firmware_package_version = package_version
            fw_request.update_firmware_by_id_request.CopyFrom(
                _fw_req_obj,
            )

            return fw_request
        except Exception as e:
            log.error('Failed to create the firmware request: {}'.format(e))
            raise e

    def create_update_firmware_by_id(self, product_uuid, package_version):
        """
            Method to create a protobuf request for UpdateFirmwareByProductIdRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get UpdateFirmwareByProductIdRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_update_firmware_by_id(product_uuid=product_uuid, package_version=package_version)
            logisync_message.request.firmware_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'UpdateFirmwareByProductIdRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('UpdateFirmwareByProductIdRequest Failed {}'.format(e))
            raise e

    def _create_update_all_firmware(self):
        """
            Method to create a update firmware by id request.
            It can handle protobuf APIs update_all_firmware_request
        """
        try:
            fw_request = firmware_request.FirmwareRequest()
            _fw_req_obj = firmware_request.UpdateAllFirmwareRequest()

            fw_request.update_all_firmware_request.CopyFrom(
                _fw_req_obj,
            )

            return fw_request
        except Exception as e:
            log.error('Failed to create the firmware request: {}'.format(e))
            raise e

    def create_update_all_firmware(self):
        """
            Method to create a protobuf request for UpdateAllFirmwareRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get UpdateAllFirmwareRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_update_all_firmware()
            logisync_message.request.firmware_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'UpdateAllFirmwareRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('UpdateAllFirmwareRequest Failed {}'.format(e))
            raise e

    def _create_get_firmware_update_progress(self):
        """
            Method to create a update firmware by id request.
            It can handle protobuf APIs get_firmware_update_progress_request
        """
        try:
            fw_request = firmware_request.FirmwareRequest()
            _fw_req_obj = firmware_request.GetFirmwareUpdateProgressRequest()
            fw_request.get_firmware_update_progress_request.CopyFrom(
                _fw_req_obj,
            )

            return fw_request
        except Exception as e:
            log.error('Failed to create the firmware request: {}'.format(e))
            raise e

    def create_get_firmware_update_progress(self):
        """
            Method to create a protobuf request for GetFirmwareUpdateProgressRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get GetFirmwareUpdateProgressRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_get_firmware_update_progress()
            logisync_message.request.firmware_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetFirmwareUpdateProgressRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetFirmwareUpdateProgressRequest Failed {}'.format(e))
            raise e

    def _create_set_firmware_update_schedule(self, product_id, product_m, scheduled_up=None):
        """
            Method to create a update firmware by id request.
            It can handle protobuf APIs set_firmware_update_schedule_request
        """
        try:
            fw_request = firmware_request.FirmwareRequest()
            _fw_req_obj = firmware_request.SetFirmwareUpdateScheduleRequest()
            _fw_req_obj.product_uuid = product_id
            _fw_req_obj.product_model = product_m

            if scheduled_up:
                if 'update_package_version' in scheduled_up:
                    _fw_req_obj.scheduled_update.issued_time = scheduled_up['update_package_version']
                if 'update_published_date' in scheduled_up:
                    _fw_req_obj.scheduled_update.issued_time = scheduled_up['update_published_date']
                if 'issued_time' in scheduled_up:
                    _fw_req_obj.scheduled_update.issued_time = scheduled_up['issued_time']
                if 'earliest_time' in scheduled_up:
                    _fw_req_obj.scheduled_update.earliest_time = scheduled_up['earliest_time']
                if 'latest_time' in scheduled_up:
                    _fw_req_obj.scheduled_update.latest_time = scheduled_up['latest_time']

            fw_request.set_firmware_update_schedule_request.CopyFrom(
                _fw_req_obj,
            )

            return fw_request
        except Exception as e:
            log.error('Failed to create the firmware request: {}'.format(e))
            raise e

    def create_set_firmware_update_schedule(self, product_uuid, product_model, scheduled_update):
        """
            Method to create a protobuf request for SetFirmwareUpdateScheduleRequest message.
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get SetFirmwareUpdateScheduleRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            _fw_req_obj = self._create_set_firmware_update_schedule(product_uuid, product_model, scheduled_update)
            logisync_message.request.firmware_request.CopyFrom(_fw_req_obj)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetFirmwareUpdateScheduleRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('SetFirmwareUpdateScheduleRequest Failed {}'.format(e))
            raise e