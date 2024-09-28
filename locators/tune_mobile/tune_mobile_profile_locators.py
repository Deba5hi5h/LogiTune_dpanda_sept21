from selenium.webdriver.common.by import By

class TuneMobileProfileLocators(object):
    """
    A class containing the Tune Mobile App Profile Screen element locators.
    """
    WORK_ACCOUNT = [(By.ID, "Work account"),
                    (By.ID, "com.logitech.logue:id/tv_work_account")]
    DISCONNECT = [(By.XPATH, "//XCUIElementTypeButton[@name='Disconnect']"),
                  (By.ID, "com.logitech.logue:id/button_disconnect")]
    CONFIRM_DISCONNECT = [(By.XPATH, "//XCUIElementTypeButton[@name='Cancel']/preceding-sibling::XCUIElementTypeButton"),
                          (By.ID, "com.logitech.logue:id/btn_dismiss_confirm")]
    GOOGLE_CALENDAR = [(By.ID, "Google Calendar"),
                       (By.ID, "com.logitech.logue:id/work_account_name")]
    O365_CALENDAR = [(By.ID, "Office 365 Calendar"),
                     (By.XPATH, "//android.widget.TextView[@text='Office 365 Calendar']")]
    CONNECTED = [(By.ID, "Connected"),
                 (By.ID, "com.logitech.logue:id/label_connected")]
    DISCONNECT_WORK_ACCOUNT = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Disconnect work account?']"),
                               (By.XPATH, "//android.widget.TextView[@text='Disconnect work account?']")]
    FEATURE_UNAVAILABLE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Desk booking feature will be unavaliable']"),
                           (By.XPATH, "//android.widget.TextView[@text='Desk booking feature will be unavaliable']")]
    CANCEL = [(By.XPATH, "//XCUIElementTypeButton[@label='Cancel']"),
              (By.ID, "com.logitech.logue:id/btn_dismiss_abort")]