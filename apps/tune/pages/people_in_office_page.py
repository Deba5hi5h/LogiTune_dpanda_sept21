from typing import Optional, Tuple
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_in_office_page_locators import TunePeopleInOfficePageLocators


class TunePeopleInOfficePage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_button(self) -> None:
        self._click(TunePeopleInOfficePageLocators.BACK_BUTTON)

    def click_teammates_tab(self) -> None:
        self._click(TunePeopleInOfficePageLocators.TEAMMATES_BUTTON)

    def click_everyone_tab(self) -> None:
        self._click(TunePeopleInOfficePageLocators.EVERYONE_BUTTON)

    def click_user_by_name_everyone(self, user_name: str) -> None:
        self._click_by_element_text(TunePeopleInOfficePageLocators.EVERYONE_USER_BUTTON, expected_text=user_name,
                                    expected_text_strict_check=False)

    def click_user_by_name_teammates(self, user_name: str) -> None:
        self._click_by_element_text(TunePeopleInOfficePageLocators.TEAMMATE_USER_BUTTON, expected_text=user_name,
                                    expected_text_strict_check=False)

    def input_search_everyone(self, input_text: str) -> None:
        self._delete_input(TunePeopleInOfficePageLocators.EVERYONE_INPUT_SEARCH)
        self._send_keys(TunePeopleInOfficePageLocators.EVERYONE_INPUT_SEARCH, input_text)

    def verify_no_teammates_in_office_label(self) -> bool:
        return self._is_any_element_by_text('No teammates in the office', expected_text_strict_check=False)

    def verify_no_people_in_office_label(self) -> bool:
        return self._is_any_element_by_text('No people in the office', expected_text_strict_check=False)

    def get_booking_data_by_user_id_everyone(self, user_id: str) -> str:
        paragraphs = self._wait_for_multiple_elements_visibility(
            TunePeopleInOfficePageLocators.RESERVATION_BUTTON_BY_ID_PARAGRAPH_EVERYONE,
            locator_parameter=str(user_id),
            no_elements=0,
            comparison=">")

        label = [el.text for el in paragraphs][-1]
        return label

    def get_booking_data_by_user_id_teammates(self, user_id: str) -> str:
        paragraphs = self._wait_for_multiple_elements_visibility(
            TunePeopleInOfficePageLocators.RESERVATION_BUTTON_BY_ID_PARAGRAPH_TEAMMATES,
            locator_parameter=str(user_id),
            no_elements=0,
            comparison=">")

        label = [el.text for el in paragraphs][-1]
        return label

    def verify_user_by_name_everyone(self, user_name: str) -> bool:
        return self._is_visible_by_text(TunePeopleInOfficePageLocators.EVERYONE_USER_BUTTON, expected_text=user_name,
                                        expected_text_strict_check=False)

    def verify_user_by_name_teammates(self, user_name: str) -> bool:
        return self._is_visible_by_text(TunePeopleInOfficePageLocators.TEAMMATE_USER_BUTTON, expected_text=user_name,
                                        expected_text_strict_check=False)


