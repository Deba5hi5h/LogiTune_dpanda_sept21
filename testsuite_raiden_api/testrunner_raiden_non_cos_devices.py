import unittest
import argparse
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from base import global_variables
from common import config
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-qa, raiden-stable, "
                                                "raiden-latest1, raiden-qa1,raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_users import RaidenAPIUser
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_room_note import RaidenAPIRoomNote
from testsuite_raiden_api.raiden_api_meeting_rooms_setup import RaidenAPIMeetingRoomSetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_brio import RaidenAPIBrio
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_meetup import RaidenAPIMeetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rally_camera import RaidenAPIRallyCamera
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rally_system import RaidenAPIRallySystem
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tap import RaidenAPITap
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_celestia import RaidenAPICelestia
from testsuite_raiden_api.raiden_api_meeting_rooms_teardown import RaidenAPIMeetingRoomTearDown
from testsuite_raiden_api.users.raiden_api_endusers import RaideAPIEndUsers
from testsuite_raiden_api.users.raiden_api_endusers_group import RaideAPIEndUsersGroups
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_updatechannel import RaideAPIUpdateChannel
from testsuite_raiden_api.hot_desks.raiden_api_flexdesks_updatechannel import RaideAPIUpdateChannelForFlexDesks
from testsuite_raiden_api.hot_desks.raiden_api_flexdesk_hierarchy import RaidenAPITestsForFlexDeskHierarchy
from testsuite_raiden_api.hot_desks.raiden_api_move_desk_to_group import RaidenAPIMoveDeskToGroup
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_policy import RaidenAPIUpdateFlexDesksPolicy
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_book_a_session import RaidenAPIFlexDeskSessionBooking
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_booking_settings import RaidenAPIFlexDeskBookingSettings
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_it_pin_setting_for_a_group import RaidenAPIFlexDeskITPinSettingForGroup

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaidenAPIRoomNote = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomNote)
tests_RaidenAPIMeetingRoomSetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomSetup)
tests_RaidenAPIBrio = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIBrio)
tests_RaidenAPIMeetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetup)
tests_RaidenAPIRallyCamera = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyCamera)
tests_RaidenAPIRallySystem = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallySystem)
tests_RaidenAPITap = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITap)
tests_RaidenAPICelestia = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICelestia)
tests_RaidenAPIMeetingRoomTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomTearDown)
tests_RaidenAPIEndUser = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsers)
tests_RaidenAPIEndUsersGroup = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsersGroups)
test_RaidenAPIUpdateChannel = unittest.TestLoader().loadTestsFromTestCase(RaideAPIUpdateChannel)
test_RaidenAPIUpdateChannelForFlexDesks = unittest.TestLoader().loadTestsFromTestCase(RaideAPIUpdateChannelForFlexDesks)
test_RaidenAPITestsForFlexDeskHierarchy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITestsForFlexDeskHierarchy)
test_RaidenAPIMoveDeskToGroup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMoveDeskToGroup)
test_RaidenAPIUpdateFlexDesksPolicy = unittest.TestLoader.loadTestsFromTestCase(RaidenAPIUpdateFlexDesksPolicy)
test_RaidenAPIFlexDeskSessionBooking = unittest.TestLoader.loadTestsFromTestCase(RaidenAPIFlexDeskSessionBooking)
test_RaidenAPIFlexDeskBookingSettings = unittest.TestLoader.loadTestsFromTestCase(RaidenAPIFlexDeskBookingSettings)
test_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestLoader.loadTestsFromTestCase(RaidenAPIFlexDeskITPinSettingForGroup)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaidenAPIRoomNote = unittest.TestSuite(tests_RaidenAPIRoomNote)
suite_RaidenAPIMeetingRoomSetup = unittest.TestSuite(tests_RaidenAPIMeetingRoomSetup)
suite_RaidenAPIBrio = unittest.TestSuite(tests_RaidenAPIBrio)
suite_RaidenAPIMeetup = unittest.TestSuite(tests_RaidenAPIMeetup)
suite_RaidenAPIRallyCamera = unittest.TestSuite(tests_RaidenAPIRallyCamera)
suite_RaidenAPIRallySystem = unittest.TestSuite(tests_RaidenAPIRallySystem)
suite_RaidenAPITap = unittest.TestSuite(tests_RaidenAPITap)
suite_RaidenAPICelestia = unittest.TestSuite(tests_RaidenAPICelestia)
suite_RaidenAPIMeetingRoomTearDown = unittest.TestSuite(tests_RaidenAPIMeetingRoomTearDown)
suite_RaidenAPIEndUser = unittest.TestSuite(tests_RaidenAPIEndUser)
suite_RaidenAPIEndUsersGroup = unittest.TestSuite(tests_RaidenAPIEndUsersGroup)
suite_RaidenAPIUpdateChannel = unittest.TestSuite(test_RaidenAPIUpdateChannel)
suite_RaidenAPIUpdateChannelForFlexDesks = unittest.TestSuite(test_RaidenAPIUpdateChannelForFlexDesks)
suite_test_RaidenAPITestsForFlexDeskHierarchy = unittest.TestSuite(test_RaidenAPITestsForFlexDeskHierarchy)
suite_RaidenAPIMoveDeskToGroup = unittest.TestSuite(test_RaidenAPIMoveDeskToGroup)
suite_RaidenAPIUpdateFlexDesksPolicy = unittest.TestSuite(test_RaidenAPIUpdateFlexDesksPolicy)
suite_RaidenAPIFlexDeskSessionBooking = unittest.TestSuite(test_RaidenAPIFlexDeskSessionBooking)
suite_RaidenAPIFlexDeskBookingSettings = unittest.TestSuite(test_RaidenAPIFlexDeskBookingSettings)
suite_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestSuite(test_RaidenAPIFlexDeskITPinSettingForGroup)

global_variables.test_category = 'Functional'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIEndUser)
unittest.TextTestRunner().run(suite_RaidenAPIEndUsersGroup)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaidenAPIRoomNote)
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomSetup)
unittest.TextTestRunner().run(suite_RaidenAPIBrio)
unittest.TextTestRunner().run(suite_RaidenAPIMeetup)
unittest.TextTestRunner().run(suite_RaidenAPIRallyCamera)
unittest.TextTestRunner().run(suite_RaidenAPIRallySystem)
unittest.TextTestRunner().run(suite_RaidenAPITap)
unittest.TextTestRunner().run(suite_RaidenAPICelestia)
unittest.TextTestRunner().run(suite_RaidenAPIEndUser)
unittest.TextTestRunner().run(suite_RaidenAPIEndUsersGroup)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateChannel)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateChannelForFlexDesks)
unittest.TextTestRunner().run(suite_test_RaidenAPITestsForFlexDeskHierarchy)
unittest.TextTestRunner().run(suite_RaidenAPIMoveDeskToGroup)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateFlexDesksPolicy)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskSessionBooking)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskBookingSettings)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskITPinSettingForGroup)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomTearDown)


