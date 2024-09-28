from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes
from locators.base.attributes import HtmlAttribute


class TuneSettingsLocators:
    CLOSE_BUTTON = xpath_by_data_testid(El.svg, 'screen.button.close')
    CALENDAR_AND_MEETINGS_SETTINGS_BUTTON = xpath_by_data_testid(El.div, 'appSettings.settingsMain.calendarAndMeetings')
    NOTIFICATIONS_SETTINGS_BUTTON = xpath_by_data_testid(El.div, 'appSettings.settingsMain.notifications')
    CONNECTED_ACCOUNT_SETTINGS_BUTTON = xpath_by_data_testid(El.div, 'appSettings.settingsMain.workAccount')
    APPEARANCE_SETTINGS_BUTTON = xpath_by_data_testid(El.div, 'appSettings.settingsMain.themeSettings')

    # Appearance popup
    APPEARANCE_OPENED_LABEL = xpath_by_data_testid(El.p, "dialog.title")
    LIGHT_MODE_BUTTON = xpath_by_data_testid(El.div, 'screens.appSettings.appearance.radio-light')
    DARK_MODE_BUTTON = xpath_by_data_testid(El.div, 'screens.appSettings.appearance.radio-dark')
    SYSTEM_MODE_BUTTON = xpath_by_data_testid(El.div, 'screens.appSettings.appearance.radio-system')
    HTML_MAIN_WINDOW = xpath_by_multiple_attributes(El.html, (HtmlAttribute.data_theme, None))
    CLOSE_APPEARANCE_POPUP = xpath_by_data_testid(El.div, 'dialog.button.close')
