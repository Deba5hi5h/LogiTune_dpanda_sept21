import logging
import time
import re
import random
from extentreport.report import Report
from common import raiden_config

log = logging.getLogger(__name__)


def validate_get_device(response: dict):
    """
    Validate the GET Device API response.
    """
    try:
        if response['id'] is not None:
            Report.logPass(f"Received id field - {response['id']}")
        else:
            Report.logFail('Error in id field')

        if response['name'] is not None:
            Report.logPass(f"Received name field - {response['name']}")
        else:
            Report.logFail('Error in name field')

        if response['room'] is not None:
            Report.logPass(f"Received room field - {response['room']}")
        else:
            Report.logFail('Error in room field')

        if response['hostId'] is not None:
            Report.logPass(f"Received org field - {response['hostId']}")
        else:
            Report.logFail('Error in hostId field')

        reported_state = response['state']['reported']
        if reported_state['status'] is not None:
            Report.logPass(f"Received status field - {reported_state['status']}")
        else:
            Report.logFail('Error in status field')

        if reported_state['healthStatus'] is not None:
            Report.logPass(f"Received healthStatus field - {reported_state['healthStatus']}")
        else:
            Report.logFail('Error in healthStatus field')

        if reported_state['updateStatus'] is not None:
            Report.logPass(f"Received updateStatus field - {reported_state['updateStatus']}")
        else:
            Report.logFail('Error in updateStatus field')

        assert response['id'] is not None, 'Error in device id'
        assert response['name'] is not None, 'Error in device name'
        assert response['room'] is not None
        assert response['hostId'] is not None, 'Error in hostId'
        assert reported_state['status'] is not None, 'Error in status'
        assert reported_state['healthStatus'] is not None, 'Error in healthStatus'
        assert reported_state['updateStatus'] is not None, 'Error in updateStatus'
        return True

    except Exception as e:
        Report.logException(f'{e}')


def _validate_org_response(response: dict, org_name: str):
    """
    Validating the Create Org Response

    :param response:
    :param org_name:
    :return:
    """
    if response['cat'] is not None:
        Report.logPass(f"Received cat field - {response['cat']}")
    else:
        Report.logFail('Error in cat field')

    if response['id'] is not None:
        Report.logPass(f"Received id field - {response['id']}")
    else:
        Report.logFail('Error in id field')

    if response['name'] == org_name:
        Report.logPass(f"Received name field - {response['name']}")
    else:
        Report.logFail('Error in name field')

    if response['uat'] is not None:
        Report.logPass(f"Received uat field - {response['uat']}")
    else:
        Report.logFail('Error in uat field')

    assert response['cat'] is not None, 'Error in cat Field'
    assert response['id'] is not None, 'Error in id Field'
    assert response['name'] is not None, 'Error in name Field'
    assert response['name'] == org_name, 'Error in org name'
    assert response['uat'] is not None, 'Error in uat Field'
    return True


def _validate_org_error_response(response: dict, role: str):
    """
    Validate the attributes of error response

    :param response:
    :param role:
    :return:
    """
    try:
        if response['message'] is not None:
            Report.logPass(f"Received message field - {response['message']}")
        else:
            Report.logFail('Error in message field')

        if response['statusCode'] is not None:
            Report.logPass(f"Received statusCode field - {response['statusCode']}")

        assert response['message'] is not None, 'Error in message Field'
        assert response['statusCode'] == raiden_config.ORG_UPDATE_ERROR[role][0], 'Error in status code'
        return True

    except AssertionError as e:
        log.error('{}'.format(e))
        raise e


def validate_org_response(response: dict, role: str, org_name: str):
    """
    Validate that the org is created when the role is admin
    and forbidden error is thrown when other roles try to create org from backend

    :param response:
    :param role:
    :param org_name:
    :return:
    """
    try:
        if role == 'SysAdmin':
            return _validate_org_response(response, org_name)
        else:
            return _validate_org_error_response(response, role)

    except Exception as e:
        Report.logException(f'{e}')


