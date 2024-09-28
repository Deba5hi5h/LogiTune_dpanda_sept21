import random
from datetime import datetime, timedelta

from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from base.base_settings import GOOGLE
from common.framework_params import COILY_BASECAMP_NAME
from common.platform_helper import (get_correct_time_format_based_on_system,
                                    tune_time_format_from_datetime_obj)
from extentreport.report import Report


class HomeDashboardScenarios(WorkAccountScenarios):

    def tc_home_screen_page_check(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if Home Label is highlighted")
            self._assert(
                condition=self.tune_pages.home.verify_if_home_label_is_highlighted(highlight_color=
                                                                                   self.tune_colors.
                                                                                   color_calendar_hover),
                log_pass="Home Label is highlighted after entering Home Page",
                log_fail="Home Label is not highlighted after entering Home Page"
            )
            Report.logInfo("Checking if Devices tab is visible")
            self._assert(
                condition=self.tune_pages.home.verify_device_tab(),
                log_pass="Devices Tab is visible",
                log_fail="Devices tab is not visible"
            )

            correct_system_format = get_correct_time_format_based_on_system("%A, %B %_d")
            today_date = datetime.now().strftime(correct_system_format)
            Report.logInfo("Checking if title contains correct day and date")
            self._assert(
                condition=self.tune_pages.home.verify_title_date_by_text(today_date),
                log_pass=f"Correct date ({today_date}) visible in Dashboard Page title",
                log_fail="Wrong date visible in Dashboard Page title"
            )
            Report.logInfo("Checking if People Tab is visible")
            self._assert(
                condition=self.tune_pages.home.verify_people_tab(),
                log_pass="People Tab is visible",
                log_fail="People Tab is not visible"
            )
            Report.logInfo("Check if Notifications Button is visible on Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_notifications_button(),
                log_pass="Notifications button is visible on Dashboard",
                log_fail="Notifications button is not visible on Dashboard"
            )
            Report.logInfo("Check if User Profile Button is visible on Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_user_profile_button(),
                log_pass="User Profile Button is visible on Dashboard",
                log_fail="User Profile Button is not visible on Dashboard"
            )
            Report.logInfo("Check if Calendar Expand Button is visible on Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_open_calendar_button(),
                log_pass="User Calendar Expand Button is visible on Dashboard",
                log_fail="User Calendar Expand Button is not visible on Dashboard"
            )
            Report.logInfo(f"Check if Basecamp Name ({COILY_BASECAMP_NAME}) is visible on Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_basecamp_name(COILY_BASECAMP_NAME),
                log_pass=f"User Basecamp Name ({COILY_BASECAMP_NAME}) is visible on Dashboard",
                log_fail=f"User Basecamp Name ({COILY_BASECAMP_NAME}) is not visible on Dashboard"
            )

            teammates_label_text = "No teammates in the office."
            Report.logInfo(f"Check if Teammates text ({teammates_label_text}) is visible on Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_teammates_by_text(teammates_label_text),
                log_pass=f"User Teammates text ({teammates_label_text}) is visible on Dashboard",
                log_fail=f"User Teammates text ({teammates_label_text}) is not visible on Dashboard"
            )

            self.delete_calendar_events(provider, credentials)
            start_time = datetime.now()
            events = []
            for delta in range(3):
                event_data = {
                    "summary": f"Test Event: {delta + 1}",
                    "start_time": start_time + timedelta(minutes=10 * delta),
                    "duration": 15 + delta * 5
                }
                event = self.create_calendar_event(provider, credentials, event_data)
                events.append({'id': event.get('id'),
                               'summary': event_data.get('summary')})
            event_titles = [event.get('summary') for event in events]
            Report.logInfo("Refreshing Dashboard")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            Report.logInfo("Check if every scheduled Calendar Event is present")
            self._assert(
                condition=self.tune_pages.home.verify_calendar_events_titles_incoming(event_titles),
                log_pass="Every scheduled Calendar Event is visible on Dashboard",
                log_fail="Not every scheduled Calendar Event is visible on Dashboard"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_calendar_not_expanded_calendar_check(self) -> None:
        try:

            self.tune_pages.home.click_home_tab()
            Report.logInfo("Checking if correct day order (S, M, T, W, T, F, S) is visible on non-expanded Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_non_expanded_calendar_weekdays(),
                log_fail="Wrong day order visible on Calendar",
                log_pass="Correct day order visible on Calendar"
            )

            today: datetime = datetime.now()
            today_day_number: int = today.day
            today_weekday: str = today.strftime('%a')[0]
            Report.logInfo(f"Check if Today's day ({today_day_number}) is highlighted in Tune Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_if_day_calendar_day_is_highlighted(today_day_number,
                                                                                         self.tune_colors.
                                                                                         color_calendar_hover),
                log_pass=f"Today's day: {today_day_number} is highlighted in Tune Calendar",
                log_fail=f"Today's day: {today_day_number} is not highlighted in Tune Calendar"
            )
            Report.logInfo(f"Check if Today's day ({today}) has correct weekday ({today_weekday})")
            self._assert(
                condition=self.tune_pages.home.verify_if_day_calendar_has_correct_weekday(
                    expected_weekday=today_weekday, day=today_day_number),
                log_pass=f"Today's day ({today}) has correct weekday",
                log_fail=f"Today's day ({today}) has wrong weekday",
            )

            today_weekday_number = (today.weekday() + 1) % 7
            Report.logInfo(f"Check if weekdays before today ({today_day_number} {today_weekday_number}) are disabled")
            self._assert(
                condition=self.tune_pages.home.verify_past_days_disabled(today_weekday_number),
                log_pass="Weekdays before today are disabled",
                log_fail="Weekdays before today are not disabled"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_calendar_expanded_calendar_check(self) -> None:

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_open_calendar_button()
            Report.logInfo("Checking if correct day order (S, M, T, W, T, F, S) is visible on expanded Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_expanded_calendar_weekdays(),
                log_fail="Wrong day order visible on Calendar",
                log_pass="Correct day order visible on Calendar"
            )
            Report.logInfo("Checking if remaining days from current month are present in Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_expanded_calendar_entire_month_is_shown(),
                log_fail="Not every day remaining in current month is visible in Calendar",
                log_pass="Every day remaining in current month is visible in Calendar"
            )
            Report.logInfo("Checking if next 30 days are visible in Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_expanded_calendar_next_30_days_visible(),
                log_fail="Not every day remaining in next 30 days range is visible in Calendar",
                log_pass="Every day remaining in next 30 days range is visible in Calendar"
            )
            self.tune_pages.home.click_close_calendar_button()
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_calendar_future_date_select(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_open_calendar_button()

            current_date = datetime.now()
            self.tune_pages.home.click_calendar_day_by_datetime(current_date)
            self.tune_pages.home.click_open_calendar_button()

            current_month: int = current_date.month
            current_year: int = current_date.year

            next_month: int = current_month + 1 if current_month != 12 else 1
            next_year: int = current_year if next_month != 1 else current_year + 1
            first_day_next_month: datetime = datetime(next_year, next_month, 1, hour=11, minute=0)
            Report.logInfo("Checking if abbreviation is visible above first day of next month")
            self._assert(
                condition=self.tune_pages.home.verify_if_next_month_is_displayed_on_first_day(first_day_next_month),
                log_fail="Next month abbreviation is not visible above the first day of next month",
                log_pass="Next month abbreviation is visible above the first day of next month"
            )
            self.delete_calendar_events(provider, credentials)
            next_week_date = datetime.now() + timedelta(days=7)
            next_week = datetime(next_week_date.year, next_week_date.month, next_week_date.day,
                                 hour=11, minute=0)
            events = []
            for delta in range(3):
                event_data = {
                    "summary": f"Test Event: {delta + 1}",
                    "start_time": next_week + timedelta(minutes=10 * delta),
                    "duration": 15 + delta * 5
                }
                event = self.create_calendar_event(provider, credentials, event_data)
                events.append({'id': event.get('id'),
                               'summary': event_data.get('summary')})
            event_titles = [event.get('summary') for event in events]

            self.tune_pages.home.click_calendar_day_by_datetime(next_week)
            Report.logInfo("Refreshing Dashboard")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            next_week_day_number: int = next_week.day
            Report.logInfo(f"Check if Selected day ({next_week_date}) is highlighted in Tune Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_if_day_calendar_day_is_highlighted(next_week_day_number,
                                                                                         self.tune_colors.
                                                                                         color_calendar_hover),
                log_pass=f"Selected day: {next_week_date} is highlighted in Tune Calendar",
                log_fail=f"Selected day: {next_week_date} is not highlighted in Tune Calendar"
            )

            Report.logInfo(f"Check if every scheduled Calendar Event is present for {next_week}")
            self._assert(
                condition=self.tune_pages.home.verify_calendar_events_titles_later(event_titles),
                log_pass=f"Every scheduled Calendar Event for {next_week} is visible on Dashboard",
                log_fail=f"Not every scheduled Calendar Event for {next_week} is visible on Dashboard"
            )
            self.delete_calendar_events(provider, credentials)
            events = []
            for delta in range(3):
                event_data = {
                    "summary": f"Test Event: {delta + 1}",
                    "start_time": first_day_next_month + timedelta(minutes=10 * delta),
                    "duration": 15 + delta * 5
                }
                event = self.create_calendar_event(provider, credentials, event_data)
                events.append({'id': event.get('id'),
                               'summary': event_data.get('summary')})
            event_titles = [event.get('summary') for event in events]

            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(first_day_next_month)
            Report.logInfo("Refreshing Dashboard")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            first_day_next_month_day_number: int = first_day_next_month.day
            Report.logInfo(f"Check if Selected day ({first_day_next_month}) is highlighted in Tune Calendar")
            self._assert(
                condition=self.tune_pages.home.verify_if_day_calendar_day_is_highlighted(
                    first_day_next_month_day_number, self.tune_colors.color_calendar_hover),
                log_pass=f"Selected day: {first_day_next_month} is highlighted in Tune Calendar",
                log_fail=f"Selected day: {first_day_next_month} is not highlighted in Tune Calendar"
            )
            Report.logInfo(f"Check if every scheduled Calendar Event is present for {first_day_next_month}")
            self._assert(
                condition=self.tune_pages.home.verify_calendar_events_titles_later(event_titles),
                log_pass=f"Every scheduled Calendar Event for {first_day_next_month} is visible on Dashboard",
                log_fail=f"Not every scheduled Calendar Event for {first_day_next_month} is visible on Dashboard"
            )
            self.delete_calendar_events(provider, credentials)

            current_weekday = current_date.weekday()
            next_sunday_time_delta: timedelta = timedelta(days=6 - current_weekday)
            next_sunday_date = current_date + next_sunday_time_delta

            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(next_sunday_date)
            Report.logInfo(f"Check if No Meetings Upcoming is visible when no meetings for selected Sunday")
            self._assert(
                condition=self.tune_pages.home.verify_no_meetings_upcoming(),
                log_pass=f"No Meetings Upcoming is visible when no meetings for selected Sunday",
                log_fail=f"No Meetings Upcoming is not visible when no meetings for selected Sunday"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_calenar_meeting_details_check(self, provider: str, credentials: dict) -> None:

        try:
            self.tune_pages.home.click_home_tab()
            self.delete_calendar_events(provider, credentials)
            today = datetime.now()
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(today)
            attendees_number = random.randint(3, 7)
            event_data = {
                "summary": f"Test Event 1",
                "start_time": today + timedelta(minutes=5),
                "duration": 30,
                "attendees": [f"testmaillogib{i}+test@{provider.lower()}.com" for i in range(attendees_number)]
            }
            event = self.create_calendar_event(provider, credentials, event_data)
            event_title = event_data.get("summary")

            Report.logInfo("Refreshing Dashboard")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Checking if events are visible in Dashboard")
            self._assert(
                condition=self.tune_pages.home.verify_calendar_events_titles_incoming(expected_titles=[event_title]),
                log_pass="Upcoming meetings visible in Tune",
                log_fail="Upcoming meetings not visible in Tune"
            )
            self.tune_pages.home.click_event_details(event_title)

            Report.logInfo(f"Verifying if meeting title: {event_title} is visible")

            self._assert(
                condition=self.tune_pages.meeting_detail_page.verify_meeting_title(event_title),
                log_pass="Meeting tittle visible in meeting detail page",
                log_fail="Meeting tittle not visible in meeting detail page"
            )

            start_time: datetime = event_data.get('start_time')
            end_time: datetime = start_time + timedelta(minutes=event_data.get('duration'))

            am_pm_start = start_time.strftime("%p").lower()
            am_pm_end = end_time.strftime("%p").lower()

            subtitle = (start_time.strftime(get_correct_time_format_based_on_system(f"%A, %B %_d · %I:%M "
                                                                                    f"{am_pm_start} - ")) +
                        end_time.strftime(get_correct_time_format_based_on_system(f"%I:%M {am_pm_end}")))

            Report.logInfo(f"Verifying if meeting subtitle: {subtitle} is visible")
            self._assert(
                condition=self.tune_pages.meeting_detail_page.verify_meeting_subtitle(subtitle),
                log_pass=f"Meeting subtitle is correct: {subtitle}",
                log_fail="Meeting subtitle not correct"
            )

            event_link = event.get('htmlLink') if provider == GOOGLE else event.get('webLink')

            Report.logInfo("Verifying if Open Details link is correct")
            self._assert(
                condition=self.tune_pages.meeting_detail_page.verify_details(event_link),
                log_pass="Open Details link is correct",
                log_fail="Open Details link is not correct"
            )

            hangout_link = event.get("hangoutLink") if provider == GOOGLE else event.get('onlineMeeting').get('joinUrl')

            Report.logInfo("Verifying if Copy Link is correct")
            self._assert(
                condition=self.tune_pages.meeting_detail_page.verify_copy_link(hangout_link),
                log_pass="Copy link is correct",
                log_fail="Copy link is not correct"
            )

            meeting_owner = credentials['signin_payload']['email'] if provider == GOOGLE \
                else credentials['signin_payload']['name'] + " " + credentials['signin_payload']['surname']
            meeting_owner = meeting_owner + "Organizer"
            attendees_list = [meeting_owner, *event_data.get('attendees')]

            Report.logInfo(f"Verifying if attendees list contains all people invited")
            self._assert(
                condition=self.tune_pages.meeting_detail_page.verify_attendees_list(attendees_list),
                log_pass="Every invited person is visible in meeting detail",
                log_fail="Not every invited person is visible in meeting detail"
            )
            self.tune_pages.meeting_detail_page.click_back_to_dashboard()
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_multiple_events_scrollable(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.delete_calendar_events(provider, credentials)
            today = datetime.now()
            events = []
            events_data = []
            event_number = random.randint(4, 8)
            for delta in range(event_number):
                event_data = {
                    "summary": f"Test Event {delta + 1}",
                    "start_time": today + timedelta(minutes=5 + 3 * delta),
                    "duration": 15,
                }
                events.append(self.create_calendar_event(provider, credentials, event_data))
                events_data.append({**event_data,
                                    "end_time": event_data['start_time'] + timedelta(minutes=event_data['duration'])})

            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Waiting for events to load on Dashboard Page")
            self._assert(
                condition=self.tune_pages.home.wait_for_expected_events_to_load(events),
                log_pass="All events present on Dashboard Page",
                log_fail="Not every event present on Dashboard Page"
            )
            for event in events_data:
                event_start_time: datetime = event.get("start_time")
                event_end_time: datetime = event.get("end_time")
                event_start_formatted: str = event_start_time.strftime(
                    get_correct_time_format_based_on_system(f"%I:%M %p"))
                event_end_formatted: str = event_end_time.strftime(
                    get_correct_time_format_based_on_system(f"%I:%M %p"))
                event_title = event.get("summary")
                meeting_time, attendees, time_to, summary, join_early = (
                    self.tune_pages.home.verify_event_scrollable(event).split("\n"))
                self._assert(meeting_time == f"{event_start_formatted} - {event_end_formatted}"
                             and event_title == summary,
                             log_pass=f"Meeting data for {summary} is correct",
                             log_fail=f"Meeting data for {summary} is not correct"
                             )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_book_a_desk_default(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.wait_for_rounded_minute()
            start_time, end_time = self.default_booking_timestamps
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

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

    def tc_multiple_booking(self) -> None:
        try:
            sibling_desk_name = random.choice(self.desk_sibling_name_list)
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.wait_for_rounded_minute()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()

            first_book_start = datetime.now()
            first_book_end = first_book_start.replace(minute=0) + timedelta(hours=2)

            second_book_start = first_book_end + timedelta(minutes=30)
            second_book_end = second_book_start + timedelta(hours=1)

            third_book_start = second_book_end + timedelta(minutes=30)
            third_book_end = third_book_start + timedelta(hours=1)

            if first_book_start.day != third_book_end.day:
                return Report.logSkip("Skipped due to execution time")

            first_book_start_time = tune_time_format_from_datetime_obj(first_book_start)
            first_book_end_time = tune_time_format_from_datetime_obj(first_book_end)

            second_book_start_time = tune_time_format_from_datetime_obj(second_book_start)
            second_book_end_time = tune_time_format_from_datetime_obj(second_book_end)

            third_book_start_time = tune_time_format_from_datetime_obj(third_book_start)
            third_book_end_time = tune_time_format_from_datetime_obj(third_book_end)

            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.set_end_time(first_book_end_time)
            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()

            self.tune_pages.desk_booking.click_collapsable_desks_list(parameter=self.area.upper())
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )
            Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{first_book_start_time} - {first_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on first booking card")
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

            Report.logInfo("Creating another reservation for same desk")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()

            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.set_end_time(second_book_end_time)
            self.tune_pages.desk_booking_time_selection.set_start_time(second_book_start_time)
            Report.logInfo(f"Booking time set to: {second_book_start_time} - {second_book_end_time}",
                           screenshot=True)

            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()

            self.tune_pages.desk_booking.click_collapsable_desks_list(parameter=self.area.upper())
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            Report.logInfo("Checking if 2 booking cards are visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_cards_displayed(2),
                log_pass="2 Booking cards are visible",
                log_fail="2 Booking cards are not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on second booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "desk_name", self.desk_name,
                                                                            total_cards_number=2),
                log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on second booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "location_info", self.location,
                                                                            total_cards_number=2),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{second_book_start_time} - {second_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on second booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "timestamps", timestamps,
                                                                            total_cards_number=2),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(1, "color", self.tune_colors.
                                                                            color_future_today,
                                                                            total_cards_number=2),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

            Report.logInfo("Creating reservation for different desk")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()

            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            self.tune_pages.desk_booking_time_selection.set_end_time(third_book_end_time)
            self.tune_pages.desk_booking_time_selection.set_start_time(third_book_start_time)
            Report.logInfo(f"Booking time set to: {third_book_start_time} - {third_book_end_time}",
                           screenshot=True)

            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()

            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            self.tune_pages.desk_booking.click_desk_by_desk_name(sibling_desk_name)
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            Report.logInfo("Checking if 3 booking cards are visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_cards_displayed(3),
                log_pass="3 Booking cards are visible",
                log_fail="3 Booking cards are not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {sibling_desk_name} is visible on third booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(2, "desk_name", sibling_desk_name,
                                                                            total_cards_number=3),
                log_fail=f"Desk name: {sibling_desk_name} is not visible on Booking Card",
                log_pass=f"Desk name: {sibling_desk_name} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on third booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(2, "location_info", self.location,
                                                                            total_cards_number=3),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{third_book_start_time} - {third_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on third booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(2, "timestamps", timestamps,
                                                                            total_cards_number=3),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(2, "color", self.tune_colors.
                                                                            color_future_today,
                                                                            total_cards_number=3),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )
            tomorrow = datetime.now() + timedelta(days=1)

            Report.logInfo("Creating reservation for different day")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.verify_no_desks_available_label()

            Report.logInfo("Entering Time Selection Page")
            self.tune_pages.desk_booking.click_book_a_desk_date_button()
            Report.logInfo("Collapsing calendar")
            self.tune_pages.desk_booking_time_selection.click_open_calendar_button()

            self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(tomorrow)
            self.tune_pages.desk_booking_time_selection.set_end_time(second_book_end_time)
            self.tune_pages.desk_booking_time_selection.set_start_time(second_book_start_time)
            Report.logInfo(f"Booking time set to: {second_book_start_time} - {second_book_end_time}",
                           screenshot=True)
            if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                self.tune_pages.desk_booking_time_selection.click_confirm_button()
            else:
                self.tune_pages.desk_booking_time_selection.click_back_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()


            self.tune_pages.desk_booking.click_collapsable_desks_list(parameter=self.area.upper())
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(datetime.now())

            Report.logInfo("Check if tomorrows day has little dot under day number because of reservation")
            self._assert(
                condition=self.tune_pages.home.verify_if_meeting_dot_is_visible_in_day(
                    first_book_start.day + 1, self.tune_colors.color_calendar_hover),
                log_pass="Little dot under day number is visible",
                log_fail="Little dot under day number is not visible"
            )

            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(datetime.now() + timedelta(days=1))
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            Report.logInfo("Checking if 1 booking tomorrow card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_cards_displayed(1),
                log_pass="1 Booking card is visible",
                log_fail="1 Booking card is not visible"
            )

            Report.logInfo(f"Checking if correct desk name: {self.desk_name} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", self.desk_name,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {self.desk_name} is not visible on Booking Card",
                log_pass=f"Desk name: {self.desk_name} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{second_book_start_time} - {second_book_end_time}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                            total_cards_number=1),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "color", self.tune_colors.
                                                                            color_future_not_today,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_max_days_in_advance(self) -> None:
        try:
            days_in_advance_list = [1, random.randint(2, 29), 30]
            for days_in_advance in days_in_advance_list:
                self.tune_pages.home.click_book_a_desk_button()
                self.tune_pages.home.click_by_location_and_preferences_button()
                self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
                self.tune_pages.desk_booking.select_floor_by_text(self.floor)
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo(f"Changing max days in advance to {days_in_advance}")
                dia_changed = self.sync_api_methods.change_max_days_in_advance(self.desk_id, days_in_advance)
                self.tune_pages.home.wait_seconds_to_pass(10)
                self._assert(
                    condition=dia_changed,
                    log_fail=f"Days in advance change to: {days_in_advance} failed",
                    log_pass=f"Successfully changed max days in advance to value: {days_in_advance}",
                )
                last_available_day = datetime.today() + timedelta(days=days_in_advance)
                last_available_day_formatted = last_available_day.strftime("%a, %b %d")
                self.tune_pages.desk_booking.click_book_a_desk_date_button()
                self.tune_pages.desk_booking_time_selection.click_open_calendar_button()
                self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(last_available_day)
                if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                    self.tune_pages.desk_booking_time_selection.click_confirm_button()
                else:
                    self.tune_pages.desk_booking_time_selection.click_back_button()
                Report.logInfo(f"Checking if collapse button visible on last available booking day: "
                               f"{last_available_day_formatted}")
                self._assert(
                    condition=self.tune_pages.desk_booking.verify_collapsable_desks_list(parameter=self.area.upper()),
                    log_fail=f"Collapse button is not visible on last available day: {last_available_day_formatted}",
                    log_pass=f"Collapse button is visible on last available day: {last_available_day_formatted}",
                )
                self.tune_pages.desk_booking.click_collapsable_desks_list(parameter=self.area.upper())
                for desk in self.group_desk_list_names:
                    Report.logInfo(f"Checking if desk {desk} is visible on last available day: "
                                   f"{last_available_day_formatted}")
                    self._assert(
                        condition=self.tune_pages.desk_booking.verify_desk_by_desk_name(desk),
                        log_fail=f"Desk {desk} is not available on {last_available_day_formatted}",
                        log_pass=f"Desk {desk} is available on {last_available_day_formatted}",
                    )

                if days_in_advance < 30:
                    first_not_available_day = last_available_day + timedelta(days=1)
                    first_not_available_day_formatted = first_not_available_day.strftime("%a, %b %d")
                    self.tune_pages.desk_booking.click_book_a_desk_date_button()
                    self.tune_pages.desk_booking_time_selection.click_open_calendar_button()
                    self.tune_pages.desk_booking_time_selection.click_day_in_calendar_by_datetime(
                        first_not_available_day)
                    if self.tune_pages.desk_booking_time_selection.verify_confirm_button():
                        self.tune_pages.desk_booking_time_selection.click_confirm_button()
                    else:
                        self.tune_pages.desk_booking_time_selection.click_back_button()

                    Report.logInfo(f"Checking if desks are not visible on first unavailable day: "
                                   f"{first_not_available_day_formatted}")
                    for desk in self.group_desk_list_names:
                        self._assert(
                            condition=self.tune_pages.desk_booking.verify_no_desks_available_label() or
                            not self.tune_pages.desk_booking.verify_desk_by_desk_name(desk),
                            log_fail=f"Desk {desk} is visible on last available day: "
                                     f"{first_not_available_day_formatted}",
                            log_pass=f"Desks {desk} is not visible on last available day: "
                                     f"{first_not_available_day_formatted}",
                        )
                self.tune_pages.desk_booking.click_back_button()

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
