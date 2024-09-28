from typing import Optional, Tuple
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_user_page_locators import TunePeopleUserPageLocators


class TunePeopleUserPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_add_to_teammates_button(self) -> None:
        self._click(TunePeopleUserPageLocators.ADD_TO_TEAMMATES_BUTTON)

    def click_booking_by_booking_id(self, booking_id: str) -> None:
        self._click(TunePeopleUserPageLocators.RESERVATION_BUTTON_BY_ID, locator_parameter=str(booking_id))

    def click_manage_teams_button(self) -> None:
        self._click(TunePeopleUserPageLocators.MANAGE_TEAMS_BUTTON)

    def click_remove_from_teammates_button(self) -> None:
        self._click(TunePeopleUserPageLocators.REMOVE_FROM_TEAMMATES_BUTTON)

    def click_remove_from_teammates_button_confirm(self) -> None:
        self._click(TunePeopleUserPageLocators.POPUP_REMOVE_FROM_TEAMMATES_OK_BUTTON)

    def click_back_button(self) -> None:
        self.wait_seconds_to_pass(3)
        self._click(TunePeopleUserPageLocators.BACK_BUTTON)

    def wait_for_back_button_to_be_clickable(self) -> None:
        self._wait_until_element_clickable(TunePeopleUserPageLocators.BACK_BUTTON)

    def wait_for_remove_button_to_be_not_visible(self) -> None:
        self._wait_until_element_not_visible(TunePeopleUserPageLocators.POPUP_REMOVE_FROM_TEAMMATES_OK_BUTTON)

    def verify_remove_button_to_be_visible(self) -> bool:
        return self._is_visible(TunePeopleUserPageLocators.REMOVE_FROM_TEAMMATES_BUTTON)

    def verify_add_button_to_be_visible(self) -> bool:
        return self._is_visible(TunePeopleUserPageLocators.ADD_TO_TEAMMATES_BUTTON)

    def verify_user_profile_name_by_text(self, name: str) -> bool:
        return self._compare_text(TunePeopleUserPageLocators.USER_NAME_LABEL, name, strict_text_check=False)

    def verify_user_email_name_by_text(self, email: str) -> bool:
        return self._compare_text(TunePeopleUserPageLocators.USER_EMAIL_LABEL, email, strict_text_check=False)

    def verify_user_group_by_text(self, group: str) -> bool:
        return self._compare_text(TunePeopleUserPageLocators.USER_GROUPS_LABEL, group, strict_text_check=False)

    def verify_no_bookings_for_user(self) -> bool:
        return self._is_visible(TunePeopleUserPageLocators.NO_BOOKINGS_FOR_USER_LABEL)

    def verify_booking_by_booking_id(self, booking_id: str) -> bool:
        return self._is_visible(TunePeopleUserPageLocators.RESERVATION_BUTTON_BY_ID,
                                locator_parameter=str(booking_id))

    def verify_user_teams_number(self, teams_number: int) -> bool:
        user_teams_number_visible = (
            self._get_all_available_elements(TunePeopleUserPageLocators.MANAGE_TEAMS_BUTTON_PARAGRAPH))[-1]
        return int(user_teams_number_visible.text) == teams_number

    def get_booking_data_by_booking_id(self, booking_id: str) -> (
            Tuple)[str, str, str]:
        paragraphs = self._wait_for_multiple_elements_visibility(
            TunePeopleUserPageLocators.RESERVATION_BUTTON_BY_ID_PARAGRAPH,
            locator_parameter=str(booking_id),
            no_elements=0,
            comparison=">")

        date, timestamps, label = [el.text for el in paragraphs]
        return date, timestamps, label

    def click_refresh_button_and_wait_for_refresh(self) -> bool:
        self._click(TunePeopleUserPageLocators.DASHBOARD_REFRESH_BUTTON)
        while self._is_visible(TunePeopleUserPageLocators.DASHBOARD_ICON_LOADER, timeout=3):
            pass
        return True

    def wait_for_refresh(self) -> bool:
        while self._is_visible(TunePeopleUserPageLocators.DASHBOARD_ICON_LOADER, timeout=3):
            pass
        return True





