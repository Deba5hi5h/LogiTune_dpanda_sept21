import random
from datetime import datetime, timedelta

from apps.tune.base.desk_booking_base import Account
from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from common.platform_helper import tune_time_format_from_datetime_obj
from extentreport.report import Report


class MultipleDayBookingScenarios(WorkAccountScenarios):

    def tc_book_multiple_day_booking(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.click_multiple_tab_button()

            multiple_day_booking_number = random.randint(3, 6)
            Report.logInfo(f"Creating a multiple day booking "
                           f"with randomly generated days: {multiple_day_booking_number + 1}")

            days_to_book = [datetime.now() + timedelta(days=i) for i in range(multiple_day_booking_number + 1)]
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            for day in days_to_book[::-1]:
                day_formatted = day.strftime('%B-%d')
                Report.logInfo(f"Clicking day in calendar {day_formatted}")
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(day)
                if days_to_book.index(day) != 0:
                    Report.logInfo(f"Checking if day {day_formatted} is highlighted after click")
                    self._assert(
                        condition=self.tune_pages.desk_booking_time_selection.
                        wait_for_background_color_in_element_by_datetime(day, self.tune_colors.color_calendar_hover),
                        log_pass=f"Clicked day ({day_formatted}) has effect with hovered background",
                        log_fail=f"Clicked day ({day_formatted} has no effect with hovered background"
                    )
            self.tune_pages.desk_booking_time_selection.click_close_calendar_button()

            start_time = datetime.now().replace(minute=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)

            start_time_tune = tune_time_format_from_datetime_obj(start_time)
            end_time_tune = tune_time_format_from_datetime_obj(end_time)
            Report.logInfo(f"Selecting timestamps: {start_time_tune} - {end_time_tune}")

            self.tune_pages.desk_booking_time_selection.set_end_time(time=end_time_tune)
            self.tune_pages.desk_booking_time_selection.set_start_time(time=start_time_tune)
            Report.logInfo("Clicking confirm button")
            self.tune_pages.desk_booking_time_selection.click_confirm_button()
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Clicking OK in multiple-day booking select PopUp")
            self.tune_pages.desk_booking.click_multiple_booking_confirm_popup_confirm()
            Report.logInfo("Skipping notify teammates")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done button")
            self.tune_pages.desk_successfully_booked.click_done_button()

            for day in days_to_book[1:]:
                Report.logInfo(f"Selecting day {day.strftime('%B-%d')}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(day)
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

                Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                                total_cards_number=1),
                    log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                    log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
                )


                Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                                total_cards_number=1),
                    log_fail=f"Location: {self.location} is not visible on Booking Card",
                    log_pass=f"Location: {self.location} is visible on Booking Card"
                )

                timestamps = f"{start_time_tune} - {end_time_tune}"

                Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                                total_cards_number=1),
                    log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                    log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
                )

                Report.logInfo(f"Checking if booking is highlighted with correct color")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "color",
                                                                                self.tune_colors.color_future_not_today,
                                                                                total_cards_number=1),
                    log_fail=f"Booking card is not highlighted with correct color",
                    log_pass=f"Booking card is highlighted with correct color"
                )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_book_multiple_day_booking_edit_one_booking(self) -> None:
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.click_multiple_tab_button()

            multiple_day_booking_number = random.randint(3, 6)
            Report.logInfo(f"Creating a multiple day booking "
                           f"with randomly generated days: {multiple_day_booking_number + 1}")

            days_to_book = [datetime.now() + timedelta(days=i) for i in range(multiple_day_booking_number + 1)]
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            for day in days_to_book[::-1]:
                day_formatted = day.strftime('%B-%d')
                Report.logInfo(f"Clicking day in calendar {day_formatted}")
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(day)
                if days_to_book.index(day) != 0:
                    Report.logInfo(f"Checking if day {day_formatted} is highlighted after click")
                    self._assert(
                        condition=self.tune_pages.desk_booking_time_selection.
                        wait_for_background_color_in_element_by_datetime(day, self.tune_colors.color_calendar_hover),
                        log_pass=f"Clicked day ({day_formatted}) has effect with hovered background",
                        log_fail=f"Clicked day ({day_formatted} has no effect with hovered background"
                    )
            self.tune_pages.desk_booking_time_selection.click_close_calendar_button()

            start_time = datetime.now().replace(minute=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)

            start_time_tune = tune_time_format_from_datetime_obj(start_time)
            end_time_tune = tune_time_format_from_datetime_obj(end_time)
            Report.logInfo(f"Selecting timestamps: {start_time_tune} - {end_time_tune}")

            self.tune_pages.desk_booking_time_selection.set_end_time(time=end_time_tune)
            self.tune_pages.desk_booking_time_selection.set_start_time(time=start_time_tune)
            Report.logInfo("Clicking confirm button")
            self.tune_pages.desk_booking_time_selection.click_confirm_button()
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Clicking OK in multiple-day booking select PopUp")
            self.tune_pages.desk_booking.click_multiple_booking_confirm_popup_confirm()
            Report.logInfo("Skipping notify teammates")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done button")
            self.tune_pages.desk_successfully_booked.click_done_button()

            book_to_edit = random.choice(days_to_book[1:])
            book_to_edit_formatted = book_to_edit.strftime("%B-%d")
            Report.logInfo(f"Editing randomly selected day with booked desk {book_to_edit_formatted}")
            self.tune_pages.home.click_open_calendar_button()
            Report.logInfo(f"Selecting day in calendar: {book_to_edit_formatted}")
            self.tune_pages.home.click_calendar_day_by_datetime(book_to_edit)
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_booking_details_button()
            self.tune_pages.home.click_booking_edit_button()
            edited_start_time = tune_time_format_from_datetime_obj(start_time - timedelta(minutes=15))
            Report.logInfo("Setting new start time {edited_start_time}")
            self.tune_pages.desk_booking_time_selection.set_start_time(time=edited_start_time)
            self.tune_pages.desk_booking_time_selection.click_update_button()
            self.tune_pages.desk_booking_time_selection.click_update_ok_button()

            for day in days_to_book[1:]:
                Report.logInfo(f"Selecting day {day.strftime('%B-%d')}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(day)
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

                is_edited = day is book_to_edit

                timestamps = f"{edited_start_time if is_edited else start_time_tune} - {end_time_tune}"

                Report.logInfo(f"Checking if correct {'edited' if is_edited else ''}timestamps: "
                               f"{timestamps} are visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                                total_cards_number=1),
                    log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                    log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
                )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_book_multiple_day_booking_delete_one_booking(self) -> None:
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.click_multiple_tab_button()

            multiple_day_booking_number = random.randint(3, 6)
            Report.logInfo(f"Creating a multiple day booking "
                           f"with randomly generated days: {multiple_day_booking_number + 1}")

            days_to_book = [datetime.now() + timedelta(days=i) for i in range(multiple_day_booking_number + 1)]
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            for day in days_to_book[::-1]:
                day_formatted = day.strftime('%B-%d')
                Report.logInfo(f"Clicking day in calendar {day_formatted}")
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(day)
                if days_to_book.index(day) != 0:
                    Report.logInfo(f"Checking if day {day_formatted} is highlighted after click")
                    self._assert(
                        condition=self.tune_pages.desk_booking_time_selection.
                        wait_for_background_color_in_element_by_datetime(day, self.tune_colors.color_calendar_hover),
                        log_pass=f"Clicked day ({day_formatted}) has effect with hovered background",
                        log_fail=f"Clicked day ({day_formatted} has no effect with hovered background"
                    )
            self.tune_pages.desk_booking_time_selection.click_close_calendar_button()

            start_time = datetime.now().replace(minute=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)

            start_time_tune = tune_time_format_from_datetime_obj(start_time)
            end_time_tune = tune_time_format_from_datetime_obj(end_time)
            Report.logInfo(f"Selecting timestamps: {start_time_tune} - {end_time_tune}")

            self.tune_pages.desk_booking_time_selection.set_end_time(time=end_time_tune)
            self.tune_pages.desk_booking_time_selection.set_start_time(time=start_time_tune)
            Report.logInfo("Clicking confirm button")
            self.tune_pages.desk_booking_time_selection.click_confirm_button()
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Clicking OK in multiple-day booking select PopUp")
            self.tune_pages.desk_booking.click_multiple_booking_confirm_popup_confirm()
            Report.logInfo("Skipping notify teammates")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done button")
            self.tune_pages.desk_successfully_booked.click_done_button()

            book_to_delete = random.choice(days_to_book[1:])
            book_to_edit_formatted = book_to_delete.strftime("%B-%d")
            Report.logInfo(f"Deleting randomly selected day with booked desk {book_to_edit_formatted}")
            self.tune_pages.home.click_open_calendar_button()
            Report.logInfo(f"Selecting day in calendar: {book_to_edit_formatted}")
            self.tune_pages.home.click_calendar_day_by_datetime(book_to_delete)
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_booking_details_button()
            self.tune_pages.home.click_end_booking_button()
            self.tune_pages.home.click_end_booking_confirm_yes_button()
            self.tune_pages.home.click_booking_cancelled_ok_button()

            for day in days_to_book[1:]:
                day_formatted = day.strftime("%B-%d")
                Report.logInfo(f"Selecting day {day_formatted}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(day)
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

                is_deleted = day is book_to_delete
                if is_deleted:
                    self._assert(
                        condition=self.tune_pages.home.verify_booking_card_not_displayed(),
                        log_pass=f"Deleted booking on {day_formatted} is not visible as intended",
                        log_fail=f"Deleted booking on {day_formatted} is visible which is NOK"
                    )
                    continue

                Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                                total_cards_number=1),
                    log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                    log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
                )


                Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                                total_cards_number=1),
                    log_fail=f"Location: {self.location} is not visible on Booking Card",
                    log_pass=f"Location: {self.location} is visible on Booking Card"
                )

                timestamps = f"{start_time_tune} - {end_time_tune}"

                Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                                total_cards_number=1),
                    log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                    log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
                )

                Report.logInfo(f"Checking if booking is highlighted with correct color")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "color",
                                                                                self.tune_colors.color_future_not_today,
                                                                                total_cards_number=1),
                    log_fail=f"Booking card is not highlighted with correct color",
                    log_pass=f"Booking card is highlighted with correct color"
                )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_book_multiple_day_booking_max_days_in_advance(self, credentials: Account) -> None:

        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.click_multiple_tab_button()

            random_max_days_in_advance = random.randint(3, 6)

            Report.logInfo(f"Changing max days in advance number to random with value: {random_max_days_in_advance}")

            dia_changed = self.sync_api_methods.change_max_days_in_advance(self.desk_id, random_max_days_in_advance)

            self._assert(
                condition=dia_changed,
                log_fail=f"Days in advance change to: {random_max_days_in_advance} failed",
                log_pass=f"Successfully changed max days in advance to value: {random_max_days_in_advance}",
            )

            self.tune_pages.home.wait_seconds_to_pass(10)
            days_to_book_allowed = [datetime.now() + timedelta(days=i) for i in range(random_max_days_in_advance)]
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            for day in days_to_book_allowed[::-1]:
                day_formatted = day.strftime('%B-%d')
                Report.logInfo(f"Clicking day in calendar {day_formatted}")
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(day)
                if days_to_book_allowed.index(day) != 0:
                    Report.logInfo(f"Checking if day {day_formatted} is highlighted after click")
                    self._assert(
                        condition=self.tune_pages.desk_booking_time_selection.
                        wait_for_background_color_in_element_by_datetime(day, self.tune_colors.color_calendar_hover),
                        log_pass=f"Clicked day ({day_formatted}) has effect with hovered background",
                        log_fail=f"Clicked day ({day_formatted} has no effect with hovered background"
                    )
            self.tune_pages.desk_booking_time_selection.click_close_calendar_button()

            start_time = datetime.now().replace(minute=0) + timedelta(hours=1)
            end_time = start_time + timedelta(hours=2)

            start_time_tune = tune_time_format_from_datetime_obj(start_time)
            end_time_tune = tune_time_format_from_datetime_obj(end_time)
            Report.logInfo(f"Selecting timestamps: {start_time_tune} - {end_time_tune}")

            self.tune_pages.desk_booking_time_selection.set_end_time(time=end_time_tune)
            self.tune_pages.desk_booking_time_selection.set_start_time(time=start_time_tune)
            Report.logInfo("Clicking confirm button")
            self.tune_pages.desk_booking_time_selection.click_confirm_button()
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Clicking OK in multiple-day booking select PopUp")
            self.tune_pages.desk_booking.click_multiple_booking_confirm_popup_confirm()
            Report.logInfo("Skipping notify teammates")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            for day in days_to_book_allowed[1:]:
                day_formatted = day.strftime("%B-%d")
                Report.logInfo(f"Selecting day {day_formatted}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(day)
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

                Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                                total_cards_number=1),
                    log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                    log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
                )

                Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                                total_cards_number=1),
                    log_fail=f"Location: {self.location} is not visible on Booking Card",
                    log_pass=f"Location: {self.location} is visible on Booking Card"
                )

                timestamps = f"{start_time_tune} - {end_time_tune}"

                Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                                total_cards_number=1),
                    log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                    log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
                )

                Report.logInfo(f"Checking if booking is highlighted with correct color")
                self._assert(
                    condition=self.tune_pages.home.verify_booking_card_by_index(0, "color",
                                                                                self.tune_colors.color_future_not_today,
                                                                                total_cards_number=1),
                    log_fail=f"Booking card is not highlighted with correct color",
                    log_pass=f"Booking card is highlighted with correct color"
                )
            Report.logInfo(f"Deleting Bookings and events for user: "
                           f"{credentials.get('signin_payload').get('email')}")

            self.sync_api_methods.delete_reservations_for_user(
                credentials.get('signin_payload').get('identifier'))

            days_to_book_not_allowed = [datetime.now() +
                                        timedelta(days=i) for i in range(random_max_days_in_advance + 2)]
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_calendar_day_by_datetime(datetime.now())
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.click_multiple_tab_button()
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            for day in days_to_book_not_allowed[::-1]:
                day_formatted = day.strftime('%B-%d')
                Report.logInfo(f"Clicking day in calendar {day_formatted}")
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(day)
                if days_to_book_not_allowed.index(day) != 0:
                    Report.logInfo(f"Checking if day {day_formatted} is highlighted after click")
                    self._assert(
                        condition=self.tune_pages.desk_booking_time_selection.
                        wait_for_background_color_in_element_by_datetime(day, self.tune_colors.color_calendar_hover),
                        log_pass=f"Clicked day ({day_formatted}) has effect with hovered background",
                        log_fail=f"Clicked day ({day_formatted} has no effect with hovered background"
                    )

            self.tune_pages.desk_booking_time_selection.click_close_calendar_button()
            Report.logInfo(f"Selecting timestamps: {start_time_tune} - {end_time_tune}")

            self.tune_pages.desk_booking_time_selection.set_end_time(time=end_time_tune)
            self.tune_pages.desk_booking_time_selection.set_start_time(time=start_time_tune)
            Report.logInfo("Clicking confirm button")
            self.tune_pages.desk_booking_time_selection.click_confirm_button()
            self._assert(
                condition=self.tune_pages.desk_booking.verify_no_desks_available_label()
                or not self.tune_pages.desk_booking.verify_collapsable_desks_list(self.area.upper()),
                log_fail=f"Booking exceeding max days in advance possible which is NOK",
                log_pass=f"Booking exceeding max days in advance not possible which is OK"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")
