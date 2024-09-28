from selenium.webdriver.common.by import By


class LNACameraLocators(object):
    """
    A class containing the Local Network Access Camera page
    element locators.
    """
    RIGHTSIGHT = (By.XPATH, "//button//*[text()='RightSight 2']")
    RIGHTSIGHT_EXPAND = (By.XPATH, "//*[text()='RightSight 2']/ancestor::button[contains(@class, 'triggerRoot')]")
    RIGHTSIGHT_CHECKBOX = (By.XPATH, "//*[text()='RightSight 2']/input")
    RIGHTSIGHT_TOGGLE = (By.XPATH, "//*[text()='RightSight 2']/span")
    GROUP_VIEW = (By.XPATH, "//input[@id='Group View']")
    SPEAKER_VIEW = (By.XPATH, "//input[@id='settings.camera.rightSight.speakerView']")
    PICTURE_IN_PICTURE = (By.XPATH, "//*[text()='Picture-in-picture']/following-sibling::span")
    ROOM_OCCUPANCY = (By.XPATH, "//button//*[text()='Room occupancy']")
    ROOM_OCCUPANCY_EXPAND = (By.XPATH, "//*[text()='Room occupancy']/ancestor::button[contains(@class, 'triggerRoot')]")
