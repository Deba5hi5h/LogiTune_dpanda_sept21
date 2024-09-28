from selenium.webdriver.common.by import By


class SyncPortalIssuesMeetingRoomsLocators(object):
    """
    A class containing the Sync Portal Meeting Rooms Issues Page
    element locators.
    """
    MEETING_ROOMS_ISSUES_TAB = (By.XPATH, "//a[contains(text(),'Issues')]")
