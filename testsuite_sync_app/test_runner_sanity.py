import unittest

from common import config
#Command Line arguments
import argparse

from common.email_notification import EmailNotification

parser = argparse.ArgumentParser()
parser.add_argument("-n","--installer", help="installer version")
args = parser.parse_args()

#Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')

from base import global_variables
from testsuite_sync_app.tc00_install import Install
from testsuite_sync_app.tc01_meetup import Meetup
from testsuite_sync_app.tc02_rally import Rally
from testsuite_sync_app.tc03_rallycamera import RallyCamera
from testsuite_sync_app.tc04_kong import Kong
from testsuite_sync_app.tc05_diddy import Diddy
from testsuite_sync_app.tc06_brio import Brio
from testsuite_sync_app.tc07_celestia import Celestia
from testsuite_sync_app.tc08_tap import Tap
from testsuite_sync_app.tc09_swytch import Swytch
from testsuite_sync_app.tc25_uninstall import Uninstall
from testsuite_sync_app.tc26_first_run_experience import FRE

#Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)

#Setup Suite
suite_Install = unittest.TestSuite(tests_Install) #All test cases
suite_Meetup = unittest.TestSuite() #Selected test cases
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

#Add Sanity test cases to suite
suite_Meetup.addTests([Meetup('test_101_VC_39972_meetup_add_device'),
                       Meetup('test_103_VC_40063_meetup_video_tab'),
                       Meetup('test_104_VC_40015_meet_up_rightsight_in_sync'),
                       Meetup('test_108_VC_40060_meetup_audio_tab'),
                       Meetup('test_110_VC_39987_meetup_forget_device')
                       ])
suite_Rally.addTests([Rally('test_201_VC_40085_rally_add_device_pnp'),
                      Rally('test_204_VC_40016_rally_rightsight_options'),
                      Rally('test_206_VC_40061_rally_audio_tab'),
                      Rally('test_208_VC_39988_rally_forget_device'),
                      Rally('test_209_VC_39973_rally_add_device'),
                      Rally('test_210_VC_39997_rally_forget_problem_device')
                      ])
suite_RallyCamera.addTests([RallyCamera('test_301_VC_40086_rally_camera_add_device_pnp'),
                            RallyCamera('test_302_VC_40065_rallycamera_video_tab'),
                            RallyCamera('test_304_VC_40017_rallycamera_rightsight_options'),
                            RallyCamera('test_308_VC_39989_rallycamera_forget_device'),
                            RallyCamera('test_309_VC_39974_rallycamera_add_device'),
                            RallyCamera('test_310_VC_39998_rally_camera_forget_problem_device')
                            ])
suite_Kong.addTests([Kong('test_401_VC_39951_kong_add_device'),
                     Kong('test_402_VC_40066_kong_video_tab'),
                     Kong('test_404_VC_40019_kong_rightsight_options'),
                     Kong('test_405_VC_58626_kong_rightsight2'),
                     Kong('test_407_VC_66922_kong_speakerview'),
                     Kong('test_408_VC_66920_kong_groupview'),
                     Kong('test_412_VC_40029_kong_antiflicker_settings'),
                     Kong('test_427_VC_39993_kong_forget_problem_device')
                     ])
suite_Diddy.addTests([Diddy('test_501_VC_39952_diddy_add_device'),
                      Diddy('test_504_VC_40020_diddy_rightsight_options'),
                      Diddy('test_505_VC_58628_diddy_rightsight2'),
                      Diddy('test_507_VC_66926_diddy_speakerview'),
                      Diddy('test_508_VC_66924_diddy_groupview'),
                      Diddy('test_510_VC_40062_diddy_audio_tab'),
                      Diddy('test_511_VC_40067_diddy_video_tab'),
                      Diddy('test_512_VC_40030_diddy_antiflicker_settings'),
                      Diddy('test_513_VC_40032_diddy_bluetooth_options'),
                      Diddy('test_525_VC_39958_diddy_forget_device')
                      ])
suite_Celestia.addTests([Celestia('test_701_VC_39953_celestia_add_device'),
                         Celestia('test_704_VC_40053_celestia_video_tab'),
                         Celestia('test_705_VC_39959_celestia_forget_device')])
suite_Uninstall.addTests([Uninstall('test_251_VC_39960_disconnect_from_sync_app'),
                          Uninstall('test_252_VC_40002_disconnect_from_sync_portal'),
                          Uninstall('test_258_VC_39961_uninstall_sync_app')
                          ])

#Run Suite
global_variables.email_flag=True
global_variables.email_to="sveerbhadrappa@logitech.com,azuger@logitech.com,eestrada@logitech.com,sboruthalupula@logitech.com"
EmailNotification.send_job_email()
global_variables.test_category = 'Sanity'
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
