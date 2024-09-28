import time
import unittest

from common import config
# Command Line arguments
import argparse
from apps.tune_mobile.config import tune_mobile_config

parser = argparse.ArgumentParser()
parser.add_argument("-qv", "--qa_version", help="QA version of App to be tested")
parser.add_argument("-up", "--user_phone", help="User phone for running tests")
args = parser.parse_args()

# Run Configuration
tune_mobile_config.phone = "iPhone12"
qa_version = '3.15.0-4'
settings = config.CommonConfig.get_instance()
if args.qa_version is not None:
    qa_version = args.qa_version
if args.user_phone is not None:
    tune_mobile_config.phone = args.user_phone

settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', qa_version)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'TuneMobile')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_tune_mobile.tc01_headset_functionality import HeadsetFunctionality
from apps.tune_mobile.tune_mobile_utils import TuneMobileUtils

# Load Tests
tests_functional = unittest.TestLoader().loadTestsFromTestCase(HeadsetFunctionality)

# Setup Suite
suite_zone_wireless_plus = unittest.TestSuite(tests_functional)
suite_zone_vibe_130 = unittest.TestSuite(tests_functional)
suite_zone_vibe_100 = unittest.TestSuite(tests_functional)
suite_zone_vibe_wireless = unittest.TestSuite(tests_functional)
suite_zone_true_wireless = unittest.TestSuite(tests_functional)
suite_zone_wireless2 = unittest.TestSuite(tests_functional)

# Run Suite
# global_variables.email_flag = True
# EmailNotification.send_job_email()

headsets = ["Zone Wireless Plus"]
global_variables.update_test_automation_field = True
global_variables.retry_count = 1
global_variables.test_category = "Headset-Sanity"
global_variables.teardownFlag = False
count = 0
TuneMobileUtils.start_appium()
for headset in headsets:
    count += 1
    if count == len(headsets):
        global_variables.teardownFlag = True
    HeadsetFunctionality.bluetooth = False
    HeadsetFunctionality.headset = headset
    suite = unittest.TestSuite(tests_functional)
    unittest.TextTestRunner().run(suite)
    time.sleep(2)
TuneMobileUtils.stop_appium()