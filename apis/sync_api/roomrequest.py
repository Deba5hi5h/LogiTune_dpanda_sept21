"""
:Module Name: **roomrequest**

==============================

A library that implements the RoomRequest protobuf API.
All methods that are part of this API class can be defined here.
For ex: get list of all products

"""
import asyncio
import logging

import room_requests_pb2 as room_requests
from apis.sync_api.protobuf_helper import ProtobufUtils

log = logging.getLogger(__name__)


class RoomRequest:
    '''
    This class implements the RoomRequest protobuf API

    '''

    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()
        self.ws_dict = dict()
        self.ws_dict['type'] = 'LogiSync'
        self.ws_dict['timeout'] = 10.0

    def __del__(self):
        del self.ws_dict

    def _create_getRoomInformationRequest(self):
        """
        Method to create a GetRoomInformationRequest .
        It can handle protobuf APIs , get_room_information_request.

        :return:
        """
        try:
            room_req = room_requests.RoomRequest()
            _room_req_obj = room_requests.GetRoomInformationRequest()
            room_req.get_room_information_request.CopyFrom(
                _room_req_obj
            )
            return room_req

        except Exception as e:
            log.error('Failed to create get room information request message: {}'.format(e))
            raise e

    def create_get_room_information_request(self):
        """
        Method to create a protobuf request for create get Room Information Request
        :return: response payload
        """

        try:
            log.debug(
                'Preparing to get room information request',
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _room_req_obj = self._create_getRoomInformationRequest()

            logisync_message.request.room_request.CopyFrom(_room_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'GetRoomInformationRequest - Message Request - {}'.format(
                    msg_buffer,
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('GetRoomInformationRequest Failed {}'.format(e))
            raise e

    def _create_setRoomNameRequest(self, room_name):
        """
        Method to create SetRoomNameRequest
        :param room_name:
        :return:
        """
        try:
            room_req = room_requests.RoomRequest()
            _room_req_obj = room_requests.SetRoomNameRequest()
            _room_req_obj.room_name = room_name
            room_req.set_room_name_request.CopyFrom(
                _room_req_obj
            )
            return room_req

        except Exception as e:
            log.error('Failed to create SetRoomNameRequest message: {}'.format(e))
            raise e

    def _create_setMaxOccupancyRequest(self, max_occupancy):
        """
        Method to create SetMaxOccupancyRequest.
        :param max_occupancy:
        :return:
        """
        try:
            room_req = room_requests.RoomRequest()
            _room_req_obj = room_requests.SetRoomMaxOccupancyRequest()
            _room_req_obj.max_occupancy = max_occupancy
            room_req.set_room_max_occupancy_request.CopyFrom(
                _room_req_obj
            )
            return room_req

        except Exception as e:
            log.error('Failed to create SetMaxOccupancyRequest message: {}'.format(e))
            raise e

    def _create_setRoomOccupancyModeRequest(self, mode):
        """
        Method to create SetRoomOccupancyModeRequest.
        :param max_occupancy:
        :return:
        """
        try:
            room_req = room_requests.RoomRequest()
            _room_req_obj = room_requests.SetRoomOccupancyModeRequest()
            _room_req_obj.mode = mode
            room_req.set_room_occupancy_mode_request.CopyFrom(
                _room_req_obj
            )
            return room_req

        except Exception as e:
            log.error('Failed to SetRoomOccupancyModeRequest message: {}'.format(e))
            raise e

    def _create_bulkSetRoomInformationRequest(self, room_info):
        """
        Method to create BulkSetRoomInformationRequest.
        :param max_occupancy:
        :return:
        """
        try:
            room_req = room_requests.RoomRequest()
            room_req_obj = room_requests.BulkSetRoomInformationRequest()
            for attribute, response in room_info.items():
                room_req_obj.room_information[attribute] = response

            room_req.bulk_set_room_information_request.CopyFrom(
                room_req_obj
            )
            return room_req

        except Exception as e:
            log.error('Failed to SetRoomOccupancyModeRequest message: {}'.format(e))
            raise e


    def create_set_room_name_request(self, room_name):
        """
        Method to create a protobuf request for create SetRoomNameRequest
        :param room_name:
        :return:
        """

        try:
            log.debug(
                'Preparing to set room name to {}'.format(room_name),
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _room_req_obj = self._create_setRoomNameRequest(room_name)

            logisync_message.request.room_request.CopyFrom(_room_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetRoomNameRequest - Message Request - {}'.format(
                    msg_buffer
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('SetRoomNameRequest Failed {}'.format(e))
            raise e

    def create_set_max_occupancy_request(self, max_occupancy):
        """
            Method to create a protobuf request for create SetRoomMaxOccupancyRequest
            :param room_name:
            :return:
        """

        try:
            log.debug(
                'Preparing to set max occupancy of room to {}'.format(max_occupancy),
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _room_req_obj = self._create_setMaxOccupancyRequest(max_occupancy)

            logisync_message.request.room_request.CopyFrom(_room_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetRoomMaxOccupancyRequest - Message Request - {}'.format(
                    msg_buffer
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('SetRoomMaxOccupancyRequest Failed {}'.format(e))
            raise e

    def create_set_room_occupancy_mode_request(self, mode):
        """
            Method to create a protobuf request for create SetRoomOccupancyModeRequest
            :param room_name:
            :return:
        """

        try:
            log.debug(
                'Preparing to set occupancy mode of room to {}'.format(mode),
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _room_req_obj = self._create_setRoomOccupancyModeRequest(mode)

            logisync_message.request.room_request.CopyFrom(_room_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'SetRoomOccupancyModeRequest - Message Request - {}'.format(
                    msg_buffer
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('SetRoomOccupancyModeRequest Failed {}'.format(e))
            raise e

    def create_bulk_set_room_information_request(self, room_information):
        """
            Method to create a protobuf request for create BulkSetRoomInformationRequest
            :param room_name:
            :return:
        """

        try:
            log.debug(
                'Preparing to bulk set room information with room information {}'.format(room_information),
            )

            # Construct probuf config request
            logisync_message = self.proto_buf.create_logisync_message_header

            _room_req_obj = self._create_bulkSetRoomInformationRequest(room_information)

            logisync_message.request.room_request.CopyFrom(_room_req_obj)
            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'BulkSetRoomInformationRequest - Message Request - {}'.format(
                    msg_buffer
                )
            )
            return msg_buffer

        except Exception as e:
            log.error('SetRoomOccupancyModeRequest Failed {}'.format(e))
            raise e

