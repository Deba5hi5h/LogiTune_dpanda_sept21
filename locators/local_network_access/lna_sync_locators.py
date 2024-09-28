from selenium.webdriver.common.by import By


class LNASyncLocators(object):
    """
    A class containing the Local Network Access Sync page
    element locators.
    """
    CONNECTION_EXPAND = (By.XPATH, "//*[text()='Connection']/ancestor::button[contains(@class, 'triggerRoot')]")
    CONNECT_TO_SYNC = (By.XPATH, "//button[text()='Connect to Sync']")
    SYNC_PROVISION_CODE_INPUT = (By.XPATH, "//input[@data-testid='provision-code-input']")
    CONTINUE = (By.XPATH, "//button[text()='Continue']")
    SEAT_COUNT = (By.XPATH, "//input[@id='seatCount']")
    SKIP_THIS_STEP = (By.XPATH, "//button[text()='Skip this step']")
    SUBMIT = (By.XPATH, "//button[text()='Submit']")
    DISCONNECT_FROM_SYNC = (By.XPATH, "//button[text()='Disconnect from Sync']")
    ROOM_INFORMATION_EXPAND = (
    By.XPATH, "//*[text()='Room Information']/ancestor::button[contains(@class, 'triggerRoot')]")
    ROOM_NAME_VALUE = (By.XPATH, "//span[contains(@data-testid, 'roomName')]")
    SEAT_COUNT_VALUE = (By.XPATH, "//span[contains(@data-testid, 'seatCount')]")
