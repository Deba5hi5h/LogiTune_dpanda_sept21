from typing import Optional

from selenium.common.exceptions import TimeoutException

from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_page_locators import TunePeoplePageLocators


class TunePeoplePage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def verify_presence_of_onboarding_page(self) -> bool:
        return self._is_visible(TunePeoplePageLocators.EVERYONE_TAB_BUTTON, timeout=60)

    def verify_searched_user(self, user: str) -> bool:
        return self._is_visible_by_text(TunePeoplePageLocators.EVERYONE_USER_BUTTON, expected_text=user,
                                        expected_text_strict_check=False)

    def verify_edit_teams_button(self) -> bool:
        return self._is_visible(TunePeoplePageLocators.EDIT_TEAMS_BUTTON)

    def verify_no_results_found_for_str(self, search_value: str) -> bool:
        return self._compare_text(TunePeoplePageLocators.NO_USERS_FOUND_LABEL,
                                  f'No results found for "{search_value}"')

    def verify_user_from_everyone_tab_by_name(self, user_name: str) -> None:
        self._is_visible_by_text(TunePeoplePageLocators.EVERYONE_USER_BUTTON, user_name,
                                 expected_text_strict_check=False)

    def verify_all_teammates_button(self) -> bool:
        return self._is_visible_by_text(TunePeoplePageLocators.USERS_TEAM_PARAGRAPH, expected_text="All teammates")

    def verify_team_by_team_name(self, team_name: str) -> bool:
        return self._is_visible_by_text(TunePeoplePageLocators.USERS_TEAM_PARAGRAPH, expected_text=team_name)

    def verify_team_not_visible_by_team_name(self, team_name: str) -> bool:
        return self._is_not_visible_by_text(TunePeoplePageLocators.USERS_TEAM_PARAGRAPH, expected_text=team_name)

    def verify_teammates_order(self) -> bool:
        teammates = self._get_all_available_elements(TunePeoplePageLocators.EVERYONE_USER_BUTTON)
        teammates_text = [el.text.split('\n')[-1].lower() for el in teammates]
        return teammates_text == sorted(teammates_text)

    def verify_create_team_button_enabled(self) -> bool:
        return self._is_clickable(TunePeoplePageLocators.POPUP_NEW_TEAM_CREATE_BUTTON, timeout=1)

    def click_everyone_tab_button(self) -> None:
        self._click(TunePeoplePageLocators.EVERYONE_TAB_BUTTON)
        self.wait_for_everyone_tab_load()

    def click_teammates_tab_button(self) -> None:
        self._click(TunePeoplePageLocators.TEAMMATES_TAB_BUTTON)

    def click_everyone_search_bar_delete_input_button(self) -> None:
        self._click(TunePeoplePageLocators.EVERYONE_SEARCH_BAR_DELETE_INPUT_BUTTON)

    def click_random_user_button_from_everyone_tab(self) -> None:
        self._click_random_element(TunePeoplePageLocators.EVERYONE_USER_BUTTON)

    def click_user_from_everyone_tab_by_name(self, user_name: str, match_case: bool = False) -> None:
        self._click_by_element_text(TunePeoplePageLocators.EVERYONE_USER_BUTTON, user_name,
                                    match_case=match_case, expected_text_strict_check=False)
    def click_all_teammates_button(self) -> None:
        self.click_team_button_by_team_name('All teammates', match_case=True)

    def click_team_button_by_team_name(self, team_name: str, match_case: bool = False) -> None:
        self._click_by_element_text(TunePeoplePageLocators.USERS_TEAM_PARAGRAPH, team_name,
                                    match_case=True)

    def click_new_team_button(self) -> None:
        self._click(TunePeoplePageLocators.NEW_TEAM_BUTTON)

    def click_create_team_button(self) -> None:
        self._click(TunePeoplePageLocators.POPUP_NEW_TEAM_CREATE_BUTTON)

    def click_close_create_team_button(self) -> None:
        self._click(TunePeoplePageLocators.POPUP_NEW_TEAM_CLOSE_BUTTON)

    def click_edit_teams_button(self) -> None:
        self._click(TunePeoplePageLocators.EDIT_TEAMS_BUTTON)

    def wait_for_everyone_tab_load(self) -> None:
        self.wait_seconds_to_pass(2)

    def input_everyone_search_bar(self, data: str) -> None:
        self._delete_input(TunePeoplePageLocators.EVERYONE_SEARCH_BAR)
        self._send_keys(TunePeoplePageLocators.EVERYONE_SEARCH_BAR, data)

    def wait_search_to_load(self) -> None:
        self._wait_for_multiple_elements_visibility(
            locator=TunePeoplePageLocators.EVERYONE_USER_BUTTON,
            comparison='<',
            no_elements=10
        )

    def input_team_name(self, team_name: str) -> None:
        self._delete_input(TunePeoplePageLocators.POPUP_NEW_TEAM_INPUT)
        self._send_keys(TunePeoplePageLocators.POPUP_NEW_TEAM_INPUT, keys_input=team_name)

    def clear_input_team_name(self):
        self._delete_input_manually(TunePeoplePageLocators.POPUP_NEW_TEAM_INPUT)

    def verify_input_alert(self, alert_msg: str) -> bool:
        return self._is_any_element_by_text(alert_msg, expected_text_strict_check=False)

    def wait_for_team_creation(self) -> bool:
        return self._is_not_visible(TunePeoplePageLocators.POPUP_NEW_TEAM_CREATE_BUTTON)

    def verify_user_group_visible_by_name(self, group_name: str) -> bool:
        return self._is_any_element_by_text(group_name, expected_text_strict_check=True)

    def click_user_group_visible_by_name(self, group_name: str) -> None:
        self._click_any_element_by_text(group_name, expected_text_strict_check=True)
