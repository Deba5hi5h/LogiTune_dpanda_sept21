"""
IMPORTS NEED TO BE THIS WAY, AS UPDATING SETTINGS FILE
NEEDS TO BE DONE BEFORE IMPORTING IT TO ANY FILE
"""

import argparse
from common import config
from testsuite_tune_app.tc38a_calendar_and_meetings_google import CalendarAndMeetingsTestsGoogle
from testsuite_tune_app.tc38b_calendar_and_meetings_microsoft import CalendarAndMeetingsTestsMicrosoft

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-e", "--email_notification", help="send email notification", default=True,
                    type=lambda x: (str(x).lower() == 'true'))
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
settings.set_value_in_section('JENKINS_FWU_TESTS', 'JENKINS_FWU_CONFIG', 'True')

if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'LogiTune')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
settings.set_value_in_section('RUN_CONFIG', 'jira_update', 'True')

MAILING_LIST = (
    'ptokarczyk@logitech.com',
    'plesniak@logitech.com',
    'rdrozd@logitech.com',
)

from testsuite_tune_app.test_runner import run_tests
from testsuite_tune_app.verify_device_connection import check_devices

from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc01_webcam_brio import WebcamBrio
from testsuite_tune_app.tc06_webcam_streamcam import WebcamStreamCam
from testsuite_tune_app.tc34_webcam_brio_10X import WebcamBrio10X
from testsuite_tune_app.tc16_webcam_brio_30X import WebcamBrio30X
from testsuite_tune_app.tc08_webcam_brio_50X import WebcamBrio50X
from testsuite_tune_app.tc17_webcam_brio_70X import WebcamBrio70X
from testsuite_tune_app.tc10_headset_zone_750 import Zone750
from testsuite_tune_app.tc12_headset_zone_wireless_plus import ZoneWirelessPlus
from testsuite_tune_app.tc14_headset_zone_900 import Zone900
from testsuite_tune_app.tc24_headset_zone_vibe_wireless import ZoneVibeWireless
from testsuite_tune_app.tc36_headset_zone_950 import Zone950
from testsuite_tune_app.tc42_headset_bomberman_mono import BombermanMono
from testsuite_tune_app.tc43_headset_bomberman_stereo import BombermanStereo
from testsuite_tune_app.tc41_headset_zone_305 import Zone305
from testsuite_tune_app.tc18a_google_calendar import GoogleCalendarTests
from testsuite_tune_app.tc18b_microsoft_calendar import MicrosoftCalendarTests
from testsuite_tune_app.tc22_logi_dock import LogiDock
from testsuite_tune_app.tc25_litra_beam import LitraBeam
from testsuite_tune_app.tc20_uninstall import TuneUninstall
from testsuite_tune_app.tc27a_tune_app_update_between_branches import TuneAppUpdate
from testsuite_tune_app.tc40_appearance_settings import AppearanceTests
from testsuite_tune_app.tc99_logi_sync_personal_collab import LogiSyncPersonalCollab

tc_to_run = [
    TuneInstall,
    Zone950,
    WebcamBrio,
    WebcamStreamCam,
    WebcamBrio10X,
    WebcamBrio30X,
    WebcamBrio50X,
    WebcamBrio70X,
    Zone750,
    Zone900,
    Zone305,
    ZoneVibeWireless,
    ZoneWirelessPlus,
    BombermanMono,
    BombermanStereo,
    LogiDock,
    LitraBeam,
    AppearanceTests,
    GoogleCalendarTests,
    MicrosoftCalendarTests,
    CalendarAndMeetingsTestsGoogle,
    CalendarAndMeetingsTestsMicrosoft,
    # LogiSyncPersonalCollab,  # more tests needed before adding it
    TuneUninstall,
    TuneAppUpdate,
]


if __name__ == '__main__':
    tune_install = TuneInstall()
    tune_install.setUpClass()
    tune_install.test_001_VC_42593_install_logi_tune()
    check_devices(testcases_to_run=tc_to_run, mailing_list=MAILING_LIST,
                  skip_missing_devices_in_test_suite=True, is_svc_lab=False)
    run_tests(tc_to_run, retry=args.retry, mailing=args.email_notification)

