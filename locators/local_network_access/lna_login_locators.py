from selenium.webdriver.common.by import By


class LNALoginLocators(object):
    """
    A class containing the Local Network Access Login
    element locators.
    """
    # SECURITY_ADVANCED = (By.ID, "details-button")
    # SECURITY_PROCEED = (By.ID, "proceed-link")
    SECURITY_ADVANCED = (By.ID, "advancedButton")
    SECURITY_PROCEED = (By.ID, "exceptionDialogButton")

    USER_NAME = (By.XPATH, "//input[@name='username']")
    PASSWORD = (By.XPATH, "//input[@name='password']")
    LOGIN = (By.XPATH, "//button[text()='Login' and @type='submit']")
