"""
:Module Name: **Sync helper**

====================================

Contains helper files for sync test cases.
"""

import logging
import apis.helper as helper
import re
import os
import common.config as config
import sys
import apis.process_helper as process_helper
from extentreport.report import Report

log = logging.getLogger(__name__)

if sys.platform.startswith('win'):
    from win32api import GetFileVersionInfo, LOWORD, HIWORD


class SyncHelper(object):
    """
    Contains sync helper methods.
    """
    
    def __init__(self):
        pass

    @staticmethod
    def get_logisync_version():
        """
        Get logi sync version for the provided operating system.
        :return: ``Version Info``
        :rtype: ``string``
        """
        version = None
        try:
            platform = helper.get_name_of_os()
            if platform is 'windows':
                version = SyncHelper.get_windows_sync_version()
            elif platform is 'macos':
                version = SyncHelper.get_mac_sync_version()
            else:
                log.error('Platform Not Supported')
            # checked added Logisync software version if it is in format
            # [a.b.c.d] then it will be trimmed to version [a.b.c]
            check_version = re.match(r'^\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}$', version)
            if check_version:
                version = '.'.join(version.split('.')[:-1])
            return version

        except Exception as exp_err:
            log.error('Exception is %s' % exp_err)
            raise exp_err

    @staticmethod
    def get_file_version_number_windows(filename):
        """
        method to get file version number in windows

        """
        try:
            info = GetFileVersionInfo(filename, '\\')
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)

        except Exception as e:
            log.error('Error found {}'.format(e))
            raise Exception('Unknown version for file : {}'.format(filename))

    @staticmethod
    def get_windows_sync_version():
        '''
        Method to get the LogiSync Software version on windows.

        :return: ``Version Info``
        :rtype: ``string``
        '''
        try:
            version = None

            if os.path.exists(config.LOGISYNC_WINDOWSx86_PATH):
                version = '.'.join([str(i) for i in
                                    SyncHelper.get_file_version_number_windows(
                                        config.LOGISYNC_WINDOWSx86_PATH,
                                    )])
            elif os.path.exists(config.LOGISYNC_WINDOWS_PATH):
                version = '.'.join([str(i) for i in
                                    SyncHelper.get_file_version_number_windows(
                                        config.LOGISYNC_WINDOWS_PATH,
                                    )])
            else:
                log.error(
                    'Either LogiSync Software is not installed or installed in a different configured path',
                )
            return version

        except Exception as e:
            log.error('Error is %s', e)
            raise e

    @staticmethod
    def parse_mac_sync_version(output):
        """
        Parse the logisync app version from output.
        :param output:
        :return:
        """
        try:
            return str(output).split('= ')[1].split('\\')[0]

        except Exception as e:
            log.error('Error is %s', e)
            raise e

    @staticmethod
    def get_mac_sync_version():
        """
        Method to get the LogiSync Software version using command line.

        """
        try:
            (p_out, command_output, command_error) = \
                process_helper.execute_command(config.MAC_LOGISYNC_VERSION)

            if "could not find" in str(command_output).replace('\n', ' '):
                return "None"
            else:
                sync_version = SyncHelper.parse_mac_sync_version(
                    command_output,
                )
                return sync_version

        except Exception as except_err:
            log.error('Error is %s', except_err)
            raise except_err

    @staticmethod
    def validate_get_all_products_response(product_response):
        """
        Products are connected to host during initial setup. Validate that the response contains the product details.
        """
        try:
            flag = 0
            if 'products' in product_response:
                total_products = len(product_response['products'])
                log.info('Product Response: {}'.format(product_response['products']))
                if total_products >= 1:
                    log.info('Number of Products: {}'.format(total_products))
                    for product_index in range(total_products):
                        if product_response['products'][product_index]:
                            Report.logPass('Received Product Details - {}'.format(product_response['products'][product_index]))
                        else:
                            Report.logFail('Error in Product details')
                        log.info('Name of Product: {}'.format(product_response['products'][product_index]['name']))
                        log.info('Product Details: {}'.format(product_response['products'][product_index]))

                        product = product_response['products'][product_index]
                        product_attributes = ['uuid', 'model', 'name', 'devices', 'connectionState', 'updateState', 'scheduledUpdate']
                        for attribute in product_attributes:
                            if attribute in product:
                                Report.logPass('Received attribute - {}'.format(attribute))
                            else:
                                Report.logFail('Error in the attribute - {}'.format(attribute))
                            assert attribute in product, 'Error in {} field'.format(attribute)
                    flag = 1
            else:
                Report.logFail(f"Products are not returned in response")
                assert product_response, 'Product response is empty'
            return True if flag == 1 else False

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_get_configuration_response(conf_response):
        """
        Validate the response that we receive from getHostInformation API
        example response: {1 : "", 2: "SyncNAme", 3: "", 4 : ""}
        """
        try:
            conf_response = {int(k): v for k, v in conf_response.items()}
            if 1 in conf_response:
                Report.logPass(f'Received COLLECTING ANALYTICS field {conf_response[1]}')
            else:
                Report.logFail('Error in COLLECTING_ANALYTICS field')
            if 2 in conf_response:
                Report.logPass(f'Received ROOM_NAME field {conf_response[2]}')
            else:
                Report.logFail('Error in ROOM_NAME field')
            if 3 in conf_response:
                Report.logPass(f'Received EULA_ACCEPTED field {conf_response[3]}')
            else:
                Report.logFail('Error in EULA_ACCEPTED field')
            if 4 in conf_response:
                Report.logPass(f'Received ORGANIZATION_NAME field {conf_response[4]}')
            else:
                Report.logFail('Error in ORGANIZATION_NAME field')

            assert 1 in conf_response, 'Error in COLLECTING_ANALYTICS'
            assert conf_response[2] is not None, 'Error in ROOM_NAME'
            assert 3 in conf_response, 'Error in EULA_ACCEPTED'
            assert 4 in conf_response, 'Error in ORGANIZATION_NAME'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_restore_configuration_response(conf_base, conf_response):
        """
        Validate the response that we receive from getHostInformation API
        example response: {1 : "", 2: "SyncNAme", 3: "", 4 : ""}
        """
        try:
            log.debug('len(conf_response) {}'.format(len(conf_response)))
            log.debug('len(conf_base) {}'.format(len(conf_base)))
            assert len(conf_response) == len(conf_base), 'Response config is different than base config'

            if 1 in conf_base:
                assert conf_response[1] == conf_base[1], 'Error in COLLECTING_ANALYTICS'
            if 2 in conf_base:
                assert conf_response[2] == conf_base[2], 'Error in ROOM_NAME'
            if 3 in conf_base:
                assert conf_response[3] == conf_base[3], 'Error in EULA_ACCEPTED'
            if 4 in conf_base:
                assert conf_response[4] == conf_base[4], 'Error in ORGANIZATION_NAME'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_set_configuration_response(conf_base, conf_response):
        """
        Validate the response that we receive from getHostInformation API
        example response: {1 : "", 2: "SyncNAme", 3: "", 4 : ""}
        """
        try:
            log.debug('len(conf_response) {}'.format(len(conf_response)))
            log.debug('len(conf_base) {}'.format(len(conf_base)))
            assert len(conf_response) == len(conf_base), 'Response config is different than base config'

            if 1 in conf_base:
                if conf_response[1] == conf_base[1]:
                    Report.logPass('Received COLLECTING_ANALYTICS field')
                else:
                    Report.logFail('Error in COLLECTING_ANALYTICS')
                assert conf_response[1] == conf_base[1], 'Error in COLLECTING_ANALYTICS'

            if 2 in conf_base:
                if conf_response[2] == conf_base[2]:
                    Report.logPass('Received ROOM_NAME field')
                else:
                    Report.logFail('Error in ROOM_NAME')
                assert conf_response[2] == conf_base[2], 'Error in ROOM_NAME'

            if 3 in conf_base:
                if conf_response[3] == conf_base[3]:
                    Report.logPass('Received EULA_ACCEPTED field')
                else:
                    Report.logFail('Error in EULA_ACCEPTED')
                assert conf_response[3] == conf_base[3], 'Error in EULA_ACCEPTED'

            if 4 in conf_base:
                if conf_response[4] == conf_base[4]:
                    Report.logPass('Received ORGANIZATION_NAME field')
                else:
                    Report.logFail('Error in ORGANIZATION_NAME')
                assert conf_response[4] == conf_base[4], 'Error in ORGANIZATION_NAME'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_get_host_information_response(host_inf_response):
        """
        Validate the response that we receive from getHostInformation API
        """
        try:
            if host_inf_response['hardwareModel']:
                Report.logPass('Received hardwareModel field - {}'.format(host_inf_response['hardwareModel']))
            else:
                Report.logFail('Error in hardwareModel field')
            if host_inf_response['operatingSystemName']:
                Report.logPass('Received operatingSystemName field - {}'.format(host_inf_response['operatingSystemName']))
            else:
                Report.logFail('Error in operatingSystemName field')
            if host_inf_response['operatingSystemVersion']:
                Report.logPass('Received operatingSystemVersion field - {}'.format(host_inf_response['operatingSystemVersion']))
            else:
                Report.logFail('Error in operatingSystemVersion field')
            if host_inf_response['processor']:
                Report.logPass('Received processor field - {}'.format(host_inf_response['processor']))
            else:
                Report.logFail('Error in processor field')
            if host_inf_response['memory']:
                Report.logPass('Received memory field - {}'.format(host_inf_response['memory']))
            else:
                Report.logFail('Error in memory field')
            if host_inf_response['hostName']:
                Report.logPass('Received hostName field - {}'.format(host_inf_response['hostName']))
            else:
                Report.logFail('Error in hostName field')
            if host_inf_response['roomName']:
                Report.logPass('Received roomName field - {}'.format(host_inf_response['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if host_inf_response['operatingSystemName']:
                Report.logPass('Received operatingSystemName field - {}'.format(host_inf_response['operatingSystemName']))
            else:
                Report.logFail('Error in syncVersion field')
            if host_inf_response['syncVersion']:
                Report.logPass('Received syncVersion field - {}'.format(host_inf_response['syncVersion']))
            else:
                Report.logFail('Error in syncProxyVersion field')
            if host_inf_response['syncMiddlewareVersion']:
                Report.logPass('Received syncMiddlewareVersion field - {}'.format(host_inf_response['syncMiddlewareVersion']))
            else:
                Report.logFail('Error in syncMiddlewareVersion field')
            if host_inf_response['syncHandlerVersion']:
                Report.logPass('Received syncHandlerVersion field - {}'.format(host_inf_response['syncHandlerVersion']))
            else:
                Report.logFail('Error in syncHandlerVersion field')

            assert host_inf_response['hardwareModel'] is not None, 'Error in hardware model'
            assert host_inf_response['operatingSystemName'] is not None, 'Error in OS name'
            assert host_inf_response['operatingSystemVersion'] is not None, 'Error in OS version'
            assert host_inf_response['processor'] is not None, 'Error in processor model'
            assert host_inf_response['memory'] is not None, 'Error in memory value'
            assert host_inf_response['hostName'] is not None, 'Error in host name'
            assert host_inf_response['roomName'] is not None, 'Error in room name'
            assert host_inf_response['syncVersion'] is not None, 'Error in sync Version'
            assert host_inf_response['syncProxyVersion'] is not None, 'Error in sync Proxy Version'
            assert host_inf_response['syncMiddlewareVersion'] is not None, 'Error in sync Middleware Version'
            assert host_inf_response['syncHandlerVersion'] is not None, 'Error in sync Handler Version'

            displays = host_inf_response['displays']
            if len(displays) >= 1:
                Report.logPass('Received length of connected displays - {}'.format(len(displays)))
            else:
                Report.logFail('Error in length of displays')
            assert len(displays) >= 1, 'Error in length of connected displays'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_response_product_by_id(product, DEVICE_TYPE):
        """
        Validate the response that we receive from
        """
        try:
            print('Product is {}'.format(product))
            if DEVICE_TYPE == 'MEETUP':
                if product['model']:
                    Report.logPass('Received product model field - {}'.format(product['model']))
                else:
                    Report.logFail('Error in product model field')
                if product['name']:
                    Report.logPass('Received product name field - {}'.format(product['name']))
                else:
                    Report.logFail('Error in product name field')
                if product['devices']:
                    Report.logPass('Received product devices field - {}'.format(product['devices']))
                else:
                    Report.logFail('Error in product devices field')

                assert product['model'] == 'MEETUP', 'Error in device model'
                assert product['name'] == 'MeetUp', 'Error in device name'
                assert product['devices'][0]['formFactor'] == 'MEETUP', 'Error in form factor'
                assert product['devices'][0]['information'] is not None, 'Error in information field'
                _fw_dict = product['devices'][0]['information']
                assert len(_fw_dict) >= 5, 'Error in length of firmware components'

            elif DEVICE_TYPE == 'RALLYCAMERA':
                if product['model']:
                    Report.logPass('Received product model field - {}'.format(product['model']))
                else:
                    Report.logFail('Error in product model field')
                if product['name']:
                    Report.logPass('Received product name field - {}'.format(product['name']))
                else:
                    Report.logFail('Error in product name field')
                if product['devices']:
                    Report.logPass('Received product devices field - {}'.format(product['devices']))
                else:
                    Report.logFail('Error in product devices field')

                assert product['model'] == 'RALLY_CAMERA', 'Error in device model'
                assert product['name'] == 'Rally Camera', 'Error in device name'
                assert product['devices'][0]['formFactor'] == 'RALLY_CAMERA', 'Error in form factor'
                assert product['devices'][0]['information'] is not None, 'Error in information field'
                _fw_dict = product['devices'][0]['information']
                assert len(_fw_dict) >= 3, 'Error in length of firmware components'

            elif DEVICE_TYPE == 'BRIO':
                if 'model' in product:
                    Report.logPass('Received product model field - {}'.format(product['model']))
                else:
                    Report.logFail('Error in product model field')
                if 'name' in product:
                    Report.logPass('Received product name field - {}'.format(product['name']))
                else:
                    Report.logFail('Error in product name field')
                if 'devices' in product:
                    Report.logPass('Received product devices field - {}'.format(product['devices']))
                else:
                    Report.logFail('Error in product devices field')

                assert product['name'] == 'Brio', 'Error in device name'
                assert product['devices'][0]['information'] is not None, 'Error in information field'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setAntiFlickerConfigurationResponse(product, anti_flicker_mode):
        """
        Validate the setAntiFlickerConfigurationResponse
        """
        try:
            if len(product['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(product['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(product['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(product['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(product['videoSettingsConfiguration']) > 0:
                Report.logPass('Received videoSettingsConfiguration field - {}'.format(product['videoSettingsConfiguration']))
            else:
                Report.logFail('Error in videoSettingsConfiguration field')
            if 'errors' not in product:
                Report.logPass('errors field not present')
            else:
                Report.logFail('errors field should not be present')

            assert product['productUuid'] is not None, 'Error in productUuid field'
            assert product['productModel'] is not None, 'Error in productModel field'
            assert product['videoSettingsConfiguration'] is not None, 'Error in videoSettingsConfiguration field'
            assert 'errors' not in product, 'errors field should not be present'

            if anti_flicker_mode == 'PAL':
                if product['videoSettingsConfiguration']['antiFlickerMode'] == 'PAL_50HZ':
                    Report.logPass('Anti-Flicker Mode is PAL')
                else:
                    Report.logFail('Anti-Flicker Mode is not PAL')
                assert product['videoSettingsConfiguration']['antiFlickerMode'] == 'PAL_50HZ', 'Error in antiFlickerMode field'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            Report.logFail('Key Error {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setRightSightConfigurationResponse(product, mode= None):
        """
        Validate the setRightSightConfigurationResponse.
        """
        try:
            if len(product['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(product['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(product['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(product['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(product['rightSightConfiguration']) > 0:
                Report.logPass('Received rightSightConfiguration field - {}'.format(product['rightSightConfiguration']))
            else:
                Report.logFail('Error in rightSightConfiguration field')

            assert product['productUuid'] is not None, 'Error in productUuid field'
            assert product['productModel'] is not None, 'Error in productModel field'
            assert product['rightSightConfiguration'] is not None, 'Error in videoSettingsConfiguration field'

            if mode == 'ON_CALL_START':
                if product['rightSightConfiguration']['mode'] == mode:
                    Report.logPass('RightSight Configuration ON_CALL_START Mode field correct')
                else:
                    Report.logFail('RightSight Configuration ON_CALL_START Mode field error')
                if product['rightSightConfiguration']['enabled'] == True:
                    Report.logPass('RightSight Configuration ON_CALL_START Enabled field True')
                else:
                    Report.logFail('RightSight Configuration ON_CALL_START Enabled field False')
                if product['rightSightConfiguration']['status'] == str("OK"):
                    Report.logPass('RightSight Configuration ON_CALL_START Status field OK')
                else:
                    Report.logFail('RightSight Configuration ON_CALL_START Status field Error')

                assert product['rightSightConfiguration']['mode'] == mode, 'Error in mode field'
                assert product['rightSightConfiguration']['enabled'] == True, 'Error in enabled field'
                assert product['rightSightConfiguration']['status'] == str("OK"), 'Error in status field'

            elif mode == 'DYNAMIC':
                if product['rightSightConfiguration']['enabled'] == True:
                    Report.logPass('RightSight Configuration DYNAMIC Enabled field True')
                else:
                    Report.logFail('RightSight Configuration DYNAMIC Enabled field False')
                if product['rightSightConfiguration']['status'] == str("OK"):
                    Report.logPass('RightSight Configuration DYNAMIC Status field OK')
                else:
                    Report.logFail('RightSight Configuration DYNAMIC Status field Error')

                assert product['rightSightConfiguration']['enabled'] == True, 'Error in enabled field'
                assert product['rightSightConfiguration']['status'] == str("OK"), 'Error in status field'

            else:
                if 'mode' not in product['rightSightConfiguration']:
                    Report.logPass('RightSight Configuration mode field not present')
                else:
                    Report.logFail('RightSight Configuration mode field should not be present')
                if 'enabled' not in product['rightSightConfiguration']:
                    Report.logPass('RightSight Configuration enabled field not present')
                else:
                    Report.logFail('RightSight Configuration enabled field should not be present')
                if product['rightSightConfiguration']['status'] == str("OK"):
                    Report.logPass('RightSight Configuration Status field OK')
                else:
                    Report.logFail('RightSight Configuration Status field Error')

                assert 'mode' not in product['rightSightConfiguration'], 'mode field should not be present'
                assert 'enabled' not in product['rightSightConfiguration'], 'enabled field should not be present'
                assert product['rightSightConfiguration']['status'] == str("OK"), 'Error in status field'

            return True

        except AssertionError as assert_err:
            Report.logFail('Assertion Error {}'.format(assert_err))
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            Report.logFail('Error {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_getProductConfigurationResponse(product):
        """
        Validate the getProductConfigurationResponse
        """
        try:
            if product['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(product['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if product['expectedDeviceCount']:
                Report.logPass('Received expectedDeviceCount field - {}'.format(product['expectedDeviceCount']))
            else:
                Report.logFail('Error in expectedDeviceCount field')
            if product['actualDeviceCount']:
                Report.logPass('Received actualDeviceCount field - {}'.format(product['actualDeviceCount']))
            else:
                Report.logFail('Error in actualDeviceCount field')
            if 'errors' not in product:
                Report.logPass('errors field is not present')
            else:
                Report.logFail('errors field should not be present')

            assert product['productUuid'] is not None, 'Error in productUuid field'
            assert product['expectedDeviceCount'] is not None, 'Error in expected_device_count field'
            assert product['actualDeviceCount'] is not None, 'Error in actual_device_count field'
            assert 'errors' not in product, 'errors field should not be present'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setProductConfigurationResponse(product_response, product_uuid, configuration_base):
        """
        Validate the setProductConfigurationResponse
        """
        try:
            if product_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(product_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field.')

            assert product_response['productUuid'] == product_uuid, 'Error in productUuid field'
            if len(configuration_base) > 0:
                for key, value in product_response['expectedDeviceCount'].items():
                    if value == configuration_base[key]:
                        Report.logPass('Valid expected device count - {}'.format(value))
                    else:
                        Report.logFail('Error in expected device count')
                    assert value == configuration_base[key], "Error in expected device count"
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_clearProductConfigurationResponse(product_response, product_uuid):
        """
        Validate the clearProductConfigurationResponse
        """
        try:
            if product_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(product_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field.')

            assert product_response['productUuid'] == product_uuid, 'Error in productUuid field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_forget_device_response(product_response, product_uuid, device_uuids=None):
        """
        Validate the ForgetDeviceResponse
        """
        try:
            if product_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(product_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(product_response['productUuid']))

            assert product_response['productUuid'] == product_uuid, 'Error in productUuid field'
            if device_uuids:
                if len(device_uuids) > 0:
                    for p_uuid in product_response['deviceUuids']:
                        if p_uuid in device_uuids:
                            Report.logPass('Forgotten device UUID is specified - {}'.format(p_uuid))
                        else:
                            Report.logFail('Forgotten device UUID was not specified')
                        assert p_uuid in device_uuids, 'Forgotten device UUID was not specified'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_send_product_reboot_response(product_response, product_uuid):
        """
        Validate the SendProductRebootResponse.
        """
        try:
            if product_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(product_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(product_response['productUuid']))

            if product_response['success'] == True:
                Report.logPass('Received success field - {}'.format(product_response['success']))
            else:
                Report.logFail('Error in success field - {}'.format(product_response['success']))

            assert product_response['productUuid'] == product_uuid, 'Error in productUuid field'
            assert product_response['success'] == True, 'Error in success field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_product_state_changed_event(product_event):
        """
        Validate the GetRoomInformationResponse
        """
        try:
            if product_event['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(product_event['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(product_event['productUuid']))
            if product_event['connectionState']:
                Report.logPass('Received connectionState field - {}'.format(product_event['connectionState']))
            else:
                Report.logFail('Error in connectionState field - {}'.format(product_event['connectionState']))

            assert product_event['productUuid'] is not None, 'Error in productUuid field'
            assert product_event['connectionState'] is not None, 'Error in connectionState field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_product_configuration_changed_event(product_event):
        """
        Validate the GetRoomInformationResponse
        """
        try:
            if product_event['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(product_event['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(product_event['productUuid']))
            if product_event['connectionState']:
                Report.logPass('Received connectionState field - {}'.format(product_event['connectionState']))
            else:
                Report.logFail('Error in connectionState field - {}'.format(product_event['connectionState']))

            assert product_event['productUuid'] is not None, 'Error in productUuid field'
            assert product_event['connectionState'] is not None, 'Error in connectionState field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_getInitRoomInfo(room):
        """
        Validate the getInitRoomInfo
        """
        try:
            assert room['roomInformation'] is not None, 'Error in roomInformation field'
            room_info = room['roomInformation']
            assert room_info['lastModified'] is not None, 'Error in lastModified field'
            assert room_info['roomName'] is not None, 'Error in roomName field'
            assert room_info['maxOccupancy'] is not None, 'Error in maxOccupancy field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_getRoomInformationResponse(room):
        """
        Validate the GetRoomInformationResponse
        """
        try:
            if len(room['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(room['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')

            assert room['roomInformation'] is not None, 'Error in roomInformation field'

            room_info = room['roomInformation']
            if room_info['lastModified']:
                Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
            else:
                Report.logFail('Error in lastModified field')
            if room_info['roomName']:
                Report.logPass(
                    'Received roomName field - {}'.format(room_info['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if room_info['maxOccupancy']:
                Report.logPass(
                    'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
            else:
                Report.logFail('Error in maxOccupancy field')

            assert room_info['lastModified'] is not None, 'Error in lastModified field'
            assert room_info['roomName'] is not None, 'Error in roomName field'
            assert room_info['maxOccupancy'] is not None, 'Error in maxOccupancy field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setRoomNameResponse(room, room_name):
        """
            Validate the SetRoomNameResponse
        """
        try:
            if len(room['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(room['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')

            assert room['roomInformation'] is not None, 'Error in roomInformation field'
            room_info = room['roomInformation']
            if room_info['lastModified']:
                Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
            else:
                Report.logFail('Error in lastModified field')
            if room_info['roomName']:
                Report.logPass(
                    'Received roomName field - {}'.format(room_info['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if room_info['maxOccupancy']:
                Report.logPass(
                    'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
            else:
                Report.logFail('Error in maxOccupancy field')

            assert room_info['lastModified'] is not None, 'Error in lastModified field'
            assert room_info['roomName'] == room_name, 'Error in roomName field'
            assert room_info['maxOccupancy'] is not None, 'Error in maxOccupancy field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setMaxOccupancyResponse(room, max_occupancy):
        """
            Validate the SetMaxOccupancyResponse
        """
        try:
            if len(room['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(room['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')
            assert room['roomInformation'] is not None, 'Error in roomInformation field'

            room_info = room['roomInformation']
            if room_info['lastModified']:
                Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
            else:
                Report.logFail('Error in lastModified field')
            if room_info['roomName']:
                Report.logPass(
                    'Received roomName field - {}'.format(room_info['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if room_info['maxOccupancy']:
                Report.logPass(
                    'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
            else:
                Report.logFail('Error in maxOccupancy field')
            assert room_info['lastModified'] is not None, 'Error in lastModified field'
            assert room_info['roomName'] is not None, 'Error in roomName field'
            assert room_info['maxOccupancy'] == max_occupancy, 'Error in maxOccupancy field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setRoomOccupancyModeResponse(room, mode):
        """
            Validate the SetRoomOccupancyModeResponse
        """
        try:
            if len(room['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(room['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')

            assert room['roomInformation'] is not None, 'Error in roomInformation field'
            room_info = room['roomInformation']
            if room_info['lastModified']:
                Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
            else:
                Report.logFail('Error in lastModified field')
            if room_info['roomName']:
                Report.logPass(
                    'Received roomName field - {}'.format(room_info['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if room_info['maxOccupancy']:
                Report.logPass(
                    'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
            else:
                Report.logFail('Error in maxOccupancy field')
            assert room_info['lastModified'] is not None, 'Error in lastModified field'
            assert room_info['roomName'] is not None, 'Error in roomName field'
            assert room_info['maxOccupancy'] is not None, 'Error in maxOccupancy field'
            if mode == 1:
                if room_info['roomOccupancyMode'] == str('ROOM_OCCUPANCY_MODE_ALWAYS_ON'):
                    Report.logPass('Room occupancy mode is always on')
                else:
                    Report.logFail('Error in room occupancy mode')

                assert room_info['roomOccupancyMode'] == str('ROOM_OCCUPANCY_MODE_ALWAYS_ON'), \
                    'Error in roomOccupancyMode field'
            elif mode == 2:
                if room_info['roomOccupancyMode'] == str('ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'):
                    Report.logPass('Room occupancy mode is meetings only')
                else:
                    Report.logFail('Error in room occupancy mode')
                assert room_info['roomOccupancyMode'] == str('ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'), \
                    'Error in roomOccupancyMode field'
            elif mode == 0:
                if 'roomOccupancyMode' not in room_info:
                    Report.logPass('roomOccupancyMode field is not present as expected.')
                else:
                    Report.logPass('roomOccupancyMode field should not be present.')
                assert 'roomOccupancyMode' not in room_info, 'roomOccupancyMode field should not be present'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setInitRoomInfo(room, room_inf, room_base=None):
        """
        Validate the setting of Initial Room Information.
        :param room:
        :param room_inf:
        :return:
        """
        # ROOM_OCCUPANCY_MODE_DISABLED -> 0 -> Room Occupancy feature disabled.
        # ROOM_OCCUPANCY_MODE_ALWAYS_ON -> 1 -> Room Occupancy counting enabled whether or not a meeting is active.
        # ROOM_OCCUPANCY_MODE_MEETINGS_ONLY -> 2 -> Room Occupancy counting enabled only when a
        # meeting is active
        try:
            assert room['roomInformation'] is not None, 'Error in roomInformation field'
            room_info = room['roomInformation']
            if len(room_inf) == 3:
                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                assert room_info['roomName'] == room_inf[0], 'Error in roomName field'
                assert room_info['maxOccupancy'] == int(room_inf[1]), 'Error in maxOccupancy field'
                # roomOccupancyMode attribute does not appear in response if the mode is disabled.
                if room_inf[2] == '1':
                    mode = 'ROOM_OCCUPANCY_MODE_ALWAYS_ON'
                    assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                elif room_inf[2] == '2':
                    mode = 'ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'
                    assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                elif room_inf[2] == '0':
                    assert 'roomOccupancyMode' not in room_info, 'roomOccupancyMode attribute should not be present'

            elif len(room_inf) == 0:
                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                assert room_info['roomName'] == room_base['roomName'], 'Error in roomName field'
                assert room_info['maxOccupancy'] == room_base['maxOccupancy'], 'Error in maxOccupancy field'
                assert room_info['roomOccupancyMode'] == room_base['roomOccupancyMode'], 'Error in roomOccupancy Mode'

            else:
                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                room_info = room['roomInformation']
                if 0 in room_inf:
                    assert room_info['roomName'] == room_inf[0], 'Error in room_name field'
                if 1 in room_inf:
                    assert room_info['maxOccupancy'] == int(room_inf[1]), 'Error in max_occupancy field'
                if 2 in room_inf:
                    if room_inf[2] == '1':
                        mode = 'ROOM_OCCUPANCY_MODE_ALWAYS_ON'
                        assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                    elif room_inf[2] == '2':
                        mode = 'ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'
                        assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                    elif room_inf[2] == '0':
                        assert 'roomOccupancyMode' not in room_info, 'roomOccupancyMode attribute should not be present'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_bulkSetRoomInformationRequest(room, room_inf, room_base= None):
        """
        Validate the BulkSetRoomInformationRequest
        :param room:
        :param room_inf:
        :return:
        """
        # ROOM_OCCUPANCY_MODE_DISABLED -> 0 -> Room Occupancy feature disabled.
        # ROOM_OCCUPANCY_MODE_ALWAYS_ON -> 1 -> Room Occupancy counting enabled whether or not a meeting is active.
        # ROOM_OCCUPANCY_MODE_MEETINGS_ONLY -> 2 -> Room Occupancy counting enabled only when a
        # meeting is active
        try:
            if len(room['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(room['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')
            assert room['roomInformation'] is not None, 'Error in roomInformation field'

            room_info = room['roomInformation']
            if len(room_inf) == 3:
                if room_info['lastModified']:
                    Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
                else:
                    Report.logFail('Error in lastModified field')
                if room_info['roomName']:
                    Report.logPass(
                        'Received roomName field - {}'.format(room_info['roomName']))
                else:
                    Report.logFail('Error in roomName field')
                if room_info['maxOccupancy']:
                    Report.logPass(
                        'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
                else:
                    Report.logFail('Error in maxOccupancy field')

                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                assert room_info['roomName'] == room_inf[0], 'Error in roomName field'
                assert room_info['maxOccupancy'] == int(room_inf[1]), 'Error in maxOccupancy field'
                # roomOccupancyMode attribute does not appear in response if the mode is disabled.
                if room_inf[2] == '1':
                    mode = 'ROOM_OCCUPANCY_MODE_ALWAYS_ON'
                    assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                elif room_inf[2] == '2':
                    mode = 'ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'
                    assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                elif room_inf[2] == '0':
                    assert 'roomOccupancyMode' not in room_info, 'roomOccupancyMode attribute should not be present'

            elif len(room_inf) == 0:
                if room_info['lastModified']:
                    Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
                else:
                    Report.logFail('Error in lastModified field')
                if room_info['roomName']:
                    Report.logPass(
                        'Received roomName field - {}'.format(room_info['roomName']))
                else:
                    Report.logFail('Error in roomName field')
                if room_info['maxOccupancy']:
                    Report.logPass(
                        'Received maxOccupancy field - {}'.format(room_info['maxOccupancy']))
                else:
                    Report.logFail('Error in maxOccupancy field')
                if room_info['roomOccupancyMode']:
                    Report.logPass(
                        'Received roomOccupancyMode field - {}'.format(room_info['roomOccupancyMode']))
                else:
                    Report.logFail('Error in maxOccupancy field')

                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                assert room_info['roomName'] == room_base['roomName'], 'Error in roomName field'
                assert room_info['maxOccupancy'] == room_base['maxOccupancy'], 'Error in maxOccupancy field'
                assert room_info['roomOccupancyMode'] == room_base['roomOccupancyMode'], 'Error in roomOccupancy Mode'

            else:
                assert room_info['lastModified'] is not None, 'Error in lastModified field'
                if room_info['lastModified']:
                    Report.logPass('Received lastModified field - {}'.format(room_info['lastModified']))
                room_info = room['roomInformation']
                if 0 in room_inf:
                    assert room_info['roomName'] == room_inf[0], 'Error in room_name field'
                if 1 in room_inf:
                    assert room_info['maxOccupancy'] == int(room_inf[1]), 'Error in max_occupancy field'
                if 2 in room_inf:
                    if room_inf[2] == '1':
                        mode = 'ROOM_OCCUPANCY_MODE_ALWAYS_ON'
                        assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                    elif room_inf[2] == '2':
                        mode = 'ROOM_OCCUPANCY_MODE_MEETINGS_ONLY'
                        assert room_info['roomOccupancyMode'] == mode, 'Error in roomOccupancyMode field'
                    elif room_inf[2] == '0':
                        assert 'roomOccupancyMode' not in room_info, 'roomOccupancyMode attribute should not be present'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_get_latest_firmware(firmware_response, device_type, product_uuid):
        """
        Validate the ForgetDeviceResponse
        """
        try:
            if 'productUuid' in firmware_response:
                Report.logPass('Received productUuid field - {}'.format(firmware_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if 'latestFirmwarePackageVersion' in firmware_response:
                Report.logPass('Received latestFirmwarePackageVersion field - {}'.format(firmware_response['latestFirmwarePackageVersion']))
            else:
                Report.logFail('Error in latestFirmwarePackageVersion field')
            if 'latestFirmwarePublishedDate' in firmware_response:
                Report.logPass('Received latestFirmwarePublishedDate field - {}'.format(firmware_response['latestFirmwarePublishedDate']))
            else:
                Report.logFail('Error in latestFirmwarePublishedDate field')

            assert firmware_response['productUuid'] == str(product_uuid), 'Error in productUuid field'
            assert firmware_response[
                       'latestFirmwarePackageVersion'] is not None, 'Error in latestFirmwarePackageVersion field'
            assert firmware_response[
                       'latestFirmwarePublishedDate'] is not None, 'Error in latestFirmwarePublishedDate field'
            if device_type == config.DeviceModelConfig.model_rally_bar:
                assert firmware_response[
                           'latestFirmwareReleaseNotesUri'] is not None, 'Error in latestFirmwareReleaseNotesUri field'

            if len(firmware_response['latestDeviceFirmwareVersions']) > 0:
                for device in firmware_response['latestDeviceFirmwareVersions']:
                    if 'latestFirmwareVersion' in device:
                        Report.logPass('Received latestFirmwareVersion field')
                    else:
                        Report.logFail('Error in latestFirmwareVersion field')
                    assert device['latestFirmwareVersion'] is not None, 'Error in latestFirmwareVersion field'
                    if device_type == config.DeviceModelConfig.model_meetup:
                        if 'type' in device:
                            Report.logPass('Received type field')
                        else:
                            Report.logFail('Error in type field')
                        assert device['type'] is not None, 'Error in type field'
                    if device_type is not config.DeviceModelConfig.model_meetup:
                        if 'deviceFormFactor' in device:
                            Report.logPass('Received deviceFormFactor field')
                        else:
                            Report.logFail('Error in deviceFormFactor field')
                        assert device['deviceFormFactor'] is not None, 'Error in deviceFormFactor field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_update_firmware_by_id(firmware_response, product_uuid, package_version=None):
        """
        Validate the UpdateFirmwareByProductIdResponse
        """
        try:
            if firmware_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(firmware_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(firmware_response['productUuid']))
            if firmware_response['firmwarePackageVersion']:
                Report.logPass('Received firmwarePackageVersion field - {}'.format(firmware_response['firmwarePackageVersion']))
            else:
                Report.logFail('Error in firmwarePackageVersion field - {}'.format(firmware_response['firmwarePackageVersion']))

            assert firmware_response['productUuid'] == str(product_uuid), 'Error in productUuid field'
            assert firmware_response['firmwarePackageVersion'] is not None, 'Error in firmwarePackageVersion field'
            if package_version:
                if firmware_response['firmwarePackageVersion'] == package_version:
                    Report.logPass('Received firmwarePackageVersion field - {}'.format(firmware_response['firmwarePackageVersion']))
                else:
                    Report.logFail('Error in firmwarePackageVersion field - {}'.format(firmware_response['firmwarePackageVersion']))

                assert firmware_response['firmwarePackageVersion'] == package_version, 'Error in firmwarePackageVersion field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_update_all_firmware(firmware_response):
        """
        Validate the UpdateAllFirmwareResponse
        """
        try:
            for update in firmware_response:
                if update['productUuid']:
                    Report.logPass('Received productUuid field - {}'.format(update['productUuid']))
                else:
                    Report.logFail('Error in productUuid field - {}'.format(update['productUuid']))
                if update['firmwarePackageVersion']:
                    Report.logPass('Received firmwarePackageVersion field - {}'.format(
                        update['firmwarePackageVersion']))
                else:
                    Report.logFail('Error in firmwarePackageVersion field - {}'.format(
                        update['firmwarePackageVersion']))

                assert update['productUuid'] is not None, 'Error in productUuid field'
                assert update['firmwarePackageVersion'] is not None, 'Error in firmwarePackageVersion field'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_set_firmware_update_schedule_response(firmware_response, product_uuid, scheduled_update, error=None):
        """
        Validate the SetFirmwareUpdateScheduled Response
        """
        try:
            if firmware_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(firmware_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field - {}'.format(firmware_response['productUuid']))

            if firmware_response['productModel']:
                Report.logPass('Received productModel field - {}'.format(firmware_response['productModel']))
            else:
                Report.logFail('Error in productModel field - {}'.format(firmware_response['productModel']))

            assert firmware_response['productUuid'] == str(product_uuid), 'Error in productUuid field'
            assert firmware_response['productModel'] is not None, 'Error in productModel field'

            if scheduled_update:
                if 'update_package_version' in scheduled_update:
                    if firmware_response['scheduledUpdate']['updatePackageVersion'] == scheduled_update['update_package_version']:
                        Report.logPass('Received updatePackageVersion field')
                    else:
                        Report.logFail('Error in updatePackageVersion field')
                    assert firmware_response['scheduledUpdate']['updatePackageVersion'] == scheduled_update[
                        'update_package_version'], 'Error in update_package_version field'
                if 'update_published_date' in scheduled_update:
                    if firmware_response['scheduledUpdate']['updatePackageVersion'] == scheduled_update['update_package_version']:
                        Report.logPass('Received updatePackageVersion field')
                    else:
                        Report.logFail('Error in updatePackageVersion field')
                    if firmware_response['scheduledUpdate']['updatePublishedDate'] == scheduled_update['update_published_date']:
                        Report.logPass('Received updatePublishedDate field')
                    else:
                        Report.logFail('Error in updatePublishedDate field')
                    assert firmware_response['scheduledUpdate']['updatePackageVersion'] == scheduled_update[
                        'update_package_version'], 'Error in update_package_version field'

                    assert firmware_response['scheduledUpdate']['updatePublishedDate'] == scheduled_update[
                        'update_published_date'], 'Error in update_published_date field'
                if 'issued_time' in scheduled_update:
                    if firmware_response['scheduledUpdate']['issuedTime'] == str(scheduled_update['issued_time']):
                        Report.logPass('Received issuedTime field')
                    else:
                        Report.logFail('Error in issuedTime field')
                    assert firmware_response['scheduledUpdate']['issuedTime'] == str(scheduled_update[
                                                                                         'issued_time']), 'Error in issued_time field'
                if 'earliest_time' in scheduled_update:
                    if firmware_response['scheduledUpdate']['earliestTime'] == str(scheduled_update['earliest_time']):
                        Report.logPass('Received earliestTime field')
                    else:
                        Report.logFail('Error in earliestTime field')
                    assert firmware_response['scheduledUpdate']['earliestTime'] == str(scheduled_update[
                                                                                           'earliest_time']), 'Error in earliest_time field'
                if 'latest_time' in scheduled_update:
                    if firmware_response['scheduledUpdate']['latestTime'] == str(scheduled_update['latest_time']):
                        Report.logPass('Received latest_time field')
                    else:
                        Report.logFail('Error in latest_time field')
                    assert firmware_response['scheduledUpdate']['latestTime'] == str(scheduled_update[
                                                                                         'latest_time']), 'Error in latest_time field'
            else:
                if firmware_response['scheduledUpdate'] == {}:
                    Report.logPass('Did not schedule an update')
                else:
                    Report.logFail('Error in scheduled update field')
                assert firmware_response['scheduledUpdate'] == {}, 'Error in scheduledUpdate field'

            if error:
                if firmware_response['errors'][0]["errorCode"] == error['id']:
                    Report.logPass('Received error_code field')
                else:
                    Report.logFail('Error in error_code field')
                if firmware_response['errors'][0]["errorMessage"] == error['message']:
                    Report.logPass('Received error_message field')
                else:
                    Report.logFail('Error in error_message field')
                assert firmware_response['errors'][0]["errorCode"] == error['id'], 'Error in error_code field.'
                assert firmware_response['errors'][0]["errorMessage"] == error['message'], 'Error in error_message field.'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_get_firmware_update_progress(firmware_response, product_uuid):
        """
        Validate the GetFirmwareUpdateProgressResponse
        """
        try:
            device_response = [resp for resp in firmware_response if resp['productUuid'] == product_uuid]
            assert len(device_response) == 1, 'Error: Update progress response for productUuid not found'

            if device_response[0]['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(device_response[0]['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if device_response[0]['deviceUuid']:
                Report.logPass('Received deviceUuid field - {}'.format(device_response[0]['deviceUuid']))
            else:
                Report.logFail('Error in deviceUuid field')
            if device_response[0]['firmwarePackageVersion']:
                Report.logPass('Received firmwarePackageVersion field - {}'.format(device_response[0]['firmwarePackageVersion']))
            else:
                Report.logFail('Error in firmwarePackageVersion field'.format(device_response[0]['firmwarePackageVersion']))
            if device_response[0]['currentProgress']:
                Report.logPass('Received currentProgress field - {}'.format(device_response[0]['currentProgress']))
            else:
                Report.logFail('Error in currentProgress field')
            if device_response[0]['overallProgress']:
                Report.logPass('Received overallProgress field - {}'.format(device_response[0]['overallProgress']))
            else:
                Report.logFail('Error in overallProgress field')
            if device_response[0]['remainingUpdateTime']:
                Report.logPass('Received remainingUpdateTime field - {}'.format(device_response[0]['remainingUpdateTime']))
            else:
                Report.logFail('Error in remainingUpdateTime field')

            assert device_response[0]['productUuid'] == str(product_uuid), 'Error in productUuid field'
            assert device_response[0]['deviceUuid'] is not None, 'Error in deviceUuid field'
            assert device_response[0]['firmwarePackageVersion'] is not None, 'Error in firmwarePackageVersion field'
            assert device_response[0]['currentProgress'] is not None, 'Error in currentProgress field'
            assert device_response[0]['overallProgress'] is not None, 'Error in overallProgress field'
            assert device_response[0]['remainingUpdateTime'] is not None, 'Error in remainingUpdateTime field'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setBleSettingsResponse(response_data, ble_mode):
        """
        Validate the SetBleConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['bleConfiguration']) > 0:
                Report.logPass(
                    'Received bleConfiguration field - {}'.format(response_data['bleConfiguration']))
            else:
                Report.logFail('Error in bleConfiguration field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['bleConfiguration'] is not None, 'Error in bleConfiguration message.'

            if ble_mode == 'BLE_OFF':
                if 'bleMode' not in response_data['bleConfiguration']:
                    Report.logPass('Ble_mode field is not present.')
                else:
                    Report.logFail('Ble_mode field should not be present.')
                if 'lastModified' in response_data['bleConfiguration']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. BLE mode may not have changed.')
                assert 'bleMode' not in response_data['bleConfiguration'], 'Ble_mode field should not be present.'
                assert 'lastModified' in response_data['bleConfiguration'], \
                    'No last modified timestamp present. BLE mode may not have changed.'
            elif ble_mode == 'BLE_OFF_redundant_test':
                if 'timeout' in response_data['bleConfiguration']['errorCode']:
                    Report.logPass('Timeout in Bluetooth Configuration as expected')
                else:
                    Report.logFail('Timeout field should be present')
                assert 'timeout' in response_data['bleConfiguration']['errorCode'], \
                    'Redundant BLE request did not time out as expected.'
            elif ble_mode == 'BLE_ON':
                if 'bleMode' in response_data['bleConfiguration']:
                    Report.logPass('Ble_mode field is present.')
                else:
                    Report.logFail('Ble_mode field should be present.')
                if response_data['bleConfiguration']['bleMode'] == 'BLE_ON':
                    Report.logPass('BLE mode is on')
                else:
                    Report.logFail('Error in ble mode field')
                if 'lastModified' in response_data['bleConfiguration']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. BLE mode may not have changed.')
                assert 'bleMode' in response_data['bleConfiguration'], 'Ble_mode field should be present.'
                assert response_data['bleConfiguration']['bleMode'] == 'BLE_ON', 'Error in ble_mode field.'
                assert 'lastModified' in response_data['bleConfiguration'], \
                    'No last modified timestamp present. BLE mode may not have changed.'
            elif ble_mode == 'BLE_ON_redundant_test':
                if 'timeout' in response_data['bleConfiguration']['errorCode']:
                    Report.logPass('Timeout field in Bluetooth Configuration as expected')
                else:
                    Report.logFail('Timeout field should be present')
                assert 'timeout' in response_data['bleConfiguration']['errorCode'], \
                    'Redundant BLE request did not time out as expected.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_error_bluetooth_settings(response_data):
        """
        Validate the ble configuration settings response when error occurs.
        """
        try:
            if 'errors' in response_data:
                Report.logPass('Received errors field - {}'.format(response_data['errors']))
            else:
                Report.logFail('Error in errors field')
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['bleConfiguration']) > 0:
                Report.logPass(
                    'Received bleConfiguration field - {}'.format(response_data['bleConfiguration']))
            else:
                Report.logFail('Error in audioSettings field')

            assert response_data['errors'] is not None, 'errors object is not seen'
            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['bleConfiguration'] is not None, 'Error in bleConfiguration message.'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err


    @staticmethod
    def validate_setAudioNoiseReductionResponse(response_data, noise_reduction):
        """
        Validate the SetBleConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['audioSettings']) > 0:
                Report.logPass(
                    'Received audioSettings field - {}'.format(response_data['audioSettings']))
            else:
                Report.logFail('Error in audioSettings field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['audioSettings'] is not None, 'Error in audioSettings message.'

            if noise_reduction == 'DISABLE':
                if 'noiseReduction' not in response_data['audioSettings']:
                    Report.logPass('noise_reduction field is not present.')
                else:
                    Report.logFail('noise_reduction field should not be present.')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. noise reduction field may not have changed.')
                assert 'noiseReduction' not in response_data['audioSettings'], 'noise reduction field should not be present.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. noise reduction field may not have changed.'

            elif noise_reduction == 'ENABLE':
                if 'noiseReduction' in response_data['audioSettings']:
                    Report.logPass('noise_reduction field is present.')
                else:
                    Report.logFail('noise_reduction field should be present.')
                if response_data['audioSettings']['noiseReduction'] == 1:
                    Report.logPass('noise Reduction is enabled')
                else:
                    Report.logFail('Error in noise reduction field')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. noiseReduction field may not have changed.')
                assert 'noiseReduction' in response_data['audioSettings'], 'noiseReduction field should be present.'
                assert response_data['audioSettings']['noiseReduction'] == 1, 'Error in noiseReduction field.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. noiseReduction may not have changed.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_error_audio_settings(response_data):
        """
        Validate the audio settings response when error occurs.
        """
        try:
            if 'errors' in response_data:
                Report.logPass('Received errors field - {}'.format(response_data['errors']))
            else:
                Report.logFail('Error in errors field')
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['audioSettings']) > 0:
                Report.logPass(
                    'Received audioSettings field - {}'.format(response_data['audioSettings']))
            else:
                Report.logFail('Error in audioSettings field')

            assert response_data['errors'] is not None, 'errors object is not seen'
            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['audioSettings'] is not None, 'Error in audioSettings message.'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setAudioSpeakerBoostResponse(response_data, speaker_boost):
        """
        Validate the SetBleConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['audioSettings']) > 0:
                Report.logPass(
                    'Received audioSettings field - {}'.format(response_data['audioSettings']))
            else:
                Report.logFail('Error in audioSettings field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['audioSettings'] is not None, 'Error in audioSettings message.'

            if speaker_boost == 'DISABLE':
                if 'speakerBoost' not in response_data['audioSettings']:
                    Report.logPass('speaker_boost field is not present.')
                else:
                    Report.logFail('speaker_boost field should not be present.')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. speaker_boost field may not have changed.')
                assert 'speakerBoost' not in response_data[
                    'audioSettings'], 'speaker_boost field should not be present.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. speaker_boost field may not have changed.'

            elif speaker_boost == 'ENABLE':
                if 'speakerBoost' in response_data['audioSettings']:
                    Report.logPass('speaker_boost field is present.')
                else:
                    Report.logFail('speaker_boost field should be present.')
                if response_data['audioSettings']['speakerBoost'] == 1:
                    Report.logPass('speaker_boost is enabled')
                else:
                    Report.logFail('Error in speaker_boost field')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. noiseReduction field may not have changed.')
                assert 'speakerBoost' in response_data['audioSettings'], 'speaker_boost field should be present.'
                assert response_data['audioSettings']['speakerBoost'] == 1, 'Error in speaker_boost field.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. speaker_boost may not have changed.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setAudioReverbModeResponse(response_data, reverb_mode):
        """
        Validate the setAudioReverbModeResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if len(response_data['audioSettings']) > 0:
                Report.logPass(
                    'Received audioSettings field - {}'.format(response_data['audioSettings']))
            else:
                Report.logFail('Error in audioSettings field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['audioSettings'] is not None, 'Error in audioSettings message.'

            if reverb_mode == 'NORMAL':
                if 'reverbMode' in response_data['audioSettings']:
                    Report.logPass('reverb_mode field is present.')
                else:
                    Report.logFail('reverb_mode field should be present.')
                if response_data['audioSettings']['reverbMode'] == "NORMAL":
                    Report.logPass('reverb_mode is enabled')
                else:
                    Report.logFail('Error in reverb_mode field')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. reverb_mode field may not have changed.')
                assert 'reverbMode' in response_data[
                    'audioSettings'], 'reverb_mode field should be present.'
                assert response_data['audioSettings']['reverbMode'] == 'NORMAL', 'Error in reverbMode field.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. reverb_mode field may not have changed.'

            elif reverb_mode == 'AGGRESSIVE':
                if 'reverbMode' in response_data['audioSettings']:
                    Report.logPass('reverb_mode field is present.')
                else:
                    Report.logFail('reverb_mode field should be present.')
                if response_data['audioSettings']['reverbMode'] == "AGGRESSIVE":
                    Report.logPass('reverb_mode is enabled')
                else:
                    Report.logFail('Error in reverb_mode field')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. noiseReduction field may not have changed.')
                assert 'reverbMode' in response_data['audioSettings'], 'reverb_mode field should be present.'
                assert response_data['audioSettings']['reverbMode'] == 'AGGRESSIVE', 'Error in reverbMode field.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. speaker_boost may not have changed.'

            elif reverb_mode == 'DISABLE':
                if 'reverbMode' not in response_data['audioSettings']:
                    Report.logPass('reverbMode field is not present.')
                else:
                    Report.logFail('reverbMode field should not be present.')
                if 'lastModified' in response_data['audioSettings']:
                    Report.logPass('lastModified field is present.')
                else:
                    Report.logFail('No last modified timestamp present. speaker_boost field may not have changed.')
                assert 'reverbMode' not in response_data[
                    'audioSettings'], 'reverbMode field should not be present.'
                assert 'lastModified' in response_data['audioSettings'], \
                    'No last modified timestamp present. speaker_boost field may not have changed.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setDeviceWhiteboardConfigurationResponse(response_data, whiteboard_configuration):
        """
        Validate the setDeviceWhiteboardConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if 'whiteboardConfiguration' in response_data:
                Report.logPass('Received whiteBoardConfiguration field - {}'.format(response_data['whiteboardConfiguration']))
            else:
                Report.logFail('Errro in whiteboardConfiguration field')
            if 'imageEnhancement' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received imageEnhancement field - {}'.format(response_data['whiteboardConfiguration']['imageEnhancement']))
            else:
                Report.logFail('Error in imageEnhancement field')
            if 'ghosting' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received ghosting field - {}'.format(response_data['whiteboardConfiguration']['ghosting']))
            else:
                Report.logFail('Error in ghosting field')
            if 'lastModified' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received lastModified field - {}'.format(response_data['whiteboardConfiguration']['lastModified']))
            else:
                Report.logFail('Error in lastModified field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['whiteboardConfiguration'] is not None, 'Error in whiteboardConfiguration message.'
            assert response_data['whiteboardConfiguration']['imageEnhancement'] == whiteboard_configuration['image_enhancement'], 'Error in imageEnhancement field'
            assert response_data['whiteboardConfiguration']['ghosting'] == whiteboard_configuration['ghosting'], 'Error in ghosting field'
            assert response_data['whiteboardConfiguration']['lastModified'] is not None, 'Error in lastModified field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_setDeviceWhiteboardEditBoundariesResponse(response_data):
        """
        Validate the setDeviceWhiteboardConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if 'whiteboardConfiguration' in response_data:
                Report.logPass(
                    'Received whiteBoardConfiguration field - {}'.format(response_data['whiteboardConfiguration']))
            else:
                Report.logFail('Error in whiteboardConfiguration field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['whiteboardConfiguration'] is not None, 'Error in whiteboardConfiguration message.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_create_set_device_whiteboard_edit_boundaries_request(response_data):
        """
        Validate the setDeviceWhiteboardConfigurationResponse
        """
        try:
            if len(response_data['productUuid']) > 0:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if len(response_data['productModel']) > 0:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if 'whiteboardConfiguration' in response_data:
                Report.logPass(
                    'Received whiteBoardConfiguration field - {}'.format(response_data['whiteboardConfiguration']))
            else:
                Report.logFail('Errro in whiteboardConfiguration field')
            if 'imageEnhancement' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received imageEnhancement field - {}'.format(
                        response_data['whiteboardConfiguration']['imageEnhancement']))
            else:
                Report.logFail('Error in imageEnhancement field')
            if 'ghosting' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received ghosting field - {}'.format(response_data['whiteboardConfiguration']['ghosting']))
            else:
                Report.logFail('Error in ghosting field')
            if 'lastModified' in response_data['whiteboardConfiguration']:
                Report.logPass(
                    'Received lastModified field - {}'.format(response_data['whiteboardConfiguration']['lastModified']))
            else:
                Report.logFail('Error in lastModified field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['whiteboardConfiguration'] is not None, 'Error in whiteboardConfiguration message.'
            assert response_data['whiteboardConfiguration']['imageEnhancement'] is not None, 'Error in imageEnhancement field'
            assert response_data['whiteboardConfiguration']['ghosting'] is not None, 'Error in ghosting field'
            assert response_data['whiteboardConfiguration']['lastModified'] is not None, 'Error in lastModified field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_videoSettingsConfigurationChangedEvent(event_response):
        """
        Validate validate_videoSettingsConfigurationChangedEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid'] is not None:
                Report.logPass('Event Response - Received productUuid field')
            else:
                Report.logFail('Event Response - Error in productUuid field')
            if event_response['productModel'] is not None:
                Report.logPass('Event Response - Received productModel field ')
            else:
                Report.logFail('Event Response - Error in productModel field')
            if event_response['videoSettingConfiguration'] is not None:
                Report.logPass('Event Response - Received videoSettingsConfiguration field')
            else:
                Report.logFail('Event Response - Error in videoSettingsConfiguration field')

            assert event_response['productUuid'] is not None, 'Error in productUuid field.'
            assert event_response['productModel'] is not None, 'Error in productModel field.'
            assert event_response['videoSettingConfiguration'] is not None, 'Error in videoSettingConfiguration message.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_rightSightConfigurationChangedEvent(event_response):
        """
        Validate validate_videoSettingsConfigurationChangedEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid'] is not None:
                Report.logPass('Event Response - Received productUuid field')
            else:
                Report.logFail('Event Response - Error in productUuid field')
            if event_response['productModel'] is not None:
                Report.logPass('Event Response - Received productModel field ')
            else:
                Report.logFail('Event Response - Error in productModel field')
            if event_response['rightSightConfiguration'] is not None:
                Report.logPass('Event Response - Received rightSightConfiguration field')
            else:
                Report.logFail('Event Response - Error in rightSightConfiguration field')

            assert event_response['productUuid'] is not None, 'Error in productUuid field.'
            assert event_response['productModel'] is not None, 'Error in productModel field.'
            assert event_response[
                       'rightSightConfiguration'] is not None, 'Error in rightSightConfigurationChanged Event message.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_roomInformationChangedEvent(response_data):
        """
        Validate the RoomInformationChangedEvent
        """
        try:
            if len(response_data['roomInformation']) > 0:
                Report.logPass('Received roomInformation field - {}'.format(response_data['roomInformation']))
            else:
                Report.logFail('Error in roomInformation field')
            assert response_data['roomInformation'] is not None, 'Error in roomInformation message'

            response = response_data['roomInformation']
            if response['lastModified']:
                Report.logPass('Received lastModified field - {}'.format(response['lastModified']))
            else:
                Report.logFail('Error in lastModified field')
            if response['roomName']:
                Report.logPass(
                    'Received roomName field - {}'.format(response['roomName']))
            else:
                Report.logFail('Error in roomName field')
            if response['maxOccupancy']:
                Report.logPass(
                    'Received maxOccupancy field - {}'.format(response['maxOccupancy']))
            else:
                Report.logFail('Error in maxOccupancy field')

            assert response['lastModified'] is not None, 'Error in lastModified field'
            assert response['roomName'] is not None, 'Error in roomName field.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @ staticmethod
    def logisync_configuration_changed_event(response_data, conf_base):
        """
        Validate the LogiSyncConfigurationChangedEvent
        """
        try:
            assert response_data['configuration'] is not None, 'Error in configuration message'
            response = response_data['configuration']['configuration']
            if response:
                Report.logPass('Received configuration field - {}'.format(response_data['configuration']))
            else:
                Report.logFail('Error in configuration field')
            assert response is not None, 'configuration should not be empty'
            assert len(response) == len(conf_base), 'Error in the length of configuration response'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_ble_configuration_changed_event(response_data):
        """
        Validate the bleConfigurationChangedEvent
        """
        try:
            if response_data['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(response_data['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if response_data['productModel']:
                Report.logPass('Received productModel field - {}'.format(response_data['productModel']))
            else:
                Report.logFail('Error in productModel field')
            if response_data['bleConfiguration']:
                Report.logPass('Received bleConfiguration field - {}'.format(response_data['bleConfiguration']))
            else:
                Report.logFail('Error in bleConfiguration field')

            assert response_data['productUuid'] is not None, 'Error in productUuid field.'
            assert response_data['productModel'] is not None, 'Error in productModel field.'
            assert response_data['bleConfiguration'] is not None, 'Error in bleConfiguration message.'

            if response_data['bleConfiguration']['lastModified']:
                Report.logPass('Last Modified present in Bluetooth Configuration')
            else:
                Report.logFail('Error in lastModified field')

            assert 'lastModified' in response_data['bleConfiguration'], \
                'No last modified timestamp present. BLE mode may not have changed.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            Report.logFail('Assertion Error - {}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            Report.logFail('Error - {}'.format(key_err))
            raise key_err

    @staticmethod
    def validate_firmware_update_started_Event(event_response, product_uuid):
        """
        Validate validate_firmwareUpdateStartedEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if event_response['currentFirmwarePackageVersion']:
                Report.logPass('Received currentFirmwarePackageVersion field - {}'.format(event_response['currentFirmwarePackageVersion']))
            else:
                Report.logFail('Error in currentFirmwarePackageVersion field')
            if event_response['newFirmwarePackageVersion']:
                Report.logPass('Received newFirmwarePackageVersion field - {}'.format(event_response['newFirmwarePackageVersion']))
            else:
                Report.logFail('Error in newFirmwarePackageVersion field')

            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            assert event_response[
                       'currentFirmwarePackageVersion'] is not None, 'Error in currentFirmwarePackageVersion field.'
            assert event_response['newFirmwarePackageVersion'] is not None, 'Error in newFirmwarePackageVersion field.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_firmware_update_progress_Event(event_response, product_uuid):
        """
        Validate validate_firmwareUpdateProgressEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if event_response['deviceUuid']:
                Report.logPass('Received deviceUuid field - {}'.format(event_response['deviceUuid']))
            else:
                Report.logFail('Error in deviceUuid field')
            if event_response['firmwarePackageVersion']:
                Report.logPass('Received firmwarePackageVersion field - {}'.format(event_response['firmwarePackageVersion']))
            else:
                Report.logFail('Error in firmwarePackageVersion field')
            if event_response['currentProgress']:
                Report.logPass('Received currentProgress field - {}'.format(event_response['currentProgress']))
            else:
                Report.logFail('Error in currentProgress field')
            if event_response['overallProgress']:
                Report.logPass('Received overallProgress field - {}'.format(event_response['overallProgress']))
            else:
                Report.logFail('Error in overallProgress field')
            if event_response['remainingUpdateTime']:
                Report.logPass('Received remainingUpdateTime field - {}'.format(event_response['remainingUpdateTime']))
            else:
                Report.logFail('Error in remainingUpdateTime field')

            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            assert event_response['deviceUuid'] is not None, 'Error in deviceUuid field.'
            assert event_response['firmwarePackageVersion'] is not None, 'Error in firmwarePackageVersion field.'
            assert event_response['currentProgress'] is not None, 'Error in currentProgress field.'
            assert event_response['overallProgress'] is not None, 'Error in overallProgress field.'
            assert event_response['remainingUpdateTime'] is not None, 'Error in remainingUpdateTime field.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_firmware_update_completed_Event(event_response, product_uuid):
        """
        Validate validate_firmwareUpdateProgressEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_firmware_update_completed_Event_with_fw_package_version(event_response, product_uuid, firmware_package_version):
        """
        Validate validate_firmwareUpdateProgressEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if event_response['newFirmwarePackageVersion'] == firmware_package_version:
                Report.logPass('Received newFirmwarePackageVersion field - {}'.format(
                    event_response['newFirmwarePackageVersion']))
            else:
                Report.logFail('Error in newFirmwarePackageVersion field')
            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            assert event_response['newFirmwarePackageVersion'] == firmware_package_version, \
                'Error in newFirmwarePackageVersion field'
            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err


    @staticmethod
    def validate_firmware_update_error_Event(event_response, product_uuid, error):
        """
        Validate validate_firmwareUpdateErrorEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid'] == product_uuid:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if event_response['errors'][0]['errorCode'] == error['id']:
                Report.logPass('Received error_code field - {}'.format(event_response['errors'][0]['errorCode']))
            else:
                Report.logFail('Error in error_code field')
            if event_response['errors'][0]['errorMessage'] == error['message']:
                Report.logPass('Received error_message field - {}'.format(event_response['errors'][0]['errorMessage']))
            else:
                Report.logFail('Error in error_message field')
            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            assert event_response['errors'][0]['errorCode'] == error['id'], 'Error in error_code field.'
            assert event_response['errors'][0]['errorMessage'] == error['message'], 'Error in error_message field.'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err

    @staticmethod
    def validate_firmware_update_scheduled_Event(event_response, product_uuid):
        """
        Validate validate_firmwareUpdateProgressEvent.
        :param event_response:
        :return:
        """
        try:
            if event_response['productUuid']:
                Report.logPass('Received productUuid field - {}'.format(event_response['productUuid']))
            else:
                Report.logFail('Error in productUuid field')
            if event_response['deviceUuid']:
                Report.logPass('Received deviceUuid field - {}'.format(event_response['deviceUuid']))
            else:
                Report.logFail('Error in deviceUuid field')
            if event_response['firmwarePackageVersion']:
                Report.logPass('Received firmwarePackageVersion field - {}'.format(event_response['firmwarePackageVersion']))
            else:
                Report.logFail('Error in firmwarePackageVersion field')
            if event_response['currentProgress']:
                Report.logPass('Received currentProgress field - {}'.format(event_response['currentProgress']))
            else:
                Report.logFail('Error in currentProgress field')
            if event_response['overallProgress']:
                Report.logPass('Received overallProgress field - {}'.format(event_response['overallProgress']))
            else:
                Report.logFail('Error in overallProgress field')
            if event_response['remainingUpdateTime']:
                Report.logPass('Received remainingUpdateTime field - {}'.format(event_response['remainingUpdateTime']))
            else:
                Report.logFail('Error in remainingUpdateTime field')

            assert event_response['productUuid'] == product_uuid, 'Error in productUuid field.'
            assert event_response['deviceUuid'] is not None, 'Error in deviceUuid field.'
            assert event_response['firmwarePackageVersion'] is not None, 'Error in firmwarePackageVersion field.'
            assert event_response['currentProgress'] is not None, 'Error in currentProgress field.'
            assert event_response['overallProgress'] is not None, 'Error in overallProgress field.'
            assert event_response['remainingUpdateTime'] is not None, 'Error in remainingUpdateTime field.'

            return True

        except AssertionError as assert_err:
            log.error('{}'.format(assert_err))
            raise assert_err
        except KeyError as key_err:
            log.error('{} field is not present.'.format(key_err))
            raise key_err
