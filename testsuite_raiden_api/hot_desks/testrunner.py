import unittest
from testsuite_raiden_api.hot_desks.raiden_api_hot_desks import RaidenAPIHotDesks

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

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

test_RaidenAPIHotDesks = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHotDesks)

suite_RaidenAPIHotDesks = unittest.TestSuite(test_RaidenAPIHotDesks)

unittest.TextTestRunner().run(suite_RaidenAPIHotDesks)