def validate_valid_get_orgs_response(response: dict) -> bool:
    """
    Validate the valid org parameters

    :param response:
    :return:
    """
    try:
        _len = response.__len__()
        if _len == 0:
            Report.logInfo('No organizations found in this environments')
            return True

        _rand_index = random.randint(0, _len)
        if response[_rand_index]['cat'] is not None:
            Report.logPass(f"Received cat field - {response[_rand_index]['cat']}")
        else:
            Report.logFail('Error in cat field')

        if response[_rand_index]['id'] is not None:
            Report.logPass(f"Received id field - {response[_rand_index]['id']}")
        else:
            Report.logFail('Error in id field')

        if response[_rand_index]['name'] is not None:
            Report.logPass(f"Received name field - {response[_rand_index]['name']}")
        else:
            Report.logFail('Error in name field')

        if response[_rand_index]['uat'] is not None:
            Report.logPass(f"Received uat field - {response[_rand_index]['uat']}")
        else:
            Report.logFail('Error in uat field')

        assert response[_rand_index]['cat'] is not None, 'Error in cat Field'
        assert response[_rand_index]['id'] is not None, 'Error in id Field'
        assert response[_rand_index]['name'] is not None, 'Error in name Field'
        assert response[_rand_index]['uat'] is not None, 'Error in uat Field'

        return True
    except Exception as e:
        Report.logException(f'{e}')


def validate_room_parameters(room_info: dict) -> bool:
    """
    Validate the room parameters

    :param room_info:
    :return:
    """
    try:
        if room_info['objectID'] is not None:
            Report.logPass(f"Received objectID field - {room_info['objectID']}")
        else:
            Report.logFail('Error in objectID field')

        if room_info['_highlightResult']['name']['value'] is not None:
            Report.logPass(f"Received name field - {room_info['_highlightResult']['name']['value']}")
        else:
            Report.logFail('Error in name field')
        if room_info['_highlightResult']['sw']['value'] is not None:
            Report.logPass(f"Received sw field - { room_info['_highlightResult']['sw']['value']}")
        else:
            Report.logFail('Error in sw field')

        if room_info['_highlightResult']['os']['value'] is not None:
            Report.logPass(f"Received os field - {room_info['_highlightResult']['os']['value']}")
        else:
            Report.logFail('Error in os field')
        assert room_info is not dict, 'Room Details should be in Dictionary'
        assert room_info['objectID'] is not None, 'Room ID should be a String'
        assert room_info['_highlightResult']['name']['value'] is not None, 'Room Name should be a String'
        assert room_info['_highlightResult']['sw']['value'] is not None, 'SW should be a String'
        assert room_info['_highlightResult']['os']['value'] is not None, 'OS should be a String'
        return True
    except Exception as e:
        log.error(f'Validate the Room parameters {e}')
        raise e


