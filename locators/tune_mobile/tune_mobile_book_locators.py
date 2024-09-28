from selenium.webdriver.common.by import By

class TuneMobileBookLocators(object):
    """
    A class containing the Tune Mobile App Home Screen element locators.
    """
    BY_LOCATION_AND_PREFERENCES = [(By.XPATH, "//XCUIElementTypeImage[@name='location-and-preferences']"),
                                   (By.ID, "com.logitech.logue:id/location_pref")]
    NEAR_TEAMMATE = [(By.XPATH, "//XCUIElementTypeImage[@name='near-teammate']"),
                     (By.ID, "com.logitech.logue:id/near_teammate_text")]
    SCHEDULE = [(By.ID, "schedule"),
                (By.XPATH, "")]
    START_TIME = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Time starts']/following-sibling::XCUIElementTypeStaticText"),
                  (By.XPATH, "")]
    START_HOUR = [(By.XPATH, "//XCUIElementTypePickerWheel[2]"),
                  (By.XPATH, "")]
    START_MINUTE = [(By.XPATH, "//XCUIElementTypePickerWheel[3]"),
                    (By.XPATH, "")]
    START_AMPM = [(By.XPATH, "//XCUIElementTypePickerWheel[4]"),
                  (By.XPATH, "")]
    END_TIME = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Time ends']/following-sibling::XCUIElementTypeStaticText"),
                (By.XPATH, "")]
    END_HOUR = [(By.XPATH, "//XCUIElementTypePickerWheel[1]"),
                (By.XPATH, "")]
    END_MINUTE = [(By.XPATH, "//XCUIElementTypePickerWheel[2]"),
                  (By.XPATH, "")]
    END_AMPM = [(By.XPATH, "//XCUIElementTypePickerWheel[3]"),
                (By.XPATH, "")]
    LOCATION = [(By.ID, "location"),
                (By.XPATH, "")]
    FLOOR = [(By.ID, "stairs"),
             (By.ID, "com.logitech.logue:id/floor_info_layout")]
    OK = [(By.XPATH, "//XCUIElementTypeButton[@label='OK']"),
             (By.XPATH, "//android.widget.Button[@text='OK']")]
    BUILDING = [(By.ID, "building"),
                (By.ID, "com.logitech.logue:id/building_info_layout")]
    AREA = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'XXX')]"),
            (By.XPATH, "//android.widget.TextView[contains(@text,'XXX')]")]
    DESK = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
            (By.XPATH, "//*[@resource-id='com.logitech.logue:id/desk_name' and @text='XXX']")]
    WORKSPACE = [(By.XPATH, "//XCUIElementTypeStaticText[starts-with(@name,'XXX')]"),
                 (By.XPATH, "//android.widget.TextView[starts-with(@text,'XXX')]")]
    WORKSPACE_BY_DESK = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']/parent::XCUIElementTypeCell/preceding-sibling::XCUIElementTypeOther"),
                         (By.XPATH, "//*[@resource-id='com.logitech.logue:id/desk_name' and @text='XXX']/parent::android.view.ViewGroup/preceding-sibling::android.view.ViewGroup/android.widget.TextView")]
    BUILDING_NAME = [(By.XPATH, "//XCUIElementTypeImage[@name='building']/following-sibling::XCUIElementTypeStaticText"),
                     (By.ID, "com.logitech.logue:id/selected_building_name")]
    FLOOR_NAME = [(By.XPATH, "//XCUIElementTypeImage[@name='stairs']/following-sibling::XCUIElementTypeStaticText"),
                  (By.ID, "com.logitech.logue:id/selected_floor_name")]
    BOOK = [(By.XPATH, "//XCUIElementTypeButton[@name='Book']"),
            (By.ID, "com.logitech.logue:id/book_desk_button")]
    DONE = [(By.XPATH, "//XCUIElementTypeButton[@name='Done']"),
            (By.ID, "com.logitech.logue:id/success_button_done")]
    START_KNOB = [(By.XPATH, "(//XCUIElementTypeImage)[1]"),
                  ()]
    END_KNOB = [(By.XPATH, "(//XCUIElementTypeImage)[2]"),
                ()]
    CALENDAR_ICON = [(By.ID, "profile_calendar"),
                     (By.ID, "com.logitech.logue:id/book_desk_button_start_time")]
    CURRENT_SCHEDULE = [(By.XPATH, "//XCUIElementTypeImage/parent::XCUIElementTypeOther/preceding-sibling::XCUIElementTypeOther/XCUIElementTypeStaticText"),
                        ()]
    BOOKING_START = [(By.XPATH, "//XCUIElementTypeImage[@name='profile_calendar']/following-sibling:: XCUIElementTypeStaticText"),
                     (By.ID, "com.logitech.logue:id/book_desk_button_start_time")]
    BOOKING_END = [(By.XPATH, "//XCUIElementTypeImage[@name='profile_calendar']/following-sibling:: XCUIElementTypeStaticText"),
                   (By.ID, "com.logitech.logue:id/book_desk_button_end_time")]
    DATE = [(By.XPATH, "//XCUIElementTypeButton[@name='XXX']"),
            (By.XPATH, "//*[@resource-id='com.logitech.logue:id/txt_date' and @text='XXX']")]
    CONFIRM = [(By.XPATH, "//XCUIElementTypeButton[@label='Confirm']"),
               ()]
    UPDATE_BOOKING = [(By.XPATH, "//XCUIElementTypeButton[@label='Update booking']"),
                      (By.XPATH, "//android.widget.Button[@text='Update booking']")]
    BOOKING_UPDATED = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Booking updated']"),
                       (By.XPATH, "//android.widget.TextView[@text='Booking updated']")]
    EDIT_BOOKING = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Edit booking']"),
                    (By.XPATH, "//android.widget.TextView[@text='Edit booking']")]
    BOOK_A_DESK = [(By.ID, "Book a desk"),
                   (By.XPATH, "//android.widget.TextView[@text='Book a desk']")]
    CLOSE = [(By.ID, "clear large"),
             (By.ID, "com.logitech.logue:id/btn_dismiss")]
    LIST = [(By.XPATH, "//XCUIElementTypeButton[@label='List']"),
            (By.ID, "com.logitech.logue:id/list_button")]
    STATIC_TEXT = [(By.XPATH, "//XCUIElementTypeStaticText[@value='XXX']"),
                   (By.XPATH, "//android.widget.TextView[@text='XXX']")]
    NOTIFY_TEAMMATES_SCREEN = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Notify teammates']"),
                               (By.XPATH, "//android.widget.TextView[@text='Notify Teammates']")]
    NOTIFY_TEAMMATES_TITLE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='No teammates added']"),
                              (By.XPATH, "//android.widget.TextView[@text='No teammates added']")]
    NOTIFY_TEAMMATES_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Add people to teammates in order to notify them of your reservation']"),
                                (By.XPATH, "//android.widget.TextView[@text='Add people to teammates in order to notify them of your reservation']")]
    SKIP = [(By.XPATH, "//XCUIElementTypeButton[@label='Skip']"),
            (By.XPATH, "//android.widget.Button[@text='Skip']")]
    DESK_BOOKED_SCREEN = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Desk XXX booked']"),
                          (By.XPATH, "//android.widget.TextView[@text='Desk XXX booked']")] #Pass Desk Name
    DESK_BOOKED_MESSAE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Your desk will be waiting:']"),
                          (By.XPATH, "//android.widget.TextView[@text='Your desk will be waiting:']")]
    DESK_BOOKED_SCHEDULE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@value, 'XXX')]"),
                            (By.XPATH, "//android.widget.TextView[contains(@text, 'XXX')]")] #Pass schedule
    DESK_BOOKED_DAY = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@value, 'XXX')]/following-sibling::XCUIElementTypeStaticText"),
                       (By.XPATH, "//android.widget.TextView[contains(@text, 'XXX')]")]  # Pass schedule
    CHECK_IN_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Are you trying to check in?']"),
                        (By.XPATH, "//android.widget.TextView[@text='Are you trying to check in?']")]
    CHECK_IN_DESK_NAME = [(By.XPATH, "//XCUIElementTypeStaticText[@value='XXX']"),
                          (By.XPATH, "//android.widget.TextView[@text='XXX']")] #Pass Desk Name
    CHECK_IN_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[@label='Check in']"),
                       (By.XPATH, "//android.widget.Button[@text='Check in']")]
    DECLINE_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[@label='Decline']"),
                      (By.XPATH, "//android.widget.Button[@text='Decline']")]
    CHECK_IN_OK = [(By.XPATH, "//XCUIElementTypeButton[@label='OK']"),
                   (By.XPATH, "//android.widget.Button[@text='OK']")]
    CHECK_IN_SUCCESS_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Checked in to desk XXX']"),
                                (By.XPATH, "//android.widget.TextView[@text='Checked in to desk XXX']")] #Pass Desk Name
    ALL_SET_MESSAGE = [(By.ID, "You're all set!"),
                       (By.XPATH, "//android.widget.TextView[@text='You’re all set!']")]
    NOTIFY_TEAMMATE_TOGGLE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'XXX')]/following-sibling:: XCUIElementTypeSwitch"),
                              (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::android.widget.Switch")] #Pass Full Teammate name
    NOTIFY_TEAMMATE_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[contains(@label,'Notify teammate')]"),
                              (By.XPATH, "//android.widget.Button[contains(@text,'Notify teammate')]")]
    NOTIFY_WITH_MESSAGE_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[contains(@label,'Notify with message')]"),
                                  (By.XPATH, "//android.widget.Button[@text='Notify with message']")]
    MESSAGE_TEXT_BOX = [(By.CLASS_NAME, "XCUIElementTypeTextView"),
                        (By.ID, "com.logitech.logue:id/et_message")]
    CUSTOM_MESSAE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='XXX']"),
                     (By.XPATH, "//android.widget.TextView[@text='XXX']")]  # Pass custom text
    INCLUDE_MESSAGE_TEXT = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Include message (XXX/128)']"),
                            (By.XPATH, "//android.widget.TextView[@text='Include message (XXX/128)']")] #Pass count
    TEAMMATE_NOTIFIED_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Teammate notified']"),
                                 (By.XPATH, "//android.widget.TextView[@text='Teammate notified']")]
    NOTIFICATION_SENT_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@value,'Notification sent to')]"),
                                 (By.XPATH, "//android.widget.TextView[contains(@text,'Notification sent to')]")]
    BACK = [(By.ID, "Back"),
            (By.ID, "com.logitech.logue:id/back_button_image")]
