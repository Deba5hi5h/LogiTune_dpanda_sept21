from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.connected_account_settings_locators import TuneConnectedAccountSettingsLocators


class TuneConnectedAccountSettingsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_button(self) -> None:
        self._click(TuneConnectedAccountSettingsLocators.BACK_BUTTON)

    def click_disconnect_account_button(self) -> None:
        self._click(TuneConnectedAccountSettingsLocators.DISCONNECT_BUTTON)

    def click_popup_disconnect_button(self) -> None:
        self._click(TuneConnectedAccountSettingsLocators.DISCONNECT_ACCOUNT_POPUP_DISCONNECT_BUTTON)

    def click_popup_cancel_button(self) -> None:
        self._click(TuneConnectedAccountSettingsLocators.DISCONNECT_ACCOUNT_POPUP_CANCEL_BUTTON)

    def wait_for_disconnect(self) -> None:
        self._is_not_visible(TuneConnectedAccountSettingsLocators.DISCONNECT_ACCOUNT_POPUP_DISCONNECT_BUTTON,
                             timeout=5)
