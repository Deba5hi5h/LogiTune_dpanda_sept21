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
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from common import framework_params
importlib.reload(framework_params)

from testsuite_raiden_api.raiden_api_collabos_compatibility_setup import RaidenAPICollabOSCompatibilitySetup
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybar import RaidenAPIHostedRallyBar
from testsuite_raiden_api.raiden_api_collabos_compatibility_teardown import RaidenAPICollabOSCompatibilityTearDown
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarmini import RaidenAPIRallyBarMini

tests_RaidenAPICollabOSCompatibilitySetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICollabOSCompatibilitySetup)
tests_RaidenAPICollabOSCompatibilityTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICollabOSCompatibilityTearDown)

suite_RaidenAPICollabOSCompatibilitySetup = unittest.TestSuite(tests_RaidenAPICollabOSCompatibilitySetup)
suite_RaidenAPIHostedRallyBar = unittest.TestSuite()
suite_RaidenAPIRallyBarMini = unittest.TestSuite()
suite_RaidenAPICollabOSCompatibilityTearDown = unittest.TestSuite(tests_RaidenAPICollabOSCompatibilityTearDown)

suite_RaidenAPIHostedRallyBar.addTests([RaidenAPIHostedRallyBar('test_1301_VC_102254_Get_Device_RallyBar_in_Device_'
                                                                'mode'),
                                        RaidenAPIHostedRallyBar('test_1302_VC_102255_Change_RightSight2_Turn_Off_'
                                                                'RallyBar_in_Device_mode'),
                                        RaidenAPIHostedRallyBar('test_1304_VC_102258_Set_RS2_GroupView_Framing_'
                                                                'Speed_To_Default_RallyBar_in_Device_mode'),
                                        RaidenAPIHostedRallyBar('test_1309_VC_102451_Disable_Reverb_Control_RallyBar_'
                                                                'in_Device_mode'),
                                        RaidenAPIHostedRallyBar('test_1310_VC_102452_Enable_Reverb_Control_Normal_'
                                                                'RallyBar_in_Device_mode'),
                                        RaidenAPIHostedRallyBar('test_1311_VC_102454_Turn_Off_Bluetooth_RallyBar_'
                                                                'in_Device_mode'),
                                        RaidenAPIHostedRallyBar('test_1312_VC_102455_Turn_On_Bluetooth_RallyBar_'
                                                                'in_Device_mode')
                                        ])

suite_RaidenAPIRallyBarMini.addTests([RaidenAPIRallyBarMini('test_1601_Provision_RallyBarMini_to_Sync_Portal'),
                                      RaidenAPIRallyBarMini('test_1602_VC_53889_Get_Device_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1630_VC_69082_Set_SpeakerView_Framing_Speed_To_'
                                                            'Slower_Speaker_Detection_To_Default_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1632_VC_69084_Disable_Enable_RightSight_Verify_'
                                                            'Group_View_Framing_Speed_Default_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1621_VC_69070_Speaker_EQ_Voice_Boost_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1622_VC_69071_Speaker_EQ_Normal_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1608_VC_53893_Disable_AI_Noise_Suppression_'
                                                            'RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1609_VC_53894_Enable_AI_Noise_Suppression_'
                                                            'RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1633_VC_69086_Disable_Local_Network_Access_'
                                                            'RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1634_VC_69085_Enable_Local_Network_Access_'
                                                            'RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1620_VC_69069_Speaker_EQ_Bass_Boost_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1622_VC_69071_Speaker_EQ_Normal_RallyBarMini'),
                                      RaidenAPIRallyBarMini('test_1646_Delete_Room')
                                      ])

global_variables.test_category = 'CollabOS-Compatibility'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPICollabOSCompatibilitySetup)
# Kong in device mode
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBar)
# Diddy in host mode
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMini)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPICollabOSCompatibilityTearDown)