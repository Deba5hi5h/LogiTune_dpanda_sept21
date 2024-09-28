from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_team_edit_page_locators import TunePeopleTeamEditPageLocators


class TunePeopleTeamEditPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_done_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.DONE_BUTTON)

    def click_edit_team_name_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.EDIT_NAME_BUTTON)

    def click_popup_close_edit_team_name_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.POPUP_EDIT_NAME_CLOSE_BUTTON)

    def click_popup_update_team_name_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.POPUP_EDIT_NAME_UPDATE_BUTTON)

    def click_delete_user_button_by_name(self, user_name: str) -> None:
        self._click_by_element_text(TunePeopleTeamEditPageLocators.DELETE_USER_BUTTON, user_name)

    def click_random_delete_user_button(self) -> None:
        self._click_random_element(TunePeopleTeamEditPageLocators.DELETE_USER_BUTTON)

    def click_delete_team_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.DELETE_TEAM_BUTTON)

    def click_popup_delete_team_delete_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.POPUP_DELETE_TEAM_DELETE_BUTTON)

    def click_popup_delete_team_cancel_button(self) -> None:
        self._click(TunePeopleTeamEditPageLocators.POPUP_DELETE_TEAM_CANCEL_BUTTON)

    def input_team_name(self, team_name: str) -> None:
        self._delete_input(TunePeopleTeamEditPageLocators.POPUP_EDIT_NAME_INPUT)
        self._send_keys(TunePeopleTeamEditPageLocators.POPUP_EDIT_NAME_INPUT, team_name)

    def verify_team_name(self, team_name: str) -> bool:
        return self._compare_text(TunePeopleTeamEditPageLocators.EDIT_NAME_BUTTON, team_name)

    def verify_update_team_button_enabled(self) -> bool:
        return self._is_clickable(TunePeopleTeamEditPageLocators.POPUP_EDIT_NAME_UPDATE_BUTTON, timeout=1)

    def delete_all_teammates(self) -> bool:
        teammates = self._wait_for_multiple_elements_presence(
            locator=TunePeopleTeamEditPageLocators.DELETE_USER_BUTTON,
            comparison=">",
            no_elements=0
        )
        for teammate in teammates:
            self._scroll_to_element(teammate)
            teammate.click()

        return self._is_not_visible(TunePeopleTeamEditPageLocators.DELETE_USER_BUTTON)

    def wait_for_team_to_be_deleted(self) -> None:
        self._is_not_visible(TunePeopleTeamEditPageLocators.POPUP_DELETE_TEAM_CANCEL_BUTTON)
