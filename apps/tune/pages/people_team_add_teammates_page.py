from typing import List, Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver, WebElement
from locators.tune.people_team_add_teammates_page_locators import TunePeopleTeamAddTeammatesPageLocators


class TunePeopleTeamAddTeammatesPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_close_button(self) -> None:
        self._click(TunePeopleTeamAddTeammatesPageLocators.CLOSE_BUTTON)

    def click_delete_search_bar_input_button(self) -> None:
        self._click(TunePeopleTeamAddTeammatesPageLocators.SEARCH_BAR_DELETE_INPUT_BUTTON)

    def verify_user_button_by_name(self, user_name: str) -> bool:
        return self._is_visible_by_text(TunePeopleTeamAddTeammatesPageLocators.USER_BUTTON,
                                        expected_text=user_name,
                                        expected_text_strict_check=False)

    def click_user_button_by_name(self, user_name: str, match_case: bool = False) -> None:
        self._click_by_element_text(TunePeopleTeamAddTeammatesPageLocators.USER_BUTTON,
                                    user_name, match_case=match_case, expected_text_strict_check=False)

    def click_random_user_button(self) -> None:
        self._click_random_element(TunePeopleTeamAddTeammatesPageLocators.USER_BUTTON)

    def verify_delete_search_bar_input_button(self) -> bool:
        return self._is_visible(TunePeopleTeamAddTeammatesPageLocators.SEARCH_BAR_DELETE_INPUT_BUTTON,
                                timeout=2)

    def verify_loader_not_visible(self) -> bool:
        return self._is_not_visible(TunePeopleTeamAddTeammatesPageLocators.ICON_LOADER, timeout=5)

    def get_all_available_users_elements(self) -> List[WebElement]:
        return self._get_all_available_elements(TunePeopleTeamAddTeammatesPageLocators.USER_BUTTON)

    def input_search_bar(self, data: str) -> None:
        self._send_keys(TunePeopleTeamAddTeammatesPageLocators.SEARCH_BAR, data)

    def wait_users_search(self) -> None:
        self._wait_for_multiple_elements_visibility(
            locator=TunePeopleTeamAddTeammatesPageLocators.USER_BUTTON,
            comparison="<",
            no_elements=10
        )
