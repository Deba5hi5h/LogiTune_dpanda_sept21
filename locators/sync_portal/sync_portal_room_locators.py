from selenium.webdriver.common.by import By


class SyncPortalRoomLocators(object):
    """
    A class containing the Sync Portal Room Page
    element locators.
    """
    DEVICE_NAME = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='XXX']")  # Pass Device Name
    DEVICE_AUDIO = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='XXX']//ancestor::li//"
                              "following-sibling::a/div/div[text()='Audio']")  # Pass Device Name

    DEVICE_CONNECTIVITY = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='XXX']//ancestor::li//"
                                     "following-sibling::a/div/div[text()='Connectivity']")  # Pass Device Name
    DEVICE_CAMERA = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='XXX']//ancestor::li//"
                               "following-sibling::a/div/div[text()='Camera']")  # Pass Device Name
    LEFT_NAV_DEVICE = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='XXX']")  # Pass Device Name
    COMPUTER = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='Computer']")
    PAL_50HZ = (By.XPATH, "//input[@data-testid='antiflicker.pal']")
    NTSC_60HZ = (By.XPATH, "//input[@data-testid='antiflicker.ntsc']")
    # PAL_50HZ = (By.XPATH, "//label[text()='PAL 50Hz']/ancestor::div/input")
    # NTSC_60HZ = (By.XPATH, "//label[text()='NTSC 60Hz']/ancestor::div/input")
    BLUETOOTH = (By.XPATH, "//div[contains(@class, 'Switch')]")
    BLUETOOTH_STATUS = (By.XPATH, "//div[contains(@class, 'Switch')]//*[local-name()='rect']")
    BLUETOOTH_SUCCESS_MESSAGE = (By.XPATH, "//div[text()='Bluetooth updated']")
    # Audio
    SPEAKER_BOOST = (By.XPATH, "//p[contains(text(), 'maximum volume')]/following-sibling::"
                               "div[contains(@class, 'Switch')]")
    SPEAKER_BOOST_STATUS = (By.XPATH, "//p[contains(text(), 'maximum volume')]/following-sibling::"
                                      "div[contains(@class, 'Switch')]//*[local-name()='rect']")
    AI_NOISE_SUPPRESSION = (By.XPATH, "//p[contains(text(), 'unwanted noise')]/following-sibling::"
                                      "div[contains(@class, 'Switch')]")
    AI_NOISE_SUPPRESSION_STATUS = (By.XPATH, "//p[contains(text(), 'unwanted noise')]/following-sibling::"
                                             "div[contains(@class, 'Switch')]//*[local-name()='rect']")
    # REVERB_CONTROL_DISABLED = (By.XPATH, "//p[contains(text(),'control echo')]/parent::div//input[@name='disabled']")
    REVERB_CONTROL_DISABLED = (By.XPATH, "//input[@data-testid='reverb_control.disabled']")
    # REVERB_CONTROL_NORMAL = (By.XPATH, "//p[contains(text(),'control echo')]/parent::div//input[@name='normal']")
    REVERB_CONTROL_NORMAL = (By.XPATH, "//input[@data-testid='reverb_control.normal']")
    # REVERB_CONTROL_AGGRESSIVE = (By.XPATH, "//p[contains(text(),'control echo')]/"
    #                                        "parent::div//input[@name='aggressive']")
    REVERB_CONTROL_AGGRESSIVE = (By.XPATH, "//input[@data-testid='reverb_control.aggressive']")
    SETTINGS_SUCCESS_MESSAGE = (By.XPATH, "//div[text()='Settings updated']")
    # MICROPHONE_BASS_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/parent::div/following-sibling::"
    #                                    "div[4]//input[@name='bassBoost']")
    MICROPHONE_BASS_BOOST = (By.XPATH, "//input[@data-testid='microphone_eq.bass_boost']")
    # MICROPHONE_NORMAL = (By.XPATH, "//p[text()='Microphone EQ']/parent::div/following-sibling::"
    #                                "div[4]//input[@name='normal']")
    MICROPHONE_NORMAL = (By.XPATH, "//input[@data-testid='microphone_eq.normal']")
    # MICROPHONE_VOICE_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/parent::div/following-sibling::"
    #                                     "div[4]//input[@name='voiceBoost']")
    MICROPHONE_VOICE_BOOST = (By.XPATH, "//input[@data-testid='microphone_eq.voice_boost']")
    # SPEAKER_BASS_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/parent::div/following-sibling::"
    #                                 "div[4]//input[@name='bassBoost']")
    SPEAKER_BASS_BOOST = (By.XPATH, "//input[@data-testid='speaker_eq.bass_boost']")
    # SPEAKER_NORMAL = (By.XPATH, "//p[text()='Speaker EQ']/parent::div/following-sibling::"
    #                             "div[4]//input[@name='normal']")
    SPEAKER_NORMAL = (By.XPATH, "//input[@data-testid='speaker_eq.normal']")
    # SPEAKER_VOICE_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/parent::div/following-sibling::"
    #                                  "div[4]//input[@name='voiceBoost']")
    SPEAKER_VOICE_BOOST = (By.XPATH, "//input[@data-testid='speaker_eq.voice_boost']")
    LETS_FIX_IT = (By.XPATH, "//a[text()='LET’S FIX IT']")
    FORGET = (By.XPATH, "//button[text()='Forget']")
    FORGET_NOW = (By.XPATH, "//button[text()='Forget Now']")
    DEVICE_FORGET_MESSAGE = (By.XPATH, "//*[text()='Device forgotten']")
    # Camera
    RIGHTSIGHT = (By.XPATH, "//p[text()='RightSight']/following-sibling::div[4]/div[contains(@class, 'Switch')]")
    RIGHTSIGHT_STATUS = (By.XPATH, "//p[text()='RightSight']/following-sibling::div[4]/"
                                   "div[contains(@class, 'Switch')]//*[local-name()='rect']")
    RIGHTSIGHT2 = (By.XPATH, "//p[text()='RightSight 2']/following-sibling::div[6]/div[contains(@class, 'Switch')]")
    RIGHTSIGHT2_STATUS = (By.XPATH, "//p[text()='RightSight 2']/following-sibling::div[6]/"
                                    "div[contains(@class, 'Switch')]//*[local-name()='rect']")
    GROUP_VIEW = (By.XPATH, "//p[text()='Group View']/ancestor::div[2]")
    SPEAKER_VIEW = (By.XPATH, "//p[text()='Speaker View']/ancestor::div[2]")
    ENABLE_BUTTON = (By.XPATH, "//button[text()='Enable']")
    PICTURE_IN_PICTURE = (By.XPATH, "//p[text()='Picture In Picture']/parent::div/preceding-sibling::div")
    PICTURE_IN_PICTURE_STATUS = (By.XPATH, "//p[text()='Picture In Picture']/parent::div/"
                                           "preceding-sibling::div//*[local-name()='rect']")
    RIGHTSIGHT_SUCCESS_MESSAGE = (By.XPATH, "//div[text()='RightSight setting updated.']")

    SPEAKER_DETECTION_SLOW = (By.XPATH, "//p[text()='Speaker Detection']/parent::div//input[@name='slow']")
    SPEAKER_DETECTION_DEFAULT = (By.XPATH, "//p[text()='Speaker Detection']/parent::div//input[@name='default']")
    SPEAKER_DETECTION_FAST = (By.XPATH, "//p[text()='Speaker Detection']/parent::div//input[@name='fast']")
    FRAMING_SPEED_SLOW = (By.XPATH, "//p[text()='Framing Speed']/parent::div//input[@name='slow']")
    FRAMING_SPEED_DEFAULT = (By.XPATH, "//p[text()='Framing Speed']/parent::div//input[@name='default']")
    FRAMING_SPEED_FAST = (By.XPATH, "//p[text()='Framing Speed']/parent::div//input[@name='fast']")

    PROVISION_TAB = (By.XPATH, "//a[text()='Provision']")
    PROVISION_CODE = (By.XPATH, "//div[contains(@class, 'ProvisionCode__CodeContainer')]/h3")
    INFO_ICON = (By.XPATH, "//div[contains(@class,'IconButton')]")  # position 1
    MENU_ICON = (By.XPATH, "//div[contains(@class,'IconButton')]")  # position 2
    MENU_PROVISION_CODE = (By.XPATH, "//a[text()='Room provisioning code']")

    MENU_ITEM = (By.XPATH, "//p[text()='XXX']/parent::td/following-sibling::td/p") # Pass Menu item name
    ROOT = (By.XPATH, "//div[@id='root']")
    FIRMWARE_UPDATE_AVAILABLE = (By.XPATH, "//span[text()='Firmware update available.']")

    ROOM_CHECKBOX = (By.XPATH, "//div[text()='XXX']/ancestor::div[@role='gridcell']/preceding-sibling::div")
    DELETE_BUTTON = (By.XPATH, "//p[text()='Delete']")
    CONFIRM_DELETE_TEXTBOX = (By.XPATH, "//input[@id='textToConfirm']")
    CONFIRM_DELETE_YES = (By.XPATH, "//button[text()='Confirm and Delete']")
    CONFIRM_DELETE_CANCEL = (By.XPATH, "//button[text()='Cancel']")
    DELETE_SUCCESS_MESSAGE = (By.XPATH, "//div[text()='Room deleted successfully']")

    SWYTCH_CONNECTED_TO_EXTERNAL_PC = (By.XPATH, "//*[text()='Swytch is connected to an external computer']")
    SWYTCH_BYOD_DEVICE_STATUS = (By.XPATH, "//*[text()='Status unknown since the device has been "
                                           "connected to an external computer']")
    SWYTCH_BYOD_DEVICE_SETTINGS = (By.XPATH,"//*[text()='Settings can not be modified now since the device "
                                            "has been connected to an external computer']")
    CLOSE_BUTTON = (By.XPATH, "//a[@data-testid='room.back_link']")
    ADD_COLLABOS_DEVICE = (By.XPATH, "//img[@alt='CollabOS']")
