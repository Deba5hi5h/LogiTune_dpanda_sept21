from selenium.webdriver.common.by import By

from apps.collabos.coily.coily_messages import MSG_IN_A_MEETING, MSG_OUT_FOR_LUNCH


class TuneCoilyMainPageLocators(object):
    """
    Locators from Coily Main page.
    """
    HIERARCHY = (By.ID, "com.logitech.vc.scheduler:id/hierarchy")
    GROUP_NAME = (By.ID, "com.logitech.vc.scheduler:id/resource_group")
    DESK_NAME = (By.ID, "com.logitech.vc.scheduler:id/resource_name")
    CLOCK = (By.ID, "com.logitech.vc.scheduler:id/clock")
    PLUG_IN_TO_START_LABEL = (By.ID, "com.logitech.vc.scheduler:id/plug_in_to_start")
    PLUG_IN_TO_START_TEXT = (By.ID, "com.logitech.vc.scheduler:id/plug_in_text")
    SETTINGS_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/settings_button")
    TIME_LEFT_TO_RESERVATION = (By.ID, "com.logitech.vc.scheduler:id/timeLeftButtonText")
    TIME_LEFT_TO_RESERVATION_ICON = (By.ID, "com.logitech.vc.scheduler:id/imeLeftButtonIcon")
    BOOK_DESK = (By.ID, "com.logitech.vc.scheduler:id/scan_qr_button")
    BOOK_DESK_OK = (By.ID, "com.logitech.vc.scheduler:id/action")
    BOOK_DESK_GOT_IT = (By.ID, "com.logitech.vc.scheduler:id/button")
    PIN_PAGE_CLOSE = (By.ID, "com.logitech.vc.scheduler:id/button_close")

class TuneCoilyBookedDeskLocators(object):
    """
    Locators from Coily Booked page.
    """
    ORG_NAME = (By.ID, "com.logitech.vc.scheduler:id/floor")
    GROUP_NAME = (By.ID, "com.logitech.vc.scheduler:id/resource_group")
    DESK_NAME = (By.ID, "com.logitech.vc.scheduler:id/resource_name")
    CLOCK = (By.ID, "com.logitech.vc.scheduler:id/clock")
    PLUG_IN_TO_START_LABEL = (By.ID, "com.logitech.vc.scheduler:id/plug_in_to_start")
    PLUG_IN_TO_START_TEXT = (By.ID, "com.logitech.vc.scheduler:id/plug_in_text")
    SETTINGS_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/settings_button")
    CHECK_IN_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/check_in_button")
    GOT_IT_BUTTON = (By.XPATH, "//android.widget.Button[@text='Got it']")
    START_STATUS = (By.ID, "com.logitech.vc.scheduler:id/start_status")
    USER_NAME = (By.ID, "com.logitech.vc.scheduler:id/user_name")
    BACK = (By.ID, "com.logitech.vc.scheduler:id/back_button")
    CANCEL_TRANSFER = (By.ID, "com.logitech.vc.scheduler:id/cancelButton")

class TuneCoilyAuthorizedDeskLocators(object):
    """
    Locators from Coily Authorized page.
    """
    DATE = (By.ID, "com.logitech.vc.scheduler:id/date")
    HIERARHY = (By.ID, "com.logitech.vc.scheduler:id/hierarchy")
    CLOCK = (By.ID, "com.logitech.vc.scheduler:id/clock")
    NOTIFICATION_MESSAGE = (By.ID, "com.logitech.vc.scheduler:id/notification_message")
    NOTIFICATION_ACTION = (By.ID, "com.logitech.vc.scheduler:id/notification_action")
    NOTIFICATION_DISMISS = (By.ID, "com.logitech.vc.scheduler:id/dismiss_button")
    EVENT_ITEM = (By.ID, "com.logitech.vc.scheduler:id/event_item")
    EVENT_TIME = (By.ID, "com.logitech.vc.scheduler:id/time")
    EVENT_ATTENDEES = (By.ID, "com.logitech.vc.scheduler:id/attendees")
    EVENT_TITLE = (By.ID, "com.logitech.vc.scheduler:id/title")
    EVENT_JOIN_NOW_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/join_now_button")
    AGENDA_BOTTOM_SHEET = (By.ID, "com.logitech.vc.scheduler:id/bottomSheetView")
    AGENDA_VIEW_CLOSE_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/close_agenda_button")
    PRIVACY_AGENDA = (By.ID, "com.logitech.vc.scheduler:id/privacy_agenda")
    EVENT_VIEW_CLOSE_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/close_button")
    EVENT_SHOW_ALL_ATTENDEES = (By.ID, "com.logitech.vc.scheduler:id/show_all")
    EVENT_NOTES = (By.ID, "com.logitech.vc.scheduler:id/notes_header")



