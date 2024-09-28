import random

from apps.tune.base.desk_booking_base import Account
from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from extentreport.report import Report
from datetime import datetime, timedelta
from common.platform_helper import get_correct_time_format_based_on_system


class NotificationsScenarios(WorkAccountScenarios):

    def tc_notifications_page_admin_created_booking(self, provider: str, credentials: dict) -> None:
        try:
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            self.tune_pages.home.click_home_tab()
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Admin created reservation")
            self._assert(
                condition=latest_notification.verify_label("Admin created reservation"),
                log_pass="Admin created reservation label is visible on latest notification",
                log_fail="Admin created reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )

            expected_time_format = datetime.now().strftime(get_correct_time_format_based_on_system("%A, %B %_d"))

            main_text_expected = (f"A desk booking in {self.building} on {expected_time_format} was made on your"
                                  f" behalf by an administrator")

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
        finally:
            if self.tune_pages.notifications_page.verify_notifications_page_present():
                self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.delete_calendar_events(provider, credentials)
            self.sync_api_methods.delete_reservations_for_desk(self.desk_id)

    def tc_notifications_page_admin_edited_booking(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Editing booking by administrator")

            self.sync_api_methods.edit_booking_by_id(self.org_id, self.desk_id, booking_id, fields={
                "start": self.sync_api_methods.format_to_zulu_format(datetime.now() + timedelta(minutes=10))
            })

            Report.logInfo("Clicking Refresh button after booking edit")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking edited by administrator is visible on user's dashboard page")

            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card edited by admin is visible on Dashboard Page",
                log_fail="Booking card edited by admin is not visible on Dashboard Page")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Admin updated reservation")
            self._assert(
                condition=latest_notification.verify_label("Admin updated reservation"),
                log_pass="Admin updated reservation label is visible on latest notification",
                log_fail="Admin updated reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )

            desk_info = self.sync_api_methods.get_desk_info(self.org_id, self.desk_id).json()
            group = desk_info.get('group')
            site, current_building, floor, area = group[1:-2].split('/')

            expected_time_format = datetime.now().strftime(get_correct_time_format_based_on_system("%A, %B %_d"))

            main_text_expected = (f"Your desk booking in {current_building} on {expected_time_format} has been "
                                  f"modified by an administrator")

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_admin_edited_booking_created_by_user(self,
                                                                   credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo("Booking desk as user with default values")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booked desk is visible on dashboard")

            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible on Dashboard Page",
                log_fail="Booking card is not visible on Dashboard Page"
            )

            booking_id = self.tune_pages.home.get_booking_id_by_index(0)

            Report.logInfo("Editing booking by administrator")

            self.sync_api_methods.edit_booking_by_id(self.org_id, self.desk_id, booking_id, fields={
                "start": self.sync_api_methods.format_to_zulu_format(datetime.now() + timedelta(minutes=10))
            })

            Report.logInfo("Clicking Refresh button after booking edit")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking edited by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card edited by admin is visible on Dashboard Page",
                         log_fail="Booking card edited by admin is not visible on Dashboard Page")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Admin updated reservation")
            self._assert(
                condition=latest_notification.verify_label("Admin updated reservation"),
                log_pass="Admin updated reservation label is visible on latest notification",
                log_fail="Admin updated reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )

            expected_time_format = datetime.now().strftime(get_correct_time_format_based_on_system("%A, %B %_d"))

            main_text_expected = (f"Your desk booking in {self.building} on {expected_time_format} has been "
                                  f"modified by an administrator")

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_admin_cancelled_booking(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Deleting booking by administrator")
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by administrator is not visible anymore")

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Admin cancelled reservation")
            self._assert(
                condition=latest_notification.verify_label("Admin cancelled reservation"),
                log_pass="Admin cancelled reservation label is visible on latest notification",
                log_fail="Admin cancelled reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )

            expected_time_format = datetime.now().strftime(get_correct_time_format_based_on_system("%A, %B %_d"))

            main_text_expected = (f"Your booking on {expected_time_format} in {self.building} was "
                                  f"cancelled by an administrator")

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_admin_cancelled_booking_created_by_user(self,
                                                                      credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo("Booking desk as user with default values")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booked desk is visible on dashboard")

            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible on Dashboard Page",
                log_fail="Booking card is not visible on Dashboard Page"
            )

            booking_id = self.tune_pages.home.get_booking_id_by_index(0)

            Report.logInfo("Deleting booking by administrator")
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by administrator is not visible anymore")

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Admin cancelled reservation")
            self._assert(
                condition=latest_notification.verify_label("Admin cancelled reservation"),
                log_pass="Admin cancelled reservation label is visible on latest notification",
                log_fail="Admin cancelled reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )

            expected_time_format = datetime.now().strftime(get_correct_time_format_based_on_system("%A, %B %_d"))

            main_text_expected = (f"Your booking on {expected_time_format} in {self.building} was "
                                  f"cancelled by an administrator")

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_notifications_order(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Editing booking by administrator")

            self.sync_api_methods.edit_booking_by_id(self.org_id, self.desk_id, booking_id, fields={
                "start": self.sync_api_methods.format_to_zulu_format(datetime.now() + timedelta(minutes=10))
            }).json()

            Report.logInfo("Clicking Refresh button after booking edit")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking edited by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card edited by admin is visible on Dashboard Page",
                         log_fail="Booking card edited by admin is not visible on Dashboard Page")

            Report.logInfo("Deleting booking by administrator")
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by administrator is not visible anymore")

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            first, second, third = self.tune_pages.notifications_page.get_all_notifications()

            Report.logInfo("Checking if newest notification contains label Admin cancelled reservation")
            self._assert(
                condition=first.verify_label("Admin cancelled reservation"),
                log_pass="Admin cancelled reservation label is visible on latest notification",
                log_fail="Admin cancelled reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if second newest notification contains label Admin updated reservation")
            self._assert(
                condition=second.verify_label("Admin updated reservation"),
                log_pass="Admin updated reservation label is visible on latest notification",
                log_fail="Admin updated reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if third newest notification contains label Admin created reservation")
            self._assert(
                condition=third.verify_label("Admin created reservation"),
                log_pass="Admin created reservation label is visible on latest notification",
                log_fail="Admin created reservation label is not visible on latest notification"
            )

            Report.logInfo("Checking if time created label values are in correct order (newest -> lower)")
            self._assert(
                condition=first.time_created_seconds < second.time_created_seconds < third.time_created_seconds,
                log_pass="All time labels are correct in ordered notifications",
                log_fail="Time labels are not correct in ordered notifications"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_cancel_booking_created_by_admin(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Clicking Review Booking")
            latest_notification.action_button.click()

            self.tune_pages.home.click_end_booking_button()
            self.tune_pages.home.click_end_booking_confirm_yes_button()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by user is not visible anymore")

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_rebook_after_booking_deleted_by_admin(self,
                                                                    credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Deleting booking by administrator")
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by user is not visible anymore")

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()
            Report.logInfo("Clicking Book a new desk on notification")

            latest_notification.action_button.click()

            Report.logInfo(f"Changing floor to {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            Report.logInfo(f"Collapsing desks list and clicking desk: {self.desk_name}")
            self.tune_pages.desk_booking.click_collapsable_desks_list(parameter=self.area.upper())
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            Report.logInfo("Booking desk with default parameters")
            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()

            self._assert(
                self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking created by user after admin cancellation is visible",
                log_fail="Booking created by user after admin cancellation is not visible"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notifications_page_check_in_required(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            check_in_required_minutes = 10
            Report.logInfo(f"Changing check in required time to: {check_in_required_minutes} minutes")
            self._assert(
                condition=self.sync_api_methods.change_check_in_required(self.desk_id, check_in_required_minutes * 60),
                log_pass=f"Check in required successfully changed to: {check_in_required_minutes} minutes",
                log_fail="Check in required change failed"
            )

            Report.logInfo("Waiting 20 seconds")
            self.tune_pages.home.wait_seconds_to_pass(20)

            Report.logInfo(f"Booking desk for user: {creds['email']}")

            booking_start_time = datetime.now()
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id,
                                                                    start_time=booking_start_time).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Waiting for rounded minute")
            self.tune_pages.home.wait_for_rounded_minute()

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()
            latest_notification = self.tune_pages.notifications_page.get_latest_notification()

            Report.logInfo("Checking if latest notification's label is Check in required")
            self._assert(
                condition=latest_notification.verify_label("Check in required"),
                log_pass="Check in required label is visible on latest notification",
                log_fail="Check in required label is not visible on latest notification"
            )

            Report.logInfo("Checking if seconds ago phrase is visible in notification's time created label")
            self._assert(
                condition=latest_notification.verify_time_created("seconds ago", strict=False) or latest_notification.
                verify_time_created("second ago", strict=False),
                log_pass="Seconds ago phrase is visible on latest notification",
                log_fail="Seconds ago phrase is not visible on latest notification"
            )
            check_in_deadline = booking_start_time + timedelta(minutes=check_in_required_minutes)

            check_in_deadline_str = check_in_deadline.strftime(get_correct_time_format_based_on_system("%_H:%M"))
            main_text_expected = f"You need to check-in at the desk, {self.desk_name} before {check_in_deadline_str}"

            Report.logInfo(f"Checking if main text is: {main_text_expected}")
            self._assert(
                condition=latest_notification.verify_main_text(main_text_expected),
                log_pass="Main Text is correct",
                log_fail="Main Text is not correct"
            )

            self.tune_pages.notifications_page.click_back_to_dashboard_button()
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
        finally:
            self.sync_api_methods.change_check_in_required(self.desk_id)

    def tc_notifications_page_close_button_check(self, credentials: Account) -> None:
        try:
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )
            creds = credentials['signin_payload']
            user_id = creds['identifier']

            self.tune_pages.home.click_home_tab()
            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            Report.logInfo("Clearing notifications if not empty")
            if not self.tune_pages.notifications_page.verify_notifications_empty():
                self.tune_pages.notifications_page.click_clear_notifications_button()
                self.tune_pages.notifications_page.click_clear_notifications_button_confirm()
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

            Report.logInfo(f"Booking desk for user: {creds['email']}")
            booking = self.sync_api_methods.create_booking_for_user(self.org_id, self.desk_id, user_id).json()
            Report.logResponse(repr(booking))
            booking_id = booking['reservations'][0]['identifier']

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking created by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card is visible on Dashboard Page",
                         log_fail="Booking card is not visible on Dashboard Page")

            Report.logInfo("Editing booking by administrator")

            self.sync_api_methods.edit_booking_by_id(self.org_id, self.desk_id, booking_id, fields={
                "start": self.sync_api_methods.format_to_zulu_format(datetime.now() + timedelta(minutes=10))
            }).json()

            Report.logInfo("Clicking Refresh button after booking edit")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking edited by administrator is visible on user's dashboard page")

            self._assert(self.tune_pages.home.verify_booking_card_displayed(),
                         log_pass="Booking card edited by admin is visible on Dashboard Page",
                         log_fail="Booking card edited by admin is not visible on Dashboard Page")

            Report.logInfo("Deleting booking by administrator")
            self.sync_api_methods.delete_reservation_by_id(self.org_id, self.desk_id, booking_id)

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            Report.logInfo("Verifying if booking deleted by administrator is not visible anymore")

            Report.logInfo("Clicking Refresh button")
            self._assert(
                condition=self.tune_pages.home.click_refresh_button_and_wait_for_refresh(),
                log_pass="Dashboard successfully refreshed",
                log_fail="Dashboard refresh failed"
            )

            self._assert(self.tune_pages.home.verify_booking_card_not_displayed(),
                         log_pass="Booking card is not visible on Dashboard Page, which is OK",
                         log_fail="Booking card is visible on Dashboard Page, which is NOK")

            Report.logInfo("Clicking Notifications Button")
            self.tune_pages.home.click_notifications_button()

            present_notifications = self.tune_pages.notifications_page.get_all_notifications()

            Report.logInfo("Checking if every expected notification is present on Notification Page - 4 notifications")
            self._assert(
                condition=len(present_notifications) == 3,
                log_pass="All expected notifications are visible",
                log_fail="Not every expected notification is visible"
            )

            notifications_labels = [notification.label for notification in present_notifications]

            Report.logInfo(f"Visible notifications: {', '.join(notifications_labels)}")

            while notifications_labels:
                selected_notification = random.choice(notifications_labels)
                notifications_labels.remove(selected_notification)

                Report.logInfo(f"Closing randomly selected notification: {selected_notification}")
                selected_notification_card = next(filter(lambda n: n.label == selected_notification,
                                                         present_notifications))
                self.tune_pages.notifications_page.scroll_to_notification(selected_notification_card)
                selected_notification_card.close_button.click()
                self.tune_pages.notifications_page.wait_for_notifications_to_load()
                visible_notifications = self.tune_pages.notifications_page.get_all_notifications()
                self._assert(
                    condition=len(visible_notifications) == len(notifications_labels),
                    log_pass=f"After deleting {selected_notification} number of remaining notifications is correct"
                             f" ({len(notifications_labels)})",
                    log_fail=f"After deleting {selected_notification} number of remaining notifications is not correct"
                             f" ({len(notifications_labels)})"
                )

                visible_notifications_labels = [notification.label for notification in visible_notifications]

                self._assert(
                    condition=visible_notifications_labels == notifications_labels,
                    log_pass="All remaining notifications are correct",
                    log_fail="Not every remaining notification is correct"
                )
            self.tune_pages.notifications_page.click_back_to_dashboard_button()

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
