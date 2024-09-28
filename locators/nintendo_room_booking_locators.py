from selenium.webdriver.common.by import By


class RoomBookingMainPageLocators(object):
    """
    Locators from Nintendo Main page.
    """

    CLOCK = (By.ID, "android:id/home:currentTime")
    BOOK_NOW = (By.ID, "android:id/home:bookNow")
    AVAILABILITY = (By.ID, "android:id/home:availability")
    MINUTES_30 = (By.ID, "android:id/home:bookNowOptions:0")
    HOUR_1 = (By.ID, "android:id/home:bookNowOptions:1")
    HOUR_2 = (By.ID, "android:id/home:bookNowOptions:2")
    CHECK_MARK = (By.ID, "android:id/home:bookNowOptions:cancel")
    CHECKIN = (By.ID, "android:id/home:checkIn")
    CHECKIN_CANCEL = (By.ID, "android:id/home:checkInConfirm:cancel")
    CHECKIN_CONFIRM = (By.ID, "android:id/home:checkInConfirm:confirm")
    RELEASE_ROOM = (By.ID, "android:id/home:releaseRoom")
    RELEASE_ROOM_CONFIRM = (By.ID, "android:id/home:releaseConfirm:confirm")
    RELEASE_ROOM_CANCEL = (By.ID, "android:id/home:releaseConfirm:cancel")
    EXTEND_BOOKING = (By.ID, "android:id/home:extendBooking")
    EXTEND_MINUTES_15 = (By.ID, "android:id/home:extendOptions:0")
    EXTEND_MINUTES_30 = (By.ID, "android:id/home:extendOptions:1")
    EXTEND_HOUR_1 = (By.ID, "android:id/home:extendOptions:2")
    FIRST_AGENDA_ITEM_TITLE = (By.ID, "android:id/agenda:0:title")
    FIRST_AGENDA_ITEM_ORGANIZER = (By.ID, "android:id/agenda:0:organizer")
    FIRST_AGENDA_ITEM_TIME = (By.ID, "android:id/agenda:0:time")
    FIRST_AGENDA_ITEM_ATTENDEES_COUNT = (By.ID, "android:id/agenda:0:attendeesCount")
    OPEN_SETTINGS = (By.ID, "android:id/home:openSettings")
    FLOOR_MAP = (By.ID, "android:id/home:openFloorMap")
    ROOM_NAME = (By.ID, "android:id/home:roomName")


class RoomBookingDevicePinLocators(object):
    """
    Locators from Nintendo Device PIN page.
    """

    ENTER_DEVICE_PIN_TEXT = (
        By.XPATH,
        "//android.widget.TextView[@text='Enter device PIN']",
    )
    CLOSE = (By.XPATH, "//android.view.View[@content-desc='Close']")

    @staticmethod
    def digit_n(digit: int):
        """
        Get XPATH associated with digit in Settings PIN Keypad. Digit ranges from 0-> 9.
        """
        if digit == 0:
            digit_n_xpath = (
                By.XPATH,
                "//p0.Y/android.view.View/android.view.View/android.view.View/android.view.View[11]",
            )
        else:
            digit_n_xpath = (
                By.XPATH,
                f"//p0.Y/android.view.View/android.view.View/android.view.View/android.view.View[{digit+1}]",
            )
        return digit_n_xpath


class LogitechSettingsLocators(object):
    """
    Locators from Nintendo Logitech Settings page.
    """

    LOGITECH_SETTINGS_TITLE = (By.ID, "com.logitech.oobe_settings:id/txt_screen_title")
    CLOSE = (By.ID, "com.logitech.oobe_settings:id/closeButton")


class FloorMapLocators(object):
    """
    Locators from Jasmine Floor Map
    """

    FLOOR_MAP = (By.XPATH, "//android.webkit.WebView[@text='Map']")
    CLOSE_FLOOR_MAP = (By.XPATH, "//android.view.View[@resource-id='android:id/floorMap:close']")

