import requests
from requests import Response
from apps.tune.api.sync_api_endpoints import SyncApiEndpoints
from apps.tune.tune_algolia_methods import TuneAlgoliaMethods
from extentreport.report import Report
from datetime import datetime, timedelta, timezone
from typing import Optional


class SyncApi:
    def __init__(self, email: str, password: str, root_domain: str):
        self.email = email
        self._password = password
        self.sync_api_endpoints = SyncApiEndpoints(root_domain)
        self.algolia = TuneAlgoliaMethods(email, password)
        self._headers = dict()
        self._sign_in()

    @staticmethod
    def format_to_zulu_format(input_time: datetime) -> str:
        return (input_time.astimezone().astimezone(timezone.utc).isoformat(timespec='seconds').
                replace("+00:00", "Z"))

    def _sign_in(self) -> None:
        payload = {
            'email': self.email,
            'password': self._password,
        }
        response = requests.post(self.sync_api_endpoints.sign_in(), json=payload)
        if response.ok:
            self._headers['Authorization'] = f'Bearer {response.json().get("token")}'
        else:
            Report.logException(f'Unable to Sign in to Sync: {response.status_code} - '
                                f'{response.text}')

    def get_user_by_email(self) -> Response:
        """
        Get Sync user info by email. Only possible to get info of logged in email account.
        When trying to check other emails, 401 is returned
        Returns: Response

        """
        body = {'email': self.email}
        response = requests.post(self.sync_api_endpoints.get_user_by_email(), json=body,
                                 headers=self._headers)
        return response

    def get_user_info_by_id(self, user_id: str) -> Response:
        response = requests.get(self.sync_api_endpoints.get_user_info_by_id(user_id),
                                headers=self._headers)
        return response

    def get_desk_info(self, org_id: str, desk_id: str) -> Response:
        response = requests.get(self.sync_api_endpoints.get_desk_info(org_id, desk_id),
                                headers=self._headers)
        return response

    def get_org_info(self, org_id: str) -> Response:
        return requests.get(self.sync_api_endpoints.org_info(org_id), headers=self._headers)

    def get_reservations_for_user(self, org_id: str, user_id: str,
                                  time_start: datetime = None,
                                  time_delta: int = 90) -> Response:
        if not time_start:
            time_start = datetime.now() - timedelta(days=5)

        params = {
            "start": self.format_to_zulu_format(time_start),
            "stop": self.format_to_zulu_format(time_start + timedelta(days=time_delta)),
            "include": "session_type",
        }

        return requests.get(self.sync_api_endpoints.get_reservations_for_user(org_id, user_id),
                            params=params, headers=self._headers)

    def delete_reservation_by_id(self, org_id, desk_id, reservation_id) -> Response:
        return requests.delete(self.sync_api_endpoints.edit_delete_reservation(org_id, desk_id, reservation_id),
                               headers=self._headers)

    def get_reservations_for_desk(self, org_id: str, desk_id: str) -> Response:

        start_time = self.format_to_zulu_format(datetime.now() - timedelta(days=5))
        stop_time = self.format_to_zulu_format(datetime.now() + timedelta(days=90))
        params = {'start': start_time,
                  'stop': stop_time}
        return requests.get(self.sync_api_endpoints.get_reservations_for_desk(org_id, desk_id),
                            headers=self._headers,
                            params=params)

    def get_desk_settings(self, org_id: str, desk_id: str) -> Response:
        group = self.get_desk_info(org_id, desk_id).json().get('group')
        params = {
            "group": group,
        }
        return requests.get(self.sync_api_endpoints.desk_settings(org_id), params=params, headers=self._headers)

    def set_desk_settings(self, org_id: str, desk_id: str, body: dict) -> Response:
        group = self.get_desk_info(org_id, desk_id).json().get('group')
        params = {
            "group": group,
        }
        return requests.post(self.sync_api_endpoints.desk_settings(org_id), params=params, headers=self._headers,
                             json=body)

    def get_floor_id(self, org_id: str, desk_id: str) -> Response:
        group = self.get_desk_info(org_id, desk_id).json().get('group')
        site, building, floor, area = group[1:-2].split('/')
        floor_endpoint = "%2F".join([site, building, floor, ""]).replace(" ", "%20")
        return requests.get(self.sync_api_endpoints.get_floor_info(org_id, floor_endpoint), headers=self._headers)

    def get_floor_maps(self, org_id: str, floor_id: str) -> Response:
        return requests.get(self.sync_api_endpoints.get_floor_maps(org_id, floor_id), headers=self._headers)

    def enable_map_by_id(self, org_id: str, map_id: str, status: bool) -> Response:
        body = {'published': status}
        return requests.put(self.sync_api_endpoints.enable_floor_map(org_id, map_id), json=body, headers=self._headers)

    def get_end_user_info_by_id(self, org_id: str, user_id: str) -> Response:
        return requests.get(self.sync_api_endpoints.get_end_user_info(org_id, user_id), headers=self._headers)

    def create_booking_for_user(self, org_id: str, desk_id: str,
                                user_id: str, start_time: Optional[datetime] = None,
                                duration: int = 60) -> Response:
        if not start_time:
            start_time = datetime.now()
        user_data = self.get_end_user_info_by_id(org_id, user_id).json()

        user_dict = {
            'email': user_data.get('email'),
            'identifier': user_id,
            'name': user_data.get('name'),
        }

        reservation_data = {
            'user': user_dict,
            'start': self.format_to_zulu_format(start_time),
            'stop': self.format_to_zulu_format(start_time + timedelta(minutes=duration)),
            'tz': self.algolia.get_desk_timezone(org_id, desk_id),
            'title': "Sync Admin Reservation"
        }

        return requests.post(self.sync_api_endpoints.create_reservation(org_id, desk_id),
                             json=reservation_data, headers=self._headers)

    def edit_booking_by_id(self, org_id: str, desk_id: str, booking_id: str, fields: dict) -> Response:

        all_booking = self.get_reservations_for_desk(org_id, desk_id).json()['reservations']
        filtered_booking = next(iter(el for el in all_booking if el['identifier'] == booking_id))

        booking_edit_data = dict()
        booking_edit_data["resourceId"] = filtered_booking['resource']['identifier']
        booking_edit_data['tz'] = filtered_booking['tz']
        booking_edit_data['start'] = filtered_booking['start']
        booking_edit_data['stop'] = filtered_booking['stop']
        booking_edit_data['title'] = filtered_booking['title']

        for key, value in fields.items():
            if key in booking_edit_data.keys():
                booking_edit_data[key] = value

        return requests.put(self.sync_api_endpoints.edit_delete_reservation(org_id, desk_id, booking_id),
                            headers=self._headers,
                            json=booking_edit_data)





