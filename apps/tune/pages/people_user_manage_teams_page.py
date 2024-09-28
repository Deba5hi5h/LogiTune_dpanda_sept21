from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_user_manage_teams_page_locators import TunePeopleUserManageTeamsPageLocators


class TunePeopleUserManageTeamsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_done_button(self) -> None:
        self._click(TunePeopleUserManageTeamsPageLocators.DONE_BUTTON)

    def click_new_team_button(self) -> None:
        self._click(TunePeopleUserManageTeamsPageLocators.NEW_TEAM_BUTTON)

    def click_create_team_button(self) -> None:
        self._click(TunePeopleUserManageTeamsPageLocators.POPUP_NEW_TEAM_CREATE_BUTTON)

    def click_close_create_team_button(self) -> None:
        self._click(TunePeopleUserManageTeamsPageLocators.POPUP_NEW_TEAM_CLOSE_BUTTON)

    def click_team_action_button_for_team_with_name(self, team_name: str) -> None:
        self._click_elements_button_by_element_text(TunePeopleUserManageTeamsPageLocators.TEAM_DIV,
                                                    expected_text=team_name,
                                                    button_relative_locator=
                                                    TunePeopleUserManageTeamsPageLocators.TEAM_ACTION_BUTTON_RELATIVE,
                                                    expected_text_strict_check=False,
                                                    )

    def verify_team_visible(self, team_name: str) -> bool:
        return self._is_visible_by_text(TunePeopleUserManageTeamsPageLocators.TEAM_DIV, expected_text=team_name,
                                        expected_text_strict_check=False)

    def verify_teammates_number_for_team(self, team_name: str, teammates_number: int) -> bool:
        expected_teammates_text = f"{teammates_number} teammate{'s' if teammates_number > 1 else ''}"
        team_label = self._get_element_by_text(TunePeopleUserManageTeamsPageLocators.TEAM_DIV,
                                               expected_text_strict_check=False,
                                               expected_text=team_name)
        return expected_teammates_text in team_label.text if team_label else False

    def input_team_name(self, team_name: str) -> None:
        self._delete_input(TunePeopleUserManageTeamsPageLocators.POPUP_NEW_TEAM_INPUT)
        self._send_keys(TunePeopleUserManageTeamsPageLocators.POPUP_NEW_TEAM_INPUT, keys_input=team_name)


