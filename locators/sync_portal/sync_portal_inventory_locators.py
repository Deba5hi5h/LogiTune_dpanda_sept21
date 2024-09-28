from selenium.webdriver.common.by import By


class SyncPortalInventoryLocators(object):
    """
    A class containing the Sync Portal Inventory Page
    element locators.
    """
    SEARCH_BOX = (By.XPATH, "//input[contains(@class, 'SearchInput')]")
    INVENTORY_ROOM = (By.XPATH, "//div[text()='XXX']")  # Pass Room Name
    LEFT_NAVIGATION_ROOM = (By.XPATH, "//div[contains(@class, 'SideNav') and text()='Room']")
    ROOM_DEVICES = (By.XPATH, "//div[text()= 'XXX']/ancestor::div[@aria-label='row']/"
                              "div[4]")  # Pass room name in look element as param
    ROOM_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Room']")
    GROUP_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Group']")
    DEVICES_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Devices']")
    SYNC_VERSION_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Sync Version']")
    STATUS_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Status']")
    HEALTH_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Health']")
    USE_STATE_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Use State']")
    SEAT_COUNT_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='Seat count']")
    ROOM_STATUS = (By.XPATH, "//div[text()= 'XXX']/ancestor::div[@aria-label='row']"
                             "//*[contains(@class,'UpdateStatus')]")  # Pass room name in look element as param
    ROOM_HEALTH = (By.XPATH, "//div[text()= 'XXX']/ancestor::div[@aria-label='row']//"
                             "*[contains(@class,'Health')]/div[2]")  # Pass room name in look element as param
    ROOM_USE_STATE = (By.XPATH, "//div[text()= 'XXX']/ancestor::div[@aria-label='row']//"
                                "*[contains(@class,'UseState')]")  # Pass room name in look element as param
    DEVICE_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='DEVICE']")
    VERSION_HEADER = (By.XPATH, "//div[@role='columnheader']/div/div/span[text()='VERSION']")
    DEVICES_TAB = (By.XPATH, "//a[text()= 'Devices']")
    DEVICE_STATUS = (By.XPATH, "//a[text()= 'XXX']/ancestor::div[@aria-label='row']//"
                               "*[contains(@class,'UpdateStatus')]")  # Pass Device Name in look element as param
    DEVICE_HEALTH = (By.XPATH, "//a[text()= 'XXX']/ancestor::div[@aria-label='row']//"
                               "*[contains(@class,'Health')]/div[2]")  # Pass Device Name in look element as param
    DEVICE_USE_STATE = (By.XPATH, "//a[text()= 'XXX']/ancestor::div[@aria-label='row']//"
                                  "*[contains(@class,'UseState')]")  # Pass Device Name in look element as param
    ADD_ROOM = (By.XPATH, "//button[text()='Add room']")
    EMPTY_ROOM = (By.XPATH, "//h3[text()='Empty room']")
    CREATE_ROOM_NAME = (By.XPATH, "//input[@id='rooms[0].name']")
    CREATE_ROOM_SEAT = (By.XPATH, "//input[@id='rooms[0].seatCount']")
    CREATE_BUTTON = (By.XPATH, "//button[text()='Create']")
    CREATE_ROOM_SUCCESS_MSG = (By.XPATH, "//*[text()='1 room created']")
