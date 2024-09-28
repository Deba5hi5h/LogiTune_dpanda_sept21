import asyncio
import json
import sys
import unittest
import logging
import time

from common.config import DeviceModelConfig
from apis.sync_api.devicesettingsrequest import DeviceSettingsRequest
from base.sync_base_api import SyncBaseAPI
from apis.sync_helper import SyncHelper
import apis.process_helper as process_helper
import common.log_helper as log_helper
from common import framework_params as fp
from apis.sync_api.websocketconnection import WebsocketConnection
from extentreport.report import Report

log = logging.getLogger(__name__)


class LogiSyncDeviceSettingsAPI(SyncBaseAPI):
    """
     Tests to verify device settings API

    """

    @classmethod
    def setUpClass(cls):
        try:
            super(LogiSyncDeviceSettingsAPI, cls).setUpClass()
            cls.sync = SyncHelper()
            sync_version = cls.sync.get_logisync_version()
            log.info('Sync App version is: {}'.format(sync_version))

            cls.loop = asyncio.get_event_loop()
            if not process_helper.check_sync_service_status():
                log.error('Please start the sync service to execute test-suite')
                raise AssertionError('Sync Service not running')

        except Exception as e:
            log.error('Unable to setup the logisync Test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(LogiSyncDeviceSettingsAPI, cls).tearDownClass()

    def setUp(self):
        super(LogiSyncDeviceSettingsAPI, self).setUp()  # Extent Report
        log.info('Starting {}'.format(self._testMethodName))
        self.websocket_dict = {'type': 'LogiSync', 'timeout': 60.0}

    def tearDown(self):
        super(LogiSyncDeviceSettingsAPI, self).tearDown() #Extent Report

    @unittest.skip("Waiting for response from DEV team. Method returns nothing when changing brightness on TAP.")
    def test_001_setDeviceDisplayConfigurationRequest(self):
        """By sending this message, the client requests setting the device’s display-related configuration parameters.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetDeviceDisplayConfigurationRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('Get all products attached to host via Sync App.')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_device_display_configuration(
                device_uuid=self.product_uuid['TAP'],
                product_model=DeviceModelConfig.model_tap,
                brightness=0)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            product_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_display_config_data = json.dumps(product_data, indent=2)
            log.debug('Device Settings API - SetDeviceDisplayConfigurationRequest : {}'.
                      format(json_formatted_display_config_data))
            Report.logResponse(format(json_formatted_display_config_data))

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_002_VC_43251_RallyBar_setAudioNoiseReductionRequest_off(self):
        """SetAudioNoiseReductionRequest

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetAudioNoiseReductionRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioNoiseReductionRequest: Disable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_noise_reduction = 'DISABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_noise_reduction_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                noise_reduction=audio_noise_reduction)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioNoiseReductionRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioNoiseReductionResponse']

            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioNoiseReductionResponse(response_data,
                                                                            noise_reduction=audio_noise_reduction)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                )
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_003_VC_43252_RallyBar_setAudioNoiseReductionRequest_on(self):
        """SetAudioNoiseReductionRequest

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. One or more monitored or managed devices have to be connected to system

            Test:
                 1. Create a protobuf API request: SetAudioNoiseReductionRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioNoiseReductionRequest: Enable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_noise_reduction = 'ENABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_noise_reduction_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                noise_reduction=audio_noise_reduction)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioNoiseReductionRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioNoiseReductionResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioNoiseReductionResponse(response_data,
                                                                            noise_reduction=audio_noise_reduction)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_004_VC_43254_RallyBar_setAudioSpeakerBoostRequest_on(self):
        """SetAudioSpeakerBoostRequest : On

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar along with a micpod is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioSpeakerBoostRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioSpeakerBoostRequest: Enable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_speaker_boost = 'ENABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_speaker_boost_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                speaker_boost=audio_speaker_boost)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioSpeakerBoostRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioSpeakerBoostResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioSpeakerBoostResponse(response_data, speaker_boost=audio_speaker_boost)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_005_VC_43253_RallyBar_setAudioSpeakerBoostRequest_off(self):
        """SetAudioSpeakerBoostRequest : Off

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar along with a micpod is connected to host system.
            Test:
                 1. Create a protobuf API request: SetAudioSpeakerBoostRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioSpeakerBoostRequest: Disable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_speaker_boost = 'DISABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_speaker_boost_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                speaker_boost=audio_speaker_boost)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioSpeakerBoostRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioSpeakerBoostResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioSpeakerBoostResponse(response_data, speaker_boost=audio_speaker_boost)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                )
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_006_VC_43256_RallyBar_setAudioReverbModeRequest_aggressive(self):
        """setAudioReverbModeRequest : Aggressive

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest: Aggressive
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Aggressive, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'AGGRESSIVE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_007_VC_43257_RallyBar_setAudioReverbModeRequest_disabled(self):
        """setAudioReverbModeRequest : Disabled

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest: Disabled.
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Disabled, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'DISABLED'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_008_VC_43255_RallyBar_setAudioReverbModeRequest_normal(self):
        """setAudioReverbModeRequest : Normal

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Normal, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'NORMAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR'],
                product_model=DeviceModelConfig.model_rally_bar,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_101_VC_43928_RallyBarMini_setAudioNoiseReductionRequest_off(self):
        """SetAudioNoiseReductionRequest: Turn off AI Noise suppression for Rally Bar Mini

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Rally Bar Mini has to be connected to system

            Test:
                 1. Create a protobuf API request: SetAudioNoiseReductionRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioNoiseReductionRequest: Disable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_noise_reduction = 'DISABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_noise_reduction_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                noise_reduction=audio_noise_reduction)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioNoiseReductionRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioNoiseReductionResponse']

            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioNoiseReductionResponse(response_data,
                                                                            noise_reduction=audio_noise_reduction)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                )
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_102_VC_43929_RallyBarMini_setAudioNoiseReductionRequest_on(self):
        """SetAudioNoiseReductionRequest: Turn on AI Noise suppressoin for Rally Bar Mini

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Rally Bar Mini has to be connected to system

            Test:
                 1. Create a protobuf API request: SetAudioNoiseReductionRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioNoiseReductionRequest: Enable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_noise_reduction = 'ENABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_noise_reduction_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                noise_reduction=audio_noise_reduction)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioNoiseReductionRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioNoiseReductionResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioNoiseReductionResponse(response_data,
                                                                            noise_reduction=audio_noise_reduction)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_103_VC_43931_RallyBarMini_setAudioSpeakerBoostRequest_on(self):
        """SetAudioSpeakerBoostRequest : On for Rally Bar Mini.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar Mini along with a micpod is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioSpeakerBoostRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioSpeakerBoostRequest: Enable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_speaker_boost = 'ENABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_speaker_boost_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                speaker_boost=audio_speaker_boost)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioSpeakerBoostRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioSpeakerBoostResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioSpeakerBoostResponse(response_data,
                                                                          speaker_boost=audio_speaker_boost)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_104_VC_43932_RallyBarMini_setAudioSpeakerBoostRequest_off(self):
        """SetAudioSpeakerBoostRequest : Off for Rally Bar Mini.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar Mini along with a micpod is connected to host system.
            Test:
                 1. Create a protobuf API request: SetAudioSpeakerBoostRequest.
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioSpeakerBoostRequest: Disable, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_speaker_boost = 'DISABLE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_speaker_boost_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                speaker_boost=audio_speaker_boost)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioSpeakerBoostRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioSpeakerBoostResponse']
            if "errors" not in response_data:
                status = SyncHelper.validate_setAudioSpeakerBoostResponse(response_data,
                                                                          speaker_boost=audio_speaker_boost)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                )
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_105_VC_43934_RallyBarMini_setAudioReverbModeRequest_aggressive(self):
        """SetAudioReverbModeRequest : Aggressive for Rally Bar Mini

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar Mini is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest: Aggressive
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Aggressive, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'AGGRESSIVE'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_106_VC_43935_RallyBarMini_setAudioReverbModeRequest_disabled(self):
        """SetAudioReverbModeRequest : Disabled for Rally Bar Mini

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar Mini is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest: Disabled.
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Disabled, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'DISABLED'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_107_VC_43936_RallyBarMini_setAudioReverbModeRequest_normal(self):
        """SetAudioReverbModeRequest : Normal for Rally Bar Mini.

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Rally Bar Mini is connected to host system.

            Test:
                 1. Create a protobuf API request: SetAudioReverbModeRequest
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetAudioReverbModeRequest: Normal, Data Structure: AudioSettings')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            audio_reverb_mode = 'NORMAL'

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_audio_reverb_mode_request(
                product_uuid=self.product_uuid['RALLY_BAR_MINI'],
                product_model=DeviceModelConfig.model_rally_bar_mini,
                reverb_mode=audio_reverb_mode)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_audio_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetAudioReverbModeRequest : {}'.
                      format(json_formatted_audio_data))
            Report.logResponse(format(json_formatted_audio_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setAudioReverbModeResponse']
            if 'errors' not in response_data:
                status = SyncHelper.validate_setAudioReverbModeResponse(response_data, reverb_mode=audio_reverb_mode)
            else:
                log.info('Request got timed out. Sync Agent will re-send another request and update the setting.')
                status = SyncHelper.validate_error_audio_settings(response_data)

            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_201_VC_43259_Scribe_setDeviceWhiteboardConfigurationRequest(self):
        """SetDeviceWhiteboardConfigurationRequest : Enabled Image Enhancement and Full Presenter Removal

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Scribe is connected to host system.

            Test:
                 1. Create a protobuf API request: SetDeviceWhiteboardConfigurationRequest: Enabled Image Enhancement and Ghosting.
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetDeviceWhiteboardConfigurationRequest : Enabled Image Enhancement and Ghosting')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            whiteboard_configuration = {'image_enhancement': True, 'ghosting': True}

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_device_whiteboard_configuration_request(
                product_uuid=self.product_uuid['SCRIBE'],
                product_model=DeviceModelConfig.model_scribe,
                whiteboard_configuration=whiteboard_configuration)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            whiteboard_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_whiteboard_data = json.dumps(whiteboard_settings_data, indent=2)
            log.debug('Device Settings API - SetDeviceWhiteboardConfigurationRequest : {}'.
                      format(json_formatted_whiteboard_data))
            Report.logResponse(format(json_formatted_whiteboard_data))

            # Validate the response.
            response_data = whiteboard_settings_data['response']['deviceSettingsResponse']['setDeviceWhiteboardConfigurationResponse']
            status = SyncHelper.validate_setDeviceWhiteboardConfigurationResponse(response_data, whiteboard_configuration)
            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')

    def test_202_VC_43260_Scribe_setDeviceWhiteboardEditBoundariesRequest(self):
        """SetDeviceWhiteboardEditBoundariesRequest : Enable

            Setup:
                  1. LogiSync Application should be running on the host
                  2. The services LogisyncMiddleware, LogisyncProxy, LogisyncHandler should be running
                  3. Make sure Scribe is connected to host system.

            Test:
                 1. Create a protobuf API request: SetDeviceWhiteboardEditBoundariesRequest: Enable
                 2. Send this to the proxy server via a websocket connection.
                 3. Receive the response.
        """
        try:
            self.banner('SetDeviceWhiteboardEditBoundariesRequest : Enable')
            # Create configuration request object
            product_request = DeviceSettingsRequest()
            log.debug('Device Settings request {}'.format(product_request))

            ENABLED = True

            # Generate the request message
            self.websocket_dict['msg_buffer'] = product_request.create_set_device_whiteboard_edit_boundaries_request(
                product_uuid=self.product_uuid['SCRIBE'],
                product_model=DeviceModelConfig.model_scribe,
                enabled=ENABLED)

            log.debug('Web socket dictionary - {}'.format(self.websocket_dict))

            # Send request to proxy server via a web socket connection
            websocket_con = WebsocketConnection(self.websocket_dict)

            time.sleep(5)

            # Get the response
            audio_settings_data = self.loop.run_until_complete(websocket_con.request_response_listener())
            json_formatted_whiteboard_data = json.dumps(audio_settings_data, indent=2)
            log.debug('Device Settings API - SetDeviceWhiteboardEditBoundariesRequest : {}'.
                      format(json_formatted_whiteboard_data))
            Report.logResponse(format(json_formatted_whiteboard_data))

            # Validate the response.
            response_data = audio_settings_data['response']['deviceSettingsResponse']['setDeviceWhiteboardEditBoundariesResponse']
            status = SyncHelper.validate_setDeviceWhiteboardEditBoundariesResponse(response_data)
            log.info(
                'Response data - {}'.format(
                    response_data
                ),
            )
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e
        except Exception as exc:
            Report.logException(f'{exc}')


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(LogiSyncDeviceSettingsAPI)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")