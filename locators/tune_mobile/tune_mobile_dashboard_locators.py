from selenium.webdriver.common.by import By

class TuneMobileDashboardLocators(object):
    """
    A class containing the Tune Mobile App Dashboard Home Screen element locators.
    """
    PROFILE = [(By.XPATH, "//XCUIElementTypeNavigationBar/XCUIElementTypeImage"),
               (By.ID, "com.logitech.logue:id/iv_user_profile")]
    NOTIFICATION = [(By.ID, "notification"),
                    (By.ID, "com.logitech.logue:id/iv_notification_bell")]
    NOTIFICATION_UNREAD = [(By.ID, "notification unread small"),
                           (By.ID, "com.logitech.logue:id/iv_notification_bell")]
    BOOK = [(By.XPATH, "//XCUIElementTypeTabBar/XCUIElementTypeOther/XCUIElementTypeButton"),
            (By.XPATH, "//*[@content-desc='Book']")]
    BOOKING_CARD_DESK_NAME = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
                              (By.XPATH, "//android.widget.TextView[@text='XXX']")] #Pass Desk Name
    BOOKING_CARD_SCHEDULE = [(By.XPATH, "//*[@name='XXX']/ancestor:: XCUIElementTypeCell//*[@name='meeting']/following-sibling::XCUIElementTypeStaticText"),
                             (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@resource-id='com.logitech.logue:id/meeting_time']")] #Pass Desk Name
    BOOKING_CARD_LOCATION = [(By.XPATH, "(//*[@name='XXX']/ancestor::XCUIElementTypeCell//*[@name='directions']/following-sibling::XCUIElementTypeStaticText)[1]"),
                             (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@resource-id='com.logitech.logue:id/workplace']")] #Pass Desk Name
    BOOKING_CARD_DETAILS = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']/parent:: XCUIElementTypeOther/following-sibling::XCUIElementTypeButton[@name='DETAILS']"),
                            (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::android.widget.Button[@text='DETAILS']")]
    MODIFY_BOOKING_DESK_IMAGE = [(By.ID, "map-desk"),
                                 (By.ID, "com.logitech.logue:id/desk_image")]
    MODIFY_BOOKING_DESK_NAME = [(By.XPATH, "//*[@name='map-desk']/parent::*/following-sibling::*/*[@value='XXX']"),
                                (By.XPATH, "//*[@resource-id='com.logitech.logue:id/selected_reservation_id' and @text='XXX']")] #Pass Desk Name
    MODIFY_BOOKING_LOCATION = [(By.XPATH, "//*[@name='map-desk']/parent::*/following-sibling::*/*[@value='XXX']"),
                               (By.XPATH, "//*[@resource-id='com.logitech.logue:id/location' and @text='XXX']")]  # Pass Floor Area
    MODIFY_BOOKING_SCHEDULE = [(By.XPATH, "(//XCUIElementTypeStaticText[@name='XXX'])[3]"),
                               (By.XPATH, "//*[@resource-id='com.logitech.logue:id/selected_reservation_time' and @text='XXX']")]  # Pass Start -end time
    SHOW_ON_MAPS = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Show on maps']"),
                    (By.XPATH, "//android.widget.TextView[@text='Show on map']")]
    TEAMMATES_NEAR_BY = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Teammates nearby']"),
                         (By.XPATH, "//android.widget.TextView[@text='Teammates nearby']")]
    EDIT_BOOKING = [(By.XPATH, "//XCUIElementTypeButton[@name='Edit booking']"),
                    (By.XPATH, "//android.widget.TextView[@text='Edit booking']")]
    NOTIFY_TEAMMATES = [(By.ID, "Notify teammates"),
                        (By.ID, "com.logitech.logue:id/tv_notify_teammates")]
    CANCEL_SESSION = [(By.XPATH, "//XCUIElementTypeButton[@name='Cancel session']"),
                      (By.XPATH, "//android.widget.TextView[@text='Cancel session']")]
    END_SESSION = [(By.XPATH, "//XCUIElementTypeButton[@name='End session']"),
                   (By.XPATH, "//android.widget.TextView[@text='End session']")]
    CANCEL_SESSION_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[starts-with(@value,'Cancel your booking of')]"),
                              (By.XPATH, "//android.widget.TextView[@text='Cancel your booking of the desk?']")]
    END_SESSION_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[starts-with(@value,'End your booking of')]"),
                           (By.XPATH, "//android.widget.TextView[starts-with(@text,'End your booking of')]")]
    RELEASE_DESK_MESSAE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='This will release your desk']"),
                           (By.XPATH, "//android.widget.TextView[@text='This will release your desk']")]
    YES_END = [(By.XPATH, "//XCUIElementTypeButton[@name='Yes, end']"),
               (By.XPATH, "//android.widget.Button[@text='Yes, end']")]
    YES_CANCEL = [(By.XPATH, "//XCUIElementTypeButton[@name='Yes, cancel']"),
                  (By.XPATH, "//android.widget.Button[@text='Yes, cancel']")]
    NO_KEEP = [(By.XPATH, "//XCUIElementTypeButton[@name='No, keep']"),
               (By.XPATH, "//android.widget.Button[@text='No, keep']")]
    CLOSE_BOTTOM_SHEET = [(By.XPATH, "//XCUIElementTypeImage[@name='map-desk']/ancestor::XCUIElementTypeOther/preceding-sibling::XCUIElementTypeButton"),
                          (By.ID, "com.logitech.logue:id/button_close")]
    BOOKING_CANCELLED_CONFIRMATION = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Booking cancelled']"),
                                      (By.XPATH, "//android.widget.TextView[@text='Booking cancelled']")]
    BOOKING_CANCELLED_MESSAGE = [(By.ID, "You're all set!"),
                                 (By.XPATH, "//android.widget.TextView[@text='You’re all set!']")]
    OK = [(By.XPATH, "//XCUIElementTypeButton[@name='OK']"),
          (By.XPATH, "//android.widget.Button[@text='OK']")]
    PEOPLE = [(By.XPATH, "//XCUIElementTypeButton[@name='People']"),
              (By.XPATH, "//*[@content-desc='People']")]
    # PEOPLE = [(By.ID, "People"),
    #           (By.XPATH, "//*[@content-desc='People']")]
    MAPS = [(By.ID, "Maps"),
            (By.XPATH, "//*[@content-desc='Map']")]
    HOME = [(By.ID, "Home"),
            (By.XPATH, "//*[@content-desc='Home']")]
    BUILDING = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, '% occupied')]"),
                (By.ID, "com.logitech.logue:id/tv_occupancy")]
    DATE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
            (By.XPATH, "//*[@resource-id='com.logitech.logue:id/txt_date' and @text='XXX']")]
    EXPAND_CALENDAR = [(By.XPATH, "//XCUIElementTypeButton[@name=' ']/parent::XCUIElementTypeOther/parent::XCUIElementTypeOther/preceding-sibling::XCUIElementTypeOther//XCUIElementTypeButton"),
                       (By.ID, "com.logitech.logue:id/iv_icon_calendar_button")]
    TEAMMATES_IN_OFFICE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@value, '% occupied')]/following-sibling::XCUIElementTypeStaticText"),
                           (By.ID, "com.logitech.logue:id/tv_office_name")]



