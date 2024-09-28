from typing import Optional, Tuple, List
from datetime import datetime

from selenium.common import TimeoutException

from apps.tune.pages.base_page import TuneBasePage, WebDriver, WebElement
from common.platform_helper import get_custom_platform
from locators.tune.desk_booking_time_selection_page_locators import (
    TuneDeskBookingTimeSelectionPageLocators)
from selenium.webdriver.support.wait import WebDriverWait

import re


class TuneDeskBookingTimeSelectionPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def get_day_background_color(self, date: datetime):
        element = self._get_calendar_web_element_by_datetime(element=TuneDeskBookingTimeSelectionPageLocators.
                                                             CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV_PARAGRAPHS,
                                                             date=date)
        return element.value_of_css_property('background-color')

    def wait_for_background_color_in_element_by_datetime(self, date: datetime,
                                                         awaited_color: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self._driver, 10).until(lambda _: self.get_day_background_color(date) == awaited_color)
            return True
        except TimeoutException:
            return False

    def click_back_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.BACK_BUTTON)

    def click_confirm_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.CONFIRM_BUTTON)

    def click_update_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.UPDATE_BUTTON)

    def click_update_ok_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.BOOKING_UPDATED_OK_BUTTON)

    def click_multiple_tab_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.MULTIPLE_TAB_BUTTON)

    def click_single_tab_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.SINGLE_TAB_BUTTON)

    def set_start_time(self, time: str) -> None:
        self._set_time_by_locator(TuneDeskBookingTimeSelectionPageLocators.TIME_DRAG_START_DIV,
                                  time, is_drag_start_locator=True)

    def set_end_time(self, time: str) -> None:
        self._set_time_by_locator(TuneDeskBookingTimeSelectionPageLocators.TIME_DRAG_END_DIV, time)

    def click_open_calendar_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.OPEN_CALENDAR_BUTTON)
        # Wait for calendar animation to finish
        self._wait_for_multiple_elements_visibility(
            TuneDeskBookingTimeSelectionPageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS, no_elements=36, comparison=">")

    def click_close_calendar_button(self) -> None:
        self._click(TuneDeskBookingTimeSelectionPageLocators.CLOSE_CALENDAR_BUTTON)
        # Wait for calendar animation to finish
        self._wait_for_multiple_elements_visibility(
            TuneDeskBookingTimeSelectionPageLocators.CALENDAR_ELEMENT_BY_DAY_BUTTONS, no_elements=7, comparison="==")

    def get_time_range_label(self) -> str:
        labels = self._get_all_available_elements(
            TuneDeskBookingTimeSelectionPageLocators.TIME_RANGE_LABEL)
        for label in labels:
            if 'AM' in label.text or 'PM' in label.text:
                return label.text

    def parse_time_range_to_valid_text(self, start_time: str, end_time: str) -> str:
        return f'{self._parse_time(start_time)} - {self._parse_time(end_time)}'

    def click_day_in_calendar_by_datetime(self, date: datetime) -> None:
        element = self._get_calendar_web_element_by_datetime(date=date)
        element.click()

    def verify_confirm_button(self) -> bool:
        return self._is_visible(TuneDeskBookingTimeSelectionPageLocators.CONFIRM_BUTTON)

    def _get_calendar_web_element_by_datetime(self, element: Optional[Tuple[str, str]] =
                                              TuneDeskBookingTimeSelectionPageLocators.
                                              CALENDAR_ELEMENT_BY_DAY_BUTTONS,
                                              date: datetime = datetime.now()) -> WebElement:
        today = datetime.now().date()
        offset: int = (date.date() - today).days
        elements: List[WebElement] = self._get_all_available_elements(
            element,
            boundaries=(7, None)
        )
        today_idx: int = -1
        for idx, val in enumerate(elements):
            day = re.search("\d+", val.text)
            if not day:
                continue
            if str(today.day) == day.group():
                today_idx = idx
                break
        return elements[today_idx + offset]

    @staticmethod
    def _parse_time(provided_time: str) -> str:
        time_format = "%#I:%M %p" if get_custom_platform() == "windows" else "%-I:%M %p"
        if 'PM' in provided_time or 'AM' in provided_time:
            return provided_time
        return datetime.strptime(provided_time, '%H:%M').strftime(time_format)

    def check_chosen_times(self, start_time: str, end_time: str) -> bool:
        valid_range = self.parse_time_range_to_valid_text(start_time, end_time)
        return self._compare_text(TuneDeskBookingTimeSelectionPageLocators.TIME_RANGE_LABEL,
                                  valid_range)

    def _set_time_by_locator(self, source_locator: Tuple[str, str], time: str,
                             is_drag_start_locator: bool = False, tuning_retries: int = 30) -> None:
        """
        This method sets the time on the Logi Tune desk booking time selection page by locating the
        source element, calculating the appropriate y-offset, and dragging and dropping the
        source element to the desired timeline.

        Args:
            source_locator: Tuple[str, str]. The locator used to identify the source element.
            time: str. The time to set in the format "HH:MM" or "HH:MM AM/PM".
            is_drag_start_locator: bool, optional. Indicates whether the time is the start time
                                   or the end time of a range. Defaults to False.
           tuning_retries: int, optional. The number of times the tuning for valid element
                           positioning will be attempted.
        """
        source_element = self._wait_until_element_visible(source_locator)
        scroll_visible_area_element = self._wait_until_element_visible(
            TuneDeskBookingTimeSelectionPageLocators.SCROLL_VISIBLE_AREA)
        scroll_area_element = self._wait_until_element_visible(
            TuneDeskBookingTimeSelectionPageLocators.SCROLL_AREA)
        all_lines = self._get_all_available_elements(
            TuneDeskBookingTimeSelectionPageLocators.CALENDAR_LINES)
        time_range_boxes = self._get_all_available_elements(
            TuneDeskBookingTimeSelectionPageLocators.TIME_RANGE_BOX)

        # Getting the valid time range box, which is containing AM/PM text
        time_range_box = [elem for elem in time_range_boxes
                          if 'BOOKED BY YOU' not in elem.text][0]

        # Getting correct timeline from provided time variable and calculating offset from
        # hour timeline for minutes
        time_lines = all_lines[:25]
        hours, minutes = self._parse_time_to_hours_and_minutes(time)
        time_line_y_location = time_lines[hours].location.get('y')
        next_line_y_location = time_lines[hours - 1].location.get('y') if hours != 0 \
            else time_lines[hours + 1].location.get('y')
        time_line_delta = abs(time_line_y_location - next_line_y_location)
        minutes_y_addition = round(minutes / 60 * time_line_delta)

        valid_time = self._parse_time(time)
        set_time = self.get_time_range_label().split('-')
        checked_time = set_time[0].strip() if is_drag_start_locator else set_time[1].strip()
        retry = 0

        while valid_time not in checked_time and retry < tuning_retries:
            self._drag_and_drop_by_coordinates(
                source_element, time_lines[hours], scroll_visible_area_element, scroll_area_element,
                minutes_y_addition, time_range_box, is_drag_start_locator=is_drag_start_locator
            )
            valid_time = self._parse_time(time)
            set_time = self.get_time_range_label().split('-')
            checked_time = set_time[0].strip() if is_drag_start_locator else set_time[1].strip()
            valid_hour, valid_minute = self._parse_time_to_hours_and_minutes(valid_time)
            checked_hour, checked_minute = self._parse_time_to_hours_and_minutes(checked_time)

            # Checking how to drag and drop element, to set correct time
            y_offset = -3 if valid_hour*60+valid_minute < checked_hour*60+checked_minute else 3
            minutes_y_addition += y_offset
            retry += 1

    @staticmethod
    def _parse_time_to_hours_and_minutes(time: str) -> Tuple[int, ...]:
        if 'PM' in time or 'AM' in time:
            time = datetime.strptime(time, '%I:%M %p').strftime('%H:%M')
        return tuple([int(item.strip()) for item in time.split(':')])
