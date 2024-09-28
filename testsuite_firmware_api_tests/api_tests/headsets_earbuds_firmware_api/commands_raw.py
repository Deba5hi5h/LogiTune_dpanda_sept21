
# Get Feature
CMD_GET_FEATURE = ["sync_word_0", "sync_word_1", 0x05, 0x00, "feature_word", 0x0d, 0x01, 0x0]
# Get protocol version
CMD_GET_PROTOCOL_VERSION = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0xda]
# Get Total  Feature Count
CMD_GET_FEATURE_COUNT = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Feature ID
CMD_GET_FEATURE_ID = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Hardware info
CMD_GET_HARDWARE_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get firmware version
CMD_GET_FIRMWARE_VERSION = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
# Get Serial Number
CMD_GET_SERIAL_NUMBER = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Get Name
CMD_GET_NAME = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Name
CMD_SET_NAME = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0x1d, 0x05, 112, 0x61, 0x77, 0x65, 0x6c]
# Get Default Name
CMD_GET_DEFAULT_NAME = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Get Max Name Length
CMD_GET_MAX_NAME_LENGTH = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
# Get EQ Parameters
CMD_GET_EQ = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set EQ Parameters
CMD_SET_EQ = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0x1d, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
# Get EQ Modes
CMD_GET_EQ_MODES = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Get Band Info
CMD_GET_BAND_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
# Get Language
CMD_GET_LANGUAGE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
# Set Language
CMD_SET_LANGUAGE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x0d, 0x00]
# Set Earcon State
CMD_SET_EARCON_STATE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x2d, 0x00]
# Get Earcon state
CMD_GET_EARCON_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
# Get Language capabilities
CMD_GET_LANGUAGE_CAPABILITIES = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x4d]
# Get Connection Info
CMD_GET_CON_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Buds Case Aes Key
CMD_GET_BUDS_CASE_AES_KEY = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Role
CMD_GET_ROLE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Notification state
CMD_GET_NOTIFICATION_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
# Set Notification state
CMD_SET_NOTIFICATION_STATE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x2d, 0x00]
# Set Ear Detection State
CMD_SET_EAR_DETECTION_STATE_CMD = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Ear Detection State
CMD_GET_EAR_DETECTION_STATE_CMD = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Zaxxon Charging Case Info
CMD_GET_ZAXXON_CHARGING_CASE_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Start Gaia Ota
CMD_ZAXXON_START_GAIA_OTA = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
CMD_GET_STATUS_THERMAL = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
CMD_SET_HDMI_MODE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x0d, 0x00]
CMD_GET_HDMI_MODE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
CMD_GET_PORT_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
CMD_GET_PORT_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
CMD_ENABLE_EVENT = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x4d, 0x00]
CMD_SET_PORT_POWER = ["sync_word_0", "sync_word_1", 0x07, 0x00, "feature_word", 0x5d, 0x00, 0x00, 0x00, 0x00]
CMD_GET_UNMUTE_MODE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
CMD_SET_UNMUTE_MODE = ["sync_word_0", "sync_word_1", 0x06, 0x00, "feature_word", 0x1d, 0x00, 0x00, 0x00]
CMD_GET_REG_APP_IDS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
CMD_GET_VIDEO_MUTE_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
CMD_START_AMBIENT_LED = ["sync_word_0", "sync_word_1", 0x0d, 0x00, "feature_word", 0x0d]
CMD_CANCEL_AMBIENT_LED = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
CMD_START_CUSTOM_AMBIENT_LED = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
CMD_GET_SPEAKERPHONE_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
CMD_GET_SPEAKERPHONE_AUDIO_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
CMD_GET_SPEAKERPHONE_CONN_STATE= ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
CMD_GET_SPEAKERPHONE_PAIRING_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x3d]
CMD_GET_SPEAKERPHONE_PAIRED_DEV_INFO = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0xcd]
CMD_GET_LED_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
CMD_SET_LED_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d, 0x00]
# Get Sidetone Level
CMD_GET_SIDETONE_LEVEL = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Set Sidetone Level
CMD_SET_SIDETONE_LEVEL = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x3d, 0x05]
# Get Mic Mute Status
CMD_GET_MIC_MUTE_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Mic Mute
CMD_SET_MIC_MUTE_STATUS = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x01]
# Set Voice Notifications Status
CMD_SET_VOICE_NOTIF_STATUS = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x3d, 0x00]
# Get Voice Notifications Status
CMD_GET_VOICE_NOTIF_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Set Mic Boom status
CMD_SET_MIC_BOOM_CMD = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x6d, 0x00]
# Get Mic Boom status
CMD_GET_MIC_BOOM_CMD = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x5d]
# Get BT Sleep timer
CMD_GET_SLEEP_TIMER = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# set sleep timer
CMD_SET_SLEEP_TIMER = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x0f]
# Get ANC Status
CMD_GET_ANC_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x4d]
# Set ANC Status
CMD_SET_ANC = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x5d, 0x01]
# Get connected device number
CMD_CONNECTED_DEVICE_NUMBER = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get connected device info
CMD_CONNECTED_DEVICE_INFO = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get audio active device
CMD_AUDIO_ACTIVE_DEVICE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x4d]
# Get Device Connect Status
CMD_GET_DEVICE_CONNECT_STATUS = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0x3d, 0xc0, 0x28, 0x8d, 0xaf, 0xa1, 0x11]
# Get Device Connected Name
CMD_GET_DEVICE_CONNECTED_NAME = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0x2d, 0xc0, 0x28, 0x8d, 0xaf, 0xa1, 0x11]
# Get Dongle FW version
CMD_GET_DONGLE_FW_VERSION = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x6d]
# Get PDL Device Info
CMD_GET_A2DP_MUTE_STATUS = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0x7d, 0xe4, 0xa4, 0x71, 0x34, 0xb9, 0x70]
# Set PDL Device Info
CMD_SET_A2DP_MUTE_STATUS = ["sync_word_0", "sync_word_1", 0x0a, 0x00, "feature_word", 0x8d, 0xe4, 0xa4, 0x71, 0x34, 0xb9, 0x70, 0x00]
# Get PDL Device Info
CMD_GET_PDL_DEVICE_NUMBER = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x9d]
# Get PDL Device Info
CMD_GET_PDL_DEVICE_INFO = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0xad, 0x02]
# Remove Device from PDL
CMD_REMOVE_DEVICE_FROM_PDL = ["sync_word_0", "sync_word_1", 0x09, 0x00, "feature_word", 0xbd, 0xc0, 0xbd, 0xc8, 0x4d, 0x2b, 0x14]
# Get Battery status
CMD_GET_BATTERY_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Button General Settings
CMD_GET_BUTTON_GEN_SETTINGS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x9d]
# Get Button Individual Capability
CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0xad, 0x00]
# Set Button Individual Capability
CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY = ["sync_word_0", "sync_word_1", 0x06, 0x00, "feature_word", 0xbd, 0x00, 0x00, 0x00]
# Get Button General Settings
CMD_RESET_BUTTON_CUSTOMIZATION_SETTINGS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0xcd]
# Get Voice Notifications Status
CMD_FACTORY_RESET_DEVICE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x4d]
# Set Do Not Disturb Mode
CMD_SET_DO_NOT_DISTRUB_MODE_CMD = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Do Not Disturb Mode
CMD_GET_DO_NOT_DISTRUB_MODE_CMD = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get BT state
CMD_GET_BT_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
# Set discoverable state
CMD_SET_DISCOVERABLE_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Get Battery status
CMD_GET_VOLTAGE_STATUS = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x1d]
# Get AI Noise reduction
CMD_GET_AI_NOISE_REDUCTION = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x2d]
# Set AI Noise reduction
CMD_SET_AI_NOISE_REDUCTION = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x3d, 0x00]
# Get Noise Exposure
CMD_GET_NOISE_EXPOSURE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Noise Exposure
CMD_SET_NOISE_EXPOSURE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Anti Startle
CMD_GET_ANTI_STARTLE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Anti Startle
CMD_SET_ANTI_STARTLE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get ANC Customization Mode
CMD_GET_ANC_CUSTOMIZATION_MODE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0xbd]
# Set ANC Customization Mode
CMD_SET_ANC_CUSTOMIZATION_MODE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0xcd, 0x00]
# Get Auto Answer On Call
CMD_GET_AUTO_ANSWER_ON_CALL = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Auto Answer On Call
CMD_SET_AUTO_ANSWER_ON_CALL = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Auto Mute On Call
CMD_GET_AUTO_MUTE_ON_CALL = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Auto Mute On Call
CMD_SET_AUTO_MUTE_ON_CALL = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Touch Sensor State
CMD_GET_TOUCH_SENSOR_STATE = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Touch Sensor State
CMD_SET_TOUCH_SENSOR_STATE = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
# Get Headset Active EQ
CMD_GET_HEADSET_ACTIVE_EQ = ["sync_word_0", "sync_word_1", 0x03, 0x00, "feature_word", 0x0d]
# Set Headset Active EQ
CMD_SET_HEADSET_ACTIVE_EQ = ["sync_word_0", "sync_word_1", 0x04, 0x00, "feature_word", 0x1d, 0x00]
