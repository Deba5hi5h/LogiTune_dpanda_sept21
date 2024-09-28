from common import config

settings = config.CommonConfig.get_instance()

#KONG_FIRMWARE_TEST
IP_KONG_FIRMWARE_TEST = settings.get_value_from_section('IP_KONG_FIRMWARE_TEST', 'KONG_FIRMWARE_TEST')

#DIDDY_FIRMWARE_TEST
IP_DIDDY_FIRMWARE_TEST = settings.get_value_from_section('IP_DIDDY_FIRMWARE_TEST', 'DIDDY_FIRMWARE_TEST')

#Acroname Switch Serial Numbers Master/Slave
SWITCH_PORT_MASTER = int(settings.get_value_from_section('SWITCH_PORT_MASTER', 'SWITCH_PORT'), 16) #This is hex value
SWITCH_PORT_MASTER2 = int(settings.get_value_from_section('SWITCH_PORT_MASTER2', 'SWITCH_PORT'), 16) #This is hex value
SWITCH_PORT_MASTER3 = int(settings.get_value_from_section('SWITCH_PORT_MASTER3', 'SWITCH_PORT'), 16) #This is hex value
SWITCH_PORT_SLAVE1 = int(settings.get_value_from_section('SWITCH_PORT_SLAVE1', 'SWITCH_PORT'), 16) #This is hex value
SWITCH_PORT_SLAVE2 = int(settings.get_value_from_section('SWITCH_PORT_SLAVE2', 'SWITCH_PORT'), 16) #This is hex value
SWITCH_PORT_SLAVE3 = int(settings.get_value_from_section('SWITCH_PORT_SLAVE3', 'SWITCH_PORT'), 16) #This is hex value
#Acroname Switch Device Port Number (from A to Z)
SWITCH_PORT_AVER_540 = settings.get_value_from_section('SWITCH_PORT_AVER_540', 'SWITCH_PORT')
SWITCH_PORT_AVER_VB342 = settings.get_value_from_section('SWITCH_PORT_AVER_VB342', 'SWITCH_PORT')
SWITCH_PORT_AVER_VC520 = settings.get_value_from_section('SWITCH_PORT_AVER_VC520', 'SWITCH_PORT')
SWITCH_PORT_BRIO = settings.get_value_from_section('SWITCH_PORT_BRIO', 'SWITCH_PORT')
SWITCH_PORT_BRIO_500 = settings.get_value_from_section('SWITCH_PORT_BRIO_500', 'SWITCH_PORT')
SWITCH_PORT_BRIO_501 = settings.get_value_from_section('SWITCH_PORT_BRIO_501', 'SWITCH_PORT')
SWITCH_PORT_BRIO_505 = settings.get_value_from_section('SWITCH_PORT_BRIO_505', 'SWITCH_PORT')
SWITCH_PORT_BRIO_300 = settings.get_value_from_section('SWITCH_PORT_BRIO_300', 'SWITCH_PORT')
SWITCH_PORT_BRIO_301 = settings.get_value_from_section('SWITCH_PORT_BRIO_301', 'SWITCH_PORT')
SWITCH_PORT_BRIO_305 = settings.get_value_from_section('SWITCH_PORT_BRIO_305', 'SWITCH_PORT')
SWITCH_PORT_BRIO_1080P_WEBCAM = settings.get_value_from_section('SWITCH_PORT_BRIO_1080P_WEBCAM', 'SWITCH_PORT')
SWITCH_PORT_MX_BRIO = settings.get_value_from_section('SWITCH_PORT_MX_BRIO', 'SWITCH_PORT')
SWITCH_PORT_BRIO_701 = settings.get_value_from_section('SWITCH_PORT_BRIO_701', 'SWITCH_PORT')
SWITCH_PORT_MX_BRIO_705_FOR_BUSINESS = settings.get_value_from_section('SWITCH_PORT_MX_BRIO_705_FOR_BUSINESS', 'SWITCH_PORT')
SWITCH_PORT_BRIO_100 = settings.get_value_from_section('SWITCH_PORT_BRIO_100', 'SWITCH_PORT')
SWITCH_PORT_BRIO_101 = settings.get_value_from_section('SWITCH_PORT_BRIO_101', 'SWITCH_PORT')
SWITCH_PORT_BRIO_105 = settings.get_value_from_section('SWITCH_PORT_BRIO_105', 'SWITCH_PORT')
SWITCH_PORT_C920_HD_PRO_WEBCAM = settings.get_value_from_section('SWITCH_PORT_C920_HD_PRO_WEBCAM', 'SWITCH_PORT')
SWITCH_PORT_C920E = settings.get_value_from_section('SWITCH_PORT_C920E', 'SWITCH_PORT')
SWITCH_PORT_C922_PRO_STREAM_WEBCAM = settings.get_value_from_section('SWITCH_PORT_C922_PRO_STREAM_WEBCAM', 'SWITCH_PORT')
SWITCH_PORT_C925E = settings.get_value_from_section('SWITCH_PORT_C925E', 'SWITCH_PORT')
SWITCH_PORT_C930E = settings.get_value_from_section('SWITCH_PORT_C930E', 'SWITCH_PORT')
SWITCH_PORT_CC3000E = settings.get_value_from_section('SWITCH_PORT_CC3000E', 'SWITCH_PORT')
SWITCH_PORT_CONNECT = settings.get_value_from_section('SWITCH_PORT_CONNECT', 'SWITCH_PORT')
SWITCH_PORT_GROUP = settings.get_value_from_section('SWITCH_PORT_GROUP', 'SWITCH_PORT')
SWITCH_PORT_MEETUP = settings.get_value_from_section('SWITCH_PORT_MEETUP', 'SWITCH_PORT')
SWITCH_PORT_PTZ_PRO2 = settings.get_value_from_section('SWITCH_PORT_PTZ_PRO2', 'SWITCH_PORT')
SWITCH_PORT_RALLY = settings.get_value_from_section('SWITCH_PORT_RALLY', 'SWITCH_PORT')
SWITCH_PORT_RALLY_BAR_HUDDLE = settings.get_value_from_section('SWITCH_PORT_RALLY_BAR_HUDDLE', 'SWITCH_PORT')
SWITCH_PORT_SIGHT = settings.get_value_from_section('SWITCH_PORT_SIGHT', 'SWITCH_PORT')
SWITCH_PORT_RALLY_BAR = settings.get_value_from_section('SWITCH_PORT_RALLY_BAR', 'SWITCH_PORT')
SWITCH_PORT_RALLY_BAR_MINI = settings.get_value_from_section('SWITCH_PORT_RALLY_BAR_MINI', 'SWITCH_PORT')
SWITCH_PORT_RALLY_CAMERA = settings.get_value_from_section('SWITCH_PORT_RALLY_CAMERA', 'SWITCH_PORT')
SWITCH_PORT_SCRIBE = settings.get_value_from_section('SWITCH_PORT_SCRIBE', 'SWITCH_PORT')
SWITCH_PORT_STREAMCAM = settings.get_value_from_section('SWITCH_PORT_STREAMCAM', 'SWITCH_PORT')
SWITCH_PORT_SWYTCH = settings.get_value_from_section('SWITCH_PORT_SWYTCH', 'SWITCH_PORT')
SWITCH_PORT_TAP = settings.get_value_from_section('SWITCH_PORT_TAP', 'SWITCH_PORT')
SWITCH_PORT_YAMAHA_CS_700 = settings.get_value_from_section('SWITCH_PORT_YAMAHA_CS_700', 'SWITCH_PORT')
SWITCH_PORT_ZONE_750 = settings.get_value_from_section('SWITCH_PORT_ZONE_750', 'SWITCH_PORT')
SWITCH_PORT_ZONE_TRUE_WIRELESS = settings.get_value_from_section('SWITCH_PORT_ZONE_TRUE_WIRELESS', 'SWITCH_PORT')
SWITCH_PORT_ZONE_VIBE_125 = settings.get_value_from_section('SWITCH_PORT_ZONE_VIBE_125', 'SWITCH_PORT')
SWITCH_PORT_ZONE_VIBE_130 = settings.get_value_from_section('SWITCH_PORT_ZONE_VIBE_130', 'SWITCH_PORT')
SWITCH_PORT_ZONE_VIBE_WIRELESS = settings.get_value_from_section('SWITCH_PORT_ZONE_VIBE_WIRELESS', 'SWITCH_PORT')
SWITCH_PORT_ZONE_WIRED = settings.get_value_from_section('SWITCH_PORT_ZONE_WIRED', 'SWITCH_PORT')
SWITCH_PORT_ZONE_WIRED_EARBUDS = settings.get_value_from_section('SWITCH_PORT_ZONE_WIRED_EARBUDS', 'SWITCH_PORT')
SWITCH_PORT_ZONE_WIRELESS = settings.get_value_from_section('SWITCH_PORT_ZONE_WIRELESS', 'SWITCH_PORT')
SWITCH_PORT_ZONE_WIRELESS_2 = settings.get_value_from_section('SWITCH_PORT_ZONE_WIRELESS_2', 'SWITCH_PORT')
SWITCH_PORT_ZONE_WIRELESS_PLUS = settings.get_value_from_section('SWITCH_PORT_ZONE_WIRELESS_PLUS', 'SWITCH_PORT')
SWITCH_PORT_ZONE_900 = settings.get_value_from_section('SWITCH_PORT_ZONE_900', 'SWITCH_PORT')
SWITCH_PORT_ZONE_950 = settings.get_value_from_section('SWITCH_PORT_ZONE_950', 'SWITCH_PORT')
SWITCH_PORT_ZONE_950_CHARGE = settings.get_value_from_section('SWITCH_PORT_ZONE_950_CHARGE', 'SWITCH_PORT')
SWITCH_PORT_LOGI_DOCK = settings.get_value_from_section('SWITCH_PORT_LOGI_DOCK', 'SWITCH_PORT')
SWITCH_PORT_LITRA_BEAM = settings.get_value_from_section('SWITCH_PORT_LITRA_BEAM', 'SWITCH_PORT')
SWITCH_PORT_LOGI_DOCK_FLEX = settings.get_value_from_section('SWITCH_PORT_LOGI_DOCK_FLEX', 'SWITCH_PORT')
SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR = settings.get_value_from_section('SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR', 'SWITCH_PORT')
SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR_MINI = settings.get_value_from_section('SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR_MINI', 'SWITCH_PORT')
SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR_HUDDLE = settings.get_value_from_section('SWITCH_PORT_RAIDEN_HOSTED_RALLY_BAR_HUDDLE', 'SWITCH_PORT')
SWITCH_PORT_RAIDEN_HOSTED_SIGHT = settings.get_value_from_section('SWITCH_PORT_RAIDEN_HOSTED_SIGHT', 'SWITCH_PORT')
SWITCH_PORT_ZONE_305 = settings.get_value_from_section('SWITCH_PORT_ZONE_305', 'SWITCH_PORT')
SWITCH_PORT_H570E_MONO = settings.get_value_from_section('SWITCH_PORT_H570E_MONO', 'SWITCH_PORT')
SWITCH_PORT_H570E_STEREO = settings.get_value_from_section('SWITCH_PORT_H570E_STEREO', 'SWITCH_PORT')

