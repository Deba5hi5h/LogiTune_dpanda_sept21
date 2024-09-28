from selenium.webdriver.common.by import By

class PhoneSettingsLocators(object):
    """
    A class containing the iOS/Android Phone settings Screen element locators.
    """
    BLUETOOTH = [(By.XPATH, "//XCUIElementTypeCell[@name='Bluetooth']/XCUIElementTypeImage"),
                 ()]
    DEVICE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX')]"),
              (By.XPATH, "//*[contains(@text, 'XXX')]")]
    DEVICE_STATUS = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX')]/following-sibling::XCUIElementTypeStaticText"),
                     (By.XPATH, "//*[contains(@text, 'XXX')]/following-sibling::android.widget.TextView")]
    DEVICE_INFO = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX')]/following-sibling::XCUIElementTypeButton"),
                   ()]
    DEVICE_DISCONNECT = [(By.ID, "Disconnect"),
                         (By.XPATH, "//android.widget.Button[@text='DISCONNECT']")]
    CONNECTED_DEVICES = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Connected']/preceding-sibling::XCUIElementTypeStaticText"),
                         (By.XPATH, "//android.widget.TextView[contains(@text, 'Connected') or contains(@text, 'Active')]/preceding-sibling::android.widget.TextView")]
    BACK_TO_BLUETOOTH = [(By.ID, "Bluetooth")]
    SEARCH = [(By.ID, "Search"),(By.ID, "com.google.android.settings.intelligence:id/open_search_view_edit_text")]
    SEARCH_BAR = [(), (By.ID, "com.android.settings:id/search_action_bar")]
    LOGITUNE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Tune']"),
                (By.XPATH, "//android.widget.TextView[@text='Tune']")]
    APPS = [(), (By.XPATH, "//android.widget.TextView[@text='Apps']")]
    NOTIFICATION_SILENT = [(), (By.XPATH, "//android.widget.TextView[@text='Silent' or @text='Deliver quietly']")]
    LANGUAGE = [(By.ID, "Language"), ()]
    ENGLISH = [(By.ID, "Default"), ()]
    SPANISH = [(By.ID, "Spanish"), ()]
    FRENCH = [(By.ID, "French"), ()]
    ITALIAN = [(By.ID, "Italian"), ()]
    GERMAN = [(By.ID, "German"), ()]
    PORTUGUESE = [(By.ID, "Portuguese"), ()]
    TUNE = [(),
            (By.XPATH, "//android.widget.TextView[@text='App info']/preceding-sibling::android.widget.TextView[@text='Tune']")]
    NOTIFICATIONS = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Notifications']"),
                     (By.XPATH, "//android.widget.TextView[@text='Notifications']")]
    LOCK_SCREEN = [(By.XPATH, "//XCUIElementTypeButton[@name='Lock Screen']"),
                   (By.ID, "com.oplus.notificationmanager:id/cb_lock_screen_notification")]
    NOTIFICATION_CENTER = [(By.XPATH, "//XCUIElementTypeButton[@name='Notification Center']"), ()]
    BANNERS = [(By.XPATH, "//XCUIElementTypeButton[@name='Banners']"),
               (By.ID, "com.oplus.notificationmanager:id/cb_banner")]
    BOOKING_CHANGES = [(),(By.XPATH, "//android.widget.Switch[@content-desc='Booking changes']")]
    BOOKING_REMINDERS = [(), (By.XPATH, "//android.widget.Switch[@content-desc='Booking reminders']")]
    CHECKIN_REQUEST = [(), (By.XPATH, "//android.widget.Switch[@content-desc='Check-in request']")]
    TEAMMATE_BOOKINGS = [(), (By.XPATH, "//android.widget.Switch[@content-desc='Teammate bookings']")]
    HEADSET_SETTINGS = [(), (By.XPATH, "//android.widget.TextView[@text='XXX']/ancestor::android.widget.LinearLayout[1]/following-sibling::android.widget.LinearLayout/android.widget.ImageView")]
    HEADSET_DISCONNECT = [(), (By.XPATH, "//android.widget.Button[@text='Disconnect']")]
    HEADSET_CONNECT = [(), (By.XPATH, "//android.widget.Button[@text='Connect']")]
    BACK = [(), (By.XPATH, "//android.widget.ImageButton[@content-desc='Back']")]
    SEE_ALL = [(), (By.XPATH, "//android.widget.TextView[@text='See all']")]
    LATER = [(By.ID, "Later"), ()]
    REMIND_ME_LATER = [(By.ID, "Remind Me Later"), ()]