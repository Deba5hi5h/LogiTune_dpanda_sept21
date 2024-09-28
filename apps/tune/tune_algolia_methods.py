from algoliasearch.search_client import SearchClient
from apis.raiden_api.raiden_algolia import RaidenAlgolia
import requests


class TuneAlgoliaMethods:
    BASE_URL = "https://sync.logitech.com"
    CONTEXT_URL = "/api/session/context"
    SIGNIN_URL = '/api/session/sign-in'

    def __init__(self, sync_mail: str, sync_passwd: str):
        self.token = self._authenticate_sync_portal(sync_mail, sync_passwd)
        self.token_header = {"Authorization": f"Bearer {self.token}"}

        algolia_context = self._get_algolia_context()
        self.app_id = algolia_context['appId']

        tokens = {}
        for key, value in algolia_context.get('tokens').items():
            if type(value) is str:
                tokens[key] = value
            else:
                tokens = {**tokens, **value}

        self.tokens = tokens

    def _authenticate_sync_portal(self, email: str, password: str):
        response = requests.post(self.BASE_URL + self.SIGNIN_URL, json={
            "email": email,
            "password": password
        })
        if response.ok:
            response_json = response.json()
            return response_json.get('token')

    def _get_algolia_context(self):
        response = requests.get(self.BASE_URL + self.CONTEXT_URL, headers=self.token_header)
        if response.ok:
            response_json = response.json()
            return response_json['search']

    def get_desks_in_group(self, org_id: str, group: str):
        client_realm_desks = SearchClient.create(self.app_id, self.tokens['Desks'])
        desks_index = client_realm_desks.init_index('raiden-prod-room:name-asc')
        response = desks_index.search(
            '', {"filters": f"orgId: \"{org_id}\" AND (groups: \"{group}\" ) ",
                 'hitsPerPage': 10000}
        )
        return response.get('hits')

    def get_desk_timezone(self, org_id: str, desk_id: str) -> str:
        client_realm_desks = SearchClient.create(self.app_id, self.tokens['Desks'])
        desks_index = client_realm_desks.init_index('raiden-prod-room:name-asc')
        response = desks_index.search(
            '', {"filters": f"orgId: \"{org_id}\" AND (id: \"{desk_id}\" ) "}
        )
        return response.get('hits')[0]['tz']['name']

    def get_end_users_in_org(self, org_id: str):
        client_realm_desks = SearchClient.create(self.app_id, self.tokens['org'])
        users_index = client_realm_desks.init_index('raiden-prod-associate:name-asc')
        response = users_index.search(
            '', {"filters": f"orgId: \"{org_id}\" AND NOT external: \"true\"",
                 'hitsPerPage': 10000}
        )
        return response.get('hits')

    def get_end_users_in_org_in_group(self, org_id: str, group_name: str):
        client_realm_desks = SearchClient.create(self.app_id, self.tokens['org'])
        users_index = client_realm_desks.init_index('raiden-prod-associate:name-asc')
        response = users_index.search(
            '', {"filters": f"orgId: \"{org_id}\" AND cohorts:\"{group_name}\"", "length": 50,
                 'hitsPerPage': 10000}
        )
        return response.get('hits')
