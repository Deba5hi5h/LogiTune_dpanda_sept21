"""
:Module Name: **protobuf_helper**

===============================

Protocol Buffers is a serialization technology developed by Google which uses a simple and efficient scheme
to transform structured data into compressed, binary data. This binary data can then, for example, be sent
to a client or server over an established WebSocket connection.

In order to use Protocol Buffers, one defines data structures that will be sent over the network in a .proto
file which can then be compiled into the developer’s language of choice. The .proto files are defined in the
github repo vc-oneapp-api which also hosts the compiled .pb2 files. This repo is cloned and the .proto and
.pb2 files are placed under library/protobuf.

Applications can then natively use these data structures in their applications which include built-in functions
for serialization and deserialization.

This module contains the 1 classes with following functionality -
1) Parse the protobuf headers - ie parse ResponseOK from the meta headers
2) Generate the Std Headers MetaClass
Refer - https://docs.google.com/document/d/1ajoZDq5C640I2cqDzHxEHNeMNjzVSU8jYY9c89Nac-k/edit#heading=h.lfzxaut69wa7

"""

import logging
import time
from random import randint

import cloud_message_pb2 as cloud_msg
import transport_pb2 as transport
from google.protobuf.json_format import MessageToDict
# import protocol buffer compiler code

log = logging.getLogger(__name__)
RESPONSEOK = 2
EVENT = 4
SOURCE_PROXY = 2
SOURCE_CLIENT = 1
INTERNAL_API_ID = 1