INSTALLER = settings.get_value_from_section('INSTALLER', 'RUN_CONFIG')
TUNE_ENV = settings.get_value_from_section('TUNE_ENV', 'RUN_CONFIG')
TUNE_RECORDER = settings.get_value_from_section('TUNE_RECORDER', 'RUN_CONFIG').lower() == "true"
PROJECT = settings.get_value_from_section('PROJECT', 'RUN_CONFIG')
DASHBOARD_PUBLISH = settings.get_value_from_section('DASHBOARD_PUBLISH', 'RUN_CONFIG').lower() == "true"
JIRA_UPDATE = settings.get_value_from_section('JIRA_UPDATE', 'RUN_CONFIG').lower() == "true"
SYNC_API_VERSION = settings.get_value_from_section('SYNC_API_VERSION', 'RUN_CONFIG')
SYNC_PROD_VERSION1 = settings.get_value_from_section('SYNC_PROD_VERSION1', 'RUN_CONFIG')
SYNC_PROD_VERSION2 = settings.get_value_from_section('SYNC_PROD_VERSION2', 'RUN_CONFIG')

# JENKINS_FWU_TESTS Part
JENKINS_FWU_CONFIG = settings.get_value_from_section('JENKINS_FWU_CONFIG', 'JENKINS_FWU_TESTS').lower() == "true"
JENKINS_REPEATS = int(settings.get_value_from_section('JENKINS_REPEATS', 'JENKINS_FWU_TESTS'))
JENKINS_BASELINE_VERSION = settings.get_value_from_section('JENKINS_BASELINE_VERSION', 'JENKINS_FWU_TESTS')
JENKINS_TARGET_VERSION = settings.get_value_from_section('JENKINS_TARGET_VERSION', 'JENKINS_FWU_TESTS')
JENKINS_SVC_RUNNER = settings.get_value_from_section('JENKINS_SVC_RUNNER', 'JENKINS_FWU_TESTS').lower() == "true"

