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
from testsuite_raiden_api.users.raiden_api_it_user_access_control import RaidenAPIITUserAccessControl
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_room_note import RaidenAPIRoomNote
from testsuite_raiden_api.meeting_rooms.room_groups.raiden_api_room_groups import RaideAPIRoomGroups
from testsuite_raiden_api.personal_devices.host_groups.raiden_api_host_groups import RaideAPIHostGroups
from testsuite_raiden_api.raiden_api_hosted_devices_setup import RaidenAPIHostedDevicesSetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybar import RaidenAPIHostedRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarmini import RaidenAPIHostedRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarhuddle import RaidenAPIHostedRallyBarHuddle
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybar import RaidenAPIRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarmini import RaidenAPIRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarhuddle import RaidenAPIRallyBarHuddle
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_roomMate import RaidenAPIRoomMate
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapip import RaidenAPITapIP
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapscheduler import RaidenAPITapScheduler
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_sight import RaidenAPIHostedSight
from testsuite_raiden_api.raiden_api_meeting_rooms_teardown import RaidenAPIMeetingRoomTearDown
from testsuite_raiden_api.users.raiden_api_endusers import RaideAPIEndUsers
from testsuite_raiden_api.users.raiden_api_endusers_group import RaideAPIEndUsersGroups
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_updatechannel import RaideAPIUpdateChannel
from testsuite_raiden_api.hot_desks.raiden_api_hot_desks import RaidenAPIHotDesks
from testsuite_raiden_api.hot_desks.raiden_api_flexdesks_updatechannel import RaideAPIUpdateChannelForFlexDesks
from testsuite_raiden_api.hot_desks.raiden_api_flexdesk_hierarchy import RaidenAPITestsForFlexDeskHierarchy
from testsuite_raiden_api.hot_desks.raiden_api_move_desk_to_group import RaidenAPIMoveDeskToGroup
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_policy import RaidenAPIUpdateFlexDesksPolicy
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_book_a_session import RaidenAPIFlexDeskSessionBooking
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_it_pin_setting_for_a_group import RaidenAPIFlexDeskITPinSettingForGroup
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_device_settings_usb_3_internet_time import RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_device_settings_local_area_network import RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_reboot_device_deprovision_device import RaidenAPIFlexDeskRebootDeprovisionDevice
from testsuite_raiden_api.hot_desks.raiden_api_sync_portal_maps import RaidenAPISyncPortalMaps
from testsuite_raiden_api.hot_desks.raiden_api_get_desk_activity_get_coily_info import RaidenAPIGetDeskActivityGetCoilyInfo
from testsuite_raiden_api.users.raiden_api_owner import RaidenAPIOwner
from testsuite_raiden_api.users.raiden_api_sysadmin import RaidenAPISystemAdmin
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_booking_settings import RaidenAPIFlexDeskBookingSettings
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_coily_group_settings import RaidenAPIFlexDeskCoilyGroupSettings
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_coily_insights import RaideAPICoilyInsights
from testsuite_raiden_api.hot_desks.raiden_api_get_flex_desk_collabos_system_image_version import RaidenAPIGetFlexDeskCollabOSSystemImageVersion
from testsuite_raiden_api.hot_desks.raiden_api_get_flex_desk_use_state import RaidenAPIGetFlexDeskUseState
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_custom_tags import RaidensApiCustomTags

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIITUserAccessControl = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIITUserAccessControl)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaidenAPIRoomNote = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomNote)
tests_RaideAPIRoomGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIRoomGroups)
tests_RaideAPIHostGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIHostGroups)
tests_RaidenAPIHostedDevicesSetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedDevicesSetup)
tests_RaidenAPIHostedRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBar)
tests_RaidenAPIHostedRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarMini)
tests_RaidenAPIHostedRallyBarHuddle = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarHuddle)
tests_RaidenAPIRallyBar = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBar)
tests_RaidenAPIRallyBarMini = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarMini)
tests_RaidenAPIRallyBarHuddle = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarHuddle)
tests_RaidenAPIRoomMate = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRoomMate)
tests_RaidenAPITapIP = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapIP)
tests_RaidenAPITapScheduler = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITapScheduler)
tests_RaidenAPIHostedSight = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedSight)
tests_RaidenAPIMeetingRoomTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomTearDown)
tests_RaideAPIEndUsers = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsers)
tests_RaideAPIEndUsersGroups = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsersGroups)
tests_RaideAPIUpdateChannel = unittest.TestLoader().loadTestsFromTestCase(RaideAPIUpdateChannel)
tests_RaidenAPIHotDesks = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHotDesks)
tests_RaideAPIUpdateChannelForFlexDesks = unittest.TestLoader().loadTestsFromTestCase(RaideAPIUpdateChannelForFlexDesks)
tests_RaidenAPITestsForFlexDeskHierarchy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITestsForFlexDeskHierarchy)
tests_RaidenAPIMoveDeskToGroup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMoveDeskToGroup)
tests_RaidenAPIUpdateFlexDesksPolicy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUpdateFlexDesksPolicy)
tests_RaidenAPIFlexDeskSessionBooking = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskSessionBooking)
tests_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskITPinSettingForGroup)
tests_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
tests_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
tests_RaidenAPIFlexDeskRebootDeprovisionDevice = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskRebootDeprovisionDevice)
tests_RaidenAPISyncPortalMaps = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISyncPortalMaps)
tests_RaidenAPIGetDeskActivityGetCoilyInfo = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetDeskActivityGetCoilyInfo)
tests_RaidenAPIOwner = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIOwner)
tests_RaidenAPISystemAdmin = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISystemAdmin)
tests_RaidenAPIFlexDeskBookingSettings = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskBookingSettings)
tests_RaidenAPIFlexDeskCoilyGroupSettings = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskCoilyGroupSettings)
tests_RaideAPICoilyInsights = unittest.TestLoader().loadTestsFromTestCase(RaideAPICoilyInsights)
tests_RaidenAPIGetFlexDeskCollabOSSystemImageVersion = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
tests_RaidenAPIGetFlexDeskUseState = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetFlexDeskUseState)
tests_RaidensApiCustomTags = unittest.TestLoader().loadTestsFromTestCase(RaidensApiCustomTags)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIITUserAccessControl = unittest.TestSuite(tests_RaidenAPIITUserAccessControl)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaidenAPIRoomNote = unittest.TestSuite(tests_RaidenAPIRoomNote)
suite_RaideAPIRoomGroups = unittest.TestSuite(tests_RaideAPIRoomGroups)
suite_RaideAPIHostGroups = unittest.TestSuite(tests_RaideAPIHostGroups)
suite_RaidenAPIHostedDevicesSetup = unittest.TestSuite(tests_RaidenAPIHostedDevicesSetup)
suite_RaidenAPIHostedRallyBar = unittest.TestSuite(tests_RaidenAPIHostedRallyBar)
suite_RaidenAPIHostedRallyBarMini = unittest.TestSuite(tests_RaidenAPIHostedRallyBarMini)
suite_RaidenAPIHostedRallyBarHuddle = unittest.TestSuite(tests_RaidenAPIHostedRallyBarHuddle)
suite_RaidenAPIRallyBar = unittest.TestSuite(tests_RaidenAPIRallyBar)
suite_RaidenAPIRallyBarMini = unittest.TestSuite(tests_RaidenAPIRallyBarMini)
suite_RaidenAPIRallyBarHuddle = unittest.TestSuite(tests_RaidenAPIRallyBarHuddle)
suite_RaidenAPIRoomMate = unittest.TestSuite(tests_RaidenAPIRoomMate)
suite_RaidenAPITapIP = unittest.TestSuite(tests_RaidenAPITapIP)
suite_RaidenAPITapScheduler = unittest.TestSuite(tests_RaidenAPITapScheduler)
suite_RaidenAPIHostedSight = unittest.TestSuite(tests_RaidenAPIHostedSight)
suite_RaidenAPIMeetingRoomTearDown = unittest.TestSuite(tests_RaidenAPIMeetingRoomTearDown)
suite_RaideAPIEndUsers = unittest.TestSuite(tests_RaideAPIEndUsers)
suite_RaideAPIEndUsersGroups = unittest.TestSuite(tests_RaideAPIEndUsersGroups)
suite_RaideAPIUpdateChannel = unittest.TestSuite(tests_RaideAPIUpdateChannel)
suite_RaidenAPIHotDesks = unittest.TestSuite(tests_RaidenAPIHotDesks)
suite_RaideAPIUpdateChannelForFlexDesks = unittest.TestSuite(tests_RaideAPIUpdateChannelForFlexDesks)
suite_RaidenAPITestsForFlexDeskHierarchy = unittest.TestSuite(tests_RaidenAPITestsForFlexDeskHierarchy)
suite_RaidenAPIMoveDeskToGroup = unittest.TestSuite(tests_RaidenAPIMoveDeskToGroup)
suite_RaidenAPIUpdateFlexDesksPolicy = unittest.TestSuite(tests_RaidenAPIUpdateFlexDesksPolicy)
suite_RaidenAPIFlexDeskSessionBooking = unittest.TestSuite(tests_RaidenAPIFlexDeskSessionBooking)
suite_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestSuite(tests_RaidenAPIFlexDeskITPinSettingForGroup)
suite_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime = unittest.TestSuite(tests_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
suite_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork = unittest.TestSuite(tests_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
suite_RaidenAPIFlexDeskRebootDeprovisionDevice = unittest.TestSuite(tests_RaidenAPIFlexDeskRebootDeprovisionDevice)
suite_RaidenAPISyncPortalMaps = unittest.TestSuite(tests_RaidenAPISyncPortalMaps)
suite_RaidenAPIGetDeskActivityGetCoilyInfo = unittest.TestSuite(tests_RaidenAPIGetDeskActivityGetCoilyInfo)
suite_RaidenAPIOwner = unittest.TestSuite(tests_RaidenAPIOwner)
suite_RaidenAPISystemAdmin = unittest.TestSuite(tests_RaidenAPISystemAdmin)
suite_RaidenAPIFlexDeskBookingSettings = unittest.TestSuite(tests_RaidenAPIFlexDeskBookingSettings)
suite_RaidenAPIFlexDeskCoilyGroupSettings = unittest.TestSuite(tests_RaidenAPIFlexDeskCoilyGroupSettings)
suite_RaideAPICoilyInsights = unittest.TestSuite(tests_RaideAPICoilyInsights)
suite_RaidenAPIGetFlexDeskCollabOSSystemImageVersion = unittest.TestSuite(tests_RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
suite_RaidenAPIGetFlexDeskUseState = unittest.TestSuite(tests_RaidenAPIGetFlexDeskUseState)
suite_RaidensApiCustomTags = unittest.TestSuite(tests_RaidensApiCustomTags)

raiden_envs = {"raiden-prod": "Raiden-Prod-Global", "raiden-prodeu": "Raiden-Prod-EU",
               "raiden-prodfr": "Raiden-Prod-France", "raiden-prodca": "Raiden-Prod-Canada",
               "raiden-latest1": "Raiden-Latest1", "raiden-qa1": "Raiden-QA1", "raiden-qa":"Raiden-QA",
               "raiden-stable1": "Raiden-Stable1"}
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"{raiden_env_name}-Functional"
global_variables.email_flag = True
EmailNotification.send_job_email()
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPIHostedDevicesSetup)
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIITUserAccessControl)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaidenAPIRoomNote)
unittest.TextTestRunner().run(suite_RaideAPIRoomGroups)
unittest.TextTestRunner().run(suite_RaideAPIHostGroups)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarHuddle)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarHuddle)
unittest.TextTestRunner().run(suite_RaidenAPIRoomMate)
unittest.TextTestRunner().run(suite_RaidenAPITapIP)
unittest.TextTestRunner().run(suite_RaidenAPITapScheduler)
unittest.TextTestRunner().run(suite_RaidenAPIHostedSight)
unittest.TextTestRunner().run(suite_RaideAPIEndUsers)
unittest.TextTestRunner().run(suite_RaideAPIEndUsersGroups)
unittest.TextTestRunner().run(suite_RaideAPIUpdateChannel)
unittest.TextTestRunner().run(suite_RaidenAPIHotDesks)
unittest.TextTestRunner().run(suite_RaideAPIUpdateChannelForFlexDesks)
unittest.TextTestRunner().run(suite_RaidenAPITestsForFlexDeskHierarchy)
unittest.TextTestRunner().run(suite_RaidenAPIMoveDeskToGroup)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateFlexDesksPolicy)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskITPinSettingForGroup)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskRebootDeprovisionDevice)
unittest.TextTestRunner().run(suite_RaidenAPISyncPortalMaps)
unittest.TextTestRunner().run(suite_RaidenAPIGetDeskActivityGetCoilyInfo)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskSessionBooking)
unittest.TextTestRunner().run(suite_RaidenAPIOwner)
unittest.TextTestRunner().run(suite_RaidenAPISystemAdmin)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskBookingSettings)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskCoilyGroupSettings)
unittest.TextTestRunner().run(suite_RaideAPICoilyInsights)
unittest.TextTestRunner().run(suite_RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
unittest.TextTestRunner().run(suite_RaidenAPIGetFlexDeskUseState)
unittest.TextTestRunner().run(suite_RaidensApiCustomTags)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomTearDown)

