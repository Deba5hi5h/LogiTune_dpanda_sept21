import random
from datetime import datetime, timedelta

from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from apps.tune.base.desk_booking_base import Account
from common.platform_helper import tune_time_format_from_datetime_obj
from extentreport.report import Report


class TuneMapScenarios(WorkAccountScenarios):

    def tc_book_a_desk_with_map_default(self) -> None:
        try:
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_maps_tab()
            self.tune_pages.maps.click_floor_choose_button()
            self.tune_pages.maps.click_floor_by_name(self.floor)
            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.maps.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )
            Report.logInfo(f"Checking if desk in area {self.area} named {self.desk_name} is visible on map as free")
            self._assert(
                condition=self.tune_pages.maps.click_on_desk_canvas_by_name(self.area, self.desk_name),
                log_pass=f"Desk {self.desk_name} is visible on the map",
                log_fail=f"Desk {self.desk_name} is not visible on the map"
            )
            Report.logInfo(f"Waiting for rounded minute")
            self.tune_pages.maps.wait_for_rounded_minute()
            start_time, end_time = self.default_booking_timestamps
            Report.logInfo(f"Clicking Book button")
            self.tune_pages.maps.click_book_button()
            Report.logInfo(f"Clicking Book button again")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Clicking Home button")
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )
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

            timestamps = f"{start_time} - {end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                            total_cards_number=1),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if booking is highlighted with correct color")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "color", self.tune_colors.color_ongoing,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_multiple_desks_booking_with_map(self) -> None:
        try:
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_maps_tab()
            self.tune_pages.maps.click_floor_choose_button()
            self.tune_pages.maps.click_floor_by_name(self.floor)
            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.maps.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )
            Report.logInfo(f"Checking if desk in area {self.area} named {self.desk_name} is visible on map as free")
            self._assert(
                condition=self.tune_pages.maps.click_on_desk_canvas_by_name(self.area, self.desk_name),
                log_pass=f"Desk {self.desk_name} is visible on the map",
                log_fail=f"Desk {self.desk_name} is not visible on the map"
            )
            Report.logInfo(f"Waiting for rounded minute")
            self.tune_pages.maps.wait_for_rounded_minute()

            first_book_start = datetime.now()
            first_book_end = first_book_start.replace(minute=0) + timedelta(hours=2)

            second_book_start = first_book_end + timedelta(minutes=30)
            second_book_end = second_book_start + timedelta(hours=1)


            if first_book_start.day != second_book_end.day:
                return Report.logSkip("Skipped due to execution time")

            first_book_start_time = tune_time_format_from_datetime_obj(first_book_start)
            first_book_end_time = tune_time_format_from_datetime_obj(first_book_end)

            second_book_start_time = tune_time_format_from_datetime_obj(second_book_start)
            second_book_end_time = tune_time_format_from_datetime_obj(second_book_end)

            Report.logInfo(f"Clicking Book button")
            self.tune_pages.maps.click_book_button()
            Report.logInfo(f"Changing timestamps to {first_book_start_time} - {first_book_end_time}")
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.set_end_time(first_book_end_time)
            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()
            Report.logInfo(f"Clicking Book button again")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.maps.wait_seconds_to_pass(3)

            second_desk = random.choice(self.desk_sibling_name_list)

            Report.logInfo(f"Checking if desk in area {self.area} named {second_desk} is visible on map as free")
            self._assert(
                condition=self.tune_pages.maps.click_on_desk_canvas_by_name(self.area, second_desk),
                log_pass=f"Desk {second_desk} is visible on the map",
                log_fail=f"Desk {second_desk} is not visible on the map"
            )

            Report.logInfo(f"Waiting for rounded minute")
            self.tune_pages.maps.wait_for_rounded_minute()
            Report.logInfo(f"Clicking Book button")
            self.tune_pages.maps.click_book_button()
            Report.logInfo(f"Changing timestamps to {second_book_start_time} - {second_book_end_time}")
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.set_end_time(second_book_end_time)
            self.tune_pages.desk_booking_time_selection.set_start_time(second_book_start_time)
            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()
            Report.logInfo(f"Clicking Book button again")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Redirecting to Home Page")
            self.tune_pages.home.click_home_tab()

            Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                            total_cards_number=2),
                log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=2),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{first_book_start_time} - {first_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                            total_cards_number=2),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if booking is highlighted with correct color")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "color",
                                                                            self.tune_colors.color_ongoing,
                                                                            total_cards_number=2),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )
            Report.logInfo(f"Checking booking card for {second_desk}")

            Report.logInfo(f"Checking if correct desk name: {second_desk} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "desk_name", second_desk,
                                                                            total_cards_number=2),
                log_fail=f"Desk name: {second_desk} is not visible on Booking Card",
                log_pass=f"Desk name: {second_desk} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "location_info", self.location,
                                                                            total_cards_number=2),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{second_book_start_time} - {second_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "timestamps", timestamps,
                                                                            total_cards_number=2),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if booking is highlighted with correct color")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "color",
                                                                            self.tune_colors.color_future_today,
                                                                            total_cards_number=2),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_book_multiple_day_booking_with_map(self) -> None:
        try:
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_maps_tab()
            self.tune_pages.maps.click_floor_choose_button()
            self.tune_pages.maps.click_floor_by_name(self.floor)
            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.maps.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )
            Report.logInfo(f"Checking if desk in area {self.area} named {self.desk_name} is visible on map as free")
            self._assert(
                condition=self.tune_pages.maps.click_on_desk_canvas_by_name(self.area, self.desk_name),
                log_pass=f"Desk {self.desk_name} is visible on the map",
                log_fail=f"Desk {self.desk_name} is not visible on the map"
            )
            Report.logInfo(f"Waiting for rounded minute")
            self.tune_pages.maps.wait_for_rounded_minute()
            Report.logInfo(f"Clicking Book button")
            self.tune_pages.maps.click_book_button()
            Report.logInfo(f"Clicking Book button again")
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
                        log_fail=f"Clicked day ({day_formatted}) has no effect with hovered background"
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
            Report.logInfo("Entering Home Page")
            self.tune_pages.home.click_home_tab()

            for day in days_to_book[1:]:
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

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_transfer_desk_with_map(self) -> None:
        try:
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_maps_tab()
            self.tune_pages.maps.click_floor_choose_button()
            self.tune_pages.maps.click_floor_by_name(self.floor)
            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.maps.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )
            Report.logInfo(f"Checking if desk in area {self.area} named {self.desk_name} is visible on map as free")
            self._assert(
                condition=self.tune_pages.maps.click_on_desk_canvas_by_name(self.area, self.desk_name),
                log_pass=f"Desk {self.desk_name} is visible on the map",
                log_fail=f"Desk {self.desk_name} is not visible on the map"
            )
            Report.logInfo(f"Waiting for rounded minute")
            self.tune_pages.maps.wait_for_rounded_minute()
            start_time, end_time = self.default_booking_timestamps

            Report.logInfo(f"Clicking Book button")
            self.tune_pages.maps.click_book_button()
            Report.logInfo(f"Clicking Book button again")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Clicking Home button")
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )
            Report.logInfo("Clicking on booking details")
            self.tune_pages.home.click_booking_details_button()
            Report.logInfo("Clicking Show on Map button")
            self.tune_pages.home.click_show_on_map_button()

            Report.logInfo("Checking if map is visible")
            self._assert(
                condition=self.tune_pages.maps.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )

            second_desk = random.choice(self.desk_sibling_name_list)

            Report.logInfo(f"Checking if desk in area {self.area} named {second_desk} is visible on map as free")
            self._assert(
                condition=self.tune_pages.desk_on_map.click_on_desk_canvas_by_name(self.area, second_desk),
                log_pass=f"Desk {second_desk} is visible on the map",
                log_fail=f"Desk {second_desk} is not visible on the map"
            )

            Report.logInfo("Clicking Transfer Button")
            self.tune_pages.desk_on_map.click_transfer_button()
            Report.logInfo("Clicking Confirm Transfer Button")
            self.tune_pages.desk_on_map.click_confirm_transfer_button()
            Report.logInfo("Clicking Done button")
            self.tune_pages.desk_transferred.click_done_button()
            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {second_desk} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", second_desk,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {second_desk} is not visible on Booking Card",
                log_pass=f"Desk name: {second_desk} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{start_time} - {end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                            total_cards_number=1),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if booking is highlighted with correct color")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "color", self.tune_colors.color_ongoing,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_book_next_to_person_on_map(self, opposite_creds: Account) -> None:

        try:
            Report.logInfo("Changing booking visible desk setting to True")
            self._assert(
                condition=self.sync_api_methods.change_keep_bookings_visible(self.desk_id, True),
                log_pass="Booking visible setting successfully set to True",
                log_fail="Booking visible setting failed to set to True",
            )

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]

            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email
            opposite_account_user_id = opposite_account.get('userId')

            Report.logInfo("Removing reservations for opposite user")
            self.sync_api_methods.delete_reservations_for_user(user_id=opposite_account_user_id)

            booking_start_time = (datetime.now().replace(minute=0, second=0, microsecond=0) +
                                  timedelta(hours=1))
            booking_duration = 120
            booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

            booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
            booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

            booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                    user_id=opposite_account_user_id,
                                                                    org_id=self.org_id,
                                                                    start_time=booking_start_time,
                                                                    duration=booking_duration).json()
            booking_id = booking['reservations'][0]['identifier']
            Report.logResponse(repr(booking))
            Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()
            Report.logInfo(f"Searching for user {opposite_account_repr}")
            Report.logInfo(f"Typing '{opposite_account_repr}' in the search input")
            self.tune_pages.people.input_everyone_search_bar(opposite_account_repr)
            self.tune_pages.people.wait_search_to_load()
            self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=opposite_account_repr)
            Report.logInfo(f"Entering profile for user: {opposite_account_repr}")
            self.tune_pages.people.click_user_from_everyone_tab_by_name(opposite_account_repr, match_case=True)

            self.tune_pages.people_user.click_booking_by_booking_id(booking_id)

            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.desk_booking.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )

            second_desk = random.choice(self.desk_sibling_name_list)
            Report.logInfo(f"Checking if desk in area {self.area} named {second_desk} is visible on map as free")
            self._assert(
                condition=self.tune_pages.desk_booking.click_on_desk_canvas_by_name(self.area, second_desk),
                log_pass=f"Desk {second_desk} is visible on the map",
                log_fail=f"Desk {second_desk} is not visible on the map"
            )
            Report.logInfo(f"Clicking Book button")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Clicking Home button")
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {second_desk} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", second_desk,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {second_desk} is not visible on Booking Card",
                log_pass=f"Desk name: {second_desk} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{booking_start_time_tune} - {booking_end_time_tune}"

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
                                                                            self.tune_colors.color_future_today,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_book_next_to_teammate_on_map(self, opposite_creds: Account) -> None:

        try:
            Report.logInfo("Changing booking visible desk setting to True")
            self._assert(
                condition=self.sync_api_methods.change_keep_bookings_visible(self.desk_id, True),
                log_pass="Booking visible setting successfully set to True",
                log_fail="Booking visible setting failed to set to True",
            )

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]

            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email
            opposite_account_user_id = opposite_account.get('userId')

            Report.logInfo("Removing reservations for opposite user")
            self.sync_api_methods.delete_reservations_for_user(user_id=opposite_account_user_id)

            booking_start_time = (datetime.now().replace(minute=0, second=0, microsecond=0) +
                                  timedelta(hours=1))
            booking_duration = 120
            booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

            booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
            booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

            booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                    user_id=opposite_account_user_id,
                                                                    org_id=self.org_id,
                                                                    start_time=booking_start_time,
                                                                    duration=booking_duration).json()
            booking_id = booking['reservations'][0]['identifier']
            Report.logResponse(repr(booking))
            Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()
            Report.logInfo(f"Searching for user {opposite_account_repr}")
            Report.logInfo(f"Typing '{opposite_account_repr}' in the search input")
            self.tune_pages.people.input_everyone_search_bar(opposite_account_repr)
            self.tune_pages.people.wait_search_to_load()
            self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=opposite_account_repr)
            Report.logInfo(f"Entering profile for user: {opposite_account_repr}")
            self.tune_pages.people.click_user_from_everyone_tab_by_name(opposite_account_repr, match_case=True)
            Report.logInfo(f"Adding user: {opposite_account_repr} to teammates list")
            self.tune_pages.people_user.click_add_to_teammates_button()
            Report.logInfo("Verifying if Remove from teammates button is visible")
            self._assert(
                condition=self.tune_pages.people_user.verify_remove_button_to_be_visible(),
                log_pass="Remove from teammates button visible - user added",
                log_fail="Remove from teammates is not visible - user was not added"
            )

            self.tune_pages.people_user.click_back_button()

            Report.logInfo("Entering home page")
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Clicking Book a Desk")
            self.tune_pages.home.click_book_a_desk_button()
            Report.logInfo("Clicking Next To Teammate button")
            self.tune_pages.home.click_near_a_teammate_button()
            Report.logInfo("Checking if recently added teammate is visible")
            self._assert(
                condition=self.tune_pages.people_in_office.verify_user_by_name_teammates(opposite_account_repr),
                log_pass="Recently added user is visible",
                log_fail="Recently added user is not visible"
            )
            self.tune_pages.people_in_office.click_user_by_name_teammates(opposite_account_repr)

            self.tune_pages.people_user.click_booking_by_booking_id(booking_id)

            Report.logInfo("Checking if enabled map is visible")
            self._assert(
                condition=self.tune_pages.desk_booking.verify_map_visible(),
                log_pass=f"Map visible in Maps Page for floor {self.floor}",
                log_fail=f"Map not visible in Maps Page for floor {self.floor}"
            )

            second_desk = random.choice(self.desk_sibling_name_list)
            Report.logInfo(f"Checking if desk in area {self.area} named {second_desk} is visible on map as free")
            self._assert(
                condition=self.tune_pages.desk_booking.click_on_desk_canvas_by_name(self.area, second_desk),
                log_pass=f"Desk {second_desk} is visible on the map",
                log_fail=f"Desk {second_desk} is not visible on the map"
            )
            Report.logInfo(f"Clicking Book button")
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo(f"Clicking Skip on Notify Teammates Page")
            self.tune_pages.notify_teammates.click_skip_button()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Clicking Home button")
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {second_desk} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", second_desk,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {second_desk} is not visible on Booking Card",
                log_pass=f"Desk name: {second_desk} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{booking_start_time_tune} - {booking_end_time_tune}"

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
                                                                            self.tune_colors.color_future_today,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
