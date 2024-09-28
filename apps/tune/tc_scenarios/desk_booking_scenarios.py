import random
import time
from datetime import datetime, timedelta
from datetime import time as dt_time
from typing import Tuple

from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from common.framework_params import COILY_BASECAMP_NAME
from common.platform_helper import (change_datetime_to_am_pm_string,
                                    create_am_pm_times_list_until_eod, create_dates_list)
from extentreport.report import Report


class DeskBookingScenarios(WorkAccountScenarios):

    def tc_verify_book_a_desk_pop_up_controls(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_book_a_desk_button()
        try:
            button = self.tune_pages.home.verify_by_location_and_preferences_button_displayed()
            self._assert(
                condition=button,
                log_pass='Button "By location and preferences" is visible on "Book a desk" popup',
                log_fail='"By location and preferences" button is not visible '
                         'on "Book a desk" popup.'
            )
            self._assert(
                condition=self.tune_pages.home.verify_near_a_teammate_button_displayed(),
                log_pass='Button "Near a teammate" is visible on "Book a desk" popup',
                log_fail='"Near a teammate" button is not visible on "Book a desk" popup.'
            )
            Report.logPass('"Book a desk" popup controls has been verified successfully!')
        finally:
            self.tune_pages.home.click_close_book_a_desk_popup_button()

    def tc_verify_book_a_desk_page_default_options(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_book_a_desk_button()
        self.tune_pages.home.click_by_location_and_preferences_button()
        try:
            date = 'Today'
            self._assert(
                condition=self.tune_pages.desk_booking.verify_default_book_a_desk_date_text(date),
                log_pass=f'Date button have valid value: {date}',
                log_fail=f'"Book a desk" date button have different default value than expected - '
                         f'Expected: {date}; Observed: '
                         f'{self.tune_pages.desk_booking.get_book_a_desk_date_text()}')

            formatted_start_time = change_datetime_to_am_pm_string(datetime.now())
            start = self.tune_pages.desk_booking.verify_default_book_a_desk_start_session_time_text(
                formatted_start_time)
            self._assert(
                condition=start,
                log_pass=f'Start session time button have expected value: {formatted_start_time}',
                log_fail=f'"Book a desk" start session time button have different default value '
                         f'than expected - Expected: {formatted_start_time}; Observed: '
                         f'{self.tune_pages.desk_booking.get_book_a_desk_start_session_time_text()}'
            )

            formatted_end_time = change_datetime_to_am_pm_string(dt_time(hour=17))
            end_dt = self.tune_pages.desk_booking.verify_default_book_a_desk_end_session_time_text(
                formatted_end_time)
            self._assert(
                condition=end_dt,
                log_pass=f'End session time button have expected value: {formatted_end_time}',
                log_fail=f'"Book a desk" end session time button have different default value than '
                         f'expected - Expected: {formatted_end_time}; Observed: '
                         f'{self.tune_pages.desk_booking.get_book_a_desk_end_session_time_text()}'
            )

            formatted_basecamp = COILY_BASECAMP_NAME.title()
            location = self.tune_pages.desk_booking.verify_default_book_a_desk_office_location_text(
                formatted_basecamp)
            self._assert(
                condition=location,
                log_pass=f'Office location button have expected value: {formatted_basecamp}',
                log_fail=f'"Book a desk" office location button have different default value than '
                         f'expected - Expected: {formatted_basecamp}; Observed: '
                         f'{self.tune_pages.desk_booking.get_book_a_desk_office_location_text()}'
            )

            # self.tune_pages.desk_booking.click_collapsable_desks_list()
            # TODO: Main floor check
            # TODO: 3a How to check which desk is the first desk?
            # TODO: 3b Implement API reservation by another account
            #  (how many account's will be needed for testing purposes of each suite)
            self._assert(
                condition=self.tune_pages.desk_booking.verify_desk_details_button_displayed(),
                log_pass='"Desk details" button is displayed as expected',
                log_fail='"Desk details" button is not displayed properly'
            )
            Report.logPass('"Book a desk" page options have been verified successfully!')
        finally:
            self.tune_pages.desk_booking.click_back_button()

    def tc_verify_book_a_desk_page_inner_options(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_book_a_desk_button()
        self.tune_pages.home.click_by_location_and_preferences_button()
        timestamp = datetime.now()
        try:
            dates_strings = create_dates_list(timestamp + timedelta(days=2), '%a, %b %d', 29)
            valid_dates_options = ['Today', 'Tomorrow', *dates_strings]
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self._assert(
                condition=self.tune_pages.desk_booking.verify_book_a_desk_date_options_by_text(
                    valid_dates_options),
                log_pass=f'All options shown correctly: {dates_strings}',
                log_fail='Not every option has been shown in the list'
            )
            self.tune_pages.desk_booking.click_book_a_desk_date_option_by_text(
                valid_dates_options[0])

            start_hours_options = create_am_pm_times_list_until_eod(timestamp)
            self.tune_pages.desk_booking.click_book_a_desk_start_session_time_button()
            start_time = self.tune_pages.desk_booking.verify_book_a_desk_start_session_time_by_text(
                start_hours_options)
            self._assert(
                condition=start_time,
                log_pass=f'All options shown correctly: {start_hours_options}',
                log_fail='Not every option has been shown in the list'
            )
            self.tune_pages.desk_booking.click_book_a_desk_start_session_time_by_text(
                start_hours_options[0])

            end_timestamp = timestamp + timedelta(minutes=30 + (15 - timestamp.minute % 15))
            end_hours_options = create_am_pm_times_list_until_eod(end_timestamp)
            self.tune_pages.desk_booking.click_book_a_desk_end_session_time_button()
            self._assert(
                condition=self.tune_pages.desk_booking.verify_book_a_desk_end_session_times_by_text(
                    end_hours_options),
                log_pass=f'All options shown correctly: {end_hours_options}',
                log_fail='Not every option has been shown in the list'
            )
            self.tune_pages.desk_booking.click_book_a_desk_end_session_time_by_text(
                end_hours_options[0])

            self.tune_pages.desk_booking.click_book_a_desk_office_location_button()
            Report.logPass('"Book a desk" page inner options have been verified successfully!')
        finally:
            self.tune_pages.desk_booking.click_back_button()

    def tc_book_a_desk(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_book_a_desk_button()
        self.tune_pages.home.click_by_location_and_preferences_button()
        self.tune_pages.desk_booking.click_book_button()
        try:
            error_displayed = self.tune_pages.desk_booking.verify_validation_error_popup_displayed()
            self._assert(
                condition=not error_displayed,
                log_pass='There is no Validation Error popup - continuing',
                log_fail='Unable to book a desk - Validation Error occurred')
        except AssertionError as e:
            self.tune_pages.desk_booking.click_popup_validation_error_ok_button()
            self.tune_pages.desk_booking.click_back_button()
            raise e
        self.tune_pages.notify_teammates.click_skip_button()
        self.tune_pages.desk_successfully_booked.click_done_button()
        self._assert(
            condition=self.tune_pages.home.verify_booking_card_displayed(),
            log_pass='Booking card is shown after booking the desk - desk booked successfully!',
            log_fail='Booking card not visible after booking the desk'
        )

    def tc_end_occupying_of_the_desk(self) -> None:
        self._assert(
            condition=self.tune_pages.home.verify_booking_card_displayed(),
            log_pass='Booking card is present in Home tab',
            log_fail='There is no pending booking for current user'
        )
        self._end_occupying_of_the_desk()
        time.sleep(2)
        self._assert(
            condition=not self.tune_pages.home.verify_booking_card_displayed(),
            log_pass='Booking card is not visible after ending occupying the desk',
            log_fail='Booking card still visible after ending occupying the desk'
        )

    def tc_set_random_desk_booking_time_range(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_book_a_desk_button()
        self.tune_pages.home.click_by_location_and_preferences_button()
        self.tune_pages.desk_booking.click_book_a_desk_date_button()

        start_time, end_time = self._create_random_time_range()

        Report.logInfo(f'Trying to set end time to {end_time}')
        self.tune_pages.desk_booking_time_selection.set_end_time(end_time)
        Report.logInfo(f'Trying to set start time to {start_time}')
        self.tune_pages.desk_booking_time_selection.set_start_time(start_time)

        expected_time = self.tune_pages.desk_booking_time_selection.parse_time_range_to_valid_text(
            start_time, end_time)
        observed_time = self.tune_pages.desk_booking_time_selection.get_time_range_label()

        self._assert(
            condition=self.tune_pages.desk_booking_time_selection.check_chosen_times(
                start_time, end_time),
            log_pass=f'Booking time selection was set as expected - {expected_time}',
            log_fail=f'Booking time was not set as expected! Expected: {expected_time}, '
                     f'Observed: {observed_time}'
        )
        self.tune_pages.desk_booking_time_selection.click_confirm_button()
        book_a_desk_time = self.tune_pages.desk_booking.get_book_a_desk_date_text()
        self._assert(
            condition=expected_time in book_a_desk_time,
            log_pass=f'Booking time label shows correct time - {book_a_desk_time}',
            log_fail=f'Booking time label doesn\'t show correct time! Expected: {expected_time}, '
                     f'Observed: {book_a_desk_time} (checking only time range string)'
        )

    @staticmethod
    def _create_random_time_range() -> Tuple[str, str]:
        current_time = datetime.now()
        min_hour = current_time.hour if current_time.minute < 45 else current_time.hour + 1
        start_time_h = random.choice(range(min_hour, min(min_hour + 8, 22)))
        if start_time_h == current_time.hour:
            start_time_m = current_time.minute
            while start_time_m <= current_time.minute:
                start_time_m = random.choice(range(0, 60, 15))
        else:
            start_time_m = random.choice(range(0, 60, 15))
        end_time_h = random.choice(range(start_time_h, 23)) if start_time_m < 30 \
            else random.choice(range(start_time_h + 1, 23))
        end_time_m = random.choice(range(0, 60, 15))
        while end_time_h * 60 + end_time_m < start_time_h * 60 + start_time_m + 30:
            end_time_m = random.choice(range(0, 60, 15))
        start_time = f"{start_time_h:02d}:{start_time_m:02d}"
        end_time = f"{end_time_h:02d}:{end_time_m:02d}"
        return start_time, end_time
