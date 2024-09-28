from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.onboarding_locators import TuneOnboardingPageLocators


class TuneOnboardingPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def verify_presence_of_onboarding_page(self) -> bool:
        return self._is_visible(TuneOnboardingPageLocators.WELCOME_TITLE, timeout=60)

    def click_continue_button(self) -> None:
        self._click(TuneOnboardingPageLocators.CONTINUE_BUTTON)

    def click_skip_button_teammates(self) -> None:
        self._click(TuneOnboardingPageLocators.TEAMMATES_SKIP_BUTTON)
