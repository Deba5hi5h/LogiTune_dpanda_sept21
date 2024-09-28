from selenium.webdriver.common.by import By

class TuneMobileAdvancedCallClarityLocators(object):
    """
    A class containing the Tune Mobile App Advanced call clarity Screen element locators.
    """
    CLOSE = [(By.ID, "close_button"),
            (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]

