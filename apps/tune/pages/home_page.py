from typing import Optional, List

from apps.tune.pages.base_page import TuneBasePage, WebDriver, WebElement
from locators.tune.home_page_locators import TuneHomePageLocators
from datetime import datetime, timedelta

import calendar


class TuneHomePage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_home_tab(self) -> None:
        self._click(TuneHomePageLocators.DASHBOARD_HOME_TAB, skip_exception=True)

    def click_maps_tab(self) -> None:
        self._click(TuneHomePageLocators.DASHBOARD_MAPS_TAB, skip_exception=True)

    def click_device_button_by_name(self, device_name: str) -> None:
        self._click_by_element_text(TuneHomePageLocators.DEVICES_TAB_DEVICE_ITEM, device_name,
                                    expected_text_strict_check=False)

    def verify_device_switch_by_name(self, device_name: str) -> bool:
        element = self._get_element_by_text(
            TuneHomePageLocators.DEVICES_TAB_DEVICE_ITEM, device_name,
            expected_text_strict_check=False
        )
        switch_element = self._get_element_from_element(
            element, TuneHomePageLocators.DEVICES_TAB_DEVICE_ITEM_CHECKBOX)
        return switch_element.is_selected()

    def wait_until_element_switched_by_name(self, device_name: str, switch_value: bool,
                                            timeout: int = 10, skip_exception: bool = False) -> None:
        self._wait_until_statement_is_valid(self.verify_device_switch_by_name, args=(device_name,),
                                            statement_result=switch_value, timeout=timeout,
                                            skip_exception=skip_exception)

    def click_device_switch_by_name(self, device_name: str) -> None:
        element = self._get_element_by_text(
            TuneHomePageLocators.DEVICES_TAB_DEVICE_ITEM, device_name)
        self._get_element_from_element(
            element, TuneHomePageLocators.DEVICES_TAB_DEVICE_ITEM_SWITCH).click()

    def click_sign_in_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_SIGN_IN_BUTTON)

    def click_user_profile_button(self):
        return self._click(TuneHomePageLocators.DASHBOARD_PROFILE_BUTTON, skip_exception=True)

    def click_devices_tab(self) -> None:
        self._click(TuneHomePageLocators.DASHBOARD_DEVICES_TAB, skip_exception=True)

    def click_teammates_in_office(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_OCCUPANCY_LABEL)

    def click_more_options(self) -> None:
        self._click(TuneHomePageLocators.HOME_MORE_OPTIONS_BUTTON)

    def click_update_finished_ok_if_visible(self):
        if self._is_visible(TuneHomePageLocators.UPDATE_SUCCESS, timeout=5):
            self._click(TuneHomePageLocators.UPDATE_SUCCESS)

    def click_settings(self) -> None:
        self._click(TuneHomePageLocators.HOME_SETTINGS_BUTTON)

    def click_about(self) -> None:
        self._click(TuneHomePageLocators.ABOUT_SETTINGS_BUTTON)

    def click_quit(self) -> None:
        self._click(TuneHomePageLocators.HOME_QUIT_BUTTON)

    def click_people_tab(self) -> None:
        self._click(TuneHomePageLocators.DASHBOARD_PEOPLE_TAB)

    def click_supported_devices_button(self) -> None:
        self._click(TuneHomePageLocators.DEVICES_TAB_SUPPORTED_DEVICES_BUTTON)

    def click_book_a_desk_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_BUTTON)

    def click_close_book_a_desk_popup_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_POPUP_CLOSE_BUTTON)

    def click_by_location_and_preferences_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_BY_LOCATION_BUTTON)

    def click_near_a_teammate_button(self) -> None:
        return self._click(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_NEAR_TEAMMATE_BUTTON)

    def click_booking_details_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_DESK_BOOKING_DETAILS_BUTTON)

    def click_show_on_map_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_DETAILS_SHOW_ON_MAPS_BUTTON)

    def click_end_booking_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_DETAILS_END_BOOKING_BUTTON)

    def click_end_booking_confirm_yes_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_DETAILS_END_BOOKING_CONFIRM_YES)

    def click_end_booking_confirm_no_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_DETAILS_END_BOOKING_CONFIRM_NO)

    def click_booking_cancelled_ok_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_CANCELLED_OK_BUTTON)

    def click_booking_edit_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_BOOKING_DETAILS_EDIT_BOOKING_BUTTON)

    def click_notifications_button(self) -> None:
        self._click_with_retry(TuneHomePageLocators.DASHBOARD_NOTIFICATIONS_BUTTON)

    def click_expand_all_day_buttons_visible(self) -> None:
        self._click(TuneHomePageLocators.HOME_ALL_DAY_MEETINGS_EXPAND)

    def click_open_calendar_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_OPEN_CALENDAR_BUTTON)
        # Wait for calendar animation to finish
        self._wait_for_multiple_elements_visibility(
            TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS,
            no_elements=36,
            comparison=">"
        )
        
    def click_close_calendar_button(self) -> None:
        self._click(TuneHomePageLocators.HOME_TAB_CLOSE_CALENDAR_BUTTON)
        # Wait for calendar animation to finish
        self._wait_for_multiple_elements_visibility(
            TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS,
            no_elements=7,
            comparison="=="
        )

    def click_event_details(self, event_name: str):
        self._click_by_element_text(TuneHomePageLocators.HOME_MEETING_CARD_TITLE,
                                    expected_text=event_name)

    def click_refresh_button_and_wait_for_refresh(self) -> bool:
        if self._is_visible(TuneHomePageLocators.DASHBOARD_REFRESH_BUTTON):
            self._click(TuneHomePageLocators.DASHBOARD_REFRESH_BUTTON)
            self.wait_for_page_reload()
            return True
        return False

    def wait_for_page_reload(self) -> None:
        while self._is_visible(TuneHomePageLocators.DASHBOARD_ICON_LOADER, timeout=3):
            pass

    def verify_booking_card_displayed(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_TAB_BOOKING_CARD, timeout=10)

    def verify_booking_card_not_displayed(self) -> bool:
        return self._is_not_visible(TuneHomePageLocators.HOME_TAB_BOOKING_CARD, timeout=5)

    def verify_booking_cards_displayed(self, cards_number: int) -> bool:
        found_cards: List[WebElement] = (
            self._wait_for_multiple_elements_visibility(TuneHomePageLocators.HOME_TAB_BOOKING_CARD,
                                                        no_elements=cards_number,
                                                        comparison="=="))
        return len(found_cards) == cards_number

    def verify_booking_details_button(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_TAB_DESK_BOOKING_DETAILS_BUTTON)

    def verify_sign_in_button_displayed(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_TAB_SIGN_IN_BUTTON, timeout=5)

    def verify_by_location_and_preferences_button_displayed(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_BY_LOCATION_BUTTON)

    def verify_near_a_teammate_button_displayed(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_NEAR_TEAMMATE_BUTTON)

    def verify_device_tab(self) -> bool:
        return self._is_visible(TuneHomePageLocators.DASHBOARD_DEVICES_TAB)

    def verify_people_tab(self) -> bool:
        return self._is_visible(TuneHomePageLocators.DASHBOARD_PEOPLE_TAB)

    def verify_home_tab(self):
        return self._is_visible(TuneHomePageLocators.DASHBOARD_HOME_TAB)

    def verify_notifications_button(self):
        return self._is_visible(TuneHomePageLocators.DASHBOARD_NOTIFICATIONS_BUTTON)

    def verify_user_profile_button(self):
        return self._is_visible(TuneHomePageLocators.DASHBOARD_PROFILE_BUTTON)

    def verify_open_calendar_button(self):
        return self._is_visible(TuneHomePageLocators.HOME_TAB_OPEN_CALENDAR_BUTTON)

    def verify_book_a_desk_button(self) -> None:
        self._is_visible(TuneHomePageLocators.HOME_TAB_BOOK_A_DESK_BUTTON)

    def verify_if_day_calendar_day_is_highlighted(self, day: int, highlighted_color: str) -> bool:
        background_color = self._get_css_value_of_xpath_locator(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV,
                                                                attribute='background-color',
                                                                locator_parameter=str(day))
        return highlighted_color == background_color

    def verify_if_meeting_dot_is_visible_in_day(self, day: int, highlighted_color: str) -> bool:
        background_color = self._get_css_value_of_xpath_locator(
            TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV_DIV,
            attribute='background-color',
            locator_parameter=str(day))
        return highlighted_color == background_color

    def verify_if_day_calendar_has_correct_weekday(self, expected_weekday: str, day: int) -> bool:
        return self._compare_text(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPH,
                                  expected_weekday,
                                  locator_parameter=str(day))

    def verify_if_home_label_is_highlighted(self, highlight_color: str) -> bool:
        home_text_color = self._get_css_value_of_xpath_locator(TuneHomePageLocators.DASHBOARD_HOME_TAB,
                                                               attribute='color')
        return highlight_color == home_text_color

    def verify_title_date_by_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneHomePageLocators.DASHBOARD_TITLE_LABEL, expected_value)

    def verify_basecamp_name(self, expected_value: str) -> bool:
        return self._compare_text(TuneHomePageLocators.HOME_TAB_OCCUPANCY_LABEL, expected_value, False)

    def verify_teammates_by_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneHomePageLocators.HOME_TAB_OCCUPANCY_TEAMMATES, expected_value)

    def verify_calendar_events_titles_incoming(self, expected_titles: List[str]) -> bool:
        return self._verify_all_found_elements_values(
            TuneHomePageLocators.HOME_MEETING_WRAPPER, expected_titles, expected_text_strict_check=False)

    def verify_calendar_events_titles_later(self, expected_titles: List[str]) -> bool:
        return self._verify_all_found_elements_values(
            TuneHomePageLocators.HOME_MEETING_SMALL_TITLE, expected_titles)

    def verify_no_meetings_upcoming(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_MEETING_NO_MEETINGS)

    def verify_non_expanded_calendar_weekdays(self) -> bool:
        return self._verify_all_found_elements_values(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPHS,
                                                      expected_values=list("SMTWTFS"),
                                                      strict_elements_order_check=True,
                                                      boundaries=(0, 7)
                                                      )

    def verify_past_days_disabled(self, day: int) -> bool:
        disabled_days = ['pointer'] * 7
        for index in range(day):
            disabled_days[index] = 'not-allowed'

        return self._verify_all_found_elements_values(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS,
                                                      expected_values=disabled_days,
                                                      parameter_function='value_of_css_property',
                                                      parameter_name='cursor',
                                                      strict_elements_order_check=True,
                                                      boundaries=(0, 7)
                                                      )

    def verify_expanded_calendar_weekdays(self) -> bool:
        return self._verify_all_found_elements_values(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPHS,
                                                      expected_values=list("SMTWTFS"),
                                                      strict_elements_order_check=True,
                                                      boundaries=(7, 14)
                                                      )

    def verify_expanded_calendar_entire_month_is_shown(self) -> bool:
        today: datetime = datetime.now()
        current_day: int = today.day
        current_month: int = today.month
        current_year: int = today.year

        _, current_month_range = calendar.monthrange(current_year, current_month)
        expected_days: List[str] = [str(i) for i in range(current_day, current_month_range + 1)]
        return self._verify_all_found_elements_values(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_DIVS,
                                                      expected_values=expected_days)

    def verify_expanded_calendar_next_30_days_visible(self) -> bool:
        today: datetime = datetime.now()
        date_range: List[str] = [str((today + timedelta(days=i)).day) for i in range(31)]

        return self._verify_all_found_elements_values(TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTON_DIVS,
                                                      expected_values=date_range)

    def verify_expand_all_day_buttons_visible(self) -> bool:
        return self._is_visible(TuneHomePageLocators.HOME_ALL_DAY_MEETINGS_EXPAND)

    def _get_calendar_web_element_by_datetime(self, date: datetime) -> WebElement:
        today = datetime.now().date()
        offset: int = (date.date() - today).days
        elements: List[WebElement] = self._get_all_available_elements(
            TuneHomePageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS,
            boundaries=(7, None)
        )
        today_idx: int = -1
        for idx, val in enumerate(elements):

            if str(today.day) in val.text and today.strftime("%a")[0] in val.text:
                today_idx = idx
                break
        return elements[today_idx + offset]

    def click_calendar_day_by_datetime(self, date: datetime) -> None:

        self._get_calendar_web_element_by_datetime(date).click()

    def verify_if_next_month_is_displayed_on_first_day(self, first_day_next_month: datetime):
        if first_day_next_month.strftime("%U") == datetime.now().strftime("%U"):
            day_abbreviation = first_day_next_month.strftime("%a")[0]
        else:
            day_abbreviation: str = first_day_next_month.strftime("%b")
        res = self._get_calendar_web_element_by_datetime(first_day_next_month).text
        return day_abbreviation in res

    def wait_for_expected_events_to_load(self, events: List):
        return self._wait_for_multiple_elements_presence(TuneHomePageLocators.HOME_MEETING_WRAPPER,
                                                         no_elements=len(events),
                                                         comparison="==")

    def verify_event_scrollable(self, event) -> str:

        element: WebElement = self._scroll_to_element_by_element_text(TuneHomePageLocators.HOME_MEETING_WRAPPER,
                                                                      expected_text=event.get("summary"),
                                                                      expected_text_strict_check=False)
        return element.text

    @staticmethod
    def _get_booking_card_data(booking_card: WebElement) -> dict:
        color = booking_card.value_of_css_property('background-color')
        child_text = [el.text for el in booking_card.find_elements("xpath", ".//p")]
        if len(child_text) == 3:
            desk_name, location_info, timestamps = child_text
            timeleft = None
        else:
            desk_name, timeleft, location_info, timestamps = child_text
        return {
            "desk_name": desk_name,
            "location_info": location_info,
            "timeleft": timeleft,
            "timestamps": timestamps,
            "color": color
        }

    def verify_booking_card_by_index(self, index: int, key: str, value: str, total_cards_number: int):
        found_cards: List[WebElement] = self._wait_for_multiple_elements_visibility(
            TuneHomePageLocators.HOME_TAB_BOOKING_CARD,
            no_elements=total_cards_number)
        if not len(found_cards):
            return False
        card = found_cards[index]
        self._scroll_to_element(card)
        return self._get_booking_card_data(card).get(key) == value

    def get_booking_id_by_index(self, index: int):
        found_cards: List[WebElement] = self._wait_for_multiple_elements_visibility(
            TuneHomePageLocators.HOME_TAB_BOOKING_CARD, comparison=">", no_elements=0)
        if not len(found_cards):
            return None
        card: WebElement = found_cards[index]
        self._scroll_to_element(card)
        booking_id = card.get_attribute('data-testid').split(".")[-1]
        return booking_id

    def get_appearance_mode(self) -> str:
        current_theme = self._get_attribute_of_xpath_locator(TuneHomePageLocators.HTML_MAIN_WINDOW,
                                                             'data-theme')
        return current_theme



