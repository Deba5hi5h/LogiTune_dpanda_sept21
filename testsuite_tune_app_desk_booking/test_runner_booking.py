import unittest

from common import config
from base import global_variables


#Command Line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-e", "--email_notification", help="send email notification", default=True,
                    type=lambda x: (str(x).lower() == 'true'))
args = parser.parse_args()

#Run Configuration
settings = config.CommonConfig.get_instance()
settings.set_value_in_section('JENKINS_FWU_TESTS', 'JENKINS_FWU_CONFIG', 'True')

if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'LogiTune')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
settings.set_value_in_section('RUN_CONFIG', 'jira_update', 'True')

global_variables.test_category = f'Desk Booking Tune: {args.installer}'

mailing_list = (
    'ptokarczyk@logitech.com',
    'plesniak@logitech.com',
    'rdrozd@logitech.com',
    'sveerbhadrappa@logitech.com',
    'bchandrashekar@logitech.com',
)

from testsuite_tune_app.test_runner import run_tests

from testsuite_tune_app_desk_booking.tc01_desk_booking import DeskBooking
from testsuite_tune_app_desk_booking.tc02_home_dashboard_google import HomeDashboardGoogle
from testsuite_tune_app_desk_booking.tc02_home_dashboard_microsoft import HomeDashboardMicrosoft
from testsuite_tune_app_desk_booking.tc03_user_profile_google import UserProfileGoogle
from testsuite_tune_app_desk_booking.tc03_user_profile_microsoft import UserProfileMicrosoft
from testsuite_tune_app_desk_booking.tc04_notifications_google import NotificationsPageGoogle
from testsuite_tune_app_desk_booking.tc04_notifications_microsoft import NotificationsPageMicrosoft
from testsuite_tune_app_desk_booking.tc05_multiple_day_booking_microsoft import MultipleDayBookingMicrosoft
from testsuite_tune_app_desk_booking.tc05_multiple_day_booking_google import MultipleDayBookingGoogle
from testsuite_tune_app_desk_booking.tc06_people_tab_microsoft import PeoplePageMicrosoft
from testsuite_tune_app_desk_booking.tc06_people_tab_google import PeoplePageGoogle
from testsuite_tune_app_desk_booking.tc07_team_creation_microsoft import TeamCreationMicrosoft
from testsuite_tune_app_desk_booking.tc07_team_creation_google import TeamCreationGoogle
from testsuite_tune_app_desk_booking.tc08_map_dashboard_microsoft import MapsMicrosoft
from testsuite_tune_app_desk_booking.tc08_map_dashboard_google import MapsGoogle
from testsuite_tune_app_desk_booking.tc09_notify_teammates_microsoft import NotifyTeammatesMicrosoft
from testsuite_tune_app_desk_booking.tc09_notify_teammates_google import NotifyTeammatesGoogle


tc_to_run = [
    HomeDashboardMicrosoft,
    HomeDashboardGoogle,
    UserProfileMicrosoft,
    UserProfileGoogle,
    NotificationsPageMicrosoft,
    NotificationsPageGoogle,
    MultipleDayBookingMicrosoft,
    MultipleDayBookingGoogle,
    PeoplePageMicrosoft,
    PeoplePageGoogle,
    TeamCreationMicrosoft,
    TeamCreationGoogle,
    MapsMicrosoft,
    MapsGoogle,
    NotifyTeammatesMicrosoft,
    NotifyTeammatesGoogle
]


if __name__ == '__main__':
    run_tests(tc_to_run, retry=args.retry, mailing=args.email_notification, install_tune=True)

