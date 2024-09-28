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
# settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'TuneMobile')
# settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
tune_mobile_config.phone = "iPhone12"

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_tune_mobile.tc00_localization import Localization


# Load Tests
tests_localization = unittest.TestLoader().loadTestsFromTestCase(Localization)

# Setup Suite
suite_zone_wireless_plus = unittest.TestSuite(tests_localization)
suite_zone_vibe_130 = unittest.TestSuite(tests_localization)
suite_zone_vibe_100 = unittest.TestSuite(tests_localization)
suite_zone_vibe_wireless = unittest.TestSuite(tests_localization)
suite_zone_true_wireless = unittest.TestSuite(tests_localization)
suite_zone_wireless2 = unittest.TestSuite(tests_localization)

# Run Suite
if args.retry is not None:
    global_variables.retry_count = args.retry

# global_variables.email_flag = False
# EmailNotification.send_job_email()
global_variables.test_category = "Localization"
# global_variables.teardownFlag = False
#
# Localization.headset = "Zone True Wireless"
# unittest.TextTestRunner().run(suite_zone_true_wireless)
#
# Localization.headset = "Zone Vibe 130"
# unittest.TextTestRunner().run(suite_zone_vibe_130)
#
# Localization.headset = "Zone Vibe 100"
# unittest.TextTestRunner().run(suite_zone_vibe_100)
#
# Localization.headset = "Zone Vibe Wireless"
# unittest.TextTestRunner().run(suite_zone_vibe_wireless)
#
Localization.headset = "Zone Wireless 2"
unittest.TextTestRunner().run(suite_zone_wireless2)

# global_variables.teardownFlag = True
#
# Localization.headset = "Zone Wireless Plus"
# unittest.TextTestRunner().run(suite_zone_wireless_plus)
