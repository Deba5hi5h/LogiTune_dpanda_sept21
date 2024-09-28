import unittest

from common import config
# Command Line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p1", "--prod1", help="Prod installer version1")
parser.add_argument("-p2", "--prod2", help="Prod installer version2")
parser.add_argument("-c", "--current", help="Current installer version1")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.prod1 is not None:
    settings.set_value_in_section('RUN_CONFIG', 'SYNC_PROD_VERSION1', args.prod1)
if args.prod2 is not None:
    settings.set_value_in_section('RUN_CONFIG', 'SYNC_PROD_VERSION2', args.prod2)
if args.current is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.current)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_sync_app.tc27_sync_update import SyncUpdate
from testsuite_sync_app.tc27_update import SyncUpdateThirdParty

# Load Tests
tests_SyncUpdate = unittest.TestLoader().loadTestsFromTestCase(SyncUpdate)
tests_SyncUpdateThirdParty = unittest.TestLoader().loadTestsFromTestCase(SyncUpdateThirdParty)

# Setup Suite
suite_SyncUpdate = unittest.TestSuite(tests_SyncUpdate)  # All test cases
suite_SyncUpdateThirdParty = unittest.TestSuite(tests_SyncUpdateThirdParty)  # All test cases

# Run Suite
global_variables.test_category = 'SW Update'
global_variables.email_flag = True
EmailNotification.send_job_email()
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_SyncUpdate)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_SyncUpdateThirdParty)