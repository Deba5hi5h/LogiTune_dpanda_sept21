import time
import unittest

from common import config
# Command Line arguments
import argparse
from apps.tune_mobile.config import tune_mobile_config

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--retry", help="retry count")
parser.add_argument("-e", "--environment", help="iPhone version or Android")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'TuneMobile')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
tune_mobile_config.phone = "S22"

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_tune_mobile.tc01_headset_functionality import HeadsetFunctionality


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
if args.retry is not None:
    global_variables.retry_count = args.retry

# global_variables.email_flag = True
# EmailNotification.send_job_email()

headsets = ["Zone True Wireless",
            "Zone Vibe 130",
            "Zone Vibe 100",
            "Zone Vibe Wireless",
            "Zone Wireless 2",
            "Zone Wireless Plus"]

global_variables.test_category = "Headset"
global_variables.teardownFlag = False
count = 0
for headset in headsets:
    count += 1
    if count == len(headsets):
        global_variables.teardownFlag = True
    HeadsetFunctionality.bluetooth = False
    HeadsetFunctionality.headset = headset
    suite = unittest.TestSuite(tests_functional)
    unittest.TextTestRunner().run(suite)
    time.sleep(2)