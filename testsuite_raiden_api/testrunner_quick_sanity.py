import unittest
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from common import config
from base import global_variables
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-latest, raiden-staging, "
                                                "raiden-qa, raiden-stable, raiden-latest1, raiden-qa1, raiden-prodca, "
                                                "raiden-prodca, raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_sysadmin import RaidenAPISystemAdmin
from testsuite_raiden_api.users.raiden_api_owner import RaidenAPIOwner
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms

tests_RaidenAPISession = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISession)
tests_RaidenAPISystemAdmin = unittest.TestLoader().loadTestsFromTestCase(RaidenAPISystemAdmin)
tests_RaidenAPIOwner = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIOwner)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)

suite_RaidenAPISession = unittest.TestSuite(tests_RaidenAPISession)
suite_RaidenAPISystemAdmin = unittest.TestSuite(tests_RaidenAPISystemAdmin)
suite_RaidenAPIOwner = unittest.TestSuite(tests_RaidenAPIOwner)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)

global_variables.test_category = 'Quick-Sanity'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPISystemAdmin)
unittest.TextTestRunner().run(suite_RaidenAPIOwner)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
