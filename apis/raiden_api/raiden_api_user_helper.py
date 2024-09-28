import random
import logging
import requests
from common import raiden_config
from common import framework_params as fp
import time
from extentreport.report import Report
from apis.raiden_api import raiden_helper
import json
import apis.process_helper as process_helper
from apis.raiden_api import raiden_validation_methods
from base import global_variables

log = logging.getLogger(__name__)


def create_new_user_info(role: str, usertype: str) -> dict:
    """
    Creating the new user info dictionary

    :param role: Role of logged in user
    :param usertype: Role of new user to be created.
    :return:
    """
    try:
        Report.logInfo(f'{role}- Creating new user - {usertype}')
        MAX = 100000000
        _id = str(random.randint(0, MAX))
        user_name = 'vc.qa.raiden' + usertype.lower() + _id + '@gmail.com'
        return {
            'email': user_name,
            'type': str(usertype),
        }
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def add_user(role: str, usertype: str, adduser_url: str, token: str) -> tuple:
    """
    Create user.

    :param role: Role of logged in user
    :param usertype: Role of new user to be created.
    :param adduser_url: API URL to add user.
    :param token: Token related to signed in user.
    :return:
    """
    try:
        # Add User
        new_user_info = create_new_user_info(
            role, usertype)

        email = new_user_info['email']

        response_add_user = raiden_helper.send_request(
            method='POST', url=adduser_url, body=new_user_info, token=token
        )
        json_formatted_response = json.dumps(response_add_user, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Response- {role}- Add User- {usertype}- {json_formatted_response}')

        # Validate that user is added successfully.
        if email == response_add_user['email']:
            Report.logPass(f'{role}- User {usertype} with email address {email}is added successfully')
        else:
            Report.logFail(f'{role}- Failed to add user {usertype} with email address {email}')
        return response_add_user['role']['userId'], email

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_user(config: dict, email_address: str, org_id: str, token: str, role: str, usertype: str) -> bool:
    """
    Get User

    :param config: config containing the users' credentials in the organization.
    :param email_address: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the signed in user.
    :param usertype: Role of the user in search.
    """
    try:
        get_user_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/role'
        response_get_users = raiden_helper.send_request(
            method='GET', url=get_user_url, token=token
        )
        user_details = None
        for user in response_get_users:
            if user['email'] == email_address:
                user_details = user

        json_formatted_response = json.dumps(response_get_users, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'{role}- Response: Get User {usertype}- {json_formatted_response}')

        # Validate that user is added successfully.
        if email_address == str(user_details['email']):
            Report.logPass(f'{role}- User {usertype} with email address {email_address}is viewed successfully')
        else:
            Report.logFail(f'{role}- Failed to get user {usertype} with email address {email_address}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def update_user_role(usertype_from: str, usertype_to: str, update_user_url: str, user_id: str, token: str) -> bool:
    """
    Update user role.

    :param usertype_from: Current Role of the user
    :param usertype_to: New role of the user after update
    :param update_user_url: API URL to update User
    :param user_id: User ID
    :param token: Token related to signed in user.
    """
    try:
        # Update User role
        user_id_list = list()
        user_id_list.append(user_id)
        user_payload = {
            'userIds': user_id_list,
            'role': {
                'type': usertype_to
            }
        }

        response_update_user_role = raiden_helper.send_request(
            method='POST', url=update_user_url, body=json.dumps(user_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_user_role, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Response- Update user role from {usertype_from} to {usertype_to}: {json_formatted_response}')

        # Validate that user is added successfully.
        if usertype_to == response_update_user_role[0]['type']:
            Report.logPass(f'Updated user role from {usertype_from} to {usertype_to} successfully')
        else:
            Report.logFail(f'Failed to Update user role from {usertype_from} to {usertype_to}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def delete_user_role(user_id, delete_user_url, token):
    """
    Delete user role
    """
    try:
        delete_users_payload = {
            'userIds': [user_id]
        }

        Report.logInfo('POST Call')
        Report.logInfo(delete_user_url)
        Report.logInfo(format(json.dumps(delete_users_payload, indent=2)))

        response = raiden_helper.send_request(
            method='POST', url=delete_user_url, body=json.dumps(delete_users_payload), token=token
        )
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_user_id_from_user_name(config: dict, role: str, get_users_url: str, token: str) -> str:
    """
    Get User ID from User Name

    :param config: Config containing users' credentials.
    :param role: Role of the user
    :param get_users_url: API URL to get users
    :param token: Token related to signed in user.

    """
    try:
        # Get User ID from User Name
        email = config.ROLES[role]['signin_payload']['email']
        user_id = None
        retries = 10
        retry = 0
        while retry < retries:
            response_get_users = raiden_helper.send_request(method='GET', url=get_users_url, token=token)
            for user in response_get_users:
                if user['email'] == email:
                    user_id = user['userId']
                    break
            if not user_id:
                time.sleep(10)
            else:
                Report.logInfo(f'User ID of the user with email {email} is {user_id}')
                break
            retry += 1
        return user_id

    except Exception as e:
        Report.logException(f'Error in getting User ID from User Name- {e}')
        raise e


def get_end_user_id_from_email(email: str, get_users_url: str, token: str) -> str:
    """
    Get User ID from End user email
    Example:  get_users_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate"

    :param email: email id of end user.
    :param get_users_url: API URL to get users
    :param token: Token related to signed in user.

    """
    try:
        response_get_users = raiden_helper.send_request(method='GET', url=get_users_url, token=token)
        user_id = None
        for user in response_get_users['associates']:
            if user['email'] == email:
                user_id = user['userId']
                break
        Report.logInfo(f'User ID of the user with email {email} is {user_id}')
        return user_id

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def configure_user_access_to_one_group(role_update_url: str, user_id_admin: str, token: str, group_name: str) -> dict:
    """
    Configure access of user to a group named AUTO GROUP in meeting rooms and AUTO GROUP in personal devices.

    :param role_update_url: API URL related to role update
    :param user_id_admin: User ID of admin
    :param token: Token related to signed in user.
    """
    try:
        payload = {
            "userIds": [
                user_id_admin
            ],
            "role": {
                "allowedGroups": {
                    "host": {
                        group_name: {}
                    },
                    "tree": {
                        group_name: {}
                    },
                    "loc": {}
                }
            }
        }
        response_user_access = raiden_helper.send_request(
            method='POST', url=role_update_url, body=json.dumps(payload), token=token
        )

        return response_user_access

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def configure_user_access_to_all_groups(role_update_url: str, user_id_admin: str, token: str) -> dict:
    """
    Configure access of user to All groups in meeting rooms and All groups in personal devices.

    :param role_update_url: API URL related to role update
    :param user_id_admin: User ID of admin
    :param token: Token related to signed in user.
    """
    try:
        payload = {
            "userIds": [
                user_id_admin
            ],
            "role": {
                "allowedGroups": {
                    "host": {},
                    "tree": {},
                    "loc": {}
                }
            }
        }
        response_user_access = raiden_helper.send_request(
            method='POST', url=role_update_url, body=json.dumps(payload), token=token
        )

        return response_user_access

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def check_allowed_group(role: str, config: str, org_id: str, group_name: str) -> bool:
    """
    Check provided group name is exclusively available in meeting rooms and personal devices.

    :param role: Role of the user.
    :param config: config containing Users' credentials.
    :param org_id: Organization ID
    :param group_name: Group name
    """
    try:
        sign_in_token = raiden_helper.signin_method(config, role)

        get_org_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id
        response = raiden_helper.send_request(
            method='GET', url=get_org_url, token=sign_in_token
        )

        json_formatted_response = json.dumps(response, indent=2)
        Report.logInfo(f'Role: {role}')
        Report.logResponse(format(json_formatted_response))

        assert group_name in response['groups']['host'], f'{group_name} not in the allowed groups of meeting rooms'
        assert len(response['groups']['host']) == 1, f'Multiple room groups are allowed instead of 1 group- ' \
                                                     f'{group_name}'
        assert group_name in response['groups']['tree'], f'{group_name} not in the allowed groups of personal devices'
        assert len(response['groups']['tree']) == 1, f'Multiple room groups are allowed instead of 1 group- ' \
                                                     f'{group_name}'

        if len(response['groups']['host']) == 1 and group_name in response['groups']['host']:
            Report.logPass(f'{role} can access room group - {group_name} belonging to meeting rooms')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name} belonging to meeting rooms')

        if len(response['groups']['tree']) == 1 and group_name in response['groups']['tree']:
            Report.logPass(f'{role} can access room group - {group_name} belonging to personal devices')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name} belonging to personal devices')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def check_group_is_available(role: str, config: dict, org_id: dict, group_name: str) -> bool:
    """
    Validate that the group is available in the room groups.

    :param role: Role of the user.
    :param config: config containing Users' credentials.
    :param org_id: Organization ID
    :param group_name: Group name
    """
    try:
        sign_in_token = raiden_helper.signin_method(config, role)
        get_context_url = config.BASE_URL + raiden_config.SESSION_ENDPNT + "?orgId=" + org_id
        response_get_context = raiden_helper.send_request(
            method='GET', url=get_context_url, token=sign_in_token
        )

        json_formatted_response = json.dumps(response_get_context, indent=2)
        Report.logInfo(f'Role: {role}')
        Report.logResponse(format(json_formatted_response))
        response = response_get_context['org']

        assert group_name in response['groups']['host'], f'{group_name} not in the allowed groups of meeting rooms'
        assert group_name in response['groups']['tree'], f'{group_name} not in the allowed groups of personal devices'

        if group_name in response['groups']['host']:
            Report.logPass(f'{role} can access room group - {group_name} belonging to meeting rooms')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name} belonging to meeting rooms')

        if group_name in response['groups']['tree']:
            Report.logPass(f'{role} can access room group - {group_name} belonging to personal devices')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name} belonging to personal devices')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def check_group_is_renamed(role: str, config: dict, org_id: dict, group_name: str, group_name_new) -> bool:
    """
    Validate that the group name is modified.

    :param role: Role of the user.
    :param config: config containing Users' credentials.
    :param org_id: Organization ID
    :param group_name: Group name
    """
    try:
        sign_in_token = raiden_helper.signin_method(config, role)
        get_context_url = config.BASE_URL + raiden_config.SESSION_ENDPNT + "?orgId=" + org_id
        response_get_context = raiden_helper.send_request(
            method='GET', url=get_context_url, token=sign_in_token
        )

        json_formatted_response = json.dumps(response_get_context, indent=2)
        Report.logInfo(f'Role: {role}')
        Report.logResponse(format(json_formatted_response))
        response = response_get_context['org']

        if group_name in response['groups']['host']:
            assert group_name_new == response['groups']['host'][group_name]['$label'], 'Error in updating group name' \
                                                                                       'belonging to meeting rooms'

        if group_name in response['groups']['tree']:
            assert group_name_new == response['groups']['tree'][group_name]['$label'], 'Error in updating group name ' \
                                                                                       'belonging to personal devices'

        if group_name in response['groups']['host']:
            if group_name_new == response['groups']['host'][group_name]['$label']:
                Report.logPass(f'{role} can access room group - {group_name_new} belonging to meeting rooms')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name_new} belonging to meeting rooms')

        if group_name in response['groups']['tree']:
            if group_name_new == response['groups']['tree'][group_name]['$label']:
                Report.logPass(f'{role} can access room group - {group_name_new} belonging to personal devices')
        else:
            Report.logFail(f'{role} cannot access room group - {group_name_new} belonging to personal devices')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def check_group_is_not_available(role: str, config: str, org_id: str, group_name: str) -> bool:
    """
    Validate that the group is not available in the room groups.

    :param role: Role of the user
    :param config: config containing Users' credentials.
    :param org_id: Organization ID
    :param group_name: Group name
    """
    try:
        sign_in_token = raiden_helper.signin_method(config, role)
        get_context_url = config.BASE_URL + raiden_config.SESSION_ENDPNT + "?orgId=" + org_id
        response_get_context = raiden_helper.send_request(
            method='GET', url=get_context_url, token=sign_in_token
        )

        json_formatted_response = json.dumps(response_get_context, indent=2)
        Report.logInfo(f'Role: {role}')
        Report.logResponse(format(json_formatted_response))
        response = response_get_context['org']

        assert group_name not in response['groups']['host'], f'{group_name} is in the allowed groups of meeting rooms'
        assert group_name not in response['groups'][
            'tree'], f'{group_name} is in the allowed groups of personal devices'

        if group_name not in response['groups']['host']:
            Report.logPass(f'{role}- {group_name} is not present in meeting rooms')
        else:
            Report.logFail(f'{role} - {group_name} is present in meeting rooms')

        if group_name not in response['groups']['tree']:
            Report.logPass(f'{role} - {group_name} is not present in personal devices')
        else:
            Report.logFail(f'{role} - {group_name} is present in personal devices')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def create_new_enduser_info(role: str) -> dict:
    """
        Creating the new end user info dictionary

        :param role: Role of logged in user
        :return:
        """
    try:
        Report.logInfo(f'{role}- Creating new end user')
        MAX = 100000000
        _id = str(random.randint(0, MAX))
        user_name = 'vc.qa.raiden' + '+testing' + _id + '@gmail.com'
        return {
            'emails': [user_name]
        }
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def add_enduser(role: str, adduser_url: str, token: str, emails: list = None) -> tuple:
    """
        Create end user.

        :param emails: List of Email ids of users to be added. Optional
        :param role: Role of logged in user
        :param adduser_url: API URL to add end user.
        :param token: Token related to signed in user.
        :return:
        """
    try:
        # Add End User
        if emails is None:
            new_enduser_info = create_new_enduser_info(role)
        else:
            new_enduser_info = {'emails': emails}

        email = new_enduser_info['emails'][0]

        response_add_enduser = raiden_helper.send_request(
            method='POST', url=adduser_url, body=json.dumps(new_enduser_info), token=token
        )
        json_formatted_response = json.dumps(response_add_enduser, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Response- {role}- Added end User- {email}- {json_formatted_response}')

        # Validate that end user is added successfully.
        data_dict = json.loads(json_formatted_response)

        if email == data_dict['associates'][0]['email']:
            Report.logPass(f'{role}- User with email address {email} is added successfully')
        else:
            Report.logFail(f'{role}- Failed to add end user with email address {email}')
        return response_add_enduser['associates'][0]['userId'], email

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_enduser(config: dict, associate_id: str, org_id: str, token: str, role: str, email: str) -> bool:
    """
    Get User

    :param config: config containing the users' credentials in the organization.
    :param email_address: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the signed in user.
    :param usertype: Role of the user in search.
    """
    try:
        get_user_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/associate/' + associate_id
        response_get_users = raiden_helper.send_request(
            method='GET', url=get_user_url, token=token
        )
        user_details = None
        for user in response_get_users:
            if response_get_users['userId'] == associate_id:
                user_details = response_get_users

        json_formatted_response = json.dumps(response_get_users, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'{role}- Response: Get User {email}- {json_formatted_response}')

        # Validate that user is added successfully.
        if email == str(user_details['email']):
            Report.logPass(f'{role}- User with email address {email} is viewed successfully')
        else:
            Report.logFail(f'{role}- Failed to get user with email address {email}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def delete_enduser_role(user_id, delete_user_url, token):
    """
    Delete end user role
    """
    try:
        delete_users_payload = {
            'userIds': [user_id]
        }

        Report.logInfo('DELETE Call')
        Report.logInfo(delete_user_url)
        Report.logInfo(format(json.dumps(delete_users_payload, indent=2)))

        response = raiden_helper.send_request(
            method='DELETE', url=delete_user_url, body=json.dumps(delete_users_payload), token=token
        )
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def create_end_users_group_name(role: str) -> dict:
    """
        Creating the new end user group name dictionary

        :param role: Role of logged in user
        :return:end user group name
   """
    try:
        Report.logInfo(f'Creating new end user group name')
        MAX = 100000000
        _id = str(random.randint(0, MAX))
        endusergroup_name = 'vc.qa.raiden' + '+testing_endusergrp' + _id
        Report.logInfo(f'New end user group name is: {endusergroup_name} ')
        return {
            'name': endusergroup_name
        }
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def add_end_user_group(role: str, add_end_user_group_url: str, token: str) -> tuple:
    """
        Create end user group

        :param role: Role of logged in user
        :param add_end_user_group_url: API URL to add end user group.
        :param token: Token related to signed in user.
        :return:
    """

    try:
        'Add End User Group'

        new_end_user_group_name = create_end_users_group_name(role)

        end_user_group_name = new_end_user_group_name

        response_add_end_user_group = raiden_helper.send_request(method='POST', url=add_end_user_group_url,
                                                              body=json.dumps(end_user_group_name), token=token)

        json_formatted_response = json.dumps(response_add_end_user_group, indent=2)
        Report.logResponse(json_formatted_response)

        Report.logInfo(f'Response - {role} - Added end user group {json_formatted_response}')

        # Validate that end user group is added successfully
        data_dict = json.loads(json_formatted_response)
        id = data_dict['id']

        if data_dict['id'] != None:
            Report.logPass(f'{role}- End User group {end_user_group_name} with id {id} is added successfully')
        else:
            Report.logFail(f'{role}- Failed to add end user group {end_user_group_name}')
        return data_dict['id'], end_user_group_name['name']

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_end_user_group(config: dict, cohort_id: str, org_id: str, token: str, role: str) -> bool:
    """
    Get End User's Groups

    :param config: config containing the users' credentials in the organization.
    :param cohort_id: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the signed in user.
    """
    try:
        get_end_user_group_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/associate/cohort'
        Report.logInfo(f'Get End User Group Url is {get_end_user_group_url}')
        response_get_endusersgrp = raiden_helper.send_request(
            method='GET', url=get_end_user_group_url, token=token
        )

        user_details = None

        json_formatted_response = json.dumps(response_get_endusersgrp, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'{role}- Response: Get End User Group {json_formatted_response}')

        # Validate that end user groups are retrieved successfully
        if any(dict['id'] == cohort_id for dict in response_get_endusersgrp):
            user_details = response_get_endusersgrp
            Report.logPass(f'{role}- End User group is viewed successfully')
        else:
            Report.logFail(f'{role}- Failed to get end user group')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def update_end_user_group(end_user_group_name_from: str, end_user_group_name_to: str, update_end_user_group_url: str, cohort_id: str,
                         token: str) -> bool:
    """
    Update end user group.

    :param end_user_group_name_from: Current Group name of the end user
    :param enduserGrpNameTo: New Group name of the end user after update
    :param update_end_user_group_url: API URL to update End User Group
    :param cohortId: User ID
    :param token: Token related to signed in user.
    """
    try:
        # Update End User Group
        update_end_user_group_payload = {
            'name': end_user_group_name_to,
            'locations': [],
            'allowAll': False
        }

        response_update_end_user_group = raiden_helper.send_request(
            method='PATCH', url=update_end_user_group_url, body=json.dumps(update_end_user_group_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_end_user_group, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(
            f'Response- For user-id {cohort_id}, update end user group name from {end_user_group_name_from} to {end_user_group_name_to}: {json_formatted_response}')

        # Validate that end user group is updated successfully.
        if (dict['id'] == cohort_id for dict in response_update_end_user_group):
            Report.logPass(
                f'Updated end user group name from {end_user_group_name_from} to {end_user_group_name_to} successfully')
        else:
            Report.logFail(f'Failed to Update user role from {end_user_group_name_from} to {end_user_group_name_to}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def delete_end_user_group(cohort_id, delete_user_url, token):
    """
    Delete end user group
    """
    try:
        delete_users_payload = {

        }

        Report.logInfo('DELETE Call')
        Report.logInfo(delete_user_url)
        Report.logInfo(format(json.dumps(delete_users_payload, indent=2)))

        response = raiden_helper.send_request(
            method='DELETE', url=delete_user_url, body=json.dumps(delete_users_payload), token=token
        )
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_end_user_validate_end_user_group(config: dict, associate_id: str, org_id: str, token: str, role: str,
                                      new_end_user_group_name: str) -> bool:
    """
    Get End User and validate the group name

    :param config: config containing the users' credentials in the organization.
    :param associate_id: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the signed in user.
    :param new_enduserGrpName: Updated group name of the end user.
    """
    try:
        get_user_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/associate/' + associate_id
        time.sleep(5)
        response_get_users = raiden_helper.send_request(
            method='GET', url=get_user_url, token=token
        )
        user_details = None
        for user in response_get_users:
            if response_get_users['userId'] == associate_id:
                user_details = response_get_users

        json_formatted_response = json.dumps(response_get_users, indent=2)
        Report.logResponse(format(json_formatted_response))
        end_user_group_name = user_details['cohorts']
        Report.logInfo(f'For End user id {associate_id}- Response: Get User group name - {json_formatted_response}')

        #  Validate end user to check that end user group is modified.
        if new_end_user_group_name == str(user_details['cohorts'][0]):
            Report.logPass(f'End user with id {associate_id} is updated to newly created group {new_end_user_group_name}')
        else:
            Report.logFail(f'{role}- End user with {associate_id} is not updated new group {new_end_user_group_name}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def update_with_new_group_name_for_end_user(end_user_group_name_from: str, end_user_group_cohort_id: str, update_end_user_group_url: str,
                                       end_user_id: str,
                                       token: str) -> bool:
    """
    Update end user group.

    :param enduserGrpNamefrom: Current Group name of the end user
    :param enduserGrpNameTo: New Group name of the end user after update
    :param update_end_user_group_url: API URL to update End User Group
    :param enduser_id: End User ID
    :param token: Token related to signed in user.
    """
    try:
        # Update End User Group
        update_end_user_group_payload = {
            'users': [end_user_id],
            'cohorts': [end_user_group_cohort_id]
        }

        response_update_end_user_group = raiden_helper.send_request(
            method='PATCH', url=update_end_user_group_url, body=json.dumps(update_end_user_group_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_end_user_group, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(
            f'Response- For user-id {end_user_id}, update end user group name from {end_user_group_name_from} to id {end_user_group_cohort_id}: {json_formatted_response}')

        Report.logInfo(f"Response is {response_update_end_user_group}")

        # Validate that end user group is updated successfully.
        if response_update_end_user_group == {}:
            Report.logPass(
                f'Updated end user group name from {end_user_group_name_from} to id {end_user_group_cohort_id} successfully')
        else:
            Report.logFail(f'Failed to Update user role from {end_user_group_name_from} to id {end_user_group_cohort_id}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def add_rooms_channel(role: str, add_channel_url: str, token: str) -> tuple:
    """
        Create new channel.

        :param role: Role of logged in user
        :param add_channel_url: API URL to add new channel.
        :param token: Token related to signed in user.
        :return:
        """
    try:
        # Add Room Channel
        new_channel_name = raiden_helper.create_new_channel_name(
            role)

        channel_name = new_channel_name['name'][0]

        # Add New Channel
        add_new_channel_payload = {
            'realm': 'Rooms',
            'name': channel_name
        }

        response_add_channel = raiden_helper.send_request(
            method='POST', url=add_channel_url, body=json.dumps(add_new_channel_payload), token=token
        )
        json_formatted_response = json.dumps(response_add_channel, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(f'Response- {role}- Added channel - {json_formatted_response}')

        # Validate that channel is added successfully.
        data_dict = json.loads(json_formatted_response)

        if channel_name == response_add_channel['name']:
            Report.logPass(f'Channel name {channel_name} is added successfully')
        else:
            Report.logFail(f'Channel name {channel_name} is not added successfully')
        return data_dict['id'], channel_name

    except Exception as e:
        Report.logException(f'{e}')
        raise e


def get_channel_info_for_meeting_room(config: dict, org_id: str, token: str):
    """
    Get meeting room channel info

    :param config: config containing the users' credentials in the organization.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    """
    try:
        # Get Channel
        get_channel_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/channel?realm=Rooms'
        Report.logInfo(f'- Channel url {get_channel_url}')
        response_get_channel = raiden_helper.send_request(
            method='GET', url=get_channel_url, token=token
        )

        # Validate that channel is added successfully.
        if response_get_channel['channels'][0]['id'] == "$prod":
            mr_channel_id = response_get_channel['channels'][0]['id']
            json_formatted_response = json.dumps(response_get_channel, indent=2)
            Report.logResponse(format(json_formatted_response))
            Report.logInfo(f'- Response: Get channel - {json_formatted_response}')
            Report.logPass(f'Channel id {mr_channel_id} is retrieved successfully')
        else:
            Report.logFail(f'Channel id could not be retrieved')
        return True, mr_channel_id

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_meeting_room_channel_info(config: dict, room_id: str, org_id: str, token: str, role: str,
                               room_name: str):
    """
    Get meeting room channel

    :param config: config containing the users' credentials in the organization.
    :param channel_id: channel ID of the update channel.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the signed in user.
    :param room_name: newly created room name.
    """
    try:
        # Get Channel name for meeting room
        get_channel_url = config.BASE_URL + raiden_config.ORG_ENDPNT + org_id + '/room/' + room_id + '/info'
        Report.logInfo(f'- Channel url {get_channel_url}')
        response_get_channel = raiden_helper.send_request(
            method='GET', url=get_channel_url, token=token
        )
        channel_details = None
        # Get channel details for newly created meeting room.
        if response_get_channel['channel']['name'] == '$prod':
            room_channel_id = response_get_channel['channel']['id']
            json_formatted_response = json.dumps(response_get_channel, indent=2)
            Report.logResponse(format(json_formatted_response))
            Report.logInfo(f'- Response: Get channel id for room with id {room_id}- {json_formatted_response}')
            Report.logPass(
                f'{role}- For room-id {room_id}, channel id {room_channel_id} is retrieved successfully')
        elif response_get_channel['name'] == room_name:
            room_channel_id = response_get_channel['channel']['id']
        else:
            Report.logFail(
                f'{role}- Failed to retrieve channel id for room {room_name}')
        return room_channel_id

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def update_with_new_channel_name_for_meeting_room(config: dict, org_id: str, role: str, room_id: str, channel_id: str,
                                    update_channel_name_url: str,
                                    token: str, room_name: str, meeting_room_channel_id: str) -> bool:
    """
    Update channel name for room.

    :param room_id: RoomId for which channel name to be updated
    :param channel_id: Room to be modified to Channel id
    :param update_channel_name_url: API URL to update room's channel name
    :param token: Token related to signed in user.
    """
    try:
        # Update room's channel name
        update_room_channel_name_payload = {
            'roomIds': [room_id],
            'channelId': channel_id,
            'realm': 'Rooms'
        }

        response_update_room_channel_name = raiden_helper.send_request(
            method='POST', url=update_channel_name_url, body=json.dumps(update_room_channel_name_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_room_channel_name, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(
            f'Response- for update channel name is: {json_formatted_response}')

        Report.logInfo(f"Response is {response_update_room_channel_name}")

        # Validate that channel name is updated for the room successfully.
        meeting_room_updated_channel_id = get_meeting_room_channel_info(config, room_id, org_id, token, role,
                                                                  room_name)

        if meeting_room_updated_channel_id == channel_id and response_update_room_channel_name == {}:
            Report.logPass(
                f'For room-id {room_id}, channel id is updated from {meeting_room_channel_id} to {channel_id} successfully')
        else:
            Report.logFail(f'Failed to Update channel name for room {room_id}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_groups_associated_with_end_user(config: dict, role: str, org_id: str, token: str, email_id: str) -> list:
    """
    Get group associated with End User

    :param config: config containing the users' credentials in the organization.
    :param email_id: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the user in search.
    """
    try:
        get_users_url = f"{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate"

        user_id = get_end_user_id_from_email(email_id, get_users_url, token)

        end_user_url = f"{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate/{user_id}"
        response_get_users = raiden_helper.send_request(
            method='GET', url=end_user_url, token=token
        )
        if email_id == str(response_get_users['email']):
            groups = response_get_users['cohorts']
        else:
            groups = []
        return groups
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def modify_with_new_channel_name_for_meeting_room(config: dict, org_id: str, role: str, room_id: str, channel_id: str,
                                     modify_channel_name_url: str,
                                     token: str, room_name: str) -> str:
    """
    Modify channel name for room.

    :param roomId: RoomId for which channel name to be updated
    :param channel_id: Room to be modified to Channel id
    :param modify_channel_name_url: API URL to update room's channel name
    :param token: Token related to signed in user.
    """
    try:
        # Modify room's channel name
        update_room_channel_name_payload = {
            'roomIds': [room_id],
            'channelId': channel_id,
            'realm': 'Rooms'
        }

        response_update_room_channel_name = raiden_helper.send_request(
            method='POST', url=modify_channel_name_url, body=json.dumps(update_room_channel_name_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_room_channel_name, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(
            f'Response- For room-id {room_id}, modify channel-id to {channel_id}: {json_formatted_response}')

        Report.logInfo(f"Response is {response_update_room_channel_name}")

        # Validate that channel name is modified for the room successfully.
        meeting_room_channel_id = get_meeting_room_channel_info(config, room_id, org_id, token, role,
                                                   room_name)

        if meeting_room_channel_id == channel_id and response_update_room_channel_name == {}:
            Report.logPass(f'Channel name modified for room {room_id} successfully')
        else:
            Report.logFail(f'Failed to modify channel name for room {room_id}')

        return meeting_room_channel_id

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_groups_associated_with_end_user(config: dict, role: str, org_id: str, token: str, email_id: str) -> list:
    """
    Get group associated with End User

    :param config: config containing the users' credentials in the organization.
    :param email_id: User ID of the user.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    :param role: Role of the user in search.
    """
    try:
        get_users_url = f"{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate"

        user_id = get_end_user_id_from_email(email_id, get_users_url, token)

        end_user_url = f"{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate/{user_id}"
        response_get_users = raiden_helper.send_request(
            method='GET', url=end_user_url, token=token
        )
        if email_id == str(response_get_users['email']):
            groups = response_get_users['cohorts']
        else:
            groups = []
        return groups
    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_end_user_group_id_by_group_name(config: dict, org_id: str, token: str, group_name: str) -> str:
    """
    Get group id by end user group name

    :param config: config containing the users' credentials in the organization.
    :param group_name: End User group name.
    :param org_id: Organization ID
    :param token: Token related to signed in user.
    """
    try:

        end_users_group_url = f"{config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate/cohort"

        response = raiden_helper.send_request(
            method='GET', url=end_users_group_url, token=token
        )

        for end_user_group in response:
            if end_user_group['name'] == group_name:
                return end_user_group['id']
    except Exception as e:
        Report.logException(f'{e}')
        raise e


def delete_meeting_room_channel(channel_id, delete_meeting_room_channel_url, token):
    """
    Delete meeting room channel
    """
    try:
        delete_mr_channel_payload = {

        }

        Report.logInfo('DELETE Call')
        Report.logInfo(delete_meeting_room_channel_url)
        Report.logInfo(format(json.dumps(delete_mr_channel_payload, indent=2)))

        response = raiden_helper.send_request(
            method='DELETE', url=delete_meeting_room_channel_url, body=json.dumps(delete_mr_channel_payload), token=token
        )
        return response

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def update_withnewgroupname_for_enduser(enduser_grpname_from: str, enduser_grp_cohortid: str,
                                        update_endusergrp_url: str,
                                        enduser_id: str,
                                        token: str) -> bool:
    """
    Update end user group.

    :param enduserGrpNamefrom: Current Group name of the end user
    :param enduserGrpNameTo: New Group name of the end user after update
    :param updateendusergrp_url: API URL to update End User Group
    :param enduser_id: End User ID
    :param token: Token related to signed in user.
    """
    try:
        # Update End User Group
        update_endusergrp_payload = {
            'users': [enduser_id],
            'cohorts': [enduser_grp_cohortid]
        }

        response_update_enduser_grp = raiden_helper.send_request(
            method='PATCH', url=update_endusergrp_url, body=json.dumps(update_endusergrp_payload), token=token
        )
        json_formatted_response = json.dumps(response_update_enduser_grp, indent=2)
        Report.logResponse(format(json_formatted_response))
        Report.logInfo(
            f'Response- For user-id {enduser_id}, update end user group name from {enduser_grpname_from} to id {enduser_grp_cohortid}: {json_formatted_response}')

        Report.logInfo(f"Response is {response_update_enduser_grp}")

        # Validate that end user group is updated successfully.
        if response_update_enduser_grp == {}:
            Report.logPass(
                f'Updated end user group name from {enduser_grpname_from} to id {enduser_grp_cohortid} successfully')
        else:
            Report.logFail(f'Failed to Update user role from {enduser_grpname_from} to id {enduser_grp_cohortid}')
        return True

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_all_end_user_names(get_users_url: str, token: str) -> list:
    """
    Get all End User names
    Example:  get_users_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate"

    :param get_users_url: API URL to get users
    :param token: Token related to signed in user.

    """
    try:
        response_get_users = raiden_helper.send_request(method='GET', url=get_users_url, token=token)
        end_user_names = []
        for user in response_get_users['associates']:
            if user['name'] is not None:
                end_user_names.append(user['name'])
        return end_user_names

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_end_user_name_from_email(email: str, get_users_url: str, token: str) -> str:
    """
    Get User Name from End user email
    Example:  get_users_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate"

    :param email: email id of end user.
    :param get_users_url: API URL to get users
    :param token: Token related to signed in user.

    """
    try:
        response_get_users = raiden_helper.send_request(method='GET', url=get_users_url, token=token)
        name = None
        for user in response_get_users['associates']:
            if user['email'] == email:
                name = user['name']
                break
        Report.logInfo(f'User Name of the user with email {email} is {name}')
        return name

    except Exception as e:
        Report.logException(f'{e}')
        raise e

def get_active_end_user_groups(org_id: str, token: str) -> list:
    """
    Get active End User groups - User group associated with at least one user

    :param org_id:
    :param token: Token related to signed in user.

    """
    try:
        get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{org_id}/associate'
        response_get_users = raiden_helper.send_request(method='GET', url=get_users_url, token=token)
        user_groups = []
        for user in response_get_users['associates']:
            groups = user['cohorts']
            for group in groups:
                if group not in user_groups:
                    user_groups.append(group)
        return user_groups

    except Exception as e:
        Report.logException(f'{e}')
        raise e