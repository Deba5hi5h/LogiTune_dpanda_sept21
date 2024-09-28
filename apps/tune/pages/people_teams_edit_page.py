from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.people_teams_edit_page_locators import TunePeopleTeamsEditPageLocators


class TunePeopleTeamsEditPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_done_button(self) -> None:
        self._click(TunePeopleTeamsEditPageLocators.DONE_BUTTON)

    def click_delete_team_button_by_name(self, team_name: str) -> None:
        self._click_by_element_text(TunePeopleTeamsEditPageLocators.DELETE_TEAM_BUTTON, team_name)

    def click_random_delete_team_button(self) -> None:
        self._click_random_element(TunePeopleTeamsEditPageLocators.DELETE_TEAM_BUTTON)

    def reorder_teams(self, team_name: str, move_to_index: int) -> None:
        self._reorder_items(TunePeopleTeamsEditPageLocators.TEAM_DIV, team_name,
                            move_to_index, TunePeopleTeamsEditPageLocators.DRAG_TEAM_DIV)

    def click_delete_team_popup_delete(self) -> None:
        self._click(TunePeopleTeamsEditPageLocators.POPUP_DELETE_TEAM_OK_BUTTON)

    def wait_for_team_to_be_removed(self) -> bool:
        return self._is_not_visible(TunePeopleTeamsEditPageLocators.POPUP_DELETE_TEAM_OK_BUTTON)

    def delete_all_teams(self) -> None:
        delete_buttons = self._get_all_available_elements(TunePeopleTeamsEditPageLocators.DELETE_TEAM_BUTTON)
        for delete_button in delete_buttons:
            self._scroll_to_element(delete_button)
            delete_button.click()
            self.click_delete_team_popup_delete()
            self.wait_for_team_to_be_removed()

    def verify_no_teams_found(self) -> bool:
        return bool(self._is_not_visible(TunePeopleTeamsEditPageLocators.DELETE_TEAM_BUTTON, timeout=1))
