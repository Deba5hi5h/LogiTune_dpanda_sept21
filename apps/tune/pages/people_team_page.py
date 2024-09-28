from typing import Optional, List
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_team_page_locators import TunePeopleTeamPageLocators


class TunePeopleTeamPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_button(self) -> None:
        self._click(TunePeopleTeamPageLocators.BACK_BUTTON)

    def click_edit_button(self) -> None:
        self._click(TunePeopleTeamPageLocators.EDIT_BUTTON)

    def click_search_bar_delete_input_button(self) -> None:
        self._click(TunePeopleTeamPageLocators.SEARCH_BAR_DELETE_INPUT_BUTTON)

    def click_user_button_by_name(self, user_name: str) -> None:
        self._click_by_element_text(TunePeopleTeamPageLocators.USER_BUTTON, user_name,
                                    expected_text_strict_check=False)

    def click_random_user_button(self) -> None:
        self._click_random_element(TunePeopleTeamPageLocators.USER_BUTTON)

    def click_add_teammates_button(self) -> None:
        self._click(TunePeopleTeamPageLocators.ADD_TEAMMATES_BUTTON)

    def input_search_bar(self, data: str) -> None:
        self._delete_input(TunePeopleTeamPageLocators.SEARCH_BAR)
        self._send_keys(TunePeopleTeamPageLocators.SEARCH_BAR, data)

    def verify_teammates_list(self, teammates_list: List[str]) -> bool:
        self.wait_seconds_to_pass(5)
        return self._verify_all_found_elements_values(TunePeopleTeamPageLocators.USER_NAME_LABEL,
                                                      expected_values=teammates_list,
                                                      expected_text_strict_check=True)

    def verify_teammates_list_length(self, teammates_list: List[str]) -> bool:
        teammates_visible = self._wait_for_multiple_elements_presence(TunePeopleTeamPageLocators.USER_NAME_LABEL,
                                                                      no_elements=len(teammates_list),
                                                                      timeout=5)
        return len(teammates_list) == len(teammates_visible)

    def verify_edit_button(self) -> bool:
        return self._is_visible(TunePeopleTeamPageLocators.EDIT_BUTTON, timeout=1)

    def verify_teammate_by_name(self, teammate_name: str) -> bool:
        return self._is_visible_by_text(TunePeopleTeamPageLocators.USER_NAME_LABEL,
                                        expected_text=teammate_name, expected_text_strict_check=False)

    def verify_teammate_not_visible_by_name(self, teammate_name: str) -> bool:
        return self._is_not_visible_by_text(TunePeopleTeamPageLocators.USER_NAME_LABEL,
                                            expected_text=teammate_name, expected_text_strict_check=False)
