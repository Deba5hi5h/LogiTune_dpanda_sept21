from selenium.webdriver.common.by import By

class SyncPortalLoginLocators(object):
    """
    A class containing the Sync Portal Login Page
    element locators.
    """
    USERNAME = (By.XPATH, "//input[@name='username']")
    PASSWORD = (By.XPATH, "//input[@name='password']")
    LOGIN = (By.XPATH, "//button[text()='Login' and @type='submit']")
    API = (By.XPATH, "//pre")