from selenium.webdriver.common.by import By

class WinAppLocators(object):
    """
    A class containing the WinAppDriver element locators.
    """
    LINE_DOWN_BTN = (By.NAME, "Line down")
    DEVICE_LIST = (By.NAME, "Device List")
    NEXT_BUTTON = (By.NAME, "Next")

    # Windows Settings
    SOUND_OUTPUT = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_OutputList_ComboBox']")
    SOUND_INPUT = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_InputList_ComboBox']")

    # Windows full headset name in Settings - Sound
    WIN_OUTPUT_ZONE_750 = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_OutputList_ComboBox']//Text[contains(@Name,'Zone 750')]")
    WIN_INPUT_ZONE_750 = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_InputList_ComboBox']//Text[contains(@Name,'Zone 750')]")
    WIN_11_OUTPUT_ZONE_750 = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_OutputCollection_ItemsControl']//Text[contains(@Name,'Zone 750')]")
    WIN_11_INPUT_ZONE_750 = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_InputCollection_ItemsControl']//Text[contains(@Name,'Zone 750')]")
    WIN_OUTPUT_ZONE_WIRED_EARBUDS = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_OutputList_ComboBox']//Text[contains(@Name,'Zone Wired Earbuds')]")
    WIN_INPUT_ZONE_WIRED_EARBUDS = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_InputList_ComboBox']//Text[contains(@Name,'Zone Wired Earbuds')]")
    WIN_11_OUTPUT_ZONE_WIRED_EARBUDS = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_OutputCollection_ItemsControl']//Text[contains(@Name,'Zone Wired Earbuds')]")
    WIN_11_INPUT_ZONE_WIRED_EARBUDS = (By.XPATH, "//*[@AutomationId='SystemSettings_Audio_InputCollection_ItemsControl']//Text[contains(@Name,'Zone Wired Earbuds')]")

    # Windows locator on Settings - Bluetooth
    ADD_BLUETOOTH_OR_OTHER_DEVICE = (By.XPATH, "//*[@AutomationId='SystemSettings_Device_Discovery_Button']")
    BLUETOOTH = (By.XPATH, "//*[@AutomationId='BluetoothDevicesButton']")
    DONE = (By.XPATH, "//Button[@Name='Done']")
    VERTICAL_LARGE_INCREASE = (By.XPATH, "//Button[@Name='Vertical Large Increase' and @AutomationId='VerdicalLargeIncrease']")
    VERTICAL_LARGE_DECREASE = (By.XPATH, "//Button[@Name='Vertical Large Decrease' and @AutomationId='VerdicalLargeDecrease']")
    REMOVE_DEVICE = (By.XPATH, "//*[@Name='Remove device']")
