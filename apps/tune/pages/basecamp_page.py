import time
from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.basecamp_locators import TuneBasecampPageLocators


class TuneBasecampPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def search_for_basecamp(self, basecamp_location: str) -> None:
        self._send_keys(TuneBasecampPageLocators.SEARCH_INPUT, basecamp_location)

    def click_chosen_basecamp(self, basecamp_name: str) -> None:
        self._click_by_element_text(TuneBasecampPageLocators.LOCATION_ITEM, basecamp_name)
        time.sleep(2)
