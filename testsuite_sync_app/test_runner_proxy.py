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
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')
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

from testsuite_sync_app.tc00_install import Install
from testsuite_sync_app.tc01_meetup import Meetup
from testsuite_sync_app.tc02_rally import Rally
from testsuite_sync_app.tc03_rallycamera import RallyCamera
from testsuite_sync_app.tc04_kong import Kong
from testsuite_sync_app.tc05_diddy import Diddy
from testsuite_sync_app.tc06_brio import Brio
from testsuite_sync_app.tc07_celestia import Celestia
from testsuite_sync_app.tc25_uninstall import Uninstall
from testsuite_sync_app.tc26_first_run_experience import FRE

# Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)

# Setup Suite
suite_Install = unittest.TestSuite(tests_Install)  # All test cases
suite_Meetup = unittest.TestSuite()  # Selected test cases
suite_Rally = unittest.TestSuite()
suite_RallyCamera = unittest.TestSuite()
suite_Kong = unittest.TestSuite()
suite_Diddy = unittest.TestSuite()
suite_Brio = unittest.TestSuite()
suite_Tap = unittest.TestSuite()
suite_Swytch = unittest.TestSuite()
suite_Celestia = unittest.TestSuite()
suite_Uninstall = unittest.TestSuite()
suite_FRE = unittest.TestSuite()

# Add Sanity test cases to suite
suite_Meetup.addTests([Meetup('test_101_VC_39972_meetup_add_device'),
                       Meetup('test_103_VC_40063_meetup_video_tab'),
                       Meetup('test_105_VC_40092_interrupt_firmware_update'),
                       Meetup('test_106_VC_39978_update_firmware'),
                       Meetup('test_108_VC_40060_meetup_audio_tab'),
                       Meetup('test_117_VC_39987_meetup_forget_device'),
                       Meetup('test_118_VC_40084_meetup_add_device_pnp'),
                       Meetup('test_119_VC_39996_meetup_forget_problem_device'),
                       Meetup('test_120_VC_44287_meetup_forget_problem_device_sync_portal')
                       ])
suite_Rally.addTests([Rally('test_201_VC_40085_rally_add_device_pnp'),
                      Rally('test_205_VC_39979_rally_update_firmware'),
                      Rally('test_215_VC_39988_rally_forget_device'),
                      Rally('test_216_VC_39973_rally_add_device'),
                      Rally('test_217_VC_39997_rally_forget_problem_device'),
                      Rally('test_218_VC_44292_rally_forget_problem_device_sync_portal')
                      ])
suite_RallyCamera.addTests([RallyCamera('test_301_VC_40086_rallycamera_add_device_pnp'),
                            RallyCamera('test_305_VC_39980_rallycamera_update_firmware'),
                            RallyCamera('test_315_VC_39989_rallycamera_forget_device'),
                            RallyCamera('test_316_VC_39974_rallycamera_add_device'),
                            RallyCamera('test_317_VC_39998_rallycamera_forget_problem_device'),
                            RallyCamera('test_318_VC_44293_rallycamera_forget_problem_device_sync_portal')
                            ])
suite_Kong.addTests([Kong('test_401_VC_39951_rallybar_add_device'),
                     Kong('test_402_VC_40066_rallybar_video_tab'),
                     Kong('test_405_VC_58626_rallybar_rightsight2'),
                     Kong('test_407_VC_66922_rallybar_speakerview'),
                     Kong('test_408_VC_66920_rallybar_groupview'),
                     Kong('test_412_VC_40029_rallybar_antiflicker_settings'),
                     Kong('test_413_VC_40031_rallybar_bluetooth_options'),
                     Kong('test_434_VC_39993_rallybar_forget_problem_device')
                     ])
suite_Diddy.addTests([Diddy('test_501_VC_39952_rallybarmini_add_device'),
                      Diddy('test_504_VC_40020_rallybarmini_rightsight_options'),
                      Diddy('test_505_VC_58628_rallybarmini_rightsight2'),
                      Diddy('test_507_VC_66926_rallybarmini_speakerview'),
                      Diddy('test_508_VC_66924_rallybarmini_groupview'),
                      Diddy('test_512_VC_40030_rallybarmini_antiflicker_settings'),
                      Diddy('test_513_VC_40032_rallybarmini_bluetooth_options'),
                      Diddy('test_532_VC_39958_rallybarmini_forget_device')
                      ])
suite_Celestia.addTests([Celestia('test_701_VC_39953_celestia_add_device'),
                         Celestia('test_705_VC_39959_celestia_forget_device')])
suite_Uninstall.addTests([Uninstall('test_251_VC_39960_disconnect_from_sync_app'),
                          Uninstall('test_252_VC_40002_disconnect_from_sync_portal'),
                          Uninstall('test_258_VC_39961_uninstall_sync_app')
                          ])

# Run Suite
global_variables.email_flag=True
EmailNotification.send_job_email()
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_Install)
unittest.TextTestRunner().run(suite_Meetup)
unittest.TextTestRunner().run(suite_Rally)
unittest.TextTestRunner().run(suite_RallyCamera)
unittest.TextTestRunner().run(suite_Kong)
unittest.TextTestRunner().run(suite_Diddy)
unittest.TextTestRunner().run(suite_Celestia)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Uninstall)
Proxy.reset_proxy()
