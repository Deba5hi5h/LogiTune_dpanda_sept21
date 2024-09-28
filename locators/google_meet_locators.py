from selenium.webdriver.common.by import By

class GoogleMeetLocators(object):
    """
    A class containing the Google Meet
    element locators.
    """
    # Home
    NEW_MEETING = (By.XPATH, "//span[text()='New meeting']")
    START_AN_INSTANT_MEETING = (By.XPATH, "//span[text()='Start an instant meeting']")

    # In Meeting
    CAMERA = (By.XPATH, "//button[contains(@aria-label, 'camera')]")
    LEAVE_CALL = (By.XPATH, "//button[contains(@aria-label, 'Leave call')]")
    VIDEO_STREAM = (By.XPATH, "//video")
    MEETING_READY = (By.XPATH, "//h2[text()=\"Your meeting's ready\"]")
    MEETING_READY_CLOSE = (By.XPATH, "//h2[text()=\"Your meeting's ready\"]/following-sibling::button")

    RETURN_TO_HOME = (By.XPATH, "//span[text()='Return to home screen']")

   #Google Meet Messages
    TRY_GOOGLE_MEET_WEBAPP_MSG = (By.XPATH, "//span[text()='Try the free Google Meet web app']")
    CLOSE = (By.XPATH, "//span[text()='Close']")