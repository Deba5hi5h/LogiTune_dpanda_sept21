from selenium.webdriver.common.by import By

class TuneMobileTestFlightLocators(object):
    """
    A class containing the TestFlight App element locators.
    """
    LOGITUNE = [(By.ID, "Logi Tune"), ()]
    PREVIOUS_BUILDS = [(By.XPATH, "//*[@name='Previous Builds']"), ()]
    VERSION = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"), ()] #Pass Major Version
    INSTALL = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name, 'XXX')]/following-sibling::XCUIElementTypeButton[@name='INSTALL' or @name='Install'][1]"), ()]  # Pass build Version
    CONFIRM_INSTALL = [(By.ID, "Install"), ()]
    OPEN = [(By.XPATH, "//XCUIElementTypeButton[@name='OPEN' or @name='Open']"), ()]
    UPDATE = [(By.XPATH, "//XCUIElementTypeButton[@name='UPDATE' or @name='Update']"), ()]
    CONTINUE = [(By.ID, "Continue"), ()]
    INSTALL_POPUP = [(By.ID, "Install"), ()]
