from selenium.webdriver.common.by import By


class LNAHomeLocators(object):
    """
    A class containing the Local Network Access Home page
    element locators.
    """
    LOCAL_NETWORK_LABEL = (By.XPATH, "//span[contains(text(),'Local Network Access')]")

    SYNC = (By.XPATH, "//a[contains(@href, 'sync')]//*[text()='Sync']")
    UPDATES = (By.XPATH, "//a[contains(@href, 'updates')]//*[text()='Updates']")
    DISPLAY_AUDIO = (By.XPATH, "//a[contains(@href, 'display')]//*[text()='Display and Audio']")
    CAMERA = (By.XPATH, "//a[contains(@href, 'camera')]//*[text()='Camera']")
    CONNECTIVITY = (By.XPATH, "//a[contains(@href, 'connectivity')]//*[text()='Connectivity']")
    PERIPHERALS = (By.XPATH, "//a[contains(@href, 'peripherals')]//*[text()='Peripherals']")
    SYSTEM = (By.XPATH, "//a[contains(@href, 'system')]//*[text()='System']")
    ABOUT = (By.XPATH, "//a[contains(@href, 'about')]//*[text()='About']")