def validate_prov_new_room(role: str, response: dict, expected_room: str) -> (bool, str):
    """
    Validate the provisional response received after provisioning complete

    :param role:
    :param response:
    :param expected_room:
    :return:
    """
    try:
        Report.logInfo(f"{role} - Validating the provisioning brand new room")
        if response.__len__():
            assert (response["credentials"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in credentials Field"
            assert (response["topics"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in topics Field"
            assert (response["connection"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in connection Field"
            assert (response["telemetry"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in telemetry Field"
            assert (response["room"] is not dict) and (
                    response["room"] is not None
            ), "Error in room Field"
            assert (response["org"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in org Field"
            assert (
                expected_room in response["room"]["name"]
            ), "Not configured the expected room"

            return True, response["room"]["id"]
        else:
            return False, None

    except Exception as e:
        Report.logException(f'{e}')
        return False, None


def validate_complete_provisioning_appliance(role: str, response: dict, expected_room: str,
                                             max_occupancy: int, on_name_conflict: str = "Fail",
                                             name_conflict: bool = False):
    """
    Validate the provisioning response received after complete provisioning

    :param role:
    :param response:
    :param expected_room:
    :param max_occupancy:
    :param on_name_conflict:
    :param name_conflict:
    :return:
    """
    try:
        log.info("{}: Validating the provisioning of new appliance with onNameConflict as MakeUnique".format(role))

        if len(response):
            assert (response["credentials"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in credentials Field"
            assert (response["topics"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in topics Field"
            assert (response["connection"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in connection Field"
            assert (response["telemetry"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in telemetry Field"
            assert (response["room"] is not dict) and (
                    response["room"] is not None
            ), "Error in room Field"
            assert (response["org"] is not dict) and (
                    response["credentials"] is not None
            ), "Error in org Field"

            if on_name_conflict == 'MakeUnique' and name_conflict is True:
                assert (
                    re.match(expected_room + r"(.+)", response['room']['name'])
                ), "Not configured the expected room"
            else:
                assert (
                        expected_room == response["room"]["name"]
                ), "Not configured the expected room"

            assert (
                response["room"]["occupancyMode"] == 'Disabled'
            ), "Error in occupancyMode Field"
            assert (
                response["room"]["maxOccupancy"] == max_occupancy
            ), "Error in max occupancy count"

            return True, response["room"]["id"]
        else:
            return False, None

    except AssertionError as e:
        log.error("Validating the provisioning brand new room Error - {}".format(e))
        return False, None


def validate_initiate_host_provisioning(response):
    try:
        if 'completion' in response:
            Report.logPass('Received completion field - {}'.format(response['completion']))
        else:
            Report.logFail('Error in completion field')
        completion_obj = response['completion']
        if 'provId' in completion_obj:
            Report.logPass('Received provId field - {}'.format(completion_obj['provId']))
        else:
            Report.logFail('Error in provId field')
        if 'orgId' in completion_obj:
            Report.logPass('Received orgId field - {}'.format(completion_obj['orgId']))
        else:
            Report.logFail('Error in orgId field')
        if 'url' in completion_obj:
            Report.logPass('Received url field - {}'.format(completion_obj['url']))
        else:
            Report.logFail('Error in url field')
        if 'max' in completion_obj:
            Report.logPass('Received max field - {}'.format(completion_obj['max']))
        else:
            Report.logFail('Error in max field')
        if 'expiry' in completion_obj:
            Report.logPass('Received expiry field - {}'.format(completion_obj['expiry']))
        else:
            Report.logFail('Error in expiry field')
        if 'sig' in completion_obj:
            Report.logPass('Received sig field - {}'.format(completion_obj['sig']))
        else:
            Report.logFail('Error in sig field')

        assert response['completion'] is not None, 'Error in completion object'
        completion_obj = response['completion']
        assert completion_obj['provId'] is not None, 'Error in provId field'
        assert completion_obj['orgId'] is not None, 'Error in orgId field'
        assert completion_obj['url'] is not None, 'Error in url field'
        assert completion_obj['max'] is not None, 'Error in max field'
        assert completion_obj['expiry'] is not None, 'Error in expiry field'
        assert completion_obj['sig'] is not None, 'Error in sig field'

        return True

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_complete_host_provisioning(response):
    try:
        if 'hostId' in response:
            Report.logPass('Received hostId field - {}'.format(response['hostId']))
        else:
            Report.logFail('Error in hostId field')
        if 'orgId' in response:
            Report.logPass('Received orgId field - {}'.format(response['orgId']))
        else:
            Report.logFail('Error in orgId field')
        if 'reportUrl' in response:
            Report.logPass('Received reportUrl field - {}'.format(response['reportUrl']))
        else:
            Report.logFail('Error in reportUrl field')
        if 'certificate' in response:
            Report.logPass('Received certificate field - {}'.format(response['certificate']))
        else:
            Report.logFail('Error in certificate field')
        if 'privateKey' in response:
            Report.logPass('Received privateKey field - {}'.format(response['privateKey']))
        else:
            Report.logFail('Error in privateKey field')

        assert response['hostId'] is not None, 'Error in hostId field'
        assert response['orgId'] is not None, 'Error in orgId field'
        assert response['reportUrl'] is not None, 'Error in reportUrl field'
        assert response['certificate'] is not None, 'Error in certificate field'
        assert response['privateKey'] is not None, 'Error in privateKey field'

        return True

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_get_host_info(response):
    try:
        if 'model' in response:
            Report.logPass('Received model field - {}'.format(response['model']))
        else:
            Report.logFail('Error in model field')
        if 'hostName' in response:
            Report.logPass('Received hostName field - {}'.format(response['hostName']))
        else:
            Report.logFail('Error in hostName field')
        if 'os' in response:
            Report.logPass('Received os field - {}'.format(response['os']))
        else:
            Report.logFail('Error in os field')
        if 'tzName' in response:
            Report.logPass('Received tzName field - {}'.format(response['tzName']))
        else:
            Report.logFail('Error in tzName field')
        if 'group' in response:
            Report.logPass('Received group field - {}'.format(response['group']))
        else:
            Report.logFail('Error in group field')
        if 'name' in response:
            Report.logPass('Received name field - {}'.format(response['name']))
        else:
            Report.logFail('Error in name field')
        if 'osv' in response:
            Report.logPass('Received osv field - {}'.format(response['osv']))
        else:
            Report.logFail('Error in osv field')
        if 'proc' in response:
            Report.logPass('Received proc field - {}'.format(response['proc']))
        else:
            Report.logFail('Error in proc field')
        if 'lastSeen' in response:
            Report.logPass('Received lastSeen field - {}'.format(response['lastSeen']))
        else:
            Report.logFail('Error in lastSeen field')
        if 'orgId' in response:
            Report.logPass('Received orgId field - {}'.format(response['orgId']))
        else:
            Report.logFail('Error in orgId field')
        if 'tzOffset' in response:
            Report.logPass('Received tzOffset field - {}'.format(response['tzOffset']))
        else:
            Report.logFail('Error in tzOffset field')
        if 'machineId' in response:
            Report.logPass('Received machineId field - {}'.format(response['machineId']))
        else:
            Report.logFail('Error in machineId field')
        if 'serial' in response:
            Report.logPass('Received serial field - {}'.format(response['serial']))
        else:
            Report.logFail('Error in serial field')
        if 'ram' in response:
            Report.logPass('Received ram field - {}'.format(response['ram']))
        else:
            Report.logFail('Error in ram field')
        if 'id' in response:
            Report.logPass('Received id field - {}'.format(response['id']))
        else:
            Report.logFail('Error in id field')
        if 'clients' in response:
            Report.logPass('Received clients field - {}'.format(response['clients']))
        else:
            Report.logFail('Error in clients field')
        if 'accessories' in response:
            Report.logPass('Received accessories field - {}'.format(response['accessories']))
        else:
            Report.logFail('Error in accessories field')

        assert response['model'] is not None, 'Error in model field'
        assert response['hostName'] is not None, 'Error in hostName field'
        assert response['os'] is not None, 'Error in os field'
        assert response['tzName'] is not None, 'Error in tzName field'
        assert response['group'] is not None, 'Error in group field'
        assert response['name'] is not None, 'Error in name field'
        assert response['osv'] is not None, 'Error in osv field'
        assert response['proc'] is not None, 'Error in proc field'
        assert response['lastSeen'] is not None, 'Error in lastSeen field'
        assert response['orgId'] is not None, 'Error in orgId field'
        assert response['tzOffset'] is not None, 'Error in tzOffset field'
        assert response['machineId'] is not None, 'Error in machineId field'
        assert response['serial'] is not None, 'Error in serial field'
        assert response['ram'] is not None, 'Error in ram field'
        assert response['id'] is not None, 'Error in id field'
        assert response['clients'] is not None, 'Error in clients field'
        assert response['accessories'] is not None, 'Error in accessories field'
        return True

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_empty_response(response):
    try:
        if response == {}:
            Report.logPass('Working as expected. Received response- {}'.format(response))
        else:
            Report.logFail('Error in response')
        assert response == {}, 'Error in response'
        return True

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_rooms_created(response: dict, room_names: list):
    """
    Validate that the rooms provided in the list: room_names are created successfully.
    """
    try:
        if response:
            flag = 0
            for object in response:
                if object['name'] not in room_names:
                    flag = 1
                    break
            if flag == 0:
                Report.logPass(f'Rooms got created successfully. Received response- {response}')
                return True
            else:
                Report.logFail('Error in response')

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_device_rebooted(response):
    """
    Validate that the device rebooted successfully.
    """
    try:
        if response:
            obj = response[0]
            if obj['deviceRebooted']:
                Report.logPass(f'Device rebooted successfully- {response}')
                return True
            else:
                Report.logFail('Device did not reboot successfully')

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_firmware_version(response, firmware_package_version):
    """
    Validate that the updated firmware version.
    """
    try:
        if response['manifest'] == firmware_package_version:
            Report.logPass('Received manifest field- {}'.format(response['manifest']))
        else:
            Report.logFail('Error in manifest field')

        if response['updateStatus'] == 'Up to Date':
            Report.logPass('Received updateStatus field- {}'.format(response['updateStatus']))
        else:
            Report.logFail('Error in updateStatus field')
        assert response['manifest'] == firmware_package_version, 'Error in manifest field'
        assert response['updateStatus'] == 'Up to Date', 'Error in updateStatus field'
        return True

    except Exception as e:
        log.error('Exception occurred- {}'.format(e))


def validate_room_note_is_present(response, room_note):
    """
    Validate that the room note is present.
    """
    try:
        if 'note' in response:
            Report.logPass('Received note field - {}'.format(response['note']))
        else:
            Report.logFail('Error in note field')

        if 'text' in response['note']:
            Report.logPass('Received text field - {}'.format(response['note']['text']))
        else:
            Report.logFail('Error in text field')

        assert response['note'] is not None, 'Error in note field'
        assert response['note']['text'] == room_note, 'Error in text field'
        return True

    except Exception as e:
        log.error('Exception occurred- {}'.format(e))


def validate_room_note_is_deleted(response):
    """
    Validate room note is deleted.
    """
    try:
        if 'note' not in response:
            Report.logPass('Note field is removed from response.')
        else:
            Report.logFail('Note field is still available.')
        assert 'note' not in response, 'Error in response'
        return True

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_group_is_available(response, group_name):
    """
    Validate that the group is added.
    """
    try:
        if group_name in response:
            Report.logPass(f'Group Name- {group_name} is in the list of room groups')
            return True
        else:
            Report.logFail(f'Group name- {group_name} is not in list of room groups')
            return False

    except Exception as e:
        Report.logException(f'Exception occurred- {e}')


def validate_group_name_is_modified(response, group_name, group_name_new):
    """
    Validate that the subgroup name is modified.
    """
    try:
        if group_name in response:
            obj = response[group_name]
            if obj['$label'] == group_name_new:
                Report.logPass(f'Subgroup- {group_name} is renamed to {group_name_new}.')
            return True
        else:
            Report.logFail('subgroup name not in list of groups')
            return False

    except Exception as e:
        log.error(f'Exception occurred- {e}')


def validate_subgroup_is_added(response, subgroup_name, group_name):
    """
    Validate that the subgroup is added.
    """
    try:
        if subgroup_name in response[group_name].keys():
            Report.logPass('Subgroup- {} is in the list of subgroups in {}.'.format(subgroup_name, group_name))
            return True
        else:
            Report.logFail('subgroup name not in list of groups')
            return False

    except Exception as e:
        log.error(f'Exception occurred- {e}')


def validate_subgroup_name_is_modified(response, subgroup_name, subgroup_name_new, group_name):
    """
    Validate that the subgroup name is modified.
    """
    try:
        if subgroup_name in response[group_name].keys():
            obj = response[group_name][subgroup_name]
            if obj['$label'] == subgroup_name_new:
                Report.logPass(f'Subgroup- {subgroup_name} is renamed to {subgroup_name_new}.')
            return True
        else:
            Report.logFail('subgroup name not in list of groups')
            return False

    except Exception as e:
        log.error(f'Exception occurred- {e}')


def validate_subgroup_is_deleted(response, subgroup_name, group_name):
    """
    Validate that the subgroup is deleted.
    """
    try:
        if subgroup_name not in response[group_name].keys():
            Report.logPass('Subgroup- {} is deleted from {}.'.format(subgroup_name, group_name))
            return True
        else:
            Report.logFail('subgroup is still not deleted')
            return False

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_group_is_deleted(response, group_name):
    """
    Validate that the group is deleted.
    """
    try:
        if group_name not in response:
            Report.logPass('Group Name- {} is deleted from list of groups.'.format(group_name))
            return True
        else:
            Report.logFail('Group name is not deleted from the list of groups')
            return False

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_response_settings_policy(response, parameter, attribute):
    """
    Validate that response works as expected after changing the group settings.
    """
    try:
        if parameter == 'micEQ' and response['policy']['audioSettings'][parameter] == attribute:
            Report.logPass('{} is set to - {}'.format(parameter, attribute))
            # Sleep is added so that enough time is provided for the change to propagate to subgroup & room level.
            time.sleep(5)
            return True
        elif parameter == 'deReverbMode' and response['policy']['audioSettings'][parameter] == attribute:
            Report.logPass('{} is set to - {}'.format(parameter, attribute))
            # Sleep is added so that enough time is provided for the change to propagate to subgroup & room level.
            time.sleep(5)
            return True
        else:
            Report.logFail('{} is not updated correctly'.format(parameter))
            return False

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_device_info_response_room_level(response, parameter, attribute):
    """
    Validate that the settings changed in group level propagate to individual room level.
    """
    try:
        if parameter == 'micEQ' and response['state']['reported']['audioSettings'][parameter] == attribute:
            Report.logPass('{} is set to - {} in individual room level'.format(parameter, attribute))
            return True

        elif parameter =='deReverbMode' and response['state']['reported']['audioSettings'][parameter] == attribute:
            Report.logPass('{} is set to - {} in individual room level'.format(parameter, attribute))
            return True

        else:
            Report.logFail('{} is not updated correctly in individual room level - {}'.format
                           (parameter, response['state']['reported']['audioSettings'][parameter]))
            return False

    except Exception as e:
        log.error('Exception occured- {}'.format(e))


def validate_room_name_updated(response, room_name):
    """
    Validate that the room name is updated.
    """
    try:
        if response['name'] == str(room_name):
            Report.logPass('Room name is updated to - {}'.format(response['name']))
            return True

        else:
            Report.logFail('Room name is not updated')
            return False

    except Exception as e:
        log.error('Exception occurred- {}'.format(e))


