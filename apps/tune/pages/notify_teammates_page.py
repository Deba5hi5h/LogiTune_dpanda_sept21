from typing import Optional
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.notify_teammates_page_locators import TuneNotifyTeammatesPageLocators


class TuneNotifyTeammatesPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_skip_button(self) -> None:
        self._click(TuneNotifyTeammatesPageLocators.SKIP_BUTTON)

    def click_notify_button(self) -> None:
        self._click(TuneNotifyTeammatesPageLocators.NOTIFY_BUTTON)

    def click_clear_button(self) -> None:
        self._click(TuneNotifyTeammatesPageLocators.CLEAR_BUTTON)

    def click_on_teammate_by_name(self, teammate: str) -> None:
        self._click_by_element_text(TuneNotifyTeammatesPageLocators.SELECTION_NAME,
                                    expected_text=teammate,
                                    expected_text_strict_check=False)

    def click_on_team_by_name(self, teammate: str) -> None:
        self._click_by_element_text(TuneNotifyTeammatesPageLocators.TEAM_CARD,
                                    expected_text=teammate,
                                    expected_text_strict_check=False)

    def click_close_team(self) -> None:
        self._click(TuneNotifyTeammatesPageLocators.TEAM_CLOSE_BUTTON)

    def verify_clear_button(self) -> bool:
        return self._is_visible(TuneNotifyTeammatesPageLocators.CLEAR_BUTTON, timeout=3)

    def verify_skip_button(self) -> bool:
        return self._is_visible(TuneNotifyTeammatesPageLocators.SKIP_BUTTON)

    def verify_notify_button(self) -> bool:
        return self._is_visible(TuneNotifyTeammatesPageLocators.NOTIFY_BUTTON)

    def verify_notify_button_text(self, expected_text: str) -> bool:
        return self._compare_text(TuneNotifyTeammatesPageLocators.NOTIFY_BUTTON, expected_text=expected_text)

    def verify_team_by_name(self, team_name: str) -> bool:
        return self._is_visible_by_text(TuneNotifyTeammatesPageLocators.TEAM_CARD,
                                        expected_text=team_name,
                                        expected_text_strict_check=False)

    def check_if_teammate_visible(self, teammate: str) -> bool:
        return self._is_visible_by_text(TuneNotifyTeammatesPageLocators.SELECTION_NAME,
                                        expected_text=teammate)

    def check_if_teammate_checkbox_in_status(self, teammate: str, status: str = 'checked') -> bool:
        return self._wait_for_attribute_in_element_by_text(TuneNotifyTeammatesPageLocators.SELECTION,
                                                           expected_text=teammate,
                                                           attribute_name="data-state",
                                                           attribute_value=status,
                                                           expected_text_strict_check=False)

    def check_if_team_checkbox_in_status(self, team_name: str, status: str = 'checked') -> bool:
        element = self._get_element_by_text(TuneNotifyTeammatesPageLocators.TEAM_CARD,
                                            expected_text=team_name,
                                            expected_text_strict_check=False)
        element_button = self._get_element_from_element(element,
                                                        locator=TuneNotifyTeammatesPageLocators.TEAM_CARD_BUTTON)

        return self._wait_for_attribute_in_element(element_button, attribute_name='data-state', attribute_value=status)

    def clear_optional_message(self) -> None:
        self._delete_input_manually(TuneNotifyTeammatesPageLocators.OPTIONAL_MESSAGE_TEXT_AREA)

    def write_optional_message(self, message: str) -> None:
        self._send_keys(TuneNotifyTeammatesPageLocators.OPTIONAL_MESSAGE_TEXT_AREA, keys_input=message)



