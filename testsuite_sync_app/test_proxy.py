import unittest

from base import global_variables
from tests_sync.tc00_install import Install
from tests_sync.tc01_meetup import Meetup
from tests_sync.tc02_rally import Rally
from tests_sync.tc03_rallycamera import RallyCamera
from tests_sync.tc04_kong import Kong
from tests_sync.tc05_diddy import Diddy
from tests_sync.tc06_brio import Brio
from tests_sync.tc07_celestia import Celestia
from tests_sync.tc08_tap import Tap
from tests_sync.tc25_uninstall import Uninstall
from tests_sync.tc26_first_run_experience import FRE


#Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)
tests_Meetup = unittest.TestLoader().loadTestsFromTestCase(Meetup)
tests_Rally = unittest.TestLoader().loadTestsFromTestCase(Rally)
tests_RallyCamera = unittest.TestLoader().loadTestsFromTestCase(RallyCamera)
tests_Kong = unittest.TestLoader().loadTestsFromTestCase(Kong)
tests_Diddy= unittest.TestLoader().loadTestsFromTestCase(Diddy)
tests_Brio= unittest.TestLoader().loadTestsFromTestCase(Brio)
tests_Tap= unittest.TestLoader().loadTestsFromTestCase(Tap)
tests_Celestia= unittest.TestLoader().loadTestsFromTestCase(Celestia)
tests_Uninstall= unittest.TestLoader().loadTestsFromTestCase(Uninstall)
tests_FRE= unittest.TestLoader().loadTestsFromTestCase(FRE)

#Setup Suite
suite_Meetup = unittest.TestSuite(tests_Meetup)
suite_Meetup.addTests(['test_101_VC_39972_meetup_add_device'])
suite_Rally = unittest.TestSuite(tests_Rally)
suite_RallyCamera = unittest.TestSuite(tests_RallyCamera)
suite_Kong = unittest.TestSuite(tests_Kong)
suite_Diddy = unittest.TestSuite(tests_Diddy)
suite_Brio = unittest.TestSuite(tests_Brio)
suite_Tap = unittest.TestSuite(tests_Tap)
suite_Celestia = unittest.TestSuite(tests_Celestia)
suite_Uninstall = unittest.TestSuite(tests_Uninstall)
suite_FRE = unittest.TestSuite(tests_FRE)

#Run Suite
global_variables.teardownFlag = False
# unittest.TextTestRunner().run(suite_Install)
unittest.TextTestRunner().run(suite_Meetup)
# unittest.TextTestRunner().run(suite_Rally)
unittest.TextTestRunner().run(suite_RallyCamera)
# unittest.TextTestRunner().run(suite_Kong)
unittest.TextTestRunner().run(suite_Diddy)
unittest.TextTestRunner().run(suite_Brio)
unittest.TextTestRunner().run(suite_Tap)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Celestia)
# global_variables.teardownFlag = True
# unittest.TextTestRunner().run(suite_Uninstall)
global_variables.teardownFlag = True
# unittest.TextTestRunner().run(suite_FRE)

