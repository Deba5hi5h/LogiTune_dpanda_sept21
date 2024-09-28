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
from testsuite_raiden_api.users.raiden_api_endusers import RaideAPIEndUsers
from testsuite_raiden_api.users.raiden_api_endusers_group import RaideAPIEndUsersGroups
from testsuite_raiden_api.hot_desks.raiden_api_flexdesks_updatechannel import RaideAPIUpdateChannelForFlexDesks
from testsuite_raiden_api.hot_desks.raiden_api_flexdesk_hierarchy import RaidenAPITestsForFlexDeskHierarchy
from testsuite_raiden_api.hot_desks.raiden_api_hot_desks import RaidenAPIHotDesks
from testsuite_raiden_api.hot_desks.raiden_api_move_desk_to_group import RaidenAPIMoveDeskToGroup
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_policy import RaidenAPIUpdateFlexDesksPolicy
from testsuite_raiden_api.hot_desks.raiden_api_flex_desks_book_a_session import RaidenAPIFlexDeskSessionBooking
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_it_pin_setting_for_a_group import RaidenAPIFlexDeskITPinSettingForGroup
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_device_settings_usb_3_internet_time import RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_device_settings_local_area_network import RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_reboot_device_deprovision_device import RaidenAPIFlexDeskRebootDeprovisionDevice
from testsuite_raiden_api.hot_desks.raiden_api_sync_portal_maps import RaidenAPISyncPortalMaps
from testsuite_raiden_api.hot_desks.raiden_api_get_desk_activity_get_coily_info import RaidenAPIGetDeskActivityGetCoilyInfo
from testsuite_raiden_api.hot_desks.raiden_api_get_flex_desk_collabos_system_image_version import RaidenAPIGetFlexDeskCollabOSSystemImageVersion
from testsuite_raiden_api.hot_desks.raiden_api_get_flex_desk_use_state import RaidenAPIGetFlexDeskUseState
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_booking_settings import RaidenAPIFlexDeskBookingSettings
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_coily_group_settings import RaidenAPIFlexDeskCoilyGroupSettings
from testsuite_raiden_api.hot_desks.raiden_api_flex_desk_coily_insights import RaideAPICoilyInsights

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPIEndUser = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsers)
tests_RaidenAPIEndUsersGroup = unittest.TestLoader().loadTestsFromTestCase(RaideAPIEndUsersGroups)
tests_RaidenAPIUpdateChannelForFlexDesks = unittest.TestLoader().loadTestsFromTestCase(RaideAPIUpdateChannelForFlexDesks)
tests_RaidenAPITestsForFlexDeskHierarchy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPITestsForFlexDeskHierarchy)
tests_RaidenAPIHotDesks = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHotDesks)
tests_RaidenAPIMoveDeskToGroup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMoveDeskToGroup)
tests_RaidenAPIUpdateFlexDesksPolicy = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUpdateFlexDesksPolicy)
tests_RaidenAPIFlexDeskSessionBooking = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskSessionBooking)
tests_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskITPinSettingForGroup)
tests_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
tests_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
tests_RaidenAPIFlexDeskRebootDeprovisionDevice = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskRebootDeprovisionDevice)
tests_RaidenAPISyncPortalMaps = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISyncPortalMaps)
tests_RaidenAPIGetDeskActivityGetCoilyInfo = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetDeskActivityGetCoilyInfo)
tests_RaidenAPIGetFlexDeskCollabOSSystemImageVersion = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
tests_RaidenAPIGetFlexDeskUseState = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIGetFlexDeskUseState)
tests_RaidenAPIFlexDeskBookingSettings =unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskBookingSettings)
tests_RaidenAPIFlexDeskCoilyGroupSettings = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIFlexDeskCoilyGroupSettings)
tests_RaideAPICoilyInsights = unittest.TestLoader().loadTestsFromTestCase(RaideAPICoilyInsights)

