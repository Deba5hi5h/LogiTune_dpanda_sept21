import importlib
import unittest

from common import config
# Command Line arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-d", "--device_list", help="list of device names separated by comma- Ex: Rally Bar,Rally Bar Mini")
parser.add_argument("-e", "--environment", help="Sync Portal Environment - raiden-prod, raiden-qa, raiden-stable")
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
from testsuite_collabos_compatibility.syncapp_collabos import SyncAppCollabOS
from testsuite_sync_app.tc25_uninstall import Uninstall

# Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)
tests_CollabOS = unittest.TestLoader().loadTestsFromTestCase(SyncAppCollabOS)

# Setup Suite
suite_Install = unittest.TestSuite()
suite_Install.addTests([Install('test_001_VC_39949_install_sync_app'),
                        Install('test_002_VC_39971_connect_to_sync_portal')
                        ])

suite_Uninstall = unittest.TestSuite()
suite_Uninstall.addTests([Uninstall('test_251_VC_39960_disconnect_from_sync_app'),
                          Uninstall('test_258_VC_39961_uninstall_sync_app')
                          ])

# Run Suite
global_variables.retry_count = 1
global_variables.test_category = 'CollabOS-Compatibility'
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
global_variables.teardownFlag = False
for device_name in args.device_list.split(','):
    disconnect_device(device_name)
unittest.TextTestRunner().run(suite_Install)
for device in args.device_list.split(','):
    SyncAppCollabOS.device_name = device
    suite_CollabOS = unittest.TestSuite(tests_CollabOS)
    unittest.TextTestRunner().run(suite_CollabOS)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Uninstall)
for device_name in args.device_list.split(','):
    connect_device(device_name, report_result=False)
