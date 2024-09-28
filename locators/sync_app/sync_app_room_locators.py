from selenium.webdriver.common.by import By


class SyncAppRoomLocators(object):
    """
    A class containing the Sync App Room Screen element locators.
    """
    ROOM_INFO = (By.XPATH, "//p[text()='Add Device']/ancestor::div[4]/following-sibling::div//p[text()='Room']/"
                           "following-sibling::div//*[local-name()='svg']")
    SEAT_COUNT = (By.XPATH, "//label[text()='Seat Count']/following-sibling::div/input")
    CONNECT_TO_SYNC_PORTAL = (By.XPATH, "//p[text()='Connect to Sync Portal.']")
    DISCONNECT_ROOM = (By.XPATH, "//button/span[text()='Disconnect']")
    EMAIL_SETUP = (By.XPATH, "//*[text()='Email and password']")
    PROVISION_CODE_SETUP = (By.XPATH, "//*[text()='Room provision code']")
    PROVISION_CODE = (By.XPATH, "//input")
    USER_NAME = (By.XPATH, "//label[text()='Username']/following-sibling::div/input")
    PASSWORD = (By.XPATH, "//label[text()='Password']/following-sibling::div/input")
    CONNECT_ROOM = (By.XPATH, "//span[text()='Connect room']/parent::button")
    PROVISION_CODE_MULTIPLE_HOSTS_ERROR = (By.XPATH, "//p[text()='This room already has host PC/appliance device']")
    INCORRECT_PROVISION_CODE_ERROR = (By.XPATH, "//p[text()='This provisioning code is invalid']")
    ORG_NAME = (By.XPATH, "//p[text()='XXX']")  # Pass group name
    NO_ORGANIZATION_MSG = (By.XPATH, "//p[text()='No affiliated organization found']")
    THIRD_PARTY_MSG = (By.XPATH, "//p[text()='Third Party permission']")
    DISCONNECT_PERMISSION_MSG = (By.XPATH, "//p[text()='Please contact an admin with permission to add rooms.']")
    OK_BUTTON = (By.XPATH, "//span[text()='Ok']")
    GROUP_RADIO = (By.XPATH, "//p[text()='XXX']/parent::div/preceding-sibling::span//input")  # Pass group name
    JOIN = (By.XPATH, "//button/span[text()='Join']")
    ROOM_CONNECTED = (By.XPATH, "//p[contains(text(),'Connected to')]")

    # Room Information on clicking info icon
    COMPUTER_TYPE = (By.XPATH, "//p[text()='Computer Type']/ancestor::div[2]/following-sibling::div/p")
    OPERATING_SYSTEM = (By.XPATH, "//p[text()='Operating System']/ancestor::div[2]/following-sibling::div/p")
    OS_VERSION = (By.XPATH, "//p[text()='OS Version']/ancestor::div[2]/following-sibling::div/p")
    PROCESSOR = (By.XPATH, "//p[text()='Processor']/ancestor::div[2]/following-sibling::div/p")
    MEMORY = (By.XPATH, "//p[text()='Memory']/ancestor::div[2]/following-sibling::div/p")

    # Sync Updates and Menu screen
    SYNC_VERSION = (By.XPATH, "//p[contains(text(),'Version')]")
    ROOM_SYNC_UPDATE_AVAILABLE = (By.XPATH, "//p[contains(text(), 'New Sync App version') and "
                                            "contains(text(), 'available')]")
    ROOM_SYNC_UPDATE = (By.XPATH, "//button/span[text()='Update']")
    CHECK_FOR_UPDATE = (By.XPATH, "//button/span[text()='Check for update']")