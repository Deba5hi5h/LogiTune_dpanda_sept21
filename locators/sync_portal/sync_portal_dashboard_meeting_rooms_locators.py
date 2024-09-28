from selenium.webdriver.common.by import By


class SyncPortalDashboardMeetingRoomsLocators(object):
    """
    A class containing the Sync Portal Meeting Rooms Dashboard Page
    element locators.
    """
    MEETING_ROOMS_HEADING = (By.XPATH, "//h2[text()='Meeting rooms']")
