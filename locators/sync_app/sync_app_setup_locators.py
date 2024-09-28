from selenium.webdriver.common.by import By


class SyncAppSetupLocators(object):
    """
    A class containing the Sync App First Run Experience setup Screen element locators.
    """
    GET_STARTED = (By.XPATH, "//*[text()='Get Started']")
    SKIP_SETUP = (By.XPATH, "//*[text()='Skip Setup']")
    SIGN_IN_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Sign in to Sync portal']")
    CONNECT_THIS_ROOM_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Connect this room to Sync portal']")
    ROOM_INFORMATION = (By.XPATH, "//p[text()='Room Information']")
    ROOM_NAME_SETUP = (By.XPATH, "//label[text()='Room Name']/parent::div//input")
    SEAT_COUNT_SETUP = (By.XPATH, "//label[text()='Seat Count']/parent::div//input")
    NEXT = (By.XPATH, "//span[text()='Next']")
    WHAT_WOULD_YOU_LIKE_TO_SET_UP = (By.XPATH, "//p[text()='What would you like to set up?']")
    RALLY_CAMERA_SETUP_BUTTON = (By.XPATH, "//button/span[text()='Rally Camera']")
    RALLY_SETUP_BUTTON = (By.XPATH, "//button/span[text()='Rally & Rally Plus']")
    MEETUP_SETUP_BUTTON = (By.XPATH, "//button/span[text()='MeetUp']")

    SEAT_ERROR = (By.XPATH, "//p[text()='Please enter a valid number.']")
    LETS_SETUP_RALLY = (By.XPATH, "//p[text()=\"Let's setup Rally\"]")
    LETS_SETUP_RALLY_CAMERA = (By.XPATH, "//p[text()=\"Let's setup Rally Camera\"]")
    RALLY_CAMERA_SETUP_VIDEO = (By.XPATH, "//*[text()='How To Setup the Logitech Rally Camera (Basic)']")
    LETS_SETUP_MEETUP = (By.XPATH, "//p[text()=\"Let's setup MeetUp\"]")
    CONNECT_RALLY_NOW = (By.NAME, "CONNECT RALLY NOW")
    CONNECT_MEETUP_NOW = (By.NAME, "CONNECT MEETUP NOW")
    CONNECT_RALLY_CAMERA_NOW = (By.NAME, "CONNECT RALLY CAMERA NOW")
    SYSTEM_DOESNT_SEE_DEVICE = (By.XPATH, "//button[text()=\"The system doesn't see my device\"]")
    WHERE_PLACE_COMPUTER = (By.XPATH, "//button[text()='Where should I place the computer?']")
    COMPUTER_BY_THE_TV = (By.XPATH, "//p[text()='Computer by the TV']")
    COMPUTER_BY_THE_TV_VIDEO = (By.XPATH, "//*[text()='Rally Setup with computer at the display']")
    COMPUTER_BY_THE_TABLE = (By.XPATH, "//p[text()='Computer by the table']")
    COMPUTER_BY_THE_TABLE_VIDEO = (By.XPATH, "//*[text()='Rally Setup with computer at the table']")
    SETUP_RALLY_CAMERA = (By.XPATH, "//p[text()='Set up Rally Camera']")
    SETUP_MEETUP = (By.XPATH, "//p[text()='Set up MeetUp']")
    SETUP_MEETUP_VIDEO = (By.XPATH, "//*[text()='How To Setup the Logitech MeetUp ConferenceCam']")
    CLOSE = (By.XPATH, "//span[text()='close']")
    SYNC_SETUP_COMPLETE = (By.XPATH, "//p[text()='Sync Setup Complete!']")
    OK_GOT_IT = (By.XPATH, "//span[text()='Ok, Got it']")
    SHARE_ANALYTICS_DATA = (By.XPATH, "//span[text()='Share analytics data']")
    HELP_US_IMPROVE = (By.XPATH, "//p[text()='Help us improve your experience']")
    DONE = (By.XPATH, "//span[text()='Done']")