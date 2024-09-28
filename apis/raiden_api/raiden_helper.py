import logging
import os
import requests
import random
import string
from common import raiden_config
from common import framework_params as fp
import time

from common.platform_helper import retry_request
from extentreport.report import Report
import json
import apis.process_helper as process_helper
from apis.raiden_api import raiden_validation_methods
from base import global_variables
import apis.raiden_api.raiden_parameters as raiden_parameters
from datetime import datetime

log = logging.getLogger(__name__)


def token_gen(token):
    return {'Authorization': 'Bearer ' + token}


def send_request(method: str, url: str, body=None, token=None, params=None) -> dict:
    """
    Create the request and returns the response using the request library

    :param method:
    :param url:
    :param body:
    :param token:
    :param params:
    :return:

    """
    try:

        kwargs = dict()
        kwargs['headers'] = token_gen(token) if token else None
        kwargs['data'] = body if method != 'GET' else None
        kwargs['params'] = params if method == 'GET' else None
        kwargs['timeout'] = 30

        return eval(f"retry_request.{method.lower()}(url, **kwargs).json()")

    except Exception as err:
        AssertionError('Request Error {}'.format(err))


def get_raiden_backend_version(config):
    """
    Getting the Raiden API Version
    :param config:
    :return:
    """
    try:
        # Construct header
        _url = config.BASE_URL + raiden_config.VERSION_ENDPNT

        # Send the request
        response = send_request(method='GET', url=_url)
        api_version = response['version']
        log.debug(f'Raiden API Version is {api_version}')
        return api_version

    except Exception as e:
        log.error(f'{e}')
        raise e


def validate_sign_in(response: dict):
    """
    Validate the Token and TTL of the Signin Users response message

    :param response:
    :return:

    """
    try:
        assert response['token'] is not None, 'Error in Token Field'
        assert response['ttl'] is not None, 'Error in TTL Field'

        if response['token']:
            Report.logPass("Token generated successfully")
        else:
            Report.logFail("Token not generated successfully")

        if response['ttl']:
            Report.logPass("TTL field occurred")
        else:
            Report.logFail("Error in TTL Field")
        return True, response['token']

    except AssertionError as e:
        log.error('validate_signinuser - {}'.format(e))
        return (False, None)


def signin_method(config, role: str):
    """
    Signin Api - added as part of setup method in unittest case class

    :param config:
    :param role:
    :return:

    """

    # Construct header
    _url = config.BASE_URL + raiden_config.SIGNIN_ENDPNT
    _data = config.ROLES[role]['signin_payload']

    Report.logInfo(f'Sign in: {role}')

    try:
        # Send the request
        response = send_request(method='POST', url=_url, body=_data)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for Sign In API - {json_formatted_response}')

        # Validate the response
        (_status, token) = validate_sign_in(response)
        if _status:
            Report.logPass(f'{role} Sign-in validation passed')
            return token
        else:
            log.info(f'{role} Sign-in validation failed')
            return None
    except Exception as e:
        log.error('{} - Unable to sign in with the user role'.format(role))
        raise e


def random_string_generator(number_of_chars=12, chars=string.ascii_uppercase + string.digits):
    """
    Generates a random serial number of length provided as input.
    :param number_of_chars:
    :param chars
    :return:
    """
    try:
        return ''.join(random.choice(chars) for _ in range(number_of_chars))

    except Exception as e:
        log.error('Error in generating serial number: {}'.format(e))
        return False


def get_session_context(config, token):
    """
    Get the session context

    :param config: Config containing users' credentials.
    :param token: Token of the signed in user.
    :return:
    """
    try:

        _url = config.BASE_URL + raiden_config.SESSION_ENDPNT

        # Send the request
        response = send_request(method='GET', url=_url, token=token)
        return response

    except Exception as e:
        log.error('get_session_context - {}'.format(e))
        raise e


