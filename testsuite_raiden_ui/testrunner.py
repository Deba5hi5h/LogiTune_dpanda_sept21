import unittest
import sys
import os
import inspect


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from common import config
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-qa, raiden-stable, "
                                                "raiden-latest1, raiden-qa1, raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenUi')

from base import global_variables
from testsuite_raiden_ui.tc01_sync_portal_sanity import SyncPortalSanity
from testsuite_raiden_ui.tc02_sync_portal_rally_bar import SyncPortalRallyBar

tests_sanity= unittest.TestLoader().loadTestsFromTestCase(SyncPortalSanity)
tests_rallybar = unittest.TestLoader().loadTestsFromTestCase(SyncPortalRallyBar)

suite_Sanity = unittest.TestSuite(tests_sanity)
suite_RallyBar = unittest.TestSuite(tests_rallybar)

if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
global_variables.test_category = 'Sanity'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_Sanity)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RallyBar)

