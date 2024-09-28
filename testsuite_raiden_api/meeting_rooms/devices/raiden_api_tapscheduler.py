import logging
import unittest
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from base import global_variables
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPITapScheduler(UIBase):
    """
    Test to verify device APIs for Tap.
    """
    syncportal_methods = SyncPortalTCMethods()
    device_name = "Nintendo"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}
    role = "OrgAdmin"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPITapScheduler, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPITapScheduler, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPITapScheduler, self).setUp()

    def tearDown(self):
        super(RaidenAPITapScheduler, self).tearDown()

    def test_1901_Provision_Tap_Scheduler_to_sync_portal(self):
        self.syncportal_methods.\
            tc_provision_device_in_appliance_mode_to_sync_portal(self.role, self.device_name, self.room_name,
                                                                 global_variables.SYNC_ENV)

    def test_1902_VC_102446_Get_Device_TapScheduler(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_name)

    def test_1903_VC_79960_Disable_Local_Network_Access_TapScheduler(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1904_VC_79959_Enable_Local_Network_Access_TapScheduler(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Disable_Local_Network_Access(self.role, self.room_name,
                                                                self.device_name, min_version)

    def test_1905_VC_79961_Change_Password_Local_Network_Access_TapScheduler(self):
        min_version = float(904.222)
        self.syncportal_methods.tc_Change_Password_Local_Network_Access(self.role, self.room_name,
                                                                        self.device_name, min_version)

    def test_1906_VC_79958_Reboot_Device_TapScheduler(self):
        self.syncportal_methods.tc_Reboot_Device(self.role, self.room_name, self.device_name)

    def test_1907_VC_79962_Move_Device_TapScheduler(self):
        self.syncportal_methods.tc_Move_Device(self.role, self.room_name, self.device_name)

    def test_1908_Delete_Room(self):
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

    def test_1909_VC_136508_Edit_TapScheduler_Host_Name(self):
        '''
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Add new room
                2) Provision Tap Scheduler to Sync Portal and get the host name of Tap Scheduler
                3) Edit the Tap Scheduler host name
                4) Validate the updated host name
                5) Set the hostname of Tap Scheduler back to its initial name.
                6) Delete the room

        '''

        Report.logInfo(
            'STEP 1: Edit tap scheduler host name')

        self.room_id, self.device_id = self.syncportal_methods.tc_edit_tapscheduler_host_name(room_name=self.room_name, role=self.role, device_name=self.device_name)

        Report.logInfo(
            'STEP 2: Delete the room.')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

    def test_1910_VC_137033_Provision_Room_Using_GroupProvisionCode(self):
        '''
            Setup:
                1. Sign in to Sync Portal using valid owner credentials.

            Test:
                1) Create a room group in an organization.
                2) Get group provision code of room group from Sync Portal.
                3) Provision Tap Scheduler to Sync Portal using group provision code. Room will be created
                automatically
                4) Delete the room
                5) Delete room group.
        '''

        Report.logInfo(
            'STEP 1: Create a room group in an organization.')
        self.room_group_name = self.syncportal_methods.tc_add_room_group(role=self.role)

        Report.logInfo(
            'STEP 2: Get group provision code of room group from Sync Portal.')
        self.roomgroup_group_provision_code = self.syncportal_methods.tc_get_group_provision_code_for_roomgroup(role=self.role, room_group_name=self.room_group_name)

        Report.logInfo(
            'STEP 3: Provision Tap Scheduler to Sync Portal using group provision code. Room will be created automatically')
        room_name = self.syncportal_methods. \
            tc_provision_nintendo_to_sync_portal(role=self.role, device_name=self.device_name, room_group_name=self.room_group_name , roomgroup_group_provision_code=self.roomgroup_group_provision_code)

        Report.logInfo(
            'STEP 4: Delete the room.')
        self.syncportal_methods.tc_delete_room(role=self.role, room_name=room_name)

        Report.logInfo('STEP 5: Delete the added room group.')
        self.syncportal_methods.tc_delete_room_group(role=self.role, room_group=self.room_group_name)

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapScheduler)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
