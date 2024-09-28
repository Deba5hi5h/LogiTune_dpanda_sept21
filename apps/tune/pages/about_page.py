from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.about_page_locators import AboutPageLocators


class TuneAboutPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_close_button(self):
        self._click(AboutPageLocators.CLOSE_BUTTON)

    def get_tune_version(self) -> str:
        a = self._get_text(AboutPageLocators.TUNE_VERSION_LABEL)
        _, _, version = self._get_text(AboutPageLocators.TUNE_VERSION_LABEL).split(' ')
        return version


