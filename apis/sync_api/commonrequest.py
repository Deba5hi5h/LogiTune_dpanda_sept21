"""
:Module Name: **commonrequest**

==============================

A library that implements the common protobuf API.
All methods that are part of this API class can be defined here.

"""
import asyncio
import logging
import time

import common_pb2 as common
from apis.sync_api.protobuf_helper import ProtobufUtils
from apis.sync_api.websocketconnection import WebsocketConnection

log = logging.getLogger(__name__)


class CommonRequest:
    """
        This class implements the Common protobuf API.
    """
    def __init__(self):
        self.proto_buf = ProtobufUtils()
        self.loop = asyncio.get_event_loop()

    def get_proto_version_request(self):
        """
            Method to create a protobuf request to get proto version
        :return: msg_buffer
        """

        try:
            log.debug(
                'Preparing to get ProtoVersionRequest',
            )

            logisync_message = self.proto_buf.create_logisync_message_header

            sync_agent_request = common.ProtoVersionRequest()

            logisync_message.request.proto_version_request.CopyFrom(sync_agent_request)

            msg_buffer = self.proto_buf.serialize_request(logisync_message)
            log.info(
                'Proto Version Request - Message Request - {}'.format(
                    msg_buffer
                ),
            )
            return msg_buffer

        except Exception as e:
            log.error('ProtoVersionRequest Failed {}'.format(e))
            raise e

    def proto_version_response(self):
        """
        Get the proto version.
        """
        try:
            log.debug(
                'Preparing to get ProtoVersionResponse',
            )

            self.websocket_dict = {'type': 'LogiSync', 'timeout': 100.0}

            common_req = CommonRequest()
            # Generate the request message
            self.websocket_dict['msg_buffer'] = common_req.get_proto_version_request()

            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            proto_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            print(proto_data)

        except Exception as e:
            log.error('ProtoVersionResponse Failed {}'.format(e))
            raise e

