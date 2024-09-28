from selenium.webdriver.common.by import By

class SyncAppLocators(object):
    """
    A class containing the Sync App
    element locators.
    """
    SYNC_APP = (By.NAME, "Sync")
    WAD_MENU = (By.XPATH, "//*[@LocalizedControlType='image'][3]")
    MENU = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']/following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']") #1st item
    RENAME_ROOM = (By.XPATH, "//li[text()='Rename Room']")
    UPDATE_SYNC_NOW = (By.XPATH, "//div[text()='Update Sync Now']")
    ROOM_EDIT_BOX = (By.XPATH, "//input[@maxlength='63']")
    ROOM_NAME = (By.XPATH, "//div/span/following-sibling::span/preceding-sibling::span")
    ROOM_NAME_FRE = (By.XPATH, "//label[text()='Room Name']/parent::div//input")
    ROOM_NAME_WAD = (By.XPATH, "//*[@Name='Room Name']/following-sibling::*[@LocalizedControlType='edit']")
    ABOUT = (By.XPATH, "//*[@Name='About Logitech Sync']")
    VERSION = (By.XPATH, "//*[contains(@Name, 'Version')]")
    # CHECK_FOR_UPDATE = (By.NAME, "CHECK FOR UPDATE")
    EULA = (By.NAME, "EULA")
    PRIVACY_POLICY = (By.NAME, "Privacy Policy")
    GET_STARTED_WAD = (By.NAME, "GET STARTED")
    SKIP_SETUP_WAD = (By.NAME, "SKIP SETUP")
    EMAIL_SETUP_WAD = (By.NAME, "Email and password")

    GET_STARTED = (By.XPATH, "//*[text()='Get Started']")
    SKIP_SETUP = (By.XPATH, "//*[text()='Skip Setup']")
    EMAIL_SETUP = (By.XPATH, "//*[text()='Email and password']")
    PROVISION_CODE_SETUP = (By.XPATH, "//*[text()='Room provision code']")
    PROVISION_CODE = (By.XPATH, "//input")
    ROOM_LINK = (By.XPATH, "//p[text()='Room']/following-sibling::div/*[local-name()='svg']/parent::div/preceding-sibling::p")
    CONNECT_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Connect to Sync Portal.']")
    USER_NAME_WAD = (By.XPATH, "//*[@LocalizedControlType='edit'][1]")
    PASSWORD_WAD = (By.XPATH, "//*[@LocalizedControlType='edit'][2]")
    USER_NAME = (By.XPATH, "//label[text()='Username']/following-sibling::div/input")
    PASSWORD = (By.XPATH, "//label[text()='Password']/following-sibling::div/input")
    CONNECT_ROOM_WAD = (By.NAME, "CONNECT ROOM")
    CONNECT_ROOM = (By.XPATH, "//span[text()='Connect room']/parent::button")
    PROVISION_CODE_MULTIPLE_HOSTS_ERROR = (By.XPATH, "//p[text()='This room already has host PC/appliance device']")
    INCORRECT_PROVISION_CODE_ERROR = (By.XPATH, "//p[text()='This provisioning code is invalid']")
    GROUP_NODE = (By.XPATH, "//p[text()='XXX']") # Pass group name
    GROUP_RADIO = (By.XPATH, "//p[text()='XXX']/parent::div/preceding-sibling::span//input")  # Pass group name
    NEXT_WAD = (By.NAME, "NEXT")
    NEXT_FRE = (By.XPATH, "//span[text()='Next']")
    # ROOM_NAME = (By.XPATH, "//*[@Name='Room Name']/following-sibling::*[@LocalizedControlType='edit']")
    SEAT_COUNT_WAD = (By.XPATH, "//*[@Name='Seat Count']/following-sibling::*[@LocalizedControlType='edit']")
    SEAT_COUNT_FRE = (By.XPATH, "//label[text()='Seat Count']/parent::div//input")
    DISCONNECT_ROOM_WAD = (By.NAME, "DISCONNECT")
    DISCONNECT_ROOM = (By.XPATH, "//button/span[text()='Disconnect']")
    ROOM_CONNECTED_WAD = (By.XPATH, "//*[contains(@Name, 'Connected to')]")
    ROOM_CONNECTED = (By.XPATH, "//p[contains(text(),'Connected to')]")
    UPDATE_AVAILABLE = (By.XPATH, "//p[text()='Firmware update available.']")
    UPDATE_FAILED = (By.XPATH, "//p[text()='Update failed.']")
    UPDATE = (By.XPATH, "//button/span[text()='Update']")
    UPDATE_NOW = (By.XPATH, "//button/span[text()='Update Now' or text()='Update now']")
    SCHEDULE_UPDATE = (By.XPATH, "//button/span[text()='Schedule Update']")
    SCHEDULE_UPDATE_WAD = (By.XPATH, "//Button[@Name='Schedule Update']")
    BACK = (By.XPATH, "//button/span[text()='Back']")
    ADD_DEVICE = (By.XPATH, "//*[text()='Add Device']")
    DONE_BUTTON = (By.XPATH, "//span[text()='Done']")
    DONE_BUTTON_WAD = (By.NAME, "DONE")
    JOIN_GROUP_WAD = (By.NAME, "JOIN")
    JOIN_GROUP = (By.XPATH, "//button/span[text()='Join']")
    READ_ONLY_MSG = (By.XPATH, "//p[text()='Read Only permission. Please contact an admin with permission to add rooms.']")
    THIRD_PARTY_MSG = (By.XPATH, "//p[text()='Third Party permission']")
    OWNER_MSG = (By.XPATH, "//p[text()='Owner permission']")
    DISCONNECT_PERMISSION_MSG = (By.XPATH, "//p[text()='Please contact an admin with permission to add rooms.']")
    NO_ORGANIZATION_MSG = (By.XPATH, "//p[text()='No affiliated organization found']")
    OK_BUTTON = (By.XPATH, "//span[text()='Ok']")
    SEAT_COUNT = (By.XPATH, "//label[text()='Seat Count']/following-sibling::div/input")

    #Device Setup
    SIGN_IN_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Sign in to Sync portal']")
    CONNECT_THIS_ROOM_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Connect this room to Sync portal']")
    ROOM_INFORMATION = (By.XPATH, "//p[text()='Room Information']")
    WHAT_WOULD_YOU_LIKE_TO_SET_UP = (By.XPATH, "//p[text()='What would you like to set up?']")
    RALLY_CAMERA_SETUP_BUTTON = (By.XPATH, "//button/span[text()='Rally Camera']")
    RALLY_SETUP_BUTTON = (By.XPATH, "//button/span[text()='Rally & Rally Plus']")
    MEETUP_SETUP_BUTTON = (By.XPATH, "//button/span[text()='MeetUp']")

    SIGN_IN_TO_SYNC_PORTAL_WAD = (By.NAME, "SIGN IN TO SYNC PORTAL")
    CONNECT_THIS_ROOM_TO_SYNC_PORTAL_WAD = (By.NAME, "CONNECT THIS ROOM TO SYNC PORTAL")
    NO_THANKS_WAD = (By.NAME, "NO THANKS")
    ROOM_INFORMATION_WAD = (By.NAME, "ROOM INFORMATION")
    SEAT_ERROR_WAD = (By.NAME, "Please enter a valid number.")
    SEAT_ERROR = (By.XPATH, "//p[text()='Please enter a valid number.']")
    WHAT_WOULD_YOU_LIKE_TO_SET_UP_WAD = (By.NAME, "WHAT WOULD YOU LIKE TO SET UP?")
    RALLY_SETUP_BUTTON_WAD = (By.XPATH, "//Button[@Name='RALLY & RALLY PLUS']")
    LETS_SETUP_RALLY = (By.XPATH, "//p[text()=\"Let's setup Rally\"]")
    LETS_SETUP_RALLY_WAD = (By.NAME, "LET'S SETUP RALLY")
    RALLY_CAMERA_SETUP_BUTTON_WAD = (By.XPATH, "//Button[@Name='RALLY CAMERA']")
    LETS_SETUP_RALLY_CAMERA = (By.XPATH, "//p[text()=\"Let's setup Rally Camera\"]")
    RALLY_CAMERA_SETUP_VIDEO = (By.XPATH, "//*[text()='How To Setup the Logitech Rally Camera (Basic)']")
    LETS_SETUP_RALLY_CAMERA_WAD = (By.NAME, "LET'S SETUP RALLY CAMERA")
    MEETUP_SETUP_BUTTON_WAD = (By.XPATH, "//Button[@Name='MEETUP']")
    LETS_SETUP_MEETUP = (By.XPATH, "//p[text()=\"Let's setup MeetUp\"]")
    LETS_SETUP_MEETUP_WAD = (By.NAME, "LET'S SETUP MEETUP")
    CONNECT_RALLY_NOW = (By.NAME, "CONNECT RALLY NOW")
    CONNECT_MEETUP_NOW = (By.NAME, "CONNECT MEETUP NOW")
    CONNECT_RALLY_CAMERA_NOW = (By.NAME, "CONNECT RALLY CAMERA NOW")
    SYSTEM_DOESNT_SEE_DEVICE = (By.XPATH, "//button[text()=\"The system doesn't see my device\"]")
    SYSTEM_DOESNT_SEE_DEVICE_WAD = (By.NAME, "The system doesn't see my device")
    WHERE_PLACE_COMPUTER = (By.XPATH, "//button[text()='Where should I place the computer?']")
    WHERE_PLACE_COMPUTER_WAD = (By.NAME, "Where should I place the computer?")
    COMPUTER_BY_THE_TV = (By.XPATH, "//p[text()='Computer by the TV']")
    COMPUTER_BY_THE_TV_VIDEO = (By.XPATH, "//*[text()='Rally Setup with computer at the display']")
    COMPUTER_BY_THE_TV_WAD = (By.NAME, "Computer by the TV")
    COMPUTER_BY_THE_TV_VIDEO_WAD = (By.NAME, "Rally Setup with computer at the display")
    COMPUTER_BY_THE_TABLE = (By.XPATH, "//p[text()='Computer by the table']")
    COMPUTER_BY_THE_TABLE_VIDEO = (By.XPATH, "//*[text()='Rally Setup with computer at the table']")
    COMPUTER_BY_THE_TABLE_WAD = (By.NAME, "Computer by the table")
    COMPUTER_BY_THE_TABLE_VIDEO_WAD = (By.NAME, "Rally Setup with computer at the table")
    SETUP_RALLY_CAMERA = (By.XPATH, "//p[text()='Set up Rally Camera']")
    SETUP_RALLY_CAMERA_WAD = (By.NAME, "Set up Rally Camera")
    SETUP_RALLY_CAMERA_VIDEO_WAD = (By.NAME, "How To Setup the Logitech Rally Camera (Basic)")
    SETUP_MEETUP = (By.XPATH, "//p[text()='Set up MeetUp']")
    SETUP_MEETUP_WAD = (By.NAME, "Set up MeetUp")
    SETUP_MEETUP_VIDEO_WAD = (By.NAME, "How To Setup the Logitech MeetUp ConferenceCam")
    SETUP_MEETUP_VIDEO = (By.XPATH, "//*[text()='How To Setup the Logitech MeetUp ConferenceCam']")
    CLOSE = (By.XPATH, "//span[text()='close']")
    CLOSE_WAD = (By.XPATH, "//Button[@Name='close']")
    SYNC_SETUP_COMPLETE_WAD = (By.NAME, "SYNC SETUP COMPLETE!")
    SYNC_SETUP_COMPLETE = (By.XPATH, "//p[text()='Sync Setup Complete!']")
    OK_GOT_IT = (By.XPATH, "//span[text()='Ok, Got it']")
    OK_GOT_IT_WAD = (By.XPATH, "//Button[@Name='OK, GOT IT']")
    SHARE_ANALYTICS_DATA_WAD = (By.XPATH, "//Button[@Name='SHARE ANALYTICS DATA']")
    SHARE_ANALYTICS_DATA = (By.XPATH, "//span[text()='Share analytics data']")
    HELP_US_IMPROVE_WAD = (By.NAME, "HELP US IMPROVE YOUR EXPERIENCE")
    HELP_US_IMPROVE = (By.XPATH, "//p[text()='Help us improve your experience']")

    #Audio
    AUDIO_TAB_TEXT = (By.XPATH, "//p[contains(text(), 'Test mics and speakers')]")
    TEST_MIC_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Test Mic')]")
    STOP_RECORDING_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Stop Recording')]")
    STOP_PLAYING_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Stop Playing')]")
    TEST_SPEAKER1 = (By.XPATH, "//*[@LocalizedControlType='button' and contains(@Name, 'Test Speaker')]")
    TEST_SPEAKER = (By.XPATH, "//button/span[contains(text(),'Test') and contains(text(), 'peaker')]")
    REFER_TO_FAQ = (By.XPATH, "//a[text()='refer to our FAQs']")

    #Video
    FULL_SCREEN = (By.XPATH, "//p[text()='Full Screen']")
    EXIT_FULL_SCREEN = (By.XPATH, "//p[text()='Exit Full Screen']")
    LEARN_MORE = (By.XPATH, "//a[text()='Learn more']")
    EDIT_BOUNDARIES = (By.XPATH, "//span[text()='Edit Boundaries']/parent::button")
    # AUTO_CALIBRATE = (By.XPATH, "//span[text()='Auto Calibrate']/parent::button")
    # EDIT_BOUNDARIES_CANCEL = (By.XPATH, "//span[text()='Cancel']/parent::button")
    # EDIT_BOUNDARIES_CONFIRM = (By.XPATH, "//span[text()='Confirm']/parent::button")
    AUTO_CALIBRATE = (By.XPATH, "//button[1]")
    EDIT_BOUNDARIES_CANCEL = (By.XPATH, "//button[3]")
    EDIT_BOUNDARIES_CONFIRM = (By.XPATH, "//button[2]")
    # AUTO_CALIBRATE_STATUS = (By.XPATH, "//button[1]")
    # EDIT_BOUNDARIES_CANCEL_STATUS = (By.XPATH, "//button[3]")
    # EDIT_BOUNDARIES_CONFIRM_STATUS = (By.XPATH, "//button[2]")

    LETS_FIX_IT = (By.XPATH, "//button/span[text()=\"Let's Fix It\"]")
    FORGET = (By.XPATH, "//button/span[text()='Forget']")
    FORGET_NOW = (By.XPATH, "//button/span[text()='Forget Now']")

    #Kebab Options
    CHECK_FOR_DEVICE_UPDATE = (By.XPATH, "//li[text()='Check for Device Update']")
    # WAD_FORGET_DEVICE = (By.NAME, "Forget Device")
    FORGET_DEVICE = (By.XPATH, "//li[text()='Forget Device']")
    REMOVE_PROBLEM_DEVICE = (By.NAME, "REMOVE A PROBLEM DEVICE")
    QUICK_START_GUIDE = (By.XPATH, "//li[text()='Quick Start Guide']")
    SETUP_VIDEO = (By.XPATH, "//li[text()='Setup Video']")
    PRODUCT_SUPPORT = (By.XPATH, "//li[text()='Product Support']")
    ORDER_NEW_DEVICE = (By.XPATH, "//li[text()='Order New Device']")

    #Device related Menu, Info
    WAD_MENU_ICON = (By.XPATH, "//*[@Name='Device not found?' and @LocalizedControlType='button']/following-sibling::*[@LocalizedControlType='image']/following-sibling::*[@LocalizedControlType='image']")
    MENU_ICON = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']/following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']") #2nd item
    INFO_ICON = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']/following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']/preceding-sibling::*[local-name()='svg']")

    #Device Version
    PID = (By.XPATH, "//p[text()='PID']/parent::div/following-sibling::div/p")
    AUDIO_FIRMWARE = (By.XPATH, "//p[text()='Audio Firmware']/parent::div/following-sibling::div/p")
    BLE_FIRMWARE = (By.XPATH, "//p[text()='BLE Firmware']/parent::div/following-sibling::div/p")
    CODEC_FIRMWARE = (By.XPATH, "//p[text()='Codec Firmware']/parent::div/following-sibling::div/p")
    EEPROM_FIRMWARE = (By.XPATH, "//p[text()='EEPROM Firmware']/parent::div/following-sibling::div/p")
    VIDEO_FIRMWARE = (By.XPATH, "//p[text()='Video Firmware']/parent::div/following-sibling::div/p")
    SERIAL_NUMBER = (By.XPATH, "//p[text()='Serial Number']/parent::div/following-sibling::div/p")
    LOGI_COLLABOS = (By.XPATH, "//p[text()='Logi CollabOS']/parent::div/following-sibling::div/p")
    FIRMWARE_VERSION = (By.XPATH, "//p[text()='Firmware Version']/parent::div/following-sibling::div/p")
    SYSTEM_IMAGE = (By.XPATH, "//p[text()='System Image']/parent::div/following-sibling::div/p")
    AUDIO = (By.XPATH, "//p[text()='Audio']/parent::div/following-sibling::div/p")
    HOUSEKEEPING = (By.XPATH, "//p[text()='Housekeeping']/parent::div/following-sibling::div/p")
    ZOOM_FOCUS = (By.XPATH, "//p[text()='Zoom & Focus']/parent::div/following-sibling::div/p")
    PAN_TILT = (By.XPATH, "//p[text()='Pan & Tilt']/parent::div/following-sibling::div/p")

    UI_NODES = (By.XPATH, "//div[contains(@class, 'align')]/p")
    DEVICE_NODE = (By.XPATH, "//div[contains(@class, 'align')]/p[text()='XXX']") #Pass Device Name
    DEVICE_ERROR_MESSAGE = (By.XPATH, "//*[text()='There was a problem connecting to XXX.']") #Pass Device Name
    DEVICE_CONNECT_MESSAGE = (By.XPATH, "//*[text()='XXX has been connected.']") #Pass Device Name
    DEVICE_DISCONNECT_MESSAGE = (By.XPATH, "//*[text()='XXX has been forgotten.']")  # Pass Device Name

    DEVICE_UPDATE_MESSAGE = (By.XPATH, "//*[text()='XXX is up to date.']")  # Pass Device Name
    DEVICE_UPDATE_SUCCESS_MESSAGE = (By.XPATH, "//*[text()='XXX successfully updated']")  # Pass Device Name

    RIGHT_SIGHT_TOGGLE = (By.XPATH, "//p[text()='Use RightSight']/ancestor::div[2]//input")
    RIGHT_SIGHT2_TOGGLE = (By.XPATH, "//p[text()='RightSight 2']/parent::div/preceding-sibling::div//input")
    GROUP_VIEW = (By.XPATH, "//p[text()='Group View']/parent::div/preceding-sibling::span//input")
    GROUP_VIEW_NEW = (By.XPATH, "//p[text()='Group View']/parent::div")
    SPEAKER_VIEW = (By.XPATH, "//p[text()='Speaker View (Beta)']/parent::div/preceding-sibling::span//input")
    SPEAKER_VIEW_NEW = (By.XPATH, "//p[text()='Speaker View']/parent::div")
    PICTURE_IN_PICTURE_TOGGLE = (By.XPATH, "//p[text()='Picture In Picture']/parent::div/preceding-sibling::div//input")
    VIDEO_TAB = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//following-sibling::div/p[text()='Video']/parent::div") # Pass Device Name
    CAMERA_TAB = (By.XPATH,
                 "//p[text()='XXX']/parent::div/parent::div//following-sibling::div/p[text()='Camera']/parent::div")  # Pass Device Name
    # AUDIO_TAB = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//following-sibling::div/p[text()='Audio']/parent::div") # Pass Device Name
    AUDIO_TAB = (By.XPATH,
                 "//p[text()='XXX']/parent::div/parent::div//following-sibling::div/p[text()='Audio']")  # Pass Device Name
    CONNECTIVITY_TAB = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//following-sibling::div/p[text()='Connectivity']/parent::div")  # Pass Device Name
    DYNAMIC_RADIO = (By.XPATH, "//p[text()='Dynamic']/parent::div/preceding-sibling::span//input")
    ON_CALL_START_RADIO = (By.XPATH, "//p[contains(text(), 'call start')]/parent::div/preceding-sibling::span//input")
    PAL_50HZ = (By.XPATH, "//p[text()='PAL 50Hz']/parent::div/preceding-sibling::span//input")
    NTSC_60HZ = (By.XPATH, "//p[text()='NTSC 60Hz']/parent::div/preceding-sibling::span//input")
    BLUETOOTH_TOGGLE = (By.XPATH, "//p[text()='Enable']/parent::div/preceding-sibling::div//input")
    SPEAKER_BOOST = (By.XPATH, "//p[text()='Speaker Boost']/following-sibling::div[1]//input")
    AI_NOISE_SUPPRESSION = (By.XPATH,
                     "//p[text()='AI Noise Suppression']/following-sibling::div[1]//input")
    REVERB_DISABLE_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]//p[text()='Disabled']/parent::div/preceding-sibling::span//input")
    # REVERB_NORMAL_RADIO = (By.XPATH, "//*[@Name='Normal (Recommended)']/preceding-sibling::*[@LocalizedControlType='radio button']")
    REVERB_NORMAL_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]//p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    # REVERB_AGGRESSIVE_RADIO  = (By.XPATH, "//*[@Name='Aggressive']/preceding-sibling::*[@LocalizedControlType='radio button']")
    REVERB_AGGRESSIVE_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]//p[text()='Aggressive']/parent::div/preceding-sibling::span//input")
    MICROPHONE_BASS_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//p[text()='Bass Boost']/parent::div/preceding-sibling::span//input")
    MICROPHONE_NORMAL = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    MICROPHONE_VOICE_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//p[text()='Voice Boost']/parent::div/preceding-sibling::span//input")
    SPEAKER_BASS_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//p[text()='Bass Boost']/parent::div/preceding-sibling::span//input")
    SPEAKER_NORMAL = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    SPEAKER_VOICE_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//p[text()='Voice Boost']/parent::div/preceding-sibling::span//input")

    SWYTCH_CONNECTED_TO_EXTERNAL_PC = (By.XPATH, "//*[text()='Swytch is connected to an external computer']")
    SWYTCH_BYOD_DEVICE_STATUS = (By.XPATH, "//*[text()='Status unknown since the device has been connected to an external computer']")
    SWYTCH_BYOD_DEVICE_SETTINGS = (By.XPATH, "//*[text()='Settings can not be modified now since the device has been connected to an external computer']")

    SPEAKER_DETECTION_SLOW = (By.XPATH, "//p[text()='Speaker Detection']/following-sibling::div[3]//p[text()='Slower']/parent::div/preceding-sibling::span//input")
    SPEAKER_DETECTION_DEFAULT = (By.XPATH,"//p[text()='Speaker Detection']/following-sibling::div[3]//p[text()='Default']/parent::div/preceding-sibling::span//input")
    SPEAKER_DETECTION_FAST = (By.XPATH,"//p[text()='Speaker Detection']/following-sibling::div[3]//p[text()='Faster']/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_SLOW = (By.XPATH, "//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Slower']/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_DEFAULT = (By.XPATH,"//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Default']/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_FAST = (By.XPATH,"//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Faster']/parent::div/preceding-sibling::span//input")

    # Room Information
    ROOM_INFO = (By.XPATH, "//p[text()='Add Device']/ancestor::div[4]/following-sibling::div//p[text()='Room']/following-sibling::div//*[local-name()='svg']")
    COMPUTER_TYPE = (By.XPATH, "//p[text()='Computer Type']/ancestor::div[2]/following-sibling::div/p")
    OPERATING_SYSTEM = (By.XPATH, "//p[text()='Operating System']/ancestor::div[2]/following-sibling::div/p")
    OS_VERSION = (By.XPATH, "//p[text()='OS Version']/ancestor::div[2]/following-sibling::div/p")
    PROCESSOR = (By.XPATH, "//p[text()='Processor']/ancestor::div[2]/following-sibling::div/p")
    MEMORY = (By.XPATH, "//p[text()='Memory']/ancestor::div[2]/following-sibling::div/p")

    # Camera Settings
    RESET_CAMERA_ADJUSTMENTS = (
        By.XPATH, "//p[contains(text(),'adjustments')]/following-sibling::*[local-name()='svg']")
    RESET_MANUAL_COLOR_SETTINGS = (
        By.XPATH, "//p[contains(text(),'Manual color')]/following-sibling::*[local-name()='svg']")
    MANUAL_COLOR_SETTINGS = (By.XPATH, "//p[text()='Manual color settings']/ancestor::div[2]")
    AUTO_EXPOSURE = (By.XPATH, "//p[text()='Auto exposure']/ancestor::div[3]//input")
    AUTO_WHITE_BALANCE = (By.XPATH, "//p[text()='Auto white balance']//ancestor::div[3]//input")
    BRIGHTNESS = (By.XPATH, "//p[text()='Brightness']/ancestor::div[3]/child::div[2]/child::div[1]/child::span")
    CONTRAST = (By.XPATH, "//p[text()='Contrast']/ancestor::div[3]/child::div[2]/child::div[1]/child::span")
    SATURATION = (By.XPATH, "//p[text()='Saturation']/ancestor::div[3]/child::div[2]/child::div[1]/child::span")
    SHARPNESS = (By.XPATH, "//p[text()='Sharpness']/ancestor::div[3]/child::div[2]/child::div[1]/child::span")
    BRIGHTNESS_PERCENTAGE = (By.XPATH, "//p[text()='Brightness']/ancestor::div[3]/child::div[2]//p")
    CONTRAST_PERCENTAGE = (By.XPATH, "//p[text()='Contrast']/ancestor::div[3]/child::div[2]//p")
    SATURATION_PERCENTAGE = (By.XPATH, "//p[text()='Saturation']/ancestor::div[3]/child::div[2]//p")
    SHARPNESS_PERCENTAGE = (By.XPATH, "//p[text()='Sharpness']/ancestor::div[3]/child::div[2]//p")
    VIDEO_STREAM = (By.XPATH, "//video")
    BRIGHTNESS_SLIDER = (
        By.XPATH, "//p[text()='Brightness']/ancestor::div[2]/following-sibling::div//input/parent::span")
    BRIGHTNESS_SLIDER_KNOB = (
        By.XPATH, "//p[text()='Brightness']/ancestor::div[2]/following-sibling::div//input/following-sibling::span")
    CONTRAST_SLIDER = (
        By.XPATH, "//p[text()='Contrast']/ancestor::div[2]/following-sibling::div//input/parent::span")
    CONTRAST_SLIDER_KNOB = (
        By.XPATH, "//p[text()='Contrast']/ancestor::div[2]/following-sibling::div//input/following-sibling::span")
    SATURATION_SLIDER = (
        By.XPATH, "//p[text()='Saturation']/ancestor::div[2]/following-sibling::div//input/parent::span")
    SATURATION_SLIDER_KNOB = (
        By.XPATH, "//p[text()='Saturation']/ancestor::div[2]/following-sibling::div//input/following-sibling::span")
    SHARPNESS_SLIDER_KNOB = (
        By.XPATH, "//p[text()='Sharpness']/ancestor::div[2]/following-sibling::div//input/following-sibling::span")
    SHARPNESS_SLIDER = (
        By.XPATH, "//p[text()='Sharpness']/ancestor::div[2]/following-sibling::div//input/parent::span")
    GRID_BUTTON = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']")
    GRID_BUTTON_PROPERTY = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']//*[local-name()='mask']")
    GRID_LINES_VERTICAL = (By.XPATH, "//video/parent::div/following-sibling::div[1]/div")
    GRID_LINES_HORIZONTAL = (By.XPATH, "//video/parent::div/following-sibling::div[2]/div")
    VIDEO_PREVIEW_COLLAPSE = (By.XPATH, "//p[text()='Video preview']/ancestor::div[2]")
    VIDEO_PREVIEW_RESTORE = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']")

    #Camera Adjustments
    CAMERA_ADJUSTMENTS = (By.XPATH, "//p[text()='Camera adjustments']/ancestor::div[2]")
    AUTO_FOCUS = (By.XPATH, "//p[text()='Auto focus']/ancestor::div[3]//input")
    MANUAL_FOCUS_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual focus']/ancestor::div[3]//input/following-sibling::span")
    MANUAL_EXPOSURE_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual exposure']/ancestor::div[3]//input/following-sibling::span")
    MANUAL_WHITE_BALANCE_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual white balance']/ancestor::div[3]//input/following-sibling::span")

    #Room Menu items
    UPDATES_AND_ABOUT = (By.XPATH, "//li[text()='Updates and About']")
    ABOUT_LOGITECH_SYNC = (By.XPATH, "//li[text()='About Logitech Sync']")

    #Sync Updates and Menu screen
    SYNC_VERSION = (By.XPATH, "//p[contains(text(),'Version')]")
    ROOM_SYNC_UPDATE_AVAILABLE = (By.XPATH, "//p[contains(text(), 'New Sync App version') and "
                                            "contains(text(), 'available')]")
    ROOM_SYNC_UPDATE = (By.XPATH, "//button/span[text()='Update']")
    CHECK_FOR_UPDATE = (By.XPATH, "//button/span[text()='Check for update']")

class InstallerLocators(object):
    """
    A class containing the Installer
    element locators.
    """
    ACCEPT_TERMS = (By.NAME, "I accept the terms of the License Agreement")
    INSTALL = (By.NAME, "Install")
    CANCEL = (By.NAME, "Cancel")
    FINISH = (By.XPATH, "//Button[@ClassName ='Button'][@Name='Finish']")
    REBOOT_LATER = (By.NAME, "I want to manually reboot later")

    UNINSTALL_PROGRAM = (By.NAME, "Uninstall a program")
    # UNINSTALL_SEARCH = (By.NAME, "Search Box")
    UNINSTALL_SEARCH = (By.XPATH, "//*[@LocalizedControlType='edit']")  # Search Box
    LOGITECH_SYNC = (By.NAME, "Logitech Sync")
    UNINSTALL_CHANGE = (By.NAME, "Uninstall/Change")
    UNINSTALL = (By.NAME, "Uninstall")
