import unittest
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from common import config
from base import global_variables

# Run Configuration
settings = config.CommonConfig.get_instance()
settings.set_value_in_section("RUN_CONFIG", "PROJECT", "JasmineUi")
settings.set_value_in_section("RUN_CONFIG", "dashboard_publish", "True")

from testsuite_jasmine_ui.tc02_jasmine_bookings import JasmineBookings
from testsuite_jasmine_ui.tc04_jasmine_agenda import JasmineAgenda
from testsuite_jasmine_ui.tc_05_jasmine_floor_map import JasmineFloorMap
from testsuite_jasmine_ui.tc_06_jasmine_settings_pin import JasmineSettingsPin

tests_JasmineBookings = unittest.TestLoader().loadTestsFromTestCase(JasmineBookings)
tests_JasmineAgenda = unittest.TestLoader().loadTestsFromTestCase(JasmineAgenda)
tests_JasmineFloorMap = unittest.TestLoader().loadTestsFromTestCase(JasmineFloorMap)
tests_JasmineSettingsPin = unittest.TestLoader().loadTestsFromTestCase(JasmineSettingsPin)

suite_JasmineBookings = unittest.TestSuite(tests_JasmineBookings)
suite_JasmineAgenda = unittest.TestSuite(tests_JasmineAgenda)
suite_JasmineFloorMap = unittest.TestSuite(tests_JasmineFloorMap)
suite_JasmineSettingsPin = unittest.TestSuite(tests_JasmineSettingsPin)

global_variables.SYNC_ENV = "raiden-latest1"
raiden_envs = {
    "raiden-latest1": "Raiden-Latest1"
}
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"Jasmine-{raiden_env_name}"

global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_JasmineBookings)
unittest.TextTestRunner().run(suite_JasmineAgenda)
unittest.TextTestRunner().run(suite_JasmineFloorMap)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_JasmineSettingsPin)
