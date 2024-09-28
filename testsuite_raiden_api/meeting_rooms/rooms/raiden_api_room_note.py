import logging
import unittest
import sys
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase
from extentreport.report import Report
from datetime import datetime

log = logging.getLogger(__name__)


class RaidenAPIRoomNote(UIBase):
    """
    Test to verify device APIs for Brio.
    """
    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIRoomNote, cls).setUpClass()
            cls.role = 'OrgAdmin'
            now = datetime.now()
            cls.room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
            cls.room_note = 'Test'

        except Exception as e:
            Report.logException('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIRoomNote, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIRoomNote, self).setUp()

    def tearDown(self):
        super(RaidenAPIRoomNote, self).tearDown()

    def test_601_VC_12844_Add_Empty_room(self):
        self.syncportal_methods.tc_add_empty_room(role=self.role, room_name=self.room_name)

    def test_602_VC_56622_Add_Room_Note(self):
        self.syncportal_methods.tc_add_room_note(room_name=self.room_name, role=self.role, room_note=self.room_note)

    def test_603_VC_56637_Update_Room_Note(self):
        self.syncportal_methods.tc_update_room_note(room_name=self.room_name, role=self.role,
                                                    room_note=self.room_note + "-updated")

    def test_604_VC_56657_Delete_Room_Note(self):
        self.syncportal_methods.tc_delete_room_note(room_name=self.room_name, role=self.role)

    def test_605_Delete_room(self):
        self.syncportal_methods.tc_delete_room(role=self.role, room_name=self.room_name)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomNote)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
