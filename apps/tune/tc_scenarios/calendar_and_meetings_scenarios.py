from datetime import datetime, timedelta

from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from extentreport.report import Report


class CalendarAndMeetingsScenarios(WorkAccountScenarios):

    def tc_calendar_and_meetings_page_check(self) -> None:
        try:
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_calendar_and_meetings_button()

            calendar_and_meetings_title = "Calendar and meetings"

            Report.logInfo(f"Check if title {calendar_and_meetings_title} is visible")

            self._assert(
                condition=self.tune_pages.calendar_and_meetings_page.verify_label_name(calendar_and_meetings_title),
                log_pass=f"{calendar_and_meetings_title} title is visible",
                log_fail=f"{calendar_and_meetings_title} is not visible"
            )

            Report.logInfo(f"Check if title Show non-video meetings button is visible")

            self._assert(
                condition=self.tune_pages.calendar_and_meetings_page.verify_show_non_video_meetings_button(),
                log_pass="Show Non-video meetings button is visible",
                log_fail="Show Non-video meetings button is not visible"
            )

            Report.logInfo(f"Check if title Show all-day meetings button is visible")

            self._assert(
                condition=self.tune_pages.calendar_and_meetings_page.verify_show_non_video_meetings_button(),
                log_pass="Show All-day meetings button is visible",
                log_fail="Show All-day meetings button is not visible"
            )

            Report.logInfo(f"Check if title Show declined meetings button is visible")

            self._assert(
                condition=self.tune_pages.calendar_and_meetings_page.verify_show_non_video_meetings_button(),
                log_pass="Show declined meetings button is visible",
                log_fail="Show declined meetings button is not visible"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_calendar_non_video_meetings(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            event_data = {
                "summary": f"Test Event non-video meetings",
                "start_time": datetime.now(),
                "duration": 30,
                "video_event": False
            }
            Report.logInfo(f"Creating calendar event with data: {event_data}")

            self.create_calendar_event(provider, credentials, event_data)

            for _ in range(2):
                Report.logInfo("Entering calendar and meetings settings page")
                self.tune_pages.home.click_more_options()
                self.tune_pages.home.click_settings()
                self.tune_pages.settings.click_calendar_and_meetings_button()
                self.tune_pages.calendar_and_meetings_page.click_show_non_video_meetings_button()
                non_video_meetings = (self.tune_pages.calendar_and_meetings_page.
                                      check_value_show_non_video_meetings_button())
                Report.logInfo(f"Current status of non-video meetings is: {non_video_meetings}")

                Report.logInfo("Clicking back to settings button")
                self.tune_pages.calendar_and_meetings_page.click_back()
                Report.logInfo("Clicking back to dashboard button")
                self.tune_pages.settings.click_close_button()
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
                if non_video_meetings:
                    Report.logInfo(f"Checking if non-video meeting is visible")
                    self._assert(self.tune_pages.home.verify_calendar_events_titles_incoming([event_data['summary']]),
                                 log_pass="Non-video meeting is visible as intended",
                                 log_fail="Non-video meeting is not visible")

                else:
                    Report.logInfo(f"Checking if non-video meeting is not visible")
                    self._assert(self.tune_pages.home.verify_no_meetings_upcoming(),
                                 log_pass="Non-video meeting is not visible as intended",
                                 log_fail="Non-video meeting is visible")

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
        finally:
            self.delete_calendar_events(provider, credentials)

    def tc_calendar_declined_meetings(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            event_data = {
                "summary": f"Test Event declined meetings",
                "start_time": datetime.now(),
                "duration": 30,
                "video_event": True
            }
            Report.logInfo(f"Creating calendar event with data: {event_data}")

            event = self.create_calendar_event(provider, credentials, event_data)

            event_id = event.get('id')

            Report.logInfo("Changing event owner's response to Declined")
            self.edit_event_response_for_owner(provider, credentials, event_id, 'declined')

            for _ in range(2):
                Report.logInfo("Entering calendar and meetings settings page")
                self.tune_pages.home.click_more_options()
                self.tune_pages.home.click_settings()
                self.tune_pages.settings.click_calendar_and_meetings_button()
                self.tune_pages.calendar_and_meetings_page.click_declined_meetings_button()
                show_declined_meetings = (self.tune_pages.calendar_and_meetings_page.
                                          check_value_declined_meetings_button())
                Report.logInfo(f"Current status of show declined meetings is: {show_declined_meetings}")

                Report.logInfo("Clicking back to settings button")
                self.tune_pages.calendar_and_meetings_page.click_back()
                Report.logInfo("Clicking back to dashboard button")
                self.tune_pages.settings.click_close_button()
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
                if show_declined_meetings:
                    Report.logInfo(f"Checking if declined meeting is visible")
                    self._assert(self.tune_pages.home.verify_calendar_events_titles_incoming([event_data['summary']]),
                                 log_pass="Declined meeting is visible as intended",
                                 log_fail="Declined meeting is not visible")

                else:
                    Report.logInfo(f"Checking if declined meeting is not visible")
                    self._assert(self.tune_pages.home.verify_no_meetings_upcoming(),
                                 log_pass="Declined meeting is not visible as intended",
                                 log_fail="Declined meeting is visible")

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
        finally:
            self.delete_calendar_events(provider, credentials)

    def tc_calendar_all_day_meetings(self, provider: str, credentials: dict) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            event_data = {
                "summary": f"Test Event all-day meetings",
                "start_time": datetime.now().date() - timedelta(days=1),
                "duration": 3,
                "video_event": True
            }
            Report.logInfo(f"Creating calendar event with data: {event_data}")

            self.create_calendar_all_day_event(provider, credentials, event_data)

            for _ in range(2):
                Report.logInfo("Entering calendar and meetings settings page")
                self.tune_pages.home.click_more_options()
                self.tune_pages.home.click_settings()
                self.tune_pages.settings.click_calendar_and_meetings_button()
                self.tune_pages.calendar_and_meetings_page.click_show_all_day_meetings_button()
                show_all_day_meetings = (self.tune_pages.calendar_and_meetings_page.
                                         check_value_show_all_day_meetings_button())
                Report.logInfo(f"Current status of show all-day meetings is: {show_all_day_meetings}")

                Report.logInfo("Clicking back to settings button")
                self.tune_pages.calendar_and_meetings_page.click_back()
                Report.logInfo("Clicking back to dashboard button")
                self.tune_pages.settings.click_close_button()
                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
                if self.tune_pages.home.verify_expand_all_day_buttons_visible():
                    self.tune_pages.home.click_expand_all_day_buttons_visible()

                if show_all_day_meetings:
                    Report.logInfo(f"Checking if all-day meeting is visible")
                    self._assert(self.tune_pages.home.verify_calendar_events_titles_incoming([event_data['summary']]),
                                 log_pass="All day meeting is visible as intended",
                                 log_fail="All day meeting is not visible")

                else:
                    Report.logInfo(f"Checking if all-day meeting is not visible")
                    self._assert(self.tune_pages.home.verify_no_meetings_upcoming(),
                                 log_pass="All day meeting is not visible as intended",
                                 log_fail="All day meeting is visible")

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
        finally:
            self.delete_calendar_events(provider, credentials)
