from selenium.webdriver.common.by import By


class SyncAppDeviceCameraLocators(object):
    """
    A class containing the Sync App Device Screen element locators.
    """
    REFER_TO_FAQ = (By.XPATH, "//a[text()='refer to our FAQs']")
    LEARN_MORE = (By.XPATH, "//a[text()='Learn more']")
    RIGHT_SIGHT_TOGGLE = (By.XPATH, "//p[contains(text(),'RightSight')]/ancestor::div[3]//input")
    RIGHT_SIGHT_TOGGLE_OFF = (By.XPATH, "//p[contains(text(),'RightSight')]/ancestor::div[3]/div/span")
    DYNAMIC_RADIO = (By.XPATH, "//p[text()='Dynamic']/parent::div/preceding-sibling::span//input")
    ON_CALL_START_RADIO = (By.XPATH, "//p[contains(text(), 'call start')]/parent::div/preceding-sibling::span//input")
    GROUP_VIEW = (By.XPATH, "//p[text()='Group View']/parent::div/preceding-sibling::span//input")
    GROUP_VIEW_NEW = (By.XPATH, "//p[text()='Group View']/parent::div")
    SPEAKER_VIEW = (By.XPATH, "//p[text()='Speaker View (Beta)']/parent::div/preceding-sibling::span//input")
    SPEAKER_VIEW_NEW = (By.XPATH, "//p[text()='Speaker View']/parent::div")
    PICTURE_IN_PICTURE_TOGGLE = (
    By.XPATH, "//p[text()='Picture In Picture']/ancestor::div[2]/preceding-sibling::div//input")

    SPEAKER_DETECTION_SLOW = (By.XPATH, "//p[text()='Speaker Detection']/following-sibling::div[3]//"
                                        "p[text()='Slower']/parent::div/preceding-sibling::span//input")
    SPEAKER_DETECTION_DEFAULT = (By.XPATH, "//p[text()='Speaker Detection']/following-sibling::div[3]//"
                                           "p[text()='Default']/parent::div/preceding-sibling::span//input")
    SPEAKER_DETECTION_FAST = (By.XPATH, "//p[text()='Speaker Detection']/following-sibling::div[3]//"
                                        "p[text()='Faster']/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_SLOW = (By.XPATH, "//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Slower']"
                                    "/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_DEFAULT = (By.XPATH, "//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Default']"
                                       "/parent::div/preceding-sibling::span//input")
    FRAMING_SPEED_FAST = (By.XPATH, "//p[text()='Framing Speed']/following-sibling::div[3]//p[text()='Faster']"
                                    "/parent::div/preceding-sibling::span//input")
    PAL_50HZ = (By.XPATH, "//p[text()='PAL 50Hz']/parent::div/preceding-sibling::span//input")
    NTSC_60HZ = (By.XPATH, "//p[text()='NTSC 60Hz']/parent::div/preceding-sibling::span//input")

    # Camera Settings
    RESET_CAMERA_ADJUSTMENTS_OLD = (By.XPATH, "//p[contains(text(),'adjustments')]/"
                                              "following-sibling::*[local-name()='svg']")
    RESET_CAMERA_ADJUSTMENTS = (By.XPATH, "//p[contains(text(),'adjustments')]/"
                                          "following-sibling::div/*[local-name()='svg']")
    RESET_MANUAL_COLOR_SETTINGS_OLD = (By.XPATH, "//p[contains(text(),'Manual color')]/"
                                                 "following-sibling::*[local-name()='svg']")
    RESET_MANUAL_COLOR_SETTINGS = (By.XPATH, "//p[contains(text(),'Manual color')]/"
                                             "following-sibling::div/*[local-name()='svg']")
    MANUAL_COLOR_SETTINGS = (By.XPATH, "//p[text()='Manual color settings']/ancestor::div[3]")
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
    BRIGHTNESS_SLIDER = (By.XPATH, "//p[text()='Brightness']/ancestor::div[2]/"
                                   "following-sibling::div//input/parent::span")
    BRIGHTNESS_SLIDER_KNOB = (By.XPATH, "//p[text()='Brightness']/ancestor::div[2]/"
                                        "following-sibling::div//input/following-sibling::span")
    CONTRAST_SLIDER = (By.XPATH, "//p[text()='Contrast']/ancestor::div[2]/"
                                 "following-sibling::div//input/parent::span")
    CONTRAST_SLIDER_KNOB = (By.XPATH, "//p[text()='Contrast']/ancestor::div[2]/"
                                      "following-sibling::div//input/following-sibling::span")
    SATURATION_SLIDER = (By.XPATH, "//p[text()='Saturation']/ancestor::div[2]/"
                                   "following-sibling::div//input/parent::span")
    SATURATION_SLIDER_KNOB = (By.XPATH, "//p[text()='Saturation']/ancestor::div[2]/"
                                        "following-sibling::div//input/following-sibling::span")
    SHARPNESS_SLIDER_KNOB = (By.XPATH, "//p[text()='Sharpness']/ancestor::div[2]/"
                                       "following-sibling::div//input/following-sibling::span")
    SHARPNESS_SLIDER = (By.XPATH, "//p[text()='Sharpness']/ancestor::div[2]/"
                                  "following-sibling::div//input/parent::span")
    GRID_BUTTON = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']")
    GRID_BUTTON_PROPERTY = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']//*[local-name()='mask']")
    GRID_LINES_VERTICAL = (By.XPATH, "//video/parent::div/following-sibling::div[1]/div")
    GRID_LINES_HORIZONTAL = (By.XPATH, "//video/parent::div/following-sibling::div[2]/div")
    VIDEO_PREVIEW_COLLAPSE = (By.XPATH, "//p[text()='Video preview']/ancestor::div[2]")
    VIDEO_PREVIEW_RESTORE = (By.XPATH, "//video/ancestor::div[2]//*[local-name()='svg']")

    # Camera Adjustments
    CAMERA_ADJUSTMENTS = (By.XPATH, "//p[text()='Camera adjustments']/ancestor::div[2]")
    AUTO_FOCUS = (By.XPATH, "//p[text()='Auto focus']/ancestor::div[3]//input")
    MANUAL_FOCUS_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual focus']/ancestor::div[3]//input/following-sibling::span")
    MANUAL_EXPOSURE_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual exposure']/ancestor::div[3]//"
                                             "input/following-sibling::span")
    MANUAL_WHITE_BALANCE_SLIDER_KNOB = (By.XPATH, "//p[text()='Manual white balance']/ancestor::div[3]//"
                                                  "input/following-sibling::span")

    # Celestia Video
    EDIT_BOUNDARIES = (By.XPATH, "//span[text()='Edit Boundaries']/parent::button")
    AUTO_CALIBRATE = (By.XPATH, "//button[1]")
    EDIT_BOUNDARIES_CANCEL = (By.XPATH, "//button[3]")
    EDIT_BOUNDARIES_CONFIRM = (By.XPATH, "//button[2]")
