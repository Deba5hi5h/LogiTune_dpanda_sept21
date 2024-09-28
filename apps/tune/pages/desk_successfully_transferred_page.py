from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.desk_successfully_transferred_page_locators import \
    TuneDeskSuccessfullyTransferredPageLocators


class TuneDeskSuccessfullyTransferredPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_done_button(self) -> None:
        self._click(TuneDeskSuccessfullyTransferredPageLocators.DONE_BUTTON)