def create_org(config, role):
    """
    Create Organization

    :param config:
    :param role:
    :return:
    """
    try:
        token = signin_method(config, role)
        org_url = config.BASE_URL + raiden_config.ORG_ENDPNT
        now = datetime.now()
        org_name = 'QAOrg-' + now.strftime("%Y%m%d%H%M%S")
        Report.logInfo(f'Creating organization with name: {org_name}')

        org_payload = {
            'name': org_name,
        }
        # Send the request
        response = send_request(
            method='POST', url=org_url, token=token, body=json.dumps(org_payload)
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logInfo(format(json_formatted_response))
        return response, org_name

    except Exception as e:
        log.error('{}'.format(e))
        raise e


def update_org(config, role, org_id):
    """
    Create Organization

    :param config:
    :param role:
    :param org_id:
    :return:
    """
    try:
        token = signin_method(config, role)
        org_url = config.BASE_URL + raiden_config.ORG_ENDPNT + str(org_id)
        now = datetime.now()
        org_name = 'QAOrg-' + now.strftime("%Y%m%d%H%M%S")
        Report.logInfo(f'Updating name of the organization to: {org_name}')
        org_payload = {
            'id': org_id,
            'name': org_name,
        }
        # Send the request
        response = send_request(
            method='PUT', url=org_url, token=token, body=json.dumps(org_payload)
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        return response, org_name

    except Exception as e:
        log.error('{}'.format(e))
        raise e


def get_orgs(config, role):
    """
    Get list of organizations
    """
    try:
        token = signin_method(config, role)
        org_url = config.BASE_URL + raiden_config.ORG_ENDPNT
        response = send_request(
            method='GET', url=org_url, token=token,
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Number of Organizations : {response.__len__()}')
        return response

    except Exception as e:
        log.error('{}'.format(e))
        raise e


def get_org_info(config, token):
    """
    Get the org info - making it as a generic method so that can be used in
    future to fetch some other org related info

    :param config:
    :param token:
    :return:

    """
    try:

        # Construct header
        _url = config.BASE_URL + raiden_config.ORG_ENDPNT

        # Send the request
        response = send_request(method='GET', url=_url, token=token)

        return response

    except Exception as e:
        log.error('get_org_info {}'.format(e))
        raise e


def parse_org_id_from_org_info(role, config, token):
    """
    parse orgid from GET Org Info

    :param role:
    :param config:
    :param token:
    :return:

    """
    try:

        response = get_org_info(config, token)

        _org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        # Filter the error responses
        if len(response):

            log.info('Using the Org Name {}'.format(_org_name))

            # log.debug("{}".format(response))
            # Updating the Org ID in configurations
            for _ in range(len(response)):
                if response[_]['name'] == _org_name:
                    log.info(
                        'orgName: {} org_id: {}'.format(
                            _org_name, response[_]['id'],
                        ),
                    )
                    return response[_]['id']

        log.error('{} ORG is not present'.format(_org_name))

        raise AssertionError('{} ORG is not present'.format(_org_name))

    except Exception as e:
        log.error('Get the ORG ID : Error - {}'.format(e))
        raise e


def parse_org_id_from_session_context(role: str, config: object, token: str):
    """
    This method will parse the org id from session context.

    :param role:
    :param config:
    :param token:
    :return:

    """
    try:

        response = get_session_context(config, token)

        if response:
            org_id = response['org']['id']
            log.info(f'{role}- Organization ID - {org_id}')
            return org_id

        return None

    except Exception as e:
        log.error('parse_org_id_from_session_context - {}'.format(e))
        raise e


def get_user_id_from_user_email(role: str, config: object, token: str):
    """
    Get User ID from User email ID
    """
    try:
        get_user_by_email = config.BASE_URL + raiden_config.USER_ENDPNT + "/get"
        email_id = config.ROLES[role]['signin_payload']['email']
        data = {"email": email_id}
        response = send_request(
            method='POST', url=get_user_by_email, body=json.dumps(data), token=token
        )
        user_id = response['id']
        log.info(f'{role}- User ID of {email_id} - {user_id}')
        return user_id

    except Exception as e:
        log.error('Error in parsing user ID from email ID - {}'.format(e))
        raise e


def parse_org_id_from_user_role(role: str, config: object, token: str):
    """
    This method will parse the org id from org name available in user role response

    :param role:
    :param config:
    :param token:
    :return:

    """
    try:
        # Step 1: Get user by email
        user_id = get_user_id_from_user_email(role, config, token)

        # Step 2: Get User role and fetch organization ID from organization name
        get_user_role = config.BASE_URL + raiden_config.USER_ENDPNT + "/" + user_id + "/role"
        response = send_request(
            method='GET', url=get_user_role, token=token
        )
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        org_id = None
        for i in range(len(response)):
            if response[i]['orgName'] == org_name:
                org_id = response[i]['orgId']
                break
        return org_id

    except Exception as e:
        log.error('Error in parsing org id - {}'.format(e))
        raise e


def get_org_id(role: str, config: object, token: str):
    """
    Get the ORG ID based on the roles

    :param role:
    :param config:
    :param token:
    :return:

    """
    org_id_dict = {
        'SysAdmin': parse_org_id_from_org_info,
        'Viewer': parse_org_id_from_org_info,
        'OrgAdmin': parse_org_id_from_user_role,
        'OrgViewer': parse_org_id_from_user_role,
        'Readonly': parse_org_id_from_user_role,
        'ThirdParty': parse_org_id_from_user_role
    }
    return org_id_dict[role](role, config, token)


def delete_org(config, token: str, org_id: str):
    """
    Delete User based on the config

    :param config:
    :param token:
    :param org_id:
    :return:
    """
    try:
        delete_org_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id
        # Send the request
        response = send_request(
            method='DELETE', url=delete_org_url, token=token,
        )
        raiden_validation_methods.validate_empty_response(response)
        return response

    except Exception as e:
        log.error('{}'.format(e))
        raise e


def get_session_context_filter_by_orgid(config, token, org_id):
    """
    Getting session context filter by org id

    :param config:
    :param token:
    :param org_id:
    :return:
    """
    try:

        _url = config.BASE_URL + raiden_config.SESSION_ENDPNT

        _params = {'orgId': org_id}

        # Send the request
        response = send_request(
            method='GET', url=_url,
            token=token, params=_params,
        )
        return response

    except Exception as e:
        Report.logException(f'{e}')


def get_device_id_from_room_name(config, room_name, org_id, token, device_type):
    """
    Get Device ID of the device for provided device type from room name.
    """
    try:
        room_id = get_room_id_from_room_name(config, org_id, room_name, token)
        get_room_info_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/" + room_id + "/info"
        device_id = None
        retries = 10
        retry = 0
        while retry < retries:
            response = send_request(method='GET', url=get_room_info_url, token=token)
            for device in response['devices']:
                if device['type'] == device_type:
                    device_id = device['id']
                    break
            if not device_id:
                time.sleep(10)
            else:
                Report.logInfo(f'Device ID of {device_type} is {device_id}')
                break
            retry += 1
        return device_id

    except Exception as e:
        Report.logException(f'Error in getting Device ID from Device type {device_type}- {e}')
        raise e


def reboot_device(config, org_id: str, token: str, device: str, device_id: str):
    """
    Reboot device using Sync Portal
    """
    try:
        log.debug('Reboot device: {}'.format(device))
        post_device_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/reboot"
        data = {'deviceIds': [device_id], 'rebootNow': True}
        Report.logInfo('PUT call')
        Report.logInfo(post_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='POST', url=post_device_url, body=json.dumps(data), token=token
        )
        time.sleep(60)

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response of device reboot- {}'.format(json_formatted_response))
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_device_wallpaper(wallpaper_option, device):
    """
    Validate that the change related to BYOD wallpaper made via sync portal is applied to device.
    """
    try:
        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        time.sleep(60)
        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(5)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")
        time.sleep(5)

        device_ip = ''
        Report.logInfo(f"Connect to device- {device} using adb over network")
        if device == 'Kong':
            device_ip = fp.KONG_IP
        elif device == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device == 'HostedKong':
            device_ip = fp.HOSTEDKONG_IP
        elif device == 'HostedDiddy':
            device_ip = fp.HOSTEDDIDDY_IP
        elif device == 'Tiny':
            device_ip = fp.TINY_IP
        elif device == 'HostedTiny':
            device_ip = fp.HOSTEDTINY_IP
        process_helper.execute_command(f"adb connect {device_ip}:5555")
        time.sleep(5)

        Report.logInfo("Send adb command to check the byod wallpaper option: "
                       f"adb -s {device_ip} shell settings get secure byod_mode_preview")
        output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure byod_mode_preview")
        result = output[1]
        time.sleep(5)

        retries = 30
        retry = 0
        while retry < retries:
            if result == b'':
                process_helper.execute_command("adb disconnect")
                process_helper.execute_command("adb connect {}:5555".format(device_ip))
                time.sleep(5)
                output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure "
                                                        f"byod_mode_preview")
                result = output[1]
                time.sleep(5)
            else:
                break
            retry += 1
        command_output = int(result)
        Report.logInfo('Wallpaper option set via sync portal is {}'.format(wallpaper_option))
        Report.logInfo('BYOD Wallpaper present in device is {}'.format(command_output))
        assert command_output == int(wallpaper_option), 'Change in wallpaper did not get apply to device.'

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)
        return True

    except Exception as e:
        Report.logException(f'{e}')


def validate_wallpaper_option_persistence_after_reboot(config, org_id, token, current_wallpaper, device_id):
    """
    Validate the persistence of wallpaper option after reboot.
    """
    try:
        Report.logInfo('Validation of the persistence of wallpaper option after reboot')
        get_device_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo('Wait until device is back online in sync portal')
        time.sleep(60)
        response = send_request(
            method='GET', url=get_device_url, token=token
        )

        wallpaper_option = int(response['state']['reported']['byodSettings']['wallpaper'])
        Report.logInfo('Wallpaper option seen in sync portal is {}'.format(current_wallpaper))
        Report.logInfo('BYOD Wallpaper option seen in sync portal after device reboot {}'.format(wallpaper_option))
        if wallpaper_option == int(current_wallpaper):
            Report.logPass('Wallpaper option is {} and persists after reboot'.format(wallpaper_option))
        else:
            Report.logFail('Wallpaper does not persist after reboot.')
        assert wallpaper_option == int(current_wallpaper), 'Error in the wallpaper option'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_byod_wallpaper_option_sync_portal(wallpaper_option, set_wallpaper_option):
    """
    Validate wallpaper option via Sync Portal.
    """
    try:
        Report.logInfo('BYOD Wallpaper option set in sync portal {}'.format(wallpaper_option))
        Report.logInfo('Wallpaper option seen via device is {}'.format(set_wallpaper_option))
        if int(set_wallpaper_option) == int(wallpaper_option):
            Report.logPass('Wallpaper is successfully set to {}'.format(set_wallpaper_option))
        else:
            Report.logFail('Wallpaper did not set successfully')
        assert int(set_wallpaper_option) == int(wallpaper_option), 'Error in setting wallpaper option'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def set_the_wallpaper_via_device(byod_preview, device):
    """
        Set the BYOD wallpaper directly via device.
    """
    try:
        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(10)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")
        time.sleep(5)
        device_ip = ''
        Report.logInfo(f"Connect to device- {device} using adb over network")
        if device == 'Kong':
            device_ip = fp.KONG_IP
        elif device == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device == 'HostedKong':
            device_ip = fp.HOSTEDKONG_IP
        elif device == 'HostedDiddy':
            device_ip = fp.HOSTEDDIDDY_IP
        elif device == 'Tiny':
            device_ip = fp.TINY_IP
        elif device == 'HostedTiny':
            device_ip = fp.HOSTEDTINY_IP
        process_helper.execute_command(f"adb connect {device_ip}:5555")
        time.sleep(5)

        Report.logInfo(f"Send adb command to set BYOD wallpaper option: adb -s {device_ip} shell settings put secure "
                       f"byod_mode_preview {byod_preview}")
        output = process_helper.execute_command(f"adb -s {device_ip} shell settings put secure "
                                                f"byod_mode_preview {byod_preview}")
        result = output[1]
        retries = 30
        retry = 0
        while retry < retries:
            if result != b'':
                process_helper.execute_command("adb disconnect")
                process_helper.execute_command(f"adb connect {device_ip}:5555")
                time.sleep(5)
                output = process_helper.execute_command(f"adb -s {device_ip} shell settings put secure "
                                                        f"byod_mode_preview {byod_preview}")
                result = output[1]
                time.sleep(5)
            else:
                break
            retry += 1

        if result == b'':
            Report.logPass('BYOD wallpaper set to {} via device'.format(byod_preview))
        else:
            Report.logFail('Unable to set BYOD wallpaper via adb command.')
        assert result == b'', 'Error in setting byod wallpaper via adb command'

        time.sleep(30)

    except Exception as e:
        log.error("{}".format(e))
        raise e


def get_system_image(device_url, token):
    """
    Get system image of logi collab os device.
    """
    try:
        response = send_request(
            method='GET', url=device_url, token=token
        )
        return response['osv']

    except Exception as e:
        log.error("{}".format(e))
        raise e


def get_device(org_id, device_name, device_id, token):
    """
    Get Device information
    """
    try:
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        response = send_request(
            method='GET', url=get_device_url, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Response for GET Device API for {device_name}- {json_formatted_response}')
        return response

    except Exception as e:
        log.error("{}".format(e))
        raise e


def check_health_status_of_device(org_id, room_id, device_type, token):
    """
    Check health status of device
    """
    try:
        room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/" + room_id + "/info"
        Report.logInfo('GET Call')
        Report.logInfo(room_url)

        response = send_request(
            method='GET', url=room_url, token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response for GET Room Info - {}'.format(json_formatted_response))
        devices = response['devices']
        device_obj = dict()
        for device in devices:
            if device['type'] == device_type:
                device_obj = device
                break
        health_status = device_obj['state']['reported']['healthStatus']
        return health_status

    except Exception as e:
        log.error("{}".format(e))
        raise e


def check_update_status_of_device(org_id, room_id, device_type, token):
    try:
        """
        Check Update Status of device.
        """
        room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/" + room_id + "/info"
        Report.logInfo('GET Call')
        Report.logInfo(room_url)

        response = send_request(
            method='GET', url=room_url, token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response for GET Room Info - {}'.format(json_formatted_response))
        list_of_devices = response['devices']
        device_obj = dict()
        for device in list_of_devices:
            if device['type'] == device_type:
                device_obj = device
                break
        update_status = int(device_obj['state']['reported']['updateStatus'])
        Report.logInfo(f'UpdateStatus is {update_status}')
        return update_status

    except Exception as e:
        Report.logException(f'{e}')


def check_fw_update_availability(org_id, room_id, device_id, device_type, token):
    """
    Check firmware update availability of device
    """
    try:
        firmware_update_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + \
                              "/device/software"
        _data = {'deviceIds': [device_id]}

        response = send_request(
            method='POST', url=firmware_update_url, body=json.dumps(_data), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        status = raiden_validation_methods.validate_empty_response(response)
        assert status is True, 'Error in checking firmware update availability'
        update_status = check_update_status_of_device(org_id, room_id, device_type, token)
        return update_status

    except Exception as e:
        log.error("{}".format(e))
        raise e


def firmware_update_availability_check(org_id, room_id, device_id, device_type, token):
    """
    Firmware update availability check
    """
    try:
        Report.logInfo(f'Firmware update availability check for {device_type}')
        # Step 1: Verify that device is online
        retries = 30
        # Health Status -1 Unknown, 0 No Issues, 1 Warning, 2 Error.
        for r in range(retries):
            health_status = check_health_status_of_device(org_id, room_id, device_type, token)
            if health_status == 0 or health_status == 1:
                break
            else:
                time.sleep(10)

        # Step 2: Check for firmware update availability.
        update_status = check_fw_update_availability(org_id, room_id, device_id, device_type, token)
        for _ in range(retries):
            if update_status == 1 or update_status == 8:
                break
            else:
                update_status = check_fw_update_availability(org_id, room_id, device_id, device_type, token)
                time.sleep(10)
        return update_status

    except Exception as e:
        Report.logException(f'{e}')


def set_update_channel_via_adb(device_name):
    """
    Set Update Channel of device via adb commands.
    """
    try:
        fw_ota = global_variables.SYNC_FWOTA
        list_fw_ota = fw_ota.split('-')
        ota_server = list_fw_ota[1]
        ota_channel = list_fw_ota[2]
        ota_servers_url = {'prod': 'updates.vc.logitech.com', 'staging': 'updates-staging.vc.logitech.com'}
        Report.logInfo(f'Set Update channel to the {device_name} via adb')
        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(20)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")

        device_ip = ''
        Report.logInfo("Connect to device using adb over network")
        if device_name == 'Kong':
            device_ip = fp.KONG_IP
        elif device_name == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device_name == 'Sega':
            device_ip = fp.SEGA_IP
        if device_name == 'Atari':
            device_ip = fp.ATARI_IP
        elif device_name == 'Nintendo':
            device_ip = fp.NINTENDO_IP
        elif device_name == 'Tiny':
            device_ip = fp.TINY_IP
        elif device_name == 'Coily':
            device_ip = fp.COILY_IP

        Report.logInfo(f"adb over internet")
        process_helper.execute_command(f"adb connect {device_ip}:5555")

        Report.logInfo(f"adb s {device_ip} root")
        process_helper.execute_command(f"adb -s {device_ip} root")

        # Set OTA server
        Report.logInfo(f"Send adb command to set OTA server: adb -s {device_ip} shell setprop "
                       f"persist.logi.fwupd.ota-server-url {ota_servers_url[ota_server]}")
        process_helper.execute_command(f"adb -s {device_ip} shell setprop persist.logi.fwupd.ota-server-url "
                                       f"{ota_servers_url[ota_server]}")

        # Set Update Channel
        Report.logInfo(f"Send adb command to set the update channel: adb -s {device_ip} shell "
                       f"setprop persist.logi.fwupd.ota.channel {ota_channel}")
        process_helper.execute_command(f"adb -s {device_ip} shell setprop persist.logi.fwupd.ota.channel "
                                       f"{ota_channel}")

        # Reboot the device.
        Report.logInfo('Reboot the device')
        Report.logInfo(f"adb -s {device_ip} reboot")
        reboot_command = f"adb -s {device_ip} reboot"
        os.popen(reboot_command)
        Report.logInfo('Device is rebooting')
        time.sleep(30)

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")

    except Exception as e:
        Report.logException(f'{e}')


def trigger_firmware_update_via_sync_portal(org_id, device_id, device_type, token):
    """
    Trigger firmware update via Sync Portal Update Now.
    """
    try:
        Report.logInfo(f'Trigger firmware update of {device_type} via Update Now')
        firmware_update_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + \
                              "/device/software"
        _data = {'deviceIds': [device_id], "updateNow": True}

        response = send_request(
            method='POST', url=firmware_update_url, body=json.dumps(_data), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response after triggering firmware update via Sync Portal- {}'.format(json_formatted_response))
        time.sleep(60)

    except Exception as e:
        Report.logException(f'{e}')


def validate_rs_mode_option_group_view_persistence_after_reboot(org_id, token, rs_data,
                                                                system_image_version, device_name, device_id):
    """
    Validate the persistence of right sight mode option after reboot.
    """
    try:
        Report.logInfo(f'Validation of the persistence of rightsight mode option after reboot for {device_name}')
        Report.logInfo('Wait until device is back online in sync portal')
        response_get_device = get_device(org_id, device_name, device_id, token)
        state_get_device = response_get_device['status']
        retries = 30
        retry = 0
        while retry < retries:
            if state_get_device != 'Available':
                time.sleep(10)
            else:
                break
            retry += 1

        response = get_device(org_id, device_name, device_id, token)
        rs_option = response['state']['reported']['rightSight']

        if system_image_version >= float(912.97):
            # Tracking mode: Group View
            rs_tracking_mode_data = int(rs_data['trackingMode'])
            rs_tracking_mode_portal = int(rs_option['trackingMode'])
            Report.logInfo('Rightsight tracking mode in sync portal is {}'.format(rs_tracking_mode_data))
            Report.logInfo(
                'Rightsight tracking mode seen in sync portal after device reboot {}'.format(rs_tracking_mode_portal))
            if rs_tracking_mode_data == rs_tracking_mode_portal:
                Report.logPass(
                    'Rightsight  tracking data is {} and persists after reboot'.format(rs_tracking_mode_portal))
            else:
                Report.logFail('Rightsight tracking mode does not persist after reboot.')
            assert rs_tracking_mode_data == rs_tracking_mode_portal, 'Error in the rightsight tracking mode'

        # Mode: Dynamic vs On Call Start
        rs_mode_data = int(rs_data['mode'])
        rs_mode_portal = int(rs_option['mode'])
        Report.logInfo('Rightsight mode in sync portal is {}'.format(rs_mode_data))
        Report.logInfo('Rightsight mode seen in sync portal after device reboot {}'.format(rs_mode_portal))
        if rs_mode_data == rs_mode_portal:
            Report.logPass('Rightsight data is {} and persists after reboot'.format(rs_mode_portal))
        else:
            Report.logFail('Rightsight mode does not persist after reboot.')
        assert rs_mode_data == rs_mode_portal, 'Error in the rightsight mode'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_rs_mode_option_speaker_view_persistence_after_reboot(org_id, token, rs_data, device_name, device_id):
    """
    Validate the persistence of right sight mode option after reboot.
    """
    try:
        Report.logInfo(f'Validation of the persistence of rightsight mode option after reboot for {device_name}')
        Report.logInfo('Wait until device is back online in sync portal')

        response = get_device(org_id, device_name, device_id, token)
        rs_option = response['state']['reported']['rightSight']

        # Tracking mode: Speaker View
        rs_tracking_mode_data = int(rs_data['trackingMode'])
        rs_tracking_mode_portal = int(rs_option['trackingMode'])
        Report.logInfo('Rightsight tracking mode in sync portal is {}'.format(rs_tracking_mode_data))
        Report.logInfo(
            'Rightsight tracking mode seen in sync portal after device reboot {}'.format(rs_tracking_mode_portal))
        if rs_tracking_mode_data == rs_tracking_mode_portal:
            Report.logPass('Rightsight  tracking data is {} and persists after reboot'.format(rs_tracking_mode_portal))
        else:
            Report.logFail('Rightsight tracking mode does not persist after reboot.')
        assert rs_tracking_mode_data == rs_tracking_mode_portal, 'Error in the rightsight tracking mode'

        # Picture in Picture option
        rs_pip_data = bool(rs_data['pip'])
        rs_pip_portal = bool(rs_option['pip'])
        Report.logInfo('Rightsight picture in picture mode in sync portal is {}'.format(rs_pip_data))
        Report.logInfo('Rightsight picture in picture mode seen in sync portal after device reboot {}'
                       .format(rs_pip_portal))
        if rs_pip_data == rs_pip_portal:
            Report.logPass('Rightsight picture in picture data is {} and persists after reboot'.format(rs_pip_portal))
        else:
            Report.logFail('Rightsight picture in picture data does not persist after reboot.')
        assert rs_pip_data == rs_pip_portal, 'Error in the rightsight pip data'

        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_righsight_state(config, org_id, token, rs_data, device_id):
    """
    Validate the persistence of right sight mode option after reboot.
    """
    try:
        Report.logInfo('Validation of the persistence of rightsight mode option after reboot')
        get_device_url = get_device_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo('Wait until device is back online in sync portal')
        time.sleep(60)
        response = send_request(
            method='GET', url=get_device_url, token=token
        )

        rs_option = response['state']['reported']['rightSight']

        # Rightsight state persistence after reboot.
        rs_state_data = int(rs_data['on'])
        rs_state_portal = int(rs_option['on'])
        Report.logInfo('Rightsight is {}'.format(rs_state_data))
        Report.logInfo('Rightsight in sync portal after device reboot {}'.format(rs_state_portal))
        if rs_state_data == rs_state_portal:
            Report.logPass('Rightsight is {} and persists after reboot'.format(rs_state_portal))
        else:
            Report.logFail('Rightsight does not persist after reboot.')
        assert rs_state_data == rs_state_portal, 'Error in the rightsight'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_change_made_in_setting_is_applied_to_device(name_of_setting, setting_set_via_portal,
                                                         device):
    """
    Validate that the change made in setting via Sync Portal is applied to the device.
    """
    try:
        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(20)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")

        device_ip = ''
        Report.logInfo("Connect to device using adb over network")
        if device == 'Kong':
            device_ip = fp.KONG_IP
        elif device == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device == 'HostedKong':
            device_ip = fp.HOSTEDKONG_IP
        elif device == 'HostedDiddy':
            device_ip = fp.HOSTEDDIDDY_IP
        elif device == 'Tiny':
            device_ip = fp.TINY_IP
        elif device == 'HostedTiny':
            device_ip = fp.HOSTEDTINY_IP

        process_helper.execute_command(f"adb connect {device_ip}:5555")
        Report.logInfo(f"Send adb command to check: adb -s {device_ip} shell settings get secure {name_of_setting}")

        def get_setting_via_adb():
            output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure {name_of_setting}")
            result = output[1]
            retries = 30
            retry = 0
            while retry < retries:
                if result == b'':
                    process_helper.execute_command("adb disconnect")
                    process_helper.execute_command(f"adb connect {device_ip}:5555")
                    time.sleep(5)
                    output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure "
                                                            f"{name_of_setting}")
                    result = output[1]
                    time.sleep(5)
                else:
                    break
                retry += 1
            return result

        result = get_setting_via_adb()
        command_output = str(result.decode("utf-8")).strip()
        time.sleep(5)

        # Logi Collab OS device could be sometimes busy and it could take some time to propagate the change made in
        # Sync Portal to propagate to the device. We can set 5 tries to see that the change set in sync portal
        # matches that of device after end of each try.
        retries = 30
        retry = 0
        while retry < retries:
            if command_output != str(setting_set_via_portal):
                result = get_setting_via_adb()
                command_output = str(result.decode("utf-8")).strip()
            else:
                break
            retry += 1

        Report.logInfo('{0} setting set via sync portal is {1}'.format(name_of_setting, setting_set_via_portal))
        Report.logInfo('{0} setting present in device is {1}'.format(name_of_setting, command_output))
        assert command_output == str(setting_set_via_portal), 'Change did not get apply to device.'

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")

        return True

    except Exception as e:
        Report.logException(f'{e}')


def validate_setting_preservation_after_reboot(config, org_id, token, device_id, name_of_setting, expected_setting):
    """
        Validate the preservation of setting after reboot.
    """
    try:
        Report.logInfo('Validation of the persistence of {} after reboot.'.format(name_of_setting))
        get_device_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo('Wait until device is back online in sync portal')
        time.sleep(60)

        response = send_request(
            method='GET', url=get_device_url, token=token
        )

        setting_sync_portal = response['state']['reported']['rightSight'][name_of_setting]

        # Setting preservation after reboot.
        Report.logInfo('{0} is {1}'.format(name_of_setting, expected_setting))
        Report.logInfo('{0} in sync portal after device reboot {1}'.format(name_of_setting, setting_sync_portal))
        if expected_setting == setting_sync_portal:
            Report.logPass('{0} persists after reboot-{1}'.format(name_of_setting, setting_sync_portal))
        else:
            Report.logFail('{0} does not persist after reboot-{1}'.format(name_of_setting, setting_sync_portal))
        assert expected_setting == setting_sync_portal, 'Error in the setting observed in sync portal.'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_expected_setting_rightsight(config, org_id, token, device_id, name_of_setting, expected_setting):
    """
        Validate that sync portal displays the expected setting.
    """
    try:
        Report.logInfo('Validation that sync portal displays the expected setting for {}'.format(name_of_setting))
        time.sleep(10)
        get_device_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        response = send_request(
            method='GET', url=get_device_url, token=token
        )
        setting_sync_portal = response['state']['reported']['rightSight'][name_of_setting]
        if expected_setting == setting_sync_portal:
            Report.logPass('{0} Setting in sync portal- {1} matches expected setting-{2}'.format(name_of_setting,
                                                                                                 setting_sync_portal,
                                                                                                 expected_setting))
        else:
            Report.logFail(
                '{0} Setting in sync portal- {1} does not match the expected setting-{2}'.format(name_of_setting,
                                                                                                 setting_sync_portal,
                                                                                                 expected_setting))
        assert expected_setting == setting_sync_portal, 'Error in the setting observed in sync portal'
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def get_room_id_from_room_name(config, org_id: str, room_name: str, token: str):
    """
     Get room id from room name.
    """
    try:
        # Step 1: Get the Room ID of the provided room name.
        get_rooms_in_organization_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/room'
        room_id = None
        retries = 10
        retry = 0
        while retry < retries:
            response = send_request(method='GET', url=get_rooms_in_organization_url, token=token)
            if len(response):
                for index in range(len(response)):
                    if str(response[index]['name']) == str(room_name):
                        room_id = response[index]['id']
                        break
            if not room_id:
                time.sleep(10)
            else:
                Report.logInfo(f'Room ID of the room {room_name} is {room_id}')
                break
            retry += 1
        return room_id

    except Exception as e:
        Report.logException(f"Error in getting the Room ID from Room Name - {e}")
        raise e


def get_setting_via_adb(name_of_setting: str, device_ip: str):
    """
    Get the value associated to the setting via adb
    """
    try:
        output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure {name_of_setting}")
        result = output[1]
        retries = 30
        retry = 0
        while retry < retries:
            if result == b'':
                process_helper.execute_command("adb disconnect")
                process_helper.execute_command("adb connect {}:5555".format(device_ip))
                time.sleep(5)

                output = process_helper.execute_command(f"adb -s {device_ip} shell settings get secure "
                                                        f"{name_of_setting}")
                result = output[1]
                time.sleep(5)
            else:
                break
            retry += 1
        command_output = str(result.decode("utf-8")).strip()
        return command_output

    except Exception as e:
        log.error("{}".format(e))
        raise e


def get_device_ip(device_name: str):
    """
    Get the device IP of the device.
    """
    try:
        Report.logInfo(f'Device Name - {device_name}')
        device_ip = ''
        if device_name == 'Kong':
            device_ip = fp.KONG_IP
        elif device_name == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device_name == 'HostedKong':
            device_ip = fp.HOSTEDKONG_IP
        elif device_name == 'HostedDiddy':
            device_ip = fp.HOSTEDDIDDY_IP
        elif device_name == 'Sega':
            device_ip = fp.SEGA_IP
        if device_name == 'Atari':
            device_ip = fp.ATARI_IP
        elif device_name == 'Nintendo':
            device_ip = fp.NINTENDO_IP
        elif device_name == 'Tiny':
            device_ip = fp.TINY_IP
        elif device_name == 'HostedTiny':
            device_ip = fp.HOSTEDTINY_IP
        return device_ip

    except Exception as e:
        log.error("{}".format(e))
        raise e


def validate_move_device(room_name: str, seat_count: int, device: str, device_ip: str):
    """
    Validate that the device is moved successfully to the provided room.
    """
    try:
        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(10)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")

        Report.logInfo("Connect to device using adb over network")
        process_helper.execute_command("adb connect {}:5555".format(device_ip))

        name_of_room = get_setting_via_adb(name_of_setting='room_name', device_ip=device_ip)
        seat_count_of_room = int(get_setting_via_adb(name_of_setting='seat_count', device_ip=device_ip))

        Report.logInfo('{0} moved to the meeting room: {1} with seat count: {2} '.format(device, name_of_room,
                                                                                         seat_count_of_room))

        if name_of_room == room_name:
            Report.logPass('{0} Device is moved to the meeting room-{1}'.format(device, room_name))
        else:
            Report.logFail('{0} Device is not moved to the meeting room-{1}'.format(device, room_name))

        if seat_count_of_room == seat_count:
            Report.logPass('{0} Device is moved to the meeting room-{1} '
                           'with seat count-{2}'.format(device, room_name, seat_count))
        else:
            Report.logFail('{0} Device is not moved to the meeting room-{1} '
                           'with seat count-{2}'.format(device, room_name, seat_count))

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)
        return True

    except Exception as e:
        log.error("{}".format(e))
        raise e


def get_device_information_of_celestia(device_url: str, token: str) -> dict:
    """
    Get Device information of Celestia.
    """
    try:
        response = send_request(
            method='GET', url=device_url, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(f'{json_formatted_response}')
        log.info(f'Get Device information of Scribe- {json_formatted_response}')
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_whiteboard_settings_of_celestia(device_url: str, token: str) -> tuple:
    """
    Get Whiteboard settings of celestia
    """
    try:
        response = send_request(
            method='GET', url=device_url, token=token
        )

        whiteboard_settings = response['state']['reported']['whiteboardSettings']

        json_formatted_response = json.dumps(whiteboard_settings, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Whiteboard settings of the device- {json_formatted_response}')

        return response, whiteboard_settings

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def put_whiteboard_settings_of_celestia(device_url: str, token: str, payload: dict) -> dict:
    """
    Update whiteboard settings of celestia.
    """
    try:
        Report.logInfo(f'PUT API call to update whiteboard settings')
        Report.logInfo(f'Payload is {payload}')

        response = send_request(
            method='PUT', url=device_url, body=json.dumps(payload), token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Whiteboard settings of device- {json_formatted_response}')
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def add_empty_room(room_name, seat_count, org_id, token):
    """
    Method to create empty room

    :param room_name:
    :param org_id:
    :param token:
    """
    try:
        Report.logInfo(f'Room name is {room_name}')
        rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/rooms/"
        payload = {
            "realm": "Rooms",
            "group": "/",
            "rooms": [
                {
                    "name": room_name,
                    "seatCount": seat_count
                }]
        }
        response = send_request(
            method='POST', url=rooms_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))

        # Get provision code
        room_id = response[0]['id']
        room_prov_code_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + \
                             "/room/" + str(room_id) + "/prov-code"
        response_prov_code = send_request(
            method='GET', url=room_prov_code_url, token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logInfo('Get Provision code')
        Report.logResponse(format(json_formatted_response))
        status_prov_code = _validate_get_prov_code(response_prov_code)
        assert status_prov_code is True, 'Error in getting prov code'
        return response_prov_code['code'], room_id

    except Exception as e:
        Report.logException(f'{e}')


def _validate_get_prov_code(response: dict):
    """
    Validate that get prov code.
    """
    try:
        if response['code']:
            Report.logPass(f'Got the code. Received response- {response}')
            return True
        else:
            Report.logFail('Error in response')

    except Exception as e:
        Report.logException('Exception occurred- {}'.format(e))


def delete_room(room_name, org_id, token):
    """
    Delete room

    :param room_id:
    :param org_id:
    :param token:
    """
    try:
        Report.logInfo(f'Deleting room - {room_name}')
        delete_room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/delete/"
        room_id = get_room_id_from_room_name(global_variables.config, org_id, room_name, token)
        payload = {
            "roomIds": [
                str(room_id),
            ]
        }
        response = send_request(
            method='POST', url=delete_room_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        status = raiden_validation_methods.validate_empty_response(response)
        assert status is True, 'Error in status'

    except Exception as e:
        Report.logException(f'{e}')


def delete_desk(desk_id, org_id, token):
    """
    Delete Desk

    :param desk_id:
    :param org_id:
    :param token:
    """
    try:
        Report.logInfo(f'Deleting Desk with ID: {desk_id}')
        delete_room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/delete/"
        payload = {
            "roomIds": [
                str(desk_id)
            ]
        }
        response = send_request(
            method='POST', url=delete_room_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        status = raiden_validation_methods.validate_empty_response(response)
        assert status is True, 'Error in status'

    except Exception as e:
        Report.logException(f'{e}')


def delete_site(site_name, org_id, token):
    """
    Delete Site

    :param site_name:
    :param org_id:
    :param token:
    """
    try:
        Report.logInfo(f'Remove Site - {site_name}')
        update_groups_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + \
                            "/update-groups"
        payload = {
            "operation": "Remove",
            "target": site_name + '/',
            "realm": "Desks"
        }

        response = send_request(
            method='POST', url=update_groups_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))

    except Exception as e:
        Report.logException(f'{e}')


def post_room_note(org_id, room_id, room_note, token):
    """
    Add room note
    """
    try:
        room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + \
                   "/room/" + room_id + "/note"
        data = {'text': room_note}

        Report.logInfo('POST Call')
        Report.logInfo(room_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='POST', url=room_url, body=json.dumps(data), token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response for POST Room note to room- {}'.format(json_formatted_response))
        return response

    except Exception as e:
        Report.logException(f'{e}')


def view_room_note(org_id, room_id, token):
    """
    View room note
    """
    try:
        room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/" + room_id + "/info"
        Report.logInfo('GET Call')
        Report.logInfo(room_url)

        response = send_request(
            method='GET', url=room_url, token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response for GET Room note - {}'.format(json_formatted_response))
        return response

    except Exception as e:
        Report.logException(f'{e}')


def delete_room_note(org_id, room_id, token):
    """
    Delete room note
    """
    try:
        room_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/room/" + room_id + "/note"

        Report.logInfo('DELETE Call')
        Report.logInfo(room_url)

        response = send_request(
            method='Delete', url=room_url, token=token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info('Response for Delete Room note to room- {}'.format(json_formatted_response))
        return response

    except Exception as e:
        Report.logException(f'{e}')


def get_system_image_version(org_id, device_name, token, room_name):
    """
    Get System image version
    """
    try:
        device_id = get_device_id_from_room_name(global_variables.config, room_name, org_id, token, device_name)

        device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + \
                     org_id + "/device/" + device_id
        response = send_request(
            method='GET', url=device_url, token=token
        )
        system_image = response['osv']
        Report.logInfo(f'System image version is {system_image}')
        system_image_version = float('.'.join(system_image.split('.')[1:]))
        return system_image_version

    except Exception as e:
        Report.logException(f'{e}')


def change_rightsight_setting(org_id, device_id, rs_setting, data, token):
    """
    Change rightsight setting
    """
    try:
        Report.logInfo(f'PUT call- Changing RightSight to {rs_setting}')
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo(get_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='PUT', url=get_device_url, body=json.dumps(data), token=token
        )
        time.sleep(2)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for changing rightsight to {rs_setting}- {json_formatted_response}')
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        Report.logException(f'{e}')


def change_audio_settings(org_id, device_id, data, token):
    """
    Change audio setting
    """
    try:
        Report.logInfo(f'PUT call- Changing Audio Settings to {data}')
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo(get_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='PUT', url=get_device_url, body=json.dumps(data), token=token
        )
        time.sleep(2)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for updated audio settings- {json_formatted_response}')
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        Report.logException(f'{e}')


def change_bluetooth_setting(org_id, device_id, data, token):
    """
    Change bluetooth setting
    """
    try:
        Report.logInfo(f'PUT call- Changing Bluetooth Setting to {data}')
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo(get_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='PUT', url=get_device_url, body=json.dumps(data), token=token
        )
        time.sleep(2)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for updated audio settings- {json_formatted_response}')
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        Report.logException(f'{e}')


def change_setting(setting_name, setting_value, org_id, device_id, data, token):
    """
    Change audio setting
    """
    try:
        Report.logInfo(f'PUT call- Changing {setting_name} setting to {setting_value}')
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + device_id
        Report.logInfo(get_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='PUT', url=get_device_url, body=json.dumps(data), token=token
        )
        time.sleep(2)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for updated {setting_name} settings- {json_formatted_response}')
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        Report.logException(f'{e}')


def change_lna_password(org_id, device_id, data, token):
    """
    Change the password of Local Network Access for the device.
    """
    try:
        Report.logInfo(f'POST call- Change password of Local Network Access')
        get_device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/device/" + \
                         device_id + '/lna-password'
        Report.logInfo(get_device_url)
        Report.logInfo(format(json.dumps(data, indent=2)))

        response = send_request(
            method='POST', url=get_device_url, body=json.dumps(data), token=token
        )
        time.sleep(2)
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response for updated password of LNA- {json_formatted_response}')
        status_response = raiden_validation_methods.validate_empty_response(response)
        return status_response

    except Exception as e:
        Report.logException(f'{e}')


def raiden_parameters_override(device, env):
    """
    Override the raiden parameters for Collab OS devices in appliance mode.
    """
    try:
        Report.logInfo(f"Connect to device- {device} using adb over network")
        if device == 'Kong':
            device_ip = fp.KONG_IP
        elif device == 'Diddy':
            device_ip = fp.DIDDY_IP
        elif device == 'HostedKong':
            device_ip = fp.HOSTEDKONG_IP
        elif device == 'HostedDiddy':
            device_ip = fp.HOSTEDDIDDY_IP
        elif device == 'Sega':
            device_ip = fp.SEGA_IP
        elif device == 'Atari':
            device_ip = fp.ATARI_IP
        elif device == 'Nintendo':
            device_ip = fp.NINTENDO_IP
        elif device == 'Tiny':
            device_ip = fp.TINY_IP
        elif device == 'HostedTiny':
            device_ip = fp.HOSTEDTINY_IP
        elif device == 'Coily':
            device_ip = fp.COILY_IP
        else:
            raise Exception("Invalid device name")
        override_collabos_raiden_parameters(device_name=device, device_ip=device_ip, env=env)

    except Exception as e:
        Report.logException(f'{e}')


def override_collabos_raiden_parameters(device_name: str, device_ip: str, env: str):
    """
    Override the raiden parameters for Collab OS devices in appliance mode based on device_ip and env.
    :param device_name: CollabOS device IP Address
    :param device_ip: CollabOS device Name
    :param env: Raiden Environment
    :return :
    """
    try:
        Report.logInfo(f'Override the raiden parameters for {device_name} based on raiden env: {env}')

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

        Report.logInfo("Start adb server")
        process_helper.execute_command("adb start-server")
        time.sleep(10)

        Report.logInfo("Disconnect existing devices")
        process_helper.execute_command("adb disconnect")
        time.sleep(5)

        Report.logInfo(f"Connect to device- {device_name} using adb over network")

        process_helper.execute_command(f"adb connect {device_ip}:5555")
        time.sleep(5)

        parameters = raiden_parameters.parameters[env]
        Report.logInfo(f"Send adb commands to override the raiden parameters to environment {env}")
        for parameter in parameters:
            parameter1 = parameter[0:3]
            parameter2 = parameter[3:]
            Report.logInfo(parameter1 + f" -s {device_ip}" + parameter2)
            process_helper.execute_command(parameter1 + f" -s {device_ip}" + parameter2)
            time.sleep(5)

        Report.logInfo('Reboot the device')
        Report.logInfo(f"adb -s {device_ip} reboot")
        reboot_command = f"adb -s {device_ip} reboot"
        os.popen(reboot_command)
        Report.logInfo('Device is rebooting')
        time.sleep(15)

        Report.logInfo("Stop adb server")
        process_helper.execute_command("adb kill-server")
        time.sleep(5)

    except Exception as e:
        Report.logException(f'{e}')


def create_new_channel_name(role: str) -> dict:
    """
        Creating the new channel info dictionary

        :param role: Role of logged in user
        :return:
        """
    try:
        Report.logInfo(f'{role}- Creating new channel')
        MAX = 100000000
        _id = str(random.randint(0, MAX))
        test_channel = 'vc.qa.raiden+testchannel_'
        channel_name = f'{test_channel}{_id}'
        return {
            'name': [channel_name]
        }
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def add_room_group(role: str, token: str, org_id: str, room_group: str) -> bool:
    """
    Add room group.
    """
    try:
        Report.logInfo(f"{role} - Add room group")
        update_groups_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/update-groups"
        realm_name_sync = 'Rooms'
        payload = {'operation': "Add", 'target': f"/{room_group}", 'realm': realm_name_sync}
        response_sync = send_request(
            method='POST', url=update_groups_url, body=payload, token=token
        )
        json_formatted_response_sync = json.dumps(response_sync, indent=2)
        Report.logResponse(format(json_formatted_response_sync))
        status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                           room_group)
        if status_add_room_group_sync:
            Report.logPass(f"Added room group - {room_group} to the list of room groups present in the organization")
        else:
            Report.logFail(f"Error in adding room group {room_group} to the list of room groups in the organization")
        return status_add_room_group_sync

    except Exception as e:
        Report.logException(e)


def view_room_group(role: str, token: str, org_id: str, room_group: str) -> bool:
    """
    View room group.
    """
    try:
        Report.logInfo(f"{role} - Get the room group")
        get_room_group_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}"
        Report.logInfo(get_room_group_url)
        response = send_request(
            method='GET', url=get_room_group_url, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        room_groups = response['groups']['tree']
        status_get_room_group = False
        for group in room_groups.keys():
            if group == room_group:
                status_get_room_group = True
                break
        if status_get_room_group:
            Report.logPass(f"Viewed room group - {room_group} in the list of room groups present in the organization")
        else:
            Report.logFail(f"Error in getting room group {room_group} from the list of room groups in the organization")
        return status_get_room_group

    except Exception as e:
        Report.logException(e)


def rename_room_group(role: str, token: str, org_id: str, existing_room_group: str, renamed_room_group: str) -> bool:
    """
    Rename room group.
    """
    try:
        Report.logInfo(f"{role} - Rename room group.")
        realm_name_rooms = 'Rooms'
        update_groups_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/rename-group"
        payload = {"name": f"{renamed_room_group}",
                   "target": f"/{existing_room_group}/",
                   "realm": realm_name_rooms}
        response = send_request(
            method='PUT', url=update_groups_url, body=payload, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        log.info(f'Response- {json_formatted_response}')
        status_renamed_room_group_sync = raiden_validation_methods.validate_group_name_is_modified(
            response, existing_room_group, renamed_room_group)
        if status_renamed_room_group_sync:
            Report.logPass(f"Renamed the room group")
        else:
            Report.logFail(f"Error in renaming the room group")
        return status_renamed_room_group_sync

    except Exception as e:
        Report.logException(e)


def delete_room_group(role: str, token: str, org_id: str, room_group: str) -> bool:
    """
    Delete room group.
    """
    try:
        Report.logInfo(f'{role} - Delete room group.')
        realm_name_rooms = 'Rooms'
        delete_group_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/update-groups"
        payload = {
            "operation": "Remove",
            "target": f"/{room_group}//",
            "realm": realm_name_rooms
        }
        response = send_request(
            method='POST', url=delete_group_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        list_of_remaining_groups = response.keys()
        status_delete_room_group = False
        if room_group not in list_of_remaining_groups:
            status_delete_room_group = True
        return status_delete_room_group

    except Exception as e:
        Report.logException(e)


def add_host_group(role: str, token: str, org_id: str, host_group: str) -> bool:
    """
    Add host group.
    """
    try:
        Report.logInfo(f"{role} - Add host group")
        update_groups_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/update-groups"
        realm_name_personal = 'Personal'
        payload = {'operation': "Add", 'target': f"/{host_group}", 'realm': realm_name_personal}
        response_sync = send_request(
            method='POST', url=update_groups_url, body=payload, token=token
        )
        json_formatted_response_sync = json.dumps(response_sync, indent=2)
        Report.logResponse(format(json_formatted_response_sync))
        status_add_room_group_sync = raiden_validation_methods.validate_group_is_available(response_sync,
                                                                                           host_group)
        if status_add_room_group_sync:
            Report.logPass(f"Added host group - {host_group} to the list of host groups present in Personal Devices")
        else:
            Report.logFail(f"Error in adding room group {host_group} to the list of room groups in Personal Devices")
        return status_add_room_group_sync

    except Exception as e:
        Report.logException(e)


def view_host_group(role: str, token: str, org_id: str, host_group: str) -> bool:
    """
    View host group.
    """
    try:
        Report.logInfo(f"{role} - Get the host group")
        get_room_group_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}"
        Report.logInfo(get_room_group_url)
        response = send_request(
            method='GET', url=get_room_group_url, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        room_groups = response['groups']['host']
        status_get_room_group = False
        for group in room_groups.keys():
            if group == host_group:
                status_get_room_group = True
                break
        if status_get_room_group:
            Report.logPass(f"Viewed host group - {host_group} in the list of host groups present in personal devices")
        else:
            Report.logFail(f"Error in getting room group {host_group} from the list of room groups in personal devices")
        return status_get_room_group

    except Exception as e:
        Report.logException(e)


def rename_host_group(role: str, token: str, org_id: str, existing_host_group: str, renamed_host_group: str) -> bool:
    """
    Rename host group.
    """
    try:
        Report.logInfo(f'{role} - Rename host group.')
        realm_name_personal = 'Personal'
        update_groups_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/rename-group"
        payload = {"name": f"{renamed_host_group}",
                   "target": f"/{existing_host_group}/",
                   "realm": realm_name_personal}
        response = send_request(
            method='PUT', url=update_groups_url, body=payload, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        status_renamed_room_group_sync = raiden_validation_methods.validate_group_name_is_modified(
            response, existing_host_group, renamed_host_group)
        if status_renamed_room_group_sync:
            Report.logPass(f"Renamed the host group")
        else:
            Report.logFail(f"Error in renaming the host group")
        return status_renamed_room_group_sync

    except Exception as e:
        Report.logException(e)


def delete_host_group(role: str, token: str, org_id: str, host_group: str) -> bool:
    """
    Delete room group.
    """
    try:
        Report.logInfo(f'{role} - Delete host group.')
        realm_name_personal = 'Personal'
        delete_group_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/update-groups"
        payload = {
            "operation": "Remove",
            "target": f"/{host_group}//",
            "realm": realm_name_personal
        }
        response = send_request(
            method='POST', url=delete_group_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        list_of_remaining_groups = response.keys()
        status_delete_room_group = False
        if host_group not in list_of_remaining_groups:
            status_delete_room_group = True
        return status_delete_room_group

    except Exception as e:
        Report.logException(e)


def edit_tapscheduler_host_name(self, room_name: str, room_id: str, token: str, org_id: str, device_id: str,
                                tapscheduler_host_name: str):
    """
            Method to edit tap scheduler user name
            :param token:token to authenticate user
            :param org_id:Organization id
            :param room_name: name of the room
            :param room_id:Id for the desk created
            :param device_id: Device id of Tap Scheduler
            :param tapscheduler_host_name: initial host name of tap scheduler device
        """
    try:

        updated_host_name = tapscheduler_host_name + '-test'
        Report.logInfo(f'Tap Scheduler host name will be updated to: {updated_host_name}')

        edit_tapscheduler_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
        Report.logInfo(f'Url to edit tap scheduler host name is: {edit_tapscheduler_host_name_url}')

        edit_tapscheduler_host_name_payload = {
            'systemSettings': {
                'hostName': updated_host_name
            }
        }

        response_edit_tapscheduler_host_name = send_request(
            method='PUT', url=edit_tapscheduler_host_name_url, body=json.dumps(edit_tapscheduler_host_name_payload),
            token=token
        )

        Report.logInfo('Device is rebooting after editing the host name')

        retries = 30
        for retry in range(0, retries):

            response_get_device_status = get_room_booking_device_information(self, room_name, room_id, token, org_id)
            bootStatus_after_hostname_edit = response_get_device_status['devices'][0]['state']['reported'][
                'bootStatus']

            if bootStatus_after_hostname_edit == 0:
                break
            else:
                time.sleep(10)

        json_formatted_response = json.dumps(response_edit_tapscheduler_host_name, indent=2)
        Report.logInfo(f'Edit tap scheduler host name:')
        Report.logResponse(json_formatted_response)

        # Validate Response
        for i in range(20):
            get_tapscheduler_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{room_id}/info'

            response_get_tapscheduler_updated_host_name = send_request(
                method='GET', url=get_tapscheduler_host_name_url,
                token=token
            )

            time.sleep(5)

            if len(response_get_tapscheduler_updated_host_name['devices']) >= 1:
                if 'systemSettings' in response_get_tapscheduler_updated_host_name['devices'][0]['state']['reported']:
                    tapscheduler_updated_host_name = \
                    response_get_tapscheduler_updated_host_name['devices'][0]['state']['reported']['systemSettings'][
                        'hostName']
                    Report.logInfo(f'Tap scheduler updated host name is: {tapscheduler_updated_host_name}')
                    break

        if tapscheduler_updated_host_name == updated_host_name:
            Report.logPass(f'Tap scheduler host name is updated successfully')
        else:
            Report.logFail(f'Tap scheduler host name didnot update')

        # Set the hostname of Nintendo back to its initial name.
        if tapscheduler_updated_host_name == updated_host_name:

            reset_tapscheduler_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/device/{device_id}'
            Report.logInfo(f'Url to reset tap scheduler host name is: {reset_tapscheduler_host_name_url}')

            reset_tapscheduler_host_name_payload = {
                'systemSettings': {
                    'hostName': tapscheduler_host_name
                }
            }

            response_reset_flexdesk_host_name = send_request(
                method='PUT', url=reset_tapscheduler_host_name_url,
                body=json.dumps(reset_tapscheduler_host_name_payload),
                token=token
            )

            Report.logInfo('Device is rebooting after reseting the host name')

            retries = 30
            for retry in range(0, retries):

                response_get_device_status = get_room_booking_device_information(self, room_name, room_id, token,
                                                                                 org_id)
                bootStatus_after_hostname_reset = response_get_device_status['devices'][0]['state']['reported'][
                    'bootStatus']

                if bootStatus_after_hostname_reset == 0:
                    break
                else:
                    time.sleep(10)

        # Get Tap Scheduler initial Host Name details
        get_tapscheduler_host_name_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(self.org_id)}/room/{room_id}/info'

        for i in range(20):
            response_get_tapscheduler_reset_host_name = send_request(
                method='GET', url=get_tapscheduler_host_name_url,
                token=token
            )

            time.sleep(5)

            tapscheduler_reseted_host_name = \
            response_get_tapscheduler_reset_host_name['devices'][0]['state']['reported']['systemSettings']['hostName']

            if tapscheduler_host_name == tapscheduler_reseted_host_name:
                Report.logPass(f'Tap scheduler host name is set back to initial host name successfully')
            else:
                Report.logFail(f'Tap scheduler host name didnot set back to initial name')

        return updated_host_name

    except Exception as e:
        Report.logException(f'{e}')


def get_room_booking_device_information(self, room_name, room_id, token, org_id):
    """
        Get room booking device information
    """
    try:
        self.banner(f'Get room booking device information: {room_name}')

        self.org_id = org_id

        info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/room/{room_id}/info'
        response = send_request(
            method='GET', url=info_url, token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logInfo(f'Response for GET info API for {room_name}')
        Report.logResponse(json_formatted_response)
        Report.logInfo(f'Response for GET info API for {room_name}- {json_formatted_response}')

        return response

    except Exception as e:
        Report.logException(f'{e}')


def get_organization_bookers(self, org_id, token):
    """
    Get organization bookers information.
    """
    try:
        get_organization_bookers_info_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/booker'
        response_get_organization_bookers_info = send_request(
            method='GET', url=get_organization_bookers_info_url, token=token
        )
        json_formatted_response = json.dumps(response_get_organization_bookers_info, indent=2)
        Report.logInfo(f'Response for GET organization bookers information is {response_get_organization_bookers_info}')
        Report.logResponse(json_formatted_response)

        return response_get_organization_bookers_info

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def import_bookables_for_bookers(self, org_id, token, booker_id):
    """
    Import bookables for bookers
    """
    try:
        import_bookables_for_bookers_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/booker/{booker_id}/import-bookables'
        response_import_bookables_for_bookers = send_request(
            method='POST', url=import_bookables_for_bookers_url, token=token
        )
        json_formatted_response = json.dumps(response_import_bookables_for_bookers, indent=2)
        Report.logInfo(f'Response to import bookables for bookers is {response_import_bookables_for_bookers}')
        Report.logResponse(json_formatted_response)

        return response_import_bookables_for_bookers

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def create_empty_room(room_name, seat_count, org_id, token):
    """
    Method to create empty room

    :param room_name:
    :param org_id:
    :param token:
    """
    try:
        Report.logInfo(f'Room name is {room_name}')
        rooms_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + "/rooms/"
        payload = {
            "realm": "Rooms",
            "group": "/",
            "rooms": [
                {
                    "name": room_name,
                    "seatCount": seat_count
                }]
        }
        response = send_request(
            method='POST', url=rooms_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))

        # Get room id
        room_id = response[0]['id']
        return room_id

    except Exception as e:
        Report.logException(f'{e}')


def set_group_room_booking_settings_to_default(group_path, org_id, token):
    """
    Set the room booking settings of group to default values.
    """
    try:
        room_booking_settings_url = (global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id +
                                     "/policy/room-booking-settings/")
        payload = {
            "group": group_path,
            "bookingPolicy": {
                "walkIn": True,
                "bookingTimes": [
                    1800000,
                    3600000,
                    7200000
                ],
                "showTentative": False,
                "showAgenda": True,
                "showTitles": True,
                "showOrganizer": True,
                "preferCalendarNames": False,
                "requireCheckIn": False,
                "releaseAfter": 300000,
                "cancelRecurring": False,
                "cancelRecurringLimit": 3,
                "autoBook": False,
                "autoBookAfter": 60000,
                "autoBookDuration": 3600000,
                "autoRelease": False,
                "autoReleaseAfter": 300000
            },
            "app": {
                "pinRequired": False,
                "pinCode": "",
                "backgroundMode": "Default"
            }
        }

        response = send_request(
            method='POST', url=room_booking_settings_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        if "policy" in response:
            Report.logPass(f'policy attribute is available in response')
        else:
            Report.logFail(f'policy attribute is not available in response')

        policy = response['policy']

        if "bookingPolicy" in policy:
            Report.logPass(f'bookingPolicy attribute is available in response')
        else:
            Report.logFail(f'bookingPolicy attribute is not available in response')

    except Exception as e:
        Report.logException(f'{e}')


def set_settings_pin_for_group(group_path, org_id, token, code):
    """
       Set the settings PIN
       """
    try:
        room_booking_settings_url = (global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + org_id +
                                     "/policy/room-booking-settings/")
        payload = {
            "group": group_path,
            "bookingPolicy": {
                "walkIn": True,
                "bookingTimes": [
                    1800000,
                    3600000,
                    7200000
                ],
                "showTentative": False,
                "showAgenda": True,
                "showTitles": True,
                "showOrganizer": True,
                "preferCalendarNames": False,
                "requireCheckIn": False,
                "releaseAfter": 300000,
                "cancelRecurring": False,
                "cancelRecurringLimit": 3,
                "autoBook": False,
                "autoBookAfter": 60000,
                "autoBookDuration": 3600000,
                "autoRelease": False,
                "autoReleaseAfter": 300000
            },
            "app": {
                "pinRequired": True,
                "pinCode": code,
                "backgroundMode": "Default"
            }
        }

        response = send_request(
            method='POST', url=room_booking_settings_url, body=json.dumps(payload), token=token
        )
        json_formatted_response = json.dumps(response, indent=2)
        Report.logResponse(format(json_formatted_response))
        time.sleep(2)
        if "policy" in response:
            Report.logPass(f'policy attribute is available in response')
        else:
            Report.logFail(f'policy attribute is not available in response')

        policy = response['policy']

        if "bookingPolicy" in policy:
            Report.logPass(f'bookingPolicy attribute is available in response')
        else:
            Report.logFail(f'bookingPolicy attribute is not available in response')

        if "app" in policy:
            Report.logPass(f'app attribute is available in response')
        else:
            Report.logFail(f'app attribute is not available in response')

    except Exception as e:
        Report.logException(f'{e}')


def deprovision_device(role, token, org_id, room_id, device_id):
    """
        Method to deprovision the device

        :param token:token to authenticate user
        :param org_id:Organization id
        :param org_id:Room id
        :param device_id: Device id
    """
    try:
        deprovision_device_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{str(org_id)}/room/{room_id}/device/{device_id}'
        Report.logInfo(
            f'Url to deprovision the device is: {deprovision_device_url}')

        response_deprovision_device = send_request(
            method='DELETE', url=deprovision_device_url, token=token
        )

        json_formatted_response = json.dumps(response_deprovision_device, indent=2)
        Report.logResponse(json_formatted_response)
        raiden_validation_methods.validate_empty_response(response_deprovision_device)
        return response_deprovision_device

    except Exception as e:
        Report.logException(f'{e}')
