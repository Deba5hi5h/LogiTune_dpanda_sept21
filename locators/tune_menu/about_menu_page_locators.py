from selenium.webdriver.common.by import By


class AboutMenuPageLocators(object):
    """
    A class containing the Tune menu "About page" element locators.
    """

    # About page
    PAGE_TITLE = (By.XPATH, "//p[text()='About']")

    APP_VERSION = (By.XPATH, "//p[text()[contains(., 'Logi Tune')]]")
