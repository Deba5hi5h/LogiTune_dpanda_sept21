import unittest
import sys
sys.path.insert(1, '../')
sys.path.insert(1, '../apis/sync_api/library/protobuf/compiled/python')

from common import config
#Command Line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n","--installer", help="installer version")
parser.add_argument("-a","--api", help="api version")
parser.add_argument("-r", "--retry", help="retry count")
args = parser.parse_args()

#Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.api is not None:
    settings.set_value_in_section('RUN_CONFIG', 'SYNC_API_VERSION', args.api)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_sync_api.blesettings_sync_api import LogiSyncBLESettingsAPI
from testsuite_sync_api.videosettings_sync_api import LogiSyncVideoSettingAPI
from testsuite_sync_api.room_sync_api import LogiSyncRoomAPI
from testsuite_sync_api.configuration_sync_api import  LogiSyncConfigurationAPI
from testsuite_sync_api.products_sync_API import LogiSyncProductAPI
from testsuite_sync_api.device_settings_sync_api import LogiSyncDeviceSettingsAPI
from testsuite_sync_api.firmware_sync_api import LogiSyncFirmwareAPI
from testsuite_sync_api.sync_api_setup import SyncAPISetup
from testsuite_sync_api.sync_api_teardown import SyncAPITeardown

tests_LogiSyncProductAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncProductAPI)
tests_LogiSyncRoomAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncRoomAPI)
tests_LogiSyncConfigurationAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncConfigurationAPI)
tests_LogiSyncDeviceSettingsAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncDeviceSettingsAPI)
tests_LogiSyncVideoSettingAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncVideoSettingAPI)
tests_LogiSyncFirmwareAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncFirmwareAPI)
tests_LogiSyncBLESettingsAPI = unittest.TestLoader().loadTestsFromTestCase(LogiSyncBLESettingsAPI)
tests_SyncAPISetup = unittest.TestLoader().loadTestsFromTestCase(SyncAPISetup)
tests_SyncAPITeardown = unittest.TestLoader().loadTestsFromTestCase(SyncAPITeardown)

suite_LogiSyncProductAPI = unittest.TestSuite(tests_LogiSyncProductAPI)
suite_LogiSyncRoomAPI = unittest.TestSuite(tests_LogiSyncRoomAPI)
suite_LogiSyncConfigurationAPI= unittest.TestSuite(tests_LogiSyncConfigurationAPI)
suite_LogiSyncDeviceSettingsAPI = unittest.TestSuite(tests_LogiSyncDeviceSettingsAPI)
suite_LogiSyncVideoSettingAPI = unittest.TestSuite(tests_LogiSyncVideoSettingAPI)
suite_LogiSyncFirmwareAPI = unittest.TestSuite(tests_LogiSyncFirmwareAPI)
suite_LogiSyncBLESettingsAPI = unittest.TestSuite(tests_LogiSyncBLESettingsAPI)
suite_SyncAPISetup = unittest.TestSuite(tests_SyncAPISetup)
suite_SyncAPITeardown = unittest.TestSuite(tests_SyncAPITeardown)

if args.retry is not None:
    global_variables.retry_count = args.retry
global_variables.email_flag = True
EmailNotification.send_job_email()
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_SyncAPISetup)
unittest.TextTestRunner().run(suite_LogiSyncProductAPI)
unittest.TextTestRunner().run(suite_LogiSyncRoomAPI)
unittest.TextTestRunner().run(suite_LogiSyncConfigurationAPI)
unittest.TextTestRunner().run(suite_LogiSyncDeviceSettingsAPI)
unittest.TextTestRunner().run(suite_LogiSyncVideoSettingAPI)
unittest.TextTestRunner().run(suite_LogiSyncFirmwareAPI)
#Remaining suites here
unittest.TextTestRunner().run(suite_LogiSyncBLESettingsAPI)
global_variables.teardownFlag = True #This should be just before the last suite
unittest.TextTestRunner().run(suite_SyncAPITeardown)