# Device IP
KONG_IP = settings.get_value_from_section('KONG_IP', 'DEVICE_IP')
HOSTEDKONG_IP = settings.get_value_from_section('HOSTEDKONG_IP', 'DEVICE_IP')
DIDDY_IP = settings.get_value_from_section('DIDDY_IP', 'DEVICE_IP')
HOSTEDDIDDY_IP = settings.get_value_from_section('HOSTEDDIDDY_IP', 'DEVICE_IP')
ATARI_IP = settings.get_value_from_section('ATARI_IP', 'DEVICE_IP')
NINTENDO_IP = settings.get_value_from_section('NINTENDO_IP', 'DEVICE_IP')
SEGA_IP = settings.get_value_from_section('SEGA_IP', 'DEVICE_IP')
COILY_IP = settings.get_value_from_section('COILY_IP', 'DEVICE_IP')
TINY_IP = settings.get_value_from_section('TINY_IP', 'DEVICE_IP')
HOSTEDTINY_IP = settings.get_value_from_section('HOSTEDTINY_IP', 'DEVICE_IP')
HOSTEDSENTINEL_IP = settings.get_value_from_section('HOSTEDSENTINEL_IP', 'DEVICE_IP')

# DESK_AND_ROOM_BOOKING
COILY_DEVICE_SN = settings.get_value_from_section('COILY_DEVICE_SN', 'DESK_AND_ROOM_BOOKING')
COILY_DESK_IP = settings.get_value_from_section('COILY_DESK_IP', 'DESK_AND_ROOM_BOOKING')
COILY_DESK_ID = settings.get_value_from_section('COILY_DESK_ID', 'DESK_AND_ROOM_BOOKING')
COILY_PERIPHERALS = settings.get_value_from_section('COILY_PERIPHERALS', 'DESK_AND_ROOM_BOOKING')
COILY_BASECAMP_LOCATION = settings.get_value_from_section('COILY_BASECAMP_LOCATION', 'DESK_AND_ROOM_BOOKING')
COILY_BASECAMP_NAME = settings.get_value_from_section('COILY_BASECAMP_NAME', 'DESK_AND_ROOM_BOOKING')
COILY_USER_CONFIG = settings.get_value_from_section('COILY_USER_CONFIG', 'DESK_AND_ROOM_BOOKING')
TUNE_CALENDAR_CONFIG = settings.get_value_from_section('TUNE_CALENDAR_CONFIG', 'DESK_AND_ROOM_BOOKING')
NINTENDO_DEVICE_SN = settings.get_value_from_section('NINTENDO_DEVICE_SN', 'DESK_AND_ROOM_BOOKING')
NINTENDO_DESK_IP = settings.get_value_from_section('NINTENDO_DESK_IP', 'DESK_AND_ROOM_BOOKING')

