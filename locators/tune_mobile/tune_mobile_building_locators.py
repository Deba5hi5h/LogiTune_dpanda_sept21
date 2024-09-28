from selenium.webdriver.common.by import By

class TuneMobileBuildingLocators(object):
    """
    A class containing the Tune Mobile App Buidling Screen element locators.
    """
    SITE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label,'XXX')]"),
            (By.XPATH, "//android.widget.TextView[contains(@text,'XXX')]")]
    BUILDING = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label,'XXX')]"),
                (By.XPATH, "//android.widget.TextView[contains(@text,'XXX')]")]
    BACK = [(By.ID, "Back"),
            (By.ID, "com.logitech.logue:id/back_button_image")]
    CHANGE_BUILDING = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Change building']"),
                       (By.XPATH, "//android.widget.TextView[@text='Change Building']")]
    SEARCH = [(By.CLASS_NAME, "XCUIElementTypeTextField"),
              (By.ID, "com.logitech.logue:id/et_search_people_everyone")]