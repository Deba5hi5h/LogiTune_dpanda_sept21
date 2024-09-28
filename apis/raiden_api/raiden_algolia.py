# Copyright (c) 2020 Logitech Inc.
# All rights reserved
"""
File: raiden_algolia.py
Raiden Algolia API uses API wrapper that abstracts from the complexity of directly interfacing with the Algolia Search API.
It handles, for example, network retry strategy, record batching, and reindexing strategy.
"""
import logging
import time
from algoliasearch.search_client import SearchClient
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAlgolia:
    def __init__(self, sc_search_dict: dict):
        """
        Initializing the Raiden Algolia API Class with app_id and app_key
        :param sc_search_dict:
        """
        try:
            self.timeout = 180
            _app_id = sc_search_dict['appId']
            _app_key_org = sc_search_dict['tokens']['org']
            _app_key_user = sc_search_dict['tokens']['user']
            _app_key_realm_rooms = sc_search_dict['tokens']['realm']['Rooms']
            _app_key_realm_personal = sc_search_dict['tokens']['realm']['Personal']
            _app_key_realm_desks = sc_search_dict['tokens']['realm']['Desks']
            self.baseindex_org = sc_search_dict['indexBases'].get('org', None)
            self.baseindex_role = sc_search_dict['indexBases'].get(
                'role', None,
            )
            self.baseindex_room = sc_search_dict['indexBases'].get(
                'room', None,
            )
            self.baseindex_device = sc_search_dict['indexBases'].get(
                'device', None,
            )
            self.client_org = SearchClient.create(_app_id, _app_key_org)
            self.client_user = SearchClient.create(_app_id, _app_key_user)
            self.client_realm_rooms = SearchClient.create(_app_id, _app_key_realm_rooms)
            self.client_realm_personal = SearchClient.create(_app_id, _app_key_realm_personal)
            self.client_realm_desks = SearchClient.create(_app_id, _app_key_realm_desks)

        except Exception as e:
            log.error(f'Raiden Algolia init Failed {e}')
            raise e

    @property
    def algolia_list_of_orgs(self) -> int:
        """
        Getting the list of Orgs using Algolia APIs
        :param index_base:
        :return:
        """
        try:
            asc_index = self.baseindex_org + ':name-asc'
            index = self.client_org.init_index(asc_index)
            res = index.search(
                '', {
                    'attributesToRetrieve': [
                        'status',
                    ],
                    'hitsPerPage': 10000,
                },
            )
            log.info(
                f'Algolia Search returned {res["hits"].__len__()} No of Orgs',
            )
            return res['hits'].__len__()

        except Exception as e:
            log.error(f'Raiden algolia_list_of_orgs Failed {e}')
            raise e

    @property
    def algolia_list_of_users(self) -> dict:
        """
        Getting the list of Users using Algolia APIs
        :param index_base:
        :return:
        """
        try:
            asc_index = self.baseindex_role + ':familyname-asc'
            index = self.client_user.init_index(asc_index)
            res = index.search(
                '', {
                    'attributesToRetrieve': [
                        'status',
                    ],
                    'hitsPerPage': 10000,
                },
            )

            log.info(
                f'Algolia Search returned {res["hits"].__len__()} Users',
            )
            return res['hits']

        except Exception as e:
            log.error(f'Raiden algolia_list_of_roles Failed {e}')
            raise e

    @property
    def algolia_list_of_rooms(self) -> dict:
        """
        Getting the list of rooms using Algolia APIs
        :param index_base:
        :return:
        """
        try:
            asc_index = self.baseindex_room + ':name-asc'
            index = self.client_realm_rooms.init_index(asc_index)
            res = index.search(
                '', {
                    'attributesToRetrieve': [
                        'status',
                    ],
                    'hitsPerPage': 10000,
                },
            )
            # log.info(f'Algolia Search returned {res["hits"]}')

            log.info(
                f'Algolia Search returned {res["hits"].__len__()} Rooms',
            )
            return res['hits']

        except Exception as e:
            log.error(f'Raiden algolia_list_of_roles Failed {e}')
            raise e

    def algolia_get_a_specific_room_details(self, room_name) -> dict:
        """
        Getting a specific room details using Algolia API
        :param room_name:
        :return:
        """
        try:
            asc_index = self.baseindex_room + ':name-asc'
            index = self.client_realm_rooms.init_index(asc_index)

            _wait_time = float(time.time()) + self.timeout

            # Searching for every 10 secs whether we received the search result
            while float(time.time()) <= _wait_time:

                log.info('Searching in Algolia for the new index')
                res = index.search(
                    room_name, {
                        'attributesToRetrieve': [
                            'status',
                        ],
                        'hitsPerPage': 20,
                    },
                )
                time.sleep(10)

                if res['nbHits'] > 0:
                    return res['hits']

            return {}

        except Exception as e:
            raise AssertionError(
                f'Not Found the room {room_name} in Org after {self.timeout} Secs',
            )

    @property
    def algolia_list_of_devices(self) -> dict:
        """
        Getting the list of devices using Algolia APIs
        :param index_base:
        :return:
        """
        try:
            asc_index = self.baseindex_device + ':roomname-asc'
            index = self.client_realm_rooms.init_index(asc_index)

            res = index.search(
                '', {
                    # 'attributesToRetrieve': [
                    #     'status',
                    # ],
                    'hitsPerPage': 10000,
                },
            )

            log.info(
                f'Algolia Search returned {res["hits"].__len__()} Rooms',
            )
            return res['hits']

        except Exception as e:
            log.error(f'Raiden algolia_list_of_roles Failed {e}')
            raise e

    def algolia_get_a_specific_device_details(self, device: str, expected_room_name: str) -> dict:
        """
        Algolia getting a device details
        :param device:
        :param expected_room_name:
        :return:
        """
        try:
            _asc_index = self.baseindex_device + ':name-asc'
            index = self.client_realm_rooms.init_index(_asc_index)

            _wait_time = float(time.time()) + self.timeout

            # Searching for every 10 secs whether we received the search result
            while float(time.time()) <= _wait_time:

                log.info('Searching in Algolia for the new index')
                res = index.search(
                    device, {
                        'attributesToRetrieve': [
                            'status',
                        ],
                        'hitsPerPage': 20,
                    },
                )
                time.sleep(10)

                # Return no of hits is more then 1
                if res['nbHits'] > 0:

                    # Parse through the hits
                    for _device in res['hits']:
                        if str(_device['status']) == 'Available':
                            # Getting the room name
                            _current_room_name = str(
                                _device['_highlightResult']['room']['name']['value'])
                            if _current_room_name == expected_room_name:
                                log.info(
                                    f'Room Name is matched {_current_room_name} with {expected_room_name}')
                                return res['hits']

            return {}

        except Exception as e:
            raise AssertionError(
                f'Not Found the specific {device} in Org after {self.timeout} Secs',
            )

    @property
    def algolia_get_list_of_desks(self) -> dict:
        """
        Get the list of desks using Algolia APIs
        """
        try:
            asc_index = self.baseindex_room + ':name-asc'
            index = self.client_realm_desks.init_index(asc_index)
            res = index.search(
                '', {
                    'attributesToRetrieve': [
                        'status',
                    ],
                    'hitsPerPage': 10000,
                },
            )
            Report.logInfo(
                f'Algolia Search returned {res["hits"].__len__()} desks',
            )
            return res['hits']

        except Exception as e:
            Report.logException(f'{e}')
            raise e
