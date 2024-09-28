from selenium.webdriver.common.by import By

class TuneMobileDeviceNameLocators(object):
    """
    A class containing the Tune Mobile App Device Name Screen element locators.
    """
    CLOSE = [(By.ID, "close_button"),
             (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]
    DEVICE_NAME_TEXTFIELD = [(By.ID, "device_name_textfield"),
                             (By.XPATH, "//android.widget.EditText")]
    HEADSET_ICON = [(By.ID, "headset-overear"),
                    (By.XPATH, "//*[@content-desc='Headset Name']")]
    SURPRISE_ME = [(By.ID, "surprise_me_button"),
                   (By.XPATH, "//*[@content-desc='Surprise me label']")]
    UPDATE = [(By.ID, "update_device_name_button"),
              (By.XPATH, "//*[@text='Update']/following-sibling::android.widget.Button")]


