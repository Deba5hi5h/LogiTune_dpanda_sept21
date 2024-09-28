from typing import List, Optional, Tuple
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.desk_booking_page_locators import TuneDeskBookingPageLocators
import cv2
import numpy as np

class TuneDeskBookingPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.BACK_BUTTON)

    def click_book_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.BOOK_BUTTON)

    def click_popup_validation_error_ok_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.POPUP_VALIDATION_ERROR_OK_BUTTON)

    def click_collapsable_desks_list(self, parameter: str) -> None:
        self._click(TuneDeskBookingPageLocators.COLLAPSABLE_DESKS_LIST, locator_parameter=parameter)

    def click_book_a_desk_date_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.DATE_SELECT_BUTTON)

    def click_book_a_desk_date_option_by_text(self, option_text: str) -> None:
        self._click_by_element_text(TuneDeskBookingPageLocators.DATE_SELECT_OPTION_BUTTON,
                                    option_text)

    def click_book_a_desk_start_session_time_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.TIME_START_BUTTON)

    def click_book_a_desk_start_session_time_by_text(self, option_text: str) -> None:
        self._click_by_element_text(TuneDeskBookingPageLocators.TIME_START_OPTION_BUTTON,
                                    option_text)

    def click_book_a_desk_end_session_time_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.TIME_END_BUTTON)

    def click_multiple_booking_confirm_popup_confirm(self) -> None:
        self._click(TuneDeskBookingPageLocators.MULTIPLE_BOOKING_CONFIRM_POPUP_CONFIRM_BUTTON)

    def click_multiple_booking_cancel_popup_confirm(self) -> None:
        self._click(TuneDeskBookingPageLocators.MULTIPLE_BOOKING_CONFIRM_POPUP_CANCEL_BUTTON)

    def click_book_a_desk_end_session_time_by_text(self, option_text: str) -> None:
        self._click_by_element_text(TuneDeskBookingPageLocators.TIME_END_OPTION_BUTTON,
                                    option_text)

    def click_book_a_desk_office_location_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.OFFICE_LOCATION_BUTTON)

    def click_book_a_desk_floor_location_button(self) -> None:
        self._click(TuneDeskBookingPageLocators.FLOOR_LOCATION_BUTTON)

    def click_desk_by_desk_name(self, desk_name: str) -> None:
        self._is_clickable_by_text(TuneDeskBookingPageLocators.COLLAPSED_DESK_CHECKBOX, desk_name)
        self._click_by_element_text(TuneDeskBookingPageLocators.COLLAPSED_DESK_CHECKBOX, desk_name)

    def get_book_a_desk_date_text(self) -> str:
        return self._get_text(TuneDeskBookingPageLocators.DATE_SELECT_BUTTON)

    def get_book_a_desk_start_session_time_text(self) -> str:
        return self._get_text(TuneDeskBookingPageLocators.TIME_START_BUTTON)

    def get_book_a_desk_end_session_time_text(self) -> str:
        return self._get_text(TuneDeskBookingPageLocators.TIME_END_BUTTON)

    def get_book_a_desk_office_location_text(self) -> str:
        return self._get_text(TuneDeskBookingPageLocators.OFFICE_LOCATION_BUTTON)

    def get_book_a_desk_floor_location_text(self) -> str:
        return self._get_text(TuneDeskBookingPageLocators.FLOOR_LOCATION_BUTTON)

    def verify_validation_error_popup_displayed(self) -> bool:
        return self._is_visible(TuneDeskBookingPageLocators.POPUP_VALIDATION_ERROR_TITLE_LABEL)

    def verify_default_book_a_desk_date_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.DATE_SELECT_BUTTON, expected_value)

    def verify_default_book_a_desk_start_session_time_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.TIME_START_BUTTON, expected_value)

    def verify_default_book_a_desk_end_session_time_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.TIME_END_BUTTON, expected_value)

    def verify_default_book_a_desk_office_location_text(self, expected_value: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.OFFICE_LOCATION_BUTTON,
                                  expected_value)

    def verify_book_a_desk_date_options_by_text(self, expected_values: List[str]) -> bool:
        return self._verify_all_found_elements_values(
            TuneDeskBookingPageLocators.DATE_SELECT_OPTION_BUTTON, expected_values)

    def verify_book_a_desk_start_session_time_by_text(self, expected_values: List[str]) -> bool:
        return self._verify_all_found_elements_values(
            TuneDeskBookingPageLocators.TIME_START_OPTION_BUTTON, expected_values)

    def verify_book_a_desk_end_session_times_by_text(self, expected_values: List[str]) -> bool:
        return self._verify_all_found_elements_values(
            TuneDeskBookingPageLocators.TIME_END_OPTION_BUTTON, expected_values)

    def verify_collapsable_desks_list(self, parameter: str) -> bool:
        return self._is_visible(TuneDeskBookingPageLocators.COLLAPSABLE_DESKS_LIST, locator_parameter=parameter)

    def verify_desk_details_button_displayed(self) -> bool:
        return self._is_visible(TuneDeskBookingPageLocators.DETAILS_BUTTON)

    def verify_no_desks_available_label(self) -> bool:
        if self._is_visible(TuneDeskBookingPageLocators.NO_DESK_AVAILABLE_POPUP_MSG):
            self._click(TuneDeskBookingPageLocators.NO_DESK_AVAILABLE_POPUP_BUTTON)
            return True
        return False

    def verify_desk_by_desk_name(self, desk_name: str) -> bool:
        return self._is_clickable_by_text(TuneDeskBookingPageLocators.COLLAPSED_DESK_CHECKBOX, desk_name, timeout=2)

    def select_floor_by_text(self, floor: str) -> None:
        self._click_by_element_text(TuneDeskBookingPageLocators.FLOOR_SELECT_BUTTON,
                                    expected_text=floor,
                                    expected_text_strict_check=False)

    def check_multiple_booking_popup_title(self, title: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.MULTIPLE_BOOKING_CONFIRM_POPUP_TITLE,
                                  expected_text=title,
                                  strict_text_check=False)

    def verify_map_visible(self) -> bool:
        return self._is_visible(TuneDeskBookingPageLocators.MAP_CANVAS)

    def click_area_by_name(self, area_name: str) -> None:
        self._click_by_element_text(TuneDeskBookingPageLocators.AREA_BUTTON, area_name,
                                    expected_text_strict_check=False)

    def verify_current_desk_name(self, expected_desk_name: str) -> bool:
        return self._compare_text(TuneDeskBookingPageLocators.SELECTED_DESK_POPUP_NAME,
                                  expected_text=expected_desk_name)

    def click_on_desk_canvas_by_name(self, area_name: str, desk_name: str) -> bool:
        self.click_area_by_name(area_name)
        self.wait_seconds_to_pass(2)
        canvas = self._get_all_available_elements(TuneDeskBookingPageLocators.MAP_CANVAS)[0].wrapped_element
        available_desks_coords = self._find_green_circles_on_element(canvas)
        for cords in available_desks_coords:
            self.click_area_by_name(area_name)
            self.wait_seconds_to_pass(3)
            self._click_on_element_with_offset(canvas, cords)
            if self.verify_current_desk_name(desk_name):
                return True
        return False




