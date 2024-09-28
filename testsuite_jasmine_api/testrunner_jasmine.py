import unittest
import argparse
import sys
import os
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

from base import global_variables
from common import config
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="Sync Installer version")
parser.add_argument("-e", "--environment", help="Sync Portal Environment: raiden-prod, raiden-qa, raiden-stable, "
                                                "raiden-latest1, raiden-qa1,raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'JasmineApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from testsuite_jasmine_api.meeting_rooms.jasmine_api_agenda import JasmineAgendaAPI
from testsuite_jasmine_api.meeting_rooms.jasmine_maps_api import JasmineMapsApi
from testsuite_jasmine_api.meeting_rooms.jasmine_room_booking_image_api import RoomBookingImageAPI

tests_JasmineAgendaAPI = unittest.TestLoader().loadTestsFromTestCase(JasmineAgendaAPI)
tests_JasmineMapsApi = unittest.TestLoader().loadTestsFromTestCase(JasmineMapsApi)
tests_RoomBookingImageAPI = unittest.TestLoader().loadTestsFromTestCase(RoomBookingImageAPI)

suite_JasmineAgendaAPI = unittest.TestSuite(tests_JasmineAgendaAPI)
suite_JasmineMapsApi = unittest.TestSuite(tests_JasmineMapsApi)
suite_RoomBookingImageAPI = unittest.TestSuite(tests_RoomBookingImageAPI)

raiden_envs = {"raiden-prod": "Raiden-Prod-Global", "raiden-prodeu": "Raiden-Prod-EU",
               "raiden-prodfr": "Raiden-Prod-France", "raiden-prodca": "Raiden-Prod-Canada",
               "raiden-latest1": "Raiden-Latest1", "raiden-qa1": "Raiden-QA1", "raiden-qa":"Raiden-QA",
               "raiden-stable1": "Raiden-Stable1"}
raiden_env_name = raiden_envs[global_variables.SYNC_ENV]
global_variables.test_category = f"{raiden_env_name}-Jasmine-Functional"
global_variables.email_flag = True
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_JasmineAgendaAPI)
unittest.TextTestRunner().run(suite_JasmineMapsApi)

global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RoomBookingImageAPI)