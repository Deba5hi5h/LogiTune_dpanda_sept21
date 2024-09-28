import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime

log = logging.getLogger(__name__)


class RaidenAPIEmptyRooms(UIBase):
    """
    Test to verify add, update and delete of empty rooms.
    """
    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIEmptyRooms, cls).setUpClass()
            cls.role = 'OrgAdmin'
            now = datetime.now()
            cls.room_name_1 = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom1"
            cls.room_name_2 = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom2"

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIEmptyRooms, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIEmptyRooms, self).setUp()

    def tearDown(self):
        super(RaidenAPIEmptyRooms, self).tearDown()

    def test_501_VC_69043_add_view_update_delete_empty_rooms(self):
        self.syncportal_methods.tc_empty_rooms(self.role, self.room_name_1, self.room_name_2)


if __name__ == "__main__":
    unittest.main()