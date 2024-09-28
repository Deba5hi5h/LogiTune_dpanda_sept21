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
args = parser.parse_args()

# Run Configuration
tune_mobile_config.phone = "iPhone12"
tune_mobile_config.teammate_phone = "Pixel2"
tune_mobile_config.building = "Logi-Auto"
prod_version = '3.14.0-9'
qa_version = '3.15.0-4'
settings = config.CommonConfig.get_instance()
if args.qa_version is not None:
    qa_version = args.qa_version
if args.prod_version is not None:
    prod_version = args.prod_version
if args.user_phone is not None:
    tune_mobile_config.phone = args.user_phone
if args.teammate_phone is not None:
    tune_mobile_config.teammate_phone = args.teammate_phone

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

# Load Tests
tests_install = unittest.TestLoader().loadTestsFromTestCase(InstallApp)

# Setup Suite
suite_install = unittest.TestSuite(tests_install)
suite_signin = unittest.TestSuite()
suite_people = unittest.TestSuite()
suite_book = unittest.TestSuite()
suite_notify_teammate = unittest.TestSuite()
suite_notifications = unittest.TestSuite()
suite_custom_team = unittest.TestSuite()

#Add Sanity test cases to suite
suite_signin.addTests([SchedulerSignIn('test_2003_VC_98517_connect_to_calendar_microsoft'),
                       SchedulerSignIn('test_2004_VC_99380_profile_work_account_microsoft')
                       ])
suite_people.addTests([SchedulerPeople('test_3001_VC_90724_people_teammates'),
                       SchedulerPeople('test_3002_VC_104625_people_remove_teammate'),
                       SchedulerPeople('test_3013_VC_123227_people_everyone_view_person_profile'),
                       SchedulerPeople('test_3018_VC_104631_people_in_office_teammate_booked_current_date'),
                       SchedulerPeople('test_3022_VC_112717_teammates_nearby_teammate_booked_current_date')
                       ])
suite_book.addTests([SchedulerBook('test_4004_VC_107007_cancel_booking_session_already_started'),
                       SchedulerBook('test_4006_VC_90735_book_desk_future_date_default_building'),
                       SchedulerBook('test_4007_VC_90737_book_desk_by_preference_and_check_in'),
                       SchedulerBook('test_4008_VC_90738_book_near_teammate'),
                       SchedulerBook('test_4010_VC_90749_cancel_and_rebook_same_desk')
                       ])
suite_notify_teammate.addTests([SchedulerNotifyTeammate('test_1001_VC_111082_notify_teammate_with_message_during_booking'),
                       SchedulerNotifyTeammate('test_1002_VC_118356_notify_teammate_with_message_edit_booking'),
                       SchedulerNotifyTeammate('test_1008_VC_107014_teammate_cancels_booking_notification'),
                       SchedulerNotifyTeammate('test_1009_VC_90709_teammate_modifies_booking_notification')
                       ])
suite_notifications.addTests([SchedulerNotifications('test_5002_VC_118477_admin_creates_booking'),
                       SchedulerNotifications('test_5003_VC_118479_admin_deletes_booking'),
                       SchedulerNotifications('test_5004_VC_118478_admin_updates_booking'),
                       SchedulerNotifications('test_5005_VC_107010_check_in_required')
                       ])
suite_custom_team.addTests([SchedulerCustomTeam('test_6002_VC_128150_custom_team_create_new_team'),
                       SchedulerCustomTeam('test_6003_VC_128152_custom_team_add_teammates_screen'),
                       SchedulerCustomTeam('test_6004_VC_128154_custom_team_multiple_teams')
                       ])

# Run Suite
# global_variables.email_flag = True
# EmailNotification.send_job_email()
TuneMobileUtils.start_appium()
TuneMobileUtils.start_emulator(tune_mobile_config.phone)
TuneMobileUtils.start_emulator(tune_mobile_config.teammate_phone)
global_variables.update_test_automation_field = True
global_variables.retry_count = 1
global_variables.test_category = "Scheduler-Sanity"
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
TuneMobileUtils.stop_appium()
TuneMobileUtils.stop_emulator()