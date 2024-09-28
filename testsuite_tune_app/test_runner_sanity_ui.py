import argparse
import random
import re
import unittest
from common import config
from testsuite_tune_app.tc09_headset_zone_wired import ZoneWired
from testsuite_tune_app.tc25_litra_beam import LitraBeam
from testsuite_tune_app.tc41_headset_zone_305 import Zone305
from testsuite_tune_app.tc42_headset_bomberman_mono import BombermanMono
from testsuite_tune_app.tc43_headset_bomberman_stereo import BombermanStereo

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer",
                    help="installer version, or use i.e. 3.6.x to run it on the latest one")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-e", "--email_notification", help="send email notification", default=True,
                    type=lambda x: (str(x).lower() == 'true'))

args = parser.parse_args()
settings = config.CommonConfig.get_instance()
settings.set_value_in_section('JENKINS_FWU_TESTS', 'JENKINS_FWU_CONFIG', 'True')

if args.installer is not None and '.x' not in args.installer:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
else:
    from common.aws_s3_utils import AwsS3Utils
    aws = AwsS3Utils()
    installer = aws.get_newest_version_tune_desktop_version_for_project(project_version=args.installer)
    print(f'The latest build in {args.installer} release is: {installer}')
    if installer:
        settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', installer)
    else:
        raise Exception(f"No matching version of Tune app found in the release: {args.installer}")

settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'LogiTune')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
settings.set_value_in_section('RUN_CONFIG', 'jira_update', 'True')

# Test Suites imports
from base import global_variables
from common.JiraLibrary import JiraAPI
from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc01_webcam_brio import WebcamBrio
from testsuite_tune_app.tc08_webcam_brio_50X import WebcamBrio50X
from testsuite_tune_app.tc17_webcam_brio_70X import WebcamBrio70X
from testsuite_tune_app.tc12_headset_zone_wireless_plus import ZoneWirelessPlus
from testsuite_tune_app.tc13_headset_zone_wireless import ZoneWireless
from testsuite_tune_app.tc14_headset_zone_900 import Zone900
from testsuite_tune_app.tc18a_google_calendar import GoogleCalendarTests
from testsuite_tune_app.tc18b_microsoft_calendar import MicrosoftCalendarTests
from testsuite_tune_app.tc22_logi_dock import LogiDock
from testsuite_tune_app_coily.tc03_walk_in_session import WalkInSession
from testsuite_tune_app_coily.tc04_booked_session import BookedSessions
from testsuite_tune_app.tc20_uninstall import TuneUninstall
from testsuite_tune_app.test_runner import run_sanity_tests
from testsuite_tune_app.verify_device_connection import check_devices


MAILING_LIST = (
    'ptokarczyk@logitech.com',
    'plesniak@logitech.com',
    'rdrozd@logitech.com',
    'sveerbhadrappa@logitech.com',
    'bchandrashekar@logitech.com',
)


class TestManager:

    def get_testcases_to_run(self):
        webcams = [WebcamBrio, WebcamBrio50X, WebcamBrio70X]
        headsets = [ZoneWirelessPlus, Zone900, ZoneWireless, Zone305]
        wired_headsets = [BombermanMono, BombermanStereo, ZoneWired]
        other_devices = [LogiDock, LitraBeam]

        coily_1 = (WalkInSession, ['test_3003_VC_112862_walk_in_session_enabled_google_user_logged_in']), (BookedSessions, ['test_4004_VC_112875_booked_microsoft_session_and_microsoft_user_logged_in'])

        coily_2 = (WalkInSession, ['test_3004_VC_112863_walk_in_session_enabled_microsoft_user_logged_in']), (BookedSessions, ['test_4003_VC_112874_booked_google_session_and_google_user_logged_in'])

        from common.platform_helper import get_custom_platform
        coily = coily_1 if get_custom_platform() == "windows" else coily_2

        testcases_to_run = [TuneInstall, random.choice(webcams), random.choice(headsets),
                            random.choice(wired_headsets),
                            random.choice(other_devices),
                            (GoogleCalendarTests, ['test_18001_VC_116107_connect_to_google_calendar',
                                                   'test_18002_VC_116108_verify_event_presence_google',
                                                   'test_18003_VC_116109_verify_event_absence_google',
                                                   'test_18004_VC_116110_tc_verify_event_join_google']),
                            (MicrosoftCalendarTests, ['test_18101_VC_130670_connect_to_microsoft_calendar',
                                                      'test_18102_VC_130671_verify_event_presence_microsoft',
                                                      'test_18103_VC_130672_verify_event_absence_microsoft',
                                                      'test_18104_VC_130673_tc_verify_event_join_microsoft']),
                            coily[0], coily[1],
                            TuneUninstall]

        return testcases_to_run

    def load_tests_from_item(self, item):
        if isinstance(item, tuple):  # If item is tuple (testcase class with specific methods)
            test_case_class, test_methods = item
            tests = [unittest.TestLoader().loadTestsFromName(method, test_case_class) for method in test_methods]
        else:  # If item is just a testcase class
            tests = unittest.TestLoader().loadTestsFromTestCase(item)

        return tests

    def extract_jira_numbers(self, tests_to_run):
        jira_numbers = []
        pattern = re.compile(r"(VC_\d+)")

        for test in tests_to_run:
            if isinstance(test, str):
                matches = pattern.findall(test)
                matches = [match.replace('_', '-') for match in matches]
                jira_numbers.extend(matches)
            elif isinstance(test, list):
                jira_numbers.extend(self.extract_jira_numbers(test))
            else:
                test_str = str(test)
                matches = pattern.findall(test_str)
                matches = [match.replace('_', '-') for match in matches]
                jira_numbers.extend(matches)

        return jira_numbers

    def run(self):
        global_variables.test_category = f'Sanity tests'
        testcases_to_run = self.get_testcases_to_run()

        tests_to_run = []
        for item in testcases_to_run:
            tests = self.load_tests_from_item(item)
            tests_to_run.append(tests)

        zephyr_tests_list = self.extract_jira_numbers(tests_to_run)

        jira = JiraAPI()
        installer_version = settings.get_value_from_section('INSTALLER', 'RUN_CONFIG')
        print(f'Installer version: {installer_version}')
        jira.add_sanity_tests_to_cycle(project_version=installer_version, tests_to_add=zephyr_tests_list)

        check_devices(testcases_to_run=tests_to_run, mailing_list=MAILING_LIST,
                      skip_missing_devices_in_test_suite=True)

        run_sanity_tests(tests_to_run, retry=args.retry)


if __name__ == '__main__':
    tm = TestManager()
    tm.run()