class ProtobufUtils:
    """
    ProtobufHandle - Parse the protobuf headers - ie parse ResponseOK
    from the meta headers

    """

    def __init__(self):
        pass

    @staticmethod
    def convert_protobuf_to_json(protobuf):
        """
        Function that converts the protobuf byte array into a json format

        """
        try:
            jsonresponse = MessageToDict(protobuf)
            return jsonresponse
        except Exception as e:
            log.error(
                'Failed to convert protobuf byte array into json {}'.format(e),
            )
            raise e

    @staticmethod
    def is_pong(jsonobject):
        """
        Function that analyzes the object, to see if it's a PONG message

        """
        try:
            return 'pong' in dict(jsonobject)
        except Exception as e:
            log.error(
                'Failed to analyze the {} object. Returned error - {}'.format(
                    jsonobject, e,
                ),
            )
            raise e

    @staticmethod
    def is_error(jsonobject):
        """
        Function that analyzes the object, to see if it's a ERROR message

        """
        try:
            return 'error' in dict(jsonobject)
        except Exception as e:
            log.error(
                'Failed to analyze the {} object. Returned error - {}'.format(
                    jsonobject, e,
                ),
            )
            raise e

    @staticmethod
    def is_producterror(jsonobject):
        """
        Function that analyzes the object, to see if it's a ERROR message

        """
        try:
            if 'event' in dict(jsonobject):
                if 'product_event' in jsonobject['event']:
                    if 'product_error_event' in jsonobject['event']['product_event']:
                        return True

            return False
        except Exception as e:
            log.error(
                'Failed to analyze the {} object. Returned error - {}'.format(
                    jsonobject, e,
                ),
            )
            raise e

    @staticmethod
    def is_event(jsonobject):
        """
        Function that analyzes the object, to see if it's a EVENT message

        """
        try:
            return 'event' in dict(jsonobject)
        except Exception as e:
            log.error(
                'Failed to analyze the {} object. Returned error - {}'.format(
                    jsonobject, e,
                ),
            )
            raise e

    @classmethod
    def parse_logisync_protobuf_response(cls, msg):
        log.debug('parse_protobuf_response started')
        try:
            syncMessage = transport.LogiSyncMessage()
            syncMessage.ParseFromString(bytes(msg))
            log.debug('Parsed sync response -\n {}'.format(syncMessage))
            if syncMessage is not None:
                return cls.convert_protobuf_to_json(syncMessage)
            else:
                log.error('Empty Response from protobuf')
                return None
        except Exception as e:
            raise e

    @property
    def create_transport_header(self):
        """
        Create the transport header for the message based on defined protobuf api.
        The header includes the timestamp and GUID.

        .. code-block:: python

           Format:
           {
           timestamp: 1541718204662.0
           guid: "1"
           }

        :return: transport request header
        """
        try:
            req_header = transport.Header()
            req_header.timestamp = time.time()
            req_header.guid = str(randint(1, 10))
            req_header.user_context = "SYNC-QA-50161F9F-DDC1-49E5-BD47-C7BB8BBE37D6"
            return req_header
        except Exception as e:
            log.error('Failed to create transport header {}'.format(e))
            raise e

    @property
    def create_logisync_message_header(self):
        """
        Create the message header for the protobuf message. This header shall
        include the transport message header and a GUID.

        .. code-block:: python

           Format:
           {
           timestamp: 1541718204662.0
           guid: "1"
           }

        :return: message header
        """
        try:
            log.debug('Generating Protobuf message header')
            message = transport.LogiSyncMessage()
            message.header.CopyFrom(self.create_transport_header)
            return message
        except Exception as e:
            log.error('Failed to create protobuf message header {}'.format(e))
            raise e

    @staticmethod
    def serialize_request(request):
        """
        Converts the message to a buffer

        :param request:
        :return: msg_buffer:

        """
        try:
            msg_buffer = []
            message = request.SerializeToString()
            message_as_list = list(message)
            msg_buffer.append(message_as_list)
            return msg_buffer
        except Exception as e:
            log.error(
                "Failed to update the request's first byte: {}".format(e),
            )
            raise e

    @classmethod
    def validate_disconnect_event(cls, event_data):
        """
        Validate the disconnection event

        :param event_data:
        :return:

        """
        log.debug('validate_disconnect_event started')
        try:
            if 'productUuid' in event_data:
                assert event_data['productUuid'] is not None, 'uuid Field is Unavailable'
                return True
            else:
                return False
        except Exception as e:
            raise e

    @classmethod
    def validate_connect_event(cls, event_data):
        """
        Validate the connection event

        :param event_data:
        :return:

        """
        log.debug('validate_connect_event started')
        try:
            if 'product' in event_data:
                _events = event_data['product']
                log.info('_events - {}'.format(_events))
                assert _events['devices'] is not None, 'Device Field is Unavailable'
                assert _events['uuid'] is not None, 'uuid Field is Unavailable'
                assert _events['model'] is not None, 'model Field is Unavailable'
                assert _events['name'] is not None, 'name Field is Unavailable'
                return True
        except Exception as e:
            raise e

    @property
    def create_raiden_message_header(self):
        """
        Create the Cloud LogiRaidenMessage mheader for the protobuf message.
        This header shall include the transport message , Header {timestamp: 1541718204662.0, guid: "1"},
        internal_api_id, source

        :return: message header

        """
        try:
            log.debug('create cloud message header - LogiRaidenMessage')
            message = cloud_msg.LogiRaidenMessage()
            message.header.CopyFrom(self.create_transport_header)
            message.internal_api_id = INTERNAL_API_ID
            message.source = SOURCE_PROXY
            return message
        except Exception as e:
            log.error('Failed to create_raiden_message_header {}'.format(e))
            raise e

    @property
    def create_lr_request(self):
        """
        Create the Cloud LRRequest message header for the protobuf message.

        :return: message header

        """
        try:
            log.debug('create cloud message header - LRRequest')
            message = cloud_msg.LRRequest()
            return message
        except Exception as e:
            log.error('Failed to create protobuf message header {}'.format(e))
            raise e

    @classmethod
    def parse_raiden_protobuf_response(cls, msg):
        log.debug('parse_raiden_protobuf_events started')
        try:
            raidenMessage = cloud_msg.LogiRaidenMessage()
            raidenMessage.ParseFromString(bytes(msg))
            log.debug('Parsed message into Raiden - {}'.format(raidenMessage))
            if raidenMessage is not None:
                return cls.convert_protobuf_to_json(raidenMessage)
            else:
                log.error('Empty Response from protobuf')
                return None
        except Exception as e:
            log.error('Exception Response from protobuf {}'.format(e))
            raise e
