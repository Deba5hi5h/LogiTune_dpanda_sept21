import unittest

from common import config
from base import global_variables


#Command Line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-c", "--coily_version", help="coily version")
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

global_variables.test_category = f'Coily CollabOS v{args.coily_version}'

mailing_list = (
    'ptokarczyk@logitech.com',
    'plesniak@logitech.com',
    'rdrozd@logitech.com',
    'sveerbhadrappa@logitech.com',
    'bchandrashekar@logitech.com',
)

from testsuite_tune_app.test_runner import run_tests

from testsuite_tune_app_coily.tc01_walk_in_session_no_tune import WalkInSessionNoTune
from testsuite_tune_app_coily.tc02_walk_in_session_installing_tune import WalkInSessionInstallingTune
from testsuite_tune_app_coily.tc03_walk_in_session import WalkInSession
from testsuite_tune_app_coily.tc04_booked_session import BookedSessions
from testsuite_tune_app_coily.tc05_booked_session_installing_tune import BookedSessionsNoTune
from testsuite_tune_app_coily.tc06_early_check_in_to_booked_session import EarlyCheckInToBookedSession
from testsuite_tune_app_coily.tc09_agenda_interactions import AgendaInteractionsDuringActiveSession
from testsuite_tune_app_coily.tc08_quit_and_re_launch_tune_during_active_session import QuitAndRelaunchTuneDuringActiveSession
from testsuite_tune_app_coily.tc07_coily_settings_in_tune import CoilySettingsInLogiTune


tc_to_run = [
    WalkInSessionNoTune,
    WalkInSessionInstallingTune,
    BookedSessionsNoTune,
    WalkInSession,
    BookedSessions,
    EarlyCheckInToBookedSession,
    AgendaInteractionsDuringActiveSession,
    QuitAndRelaunchTuneDuringActiveSession,
    CoilySettingsInLogiTune,
]
if __name__ == '__main__':
    run_tests(tc_to_run, retry=args.retry, mailing=args.email_notification, install_tune=True)
