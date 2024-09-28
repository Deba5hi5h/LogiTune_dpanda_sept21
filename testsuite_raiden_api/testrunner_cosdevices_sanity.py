import unittest
import sys
import argparse
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
                                                "raiden-latest1, raiden-qa1, raiden-prodca, raiden-prodca, "
                                                "raiden-prodfr")
args = parser.parse_args()

settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
if args.environment is not None:
    global_variables.SYNC_ENV = args.environment
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'RaidenApi')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

from testsuite_raiden_api.raiden_api_cos_devices_meeting_room_setup import RaidenAPICOSDevicesSetup
from testsuite_raiden_api.raiden_api_session import RaidenAPISession
from testsuite_raiden_api.users.raiden_api_users import RaidenAPIUser
from testsuite_raiden_api.meeting_rooms.provisioning.raiden_api_provisioning import RaidenAPIProvisioning
from testsuite_raiden_api.meeting_rooms.rooms.raiden_api_empty_rooms import RaidenAPIEmptyRooms
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybar import RaidenAPIHostedRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_hosted_rallybarmini import RaidenAPIHostedRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybar import RaidenAPIRallyBar
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_rallybarmini import RaidenAPIRallyBarMini
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_roomMate import RaidenAPIRoomMate
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapip import RaidenAPITapIP
from testsuite_raiden_api.meeting_rooms.devices.raiden_api_tapscheduler import RaidenAPITapScheduler
from testsuite_raiden_api.raiden_api_meeting_rooms_teardown import RaidenAPIMeetingRoomTearDown

tests_RaidenAPICOSDevicesSetup = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICOSDevicesSetup)
tests_RaidenAPIUser = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIUser)
tests_RaidenAPIProvisioning = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIProvisioning)
tests_RaidenAPIEmptyRooms = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIEmptyRooms)
tests_RaidenAPIMeetingRoomTearDown = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIMeetingRoomTearDown)

suite_RaidenAPICOSDevicesSetup = unittest.TestSuite(tests_RaidenAPICOSDevicesSetup)
suite_RaidenAPIUser = unittest.TestSuite(tests_RaidenAPIUser)
suite_RaidenAPIProvisioning = unittest.TestSuite(tests_RaidenAPIProvisioning)
suite_RaidenAPIEmptyRooms = unittest.TestSuite(tests_RaidenAPIEmptyRooms)
suite_RaidenAPISession = unittest.TestSuite()
suite_RaidenAPIHostedRallyBar = unittest.TestSuite()
suite_RaidenAPIHostedRallyBarMini = unittest.TestSuite()
suite_RaidenAPIRallyBar = unittest.TestSuite()
suite_RaidenAPIRallyBarMini = unittest.TestSuite()
suite_RaidenAPIRoomMate = unittest.TestSuite()
suite_RaidenAPITapIP = unittest.TestSuite()
suite_RaidenAPITapScheduler = unittest.TestSuite()
suite_RaidenAPIMeetingRoomTearDown = unittest.TestSuite(tests_RaidenAPIMeetingRoomTearDown)


suite_RaidenAPISession.addTests([RaidenAPISession('test_101_VC_12849_Get_Raiden_Backend_Version'),
                                 RaidenAPISession('test_102_VC_16601_Sign_In_Owner')])

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
suite_RaidenAPIHostedRallyBarMini.addTests([RaidenAPIHostedRallyBarMini('test_1401_VC_102262_Get_Device_RallyBarMini_'
                                                                        'in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1403_VC_102264_Set_RS2_SpeakerView_'
                                                                        'Framing_Speed_To_Slower_Speaker_Detection_To_'
                                                                        'Slower_RallyBarMini_in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1404_VC_102266_Set_RS2_GroupView_Framing_'
                                                                        'Speed_To_Default_RallyBarMini_in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1405_VC_102267_Disable_AI_Noise_'
                                                                        'Suppression_RallyBarMini_in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1406_VC_102268_Enable_AI_Noise_'
                                                                        'Suppression_RallyBarMini_in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1415_VC_102466_Speaker_EQ_Bass_Boost_'
                                                                        'RallyBarMini_in_Device_mode'),
                                            RaidenAPIHostedRallyBarMini('test_1416_VC_102467_Speaker_EQ_Normal_'
                                                                        'RallyBarMini_in_Device_mode')
                                            ])
