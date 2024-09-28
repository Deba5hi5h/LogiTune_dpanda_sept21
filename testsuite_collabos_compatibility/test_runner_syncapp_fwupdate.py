import importlib
import unittest

from common import config
# Command Line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-d", "--device_list", help="list of device names separated by comma- Ex: Rally Bar,Rally Bar Mini")
parser.add_argument("-e", "--environment", help="Sync Portal Environment - raiden-prod, raiden-qa, raiden-stable")
parser.add_argument("-f", "--firmware", help="FW Update channel - futen-prod-qa, futen-prod-q3, futen-prod-untested")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from common import framework_params
importlib.reload(framework_params)

from common.usb_switch import connect_device, disconnect_device
from base import global_variables
from testsuite_sync_app.tc00_install import Install
from testsuite_collabos_compatibility.syncapp_collabos_fwupdate import SyncAppCollabOSFWUpdate
from testsuite_sync_app.tc25_uninstall import Uninstall

# Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)
tests_CollabOS = unittest.TestLoader().loadTestsFromTestCase(SyncAppCollabOSFWUpdate)

# Setup Suite
suite_Install = unittest.TestSuite()
suite_Install.addTests([Install('test_001_VC_39949_install_sync_app')
                        ])

suite_Uninstall = unittest.TestSuite()
suite_Uninstall.addTests([Uninstall('test_258_VC_39961_uninstall_sync_app')
                          ])

# Run Suite
global_variables.SYNC_FWOTA = args.firmware
global_variables.test_category = 'CollabOS-FWUpdate'
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_Install)
for device_name in args.device_list.split(','):
    connect_device(device_name)
for device in args.device_list.split(','):
    SyncAppCollabOSFWUpdate.device_name = device
    suite_CollabOS = unittest.TestSuite(tests_CollabOS)
    unittest.TextTestRunner().run(suite_CollabOS)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Uninstall)
