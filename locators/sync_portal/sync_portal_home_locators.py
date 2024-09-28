from selenium.webdriver.common.by import By

class SyncPortalHomeLocators(object):
    """
    A class containing the Sync Portal Home Page
    element locators.
    """
    ORG_SELECTOR_ICON = (By.XPATH, "//div[contains(@class, 'OrganizationSelector')]//*[local-name()='svg']")
    ORG_VIEW_ALL = (By.XPATH, "//p[text()='View all']")
    ORG_NAME = (By.XPATH, "//div[text()='XXX']")  # Pass Org Name as parameter
    SYSTEM = (By.XPATH, "//div[text()='System']")
    LOGOUT_ICON = (By.XPATH, "//div[contains(@class, 'FlyoutContainer')]/button[contains(@class, 'ResetButton')]")
    LOGOUT = (By.XPATH, "//a[text()='Logout']")
    MEETING_ROOMS_DASHBOARD = (By.XPATH, "//*[@data-testid='rooms.sidenav']//div[text()='Dashboard']")
    FLEX_DESKS_DASHBOARD = (By.XPATH, "//*[@data-testid='desks.sidenav']//div[text()='Dashboard']")
    MEETING_ROOMS_ISSUES = (By.XPATH, "//*[@data-testid='rooms.sidenav']//div[text()='Issues']")
    FLEX_DESKS_ISSUES = (By.XPATH, "//*[@data-testid='desks.sidenav']//div[text()='Issues']")
