from selenium.webdriver.common.by import By

class TuneMobileVoicePromptsLocators(object):
    """
    A class containing the Tune Mobile App Voice Prompts Screen element locators.
    """
    CLOSE = [(By.ID, "close_button"),
            (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]

