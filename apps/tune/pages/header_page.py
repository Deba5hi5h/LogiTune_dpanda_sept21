from typing import Optional

from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.header_page_locators import TuneHeaderLocators


class TuneHeaderPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_settings_dropdown_button(self) -> None:

        self._click(TuneHeaderLocators.SETTINGS_BUTTON)

    def click_popup_settings_button(self) -> None:

        self._click(TuneHeaderLocators.SETTINGS_POPUP_SETTINGS_BUTTON)

    def click_popup_share_feedback_button(self) -> None:
        self._click(TuneHeaderLocators.SETTINGS_POPUP_SHARE_FEEDBACK_BUTTON)

    def click_popup_support_button(self) -> None:

        self._click(TuneHeaderLocators.SETTINGS_POPUP_SUPPORT_BUTTON)

    def click_popup_about_button(self) -> None:

        self._click(TuneHeaderLocators.SETTINGS_POPUP_ABOUT_BUTTON)

    def click_popup_quit_button(self) -> None:

        self._click(TuneHeaderLocators.SETTINGS_POPUP_QUIT_BUTTON)
