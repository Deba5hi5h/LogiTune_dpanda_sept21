from selenium.webdriver.common.by import By


class SyncAppDeviceLocators(object):
    """
    A class containing the Sync App Device Screen element locators.
    """
    KEBAB = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']"
                       "/following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']")  # 2nd item
    INFO = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']"
                      "/following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']"
                      "/preceding-sibling::*[local-name()='svg']")
    # Device Information
    PID = (By.XPATH, "//p[text()='PID']/parent::div/following-sibling::div/p")
    BLE_FIRMWARE_RALLY_CAM = (By.XPATH, "//p[text()='BLE Firmware']/parent::div/following-sibling::div/child::p[2]")
    EEPROM_FIRMWARE_RALLY_CAM = (By.XPATH, "//p[text()='EEPROM Firmware']/parent::div/following-sibling::div/child"
                                           "::p[3]")
    VIDEO_FIRMWARE_RALLY_CAM = (By.XPATH, "//p[text()='Video Firmware']/parent::div/following-sibling::div/child::p[4]")
    AUDIO_FIRMWARE = (By.XPATH, "//p[text()='Audio Firmware']/parent::div/following-sibling::div/child::p[2]")
    BLE_FIRMWARE = (By.XPATH, "//p[text()='BLE Firmware']/parent::div/following-sibling::div/child::p[3]")
    CODEC_FIRMWARE = (By.XPATH, "//p[text()='Codec Firmware']/parent::div/following-sibling::div/child::p[4]")
    EEPROM_FIRMWARE = (By.XPATH, "//p[text()='EEPROM Firmware']/parent::div/following-sibling::div/child::p[5]")
    VIDEO_FIRMWARE = (By.XPATH, "//p[text()='Video Firmware']/parent::div/following-sibling::div/child::p[6]")
    SERIAL_NUMBER = (By.XPATH, "//p[text()='Serial Number']/following-sibling::p")
    LOGI_COLLABOS = (By.XPATH, "//p[text()='Logi CollabOS']/following-sibling::p")
    FIRMWARE_VERSION = (By.XPATH, "//p[text()='Firmware Version']/following-sibling::p")
    SYSTEM_IMAGE = (By.XPATH, "//p[text()='System Image']/following-sibling::p")
    AUDIO = (By.XPATH, "//p[text()='Audio']/following-sibling::p")
    HOUSEKEEPING = (By.XPATH, "//p[text()='Housekeeping']/following-sibling::p")
    ZOOM_FOCUS = (By.XPATH, "//p[text()='Zoom & Focus']/following-sibling::p")
    PAN_TILT = (By.XPATH, "//p[text()='Pan & Tilt']/following-sibling::p")

    # Kebab Options
    CHECK_FOR_DEVICE_UPDATE = (By.XPATH, "//li[text()='Check for Device Update']")
    FORGET_DEVICE = (By.XPATH, "//li[text()='Forget Device']")
    REMOVE_PROBLEM_DEVICE = (By.NAME, "REMOVE A PROBLEM DEVICE")
    QUICK_START_GUIDE = (By.XPATH, "//li[text()='Quick Start Guide']")
    SETUP_VIDEO = (By.XPATH, "//li[text()='Setup Video']")
    PRODUCT_SUPPORT = (By.XPATH, "//li[text()='Product Support']")
    ORDER_SPARE_PARTS = (By.XPATH, "//li[text()='Order Spare Parts']")

    # Device Messages
    DEVICE_ERROR_MESSAGE = (By.XPATH, "//*[text()='There was a problem connecting to XXX.']")  # Pass Device Name
    DEVICE_CONNECT_MESSAGE = (By.XPATH, "//*[text()='XXX has been connected.']")  # Pass Device Name
    DEVICE_DISCONNECT_MESSAGE = (By.XPATH, "//*[text()='XXX has been forgotten.']")  # Pass Device Name
    SWYTCH_CONNECTED_TO_EXTERNAL_PC = (By.XPATH, "//*[text()='Swytch is connected to an external computer']")
    SWYTCH_BYOD_DEVICE_STATUS = (By.XPATH, "//*[text()='Status unknown since the device has been "
                                           "connected to an external computer']")
    SWYTCH_BYOD_DEVICE_SETTINGS = (By.XPATH, "//*[text()='Settings can not be modified now since the device "
                                             "has been connected to an external computer']")

    # Device Forget
    LETS_FIX_IT = (By.XPATH, "//button/span[text()=\"Let's Fix It\"]")
    FORGET = (By.XPATH, "//button/span[text()='Forget']")
    FORGET_NOW = (By.XPATH, "//button/span[text()='Forget Now']")

    # Device FW Update
    UPDATE_AVAILABLE = (By.XPATH, "//p[text()='Firmware update available.']")
    UPDATE_FAILED = (By.XPATH, "//p[text()='Update failed.']")
    UPDATE = (By.XPATH, "//button/span[text()='Update']")
    UPDATE_NOW = (By.XPATH, "//button/span[text()='Update Now' or text()='Update now']")
    SCHEDULE_UPDATE = (By.XPATH, "//button/span[text()='Schedule Update']")
    BACK = (By.XPATH, "//button/span[text()='Back']")
    DEVICE_UPDATE_MESSAGE = (By.XPATH, "//*[text()='XXX is up to date.']")  # Pass Device Name
    DEVICE_UPDATE_SUCCESS_MESSAGE = (By.XPATH, "//*[text()='XXX successfully updated']")  # Pass Device Name
