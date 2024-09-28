from apps.tune.api.sync_api import SyncApi
from typing import Union, Optional
from config.aws_helper import AWSHelper
from datetime import datetime, timedelta
from common.platform_helper import find_path_in_dict, set_value_in_dict_for_path, get_value_in_dict_for_path


class SyncApiMethods(SyncApi):
    def __init__(self):
        cfg = AWSHelper.get_config('raiden-latest1').ROLES['Owner']['signin_payload']
        super().__init__(**cfg, root_domain="https://sync.logitech.com")
        user_id = self.get_user_by_email().json().get('id')
        self.org_id = self.get_user_info_by_id(user_id).json()[0].get('orgId')
        self.org_name = self.get_user_info_by_id(user_id).json()[0].get('orgName')

    def set_desk_settings_by_fields(self, desk_id: str, desk_settings: dict) -> dict:
        current_coily_settings = self.get_desk_settings(self.org_id, desk_id).json()

        for setting, value in desk_settings.items():
            setting_path = find_path_in_dict(setting, current_coily_settings)
            set_value_in_dict_for_path(current_coily_settings, setting_path, value)

        updated_coily_settings = {'group': current_coily_settings['group'], **current_coily_settings['policy']}
        return self.set_desk_settings(self.org_id, desk_id, updated_coily_settings).json()

    def get_desk_setting_by_field(self, desk_id: str, setting_key: str) -> any:
        current_coily_settings = self.get_desk_settings(self.org_id, desk_id).json()
        setting_path = find_path_in_dict(setting_key, current_coily_settings)
        return get_value_in_dict_for_path(current_coily_settings, setting_path)

    def change_check_in_required(self,  desk_id: str, check_in_required: Union[bool, int] = None) -> bool:

        self.set_desk_settings_by_fields(desk_id, {'enforceCheckInTimeLimit': check_in_required})
        return self.get_desk_setting_by_field(desk_id, "enforceCheckInTimeLimit") == check_in_required

    def change_keep_bookings_visible(self,  desk_id: str, bookings_visible: bool = True) -> bool:

        self.set_desk_settings_by_fields(desk_id, {'reservedSpotVisibleToOthers': bookings_visible})
        return self.get_desk_setting_by_field(desk_id, "reservedSpotVisibleToOthers") == bookings_visible

    def set_desks_default_settings(self, desk_id) -> None:
        self.set_desk_settings_by_fields(desk_id, {
            'enforceCheckInTimeLimit': None,
            'reservedSpotVisibleToOthers': False,
            'reservationTimeLimit': 24,
            'maxDaysInAdvance': 30,
        })

    def delete_reservations_for_user(self, user_id: str, start_time: Optional[datetime] = None,
                                     time_delta_days: int = 90):
        if not start_time:
            start_time = datetime.now() - timedelta(days=5)
        reservations = self.get_reservations_for_user(self.org_id, user_id, start_time, time_delta_days)
        reservations_json = reservations.json()

        to_delete = [{"desk": reservation.get('resource').get('identifier'),
                      "id": reservation.get('identifier')} for reservation in reservations_json.get('reservations')]

        for reservation in to_delete:
            res = self.delete_reservation_by_id(self.org_id, reservation['desk'], reservation['id'])
            if not res.ok:
                raise Exception(f"Reservation with id: {reservation['id']} could not be deleted")

    def delete_reservations_for_desk(self, desk_id: str):
        reservations = self.get_reservations_for_desk(self.org_id, desk_id)
        reservations_json = reservations.json()

        to_delete = [{"desk": reservation.get('resource').get('identifier'),
                      "id": reservation.get('identifier')} for reservation in reservations_json.get('reservations')]

        for reservation in to_delete:
            self.delete_reservation_by_id(self.org_id, reservation['desk'], reservation['id'])

    def change_max_days_in_advance(self, desk_id: str, days_in_advance: int) -> bool:
        self.set_desk_settings_by_fields(desk_id, {'maxDaysInAdvance': days_in_advance})
        return self.get_desk_setting_by_field(desk_id, "maxDaysInAdvance") == days_in_advance

    def enable_map_for_desks_floor(self, org_id: str, desk_id: str, status: bool) -> bool:
        floor_id = self.get_floor_id(org_id, desk_id).json().get('id')
        map_id_json = self.get_floor_maps(org_id, floor_id).json()
        if v := map_id_json:
            map_id = v[0].get('id')
            resp = self.enable_map_by_id(org_id, map_id, status)
            return resp.ok
        return False


    