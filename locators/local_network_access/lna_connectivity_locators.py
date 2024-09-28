from selenium.webdriver.common.by import By


class LNAConnectivityLocators(object):
    """
    A class containing the Local Network Access Connectivity page
    element locators.
    """
    BLUETOOTH = (By.XPATH, "//button//*[text()='Bluetooth']")
    BLUETOOTH_EXPAND = (By.XPATH, "//*[text()='Bluetooth']/ancestor::button[contains(@class, 'triggerRoot')]")
    BLUETOOTH_CHECKBOX = (By.XPATH, "//*[text()='Bluetooth connection']/following-sibling::input")
    BUTTON_APPLY = (By.XPATH, "//button[text()='Apply']")