suite_RaidenAPISession = unittest.TestSuite()
suite_RaidenAPISession.addTests([RaidenAPISession('test_101_VC_12849_get_raiden_backend_version')])
suite_RaidenAPIEndUser = unittest.TestSuite(tests_RaidenAPIEndUser)
suite_RaidenAPIEndUsersGroup = unittest.TestSuite(tests_RaidenAPIEndUsersGroup)
suite_RaidenAPIUpdateChannelForFlexDesks = unittest.TestSuite(tests_RaidenAPIUpdateChannelForFlexDesks)
suite_RaidenAPITestsForFlexDeskHierarchy = unittest.TestSuite(tests_RaidenAPITestsForFlexDeskHierarchy)
suite_RaidenAPIHotDesks = unittest.TestSuite(tests_RaidenAPIHotDesks)
suite_RaidenAPIMoveDeskToGroup = unittest.TestSuite(tests_RaidenAPIMoveDeskToGroup)
suite_RaidenAPIUpdateFlexDesksPolicy = unittest.TestSuite(tests_RaidenAPIUpdateFlexDesksPolicy)
suite_RaidenAPIFlexDeskSessionBooking = unittest.TestSuite(tests_RaidenAPIFlexDeskSessionBooking)
suite_RaidenAPIFlexDeskITPinSettingForGroup = unittest.TestSuite(tests_RaidenAPIFlexDeskITPinSettingForGroup)
suite_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime = unittest.TestSuite(tests_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
suite_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork = unittest.TestSuite(tests_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
suite_RaidenAPIFlexDeskRebootDeprovisionDevice = unittest.TestSuite(tests_RaidenAPIFlexDeskRebootDeprovisionDevice)
suite_RaidenAPISyncPortalMaps = unittest.TestSuite(tests_RaidenAPISyncPortalMaps)
suite_RaidenAPIGetDeskActivityGetCoilyInfo = unittest.TestSuite(tests_RaidenAPIGetDeskActivityGetCoilyInfo)
suite_RaidenAPIGetFlexDeskCollabOSSystemImageVersion = unittest.TestSuite(tests_RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
suite_RaidenAPIGetFlexDeskUseState = unittest.TestSuite(tests_RaidenAPIGetFlexDeskUseState)
suite_RaidenAPIFlexDeskBookingSettings = unittest.TestSuite(tests_RaidenAPIFlexDeskBookingSettings)
suite_RaidenAPIFlexDeskCoilyGroupSettings = unittest.TestSuite(tests_RaidenAPIFlexDeskCoilyGroupSettings)
suite_RaideAPICoilyInsights = unittest.TestSuite(tests_RaideAPICoilyInsights)

raiden_envs = {"raiden-prod": "Raiden-Prod-Global", "raiden-prodeu": "Raiden-Prod-EU",
               "raiden-prodfr": "Raiden-Prod-France", "raiden-prodca": "Raiden-Prod-Canada",
               "raiden-latest1": "Raiden-Latest1", "raiden-qa1": "Raiden-QA1", "raiden-qa":"Raiden-QA",
               "raiden-stable1": "Raiden-Stable1"}
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"{raiden_env_name}-Coily-Functional"
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIEndUser)
unittest.TextTestRunner().run(suite_RaidenAPIEndUsersGroup)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateChannelForFlexDesks)
unittest.TextTestRunner().run(suite_RaidenAPITestsForFlexDeskHierarchy)
unittest.TextTestRunner().run(suite_RaidenAPIHotDesks)
unittest.TextTestRunner().run(suite_RaidenAPIMoveDeskToGroup)
unittest.TextTestRunner().run(suite_RaidenAPIUpdateFlexDesksPolicy)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskITPinSettingForGroup)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskDeviceSettingsLocalAreaNetwork)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskRebootDeprovisionDevice)
unittest.TextTestRunner().run(suite_RaidenAPISyncPortalMaps)
unittest.TextTestRunner().run(suite_RaidenAPIGetDeskActivityGetCoilyInfo)
unittest.TextTestRunner().run(suite_RaidenAPIGetFlexDeskCollabOSSystemImageVersion)
unittest.TextTestRunner().run(suite_RaidenAPIGetFlexDeskUseState)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskBookingSettings)
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskCoilyGroupSettings)
unittest.TextTestRunner().run(suite_RaideAPICoilyInsights)

global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIFlexDeskSessionBooking)


