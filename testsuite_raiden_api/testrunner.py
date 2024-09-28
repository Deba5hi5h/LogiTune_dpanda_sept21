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
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-qa, raiden-stable, "
                                                "raiden-latest1, raiden-qa1, raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')

from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_users import RaidenAPIUser
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_room_note import RaidenAPIRoomNote
from testsuite_raiden_api.meeting_rooms.room_groups.raiden_api_room_groups import RaideAPIRoomGroups
from testsuite_raiden_api.personal_devices.host_groups.raiden_api_host_groups import RaideAPIHostGroups
from testsuite_raiden_api.raiden_api_meeting_rooms_setup import RaidenAPIMeetingRoomSetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_brio import RaidenAPIBrio
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_meetup import RaidenAPIMeetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rally_camera import RaidenAPIRallyCamera
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rally_system import RaidenAPIRallySystem
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tap import RaidenAPITap
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_celestia import RaidenAPICelestia
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybar import RaidenAPIHostedRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarmini import RaidenAPIHostedRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybar import RaidenAPIRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarmini import RaidenAPIRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_roomMate import RaidenAPIRoomMate
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapip import RaidenAPITapIP
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapscheduler import RaidenAPITapScheduler
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarhuddle import RaidenAPIRallyBarHuddle
from testsuite_raiden_api.raiden_api_meeting_rooms_teardown import RaidenAPIMeetingRoomTearDown

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaidenAPIRoomNote = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomNote)
tests_RaideAPIRoomGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIRoomGroups)
tests_RaideAPIHostGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIHostGroups)
tests_RaidenAPIMeetingRoomSetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomSetup)
tests_RaidenAPIBrio = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIBrio)
tests_RaidenAPIMeetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetup)
tests_RaidenAPIRallyCamera = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyCamera)
tests_RaidenAPIRallySystem = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallySystem)
tests_RaidenAPITap = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITap)
tests_RaidenAPICelestia = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICelestia)
tests_RaidenAPIHostedRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBar)
tests_RaidenAPIHostedRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarMini)
tests_RaidenAPIRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBar)
tests_RaidenAPIRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarMini)
tests_RaidenAPIRoomMate = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomMate)
tests_RaidenAPITapIP = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapIP)
tests_RaidenAPITapScheduler = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapScheduler)
tests_RaidenAPIRallyBarHuddle = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarHuddle)
tests_RaidenAPIMeetingRoomTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomTearDown)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaidenAPIRoomNote = unittest.TestSuite(tests_RaidenAPIRoomNote)
suite_RaideAPIRoomGroups = unittest.TestSuite(tests_RaideAPIRoomGroups)
suite_RaideAPIHostGroups = unittest.TestSuite(tests_RaideAPIHostGroups)
suite_RaidenAPIMeetingRoomSetup = unittest.TestSuite(tests_RaidenAPIMeetingRoomSetup)
suite_RaidenAPIBrio = unittest.TestSuite(tests_RaidenAPIBrio)
suite_RaidenAPIMeetup = unittest.TestSuite(tests_RaidenAPIMeetup)
suite_RaidenAPIRallyCamera = unittest.TestSuite(tests_RaidenAPIRallyCamera)
suite_RaidenAPIRallySystem = unittest.TestSuite(tests_RaidenAPIRallySystem)
suite_RaidenAPITap = unittest.TestSuite(tests_RaidenAPITap)
suite_RaidenAPICelestia = unittest.TestSuite(tests_RaidenAPICelestia)
suite_RaidenAPIHostedRallyBar = unittest.TestSuite(tests_RaidenAPIHostedRallyBar)
suite_RaidenAPIHostedRallyBarMini = unittest.TestSuite(tests_RaidenAPIHostedRallyBarMini)
suite_RaidenAPIRallyBar = unittest.TestSuite(tests_RaidenAPIRallyBar)
suite_RaidenAPIRallyBarMini = unittest.TestSuite(tests_RaidenAPIRallyBarMini)
suite_RaidenAPIRoomMate = unittest.TestSuite(tests_RaidenAPIRoomMate)
suite_RaidenAPITapIP = unittest.TestSuite(tests_RaidenAPITapIP)
suite_RaidenAPITapScheduler = unittest.TestSuite(tests_RaidenAPITapScheduler)
suite_RaidenAPIRallyBarHuddle = unittest.TestSuite(tests_RaidenAPIRallyBarHuddle)
suite_RaidenAPIMeetingRoomTearDown = unittest.TestSuite(tests_RaidenAPIMeetingRoomTearDown)

global_variables.test_category = 'Functional'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaidenAPIRoomNote)
unittest.TextTestRunner().run(tests_RaideAPIRoomGroups)
unittest.TextTestRunner().run(tests_RaideAPIHostGroups)
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomSetup)
unittest.TextTestRunner().run(suite_RaidenAPIBrio)
unittest.TextTestRunner().run(suite_RaidenAPIMeetup)
unittest.TextTestRunner().run(suite_RaidenAPIRallyCamera)
unittest.TextTestRunner().run(suite_RaidenAPIRallySystem)
unittest.TextTestRunner().run(suite_RaidenAPITap)
unittest.TextTestRunner().run(suite_RaidenAPICelestia)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRoomMate)
unittest.TextTestRunner().run(suite_RaidenAPITapIP)
unittest.TextTestRunner().run(suite_RaidenAPITapScheduler)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarHuddle)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomTearDown)

