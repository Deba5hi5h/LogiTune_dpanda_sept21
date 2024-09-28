import unittest
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from common import config
from base import global_variables
import argparse
from common.email_notification import EmailNotification
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-qa1, raiden-stable, "
                                                "raiden-latest1, raiden-qa")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section("RUN_CONFIG", "dashboard_publish", "True")

from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_users import RaidenAPIUser
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.room_groups.raiden_api_room_groups import RaideAPIRoomGroups
from testsuite_raiden_api.personal_devices.host_groups.raiden_api_host_groups import RaideAPIHostGroups
from testsuite_raiden_api.raiden_api_hosted_devices_setup import RaidenAPIHostedDevicesSetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybar import RaidenAPIHostedRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarmini import RaidenAPIHostedRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarhuddle import RaidenAPIHostedRallyBarHuddle
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybar import RaidenAPIRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarmini import RaidenAPIRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarhuddle import RaidenAPIRallyBarHuddle
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_sight import RaidenAPIHostedSight
from testsuite_raiden_api.raiden_api_meeting_rooms_teardown import RaidenAPIMeetingRoomTearDown
from testsuite_raiden_api.users.raiden_api_endusers import RaideAPIEndUsers
from testsuite_raiden_api.hot_desks.raiden_api_hot_desks import RaidenAPIHotDesks
from testsuite_raiden_api.hot_desks.raiden_api_flexdesk_hierarchy import RaidenAPITestsForFlexDeskHierarchy

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaideAPIRoomGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIRoomGroups)
tests_RaideAPIHostGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIHostGroups)
tests_RaidenAPIHostedDevicesSetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedDevicesSetup)
tests_RaidenAPIHostedRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBar)
tests_RaidenAPIHostedRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarMini)
tests_RaidenAPIHostedRallyBarHuddle = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarHuddle)
tests_RaidenAPIRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBar)
tests_RaidenAPIRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarMini)
tests_RaidenAPIRallyBarHuddle = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarHuddle)
tests_RaidenAPIHostedSight = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedSight)
tests_RaidenAPIMeetingRoomTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomTearDown)
tests_RaideAPIEndUsers = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsers)
tests_RaidenAPIHotDesks = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHotDesks)
tests_RaidenAPITestsForFlexDeskHierarchy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITestsForFlexDeskHierarchy)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaideAPIRoomGroups = unittest.TestSuite(tests_RaideAPIRoomGroups)
suite_RaideAPIHostGroups = unittest.TestSuite(tests_RaideAPIHostGroups)
suite_RaidenAPIHostedDevicesSetup = unittest.TestSuite(tests_RaidenAPIHostedDevicesSetup)
suite_RaidenAPIHostedRallyBar = unittest.TestSuite()
suite_RaidenAPIHostedRallyBarMini = unittest.TestSuite()
suite_RaidenAPIHostedRallyBarHuddle = unittest.TestSuite()
suite_RaidenAPIRallyBar = unittest.TestSuite()
suite_RaidenAPIRallyBarMini = unittest.TestSuite()
suite_RaidenAPIRallyBarHuddle = unittest.TestSuite()
suite_RaidenAPIHostedSight = unittest.TestSuite()
suite_RaidenAPIMeetingRoomTearDown = unittest.TestSuite(tests_RaidenAPIMeetingRoomTearDown)
suite_RaideAPIEndUsers = unittest.TestSuite(tests_RaideAPIEndUsers)
suite_RaidenAPIHotDesks = unittest.TestSuite(tests_RaidenAPIHotDesks)
suite_RaidenAPITestsForFlexDeskHierarchy = unittest.TestSuite(tests_RaidenAPITestsForFlexDeskHierarchy)


suite_RaidenAPIHostedRallyBar.addTests([RaidenAPIHostedRallyBar('test_1301_VC_102254_Get_Device_RallyBar_in_Device_'
                                                                'mode')])
suite_RaidenAPIHostedRallyBarMini.addTests([RaidenAPIHostedRallyBarMini('test_1401_VC_102262_Get_Device_RallyBarMini_'
                                                                        'in_Device_mode')])
suite_RaidenAPIHostedRallyBarHuddle.addTests([RaidenAPIHostedRallyBarHuddle('test_2501_VC_116707_get_rally_bar_huddle_'
                                                                            'in_device_mode')])
suite_RaidenAPIHostedSight.addTests([RaidenAPIHostedSight('test_2501_VC_116708_get_sight_in_device_mode')])
suite_RaidenAPIRallyBar.addTests([RaidenAPIRallyBar('test_1501_Provision_Rally_Bar_to_Sync_Portal'),
                                  RaidenAPIRallyBar('test_1502_VC_53873_Get_Device_RallyBar'),
                                  RaidenAPIRallyBar('test_1547_Delete_Room')])
suite_RaidenAPIRallyBarMini.addTests([RaidenAPIRallyBarMini('test_1601_Provision_RallyBarMini_to_Sync_Portal'),
                                      RaidenAPIRallyBarMini('test_1602_VC_53889_Get_Device_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1646_Delete_Room')])
suite_RaidenAPIRallyBarHuddle.addTests([RaidenAPIRallyBarHuddle('test_2001_VC_116691_provision_rally_bar_huddle_in_'
                                                                'appliance_mode_to_sync_portal'),
                                        RaidenAPIRallyBarHuddle('test_2002_VC_116698_get_device_information_rally_bar_'
                                                                'huddle_in_appliance_mode'),
                                        RaidenAPIRallyBarHuddle('test_2022_VC_116745_delete_room_rally_bar_huddle_'
                                                                'in_appliance_mode')])

raiden_envs = {"raiden-prod": "Raiden-Prod-Global", "raiden-prodeu": "Raiden-Prod-EU",
               "raiden-prodfr": "Raiden-Prod-France", "raiden-prodca": "Raiden-Prod-Canada",
               "raiden-latest1": "Raiden-Latest1", "raiden-qa1": "Raiden-QA1", "raiden-qa":"Raiden-QA",
               "raiden-stable1": "Raiden-Stable1"}
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"{raiden_env_name}-Functional-BAT"
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPIHostedDevicesSetup)
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaideAPIRoomGroups)
unittest.TextTestRunner().run(suite_RaideAPIHostGroups)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarHuddle)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarHuddle)
unittest.TextTestRunner().run(suite_RaidenAPIHostedSight)
unittest.TextTestRunner().run(suite_RaideAPIEndUsers)
unittest.TextTestRunner().run(suite_RaidenAPIHotDesks)
unittest.TextTestRunner().run(suite_RaidenAPITestsForFlexDeskHierarchy)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomTearDown)

