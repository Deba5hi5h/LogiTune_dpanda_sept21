from selenium.webdriver.common.by import By


class SyncAppDeviceConnectivityLocators(object):
    """
    A class containing the Sync App Device Screen element locators.
    """
    BLUETOOTH = (By.XPATH, "//p[text()='Enable']/parent::div/ancestor::div[2]//input")
