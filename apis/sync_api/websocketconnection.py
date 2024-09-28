"""
:Module Name: **websocketconnection**

===============================

This module handles the Interface between python App and Proxy Server
This performs Sending the Protobuf headers and receiving the response OK messages

WebSockets
WebSockets is a fairly new protocol that provides a thin layer of abstraction over TCP allowing for asynchronous, bidirectional communication between client and server.
The WebSockets protocol was designed to solve the problem of web browser applications having to kluge together solutions to simulate real-time communication with a server
such as employing excessive server polling or opening multiple HTTP connections. Additionally, because WebSockets are just a thin abstraction layer over TCP, basically any
type of data can be sent over it.

Refer - https://docs.google.com/document/d/1ajoZDq5C640I2cqDzHxEHNeMNjzVSU8jYY9c89Nac-k/edit#heading=h.lfzxaut69wa7
"""
import asyncio
import aiohttp
import logging
import time
from apis.sync_api.protobuf_helper import ProtobufUtils
from apis.sync_api.sync_eventhandler import SyncEventHandler
import common.config as config

log = logging.getLogger(__name__)

class WS_SessionManager:
    """
    WS Session Manager manages the AIOHTTP Session including connection & disconnection of
    session for any Protobuf request, response and events

    """
    def __init__(self):
        self._session = None

    def __call__(self, fn, *args, **kwargs):
        """
        Handling the aiohttp_session decorator

        :param fn:
        :param args:
        :param kwargs:
        :return:
        """
        if asyncio.iscoroutinefunction(fn):
            async def aiohttp_session(*args, **kwargs):
                response = None
                try:
                    log.info("Aiohttp Client WS Session Established")
                    # First interface for making HTTP requests.
                    async with aiohttp.ClientSession() as self._session:
                        # Initiate websocket connection.
                        async with self._session.ws_connect(config.URL, verify_ssl=False) as ws:
                            kwargs['ws'] = ws
                            response = await fn(*args, **kwargs)
                except Exception as e:
                    log.error("Error aiohttp_session - {}".format(e))
                finally:
                    await self._session.close()
                    self._session = None
                    log.info("Websocket session is terminated")
                    return response

            return aiohttp_session

    def __del__(self):
        if self._session:
            self._session.close()
            self._session = None
            log.info("WS_SessionManager Disconnected")


class WebsocketConnection:
    """
    WebSocket Connection Class that handles Events, Request/Response & Pong messages from proxy Server

    """

    def __init__(self, ws_dict: dict):
        """
        init method for websocket connection class

        :param ws_dict:
        """
        try:
            self.msg_buffer = ws_dict.get("msg_buffer")
            self.type = ws_dict.get("type")
            self.event_list = ws_dict.get("event_list")
            self.timeout = ws_dict.get("timeout")
            self.no_wait_flag = ws_dict.get("no_wait_flag")

            assert self.type, "Websocket Type is mandatory Field"
            assert self.timeout, "Websocket Timeout is mandatory Field"

            self.eventobj = SyncEventHandler()
            # Adding a response of LogiSync_raiden type to fetch both type of
            # response
            self._parse_message = {
                "LogiSync": ProtobufUtils.parse_logisync_protobuf_response,
                "Raiden": ProtobufUtils.parse_raiden_protobuf_response
            }
        except Exception as e:
            log.error("Websocket Dict Error - {}".format(e))
            raise e

    def __del__(self):
        del self.msg_buffer, self.event_list, self.timeout

    @WS_SessionManager()
    async def request_response_listener(self, ws):
        """
        Send to Proxy Server and waits for the response

        :return:
        """
        protobuf_data = None
        _wait_time = float(time.time()) + self.timeout
        try:
            while float(time.time()) <= _wait_time:
                for message in self.msg_buffer:
                    ba = bytes(message)
                    await asyncio.sleep(1)
                    await ws.send_bytes(ba)

                    log.info("Sending {} Request Message".format(self.type))

                    # Dont wait for response if below flag is set
                    # Send the request & come out from loop
                    if not self.no_wait_flag:
                        protobuf_data = await self._get_response(ws)

                    return protobuf_data

            return protobuf_data

        except Exception as e:
            log.error(e)
            raise e

    @WS_SessionManager()
    async def event_listener(self, ws):
        """
        Method that listens to the events and parse the expected events

        :return:
        """
        _wait_time = float(time.time()) + self.timeout
        protobuf_data = None
        try:
            # Validate if event list is not empty & Timeout
            while (float(time.time()) < _wait_time) and self.event_list:

                _data = await ws.receive()

                # Decode the response, and check to see if it is a Pong message
                protobuf_data = self._parse_message[self.type](_data.data)

                # Check if we received events from the event list that we are looking for.
                event_name, final_event_flag = self.eventobj.handle_protobuf_events(protobuf_data, self.event_list)

                # Remove the received events from event_list
                if event_name in self.event_list:
                    log.info("Removing {} from List".format(event_name))
                    self.event_list.remove(event_name)

                    if final_event_flag:
                        log.warning("SKIPPING EVENTS- {}".format(self.event_list))
                        self.event_list.clear()
                        log.warning("Clearing All Events")

                log.info("Looking for events - {}".format(self.event_list))

            return protobuf_data

        except Exception as e:
            log.error(e)
            raise e

    async def _get_response(self, ws_handle):
        """
        Checking the LogiSync response from the proxy server

        :param ws_handle:
        :return protobuf_data:
        """
        log.info("Waiting for the Logisync response")
        try:
            _wait_time = float(time.time()) + self.timeout
            _is_pong, _is_event, protobuf_data = True, True, None
            while (_is_pong or _is_event) and float(time.time()) <= _wait_time:
                response = await ws_handle.receive()
                log.info("Received {} response from Proxy Server".format(self.type))

                # Decode the response, and check to see if it is a Pong message
                protobuf_data = self._parse_message[self.type](response.data)
                _is_pong = ProtobufUtils.is_pong(protobuf_data)
                _is_event = ProtobufUtils.is_event(protobuf_data)

                if protobuf_data and not (_is_pong or _is_event):
                    return protobuf_data

            return protobuf_data
        except Exception as e:
            log.error(e)
            raise e