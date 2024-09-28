import unittest
import sys
import argparse
import os
import inspect
import importlib

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from base import global_variables
from common import config
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-qa, raiden-stable, "
                                                "raiden-latest1, raiden-qa1, raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
parser.add_argument("-k", "--ipkongdevicemode", help="IP of Kong in device mode")
parser.add_argument("-d", "--ipdiddyhostmode", help="IP of Diddy in host mode")
parser.add_argument("-f", "--firmware", help="FW Update channel: futen-prod-qa, futen-prod-q3, futen-prod-untested")
args = parser.parse_args()

settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
if args.ipkongdevicemode is not None:
    settings.set_value_in_section('DEVICE_IP', 'hostedkong_ip', args.ipkongdevicemode)
if args.ipdiddyhostmode is not None:
    settings.set_value_in_section('DEVICE_IP', 'diddy_ip', args.ipdiddyhostmode)
if args.firmware is not None:
    global_variables.SYNC_FWOTA = args.firmware
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from common import framework_params
importlib.reload(framework_params)

from testsuite_raiden_api.raiden_api_collabos_compatibility_setup import RaidenAPICollabOSCompatibilitySetup
from testsuite_raiden_api.meeting_rooms.firmware_update.raiden_api_hosted_rallybar_fwupdate import RaidenAPIHostedRallyBarFWUpdate
from testsuite_raiden_api.meeting_rooms.firmware_update.raiden_api_rallybarmini_fwupdate import RaidenAPIRallyBarMiniFWUpdate
from testsuite_raiden_api.raiden_api_collabos_compatibility_teardown import RaidenAPICollabOSCompatibilityTearDown

tests_RaidenAPICollabOSCompatibilitySetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICollabOSCompatibilitySetup)
tests_RaidenAPIHostedRallyBarFWUpdate = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIHostedRallyBarFWUpdate)
tests_RaidenAPIRallyBarMiniFWUpdate = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIRallyBarMiniFWUpdate)
tests_RaidenAPICollabOSCompatibilityTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICollabOSCompatibilityTearDown)

suite_RaidenAPICollabOSCompatibilitySetup = unittest.TestSuite(tests_RaidenAPICollabOSCompatibilitySetup)
suite_RaidenAPIHostedRallyBarFWUpdate = unittest.TestSuite(tests_RaidenAPIHostedRallyBarFWUpdate)
suite_RaidenAPIRallyBarMiniFWUpdate = unittest.TestSuite(tests_RaidenAPIRallyBarMiniFWUpdate)
suite_RaidenAPICollabOSCompatibilityTearDown = unittest.TestSuite(tests_RaidenAPICollabOSCompatibilityTearDown)

global_variables.test_category = 'CollabOS-FWUpdate'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPICollabOSCompatibilitySetup)
# Kong in device mode
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarFWUpdate)
# Diddy in host mode
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMiniFWUpdate)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPICollabOSCompatibilityTearDown)