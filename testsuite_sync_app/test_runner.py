import unittest

from common import config
# Command Line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-e", "--environment", help="Sync Portal Environment - raiden-prod, raiden-qa, raiden-stable")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_sync_app.tc00_install import Install
from testsuite_sync_app.tc01_meetup import Meetup
from testsuite_sync_app.tc02_rally import Rally
from testsuite_sync_app.tc03_rallycamera import RallyCamera
from testsuite_sync_app.tc04_kong import Kong
from testsuite_sync_app.tc05_diddy import Diddy
# from testsuite_sync_app.tc06_brio import Brio
from testsuite_sync_app.tc07_celestia import Celestia
from testsuite_sync_app.tc08_tap import Tap
from testsuite_sync_app.tc09_swytch import Swytch
from testsuite_sync_app.tc10_tiny import Tiny
from testsuite_sync_app.tc11_sentinel import Sentinel
from testsuite_sync_app.tc23_multiple_devices import MultipleDevices
from testsuite_sync_app.tc24_logisyncutil import LogiSyncUtil
from testsuite_sync_app.tc25_uninstall import Uninstall
from testsuite_sync_app.tc26_first_run_experience import FRE
from testsuite_sync_app.tc28_provision_code import ProvisionCode

# Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)
tests_Meetup = unittest.TestLoader().loadTestsFromTestCase(Meetup)
tests_Rally = unittest.TestLoader().loadTestsFromTestCase(Rally)
tests_RallyCamera = unittest.TestLoader().loadTestsFromTestCase(RallyCamera)
tests_Kong = unittest.TestLoader().loadTestsFromTestCase(Kong)
tests_Diddy = unittest.TestLoader().loadTestsFromTestCase(Diddy)
# Commenting as the device is not available in the lab for test
# tests_Brio = unittest.TestLoader().loadTestsFromTestCase(Brio)
tests_Tap = unittest.TestLoader().loadTestsFromTestCase(Tap)
tests_swytch = unittest.TestLoader().loadTestsFromTestCase(Swytch)
tests_Celestia = unittest.TestLoader().loadTestsFromTestCase(Celestia)
tests_Tiny = unittest.TestLoader().loadTestsFromTestCase(Tiny)
tests_Sentinel = unittest.TestLoader().loadTestsFromTestCase(Sentinel)
tests_MultipleDevices= unittest.TestLoader().loadTestsFromTestCase(MultipleDevices)
tests_LogiSyncUtil = unittest.TestLoader().loadTestsFromTestCase(LogiSyncUtil)
tests_Uninstall = unittest.TestLoader().loadTestsFromTestCase(Uninstall)
tests_FRE = unittest.TestLoader().loadTestsFromTestCase(FRE)
tests_ProvisionCode = unittest.TestLoader().loadTestsFromTestCase(ProvisionCode)

# Setup Suite
suite_Install = unittest.TestSuite(tests_Install)
suite_Meetup = unittest.TestSuite(tests_Meetup)
suite_Rally = unittest.TestSuite(tests_Rally)
suite_RallyCamera = unittest.TestSuite(tests_RallyCamera)
suite_Kong = unittest.TestSuite(tests_Kong)
suite_Diddy = unittest.TestSuite(tests_Diddy)
# suite_Brio = unittest.TestSuite(tests_Brio)
suite_Tap = unittest.TestSuite(tests_Tap)
suite_Swytch = unittest.TestSuite(tests_swytch)
suite_Celestia = unittest.TestSuite(tests_Celestia)
suite_Tiny = unittest.TestSuite(tests_Tiny)
suite_Sentinel = unittest.TestSuite(tests_Sentinel)
suite_MultipleDevices = unittest.TestSuite(tests_MultipleDevices)
suite_LogiSyncUtil = unittest.TestSuite(tests_LogiSyncUtil)
suite_Uninstall = unittest.TestSuite(tests_Uninstall)
suite_FRE = unittest.TestSuite(tests_FRE)
suite_ProvisionCode = unittest.TestSuite(tests_ProvisionCode)

# Run Suite
if args.retry is not None:
    global_variables.retry_count = args.retry
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
global_variables.email_flag = True
EmailNotification.send_job_email()
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_Install)
unittest.TextTestRunner().run(suite_Meetup)
unittest.TextTestRunner().run(suite_Rally)
unittest.TextTestRunner().run(suite_RallyCamera)
unittest.TextTestRunner().run(suite_Kong)
unittest.TextTestRunner().run(suite_Diddy)
# unittest.TextTestRunner().run(suite_Brio)
unittest.TextTestRunner().run(suite_Tap)
unittest.TextTestRunner().run(suite_Swytch)
unittest.TextTestRunner().run(suite_Celestia)
unittest.TextTestRunner().run(suite_Tiny)
unittest.TextTestRunner().run(suite_Sentinel)
unittest.TextTestRunner().run(suite_MultipleDevices)
unittest.TextTestRunner().run(suite_LogiSyncUtil)
unittest.TextTestRunner().run(suite_Uninstall)
unittest.TextTestRunner().run(suite_FRE)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_ProvisionCode)
