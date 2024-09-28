import math
import time
from typing import Optional, Tuple

from datetime import datetime, timedelta

import pytz
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.remote.webelement import WebElement

from apps.collabos.collabos_base import AppiumServiceCollabOS, CollabOsOpenApp
from base.global_variables import APPIUM_PORT_COILY
from apps.collabos.coily.coily_messages import *
from apps.collabos.coily.pages.tune_coily_main_page import TuneCoilyMainPage
from apps.collabos.coily.coily_connect import CoilyConnect
from apps.collabos.coily.tune_coily_config import FORMAT_24H, FORMAT_AMPM
from apps.collabos.coily.utilities import check_and_connect_device, get_current_date, \
    get_times_with_offset, get_current_time, restart_adb_server, prepare_work_account_credentials

from base import global_variables
from common.framework_params import COILY_DESK_IP, COILY_DEVICE_SN
from common.platform_helper import get_custom_platform
from common.decorators import Singleton
from extentreport.report import Report
from locators.coily_locators import (TuneCoilyMainPageLocators, TuneCoilyLaptopDisconnectedLocators,
                                     TuneWalkinDisabledLocators, TuneCoilyAlreadyHaveSessionLocators)


@Singleton
class TuneCoilyMethods(CoilyConnect):
    def __init__(self):
        self.appium_service = AppiumServiceCollabOS(appium_port=APPIUM_PORT_COILY,
                                                    device_ip=COILY_DESK_IP,
                                                    device_sn=COILY_DEVICE_SN)
    home = TuneCoilyMainPage()

    def open_app(self, force: bool = False) -> None:
        scheduler_app = CollabOsOpenApp(appium_service=self.appium_service,
                                        connect_process=lambda: self.connect_to_scheduler_app(
                                            port=APPIUM_PORT_COILY,
                                            device_ip=COILY_DESK_IP,
                                            device_sn=COILY_DEVICE_SN
                                        ),
                                        force=force)

        scheduler_app.connect_to_android_app()

    def verify_coily_idle_page(self, org_name: str, group_name: str, desk_name: str,
                               time_format: str = FORMAT_AMPM) -> None:
        Report.logInfo('Verify Coily Idle page.')

        hierachy = f'{org_name} · {group_name}'
        title = self.verify_hierarchy_idle_page(hierachy)

        desk = self.verify_desk_name(desk_name)
        time = self.verify_time_idle_page(time_format=time_format)

        assert title and desk and time, "Not all the messages on the Coily Idle page are correct"
        Report.logPass('All Coily Idle page elements are correct.')

    def verify_time_idle_page(self, time_format: str = FORMAT_AMPM) -> bool:
        coily_current_clock = self.home.get_time_from_idle_page()
        current_time, current_time_minus_1, current_time_plus_1 = get_current_time(time_format)

        Report.logInfo(f"Current time is: "
                       f"{current_time_minus_1}/{current_time}/{current_time_plus_1}")
        if coily_current_clock in [current_time, current_time_plus_1, current_time_minus_1]:
            Report.logPass("Correct time displayed.", is_collabos=True, screenshot=True)
            return True
        Report.logFail(f"Incorrect time displayed: {coily_current_clock}", is_collabos=True)
        return False

    def verify_desk_name(self, desk_name: str) -> bool:
        coily_desk_name = self.home.get_desk_name()
        if coily_desk_name == desk_name:
            Report.logPass("Correct desk name displayed.", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(f"Incorrect desk name displayed: {coily_desk_name}",
                       is_collabos=True)
        return False

    def verify_group_name(self, group_name: str) -> bool:
        coily_group_name = self.home.get_group_name()
        if coily_group_name == group_name:
            Report.logPass("Correct group name displayed.", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(f"Incorrect group name displayed. {coily_group_name}",
                       is_collabos=True)
        return False

    def verify_time_left_to_beginning_of_reservation(self, input_time: str) -> None:
        timestamp = datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Get the current time
        current_time = datetime.utcnow()

        # Calculate the time difference in minutes
        time_difference_minutes = math.ceil((timestamp - current_time).total_seconds() / 60)

        expected_time_left_1 = f"{time_difference_minutes} minutes left"
        expected_time_left_2 = f"{time_difference_minutes - 1} minutes left"

        time_left_text = self.home.get_time_left_to_beginning_of_reservation()

        if time_left_text in [expected_time_left_1, expected_time_left_2]:
            Report.logPass(f"{expected_time_left_1}/{expected_time_left_2} is displayed",
                           screenshot=True, is_collabos=True)
        else:
            Report.logFail(
                f"{expected_time_left_1}/{expected_time_left_2} is not displayed: {time_left_text}",
                is_collabos=True
            )

    def verify_there_is_no_center_pile_with_time_left_for_the_reservation(self) -> None:
        Report.logInfo("Verify if center pile with 'X minutes left' is not displayed.")

        status = self.home.verify_time_left_to_end_of_reservation_is_dispalyed()
        if not status:
            Report.logPass("Center pile is not displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail("Center pile is displayed", is_collabos=True,
                           screenshot=True)

    def verify_coily_authenticated_page(self, org_name: str, group_name: str, desk_name: str,
                                        time_format: str = FORMAT_AMPM) -> None:
        Report.logInfo('Verify all elements on the Coily authenticated page.')

        hierachy = f'{org_name} · {group_name} · {desk_name}'
        title = self.verify_hierarchy_authenticated_page(hierachy)
        time = self.verify_time_authenticated_page(time_format=time_format)
        date = self.verify_date_authenticated_page()
        assert title and time and date, "Not all the messages on the Coily Authenticated page are correct"
        Report.logPass(f'All elements on Coily authenticated page are correct.')

    def verify_agenda_item(self, event_title: str, start_time: datetime, duration_min: int,
                           time_format: str, attendees: int = 1) -> None:
        self.verify_agenda_item_attendees(self.verify_agenda_item_displayed(event_title),
                                          expected_attendees=attendees)
        self.verify_agenda_time_frames(self.verify_agenda_item_displayed(event_title),
                                       start_time, duration_min, time_format)
        is_button_displayed = self.is_agenda_item_join_now_button_displayed(
            self.verify_agenda_item_displayed(event_title))
        is_join_button_expected = self._get_the_time_difference_in_minutes(start_time) <= 60
        if is_join_button_expected:
            if is_button_displayed == is_join_button_expected:
                Report.logPass(f"Join Now button is displayed as expected",
                               is_collabos=True, screenshot=True)
            else:
                Report.logFail(f"Join Now NOT displayed, but it was expected",
                               is_collabos=True)
        else:
            if is_button_displayed == is_join_button_expected:
                Report.logPass(f"Join Now button is not displayed as expected",
                               is_collabos=True, screenshot=True)
            else:
                Report.logFail(f"Join Now NOT is displayed, but it was not expected",
                               is_collabos=True)

    def verify_agenda_item_privacy_mode(self) -> None:
        element = self.home
        if element:
            Report.logInfo("Event present without details in privacy mode")
        else:
            Report.logFail("Event not present in privacy mode")

    def extend_agenda_view(self) -> None:
        self.home.extend_agenda_view()

    def close_agenda_view(self) -> None:
        self.home.click_close_agenda_view()

    def click_agenda_item_by_title(self, event_title) -> None:
        self.home.click_agenda_item_by_title(event_title)

    def close_event_details(self):
        self.home.click_close_event_details()

    def scroll_to_agenda_notes(self):
        self.home.scroll_to_agenda_notes()

    def click_show_all_attendees(self):
        self.home.click_show_all_attendees()

    @staticmethod
    def _get_the_time_difference_in_minutes(meetings_start_time: datetime) -> float:
        current_time = datetime.now()
        time_diff = (meetings_start_time - current_time).total_seconds()//60

        return time_diff

    def verify_agenda_time_frames(self, parent_element: WebElement, start_time: datetime,
                                  duration_min: int, time_format: str) -> bool:
        parent_element = self.home.get_agenda_event_time_frames(parent_element)

        end_time = start_time + timedelta(minutes=duration_min)

        if time_format == FORMAT_24H:
            expected_start_time = start_time.strftime("%H:%M")
            expected_stop_time = end_time.strftime("%H:%M")
        else:
            if get_custom_platform() == "windows":
                expected_start_time = start_time.strftime("%#I:%M %p")
                expected_stop_time = end_time.strftime("%#I:%M %p")
            else:
                expected_start_time = start_time.strftime("%-I:%M %p")
                expected_stop_time = end_time.strftime("%-I:%M %p")

        expected_string = f'{expected_start_time} - {expected_stop_time}'

        if parent_element == expected_string:
            Report.logPass(
                f"Agenda meeting timeframes '{expected_string}' displayed correctly",
                is_collabos=True,
                screenshot=True
            )
            return True
        Report.logFail(
            f"Agenda meeting timeframes '{expected_string}' "
            f"NOT displayed correctly: {parent_element}",
            is_collabos=True
        )
        return False

    def verify_agenda_item_displayed(self, event_title: str) -> Optional[WebElement]:
        paren_element = self.home.get_agenda_item_by_title(event_title)
        if paren_element:
            Report.logPass(f"Agenda itme '{event_title}' displayed correctly",
                           is_collabos=True, screenshot=True)
            return paren_element
        Report.logFail(f"Agenda itme '{event_title}' NOT displayed correctly",
                       is_collabos=True)
        return None

    def is_any_agenda_item_displayed(self) -> bool:
        is_displayed = self.home.verify_any_agenda_item_displayed()
        if is_displayed:
            Report.logInfo(f"Agenda items are displayed", is_collabos=True, screenshot=True)
            return True
        Report.logInfo(f"Agenda items are NOT displayed", is_collabos=True)
        return False

    def verify_agenda_item_attendees(self, parent_element: WebElement, expected_attendees: int = 1
                                     ) -> bool:
        attendees = self.home.get_agenda_event_attendees(parent_element)
        if attendees == str(expected_attendees):
            Report.logPass(
                f"Number of expected attendees '{expected_attendees}' matches displayed number",
                is_collabos=True,
                screenshot=True
            )
            return True
        Report.logFail(
            f"Number of expected attendees '{expected_attendees}' "
            f"DOES NOT match displayed number: '{attendees}'",
            is_collabos=True
        )
        return False

    def is_agenda_item_join_now_button_displayed(self, parent_element: WebElement) -> bool:
        is_button_displayed = self.home.get_agenda_event_join_now_button(parent_element)
        if is_button_displayed:
            Report.logInfo(f"Join Now button is displayed.", is_collabos=True,
                           screenshot=True)
            return True
        Report.logInfo(f"Join Now NOT displayed.", is_collabos=True)
        return False

    def verify_hierarchy_authenticated_page(self, hierarchy: str) -> bool:
        desk_hierarchy = self.home.get_desk_hierarchy_authenticated_page()
        if desk_hierarchy == hierarchy:
            Report.logPass("Correct hierarchy displayed on authenticated page.",
                           is_collabos=True, screenshot=True)
            return True
        Report.logFail(
            f"Incorrect hierarchy displayed on authenticated page: {desk_hierarchy} != {hierarchy}",
            is_collabos=True
        )
        return False

    def verify_hierarchy_idle_page(self, hierarchy: str) -> bool:
        desk_hierarchy = self.home.get_desk_hierarchy_idle_page()
        if desk_hierarchy == hierarchy:
            Report.logPass("Correct hierarchy displayed on Idle page.", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(
            f"Incorrect hierarchy displayed on Idle page: {desk_hierarchy} != {hierarchy}",
            is_collabos=True
        )
        return False

    def click_book_desk_button(self):
        self.home.click_book_desk_button()

    def click_book_desk_button_confirmation(self):
        self.home.click_book_desk_button_confirmation()

    def open_coily_settings_page(self):
        self.home.click_settings_button_main_page()

    def click_close_admin_settings_page(self):
        self.home.click_close_admin_settings_page()

    def open_coily_language_settings_page(self):
        self.home.click_language_settings_button()

    def close_pin_page(self):
        self.home.click_close_pin_page()

    def click_notification_action_during_check_in(self):
        self.home.click_notification_action_during_check_in()

    def click_notification_dismiss_during_check_in(self):
        self.home.click_notification_dismiss_during_check_in()


    def verify_time_authenticated_page(self, time_format: str = FORMAT_AMPM) -> bool:
        coily_current_clock = self.home.get_time_authenticated_page()
        current_time, current_time_minus_1, current_time_plus_1 = get_current_time(time_format)

        Report.logInfo(
            f"Current time is: {current_time_minus_1}/{current_time}/{current_time_plus_1}"
        )
        if coily_current_clock in [current_time_minus_1, current_time, current_time_plus_1]:
            Report.logPass("Correct time name displayed.", is_collabos=True, screenshot=True)
            return True
        Report.logFail(f"Incorrect time displayed: {coily_current_clock}", is_collabos=True)
        return False

    def verify_date_authenticated_page(self) -> bool:
        coily_current_date = self.home.get_date_authenticated_page()
        current_date = get_current_date()
        Report.logInfo(f"Current date is: {current_date}")
        if coily_current_date == current_date:
            Report.logPass("Correct date name displayed.", is_collabos=True, screenshot=True)
            return True
        Report.logFail(f"Incorrect date displayed: {coily_current_date} != {current_date}",
                       is_collabos=True)
        return False

    def verify_booking_meesage_window(self) -> bool:
        Report.logInfo('Verify Booking message on the Coily display')

        title, message = self.home.get_booking_message()
        if title == MESSAGE_BOOKING_TITLE:
            Report.logPass(f"Booking title '{MESSAGE_BOOKING_TITLE}' is displayed",
                           is_collabos=True, screenshot=True)
            return True
        Report.logFail(f"Booking title '{MESSAGE_BOOKING_TITLE} is NOT displayed: {title}",
                       is_collabos=True)
        return False

    def verify_checking_you_in_message_window(self) -> bool:
        Report.logInfo('Verify if Coily shows "Checking you in..." window.')

        title, message = self.home.get_booking_message()
        if (title == NOTIFICATION_CHECKING_YOU_IN_WINDOW_MESSAGE or
                title == NOTIFICATION_CHECKING_YOU_IN_WINDOW_MESSAGE_ALTER):
            Report.logPass(f"{NOTIFICATION_CHECKING_YOU_IN_WINDOW_MESSAGE} title is displayed",
                           is_collabos=True, screenshot=True)
            return True
        Report.logFail(
            f"{NOTIFICATION_CHECKING_YOU_IN_WINDOW_MESSAGE} title is not displayed: {title}",
            is_collabos=True
        )
        return False

    def verify_coily_is_checked_in_walk_in_session_notification(
            self, reservation_start_time: datetime, time_offset: int = 1, timeout: int = 30,
            time_format: str = FORMAT_AMPM
    ) -> bool:

        Report.logInfo(
            f'Verify if reservation is confirmed with text "{NOTIFICATION_RESERVATION_MESSAGE}"'
        )
        time.sleep(3)
        title = self.home.wait_for_notification_message(timeout=timeout,
                                                        message=NOTIFICATION_RESERVATION_MESSAGE)
        target_time_1, target_time_2, target_time_3 = (
            get_times_with_offset(reservation_start_time, time_offset, time_format))

        notification_1 = NOTIFICATION_RESERVATION_MESSAGE + target_time_1 + '.'
        notification_2 = NOTIFICATION_RESERVATION_MESSAGE + target_time_2 + '.'
        notification_3 = NOTIFICATION_RESERVATION_MESSAGE + target_time_3 + '.'

        if title in [notification_1, notification_2, notification_3]:
            Report.logPass(f"'{title}' notification is displayed", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(f"Wrong notification is displayed: '{title}' instead of '{notification_1}'",
                       is_collabos=True)
        return False

    def verify_you_desk_session_will_end_notification(
            self, reservation_end_time: datetime, timeout: int = 20, time_format: str = FORMAT_AMPM
    ) -> bool:
        Report.logInfo(f'Verify if reservation is confirmed with text '
                       f'"{NOTIFICATION_YOUR_DESK_SESSION_WILL_END}"')
        time.sleep(3)
        title = self.home.wait_for_notification_message(
            timeout=timeout, message=NOTIFICATION_YOUR_DESK_SESSION_WILL_END)

        utc_time = datetime.strptime(reservation_end_time[:-1], "%Y-%m-%dT%H:%M:%S.%f")

        # Set the timezone for the input time as UTC
        utc_timezone = pytz.timezone('UTC')
        utc_time = utc_timezone.localize(utc_time)

        from tzlocal import get_localzone_name
        gmt2_timezone = pytz.timezone(get_localzone_name())

        # Convert the time to GMT+2
        gmt2_time = utc_time.astimezone(gmt2_timezone)

        t_format = ''
        if time_format == FORMAT_24H:
            t_format = "%H:%M"
        elif time_format == FORMAT_AMPM:
            if get_custom_platform() == "windows":
                t_format = "%#I:%M %p"
            else:
                t_format = "%-I:%M %p"

        formatted_time = gmt2_time.strftime(t_format)

        notification_1 = NOTIFICATION_YOUR_DESK_SESSION_WILL_END + formatted_time

        if title in notification_1:
            Report.logPass(f"'{title}' notification is displayed", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(f"Wrong notification is displayed: '{title}' instead of '{notification_1}'",
                       is_collabos=True)
        return False

    def verify_coily_is_checked_in_booked_session_notification(
            self, stop_time: str, time_format: str = FORMAT_AMPM, timeout: int = 30) -> bool:

        notification = ''
        try:
            Report.logInfo(
                'Verify if Coily shows confirmation about reservation on the notification panel.'
            )

            utc_time = datetime.strptime(stop_time[:-1], "%Y-%m-%dT%H:%M:%S.%f")

            # Set the timezone for the input time as UTC
            utc_timezone = pytz.timezone('UTC')
            utc_time = utc_timezone.localize(utc_time)

            # Define GMT+2 timezone
            # gmt2_timezone = pytz.timezone('Etc/GMT-2')
            from tzlocal import get_localzone_name
            gmt2_timezone = pytz.timezone(get_localzone_name())

            # Convert the time to GMT+2
            gmt2_time = utc_time.astimezone(gmt2_timezone)

            formatted_time = ''
            if time_format == FORMAT_24H:
                formatted_time = gmt2_time.strftime("%H:%M")
            elif time_format == FORMAT_AMPM:
                if get_custom_platform() == "windows":
                    formatted_time = gmt2_time.strftime("%#I:%M %p")
                else:
                    formatted_time = gmt2_time.strftime("%-I:%M %p")

            notification = NOTIFICATION_RESERVATION_MESSAGE + formatted_time

            time.sleep(3)
            title = self.home.wait_for_notification_message(
                timeout=timeout, message=NOTIFICATION_RESERVATION_MESSAGE)

            if notification in title:
                Report.logPass(f"'{notification}' notification is displayed",
                               is_collabos=True, screenshot=True)
                return True

            Report.logFail(f"'{notification}' is not displayed: '{title}'", is_collabos=True)
            return False
        except Exception:
            current_notification = self.home.get_reservation_notification_message()
            Report.logException(
                f"Notification '{notification}' not found within {timeout} seconds. "
                f"Current notification is {current_notification}", is_collabos=True
            )

    def verify_the_notification_nice_to_see_you_message(self, credentials: dict) -> bool:
        time.sleep(3)
        expected_user_name = (f"{credentials['signin_payload']['name']} "
                              f"{credentials['signin_payload']['surname']}")
        expected_message = f"{NOTIFICATION_NICE_TO_SEE_YOU} {expected_user_name}!"
        Report.logInfo(f"Verify if Notification {expected_message} is displayed.")
        notification_text = self.home.wait_for_notification_message(
            timeout=3, message=expected_message)
        if expected_message == notification_text:
            Report.logPass(f"'{notification_text}' notification is displayed", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(
            f"'{expected_message}' notification is not displayed. "
            f"Current text: {notification_text}",
            is_collabos=True
        )
        return False

    def verify_the_notification_welcome_message(self) -> bool:
        time.sleep(3)
        expected_message = f"{WELCOME_MESSAGE}"
        notification_text = self.home.wait_for_notification_message(
            timeout=15, message=expected_message)
        if expected_message == notification_text:
            Report.logPass(f"'{notification_text}' notification is displayed", is_collabos=True,
                           screenshot=True)
            return True
        Report.logFail(
            f"'{expected_message}' notification is not displayed. "
            f"Current text: {notification_text}",
            is_collabos=True
        )
        return False

    def click_the_notification_action_button(self, notification_button_text: str) -> None:
        if self.home.verify_notification_action_button_is_diplayed(text=notification_button_text):
            Report.logPass(f"'{notification_button_text}' button is displayed", is_collabos=True,
                           screenshot=True)
            self.home.click_notification_action()
        else:
            Report.logFail(f"'{notification_button_text}' button is not displayed.",
                           is_collabos=True)

    def verify_the_notification_action_button_is_displayed(self, notification_button_text: str
                                                           ) -> None:
        if self.home.verify_notification_action_button_is_diplayed(text=notification_button_text):
            Report.logPass(f"'{notification_button_text}' button is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{notification_button_text}' button is NOT displayed.",
                           is_collabos=True)

    def verify_check_in_via_mobile_app_button_is_displayed(self) -> None:
        if self.home.verify_check_in_via_mobile_app_button_displayed():
            Report.logPass(f"'{CHECK_IN_VIA_TUNE_MOBILE}' button is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{CHECK_IN_VIA_TUNE_MOBILE}' button is not displayed.",
                           is_collabos=True)

    def click_check_in_via_tune_mobile(self) -> None:
        self.home.click_check_in_via_mobile_app_button_displayed()

    def click_back_on_check_in_via_mobile_app(self) -> None:
        self.home.click_back_on_check_in_via_mobile_app_button()

    def verify_coily_reservation_is_needed(self) -> None:
        Report.logInfo(f"Verify if error window '{NOTIFICATION_RESERVATION_NEEDED}' is displayed.")
        time.sleep(3)
        title, message = self.home.get_booking_message()
        if NOTIFICATION_RESERVATION_NEEDED in title:
            Report.logPass(f"'{NOTIFICATION_RESERVATION_NEEDED}' notification is displayed",
                           is_collabos=True, screenshot=True)
        else:
            Report.logFail(
                f"'{NOTIFICATION_RESERVATION_NEEDED}' notification is not displayed: {title}",
                is_collabos=True
            )

    def click_got_it(self) -> None:
        self.home.click_got_it_on_error_screen()

    def verify_coily_checking_in_taking_so_long_notification(self) -> None:
        title = self.home.wait_for_notification_on_checking_window(
            timeout=20, message=TAKING_LONGER_THAN_EXPECTED)
        if TAKING_LONGER_THAN_EXPECTED in title:
            Report.logPass(f"'{TAKING_LONGER_THAN_EXPECTED}' message is displayed",
                           is_collabos=True, screenshot=True)
        else:
            Report.logFail(f"'{TAKING_LONGER_THAN_EXPECTED}' message is not displayed: {title}",
                           is_collabos=True)

    def verify_you_cant_use_this_at_this_moment(self) -> None:
        title = self.home.wait_for_message_on_checking_window(
            timeout=50, message=CANT_USE_THIS_DESK_AT_THE_MOMENT)
        if CANT_USE_THIS_DESK_AT_THE_MOMENT in title:
            Report.logPass(f"'{CANT_USE_THIS_DESK_AT_THE_MOMENT}' message is displayed",
                           is_collabos=True, screenshot=True)
        else:
            Report.logFail(
                f"'{CANT_USE_THIS_DESK_AT_THE_MOMENT}' message is not displayed: {title}",
                is_collabos=True
            )

    def verify_the_desk_is_already_reserved(self) -> None:
        title = self.home.wait_for_message_on_checking_window(
            timeout=60, message=THIS_DESK_IS_ALREADY_RESERVED)
        if THIS_DESK_IS_ALREADY_RESERVED in title:
            Report.logPass(f"'{THIS_DESK_IS_ALREADY_RESERVED}' message is displayed",
                           is_collabos=True, screenshot=True)
        else:
            Report.logFail(f"'{THIS_DESK_IS_ALREADY_RESERVED}' message is not displayed: {title}",
                           is_collabos=True)

    def verify_coily_checking_in_notification(self) -> None:
        Report.logInfo(
            f"Verify if '{NOTIFICATION_CHECKING_YOU_IN_MESSAGE}' notification is displayed."
        )
        title = self.home.wait_for_notification_message(timeout=15, message="Checking you in")
        if NOTIFICATION_CHECKING_YOU_IN_MESSAGE in title:
            Report.logPass(f"'{NOTIFICATION_CHECKING_YOU_IN_MESSAGE}' notification is displayed",
                           is_collabos=True, screenshot=True)
        else:
            Report.logFail(
                f"'{NOTIFICATION_CHECKING_YOU_IN_MESSAGE}' notification is NOT displayed. "
                f"Found notification: {title}",
                is_collabos=True
            )

    def verify_coily_couldnt_check_you_in_notification(self) -> None:
        title = self.home.wait_for_notification_message(
            timeout=45, message=NOTIFICATION_COULDNT_CHECK_YOU_IN_MESSAGE)
        if NOTIFICATION_COULDNT_CHECK_YOU_IN_MESSAGE in title:
            Report.logPass(
                f"'{NOTIFICATION_COULDNT_CHECK_YOU_IN_MESSAGE}' notification is displayed.",
                is_collabos=True,
                screenshot=True
            )
        else:
            Report.logFail(
                f"'{NOTIFICATION_COULDNT_CHECK_YOU_IN_MESSAGE}' notification is NOT displayed. "
                f"Found notification: {title}",
                is_collabos=True
            )

    def release_the_desk(self) -> None:
        Report.logInfo('Click the Release button to release the desk.')
        self.home.click_release_the_desk_button()

    def click_release_the_desk_if_visible(self) -> None:
        if self.home.verify_release_the_desk_button():
            Report.logInfo("Release button available", is_collabos=True, screenshot=True)
            self.home.click_release_the_desk_button()
            time.sleep(30)
        else:
            Report.logInfo("Release button not available", is_collabos=True, screenshot=True)

    def verify_away_message(self, status: str, user_credentials: dict) -> None:
        """
        Verify if the given away status and username are displayed correctly.

        :param status: The expected away status.
        :param user_credentials: The expected username.

        :returns: None

        """
        Report.logInfo(f'Verify is away status "{status}" is displayed.')

        coily_desk_status = self.home.get_away_message()
        if coily_desk_status == status:
            Report.logPass("Correct desk status (away message) displayed.", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail("Incorrect desk status (away message) name displayed.", is_collabos=True)

        expected_user_name = (f"{user_credentials['signin_payload']['name']} "
                              f"{user_credentials['signin_payload']['surname']}")
        user_name_away_page = self.home.get_user_name_from_away_page()
        if user_name_away_page == expected_user_name:
            Report.logPass("Correct user name displayed on the Away page.", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(
                f"Incorrect user name displayed on the Away page.: {user_name_away_page}",
                is_collabos=True
            )

    def click_and_verify_away_message(self, msg: str, account_type: str) -> None:
        """

        Perform the following actions:
        - Click on the given message locator.
        - Verify the away message using the provided message and username.

        Parameters:
        - msg (str): The message to be used for verification.
        - account_type (str): The account type to be used for preparing work account credentials.

        """
        locator_for_msg: Tuple[str, str] = (
            TuneCoilyLaptopDisconnectedLocators.CUSTOM_MESSAGE[0],
            TuneCoilyLaptopDisconnectedLocators.CUSTOM_MESSAGE[1].replace('XXX', msg)
        )
        self.home.click_away_state(locator_for_msg)

        work_account_credentials = prepare_work_account_credentials(account_type)
        self.verify_away_message(msg, user_credentials=work_account_credentials)

    def check_if_long_away_message_is_truncated(self, msg: str) -> None:

        custom_message_locator = (
            TuneCoilyLaptopDisconnectedLocators.CUSTOM_MESSAGE[0],
            TuneCoilyLaptopDisconnectedLocators.CUSTOM_MESSAGE[1].replace('XXX', msg[:15])
        )

        self.home.click_away_state(custom_message_locator)
        away_message_on_coily = self.home.get_away_message_strict()

        away_message_on_coily_truncated_list = away_message_on_coily.split('...')
        away_message_on_coily_visible = away_message_on_coily_truncated_list[0]

        if away_message_on_coily_visible in msg:
            Report.logPass(
                "Truncated text on Coily belongs to message set with  Logi Tune Coily Settings",
                is_collabos=True
            )
        else:
            Report.logFail(
                "Truncated text on Coily is not matching with set Away Message in Logi Tune",
                is_collabos=True
            )

    def verify_session_is_over_message(self) -> None:
        Report.logInfo('Verify is "Session is over" is displayed.')
        title, message = self.home.get_session_is_over_message()
        if title == SESSION_OVER_TITLE:
            Report.logPass(f"'{SESSION_OVER_TITLE}' title is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{SESSION_OVER_TITLE}' title is not displayed: {title}",
                           is_collabos=True)

        if SESSION_OVER_TEXT in message:
            Report.logPass(f"'{SESSION_OVER_TEXT}' message is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{SESSION_OVER_TEXT}' message is not displayed: {message}",
                           is_collabos=True)

    def verify_session_is_over_message_v2(self) -> None:
        title, message = self.home.get_session_is_over_message()
        if title == SESSION_OVER_TITLE:
            Report.logPass(f"'{SESSION_OVER_TITLE}' title is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{SESSION_OVER_TITLE}' title is not displayed: {title}",
                           is_collabos=True)

        if SESSION_OVER_TEXT_V2 in message:
            Report.logPass(f"'{SESSION_OVER_TEXT_V2}' message is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{SESSION_OVER_TEXT_V2}' message is not displayed: {message}",
                           is_collabos=True)

    def verify_session_is_over_message_v3(self, verify_message: bool = True) -> None:
        title, message = self.home.get_session_is_over_message()

        if verify_message:
            if title == SESSION_OVER_TITLE:
                Report.logPass(f"'{SESSION_OVER_TITLE}' title is displayed", is_collabos=True,
                               screenshot=True)
            else:
                Report.logFail(f"'{SESSION_OVER_TITLE}' title is not displayed: {title}",
                               is_collabos=True)

            if SESSION_OVER_TEXT_V3 in message:
                Report.logPass(f"'{SESSION_OVER_TEXT_V3}' message is displayed", is_collabos=True,
                               screenshot=True)
            else:
                Report.logFail(f"'{SESSION_OVER_TEXT_V3}' message is not displayed: {message}",
                               is_collabos=True)

    def verify_personal_info_on_you_cant_you_desk_window(self, credentials: dict) -> None:
        message_1 = self.home.get_info_for_who_the_desk_is_booked_for()
        expected_user_name = (f"{credentials['signin_payload']['name']} "
                              f"{credentials['signin_payload']['surname']}")
        expected_message_1 = f"This desk is currently booked by {expected_user_name}."

        message_2 = self.home.get_actually_you_sure_xxx_text()
        expected_message_2 = f"Actually {expected_user_name}?"

        if expected_message_1 in message_1:
            Report.logPass(f"'{expected_message_1}' title is displayed", is_collabos=True,
                           screenshot=True)
            result_1 = True
        else:
            Report.logFail(f"'{expected_message_1}' title is not displayed: {message_1}",
                           is_collabos=True)
            result_1 = False

        if expected_message_2 in message_2:
            Report.logPass(f"'{expected_message_2}' message is displayed", is_collabos=True,
                           screenshot=True)
            result_2 = True
        else:
            Report.logFail(f"'{expected_message_2}' message is not displayed: {message_2}",
                           is_collabos=True)
            result_2 = False

        assert result_1 and result_2, "Wrong messages for occupied desk."

    def verify_session_in_progress_page(self, credentials: dict) -> bool:
        try:
            Report.logInfo(f"Verify session in progress page", is_collabos=True)
            res_1 = self.home.verify_session_in_progress_displayed()

            user_name = self.home.get_user_name_from_booked_screen()
            expected_user_name = (f"{credentials['signin_payload']['name']} "
                                  f"{credentials['signin_payload']['surname']}")
            if user_name and user_name in expected_user_name:
                Report.logPass(f"'{expected_user_name}' message is displayed", is_collabos=True,
                               screenshot=True)
                res_2 = True
            else:
                Report.logWarning(f"'{expected_user_name}' message is not displayed: {user_name}",
                                  is_collabos=True)
                res_2 = False

            return res_1 and res_2
        except Exception as e:
            Report.logWarning(f"'Session in progress' not displayed correctly: {e}")
            return False

    def verify_booked_in_x_minutes_for_user_page(self, credentials: dict, end_time: str) -> bool:
        Report.logInfo(f"Verify 'Booked in x minutes for' page", is_collabos=True)

        timestamp = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Get the current time
        current_time = datetime.utcnow()

        # Calculate the time difference in minutes
        time_difference_minutes = math.ceil((timestamp - current_time).total_seconds() / 60)

        expected_msg_1 = f"Booked in {time_difference_minutes} min for"
        expected_msg_2 = f"Booked in {time_difference_minutes - 1} min for"

        msg_1 = self.home.get_booked_in_x_minutes_for_text()

        if msg_1 in [expected_msg_1, expected_msg_2]:
            Report.logPass(f"'{expected_msg_1}' message is displayed", is_collabos=True,
                           screenshot=True)
            res_1 = True
        else:
            Report.logWarning(f"'{expected_msg_1}' message is not displayed: {msg_1}",
                              is_collabos=True)
            res_1 = False

        user_name = self.home.get_user_name_from_booked_screen()
        expected_user_name = (f"{credentials['signin_payload']['name']} "
                              f"{credentials['signin_payload']['surname']}")
        if user_name and user_name in expected_user_name:
            Report.logPass(f"'{expected_user_name}' message is displayed", is_collabos=True,
                           screenshot=True)
            res_2 = True
        else:
            Report.logWarning(f"'{expected_user_name}' message is not displayed: {user_name}",
                              is_collabos=True)
            res_2 = False

        return res_1 and res_2

    def verify_booked_in_x_minutes_center_notification(self, end_time: str) -> bool:
        Report.logInfo(f"Verify 'Booked in x minutes for' page", is_collabos=True)

        timestamp = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Get the current time
        current_time = datetime.utcnow()

        # Calculate the time difference in minutes
        time_difference_minutes = math.ceil((timestamp - current_time).total_seconds() / 60)

        if time_difference_minutes < 60:
            expected_msg_1 = f"Booked in {time_difference_minutes} minutes"
            expected_msg_2 = f"Booked in {time_difference_minutes - 1} minutes"
        else:
            hours = time_difference_minutes // 60
            minutes = time_difference_minutes % 60

            if minutes == 0:  # Check if there are no remaining minutes
                expected_msg_1 = f"Booked in {hours} hour{'s' if hours != 1 else ''}"
            else:
                expected_msg_1 = (f"Booked in {hours} hour{'s' if hours != 1 else ''} "
                                  f"and {minutes} minute{'s' if minutes != 1 else ''}")

            if minutes == 0:
                hours -= 1
                minutes = 59
            else:
                minutes -= 1
            expected_msg_2 = (f"Booked in {hours} hour{'s' if hours != 1 else ''} "
                              f"and {minutes} minute{'s' if minutes != 1 else ''}")

        msg_1 = self.home.get_time_left_to_beginning_of_reservation()

        if msg_1 and msg_1 in [expected_msg_1, expected_msg_2]:
            Report.logPass(f"'{expected_msg_1}' message is displayed", is_collabos=True,
                           screenshot=True)
            return True
        Report.logWarning(f"'{expected_msg_1}/{expected_msg_2}' message is not displayed: {msg_1}",
                          is_collabos=True)
        return False

    def verify_countdown_icon_displayed(self):
        Report.logInfo(f"Check if countdown icon is displayed (last minute of the reservation)")
        return self.home.verify_countdown_icon_is_displayed(timeout=310)

    def click_cancel_transfer_desk(self):
        self.home.click_cancel_transfer_desk()


    def verify_desk_will_be_released(self, verify_message=True) -> None:
        result = self.verify_countdown_icon_displayed()
        if result:
            Report.logPass(f"Countdown icon is displayed", is_collabos=True, screenshot=True)
        else:
            Report.logFail(f"Countdown icon is NOT displayed", is_collabos=True, screenshot=True)

        if verify_message:
            title, message = self.home.get_session_is_over_message()
            if title == DESK_WILL_BE_RELEASED_TITLE:
                Report.logPass(f"'{DESK_WILL_BE_RELEASED_TITLE}' title is displayed", is_collabos=True,
                               screenshot=True)
            else:
                Report.logFail(f"'{DESK_WILL_BE_RELEASED_TITLE}' title is not displayed: {title}",
                               is_collabos=True)

            if DESK_WILL_BE_RELEASED_TEXT in message:
                Report.logPass(f"'{DESK_WILL_BE_RELEASED_TEXT}' message is displayed", is_collabos=True,
                               screenshot=True)
            else:
                Report.logFail(f"'{DESK_WILL_BE_RELEASED_TEXT}' message is not displayed: {message}",
                               is_collabos=True)

        self.verify_session_is_over_v3(verify_message)

    def verify_session_is_over_v3(self, verify_message):
        result = self.home.verify_clock_icon_is_displayed(timeout=60)
        if result:
            Report.logPass(f"Clock icon is displayed", is_collabos=True, screenshot=True)
        else:
            Report.logFail(f"Clock icon is NOT displayed", is_collabos=True, screenshot=True)
        self.verify_session_is_over_message_v3(verify_message=verify_message)

    def click_center_pile_with_time_left_in_the_reservation(self):
        Report.logInfo(f"Click on on the center pile message with time left in the reservation.")
        self.home.click_center_pile_with_time_left_in_the_reservation()

    def verify_center_pile_message(self, end_time: str, time_format: str = FORMAT_AMPM) -> None:
        self.click_center_pile_with_time_left_in_the_reservation()

        title, message = self.home.get_desk_time_limit_messages()
        if title == DESK_LIMIT_TITLE:
            Report.logPass(f"'{DESK_LIMIT_TITLE}' title is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{DESK_LIMIT_TITLE}' title is not displayed: {title}",
                           is_collabos=True)

        utc_time = datetime.strptime(end_time[:-1], "%Y-%m-%dT%H:%M:%S.%f")

        # Set the timezone for the input time as UTC
        utc_timezone = pytz.timezone('UTC')
        utc_time = utc_timezone.localize(utc_time)

        # Define GMT+2 timezone
        # gmt2_timezone = pytz.timezone('Etc/GMT-2')
        from tzlocal import get_localzone_name
        gmt2_timezone = pytz.timezone(get_localzone_name())

        # Convert the time to GMT+2
        gmt2_time = utc_time.astimezone(gmt2_timezone)

        formatted_time = ''
        if time_format == FORMAT_24H:
            formatted_time = gmt2_time.strftime("%H:%M")
        elif time_format == FORMAT_AMPM:
            if get_custom_platform() == "windows":
                formatted_time = gmt2_time.strftime("%#I:%M %p")
            else:
                formatted_time = gmt2_time.strftime("%-I:%M %p")

        notification = DESK_LIMIT_MESSAGE + formatted_time

        if notification in message:
            Report.logPass(f"'{notification}' message is displayed", is_collabos=True,
                           screenshot=True)
        else:
            Report.logFail(f"'{notification}' message is not displayed: {message}",
                           is_collabos=True)

        self.click_desk_limit_got_it_button()

    def click_desk_limit_got_it_button(self):
        Report.logInfo(f"Click on 'Got it' button")
        self.home.click_desk_limit_got_it_button()

    @staticmethod
    def compare_sync_portal_and_coily_settings(sync_settings: dict, coily_settings: dict) -> None:
        sync_settings.pop('locale')
        flag = True
        Report.logInfo("Comparing settings from SYNC portal vs settings on Coily")
        Report.logInfo(f"Current settings in Sync Portal: {sync_settings}")
        Report.logInfo(f"Current settings in Coily Settings Page: {coily_settings}")
        for key, value in sync_settings.items():
            if coily_settings[key] != value:
                flag = False
                Report.logFail(
                    f"Parameter {key} value: {value} does not match with Sync Portal setting",
                    is_collabos=True,
                    screenshot=True
                )
        if flag:
            Report.logPass("All parameters match")

    def compare_tune_settings_with_coily_settings(self, tune_settings: dict,
                                                  coily_settings: dict) -> None:
        flag = True
        Report.logInfo("Comparing settings from Logi Tune vs settings on Coily")
        tune_settings['screen_brightness'] = self.tune_brightness_to_coily_brighness(
            tune_settings['screen_brightness'])
        for key, value in tune_settings.items():
            if coily_settings[key] != value:
                flag = False
                Report.logFail(
                    f"Parameter {key} value in Tune Settings: {value} "
                    f"does not match with Coily  setting: {coily_settings[key]}",
                    is_collabos=True,
                    screenshot=True
                )
        if flag:
            Report.logPass("All parameters match")

    def check_if_correct_format_displayed_on_coily(self, time_format: str) -> None:
        clock_present = self.verify_element_collabos(TuneCoilyMainPageLocators.CLOCK)

        if clock_present:
            current_time_coily = self.find_element_collabos(TuneCoilyMainPageLocators.CLOCK).text
            current_time = get_current_time(time_format)
            if current_time_coily in current_time:
                Report.logPass(
                    f"Current Time on Coily: {current_time_coily} matches Current time with"
                    f" {time_format} h format",
                    is_collabos=True
                )
            else:
                Report.logFail(
                    f"Current Time on Coily: {current_time_coily} does not match Current time with"
                    f" {time_format} h format",
                    is_collabos=True
                )
        else:
            Report.logFail("Clock not found on Coily Screen")

    def verify_coily_is_checked_in_walk_in_session_notification_without_time(
            self, timeout: int = 30) -> None:
        Report.logInfo(
            f'Verify if reservation is confirmed with text "{NOTIFICATION_RESERVATION_MESSAGE}"'
        )
        time.sleep(3)
        self.home.wait_for_notification_message(timeout=timeout,
                                                message=NOTIFICATION_RESERVATION_MESSAGE)

    def verify_privacy_mode_main_page(self, privacy_mode: bool, time_format: str,
                                      meetings: list) -> None:
        if not privacy_mode:
            self.extend_agenda_view()
            for meeting in meetings:
                start_time = meeting.get("meeting_start_time")
                event_title = f'{meeting.get("event_title")}: {start_time}'
                duration_min = meeting.get("duration_min")
                self.verify_agenda_item(event_title=event_title,
                                        start_time=start_time,
                                        duration_min=duration_min,
                                        time_format=time_format)
            self.close_agenda_view()
        else:
            privacy_element = self.home.get_privacy_mode_events()
            first_meeting = meetings[0]
            no_events = len(meetings)
            if self.home.check_if_no_meetings_match_in_privacy_mode(no_events):
                Report.logPass(f"Number of meetings in calendar {no_events} "
                               f"matches number of meetings on Coily in Privacy Mode",
                               screenshot=True,
                               is_collabos=True)
            else:
                Report.logFail(f"Number of meetings in calendar {no_events} "
                               f"do not match number of meetings in Privacy Mode",
                               screenshot=True,
                               is_collabos=True)

            start_time = first_meeting.get("meeting_start_time")
            duration_min = first_meeting.get("duration_min")
            self.verify_agenda_time_frames(privacy_element, start_time, duration_min, time_format)

    @staticmethod
    def tune_brightness_to_coily_brighness(value: int) -> int:
        return int((value - 1)/99 * 255)

    def compare_brightness_tune_coily(self, tune_brightness: int, coily_brightness: int) -> None:
        tune_to_coily = self.tune_brightness_to_coily_brighness(tune_brightness)
        compare_result = tune_to_coily == coily_brightness
        if not compare_result:
            Report.logInfo(
                f"Tune brightness ({tune_brightness}) calculated to Coily brightness "
                f"({tune_to_coily}) is not matching Coily Brightness ({coily_brightness})",
                is_collabos=True
            )
        else:
            Report.logPass(
                f"Tune brightness ({tune_brightness}) calculated to Coily brightness "
                f"({tune_to_coily}) is matching Coily Brightness ({coily_brightness})",
                is_collabos=True
            )

    def check_make_reservation_page(self):
        Report.logInfo("Checking if Book Desk Button is visible", is_collabos=True)
        if not self.verify_element_collabos(TuneWalkinDisabledLocators.BOOK_DESK_BUTTON):
            Report.logException("Book Desk Button is not visible", is_collabos=True)
        else:
            Report.logInfo("Book Desk Button is visible as intended", screenshot=True, is_collabos=True)

        expected_book_button_text = "Book desk"

        Report.logInfo(f"Checking if Book Desk Button has correct text: {expected_book_button_text}",
                       is_collabos=True)
        visible_book_button_text = self.find_element_collabos(TuneWalkinDisabledLocators.BOOK_DESK_BUTTON).text
        if expected_book_button_text.lower() not in visible_book_button_text.lower():
            Report.logException(f"Book Desk Button text is NOK: {visible_book_button_text}", is_collabos=True)
        else:
            Report.logInfo("Book Desk Button has correct text", screenshot=True, is_collabos=True)

        Report.logInfo("Checking if Title Label with 'To use this desk you need to "
                       "make a reservation is visible'",
                       is_collabos=True)
        if not self.verify_element_collabos(TuneWalkinDisabledLocators.TITLE_LABEL):
            Report.logException("Title Label is not visible", is_collabos=True)
        else:
            Report.logInfo("Title label is visible as intended", screenshot=True, is_collabos=True)

        expected_title_text = 'To use this desk, you need to make a reservation'
        Report.logInfo("Checking if Title Message is correct: To use this desk, you need to make a reservation",
                       is_collabos=True)
        visible_title_text = self.find_element_collabos(TuneWalkinDisabledLocators.TITLE_LABEL).text
        if expected_title_text not in visible_title_text:
            Report.logException(f"Expected text not in visible text, visible text: {visible_title_text}, "
                                f"expected text: {expected_title_text}", is_collabos=True)
        else:
            Report.logInfo("Expected text in visible title text which is OK", screenshot=True, is_collabos=True)

        Report.logInfo("Checking if message is visible", is_collabos=True)
        if not self.verify_element_collabos(TuneWalkinDisabledLocators.MESSAGE_LABEL):
            Report.logException("Message Label is not visible", is_collabos=True)
        else:
            Report.logInfo("Message label is visible as intended", screenshot=True, is_collabos=True)

        expected_msg_text = [
            "Your organization requires you to book desks in advance before using them.",
            "This policy ensures fair access to the shared workspace.",
            "To reserve this desk, use Logi Tune and search for the desk or scan the QR code to open the app."
        ]
        visible_msg_text = self.find_element_collabos(TuneWalkinDisabledLocators.MESSAGE_LABEL).text
        for expected_msg in expected_msg_text:
            Report.logInfo(f"Checking if {expected_msg} visible in visible message", is_collabos=True)
            if expected_msg not in visible_msg_text:
                Report.logException(f"Expected text not in visible text, visible text: {visible_title_text}, "
                                    f"expected text: {expected_title_text}", is_collabos=True)
            else:
                Report.logInfo("Expected text in visible title text which is OK",
                               screenshot=True, is_collabos=True)

        Report.logInfo("Clicking Book desk button", is_collabos=True)
        self.find_element_collabos(TuneWalkinDisabledLocators.BOOK_DESK_BUTTON).click()
        expected_popup_title = 'Scan QR code to book the desk'
        Report.logInfo(f"Checking if {expected_popup_title} is visible in the title", is_collabos=True)
        visible_popup_title = self.find_element_collabos(TuneWalkinDisabledLocators.QR_POPUP_TITLE).text
        if expected_popup_title not in visible_popup_title:
            Report.logException(f"Expected popup title: {expected_popup_title} is not present in visible title:"
                                f" {visible_popup_title}", is_collabos=True)

        expected_popup_msg = 'To reserve this desk, scan the QR code and use the Logi Tune mobile app to continue.'
        Report.logInfo(f"Checking if {expected_popup_msg} is present in the visible popup msg", is_collabos=True)
        visible_popup_msg = self.find_element_collabos(TuneWalkinDisabledLocators.QR_POPUP_MSG).text
        if expected_popup_msg not in visible_popup_msg:
            Report.logException(f"Expected popup title: {expected_popup_msg} is not present in visible title:"
                                f" {visible_popup_msg}", is_collabos=True)
        else:
            Report.logInfo(f"Expected popup title: {expected_popup_msg} is present in visible title:",
                           screenshot=True, is_collabos=True)

        expected_popup_button_msg = "GOT IT"
        Report.logInfo(f"Checking GOT IT button has correct text", is_collabos=True)
        visible_popup_button_msg = self.find_element_collabos(TuneWalkinDisabledLocators.QR_POPUP_BUTTON).text
        if expected_popup_button_msg not in visible_popup_button_msg:
            Report.logException(f"Expected popup title: {expected_popup_button_msg} is "
                                f"not present in visible title:"
                                f" {visible_popup_button_msg}", is_collabos=True)
        else:
            Report.logInfo(f"Expected popup title: {expected_popup_button_msg} is "
                           f" present in visible title", screenshot=True, is_collabos=True)

        Report.logInfo("Clicking GOT IT button")
        self.find_element_collabos(TuneWalkinDisabledLocators.QR_POPUP_BUTTON).click()
        Report.logInfo("Checking if previous title is visible again")
        Report.logInfo("Checking if Title Message is correct: To use this desk, you need to make a reservation",
                       is_collabos=True)
        visible_title_text = self.find_element_collabos(TuneWalkinDisabledLocators.TITLE_LABEL).text
        if expected_title_text not in visible_title_text:
            Report.logException(f"Expected text not in visible text, visible text: {visible_title_text}, "
                                f"expected text: {expected_title_text}", is_collabos=True)
        else:
            Report.logInfo("Expected text in visible title text which is OK", is_collabos=True)

    def check_already_have_a_session_page(self, booked_desk_name: str):
        expected_title = 'You’re already having a session'
        Report.logInfo("Checking if expected title after connecting to wrong desk is visible: "
                       f"{expected_title}", is_collabos=True)
        visible_title = self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.TITLE_LABEL).text
        if expected_title not in visible_title:
            Report.logException(f"Wrong title visible: {visible_title}", is_collabos=True)
        else:
            Report.logInfo("Correct title visible", screenshot=True, is_collabos=True)

        expected_message = f"Move your session from {booked_desk_name}?"

        Report.logInfo("Checking if expected message after connecting to wrong desk is visible: "
                       f"{expected_message}", is_collabos=True)
        visible_message = self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.MESSAGE_LABEL).text
        if expected_message not in visible_message:
            Report.logException(f"Wrong message visible: {visible_message}", is_collabos=True)
        else:
            Report.logInfo("Correct message visible", screenshot=True, is_collabos=True)

        expected_transfer_desk_button_text = "Use this desk"
        Report.logInfo(f"Checking if agree button contains correct text: {expected_transfer_desk_button_text}")

        visible_transfer_button_message = (
            self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.TRANSFER_BUTTON).text)
        if expected_transfer_desk_button_text not in visible_transfer_button_message:
            Report.logException(f"Wrong message visible: {visible_transfer_button_message}", is_collabos=True)
        else:
            Report.logInfo("Correct text visible", screenshot=True, is_collabos=True)

        expected_cancel_button_text = "Cancel"
        Report.logInfo(f"Checking if agree button contains correct text: {expected_cancel_button_text}")

        visible_transfer_button_message = (
            self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.CANCEL_BUTTON).text)
        if expected_cancel_button_text not in visible_transfer_button_message:
            Report.logException(f"Wrong message visible: {visible_transfer_button_message}", is_collabos=True)
        else:
            Report.logInfo("Correct text visible", screenshot=True, is_collabos=True)

    def check_already_have_session_cancel_button_clicked(self):
        Report.logInfo("Clicking Cancel button")
        expected_title = 'You already have a session'
        self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.CANCEL_BUTTON).click()

        Report.logInfo("Checking if expected title after clicking CANCEL button is visible: "
                       f"{expected_title}", is_collabos=True)
        visible_title = self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.TITLE_LABEL).text
        if expected_title not in visible_title:
            Report.logException(f"Wrong title visible: {visible_title}", is_collabos=True)
        else:
            Report.logInfo("Correct title visible", screenshot=True, is_collabos=True)

        expected_cancel_message = "This is not the desk you have reserved"

        Report.logInfo("Checking if expected message after clicking CANCEL button is visible: "
                       f"{expected_cancel_message}", is_collabos=True)
        visible_cancel_message = self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.MESSAGE_LABEL).text
        if expected_cancel_message not in visible_cancel_message:
            Report.logException(f"Wrong message visible: {visible_cancel_message}", is_collabos=True)
        else:
            Report.logInfo("Correct message visible", screenshot=True, is_collabos=True)

    def check_already_have_session_agree_button_clicked(self, booking_start_time: datetime,
                                                        booking_duration: int,
                                                        time_format: str,
                                                        desk_name: str):
        Report.logInfo("Clicking Use this desk button")

        self.find_element_collabos(TuneCoilyAlreadyHaveSessionLocators.TRANSFER_BUTTON).click()

        self.verify_coily_is_checked_in_walk_in_session_notification(booking_start_time,
                                                                     booking_duration//60,
                                                                     time_format=time_format)



