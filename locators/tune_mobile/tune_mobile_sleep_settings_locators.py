from selenium.webdriver.common.by import By

class TuneMobileSleepSettingsLocators(object):
    """
    A class containing the Tune Mobile App Sleep Settings Screen element locators.
    """
    CLOSE = [(By.ID, "sleep_settings_close_button"),
            (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]
    SLEEP_MINUTES = [(By.ID, "XXX minutes"),
                     (By.XPATH, "//*[@content-desc='XXX minutes label']")]
    SLEEP_NEVER = [(By.ID, "Never"),
                   (By.XPATH, "//*[@content-desc='Never label']")]
    SLEEP_HOUR = [(By.ID, "1 hour"),
                  (By.XPATH, "//*[@content-desc='1 hour label']")]
    SLEEP_HOURS = [(By.ID, "XXX hours"),
                   (By.XPATH, "//*[@content-desc='XXX hours label']")]
    SAVE = [(By.ID, "sleep_settings_save_button"),
            (By.XPATH, "//*[@content-desc='Save Sleep Time']/following-sibling::android.widget.Button")]
    SLEEP_MINUTES_RADIO = [(By.XPATH, "//XCUIElementTypeStaticText[@label='XXX minutes']/following-sibling::XCUIElementTypeButton"),
                           (By.XPATH, "//*[@content-desc='XXX minutes label']/following-sibling::android.view.View")]
    SLEEP_NEVER_RADIO = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Never']/following-sibling::XCUIElementTypeButton"),
                         (By.XPATH, "//*[@content-desc='Never label']/following-sibling::android.view.View")]
    SLEEP_HOUR_RADIO = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX hour')]/following-sibling::XCUIElementTypeButton"),
                        (By.XPATH, "//*[contains(@content-desc, 'XXX hour')]/following-sibling::android.view.View")]


