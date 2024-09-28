from selenium.webdriver.common.by import By

class TuneMobileNotificationLocators(object):
    """
    A class containing the Tune Mobile App Notification Screen element locators.
    """
    CLOSE = [(By.ID, "close"),
             (By.ID, "com.logitech.logue:id/close_icon")]
    CLEAR_ALL = [(By.ID, "Clear all"),
             (By.ID, "com.logitech.logue:id/btn_dismiss_all")]
    CONFIRM_CLEAR_ALL = [(By.XPATH, "//XCUIElementTypeButton[@name='Cancel']/preceding-sibling::XCUIElementTypeButton[@name='Clear all']"),
                         (By.ID, "com.logitech.logue:id/btn_dismiss_confirm")]
    CANCEL = [(By.XPATH, "//XCUIElementTypeButton[@name='Cancel']"),
              (By.ID, "com.logitech.logue:id/btn_dismiss_abort")]
    CLEAR_ALL_TEXT = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Clear all notifications?']"),
                      (By.XPATH, "//android.widget.TextView[@text='Clear all notifications?']")]
    CLEAR_ALL_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Dismissed notifications cannot be accessed later.']"),
                         (By.XPATH, "//android.widget.TextView[@text='Dismissed notifications cannot be accessed later.']")]
    SHOW_EXPIRED_NOTIFICATIONS = [(By.XPATH, "//XCUIElementTypeButton[@name='Show expired notifications']"),
                                  (By.XPATH, "//android.widget.TextView[@text='Show expired notifications']")]
    HIDE_EXPIRED_NOTIFICATIONS = [(By.ID, "Hide expired notifications"),
                                  (By.XPATH, "//android.widget.TextView[@text='Hide expired notifications']")]
    NO_NEW_NOTIFICATIONS = [(By.XPATH, "//XCUIElementTypeStaticText[@name='No active notifications']"),
                            (By.XPATH, "//android.widget.TextView[@text='No active notifications']")]
    LAMA_IMAGE = [(),
                  (By.CLASS_NAME, "android.widget.ImageView")]
    DISMISS_NOTIFICATION = [(By.ID, "clear large"),
                            (By.ID, "com.logitech.logue:id/btn_dismiss")]
    BOOK_DESK_NEARBY = [(By.XPATH, "//XCUIElementTypeButton[@label='BOOK A DESK NEARBY']"),
                        (By.XPATH, "//android.widget.Button[@text='BOOK A DESK NEARBY']")]
    REVIEW_BOOKING = [(By.XPATH, "//XCUIElementTypeButton[@label='REVIEW BOOKING']"),
                      (By.XPATH, "//android.widget.Button[@text='REVIEW BOOKING']")]
    BOOK_A_NEW_DESK = [(By.XPATH, "//XCUIElementTypeButton[@label='BOOK A NEW DESK']"),
                       (By.XPATH, "//android.widget.Button[@text='BOOK A NEW DESK']")]
    BOOK_DESK_NEARBY_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Would you like to book a desk near')]"),
                                    (By.XPATH, "//android.widget.TextView[contains(@text, 'Would you like to book a desk near')]")]
    CUSTOM_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX')]"),
                      (By.XPATH, "//android.widget.TextView[contains(@text, 'XXX')]")]
    ADMIN_BOOKED_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'A desk booking in') and contains(@label, 'made on your behalf by an administrator')]"),
                                (By.XPATH, "//android.widget.TextView[contains(@text, 'A desk booking in') and contains(@text, 'made on your behalf by an administrator')]")]
    ADMIN_CANCELLED_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Your booking on') and contains(@label, 'was cancelled by an administrator')]"),
                                   (By.XPATH, "//android.widget.TextView[contains(@text, 'Your booking on') and contains(@text, 'was cancelled by an administrator')]")]
    BOOK_NEW_DESK_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Would you like to book a new desk?')]"),
                                 (By.XPATH, "//android.widget.TextView[contains(@text, 'Would you like to book a new desk?')]")]
    ADMIN_UPDATED_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Your desk booking') and contains(@label, 'has been modified by an administrator')]"),
                                   (By.XPATH, "//android.widget.TextView[contains(@text, 'Your desk booking') and contains(@text, 'has been modified by an administrator')]")]
    REVIEW_BOOKING_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Review your updated booking and make any necessary changes')]"),
                                  (By.XPATH, "//android.widget.TextView[contains(@text, 'Review your updated booking and make any necessary changes')]")]
    MODIFY_BOOKING = [(By.XPATH, "//XCUIElementTypeButton[@label='MODIFY BOOKING']"),
                      (By.XPATH, "//android.widget.Button[@text='MODIFY BOOKING']")]
    TEAMMATE_CANCELLED_MESSAGE = [(By.XPATH,"//XCUIElementTypeStaticText[contains(@label, 'XXX cancelled their booking in')]"),
                                 (By.XPATH,"//android.widget.TextView[contains(@text, 'XXX cancelled their booking in')]")] #Pass Teammate name
    TEAMMATE_CANCELLED_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Would you like to modify your booking?']"),
                                      (By.XPATH, "//android.widget.TextView[@text='Would you like to modify your booking?']")]
    TEAMMATE_CHANGED_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'XXX changed a desk booking in')]"),
                                (By.XPATH, "//android.widget.TextView[contains(@text, 'XXX changed a desk booking in')]")]  # Pass Teammate name
    CHECK_IN_NOTIFICATION = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'You need to check-in at the desk')]"),
                             (By.XPATH, "//android.widget.TextView[contains(@text, 'You need to check-in at the desk')]")]
    CHECK_IN_DESCRIPTION = [(By.XPATH, "//XCUIElementTypeStaticText[@label='To not lose your reservation, confirm it at the desk. Need to review or change your booking?']"),
                            (By.XPATH, "//android.widget.TextView[@text='To not lose your reservation, confirm it at the desk. Need to review or change your booking?']")]