from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.sign_in_page_locators import TuneSignInLocators


class TuneSignInPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_button(self) -> None:
        self._click(TuneSignInLocators.BACK_BUTTON)

    def click_privacy_policy_agreement_button(self) -> None:
        self._click(TuneSignInLocators.PRIVACY_POLICY_AGREEMENT_BUTTON)

    def click_google_account_button(self) -> None:
        self._click(TuneSignInLocators.GOOGLE_ACCOUNT_BUTTON)

    def click_outlook_account_button(self) -> None:
        self._click(TuneSignInLocators.OUTLOOK_ACCOUNT_BUTTON)