class TuneCoilyLaptopDisconnectedLocators(object):
    """
    Locators from Coily 'Laptop disconnected' page.
    """
    TITLE = (By.ID, "com.logitech.vc.scheduler:id/title")
    MESSAGE = (By.ID, "com.logitech.vc.scheduler:id/message")
    RELEASE_DESK = (By.ID, "com.logitech.vc.scheduler:id/release_desk")

    BE_BACK_SOON = (By.XPATH, "//*[contains(@text,\"I'll be back soon\")]")
    IN_A_MEETING = (By.XPATH, f"//*[@text='{MSG_IN_A_MEETING}']")
    OUT_FOR_LUNCH = (By.XPATH, f"//*[@text='{MSG_OUT_FOR_LUNCH}']")
    CUSTOM_MESSAGE = (By.XPATH, '//*[contains(@text, "XXX")]')
    AWAY_MESSAGE = (By.ID, "com.logitech.vc.scheduler:id/away_message")
    AWAY_MESSAGE_TITLE = (By.ID, "com.logitech.vc.scheduler:id/message")
    USER_NAME_AWAY_PAGE = (By.ID, "com.logitech.vc.scheduler:id/user_name")


class TuneCoilyMessagesLocators(object):
    """
    Locators from Coily checking/booking page.
    """
    MESSAGE_TITLE = (By.ID, "com.logitech.vc.scheduler:id/title")
    MESSAGE_TEXT = (By.ID, "com.logitech.vc.scheduler:id/message")
    MESSAGE_ICON = (By.ID, "com.logitech.vc.scheduler:id/spinner_circle")
    GOT_IT = (By.ID, "com.logitech.vc.scheduler:id/settings_button")
    ACTUALLY_YOU_QUESTION_TEXT = (By.ID, "com.logitech.vc.scheduler:id/questionText")
    QUESTION_TEXT = (By.ID, "com.logitech.vc.scheduler:id/question_text")
    ACTION_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/action_button")
    BACK = (By.ID, "com.logitech.vc.scheduler:id/back_button")

class TuneCoilySessionIsOverLocators(object):
    """
    Locators from Coily 'Session is over' page.
    """
    MESSAGE_TITLE = (By.ID, "com.logitech.vc.scheduler:id/titleText")
    MESSAGE_TEXT = (By.ID, "com.logitech.vc.scheduler:id/messageText")
    CLOCK_ICON = (By.ID, "com.logitech.vc.scheduler:id/clock")
    COUNTDOWN_ICON = (By.ID, "com.logitech.vc.scheduler:id/countdown")

class TuneCoilyDeskTimeLimit(object):
    """
    Locators from Coily checking/booking page.
    """
    MESSAGE_TITLE = (By.ID, "com.logitech.vc.scheduler:id/title")
    MESSAGE_TEXT = (By.ID, "com.logitech.vc.scheduler:id/message")
    MESSAGE_ICON = (By.ID, "com.logitech.vc.scheduler:id/icon_background")
    GOT_IT = (By.ID, "com.logitech.vc.scheduler:id/check_in_button")


class TuneCoilySettingsLocators:
    """
    Locators from Coily Settings page
    """
    SETTINGS_FROM_MAIN_MENU = (By.ID, "com.logitech.vc.scheduler:id/settings_button")
    SETTINGS_MENU_LANGUAGE = (By.ID, "com.logitech.vc.scheduler:id/settings_language")
    TIME_FORMAT = (By.ID, "com.logitech.vc.scheduler:id/settings_time_format")
    BRIGHTNESS_BAR = (By.CLASS_NAME, "android.widget.SeekBar")
    SHOW_AGENDA = (By.ID, "com.logitech.vc.scheduler:id/settings_privacy_agenda")
    PRIVATE_AGENDA_ITEMS = (By.ID, "com.logitech.vc.scheduler:id/settings_privacy_mode")
    ADMIN_SETTINGS_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/logi_settings_button")
    CLOCK_MAIN_PAGE = (By.ID, "com.logitech.vc.scheduler:id/clock")
    CLOSE_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/close_button")
    SETTINGS_HEADER = (By.ID, "com.logitech.vc.scheduler:id/settings_header")
    LANGUAGE_SELECTOR = (By.ID, "com.logitech.vc.scheduler:id/language_selector")


class TuneWalkinDisabledLocators:

    BOOK_DESK_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/button")
    TITLE_LABEL = (By.ID, 'com.logitech.vc.scheduler:id/title')
    MESSAGE_LABEL = (By.ID, 'com.logitech.vc.scheduler:id/message')
    QR_POPUP_TITLE = (By.ID, 'com.logitech.vc.scheduler:id/titleText')
    QR_POPUP_MSG = (By.ID, 'com.logitech.vc.scheduler:id/messageText')
    QR_POPUP_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/button")


class TuneCoilyAlreadyHaveSessionLocators:

    TRANSFER_BUTTON = (By.ID, "com.logitech.vc.scheduler:id/transferButton")
    TITLE_LABEL = (By.ID, 'com.logitech.vc.scheduler:id/title')
    MESSAGE_LABEL = (By.ID, 'com.logitech.vc.scheduler:id/message')
    CANCEL_BUTTON = (By.ID, 'com.logitech.vc.scheduler:id/cancelButton')






