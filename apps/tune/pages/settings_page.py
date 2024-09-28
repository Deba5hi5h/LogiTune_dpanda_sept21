from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.settings_page_locators import TuneSettingsLocators


class TuneSettingsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_close_button(self) -> None:
        self._click(TuneSettingsLocators.CLOSE_BUTTON)

    def click_calendar_and_meetings_button(self) -> None:
        self._click(TuneSettingsLocators.CALENDAR_AND_MEETINGS_SETTINGS_BUTTON)

    def click_notifications_button(self) -> None:
        self._click(TuneSettingsLocators.NOTIFICATIONS_SETTINGS_BUTTON)

    def click_connected_account_button(self) -> None:
        self._click(TuneSettingsLocators.CONNECTED_ACCOUNT_SETTINGS_BUTTON)

    def click_light_mode_button(self) -> None:
        self._click(TuneSettingsLocators.LIGHT_MODE_BUTTON)

    def click_dark_mode_button(self) -> None:
        self._click(TuneSettingsLocators.DARK_MODE_BUTTON)

    def click_system_mode_button(self) -> None:
        self._click(TuneSettingsLocators.SYSTEM_MODE_BUTTON)

    def click_appearance_button(self) -> None:
        self._click(TuneSettingsLocators.APPEARANCE_SETTINGS_BUTTON)

    def click_close_appearance_button(self) -> None:
        self._click(TuneSettingsLocators.CLOSE_APPEARANCE_POPUP)

    def verify_appearance_label_visible(self) -> bool:
        return self._is_visible(TuneSettingsLocators.APPEARANCE_OPENED_LABEL)

    def get_appearance_mode(self) -> str:
        current_theme = self._get_attribute_of_xpath_locator(TuneSettingsLocators.HTML_MAIN_WINDOW, 'data-theme')
        return current_theme

