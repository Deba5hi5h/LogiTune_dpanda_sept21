from typing import Union


class SyncApiEndpoints:
    def __init__(self, root_domain: str):
        self.root_domain = root_domain if not root_domain.endswith('/') else root_domain[:-1]

    def sign_in(self) -> str:
        return f'{self.root_domain}/api/session/sign-in'

    def get_user_by_email(self) -> str:
        return f'{self.root_domain}/api/user/get'

    def get_user_info_by_id(self, user_id: str) -> str:
        return f'{self.root_domain}/api/user/{user_id}/role'

    def get_desk_info(self, org_id: str, desk_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/room/{desk_id}/info'

    def create_reservation(self, org_id: str, desk_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/desk/{desk_id}/reservation/'

    def edit_delete_reservation(self, org_id: str, desk_id: str, reservation_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/desk/{desk_id}/reservation/{reservation_id}'

    def get_reservations_for_user(self, org_id: str, user_id: str) -> str:
        return f"{self.root_domain}/api/org/{org_id}/associate/{user_id}/reservation"

    def get_reservations_for_desk(self, org_id: str, desk_id: str) -> str:
        return f"{self.root_domain}/api/org/{org_id}/desk/{desk_id}/reservation"

    def get_end_user_info(self, org_id: str, user_id: str) -> str:
        return f"{self.root_domain}/api/org/{org_id}/associate/{user_id}/"

    def get_floor_info(self, org_id: str, floor_param: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/location/{floor_param}'

    def get_floor_maps(self, org_id: str, floor_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/floor/{floor_id}/map'

    def enable_floor_map(self, org_id: str, map_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/map/{map_id}/status'

    def desk_settings(self, org_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}/policy/desk-settings'

    def org_info(self, org_id: str) -> str:
        return f'{self.root_domain}/api/org/{org_id}'