suite_RaidenAPIRallyBar.addTests([RaidenAPIRallyBar('test_1501_Provision_Rally_Bar_to_Sync_Portal'),
                                  RaidenAPIRallyBar('test_1502_VC_53873_Get_Device_RallyBar'),
                                  RaidenAPIRallyBar('test_1504_VC_53876_Change_RightSight_Turn_Off_RallyBar'),
                                  RaidenAPIRallyBar('test_1506_VC_60999_Change_RS2_Speaker_tracking_mode_Speaker_View_'
                                                    'Picture_in_picture_disabled_RallyBar'),
                                  RaidenAPIRallyBar('test_1507_VC_53878_Change_RightSight_Group_view_set_to_Dynamic_'
                                                    'RallyBar'),
                                  RaidenAPIRallyBar('test_1510_VC_53881_Enable_Speaker_Boost_RallyBar'),
                                  RaidenAPIRallyBar('test_1511_VC_53896_Disable_Speaker_Boost_RallyBar'),
                                  RaidenAPIRallyBar('test_1513_VC_53883_Enable_Reverb_Control_Aggressive_RallyBar'),
                                  RaidenAPIRallyBar('test_1514_VC_53885_Enable_Reverb_Control_Normal_RallyBar'),
                                  RaidenAPIRallyBar('test_1515_VC_53886_Turn_Off_Bluetooth_RallyBar'),
                                  RaidenAPIRallyBar('test_1516_VC_53887_Turn_On_Bluetooth_RallyBar'),
                                  RaidenAPIRallyBar('test_1517_VC_69046_Microphone_EQ_Bass_Boost_RallyBar'),
                                  RaidenAPIRallyBar('test_1518_VC_69047_Microphone_EQ_Voice_Boost_RallyBar'),
                                  RaidenAPIRallyBar('test_1535_VC_69065_Change_Password_Local_Network_Access_RallyBar'),
                                  RaidenAPIRallyBar('test_1547_Delete_Room')
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
suite_RaidenAPIRoomMate.addTests([RaidenAPIRoomMate('test_1701_Provision_RoomMate_to_sync_portal'),
                                  RaidenAPIRoomMate('test_1702_VC_102444_Get_Device_RoomMate'),
                                  RaidenAPIRoomMate('test_1704_VC_79951_Disable_Local_Network_Access_RoomMate'),
                                  RaidenAPIRoomMate('test_1705_VC_79950_Enable_Local_Network_Access_RoomMate'),
                                  RaidenAPIRoomMate('test_1706_VC_79952_Change_Password_Local_Network_Access_RoomMate'),
                                  RaidenAPIRoomMate('test_1707_Delete_Room')
                                  ])
suite_RaidenAPITapIP.addTests([RaidenAPITapIP('test_1801_Provision_TapIP_to_sync_portal'),
                               RaidenAPITapIP('test_1802_VC_102445_Get_Device_TapIP'),
                               RaidenAPITapIP('test_1804_VC_79955_Disable_Local_Network_Access_TapIP'),
                               RaidenAPITapIP('test_1805_VC_79954_Enable_Local_Network_Access_TapIP'),
                               RaidenAPITapIP('test_1808_Delete_Room')
                               ])
suite_RaidenAPITapScheduler.addTests([RaidenAPITapScheduler('test_1901_Provision_Tap_Scheduler_to_sync_portal'),
                                      RaidenAPITapScheduler('test_1902_VC_102446_Get_Device_TapScheduler'),
                                      RaidenAPITapScheduler('test_1905_VC_79961_Change_Password_Local_Network_Access_'
                                                            'TapScheduler'),
                                      RaidenAPITapScheduler('test_1906_VC_79958_Reboot_Device_TapScheduler'),
                                      RaidenAPITapScheduler('test_1908_Delete_Room')
                                      ])

global_variables.test_category = 'CollabOS-Compatibility'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_RaidenAPICOSDevicesSetup)
unittest.TextTestRunner().run(suite_RaidenAPISession)
unittest.TextTestRunner().run(suite_RaidenAPIUser)
unittest.TextTestRunner().run(suite_RaidenAPIProvisioning)
unittest.TextTestRunner().run(suite_RaidenAPIEmptyRooms)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIHostedRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBar)
unittest.TextTestRunner().run(suite_RaidenAPIRallyBarMini)
unittest.TextTestRunner().run(suite_RaidenAPIRoomMate)
unittest.TextTestRunner().run(suite_RaidenAPITapIP)
unittest.TextTestRunner().run(suite_RaidenAPITapScheduler)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_RaidenAPIMeetingRoomTearDown)