# LNA Credentials
LNA_USERNAME = settings.get_value_from_section('LNA_USERNAME', 'LNA_CREDENTIALS')
LNA_PASSWORD = settings.get_value_from_section('LNA_PASSWORD', 'LNA_CREDENTIALS')

# Host ID of hosts related to personal devices
HOST_PC_ID = settings.get_value_from_section('HOST_PC_ID', 'HOST_ID')

#Google Credentials
GOOGLE_ACCOUNT = settings.get_value_from_section('GOOGLE_ACCOUNT', 'GOOGLE_ACCOUNT_INFO')
GOOGLE_PASSWORD = settings.get_value_from_section('GOOGLE_PASSWORD', 'GOOGLE_ACCOUNT_INFO')

#Outlook Credentials
OUTLOOK_ACCOUNT = settings.get_value_from_section('OUTLOOK_ACCOUNT', 'OUTLOOK_ACCOUNT_INFO')
OUTLOOK_PASSWORD = settings.get_value_from_section('OUTLOOK_PASSWORD', 'OUTLOOK_ACCOUNT_INFO')

#Bluetooth MAC address
ZV125_BT_ADDRESS = settings.get_value_from_section('ZV125_BT_ADDRESS', 'DEVICE_BT_ADDRESS')
ZONE900_BT_ADDRESS = settings.get_value_from_section('ZONE900_BT_ADDRESS', 'DEVICE_BT_ADDRESS')

