import logging
import time
import json
import pytz
import requests

from common import raiden_config
from common.framework_params import COILY_DESK_ID
from extentreport.report import Report
from base import global_variables
from datetime import datetime, timedelta, timezone
from tzlocal import get_localzone
from typing import Optional, Any

log = logging.getLogger(__name__)
BASE_URL = "https://sync.logitech.com/"


class CoilySyncMethods:

    def __init__(self):
        self.token = self._signin_method()
        self.coily_org_id = self.get_org_id_for_coily_user()
        self.org_name = self.get_org_name(org_id=self.coily_org_id)
        self.desk_info = self.get_desk_info(org_id=self.coily_org_id,
                                            desk_id=COILY_DESK_ID)
        self.desk_name = self.desk_info[0]
        self.desk_path = self.desk_info[1]
        self.group_name = self.desk_path.split('/')[-3]
        self.device_ip = self.desk_info[2]
        self.device_sn = self.desk_info[3]
        self.desk_settings = self.get_coily_settings()
        self.desk_settings_time_format = self.desk_settings['timeFormat']
        self.desk_settings_agenda_enabled = self.desk_settings['agendaEnabled']
        self.desk_settings_privacy_mode_enabled = self.desk_settings['privacyModeEnabled']
        self.desk_settings_screen_brightness = self.desk_settings['screenBrightness']
        self.desk_settings_locale = self.desk_settings['locale']

    @staticmethod
    def _token_gen(token):
        return {'Authorization': f'Bearer {token}'}

    def _send_request(self, method: str, url: str, body=None, token=None, params=None, retry=3) -> dict:
        """
        Create the request and returns the response using the request library

        """
        if retry == 0:
            return Report.logException("Number of retries reached its maximum, could not send the request.")
        try:

            kwargs = dict()
            kwargs['method'] = method
            kwargs['url'] = url

            kwargs['headers'] = self._token_gen(token) if token else None
            kwargs['data'] = body if method is not 'GET' else None
            kwargs['params'] = params if method is 'GET' else None
            response = requests.request(**kwargs, timeout=30)
            if global_variables.reportInstance:
                Report.logRequest(f"Request data: "
                                  f"{json.dumps({k: v for k,v in kwargs.items()  if k != 'headers'}, indent=2)}")

            # Send the request
            if response.ok:
                response_json = response.json()
                if global_variables.reportInstance:
                    Report.logResponse(f"Request response data: {response_json}")
                return response_json
            else:
                Report.logInfo(f"Could not fetch data from Sync Portal, retrying... Error: {repr(response)}")
                try:
                    Report.logInfo(f"Response json: {response.json()}")
                except AttributeError:
                    pass
                self.token = self._signin_method()
                time.sleep(20)
                return self._send_request(method, url, body, self.token, params, retry-1)

        except Exception as err:
            self.token = self._signin_method()
            time.sleep(20)
            Report.logInfo(f"Retrying with {retry - 1} value")
            return self._send_request(method, url, body, self.token, params, retry - 1)

    def _validate_sign_in(self, response: dict):
        """
        Validate the Token and TTL of the Signin Users response message

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
            log.error(f'validate_signinuser - {e}')
            return (False, None)

    def _signin_method(self):
        """
        Signin Api - added as part of setup method in unittest case class

        """

        # Construct header
        role = 'Owner'
        _url = BASE_URL + raiden_config.SIGNIN_ENDPNT
        roles = global_variables.config
        _data = roles.ROLES[role]['signin_payload']

        Report.logInfo(f'Sign in: {role}')

        try:
            # Send the request
            response = self._send_request(method='POST', url=_url, body=_data)

            # Validate the response
            (_status, token) = self._validate_sign_in(response)
            if _status:
                Report.logPass(f'{role} Sign-in validation passed')
                return token
            else:
                log.info(f'{role} Sign-in validation failed')
                return None
        except Exception as e:
            log.error(f'{role} - Unable to sign in with the user role')
            raise e

    def get_org_id_for_coily_user(self):
        try:
            info_url = f'{BASE_URL}api/user/get'

            role = 'Owner'
            _url = BASE_URL + raiden_config.SIGNIN_ENDPNT
            roles = global_variables.config
            _email = roles.ROLES[role]['signin_payload']["email"]

            payload = {"email": _email}

            response_user = self._send_request(
                method='POST', url=info_url, token=self.token, body=json.dumps(payload)
            )

            role_url = f'{BASE_URL}api/user/{response_user["id"]}/role'

            response_role = self._send_request(
                method='GET', url=role_url, token=self.token
            )

            return response_role[0]["orgId"]
        except Exception as e:
            log.error(f'Unable to get org id: {e}')
            raise e

    def get_site_buildings(self, org_id, site_name):
        try:
            org_info = f'{BASE_URL}api/org/{org_id}'

            response = self._send_request(
                method='GET', url=org_info, token=self.token
            )
            buildings = response['groups']['loc'][site_name]
            return {key: building for key, building in buildings.items()
                    if type(building) is dict}

        except Exception as e:
            log.error(f'Unable to get Org name for org id: {org_id}')
            raise e

    def get_org_name(self, org_id):
        try:
            info_url = f'{BASE_URL}api/org/{org_id}'

            response = self._send_request(
                method='GET', url=info_url, token=self.token
            )
            return response['name']
        except Exception as e:
            log.error(f'Unable to get Org name for org id: {org_id}')
            raise e

    def get_desk_info(self, org_id, desk_id):
        try:
            device_ip = None
            device_sn = None
            info_url = f'{BASE_URL}api/org/{org_id}/room/{desk_id}/info'

            response = self._send_request(
                method='GET', url=info_url, token=self.token
            )

            for device in response['devices']:
                if device['type'] == 'Coily':
                    device_ip = device['ip']
                    device_sn = device['serial']

            return response['name'], response['group'], device_ip, device_sn
        except Exception as e:
            log.error(f'Unable to getDesk info for : {desk_id}')
            raise e

    def get_desk_scheduler_status(self):
        try:
            desk_id = COILY_DESK_ID
            info_url = f'{BASE_URL}api/org/{self.coily_org_id}/room/{desk_id}/info'

            response = self._send_request(
                method='GET', url=info_url, token=self.token
            )

            return response['scheduler']['reported']['status']
        except Exception as e:
            log.error(f'Unable to getDesk status for : {desk_id}')
            raise e

    def change_walk_in_session_value(self, value: Optional[int]):
        """
        Method to change walk in session value
        :param value: session duration value, None means disabled

        """
        try:
            org_id = self.coily_org_id
            desk_settings_url = f'{BASE_URL}api/org/{org_id}/policy/desk-settings'

            group_path = self.desk_path
            encoded_desk_group_url = self._custom_quote(f'{group_path}')

            desk_url = f'{desk_settings_url}?group={encoded_desk_group_url}'

            response = self._send_request(
                method='GET', url=desk_url, token=self.token
            )

            walk_in_session_value = response['policy']['coilySettings']['walkInSessionDefaultDuration']
            Report.logInfo(f'Current walk-in session value is: {walk_in_session_value}')

            if walk_in_session_value != value:
                Report.logInfo(f'Change walk-in session value to: {value}')

                payload = {
                    "group": group_path,
                    "reservationPolicy": {
                        "qrCheckInRequiredTimeLimit": None,
                        "qrCodeReservation": False,
                        "officeStartHours": None,
                        "maxDaysInAdvance": 14,
                        "officeEndHours": None,
                        "reservedSessionDefaultDuration": 1,
                        "reserveRemotely": True,
                        "reservationTimeLimit": None,
                        "reservedSpotVisibleToOthers": False
                    },
                    "coilySettings": {
                        "walkInSessionDefaultDuration": value,
                        "notifyUserBeforeDeskReleased": 300,
                        "generateLongOccupancyAlertThreshold": None,
                        "hardStopBlockFromReusing": None,
                        "enforceCheckInTimeLimit": None,
                        "requireCleaning": False
                    }
                }

                response_post = self._send_request(
                    method='POST', url=desk_url, token=self.token, body=json.dumps(payload)
                )

                assert response_post['policy']['coilySettings'][
                           'walkInSessionDefaultDuration'] == value, Report.logException(
                    f"walkInSessionDefaultDuration not changed to {value}")
                Report.logPass(f'Walk-in session value changed successfully.')
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def change_auto_extend_value(self, value: Any) -> None:
        try:
            org_id = self.coily_org_id
            desk_settings_url = f'{BASE_URL}api/org/{org_id}/policy/desk-settings'

            encoded_desk_group_url = self._custom_quote(f'{self.desk_path}')

            desk_url = f'{desk_settings_url}?group={encoded_desk_group_url}'

            current_coily_settings: dict = self._send_request(
                method='GET', url=desk_url, token=self.token
            )

            current_coily_settings['policy']['coilySettings']['hardStopBlockFromReusing'] = value
            new_coily_settings = {'group': current_coily_settings['group'], **current_coily_settings['policy']}
            changed_settings: dict = self._send_request(
                method='POST', url=desk_url, token=self.token, body=json.dumps(new_coily_settings)
            )
            time.sleep(2)
            assert (current_coily_settings['policy']['coilySettings']['hardStopBlockFromReusing'] ==
                    changed_settings['policy']['coilySettings']['hardStopBlockFromReusing'])

            Report.logInfo(f"Auto-Extend Session successfully changed to {value}")

        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def change_max_days_in_advance(self, value: Optional[int] = 14):
        """
        Method to change max days in advance for desk
        :param value: max days in advance value

        """
        try:
            org_id = self.coily_org_id
            desk_settings_url = f'{BASE_URL}api/org/{org_id}/policy/desk-settings'

            encoded_desk_group_url = self._custom_quote(f'{self.desk_path}')

            desk_url = f'{desk_settings_url}?group={encoded_desk_group_url}'

            current_coily_settings: dict = self._send_request(
                method='GET', url=desk_url, token=self.token
            )

            current_coily_settings['policy']['reservationPolicy']['maxDaysInAdvance'] = value
            new_coily_settings = {'group': current_coily_settings['group'], **current_coily_settings['policy']}
            changed_settings: dict = self._send_request(
                method='POST', url=desk_url, token=self.token, body=json.dumps(new_coily_settings)
            )
            time.sleep(2)
            assert (current_coily_settings['policy']['reservationPolicy']['maxDaysInAdvance'] ==
                    changed_settings['policy']['reservationPolicy']['maxDaysInAdvance'])

            Report.logInfo(f"Max days in advance successfully changed to {value}")

        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def get_coily_settings(self):
        try:
            org_id = self.coily_org_id
            app_settings_url = f'{BASE_URL}api/org/{org_id}/policy/app-settings'

            group_path = self.desk_path[:-1]
            encoded_desk_group_url = self._custom_quote(f'{group_path}')

            app_url = f'{app_settings_url}?group={encoded_desk_group_url}'

            response = self._send_request(
                method='GET', url=app_url, token=self.token
            )
            '''
            Expected format:
            {
                "agendaEnabled": true,
                "privacyModeEnabled": false,
                "locale": "en_US",
                "timeFormat": "12",
                "screenBrightness": 255
            }
            '''

            coily_settings = response['policy']['scheduler']
            Report.logInfo(f'Coily settings are: {coily_settings}')
            return coily_settings

        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def set_coily_settings(self, agenda_enabled=True, privacy_mode_enabled=True, time_format="12", screen_brightness=255, locale="en_US"):
        try:
            org_id = self.coily_org_id
            app_settings_url = f'{BASE_URL}api/org/{org_id}/policy/app-settings'

            group_path = self.desk_path[:-1]

            short_group_name = self._prepare_a_short_group_name(group_path)

            payload = {
                "group": short_group_name,
                    "appSettings": {
                        "scheduler": {
                            "agendaEnabled": agenda_enabled,
                            "privacyModeEnabled": privacy_mode_enabled,
                            "locale": locale,
                            "timeFormat": time_format,
                            "screenBrightness": screen_brightness
                        }
                    }
                }

            response = self._send_request(
                method='POST', url=app_settings_url, token=self.token, body=json.dumps(payload)
            )

            coily_settings = response['policy']['scheduler']
            Report.logInfo(f'Coily settings are: {coily_settings}')
            return coily_settings

        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def _prepare_a_short_group_name(self, group_path):
        parts = group_path.split('/')
        if len(parts) >= 5:
            desired_parts = parts[:3]
            short_group_name = '/'.join(desired_parts) + '/'
            return short_group_name


    def make_a_reservation(self, user_credentials, reservation_duration: int = 1, desk_id: str = COILY_DESK_ID):
        try:
            org_id = self.coily_org_id
            user_email = user_credentials['signin_payload']['email']
            user_full_name = f"{user_credentials['signin_payload']['name']} {user_credentials['signin_payload']['surname']}"
            user_identifier = user_credentials['signin_payload']['identifier']

            post_url = f'{BASE_URL}api/org/{org_id}/desk/{desk_id}/reservation'

            start_time, stop_time = self._prepare_timestamps_for_reservation(reservation_duration)

            payload = {
                "title": "Sync Admin Reservation",
                "start": start_time,
                "stop": stop_time,
                "tz": self._get_local_timezone(),
                "user": {
                    "identifier": user_identifier,
                    "email": user_email,
                    "name": user_full_name
                }
            }

            response_post = self._send_request(
                method='POST', url=post_url, token=self.token, body=json.dumps(payload)
            )
            Report.logInfo(f"Reservation for {user_full_name} made with success until {payload['stop']}")

            return (response_post['reservations'][0]['identifier'], payload['start'], payload['stop'])
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def make_a_future_reservation(self, user_credentials, delay_in_x_minutes=70, reservation_duration=12):
        try:
            org_id = self.coily_org_id
            desk_id = COILY_DESK_ID
            user_email = user_credentials['signin_payload']['email']
            user_full_name = f"{user_credentials['signin_payload']['name']} {user_credentials['signin_payload']['surname']}"
            user_identifier = user_credentials['signin_payload']['identifier']

            post_url = f'{BASE_URL}api/org/{org_id}/desk/{desk_id}/reservation'

            start_time, stop_time = self._prepare_timestamps_for_future_reservation(delay=delay_in_x_minutes, reservation_duration=reservation_duration)

            payload = {
                "title": "Sync Admin Reservation",
                "start": start_time,
                "stop": stop_time,
                "tz": self._get_local_timezone(),
                "user": {
                    "identifier": user_identifier,
                    "email": user_email,
                    "name": user_full_name
                }
            }

            response_post = self._send_request(
                method='POST', url=post_url, token=self.token, body=json.dumps(payload)
            )
            Report.logInfo(f"Reservation for {user_full_name} made with success from {payload['start']} to {payload['stop']}")

            return (response_post['reservations'][0]['identifier'], payload['start'], payload['stop'])
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def delete_reservation_by_reservation_id(self, desk_id=None, reservation_id=None):
        try:
            org_id = self.coily_org_id
            if not desk_id:
                desk_id = COILY_DESK_ID
            delete_url = f'{BASE_URL}api/org/{org_id}/desk/{desk_id}/reservation/{reservation_id}'

            response_delete = self._send_request(
                method='DELETE', url=delete_url, token=self.token,
            )

            assert response_delete is True, "DELETE command was not successful."
            Report.logInfo(f"Reservation deleted with success.")
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def get_reservations_for_user(self, user_credentials):
        try:
            org_id = self.coily_org_id
            user_identifier = user_credentials['signin_payload']['identifier']

            today_date = datetime.now().date()
            ninty_days_later = today_date + timedelta(days=90)

            start = today_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            end = ninty_days_later.strftime("%Y-%m-%dT%H:%M:%SZ")
            url = f"{BASE_URL}api/org/{org_id}/associate/{user_identifier}/reservation?start={start}&stop={end}&include=session_type"

            response_get = self._send_request(
                method='GET', url=url, token=self.token,
            )
            active_reservations = []
            for reservation in response_get['reservations']:
                if reservation['checkedIn'] is False:
                    active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))
                if reservation['checkedIn'] is True and self._is_there_any_ongoing_checked_reservation(reservation['stop']):
                    active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))

            return active_reservations
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    def get_reservations_for_desk(self):
        try:
            org_id = self.coily_org_id
            desk_id = COILY_DESK_ID

            today_date = datetime.now().date()
            three_days_earlier = today_date - timedelta(days=3)
            formatted_date_1 = three_days_earlier.strftime("%Y-%m-%d")
            ninty_days_later = today_date + timedelta(days=90)
            formatted_date_2 = ninty_days_later.strftime("%Y-%m-%d")

            url = f'{BASE_URL}api/org/{org_id}/desk/{desk_id}/reservation?start={formatted_date_1}T23%3A00%3A00.000Z&stop={formatted_date_2}T23%3A00%3A00.000Z&include=session_type%2Caway_periods'
            response_get = self._send_request(
                method='GET', url=url, token=self.token,
            )

            active_reservations = []
            for reservation in response_get['reservations']:
                if reservation['checkedIn'] is False:
                    active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))
                if reservation['checkedIn'] is True and self._is_there_any_ongoing_checked_reservation(reservation['stop']):
                    active_reservations.append((reservation['resource']['identifier'], reservation['identifier']))

            return active_reservations
        except Exception as e:
            Report.logException(f'{e}')
            raise Exception(e)

    @staticmethod
    def _is_there_any_ongoing_checked_reservation(reservation_stop_time):
        dt = datetime.strptime(reservation_stop_time, "%Y-%m-%dT%H:%M:%SZ")
        timestamp1 = dt.timestamp()

        current_time = datetime.utcnow()
        timestamp_now = current_time.timestamp()

        return timestamp_now < timestamp1

    @staticmethod
    def _get_local_timezone():
        local_timezone = get_localzone()
        return str(local_timezone)

    def delete_active_reservations_via_sync_api(self, user_credentials):
        Report.logInfo(f"Delete reservations for {user_credentials['signin_payload']['email']}")
        active_reservations = self.get_reservations_for_user(user_credentials)
        Report.logInfo(f'Number of active reservation: {len(active_reservations)}')

        for res in active_reservations:
            self.delete_reservation_by_reservation_id(desk_id=res[0], reservation_id=res[1])

    def delete_active_reservations_for_desk(self):
        active_desk_reservations = self.get_reservations_for_desk()
        Report.logInfo(f'Number of active desk reservation: {len(active_desk_reservations)}')
        for res in active_desk_reservations:
            self.delete_reservation_by_reservation_id(desk_id=res[0], reservation_id=res[1])

    @staticmethod
    def _prepare_timestamps_for_reservation(reservation_duration=1):
        current_time = datetime.now()
        utc_now = datetime.now(pytz.utc)
        offset_stop = timedelta(hours=reservation_duration)
        future_time = current_time + offset_stop

        start_time = utc_now
        formated_start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        if current_time.day == future_time.day:
            stop_time = utc_now + offset_stop
            formated_stop_time = stop_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            current_date = datetime.now().date()
            time_str = "23:59"
            datetime_str = f"{current_date} {time_str}"
            converted_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            utc_datetime = converted_datetime.astimezone(timezone.utc)
            formated_stop_time = utc_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        return formated_start_time, formated_stop_time

    @staticmethod
    def _prepare_timestamps_for_future_reservation(delay=10, reservation_duration=1):
        local_reservation_start_time = datetime.now()
        offset_delay = timedelta(minutes=delay)
        local_reservation_start_time = local_reservation_start_time + offset_delay

        utc_now = datetime.now(pytz.utc)
        offset_stop = timedelta(hours=reservation_duration)
        local_reservation_stop_time = local_reservation_start_time + offset_stop

        start_time_utc = utc_now + offset_delay
        formated_start_time_utc = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        if local_reservation_start_time.day == local_reservation_stop_time.day:
            local_reservation_stop_time = utc_now + offset_stop + offset_delay
            formated_stop_time = local_reservation_stop_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        else:
            current_date = datetime.now().date()
            time_str = "23:59"
            datetime_str = f"{current_date} {time_str}"
            converted_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            utc_datetime = converted_datetime.astimezone(timezone.utc)
            formated_stop_time = utc_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        return formated_start_time_utc, formated_stop_time

    def _custom_quote(self, input_string):
        # Replace space with %20 and / with %2F
        encoded_string = input_string.replace(' ', '%20').replace('/', '%2F')
        return encoded_string
