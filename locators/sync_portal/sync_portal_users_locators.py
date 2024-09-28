from selenium.webdriver.common.by import By

class SyncPortalUsersLocators(object):
    """
    A class containing the Sync Portal Users Page
    element locators.
    """
    IT_USERS = (By.XPATH, "//p[text()='IT users']")
    END_USERS = (By.XPATH, "//p[text()='End Users - Manual']")
    MODIFY_GROUPS = (By.XPATH, "//p[text()='Modify groups']")
    USER_CHECKBOX = (By.XPATH, "//div[text()='XXX']/ancestor::div[@role='row']//button")
    USER_GROUPS_TEXTBOX = (By.XPATH, "//label[text()='User groups']/following-sibling::p")
    USER_GROUPS_DROPDOWN = (By.XPATH, "//label[text()='User groups']/parent::div/following-sibling::div")
    USER_GROUPS_MAIN = (By.XPATH, "//button/p[text()='User groups']")
    USER_GROUPS_MAIN_ITEMS = (By.XPATH, "//li/button/p")
    USER_GROUP_COUNT = (By.XPATH, "//p[text()='XXX']/parent::button/following-sibling::p") # Pass Group Name
    APPLY = (By.XPATH, "//button[text()='Apply']")
    USER_GROUP_SELECTION = (By.XPATH, "//div[@title='XXX']")
    SEARCH = (By.XPATH, "//input[contains(@class, 'SearchInput')]")
    SEARCH_RESULT = (By.XPATH, "//div[text()='XXX']")  # Pass search item
    ROLE_CHANGE = (By.XPATH, "//button[text()='Change']")
    ROLE_DROPDOWN = (By.XPATH, "//label[text()='Role']/parent::div")
    ROLE_SELECT = (By.XPATH, "//div[text()='XXX']")  # Pass Role
    ROLE_SAVE = (By.XPATH, "//button[text()='Save']")
    CONFIRM = (By.XPATH, "//button[text()='Confirm']")
    USER_GROUP_SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'groups successfully modified.')]")