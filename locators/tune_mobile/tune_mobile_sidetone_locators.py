from selenium.webdriver.common.by import By

class TuneMobileSidetoneLocators(object):
    """
    A class containing the Tune Mobile App Sleep Settings Screen element locators.
    """
    CLOSE = [(By.ID, "sleep_settings_close_button"),
            (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]
    DONE = [(By.ID, "sidetone_done_button"),
            (By.XPATH, "//*[@text='Done']/following-sibling::android.widget.Button")]
    DONE_LABEL = [(By.XPATH, "//XCUIElementTypeButton[@label='Done']"),
                  (By.XPATH, "//*[@text='Done']")]
    SIDETONE_INFO = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Put headset on, start talking, and use slider to adjust sidetone volume of your own voice.']"),
                     (By.XPATH, "//*[@text='Put headset on, start talking, and use slider to adjust sidetone volume of your own voice.']")]
    SIDETONE_SLIDER = [(By.ID, "sidetone_slider"),
                       (By.CLASS_NAME, "android.widget.SeekBar")]
    SIDETONE_PERCENTAGE = [(By.ID, "XXX %"),
                           (By.XPATH, "//*[@content-desc='XXX% label']")]
    OK = [(By.ID, "OK"), ()]
    ALLOW = [(By.ID, "Allow"), ()]