#Relay board control
ENDURO_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ENDURO_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ENDURO_POWER_ON_BUTTON = settings.get_value_from_section('ENDURO_POWER_ON_BUTTON', 'RELAY_BOARD')
ENDURO_POWER_OFF_BUTTON = settings.get_value_from_section('ENDURO_POWER_OFF_BUTTON', 'RELAY_BOARD')
ENDURO_POWER_PAIR_BUTTON = settings.get_value_from_section('ENDURO_POWER_PAIR_BUTTON', 'RELAY_BOARD')
ZV130_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZV130_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZV130_POWER_ON_BUTTON = settings.get_value_from_section('ZV130_POWER_ON_BUTTON', 'RELAY_BOARD')
ZV130_POWER_OFF_BUTTON = settings.get_value_from_section('ZV130_POWER_OFF_BUTTON', 'RELAY_BOARD')
ZV130_POWER_PAIR_BUTTON = settings.get_value_from_section('ZV130_POWER_PAIR_BUTTON', 'RELAY_BOARD')
ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON = settings.get_value_from_section('ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON', 'RELAY_BOARD')
ZONE_WIRELESS_POWER_ANC_BUTTON = settings.get_value_from_section('ZONE_WIRELESS_POWER_ANC_BUTTON', 'RELAY_BOARD')
ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZONE_VIBE_WIRELESS_ON_BUTTON = settings.get_value_from_section('ZONE_VIBE_WIRELESS_ON_BUTTON', 'RELAY_BOARD')
ZONE_VIBE_WIRELESS_OFF_BUTTON = settings.get_value_from_section('ZONE_VIBE_WIRELESS_OFF_BUTTON', 'RELAY_BOARD')
ZONE_VIBE_WIRELESS_PAIR_BUTTON = settings.get_value_from_section('ZONE_VIBE_WIRELESS_PAIR_BUTTON', 'RELAY_BOARD')
ZONE900_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZONE900_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZONE900_POWER_ON_OFF_PAIR_BUTTON = settings.get_value_from_section('ZONE900_POWER_ON_OFF_PAIR_BUTTON', 'RELAY_BOARD')
ZONE_300_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZONE_300_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZONE_300_POWER_ON_OFF_PAIR_BUTTON = settings.get_value_from_section('ZONE_300_POWER_ON_OFF_PAIR_BUTTON', 'RELAY_BOARD')
ZONE_305_RELAY_BOARD_SERIAL_NUMBER = settings.get_value_from_section('ZONE_305_RELAY_BOARD_SERIAL_NUMBER', 'RELAY_BOARD')
ZONE_305_POWER_ON_OFF_PAIR_BUTTON = settings.get_value_from_section('ZONE_305_POWER_ON_OFF_PAIR_BUTTON', 'RELAY_BOARD')

#Slave pc password
MAC_SLAVE_PASS = settings.get_value_from_section('MAC_SLAVE_PASS', 'SLAVE_PASSWORD')


