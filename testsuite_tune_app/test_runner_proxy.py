import unittest
from base import global_variables
from common import config
# Command Line arguments
import argparse

from common.email_notification import EmailNotification
from common.proxy import Proxy

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-p", "--proxy", help="proxy - ip, pac_single_server or pac_multiple_server")
parser.add_argument("-c", "--channel", help="App Update Channel - dev, qa, dev2")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'LogiTune')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')
global_variables.ENABLE_PROXY = True
if str(args.proxy).upper() == 'IP':
    Proxy.set_proxy_ip()
    global_variables.test_category = 'Proxy IP'
elif str(args.proxy).upper() == 'PAC_SINGLE_SERVER':
    Proxy.set_proxy_pac_single_server()
    global_variables.PROXY_PAC = 'PAC_SINGLE_SERVER'
    global_variables.test_category = 'Proxy PAC Single Server'
elif str(args.proxy).upper() == 'PAC_MULTIPLE_SERVER':
    Proxy.set_proxy_pac_multiple_servers()
    global_variables.PROXY_PAC = 'PAC_MULTIPLE_SERVER'
    global_variables.test_category = 'Proxy PAC Multiple Servers'
else:
    print("Invalid argument for Proxy")
    raise Exception("Invalid Proxy")

from testsuite_tune_app.tc19_tune_proxy import TuneProxy

# Load Tests
tests_proxy = unittest.TestLoader().loadTestsFromTestCase(TuneProxy)

# Setup Suite
suite_Proxy = unittest.TestSuite(tests_proxy)  # All test cases

# Run Suite
if args.channel is not None:
    global_variables.TUNE_UPDATE_CHANNEL = args.channel
global_variables.email_flag = True
EmailNotification.send_job_email()
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Proxy)
Proxy.reset_proxy()
