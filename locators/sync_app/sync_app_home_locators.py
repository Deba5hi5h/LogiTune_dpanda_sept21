from selenium.webdriver.common.by import By


class SyncAppHomeLocators(object):
    """
    A class containing the Sync App Home Screen element locators.
    """
    # Sync Menu and Menu items
    MENU = (By.XPATH, "//*[local-name()='svg']//*[local-name()='circle']/following-sibling::*[local-name()='circle']/"
                      "following-sibling::*[local-name()='circle']/ancestor::*[local-name()='svg']")
    RENAME_ROOM = (By.XPATH, "//li[text()='Rename Room']")
    UPDATES_AND_ABOUT = (By.XPATH, "//li[text()='Updates and About']")
    ABOUT = (By.XPATH, "//*[@Name='About Logitech Sync']")
    ABOUT_LOGITECH_SYNC = (By.XPATH, "//li[text()='About Logitech Sync']")
    ROOM_SYNC_UPDATE = (By.XPATH, "//button/span[text()='Update']")
    CHECK_FOR_UPDATE = (By.XPATH, "//button/span[text()='Check for update']")
    UPDATE_NOW = (By.XPATH, "//button/span[text()='Update Now' or text()='Update now']")

    # Sync Room in Header
    ROOM_EDIT_BOX = (By.XPATH, "//input[@maxlength='63']")
    ROOM_NAME = (By.XPATH, "//div/span/following-sibling::span/preceding-sibling::span")

    # Left Navigation
    ROOM = (By.XPATH, "//p[text()='Room']/following-sibling::div/*[local-name()='svg']"
                      "/parent::div/preceding-sibling::p")
    DEVICE_NAME = (By.XPATH, "//div[contains(@class, 'align')]/p[text()='XXX']")
    DEVICE_AUDIO = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//"
                              "following-sibling::div/p[text()='Audio']")  # Pass Device Name
    DEVICE_CAMERA = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//"
                               "following-sibling::div/p[text()='Camera']/parent::div")  # Pass Device Name
    DEVICE_CONNECTIVITY = (By.XPATH, "//p[text()='XXX']/parent::div/parent::div//"
                                     "following-sibling::div/p[text()='Connectivity']/parent::div")  # Pass Device Name
    ADD_DEVICE = (By.XPATH, "//*[text()='Add Device']")
    UI_NODES = (By.XPATH, "//div[contains(@class, 'align')]/p")
