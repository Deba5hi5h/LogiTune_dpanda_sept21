from selenium.webdriver.common.by import By

class TuneMobileMapsLocators(object):
    """
    A class containing the Tune Mobile App Maps Screen element locators.
    """
    SELECTED_BUILDING = [(By.XPATH, "(//XCUIElementTypeButton/XCUIElementTypeStaticText)[1]"),
                         (By.ID, "com.logitech.logue:id/tv_map_building")]
    SELECTED_FLOOR = [(By.XPATH, "(//XCUIElementTypeButton/XCUIElementTypeStaticText)[2]"),
                      (By.ID, "com.logitech.logue:id/tv_map_floor")]
    STATIC_TEXT = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
                   (By.XPATH, "//android.widget.TextView[@text='XXX']")]
    OK = [(), (By.XPATH, "//android.widget.Button[@text='OK']")]
    MAP_IMAGE = [(By.ID, "Map"), (By.CLASS_NAME, "android.widget.Image")]
    ROOM_STATUS = [(By.XPATH, "//XCUIElementTypeButton/preceding-sibling::XCUIElementTypeOther/XCUIElementTypeStaticText"),
                   (By.ID, "com.logitech.logue:id/available_desk_label")]
    ROOM_NAME = [(By.XPATH, "//XCUIElementTypeStaticText[@name='ROOM']/following-sibling::XCUIElementTypeStaticText"),
                 (By.ID, "com.logitech.logue:id/selected_desk_name")]
    PEOPLE_COUNT = [(By.XPATH, "//XCUIElementTypeImage/following-sibling::XCUIElementTypeStaticText"),
                    (By.XPATH, "//android.widget.TextView[@resource-id='com.logitech.logue:id/feature_name']")]


