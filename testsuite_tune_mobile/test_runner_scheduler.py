import time
import unittest
from common import config
# Command Line arguments
import argparse
from apps.tune_mobile.config import tune_mobile_config

parser = argparse.ArgumentParser()
parser.add_argument("-qv", "--qa_version", help="QA version of App to be tested")
parser.add_argument("-pv", "--prod_version", help="Current Prod version of App")
parser.add_argument("-up", "--user_phone", help="User phone for running tests")
parser.add_argument("-tp", "--teammate_phone", help="Teammate phone for running tests")
parser.add_argument("-p", "--port", help="Appium port")
parser.add_argument("-b", "--building", help="Sync Portal building to test")
args = parser.parse_args()

# Run Configuration
tune_mobile_config.phone = "S22"
tune_mobile_config.teammate_phone = "iPhone15"
tune_mobile_config.building = "Logi-Auto"
tune_mobile_config.port = 4723
prod_version = '3.14.0-30062'
qa_version = '3.15.0-30063'
real_devices = ["iPhone12", "Pixel2", "OnePlus", "S22", "iPhone15"]
settings = config.CommonConfig.get_instance()
if args.qa_version is not None:
    qa_version = args.qa_version
if args.prod_version is not None:
    prod_version = args.prod_version
if args.user_phone is not None:
    tune_mobile_config.phone = args.user_phone
if args.teammate_phone is not None:
    tune_mobile_config.teammate_phone = args.teammate_phone
if args.port is not None:
    tune_mobile_config.port = args.port
if args.building is not None:
    tune_mobile_config.building = args.building

settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', qa_version)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'TuneMobile')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_tune_mobile.tc00_install_app import InstallApp
from testsuite_tune_mobile.tc02_scheduler_signin import SchedulerSignIn
from testsuite_tune_mobile.tc03_scheduler_people import SchedulerPeople
from testsuite_tune_mobile.tc04_scheduler_book import SchedulerBook
from testsuite_tune_mobile.tc01_scheduler_notify_teammate import SchedulerNotifyTeammate
from testsuite_tune_mobile.tc05_scheduler_notifications import SchedulerNotifications
from testsuite_tune_mobile.tc06_scheduler_custom_team import SchedulerCustomTeam
from apps.tune_mobile.tune_mobile_utils import TuneMobileUtils
from testsuite_tune_mobile.tc01_headset_functionality import HeadsetFunctionality

# Load Tests
tests_functional = unittest.TestLoader().loadTestsFromTestCase(HeadsetFunctionality)
tests_install = unittest.TestLoader().loadTestsFromTestCase(InstallApp)
tests_signin = unittest.TestLoader().loadTestsFromTestCase(SchedulerSignIn)
tests_people = unittest.TestLoader().loadTestsFromTestCase(SchedulerPeople)
tests_book = unittest.TestLoader().loadTestsFromTestCase(SchedulerBook)
tests_notify_teammate = unittest.TestLoader().loadTestsFromTestCase(SchedulerNotifyTeammate)
tests_notifications = unittest.TestLoader().loadTestsFromTestCase(SchedulerNotifications)
tests_custom_team = unittest.TestLoader().loadTestsFromTestCase(SchedulerCustomTeam)

# Setup Suite
suite_install = unittest.TestSuite(tests_install)
suite_signin = unittest.TestSuite(tests_signin)
suite_people = unittest.TestSuite(tests_people)
suite_book = unittest.TestSuite(tests_book)
suite_notify_teammate = unittest.TestSuite(tests_notify_teammate)
suite_notifications = unittest.TestSuite(tests_notifications)
suite_custom_team = unittest.TestSuite(tests_custom_team)


# Run Suite
# global_variables.email_flag = True
# EmailNotification.send_job_email()

real_device = True if tune_mobile_config.phone in real_devices else False
emulators = []
TuneMobileUtils.start_appium(port=tune_mobile_config.port)
if tune_mobile_config.phone not in real_devices:
    TuneMobileUtils.start_emulator(tune_mobile_config.phone)
    emulators.append(tune_mobile_config.phone)
if tune_mobile_config.teammate_phone not in real_devices:
    TuneMobileUtils.start_emulator(tune_mobile_config.teammate_phone)
    emulators.append(tune_mobile_config.teammate_phone)
global_variables.update_test_automation_field = True
global_variables.retry_count = 1
global_variables.test_category = "Scheduler"
global_variables.dashboard_unmount = False
global_variables.teardownFlag = False
InstallApp.prod_version = prod_version
InstallApp.current_version = qa_version
unittest.TextTestRunner().run(suite_install)
if InstallApp.continue_execution:
    unittest.TextTestRunner().run(suite_notify_teammate)
    unittest.TextTestRunner().run(suite_book)
    unittest.TextTestRunner().run(suite_people)
    unittest.TextTestRunner().run(suite_notifications)
    unittest.TextTestRunner().run(suite_custom_team)
    global_variables.teardownFlag = True
    unittest.TextTestRunner().run(suite_signin)
for emulator in emulators:
    TuneMobileUtils.stop_emulator(device_name=emulator)