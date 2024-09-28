from typing import Optional

from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.user_profile_locators import TuneProfileLocators


class TuneUserProfilePage(TuneBasePage):

    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def verify_profile_name(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_NAME)

    def verify_profile_basecamp_name(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_BASECAMP_NAME)

    def verify_keep_bookings_hidden_button(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.KEEP_BOOKINGS_HIDDEN_LABEL)

    def verify_calendar_and_meetings_button(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_CALENDAR_SETTINGS)

    def verify_notifications_button(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_NOTIFICATION_SETTINGS)

    def verify_connected_account_button(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_CONNECTED_ACCOUNT_SETTINGS)

    def verify_privacy_settings_button(self) -> bool:
        return self._is_visible(locator=TuneProfileLocators.PROFILE_PRIVACY_SETTINGS)

    def click_basecamp_button(self) -> None:
        self._click(locator=TuneProfileLocators.PROFILE_BASECAMP_NAME, skip_exception=True)

    def click_keep_bookings_hidden_button(self) -> None:
        self._click(locator=TuneProfileLocators.KEEP_BOOKINGS_HIDDEN_TOGGLE, skip_exception=True)

    def check_keep_bookings_hidden(self) -> bool:
        return self._get_attribute_of_xpath_locator(TuneProfileLocators.KEEP_BOOKINGS_HIDDEN_CHECKBOX,
                                                    'checked') == 'true'

    def click_calendar_and_meetings_button(self) -> None:
        self._click(locator=TuneProfileLocators.PROFILE_CALENDAR_SETTINGS, skip_exception=True)

    def click_notifications_button(self) -> None:
        self._click(locator=TuneProfileLocators.PROFILE_NOTIFICATION_SETTINGS, skip_exception=True)

    def click_connected_account_button(self) -> None:
        self._click(locator=TuneProfileLocators.PROFILE_CONNECTED_ACCOUNT_SETTINGS, skip_exception=True)

    def click_privacy_settings_button(self) -> None:
        self._click(locator=TuneProfileLocators.PROFILE_PRIVACY_SETTINGS, skip_exception=True)

    def click_back_to_dashboard_button(self) -> None:
        self._click(TuneProfileLocators.BACK_BUTTON, skip_exception=True)

    def verify_profile_name_by_text(self, name: str) -> bool:
        return self._compare_text(locator=TuneProfileLocators.PROFILE_NAME, expected_text=name)

    def verify_basecamp_name_by_text(self, name: str) -> bool:
        return self._compare_text(locator=TuneProfileLocators.PROFILE_BASECAMP_NAME, expected_text=name)

    def wait_keep_bookings_hidden_button_load(self) -> None:
        if self._is_visible(TuneProfileLocators.BUTTON_LOADER, timeout=2):
            self._is_not_visible(TuneProfileLocators.BUTTON_LOADER, timeout=2)




