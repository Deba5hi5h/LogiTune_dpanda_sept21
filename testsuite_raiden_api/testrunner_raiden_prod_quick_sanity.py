import unittest
import sys
import os
import inspect
import argparse

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from common import config

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-prodeu, "
                                                "raiden-prodca, raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
settings.set_value_in_section("RUN_CONFIG", "PROJECT", "RaidenApi")
settings.set_value_in_section("RUN_CONFIG", "dashboard_publish", "True")

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_users import RaidenAPIUser
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.room_groups.raiden_api_room_groups import RaideAPIRoomGroups
from testsuite_raiden_api.personal_devices.host_groups.raiden_api_host_groups import RaideAPIHostGroups
from testsuite_raiden_api.personal_devices.host_provisioning.raiden_api_host_provisioning import (
    RaidenAPI_Host_Provisioning_Personal_Devices)
from testsuite_raiden_ui.tc00_sync_portal_navigation import SyncPortalNavigation

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaideAPIRoomGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIRoomGroups)
tests_RaideAPIHostGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIHostGroups)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_SyncPortalNavigation = unittest.TestLoader().loadTestsFromTestCase(SyncPortalNavigation)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaideAPIRoomGroups = unittest.TestSuite(tests_RaideAPIRoomGroups)
suite_RaideAPIHostGroups = unittest.TestSuite(tests_RaideAPIHostGroups)
suite_RaidenAPI_Host_Provisioning_Personal_Devices = unittest.TestSuite()
suite_RaidenAPI_Host_Provisioning_Personal_Devices.addTests(
    [
        RaidenAPI_Host_Provisioning_Personal_Devices(
            "test_001_VC_53867_Host_Computer_Provisioning"
        ),
        RaidenAPI_Host_Provisioning_Personal_Devices(
            "test_005_VC_53871_Delete_Host_Computer"
        )
    ]
)
suite_SyncPortalNavigation = unittest.TestSuite(tests_SyncPortalNavigation)

raiden_envs = {"raiden-prod": "Raiden-Prod-Global", "raiden-prodeu": "Raiden-Prod-EU",
               "raiden-prodfr": "Raiden-Prod-France", "raiden-prodca": "Raiden-Prod-Canada"}
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"{raiden_env_name}-Quick-Sanity"
global_variables.email_to = "dkattegummula@logitech.com,sveerbhadrappa@logitech.com"
global_variables.email_failed = True
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(tests_RaideAPIRoomGroups)
unittest.TextTestRunner().run(tests_RaideAPIHostGroups)
unittest.TextTestRunner().run(suite_RaidenAPI_Host_Provisioning_Personal_Devices)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_SyncPortalNavigation)
