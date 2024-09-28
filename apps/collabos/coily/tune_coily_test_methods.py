import os
import random
import string
import time
from datetime import timedelta, datetime

from selenium.webdriver.common.by import By

from apps.collabos.coily.coily_messages import GOT_IT, LEARN_MORE, MSG_BE_BACK_SOON, MSG_IN_A_MEETING, MSG_OUT_FOR_LUNCH
from apps.collabos.coily.coily_sync_portal_methods import CoilySyncMethods
from apps.collabos.coily.tune_coily_config import COILY_DEVICE_NAME, GOOGLE, MICROSOFT, SYNC_PORTAL_STATUSES, AVAILABLE, IN_USE, IN_USE_AWAY
from apps.collabos.coily.coily_methods import TuneCoilyMethods
from apps.collabos.coily.utilities import get_curent_time, check_and_connect_device, prepare_work_account_credentials, \
    restart_scheduler_app_via_adb
from apps.tune.tune_calendar_methods import CalendarMethods
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from apps.tune.TunesAppInstall import TunesUIInstallWindows
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS
from base import global_variables
from base.base_settings import TUNEAPP_NAME
from base.base_ui import UIBase
from common.framework_params import COILY_DESK_IP, COILY_PERIPHERALS, INSTALLER
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all, connect_device_no_sleeps, disconnect_device_no_sleeps
from extentreport.report import Report
from locators.coily_locators import TuneCoilyLaptopDisconnectedLocators
from apps.collabos.coily.pages.tune_coily_settings_page import TuneCoilySettingsPage
from apps.collabos.coily.pages.tune_coily_logitune_settings_page import LogiTuneCoilyDeviceSettingsPage
from typing import Union, Tuple
from apps.collabos.coily.tune_coily_config import FORMAT_24H, FORMAT_AMPM
from common.platform_helper import get_all_values_to_cover_from_dict_of_lists, change_camel_case_to_snake_case
from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios


WIN_APP_BAT_PATH = "\\WinApp\\winapp.bat"
WIN_APP_CLOSE_BAT_PATH = "\\WinApp\\winapp_close.bat"


class TuneCoilyTests:
    device_name = COILY_DEVICE_NAME
    sync_portal_services = None
    global_variables.SYNC_ENV = 'raiden-latest1'
    reservation = None
    calendar_api = None
    event_id = None
    calendar_methods = None

    def __init__(self, coily_methods: TuneCoilyMethods):
        self.coily_methods: TuneCoilyMethods = coily_methods
        self.appium_service = self.coily_methods.appium_service
        self.sync_portal_services = CoilySyncMethods()
        self.tune_app = TuneElectron()
        self.tune_methods = TuneUIMethods()
        self.coily_peripherals = self._get_coily_peripherals()
        self.logi_tune_coily_settings_page = LogiTuneCoilyDeviceSettingsPage(self.tune_app)
        self.coily_settings_page = TuneCoilySettingsPage(self.coily_methods)

    def get_current_sync_portal_coily_settings(self, parameter: str = None):
        settings = self.sync_portal_services.get_coily_settings()
        reformatted_settings = {}
        for key, value in settings.items():
            reformatted_settings[change_camel_case_to_snake_case(key)] = value
        if parameter:
            return reformatted_settings.get(parameter)
        return reformatted_settings

    @staticmethod
    def _get_coily_peripherals():
        if "None" in COILY_PERIPHERALS:
            return None
        return COILY_PERIPHERALS.split('|')

    def tc_walk_in_session_enabled_logi_tune_not_installed(self):
        """
        Test method to check that anonymous session is created after connecting Coily laptop without Logi Tune.
        """
        try:
            # Set walk in session duration in Sync Portal
            reservation_time_duration = random.randint(1, 6)
            Report.logInfo(f'Set Walk-in session time duration to: {reservation_time_duration}')
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Get the start time for the walk-in session
            start_time = get_curent_time()
            Report.logInfo(f'Coily connected. Reservation start time: {start_time}')

            # Verify 'Checking you in...' notification
            self.verify_anonymous_user_check_in_notifications(reservation_time_duration, start_time)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Session is over message
            self.coily_methods.open_app()
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_enabled_install_tune_log_in_to_work_account(self, work_account_type, credentials):
        """
        Test scenario:
            1. Connect Coily to laptop without Logi Tune.
            2. Check if anonymous session has been created.
            3. Install Logi Tune and connect correct user in Work Account.
            4. Check if anonymous session has been changed into identified session.
            5. Release the desk
        """
        try:

            # Uninstall Logi Tune
            Report.logInfo(f"Uninstall existing LogiTune.")
            if get_custom_platform() == "windows":
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
                app = TunesUIInstallWindows()
                if app.check_for_app_installed_win(TUNEAPP_NAME):
                    app.uninstall_app()
                os.system(str(UIBase.rootPath) + WIN_APP_CLOSE_BAT_PATH)
            else:
                app = TunesUIInstallMacOS()
                if app.check_tune_installed_macos():
                    app.uninstallApp()
            time.sleep(5)

            # Set walk-in session duration in Sync Portal
            reservation_time_duration = random.randint(1, 12)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Start appium_service
            check_and_connect_device(COILY_DESK_IP)
            time.sleep(2)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Get the start time for the walk-in session
            start_time_anonymous = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time_anonymous}')

            # Verify 'Checking you in...' notification
            self.coily_methods.open_app()
            self.coily_methods.verify_coily_checking_in_notification()
            self.coily_methods.verify_the_notification_action_button_is_displayed(
                notification_button_text=LEARN_MORE)

            # Verify if Coily is checked in notification
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time_anonymous,
                time_offset=reservation_time_duration,
                time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Install Logi Tune
            if get_custom_platform() == "windows":
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)

            self.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)
            if get_custom_platform() == "windows":
                os.system(str(UIBase.rootPath) + WIN_APP_CLOSE_BAT_PATH)

            # Log in to Work Account in Logi Tune
            self.tune_methods.tune_app.open_tune_app()
            time.sleep(5)
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type,
                                                                account_credentials=credentials)

            time.sleep(2)

            # Get the start time for the walk-in session
            start_time_user_session = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time_user_session}')

            # Verify if Coily is checked in notifications
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time_anonymous,
                time_offset=reservation_time_duration,
                time_format=self.sync_portal_services.desk_settings_time_format)
            self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
            self.coily_methods.verify_the_notification_nice_to_see_you_message(
                credentials=credentials)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            self.coily_methods.release_the_desk()

            # Verify Session is over message
            time.sleep(1)
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(3)

            # Verify Coily  and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_enabled_user_not_logged_in(self):
        """
        Test scenario:
            1. Connect Coily to laptop with Logi Tune. No user linked to Work Account.
            2. Check if anonymous session has been created.
            3. Disconnect Coily.
        """
        try:
            # Set walk-in session duration in Sync Portal
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Verify Coily Idle Page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Get the start time for the walk-in session
            start_time = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time}')

            # Verify Coily checkin notifications
             
            time.sleep(1)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily
            self._disconnect_coily()

            # Verify Session Is Over is displayed
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()
            time.sleep(1)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_disabled_user_not_logged_in(self):
        """
        Test scenario:
                1. Walk-in session is disabled in Logi Tune.
                2. Connect Coily to laptop with Logi Tune. No user linked to Work Account.
                2. Check if Coily shows error.
                3. Disconnect self.coily_methods.
        """
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Verify "You need a reservation" error


            self.coily_methods.verify_coily_reservation_is_needed()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            time.sleep(2)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_enabled_user_logged_in(self, account_type: str = None):
        """
        Test scenario:
            1. Connect Coily to laptop with Logi Tune and user linked to Work account.
            2. Check if identified session has been created
            3. Disconnect Coily and choose Awy state.
            4. Connect Coily and verify that it authenticates back.
            5. Repeat steps 3 and 4 for all Away states.
            6. Release the desk
        """
        try:
            work_account_credentials = prepare_work_account_credentials(account_type)

            # Create Calendar event for the user
            event_details = {
                'account_type': account_type,
                'credentials': work_account_credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            # Create Calendar event
            meeting_title = self._create_calendar_event(event_details)

            # Set walk-in session duration
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            time.sleep(5)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)

            # Connect Coily to laptop
            self._connect_coily()
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()
            start_time = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time}')

            # Verify if Coily is checked in notification

            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()
            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")

            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(IN_USE)

            away_states = {
                MSG_BE_BACK_SOON: TuneCoilyLaptopDisconnectedLocators.BE_BACK_SOON,
                MSG_IN_A_MEETING: TuneCoilyLaptopDisconnectedLocators.IN_A_MEETING,
                MSG_OUT_FOR_LUNCH: TuneCoilyLaptopDisconnectedLocators.OUT_FOR_LUNCH
            }

            for msg, locator in away_states.items():

                # Disconnect Coily from laptop
                self._disconnect_coily()

                # Choose and validate Away state
                self.coily_methods.home.click_away_state(locator)
                self.coily_methods.verify_away_message(status=msg, user_credentials=work_account_credentials)

                time.sleep(3)

                # Verify Coily and peripherals are disconnected from LogiTune
                self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

                # Verify Coily status in Sync Portal
                self._verify_desk_status_in_sync_portal(IN_USE_AWAY)

                # Connect Coily to laptop
                self._connect_coily()

                # Verify if Coily is checked in notification
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              timeout=30,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)

                # Verify Coily authenticated page
                self._verify_coily_authenticated_page()

                # Verify Agenda is displayed
                self._verify_agenda_event(event_details)

                # Verify Coily and peripherals are detected in LogiTune
                self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

                # Verify Coily status in Sync Portal
                self._verify_desk_status_in_sync_portal(IN_USE)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)

    def tc_walk_in_session_enabled_user_logged_in_coily_reconnection(self, account_type: str = None):
        """
        Test scenario:
            1. Connect Coily to laptop with Logi Tune and user linked to Work Account.
            2. Check if identified session has been created
            3. Disconnect Coily and reconnect it immediately.
            4. Verify that Coily authenticates back.
            4. Disconnect Coily and wait more than 60 sec.
            5. First Away state shall be chosen.
            6. Connect Coily to the laptop.
            7. Verify that Coily authenticates back.
            8. Release the desk.
        """
        try:
            # Set walk-in session duration
            reservation_time_duration = random.randint(1, 12)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            work_account_credentials = prepare_work_account_credentials(account_type)

            # Create Calendar event for the user
            event_details = {
                'account_type': account_type,
                'credentials': work_account_credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            meeting_title = self._create_calendar_event(event_details)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            time.sleep(5)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Get the estimated start time for walk in session
            start_time = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time}')

            # Verify if Coily is checked in notification
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()
            # Verify Agenda is displayed
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            Report.logInfo("Wait for less than 5 sec and quickly reconnect Coily")
            time.sleep(5)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify if Coily is checked in notification
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                          time_offset=reservation_time_duration,
                                                                          time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify Agenda is displayed
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Wait for more 60 sec and check if away state is activated
            Report.logInfo("Wait for more than 60 sec and reconnect Coily")
            time.sleep(65)
            self.coily_methods.verify_away_message(status=MSG_BE_BACK_SOON, user_credentials=work_account_credentials)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify if Coily is checked in notification
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                          time_offset=reservation_time_duration,
                                                                          time_format=self.sync_portal_services.desk_settings_time_format)
            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify Agenda is displayed
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_disabled_user_logged_in(self, account_type=None):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Open Logi Tune and connect to Work account
            work_account_credentials = prepare_work_account_credentials(account_type)
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            time.sleep(5)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            # Verify "You need a reservation" error


            self.coily_methods.verify_coily_reservation_is_needed()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_over_on_work_account_account_disconnection(self, account_type: str = None):
        try:
            # Set walk-in session duration
            reservation_time_duration = random.randint(1, 12)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Open Logi Tune and connect to Work account
            work_account_credentials = prepare_work_account_credentials(account_type)
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            time.sleep(5)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()
            start_time = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time}')

            # Verify if Coily is checked in notification

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect work account in Logi Tune
            self.tune_methods.tc_disconnect_connected_account()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message_v3()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_booked_session_and_user_not_logged_in(self, credentials):
        try:
            # Enable walk-in session for duration 1h
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(1)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(credentials, reservation_time_duration)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification


            self.coily_methods.verify_checking_you_in_message_window()

            # Verify 'Taking so long' notification
            self.coily_methods.verify_coily_checking_in_taking_so_long_notification()
            self.coily_methods.verify_check_in_via_mobile_app_button_is_displayed()

            # Verify 'You can’t use this desk at the moment'
            self.coily_methods.verify_you_cant_use_this_at_this_moment()
            self.coily_methods.verify_personal_info_on_you_cant_you_desk_window(credentials)
            self.coily_methods.verify_check_in_via_mobile_app_button_is_displayed()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(1)

            # Verify 'Session in progres' id displayed


            result = self.coily_methods.verify_session_in_progress_page(credentials)
            assert result is True, Report.logFail("Session in progress page not displayed correctly")

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_booked_session_and_user_logged_in(self, account_type, credentials):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Create Calendar event for the user
            event_details = {
                'account_type': account_type,
                'credentials': credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            meeting_title = self._create_calendar_event(event_details)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=credentials)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(credentials,
                                                                           reservation_duration=random.randint(1, 6))

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
             

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Verify Agenda events on Coily
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")
            self._verify_agenda_event(event_details)

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(IN_USE)

            away_states = {
                MSG_BE_BACK_SOON: TuneCoilyLaptopDisconnectedLocators.BE_BACK_SOON,
                MSG_IN_A_MEETING: TuneCoilyLaptopDisconnectedLocators.IN_A_MEETING,
                MSG_OUT_FOR_LUNCH: TuneCoilyLaptopDisconnectedLocators.OUT_FOR_LUNCH
            }

            for msg, locator in away_states.items():

                # Disconnect Coily from laptop
                self._disconnect_coily()

                # Choose and verify Away state on Coily
                self.coily_methods.home.click_away_state(locator)
                self.coily_methods.verify_away_message(status=msg, user_credentials=credentials)

                time.sleep(3)

                # Verify Coily and peripherals are disconnected from LogiTune
                self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

                # Verify Coily status in Sync Portal
                self._verify_desk_status_in_sync_portal(IN_USE_AWAY)

                # Connect Coily to laptop
                self._connect_coily()

                # Verify check in notifications
                 

                # Verify Agenda event on Coily
                self._verify_agenda_event(event_details)

                # Verify Coily and peripherals are detected in LogiTune
                self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

                # Verify Coily status in Sync Portal
                self._verify_desk_status_in_sync_portal(IN_USE)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
            self.delete_all_calendar_event_for_the_user(account_type, credentials)

    def tc_booked_session_and_user_logged_in_coily_reconnection(self, account_type, credentials):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Create Calendar event for the user
            event_details = {
                'account_type': account_type,
                'credentials': credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            # Create Calendar event
            meeting_title = self._create_calendar_event(event_details)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=credentials)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(credentials,
                                                                           reservation_duration=random.randint(1, 6))

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
            self.verify_booked_session_check_in_notifications(credentials)

            # Verify Agenda events on Coily
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            Report.logInfo("Disconnect Coily for less than 60sec and quickly reconnect")

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            time.sleep(5)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify if Coily is checked in notification


            self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                         time_format=self.sync_portal_services.desk_settings_time_format)
            self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
            self.coily_methods.verify_the_notification_nice_to_see_you_message(credentials=credentials)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify Agenda events on Coily
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            Report.logInfo("Disconnect Coily for more than 60sec and reconnect")

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            time.sleep(60)

            # Verify Away status on Coily
            self.coily_methods.verify_away_message(status=MSG_BE_BACK_SOON, user_credentials=credentials)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
             

            # Verify Agenda events on Coily
            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_booked_session_and_wrong_user_logged_in(self, work_account_type_wrong_user, credentials_wrong_user,
                                                   reservation_user_credentials):
        try:
            if work_account_type_wrong_user == GOOGLE:
                self.sync_portal_services.change_walk_in_session_value(None)
            elif work_account_type_wrong_user == MICROSOFT:
                self.sync_portal_services.change_walk_in_session_value(1)

            # Log in wrong user to Logi Tune work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type_wrong_user,
                                                                account_credentials=credentials_wrong_user)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            reservation_time_duration = random.randint(1, 6)
            self.reservation = self._create_and_verify_session_in_progress(reservation_user_credentials,
                                                                           reservation_duration=reservation_time_duration)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification

            self.coily_methods.verify_checking_you_in_message_window()

            # Verify 'The desk is already reserved'
            self.coily_methods.verify_the_desk_is_already_reserved()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Delete active reservation
            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
            self.reservation = None
            time.sleep(3)
            Report.logInfo('Get Coily screen', screenshot=True, is_collabos=True)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Connect Coily to laptop
            self._connect_coily()

            if work_account_type_wrong_user == GOOGLE:
                Report.logInfo("Verify if reservation is needed window is displayed")

                # Verify 'You need a reservation' notification
                self.coily_methods.verify_coily_reservation_is_needed()

                # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
                self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

                # Disconnect Coily from laptop
                self._disconnect_coily()

            elif work_account_type_wrong_user == MICROSOFT:
                Report.logInfo("Verify if user walk-in session will be created.")

                # Get estimated start time for walk in session
                start_time = get_curent_time()
                Report.logInfo(f'Reservation start time: {start_time}')

                # Verify if Coily is checked in notification
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                    reservation_start_time=start_time,
                    time_offset=1,
                    time_format=self.sync_portal_services.desk_settings_time_format)
                self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
                self.coily_methods.verify_the_notification_nice_to_see_you_message(
                    credentials=credentials_wrong_user)

                # Verify Coily authenticated page
                self._verify_coily_authenticated_page()

                # Verify Coily and peripherals are detected in LogiTune
                self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

                # Disconnect Coily from laptop
                self._disconnect_coily()

                # Press Release the desk button
                self.coily_methods.release_the_desk()

                # Verify Session is over message
                self.coily_methods.verify_session_is_over_message()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_booked_session_correct_user_logged_in_after_previously_wrong_person_logged_in(self,
                                                                                         work_account_type_wrong_user,
                                                                                         work_account_type_correct_user,
                                                                                         credentials_wrong_user,
                                                                                         credentials_correct_user,
                                                                                         reservation_user_credentials):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type_wrong_user,
                                                                account_credentials=credentials_wrong_user)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(reservation_user_credentials,
                                                                           reservation_duration=random.randint(1, 6))

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notification

            self.coily_methods.verify_checking_you_in_message_window()

            # Verify "This desk is already reserved" error message
            self.coily_methods.verify_the_desk_is_already_reserved()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect user from LogiTune Work Account
            self.tune_methods.tc_disconnect_connected_account()

            time.sleep(5)

            # Log in to Work Account as a wrong user
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type_correct_user,
                                                                account_credentials=credentials_correct_user)

            # Verify check in notifications
            self.verify_booked_session_check_in_notifications(credentials_correct_user)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
             

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            Report.logInfo("Disconnect Coily for more than 60sec and reconnect")

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily Idle page
            self._verify_coily_idle_page()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_walk_in_session_disabled_book_button_check(self, account_type: None):
        try:
            # Disable walk-in session
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Open Logi Tune and connect to Work account
            work_account_credentials = prepare_work_account_credentials(account_type)
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()

            self.coily_methods.check_make_reservation_page()

            self._disconnect_coily()
            self._verify_coily_idle_page()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_walk_in_session_different_desk_booked(self, account_type: None):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(1)

            scenario_methods = WorkAccountScenarios(global_variables.driver)

            # Open Logi Tune and connect to Work account
            work_account_credentials = prepare_work_account_credentials(account_type)

            user_id = work_account_credentials.get('signin_payload').get('identifier')
            sibling_desks = scenario_methods.group_desk_list
            sibling_desks_filtered = [desk for desk in sibling_desks if desk.get('name') != scenario_methods.desk_name]
            random_desk = random.choice(sibling_desks_filtered)
            random_desk_name = random_desk.get('name')

            Report.logInfo("Creating booking for sibling desk")
            booking_start_time = datetime.now()
            booking_duration = 60
            time_format = self.sync_portal_services.desk_settings_time_format
            booking_resp = scenario_methods.sync_api_methods.create_booking_for_user(scenario_methods.org_id,
                                                                                     random_desk.get('id'),
                                                                                     user_id,
                                                                                     booking_start_time,
                                                                                     booking_duration)
            if not booking_resp.ok:
                Report.logException("Booking desk failed")

            else:
                Report.logInfo(f"Booking desk for: {random_desk_name} success")

            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Connect Coily to laptop
            self._connect_coily()
            time.sleep(5)
            self.coily_methods.check_already_have_a_session_page(random_desk_name)
            self.coily_methods.check_already_have_session_cancel_button_clicked()

            self._disconnect_coily()
            time.sleep(10)
            self._verify_coily_idle_page()
            self._connect_coily()
            self.coily_methods.check_already_have_a_session_page(random_desk_name)
            self.coily_methods.check_already_have_session_agree_button_clicked(booking_start_time, booking_duration,
                                                                               time_format, scenario_methods.desk_name)

            self.coily_methods.verify_coily_authenticated_page(org_name=scenario_methods.org_name,
                                                               group_name=scenario_methods.area,
                                                               desk_name=scenario_methods.desk_name,
                                                               time_format=time_format)
            self._disconnect_coily()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_booked_session_reconnect_to_laptop_with_correct_work_account_connected(self, work_account_type_wrong_user,
                                                                                  work_account_type_correct_user,
                                                                                  credentials_wrong_user,
                                                                                  credentials_correct_user,
                                                                                  reservation_user_credentials):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Open Logi Tune and connect to Work account with a wrong user
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type_wrong_user,
                                                                account_credentials=credentials_wrong_user)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(reservation_user_credentials,
                                                                           reservation_duration=random.randint(1, 6))

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing you in notification

            self.coily_methods.verify_checking_you_in_message_window()

            # Verify "This desk is already reserved" error message
            self.coily_methods.verify_the_desk_is_already_reserved()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()
            time.sleep(5)

            # Verify "Session in progress" is displayed
            result = self.coily_methods.verify_session_in_progress_page(reservation_user_credentials)
            assert result is True, "Session in progress not displayed correctly"

            # Disconnect user from LogiTune Work account
            self.tune_methods.tc_disconnect_connected_account()

            # Connect to work account with a correct user
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type_correct_user,
                                                                account_credentials=credentials_correct_user)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(5)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily Idle page
            self._verify_coily_idle_page()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_wrong_user_checks_in_before_some_booked_session(self, correct_user, wrong_user_account_type, wrong_user,
                                                           reservation_delay):
        try:
            # Set walk-in session duration in Sync Portal
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(8)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a future reservation and check if it is displayed on Coily
            self.reservation = self._create_and_verify_future_reservation_in_displayed(credentials=correct_user,
                                                                                       reservation_delay=reservation_delay,
                                                                                       reservation_time_duration=reservation_time_duration)

            if wrong_user != 'anonymous':
                self.tune_methods.connect_to_work_or_agenda_account(account_type=wrong_user_account_type,
                                                                    account_credentials=wrong_user)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify 'Checking you in...' notification


            self.coily_methods.verify_coily_checking_in_notification()

            self.coily_methods.verify_coily_is_checked_in_booked_session_notification(self.reservation[1],
                                                                         time_format=self.sync_portal_services.desk_settings_time_format)

            if reservation_delay <= 30:
                self.coily_methods.verify_time_left_to_beginning_of_reservation(self.reservation[1])
                self.coily_methods.verify_center_pile_message(self.reservation[1], time_format=self.sync_portal_services.desk_settings_time_format)
            elif 30 < reservation_delay <= 60:
                self.coily_methods.verify_time_left_to_beginning_of_reservation(self.reservation[1])
                self.coily_methods.verify_center_pile_message(self.reservation[1], time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                self.coily_methods.verify_there_is_no_center_pile_with_time_left_for_the_reservation()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            if wrong_user != 'anonymous':
                self.coily_methods.release_the_desk()
                self.coily_methods.verify_session_is_over_message()

            time.sleep(2)

            if reservation_delay <= 30:
                self.coily_methods.verify_booked_in_x_minutes_for_user_page(correct_user, self.reservation[1])
            else:
                self.coily_methods.verify_booked_in_x_minutes_center_notification(self.reservation[1])

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_wrong_user_checks_in_before_some_booked_session_end_waits_till_the_end(self, correct_user_account_type,
                                                                                  correct_user, wrong_user_account_type,
                                                                                  wrong_user, reservation_delay):
        try:
            # Set walk-in session duration in Sync Portal
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(8)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a future reservation and verify it on Coily
            self.reservation = self._create_and_verify_future_reservation_in_displayed(credentials=correct_user,
                                                                                       reservation_delay=reservation_delay,
                                                                                       reservation_time_duration=reservation_time_duration)

            if wrong_user != 'anonymous':
                self.tune_methods.connect_to_work_or_agenda_account(account_type=wrong_user_account_type,
                                                                    account_credentials=wrong_user)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify 'Checking you in...' notification

            self.coily_methods.verify_coily_checking_in_notification()

            self.coily_methods.verify_coily_is_checked_in_booked_session_notification(self.reservation[1],
                                                                         time_format=self.sync_portal_services.desk_settings_time_format)

            self.coily_methods.verify_time_left_to_beginning_of_reservation(self.reservation[1])
            self.coily_methods.verify_center_pile_message(self.reservation[1], time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Verify "This desk will be release" notification
            self.coily_methods.verify_desk_will_be_released()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            if not self.tune_methods.verify_sign_in_button_is_displayed():
                self.tune_methods.tc_disconnect_connected_account()

            self.tune_methods.connect_to_work_or_agenda_account(account_type=correct_user_account_type,
                                                                account_credentials=correct_user)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()
             

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Click "Release the desk" button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_user_checks_in_before_some_booked_session(self, user_account_type, user_credentials, reservation_delay):
        try:
            # Set walk-in session duration in Logi Tune
            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(8)

            # Create Calendar event for the user
            event_details = {
                'account_type': user_account_type,
                'credentials': user_credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=90),
                'meeting_duration_min': 30,
                'event_title': "Coily test:"
            }

            meeting_title = self._create_calendar_event(event_details)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            self.reservation = self._create_and_verify_future_reservation_in_displayed(credentials=user_credentials,
                                                                                       reservation_delay=reservation_delay,
                                                                                       reservation_time_duration=reservation_time_duration)

            self.tune_methods.connect_to_work_or_agenda_account(account_type=user_account_type,
                                                                account_credentials=user_credentials)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify 'Checking you in...' notification


            self.coily_methods.verify_coily_checking_in_notification()
            self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                         time_format=self.sync_portal_services.desk_settings_time_format)
            self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
            self.coily_methods.verify_the_notification_nice_to_see_you_message(credentials=user_credentials)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")

            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Choose and verify Away state on Coily
            self.coily_methods.home.click_away_state(TuneCoilyLaptopDisconnectedLocators.BE_BACK_SOON)
            self.coily_methods.verify_away_message(status=MSG_BE_BACK_SOON, user_credentials=user_credentials)

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
             

            self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Click "Release teh desk" button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
            self.delete_all_calendar_event_for_the_user(user_account_type, user_credentials)

    def tc_user_checks_in_before_some_booked_session_when_walk_in_disabled(self, user_account_type, user_credentials,
                                                                           reservation_delay):
        try:
            # Disable walk-in session
            self.sync_portal_services.change_walk_in_session_value(None)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a future reservation anc verify it on Coily
            reservation_time_duration = random.randint(1, 6)
            self.reservation = self._create_and_verify_future_reservation_in_displayed(credentials=user_credentials,
                                                                                       reservation_delay=reservation_delay,
                                                                                       reservation_time_duration=reservation_time_duration)

            # Log in to Work account in Logi Tune
            self.tune_methods.connect_to_work_or_agenda_account(account_type=user_account_type,
                                                                account_credentials=user_credentials)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Choose and verify Away state on Coily
            self.coily_methods.home.click_away_state(TuneCoilyLaptopDisconnectedLocators.BE_BACK_SOON)
            self.coily_methods.verify_away_message(status=MSG_BE_BACK_SOON, user_credentials=user_credentials)

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            time.sleep(1)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify check in notifications
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()


            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Click "Release the desk" button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Connect Coily to laptop
            self._connect_coily()

            # Verify reservation is needed error

            self.coily_methods.verify_coily_reservation_is_needed()

            # Verify Coily and peripherals is detected in LogiTune for NOT authorized user
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_booked_session_walk_in_disabled_tune_install_user_log_in(self, work_account_type, credentials):
        try:

            # Uninstall Logi Tune
            Report.logInfo(f"Uninstall existing LogiTune.")
            if get_custom_platform() == "windows":
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
                app = TunesUIInstallWindows()
                if app.check_for_app_installed_win(TUNEAPP_NAME):
                    app.uninstall_app()
                os.system(str(UIBase.rootPath) + WIN_APP_CLOSE_BAT_PATH)
            else:
                app = TunesUIInstallMacOS()
                if app.check_tune_installed_macos():
                    app.uninstallApp()
            time.sleep(5)

            # Set walk-in session parameter in Sync Portal
            if work_account_type == GOOGLE:
                self.sync_portal_services.change_walk_in_session_value(1)
            elif work_account_type == MICROSOFT:
                self.sync_portal_services.change_walk_in_session_value(None)

            # Start appium_service
            check_and_connect_device(COILY_DESK_IP)
            time.sleep(2)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Create a reservation for the desk and check if it is displayed on Coily
            self.reservation = self._create_and_verify_session_in_progress(credentials)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification
            self.coily_methods.verify_checking_you_in_message_window()

            # Verify 'Taking so long' notification
            self.coily_methods.verify_coily_checking_in_taking_so_long_notification()
            self.coily_methods.verify_check_in_via_mobile_app_button_is_displayed()

            # Verify 'You can’t use this desk at the moment'
            self.coily_methods.verify_you_cant_use_this_at_this_moment()
            self.coily_methods.verify_personal_info_on_you_cant_you_desk_window(credentials)
            self.coily_methods.verify_check_in_via_mobile_app_button_is_displayed()

            # Install Logi Tune and start appium service
            if get_custom_platform() == "windows":
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)

            self.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)

            self.tune_methods.tune_app.open_tune_app()
            time.sleep(5)

            # Log in to Work Account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=work_account_type,
                                                                account_credentials=credentials)

            # Start appium service
            time.sleep(2)

            self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                         time_format=self.sync_portal_services.desk_settings_time_format)
            self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
            self.coily_methods.verify_the_notification_nice_to_see_you_message(credentials=credentials)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()
            self.reservation = None

            # Verify "Session is over" message
            time.sleep(1)
            self.coily_methods.verify_session_is_over_message()

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])

    def tc_quit_and_relaunch_tune_during_active_session(self, session_type, account_type, credentials):
        try:

            if session_type == 'walk-in':
                # Set walk-in session duration param
                reservation_time_duration = random.randint(1, 6)
                self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            if account_type != 'anonymous':
                event_details = {
                    'account_type': account_type,
                    'credentials': credentials,
                    'meeting_start_time': datetime.now() + timedelta(minutes=30),
                    'meeting_duration_min': 60,
                    'event_title': "Coily test:"
                }

                meeting_title = self._create_calendar_event(event_details)

                # Open Logi Tune and connect to Work account
                self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                    account_credentials=credentials)

            if session_type == 'walk-in':
                # Get the estimated start time for walk in session
                start_time = get_curent_time()
                Report.logInfo(f'Reservation start time: {start_time}')
            else:
                # Create a reservation for the desk and check if it is displayed on Coily
                self.reservation = self._create_and_verify_session_in_progress(credentials,
                                                                               reservation_duration=random.randint(1, 6))

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification

            if session_type == 'walk-in':
                self.coily_methods.verify_coily_checking_in_notification()
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                self.coily_methods.verify_checking_you_in_message_window()
                self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                             time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            if account_type != 'anonymous':
                self.tune_app.click_home()
                self.tune_app.click_refresh_calendar_button()

                meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
                if meeting_title_visible:
                    Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
                else:
                    Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")
                self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(IN_USE)

            # Quit Logi Tune
            self.tune_app.click_tune_menu()
            time.sleep(0.5)
            self.tune_app.click_quit_menu()
            self.tune_app.verify_tune_processes_are_active()

            if session_type == 'walk-in':
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                # Verify if Coily is checked in notification
                self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                             time_format=self.sync_portal_services.desk_settings_time_format)

            if account_type != 'anonymous':
                assert self.coily_methods.is_any_agenda_item_displayed() is False, Report.logFail(f"Agenda is still displayed on Coily after Quitting Tune.")

            # Open Tune again
            self.tune_app.open_tune_app()

            if session_type == 'walk-in':
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                # Verify if Coily is checked in notification
                self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                             time_format=self.sync_portal_services.desk_settings_time_format)
            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            if account_type != 'anonymous':
                self._verify_agenda_event(event_details)

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Disconnect Coily from laptop
            self._disconnect_coily()

            if account_type != 'anonymous':
                # Press Release the desk button
                self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
            self.delete_all_calendar_event_for_the_user(account_type, credentials)

    def tc_add_and_remove_events_during_identified_session(self, session_type, account_type, credentials):
        try:
            # Clean all calendar events for the user
            self.delete_all_calendar_event_for_the_user(account_type, credentials)

            if session_type == 'walk-in':
                # Set walk-in session duration param
                reservation_time_duration = random.randint(1, 6)
                self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Verify Coily Idle page
            self._verify_coily_idle_page()

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=credentials)

            if session_type == 'walk-in':
                # Get the estimated start time for walk in session
                start_time = get_curent_time()
                Report.logInfo(f'Reservation start time: {start_time}')
            else:
                # Create a reservation for the desk and check if it is displayed on Coily
                self.reservation = self._create_and_verify_session_in_progress(credentials,
                                                                           reservation_duration=random.randint(1, 6))

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification



            if session_type == 'walk-in':
                self.coily_methods.verify_coily_checking_in_notification()
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                self.coily_methods.verify_checking_you_in_message_window()
                self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                             time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Create first calendar event for user
            event_details_1 = {
                'account_type': account_type,
                'credentials': credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            meeting_title = self._create_calendar_event(event_details_1, delete_all_other_meetings=True)

            time.sleep(10)
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()
            meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=meeting_title)
            if meeting_title_visible:
                Report.logInfo(f"Created meeting: {meeting_title} is visible in Logi Tune", screenshot=True)
            else:
                Report.logException(f"Created meeting: {meeting_title} not visible in Logi Tune")

            self._verify_agenda_event(event_details_1)

            # Create second calendar event for user
            event_details_2 = {
                'account_type': account_type,
                'credentials': credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=90),
                'meeting_duration_min': 90,
                'event_title': "Coily test:"
            }

            second_meeting_title = self._create_calendar_event(event_details_2, delete_all_other_meetings=False)
            self.tune_app.click_refresh_calendar_button()
            second_meeting_title_visible = self.tune_app.verify_meeting_title(meeting_title=second_meeting_title)

            if second_meeting_title_visible:
                Report.logInfo(f"Created meeting: {second_meeting_title} is visible in Logi Tune")
            else:
                Report.logException(f"Created meeting: {second_meeting_title} not visible in Logi Tune")

            time.sleep(10)

            self.coily_methods.extend_agenda_view()
            self._verify_agenda_event(event_details_2)
            self.coily_methods.close_agenda_view()

            # Verify Coily and peripherals are detected in LogiTune
            self.verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(IN_USE)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Choose and validate Away state
            self.coily_methods.home.click_away_state(TuneCoilyLaptopDisconnectedLocators.OUT_FOR_LUNCH)
            self.coily_methods.verify_away_message(status=MSG_OUT_FOR_LUNCH, user_credentials=credentials)

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(IN_USE_AWAY)

            # Connect Coily to laptop
            self._connect_coily()

            # Verify Check-ing-you in notification



            if session_type == 'walk-in':
                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                              time_offset=reservation_time_duration,
                                                                              time_format=self.sync_portal_services.desk_settings_time_format)
            else:
                self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                             time_format=self.sync_portal_services.desk_settings_time_format)

            # Verify Coily authenticated page
            self._verify_coily_authenticated_page()

            # Verify both events are displayed
            self.coily_methods.extend_agenda_view()
            self._verify_agenda_event(event_details_1)
            self._verify_agenda_event(event_details_2)
            self.coily_methods.close_agenda_view()

            # Delete all events
            self.delete_all_calendar_event_for_the_user(account_type, credentials)

            time.sleep(10)

            # Verify events are not displayed
            assert self.coily_methods.is_any_agenda_item_displayed() is False, (
                Report.logFail(f"Agenda is still displayed on Coily after Deleting them."))

            # Disconnect Coily from laptop
            self._disconnect_coily()

            # Press Release the desk button
            self.coily_methods.release_the_desk()

            # Verify Session is over message
            self.coily_methods.verify_session_is_over_message()

            time.sleep(3)

            # Verify Coily and peripherals are disconnected from LogiTune
            self.verify_coily_and_peripherals_are_disconnected_from_logi_tune()

            # Verify Coily status in Sync Portal
            self._verify_desk_status_in_sync_portal(AVAILABLE)
        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            if self.reservation:
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
            self.delete_all_calendar_event_for_the_user(account_type, credentials)

    def _disconnect_coily(self):
        disconnect_device_no_sleeps(device_name=self.device_name)

    def _connect_coily(self):
        connect_device_no_sleeps(device_name=self.device_name)

    def _verify_coily_idle_page(self):
        """
        Verify all elements on the Coily while it's in no session mode
        """
        self.coily_methods.open_app(force=True)
        self.coily_methods.verify_coily_idle_page(self.sync_portal_services.org_name, self.sync_portal_services.group_name,
                                     self.sync_portal_services.desk_name, time_format=self.sync_portal_services.desk_settings_time_format)

    def _verify_coily_authenticated_page(self):
        """
        Verify all elements on the Coily while it's authenticated
        """
        self.coily_methods.verify_coily_authenticated_page(self.sync_portal_services.org_name, self.sync_portal_services.group_name,
                                              self.sync_portal_services.desk_name, time_format=self.sync_portal_services.desk_settings_time_format)

    def _create_and_verify_session_in_progress(self, credentials, reservation_duration=1, verify_reservation=True):
        """
        Create reservation for the desk and verify it is displayed on Coily
        """
        self.reservation = self.sync_portal_services.make_a_reservation(credentials, reservation_duration)
        time.sleep(5)
        if verify_reservation:
            result = self.coily_methods.verify_session_in_progress_page(credentials)
            if not result:
                Report.logWarning(f"Problem with displaying 'Session in progress' page! -> Try again.")
                time.sleep(1)
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
                time.sleep(3)
                self.sync_portal_services.delete_active_reservations_for_desk()
                time.sleep(3)
                self.reservation = self.sync_portal_services.make_a_reservation(credentials, reservation_duration)
                time.sleep(5)

                result = self.coily_methods.verify_session_in_progress_page(credentials)
            time.sleep(5)
            assert result is True, "Session in progress page not displayed correctly"
        return self.reservation

    def _create_a_session_with_desk_id(self, credentials, desk_id: str, reservation_duration: int = 1):
        """
        Create reservation for the desk and verify it is displayed on Coily
        """
        self.reservation = self.sync_portal_services.make_a_reservation(credentials, reservation_duration, desk_id=desk_id)
        time.sleep(5)
        return self.reservation

    def _create_and_verify_future_reservation_in_displayed(self, credentials, reservation_delay,
                                                           reservation_time_duration, verify_reservation=True):
        """
        Create future reservation for the desk and verify it is displayed on Coily
        """
        self.reservation = self.sync_portal_services.make_a_future_reservation(user_credentials=credentials,
                                                                               delay_in_x_minutes=reservation_delay,
                                                                               reservation_duration=reservation_time_duration)
        time.sleep(5)
        if verify_reservation:
            if reservation_delay <= 30:
                result = self.coily_methods.verify_booked_in_x_minutes_for_user_page(credentials, self.reservation[1])
            else:
                result = self.coily_methods.verify_booked_in_x_minutes_center_notification(self.reservation[1])

            if not result:
                Report.logWarning(f"Problem with displaying future reservation on the Coily! -> Try again.")
                time.sleep(1)
                self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=self.reservation[0])
                time.sleep(3)
                self.sync_portal_services.delete_active_reservations_for_desk()
                time.sleep(3)
                self.reservation = self.sync_portal_services.make_a_future_reservation(user_credentials=credentials,
                                                                                       delay_in_x_minutes=reservation_delay,
                                                                                       reservation_duration=reservation_time_duration)
                time.sleep(5)

                if reservation_delay <= 30:
                    result = self.coily_methods.verify_booked_in_x_minutes_for_user_page(credentials,
                                                                                         self.reservation[1])
                else:
                    result = self.coily_methods.verify_booked_in_x_minutes_center_notification(self.reservation[1])
            time.sleep(5)
            assert result is True, "Future reservation page not displayed correctly"
        return self.reservation

    def _verify_desk_status_in_sync_portal(self, desk_status):
        """
        Verify desk status in Sync Portal
        """
        status = self.sync_portal_services.get_desk_scheduler_status()
        Report.logInfo(f'Desk status in Sync Portal is: {status}')
        if status in SYNC_PORTAL_STATUSES[desk_status]:
            Report.logPass(
                f"Sync Portal status {status} is matching values for {desk_status}: {SYNC_PORTAL_STATUSES[desk_status]}")
        else:
            Report.logFail(
                f"Sync Portal status {status} NOT matching values for {desk_status}: {SYNC_PORTAL_STATUSES[desk_status]}")

    def clean_tune_connected_account(self):
        """
        Disconnect user from Work account if any connected
        """
        self.tune_app.connect_tune_app()
        if not self.tune_methods.verify_sign_in_button_is_displayed():
            self.tune_methods.tc_disconnect_connected_account()

    def check_if_connected_to_account(self):

        self.tune_app.connect_tune_app()
        return not self.tune_methods.verify_sign_in_button_is_displayed()

    def check_if_coily_connected_in_tune(self):

        return self.tune_app.check_is_device_connected(self.device_name)

    def check_if_coily_tune_settings_present(self):
        if self.check_if_connected_to_account() and self.check_if_coily_connected_in_tune():
            self.logi_tune_coily_settings_page.open_coily_settings()
            in_settings: bool = self.logi_tune_coily_settings_page.check_if_in_coily_settings()
            return in_settings

    def set_tune_values_with_sync_portal_values(self):
        Report.logInfo("Syncing Tune Coily Settings with Sync Portal settings")
        sync_portal_settings = self.get_current_sync_portal_coily_settings()
        self.logi_tune_coily_settings_page.set_initial_values(sync_portal_settings)

    def set_tune_with_sync(self):
        try:
            if self.check_if_coily_tune_settings_present():
                self.coily_settings_page.open_coily_settings_from_authenticated_page()
                self.set_tune_values_with_sync_portal_values()
                self.coily_settings_page.close_settings_page()
        except Exception as e:
            Report.logWarning(f"Could not set Tune Coily settings with sync portal {e}")

    def verify_anonymous_user_check_in_notifications(self, reservation_time_duration, start_time):
        """
        Verify the notification for check in flow for anonymous user
        """
        self.coily_methods.verify_coily_checking_in_notification()
        self.coily_methods.verify_the_notification_action_button_is_displayed(notification_button_text=LEARN_MORE)
        self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                      time_offset=reservation_time_duration,
                                                                      time_format=self.sync_portal_services.desk_settings_time_format)
        self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
        self.coily_methods.verify_the_notification_welcome_message()
        self.coily_methods.verify_the_notification_action_button_is_displayed(notification_button_text=LEARN_MORE)
        self._verify_coily_authenticated_page()

    def verify_identified_user_check_in_notifications(self, reservation_time_duration, start_time,
                                                      work_account_credentials):
        """
        Verify the notification for check in flow for walk-in session for identified user
        """
        self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(reservation_start_time=start_time,
                                                                      time_offset=reservation_time_duration,
                                                                      time_format=self.sync_portal_services.desk_settings_time_format)
        self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
        self.coily_methods.verify_the_notification_nice_to_see_you_message(credentials=work_account_credentials)
        self._verify_coily_authenticated_page()

    def verify_booked_session_check_in_notifications(self, user_credentials):
        """
        Verify the notification for check in flow for booked session for identified user
        """
        self.coily_methods.verify_checking_you_in_message_window()
        self.coily_methods.verify_coily_is_checked_in_booked_session_notification(stop_time=self.reservation[2],
                                                                     time_format=self.sync_portal_services.desk_settings_time_format)
        self.coily_methods.click_the_notification_action_button(notification_button_text=GOT_IT)
        self.coily_methods.verify_the_notification_nice_to_see_you_message(credentials=user_credentials)
        self._verify_coily_authenticated_page()

    def verify_coily_and_peripherals_are_detected_in_logi_tune_for_identified_user(self):
        """
        Verify if Coily and all peripherals are detected in Logi tune
        """
        self.tune_app.open_my_devices_tab()
        self.tune_app.verify_coily_is_detected(device_name=self.device_name)
        self.tune_app.verify_coily_peripherals_are_detected(connected_devices=self.coily_peripherals)

    def verify_coily_and_peripherals_are_detected_in_logi_tune_for_unauthorized_user(self):
        """
        Verify if Coily and all peripherals are not detected in Logi tune for NOT authorized user
        """
        self.tune_app.open_my_devices_tab()
        self.tune_app.verify_coily_is_detected(device_name=self.device_name)
        self.tune_app.check_peripherals_for_unauthorized_user(connected_devices=self.coily_peripherals)

    def verify_coily_and_peripherals_are_disconnected_from_logi_tune(self):
        """
        Verify if Coily and all peripherals are not detected in Logi tune
        """
        self.tune_app.open_my_devices_tab()
        self.tune_app.verify_coily_is_disconnected(device_name=self.device_name)
        self.tune_app.verify_coily_peripherals_are_disconnected(connected_devices=self.coily_peripherals)

    def _create_calendar_event(self, event_details, delete_all_other_meetings=False):
        """
        Create a Calendar event for user
        """
        self.calendar_methods = CalendarMethods(account_type=event_details['account_type'], tests_type='coily',
                                                credentials=event_details['credentials'])

        if delete_all_other_meetings:
            self.calendar_methods.delete_remaining_events()

        meeting_title = f"{event_details['event_title']}: {event_details['meeting_start_time']}"

        self.event_id = self.calendar_methods.create_event_for_coily_agenda_verification(
            meeting_title=meeting_title,
            start_time=event_details['meeting_start_time'],
            meeting_duration_min=event_details['meeting_duration_min'])

        Report.logInfo(f'Meeting event created with id: {self.event_id}')
        return meeting_title

    def _create_all_day_calendar_event(self, event_details, delete_all_other_meetings=False):
        """
        Create a Calendar event for user
        """
        self.calendar_methods = CalendarMethods(account_type=event_details['account_type'], tests_type='coily',
                                                credentials=event_details['credentials'])

        if delete_all_other_meetings:
            self.calendar_methods.delete_remaining_events()

        meeting_title = f"{event_details['summary']}: {event_details['start_time']}"

        self.event_id = self.calendar_methods.create_all_day_event_for_coily_agenda_verification(
            meeting_title=meeting_title,
            start_time=event_details['start_time'],
            meeting_duration_days=event_details['duration'],
            guests_email_list=event_details['guests_email_list'],
            location=event_details['location'],
            description=event_details['description'])

        Report.logInfo(f'Meeting event created with id: {self.event_id}')
        return meeting_title

    @staticmethod
    def check_existing_events_in_calendar(account_type: str,
                                          credentials: dict) -> list:

        calendar_methods = CalendarMethods(account_type=account_type, tests_type='coily',
                                           credentials=credentials)

        events = calendar_methods.calendar_api.get_events()

        Report.logInfo(f"Current number of events in calendar: {len(events)}")
        return events if account_type == MICROSOFT else events.get('items')

    def _verify_agenda_event(self, event_details):
        self.coily_methods.verify_agenda_item(event_title=f"{event_details['event_title']}: {event_details['meeting_start_time']}",
                                              start_time=event_details['meeting_start_time'],
                                              duration_min=event_details['meeting_duration_min'],
                                              attendees=1,
                                              time_format=self.sync_portal_services.desk_settings_time_format)


    def delete_all_calendar_event_for_the_user(self, account_type, credentials):
        self.calendar_methods = CalendarMethods(account_type=account_type, tests_type='coily', credentials=credentials)

        self.calendar_methods.delete_remaining_events()

    def _sync_coily_settings_from_sync_portal_to_logi_tune(self):
        self._connect_coily()
        self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()

        current_sync_settings = self.get_current_sync_portal_coily_settings()

        self.logi_tune_coily_settings_page.toggle_time_format()
        self.logi_tune_coily_settings_page.set_time_format(current_sync_settings['time_format'])
        self.logi_tune_coily_settings_page.toggle_privacy_mode()
        self.logi_tune_coily_settings_page.set_privacy_mode(current_sync_settings['privacy_mode_enabled'])
        self.logi_tune_coily_settings_page.set_away_message_and_submit("Out for lunch")
        self._disconnect_coily()
        self.coily_methods.release_the_desk()

    def _enter_walkin_session_with_check(self,
                                         account_type: Union[str, None] = None,
                                         anonymous: bool = False) -> Tuple[datetime, int, str]:
        reservation_time_duration = random.randint(1, 6)
        self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

        if not anonymous:
            work_account_credentials = prepare_work_account_credentials(account_type)
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            self._sync_coily_settings_from_sync_portal_to_logi_tune()
        # Connect Coily to Laptop
        self._connect_coily()
        start_time = get_curent_time()
        current_time_format = self.get_current_sync_portal_coily_settings('time_format')

        # Check if walk-in session is visible
        walk_in = self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification_without_time()

        self._verify_desk_status_in_sync_portal(IN_USE)

        return start_time, reservation_time_duration, current_time_format

    def tc_settings_anonymous_session_check_with_sync_portal(self):

        try:

            reservation_time_duration = random.randint(1, 6)
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # generate available values for sync portal coily settings
            available_values = {
                "agenda_enabled": (False, True),
                "privacy_mode_enabled": (False, True),
                "time_format": ("12", "24"),
                "screen_brightness": (0, random.randint(100, 150), 255)
            }

            # Get all combinations to cover available values
            available_choices = get_all_values_to_cover_from_dict_of_lists(available_values)

            for choice in available_choices:
                # use settings combination to set in sync portal
                if not choice['agenda_enabled']:
                    choice['privacy_mode_enabled'] = False
                Report.logInfo(f"Setting SyncPortal Coily Settings to: {choice}")
                self.sync_portal_services.set_coily_settings(**choice)
                time.sleep(10)
                self._connect_coily()

                # get current Sync Portal Settings
                current_settings = self.get_current_sync_portal_coily_settings()

                # Connect Coily to Laptop and enter Walk-in Session
                self._enter_walkin_session_with_check(anonymous=True)

                # Check current settings visible on Coily Settings Page
                current_settings_on_coily = self.coily_settings_page.get_current_settings_dict()

                # Compare Settings on Coily with Settings set on Sync Portal
                self.coily_methods.compare_sync_portal_and_coily_settings(current_settings, current_settings_on_coily)

                # Check if Coily Main Page current time format matches Sync Portal Settings
                self.coily_methods.check_if_correct_format_displayed_on_coily(current_settings['time_format'])

                self._disconnect_coily()
                time.sleep(10)

        except Exception as e:
            Report.logInfo(str(e), screenshot=True)
            Report.logException(str(e), is_collabos=True)

    def tc_identified_session_change_time_format_on_coily_settings_page(self,
                                                                        account_type: Union[GOOGLE, MICROSOFT]):

        try:

            self._enter_walkin_session_with_check(account_type=account_type)

            # Check time format and toggle to opposite
            current_coily_time_format = self.coily_settings_page.get_current_time_format()

            Report.logInfo(f"Current Time format on coily: {current_coily_time_format}")

            if current_coily_time_format == FORMAT_24H:
                expected_format = (FORMAT_AMPM, FORMAT_24H)
            else:
                expected_format = (FORMAT_24H, FORMAT_AMPM)

            Report.logInfo("Toggling Time Format")
            self.coily_settings_page.toggle_time_format()
            self.coily_methods.check_if_correct_format_displayed_on_coily(expected_format[0])

            Report.logInfo("Toggling Time Format")
            self.coily_settings_page.toggle_time_format()
            self.coily_methods.check_if_correct_format_displayed_on_coily(expected_format[1])

            self._disconnect_coily()
            self.coily_methods.release_the_desk()

            self.coily_methods.verify_coily_idle_page(self.sync_portal_services.org_name,
                                                      self.sync_portal_services.group_name,
                                                      self.sync_portal_services.desk_name,
                                                      time_format=self.
                                                      get_current_sync_portal_coily_settings('time_format'))
        except Exception as e:
            Report.logWarning(str(e), screenshot=True)
            Report.logException(str(e), is_collabos=True)

    def tc_settings_interaction_tune_desktop_coily_settings_with_coily_settings_page(self,
                                                                                     account_type:
                                                                                     Union[GOOGLE, MICROSOFT]):
        try:
            start_time, reservation_time_duration, current_time_format = self._enter_walkin_session_with_check(
                account_type=account_type)

            # Set init values before tests
            self.set_tune_with_sync()

            available_values = {
                "privacy_mode_enabled": (True, False),
                "time_format": (FORMAT_24H, FORMAT_AMPM),
                "screen_brightness": (1, random.randint(40, 60), 100)
            }

            values_to_cover = get_all_values_to_cover_from_dict_of_lists(available_values)

            for values_to_set in values_to_cover:

                Report.logInfo(f"Setting values on in Logi Tune Coily Settings to: {values_to_set}")

                # Setting values on Coily Logi Tune Settings Page
                settings_logi_tune = self.logi_tune_coily_settings_page.set_settings_values_from_dict(values_to_set)

                time.sleep(2)

                # Checking values on Coily Settings Page
                settings_on_coily = self.coily_settings_page.get_current_settings_dict()

                # Compare Settings in Logi Tune with Settings visible on Coily
                self.coily_methods.compare_tune_settings_with_coily_settings(settings_logi_tune,
                                                                             settings_on_coily)

            before_reconnect_settings_values = self.coily_settings_page.get_current_settings_dict()

            self._disconnect_coily()
            time.sleep(10)
            self._connect_coily()

            # Check session after coily reconnect
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time,
                time_offset=reservation_time_duration,
                time_format=before_reconnect_settings_values['time_format'])

            # Get Current Settings on Coily and check if they persisted
            Report.logInfo("Chekcing parameters on Coily after reconnect")
            after_reset_settings_values = self.coily_settings_page.get_current_settings_dict()

            if before_reconnect_settings_values == after_reset_settings_values:
                Report.logPass("Parameters after reconnect persisted")
            else:
                Report.logFail("Parameters after reconnect did not persist", is_collabos=True)

            # Check Tune Coily Settings before disconnect
            Report.logInfo("Checking Parameters before reconnect with release the desk")
            current_settings_coily_in_tune = self.logi_tune_coily_settings_page.get_current_settings_dict()
            # disconnect and release desk
            self._disconnect_coily()
            self.coily_methods.release_the_desk()

            time_format_sync = self.get_current_sync_portal_coily_settings('time_format')

            # Check time format after desk release
            self.coily_methods.verify_coily_idle_page(self.sync_portal_services.org_name,
                                                      self.sync_portal_services.group_name,
                                                      self.sync_portal_services.desk_name,
                                                      time_format=time_format_sync)

            time.sleep(10)

            # Reconnect and re-walk in
            self._connect_coily()
            start_time = get_curent_time()

            # Check if walk-in session is visible
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time,
                time_offset=reservation_time_duration,
                time_format=before_reconnect_settings_values['time_format'])

            after_re_walk_in_settings = self.coily_settings_page.get_current_settings_dict()
            if after_re_walk_in_settings == after_reset_settings_values:
                Report.logPass("Parameters after reconnect and re walk-in persisted")
            else:
                Report.logFail("Parameters after reconnect and re walk-in do not match", is_collabos=True)
        except Exception as e:
            Report.logInfo(str(e), screenshot=True, color='red')
            Report.logException(str(e), is_collabos=True)

    def tc_identified_session_change_away_message(self,
                                                  account_type: Union[GOOGLE, MICROSOFT]):
        try:
            start_time, reservation_time_duration, current_time_format = self._enter_walkin_session_with_check(
                account_type=account_type)

            # Verify if all elements in popup page are present (submit, close, input, etc)
            Report.logInfo("Checking if away message Pop-Up has necessary needed fields")
            self.logi_tune_coily_settings_page.verify_away_message_popup_page()

            # Set starting Away message
            self.logi_tune_coily_settings_page.set_away_message_and_submit(MSG_BE_BACK_SOON)

            Report.logInfo("Disconnecting Coily and checking if default away meessage is visible.")
            self._disconnect_coily()

            # Check if default message shows up
            self.coily_methods.click_and_verify_away_message(MSG_BE_BACK_SOON, account_type)
            self._connect_coily()

            Report.logInfo("Reconnecting Coily")

            # Verify if walking session is OK
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time,
                time_offset=reservation_time_duration,
                time_format=current_time_format)

            # Check if away message stays when no submiting
            self.logi_tune_coily_settings_page.set_away_message("New Away Message")

            self._disconnect_coily()

            self.coily_methods.click_and_verify_away_message(MSG_BE_BACK_SOON, account_type)
            self._connect_coily()

            # Verify Walk-in
            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time,
                time_offset=reservation_time_duration,
                time_format=current_time_format)

            # Check if away message changes after submitting new message
            new_away_message = "New Away Message"
            self.logi_tune_coily_settings_page.set_away_message_and_submit(new_away_message)
            self._disconnect_coily()

            self.coily_methods.click_and_verify_away_message(new_away_message, account_type)
            self._connect_coily()

            self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                reservation_start_time=start_time,
                time_offset=reservation_time_duration,
                time_format=current_time_format)

            # Check if empty away message input makes not submit button not clickable
            self.logi_tune_coily_settings_page.open_away_message_popup()
            self.logi_tune_coily_settings_page.away_message_input.clear_input_manually()

            # Check if invalid message popup is present
            self.logi_tune_coily_settings_page.check_invalid_away_message()

            # Check if message is truncated if too long

            random_msg = self.logi_tune_coily_settings_page.set_random_message_and_submit(260)
            self._disconnect_coily()

            self.coily_methods.check_if_long_away_message_is_truncated(random_msg)

            # Check if different languages with foreign characters are working

            foreign_messages = {"Korean": "곧 돌아올게요",
                                "Arabic": "سأعود قريباً",
                                "Chinese": "我会很快回来",
                                "Hindi": "मैं जल्दी ही वापस आऊँगा",
                                }

            for language, message in foreign_messages.items():
                self._connect_coily()

                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                    reservation_start_time=start_time,
                    time_offset=reservation_time_duration,
                    time_format=current_time_format)

                self.logi_tune_coily_settings_page.set_away_message_and_submit(message)
                self._disconnect_coily()

                self.coily_methods.click_and_verify_away_message(message, account_type)

            emojis_messages = {
                "sick": "I am sick 🤧",
                "busy": "I am currently busy 😇😤",
                "dental": "Dental appointment 🦷"
            }
            for _, message in emojis_messages.items():
                self._connect_coily()

                self.coily_methods.verify_coily_is_checked_in_walk_in_session_notification(
                    reservation_start_time=start_time,
                    time_offset=reservation_time_duration,
                    time_format=current_time_format)

                self.logi_tune_coily_settings_page.set_away_message_with_emoji(message)
                self._disconnect_coily()
                self.coily_methods.click_and_verify_away_message(message, account_type)

        except Exception as e:
            Report.logInfo(str(e), screenshot=True, color='red')
            Report.logException(str(e), is_collabos=True)

    def tc_coily_identified_session_privacy_mode_change_visible_on_identified_page(self,
                                                                                   account_type:
                                                                                   Union[GOOGLE, MICROSOFT]):

        try:
            self._enter_walkin_session_with_check(
                account_type=account_type)

            work_account_credentials = prepare_work_account_credentials(account_type)
            current_coily_sync_settings = self.get_current_sync_portal_coily_settings()

            multiple_events = random.randint(2, 4)

            meeting_data = []

            Report.logInfo(f"Creating events with number: {multiple_events}")
            for no in range(multiple_events):
                meeting_start_time = datetime.now() + timedelta(minutes=no*30 + random.randint(0, 30))
                duration_min = 60
                event_title = f"Coily Agenda test {no+1}"
                meeting_info = dict(account_type=account_type,
                                    credentials=work_account_credentials,
                                    duration_min=duration_min,
                                    event_title=event_title,
                                    meeting_start_time=meeting_start_time,
                                    meeting_duration_min=duration_min)
                meeting_data.append(meeting_info)

                self._create_calendar_event(meeting_info)

            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            privacy_mode = current_coily_sync_settings['privacy_mode_enabled']
            time_format = current_coily_sync_settings['time_format']

            # Check if meeting notification is correct for current privacy mode
            self.coily_methods.verify_privacy_mode_main_page(privacy_mode, time_format, meeting_data)

            # toggle privacy mode
            privacy_mode = self.logi_tune_coily_settings_page.toggle_privacy_mode()
            self.coily_settings_page.verify_privacy_mode(privacy_mode)

            # Check if meeting notification is correct for toggled
            self.coily_methods.verify_privacy_mode_main_page(privacy_mode, time_format, meeting_data)

            # toggle privacy mode back
            privacy_mode = self.logi_tune_coily_settings_page.toggle_privacy_mode()
            self.coily_settings_page.verify_privacy_mode(privacy_mode)

            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)

        except Exception as e:
            Report.logWarning(str(e), screenshot=True)
            Report.logException(str(e), is_collabos=True)

    def tc_coily_identified_session_brightrness_in_tune_menu(self,
                                                             account_type:
                                                             Union[GOOGLE, MICROSOFT]):

        try:
            self._enter_walkin_session_with_check(
                account_type=account_type)

            current_brightness_in_tune = self.logi_tune_coily_settings_page.get_current_brightness()
            current_brightness_on_coily = self.coily_settings_page.get_current_brightness()

            self.coily_methods.compare_brightness_tune_coily(current_brightness_in_tune, current_brightness_on_coily)

            test_data = {
                "brightness": (1, 2, random.randint(3, 99), 100),
            }

            for scenario in range(4):
                brightness_to_set = test_data['brightness'][scenario]
                self.logi_tune_coily_settings_page.set_brightness(brightness_to_set)

                brightness_on_coily = self.coily_settings_page.get_current_brightness()
                self.coily_methods.compare_brightness_tune_coily(brightness_to_set, brightness_on_coily)

                # Close Tune Coily Settings for persistency check
                self.logi_tune_coily_settings_page.verify_parameters_persistence_after_reopening_settings()

        except Exception as e:
            Report.logWarning(str(e), screenshot=True)
            Report.logException(str(e), is_collabos=True)

    def tc_localization_main_idle_page(self, lang_name: str, lang_value: str):
        try:
            self.sync_portal_services.set_coily_settings(locale=lang_value)
            time.sleep(5)
            Report.logScreenshot(f"{lang_name}", "Home", "Home", is_collabos=True, delay=True)
            self.coily_methods.click_book_desk_button()
            Report.logScreenshot(f"{lang_name}", "BookDeskviaQR", "BookDeskViaQR", is_collabos=True, delay=True)
            self.coily_methods.click_book_desk_button_confirmation()
            self.coily_methods.open_coily_settings_page()
            Report.logScreenshot(f"{lang_name}", "PinPage", "PinPage", is_collabos=True, delay=True)
            self.coily_methods.close_pin_page()
            time.sleep(2)
        except Exception as e:
            Report.logException(str(e), is_collabos=True)

    def tc_localization_anonymous_walk_in_session(self, lang_name: str, lang_value: str):
        try:
            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)
            time.sleep(2)
            self.sync_portal_services.change_walk_in_session_value(None)
            time.sleep(1)

            # Connect Coily to laptop
            self._connect_coily()
            time.sleep(5)
            Report.logScreenshot(f"{lang_name}", "YouNeedReservation", "YouNeedReservation", is_collabos=True, delay=True)
            # Disconnect Coily from laptop
            self._disconnect_coily()
            time.sleep(2)

            # Set walk-in session duration in Sync Portal
            reservation_time_duration = 3
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)

            # Connect Coily to laptop
            self._connect_coily()

            time.sleep(3)
            Report.logScreenshot(f"{lang_name}", "AnonymousWalkInSessionCheckingYouIn",
                                 "AnonymousWalkInSessionCheckingYouIn", is_collabos=True, delay=True)

            self.coily_methods.click_notification_action_during_check_in()
            Report.logScreenshot(f"{lang_name}", "AnonymousWalkInSessionCheckingYouInLearnMore",
                                 "AnonymousWalkInSessionCheckingYouInLearnMore", is_collabos=True, delay=True)

            time.sleep(15)

            Report.logScreenshot(f"{lang_name}", "AnonymousWalkInSessionCheckedIn", "AnonymousWalkInSessionCheckedIn",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_notification_action_during_check_in()
            Report.logScreenshot(f"{lang_name}", "AnonymousWalkInSessionFeelLikeHome",
                                 "AnonymousWalkInSessionFeelLikeHome",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_notification_action_during_check_in()
            Report.logScreenshot(f"{lang_name}", "AnonymousWalkInSessionMakeDeskPersonal",
                                 "AnonymousWalkInSessionMakeDeskPersonal",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_notification_dismiss_during_check_in()
            time.sleep(2)

            self.coily_methods.open_coily_settings_page()
            Report.logScreenshot(f"{lang_name}", "AdminSettings", "AdminSettings",
                                 is_collabos=True, delay=True)

            self.coily_methods.open_coily_language_settings_page()
            Report.logScreenshot(f"{lang_name}", "AdminLangaugeSettings", "AdminLangaugeSettings",
                                 is_collabos=True, delay=True)

            # Disconnect Coily
            self._disconnect_coily()

            Report.logScreenshot(f"{lang_name}", "WalkInSessionIsOver", "WalkInSessionIsOver", is_collabos=True)
        except Exception as e:
            Report.logException(str(e), is_collabos=True, delay=True)


    def tc_localization_identified_walk_in_session(self, lang_name: str, lang_value: str, account_type: str):
        try:

            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)
            time.sleep(5)

            work_account_credentials = prepare_work_account_credentials(account_type)

            # Create Calendar event for the user
            event_details = {
                'account_type': account_type,
                'credentials': work_account_credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily single event:",

            }

            # Create Calendar event
            meeting_title = self._create_calendar_event(event_details)

            # Set walk-in session duration
            reservation_time_duration = 1
            self.sync_portal_services.change_walk_in_session_value(reservation_time_duration)
            time.sleep(5)
            self.sync_portal_services.change_auto_extend_value(None)

            # Open Logi Tune and connect to Work account
            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            time.sleep(5)

            # Connect Coily to laptop
            self._connect_coily()
            time.sleep(3)
            Report.logScreenshot(f"{lang_name}", "IdentifiedWalkInSessionCheckingYouIn",
                                 "IdentifiedWalkInSessionCheckingYouIn", is_collabos=True, delay=True)
            start_time = get_curent_time()
            Report.logInfo(f'Reservation start time: {start_time}')

            self.coily_methods.click_notification_action_during_check_in()
            time.sleep(1)
            Report.logScreenshot(f"{lang_name}", "IdentifiedWalkInSessionCheckingYouInLearnMore",
                                 "IdentifiedWalkInSessionCheckingYouInLearnMore", is_collabos=True, delay=False)

            time.sleep(15)

            Report.logScreenshot(f"{lang_name}", "IdentifiedWalkInSessionCheckedIn", "IdentifiedWalkInSessionCheckedIn",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_notification_action_during_check_in()
            Report.logScreenshot(f"{lang_name}", "IdentifiedWalkInSessionWelcomeMessage",
                                 "IdentifiedWalkInSessionWelcomeMessage",
                                 is_collabos=True, delay=True)

            time.sleep(1)

            self.coily_methods.click_agenda_item_by_title(event_title=meeting_title)
            time.sleep(2)
            Report.logScreenshot(f"{lang_name}", "EventDetails",
                                 "EventDetails",
                                 is_collabos=True, delay=True)

            self.coily_methods.close_event_details()

            time.sleep(3)

            event_all_day_details = {
                'account_type': account_type,
                'credentials': work_account_credentials,
                'start_time': datetime.now().date() - timedelta(days=1),
                'duration': 3,
                'summary': "Coily all-day test:",
                'location': "Krakow, Poland",
                'guests_email_list': [
                    ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + "@testlogi.com" for _ in
                    range(10)],
                'description': "Welcome to the jungle"
            }

            # Create Calendar event
            meeting_all_day_title = self._create_all_day_calendar_event(event_all_day_details, delete_all_other_meetings=True)

            time.sleep(10)

            Report.logScreenshot(f"{lang_name}", "EventDetails1",
                                 "EventDetails1",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_agenda_item_by_title(event_title=meeting_all_day_title)
            time.sleep(2)
            Report.logScreenshot(f"{lang_name}", "EventDetails2",
                                 "EventDetail2",
                                 is_collabos=True, delay=True)

            self.coily_methods.scroll_to_agenda_notes()

            time.sleep(2)
            Report.logScreenshot(f"{lang_name}", "EventDetails3",
                                 "EventDetails3",
                                 is_collabos=True, delay=True)

            self.coily_methods.click_show_all_attendees()

            self.coily_methods.scroll_to_agenda_notes()

            Report.logScreenshot(f"{lang_name}", "EventDetails4",
                                 "EventDetails4",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=True)

            time.sleep(2)

            self.coily_methods.close_event_details()
            Report.logScreenshot(f"{lang_name}", "AuthenticatedPagePrivacyModeON",
                                 "AuthenticatedPagePrivacyModeON",
                                 is_collabos=True, delay=True)

            event_details_2 = {
                'account_type': account_type,
                'credentials': work_account_credentials,
                'meeting_start_time': datetime.now() + timedelta(minutes=30),
                'meeting_duration_min': 60,
                'event_title': "Coily test:"
            }

            # Create Calendar event
            meeting_title = self._create_calendar_event(event_details_2)
            time.sleep(5)

            Report.logScreenshot(f"{lang_name}", "AuthenticatedPagePrivacyModeONv2",
                                 "AuthenticatedPagePrivacyModeONv2",
                                 is_collabos=True, delay=True)

            # Disconnect Coily from laptop
            self._disconnect_coily()

            time.sleep(5)

            Report.logScreenshot(f"{lang_name}", "LaptopDisconnectedAwayPicker",
                                 "LaptopDisconnectedAwayPicker",
                                 is_collabos=True, delay=True)

            self.coily_methods.home.click_away_state((By.XPATH, '//android.view.ViewGroup[@index="0"]'))
            Report.logScreenshot(f"{lang_name}", "AwayMessage",
                                 "AwayMessage",
                                 is_collabos=True, delay=True)

            time.sleep(5)
            self.delete_active_reservations_for_user(work_account_credentials)

            time.sleep(5)
            self.sync_portal_services.change_auto_extend_value(600)

            time.sleep(5)

            # Connect Coily to laptop
            self._connect_coily()
            time.sleep(10)
            Report.logScreenshot(f"{lang_name}", "BlockFromReusingTheDesk",
                                 "BlockFromReusingTheDesk", is_collabos=True, delay=True)

            self._disconnect_coily()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_active_reservations_for_user(work_account_credentials)
            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)
            self.delete_active_reservations_for_desk()
            self.clean_tune_connected_account()
            self.clean_existing_reservation_on_the_desk()

    def tc_localization_booked_session(self, lang_name: str, lang_value: str, account_type: str, wrong_account_type: str):
        try:

            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)

            time.sleep(5)
            self.sync_portal_services.change_auto_extend_value(None)

            work_account_credentials = prepare_work_account_credentials(account_type)

            self.reservation = self._create_and_verify_session_in_progress(work_account_credentials,
                                                                           reservation_duration=random.randint(1, 6),
                                                                           verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "OngoingReservation",
                                 "OngoingReservation", is_collabos=True, delay=True)

            time.sleep(5)

            # Connect Coily to laptop
            self._connect_coily()
            self.coily_methods.open_app(force=True)

            time.sleep(3)
            Report.logScreenshot(f"{lang_name}", "CheckingYouInBooked",
                                 "CheckingYouInBooked", is_collabos=True, delay=True)

            time.sleep(15)

            Report.logScreenshot(f"{lang_name}", "ErrorYouCantUseThisDesk",
                                 "ErrorYouCantUseThisDesk", is_collabos=True, delay=True)

            self.coily_methods.open_app(force=True)
            self.coily_methods.click_check_in_via_tune_mobile()
            Report.logScreenshot(f"{lang_name}", "CheckInViaTuneMobile",
                                 "CheckInViaTuneMobile", is_collabos=True, delay=True)

            self.coily_methods.open_app(force=True)
            self.coily_methods.click_back_on_check_in_via_mobile_app()

            self._disconnect_coily()

            time.sleep(3)

            # Open Logi Tune and connect to Work account
            wrong_account_credentials = prepare_work_account_credentials(wrong_account_type)

            self.tune_app.connect_tune_app()
            if not self.tune_methods.verify_sign_in_button_is_displayed():
                self.tune_methods.tc_disconnect_connected_account()

            self.tune_methods.connect_to_work_or_agenda_account(account_type=wrong_account_type,
                                                                account_credentials=wrong_account_credentials)

            self._connect_coily()
            self.coily_methods.open_app(force=True)

            time.sleep(15)

            Report.logScreenshot(f"{lang_name}", "ErrorDeskIsAlreadyReserved",
                                 "ErrorDeskIsAlreadyReserved", is_collabos=True, delay=True)

            self._disconnect_coily()

            time.sleep(3)

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_active_reservations_for_user(work_account_credentials)
            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)
            self.delete_active_reservations_for_desk()
            self.clean_tune_connected_account()
            self.clean_existing_reservation_on_the_desk()

    def tc_localization_desk_conflict(self, lang_name: str, lang_value: str, account_type: str, desk_id: str):
        try:

            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)

            time.sleep(5)
            self.sync_portal_services.change_auto_extend_value(None)

            work_account_credentials = prepare_work_account_credentials(account_type)

            self.reservation = self._create_a_session_with_desk_id(work_account_credentials,
                                                                   desk_id=desk_id,
                                                                   reservation_duration=random.randint(1, 6))

            self.tune_app.connect_tune_app()
            if not self.tune_methods.verify_sign_in_button_is_displayed():
                self.tune_methods.tc_disconnect_connected_account()

            self.tune_methods.connect_to_work_or_agenda_account(account_type=account_type,
                                                                account_credentials=work_account_credentials)

            # Connect Coily to laptop
            self._connect_coily()
            self.coily_methods.open_app(force=True)

            time.sleep(15)
            Report.logScreenshot(f"{lang_name}", "AlreadyHaveASession1",
                                 "AlreadyHaveASession1", is_collabos=True, delay=True)

            time.sleep(15)

            self.coily_methods.click_cancel_transfer_desk()

            time.sleep(2)

            Report.logScreenshot(f"{lang_name}", "AlreadyHaveASession2",
                                 "AlreadyHaveASession2", is_collabos=True, delay=True)

            self._disconnect_coily()

            time.sleep(3)

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_active_reservations_for_user(work_account_credentials)
            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)
            self.delete_active_reservations_for_desk()
            self.clean_tune_connected_account()
            self.clean_existing_reservation_on_the_desk()

    def tc_localization_initialisation_screen(self, lang_name: str, lang_value: str):
        try:

            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)

            time.sleep(10)

            restart_scheduler_app_via_adb()

            time.sleep(1)
            Report.logScreenshot(f"{lang_name}", "Initialising",
                                 "Initialising", is_collabos=True, delay=True)

        except Exception as e:
            Report.logException(str(e), is_collabos=True)


    def tc_localization_early_check_in(self,
                                       lang_name: str,
                                       lang_value: str,
                                       correct_user_account_type,
                                       correct_user,
                                       wrong_user_account_type,
                                       wrong_user,
                                       reservation_delay):
        try:
            self.sync_portal_services.change_auto_extend_value(None)
            time.sleep(1)
            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)

            time.sleep(5)

            # Set walk-in session duration in Sync Portal
            self.sync_portal_services.change_walk_in_session_value(1)

            # Create a future reservation and verify it on Coily
            self.reservation = self._create_and_verify_future_reservation_in_displayed(credentials=correct_user,
                                                                                       reservation_delay=reservation_delay,
                                                                                       reservation_time_duration=2,
                                                                                       verify_reservation=False)

            if wrong_user != 'anonymous':
                self.tune_methods.connect_to_work_or_agenda_account(account_type=wrong_user_account_type,
                                                                    account_credentials=wrong_user)

            # Connect Coily to laptop
            self._connect_coily()

            time.sleep(20)

            Report.logScreenshot(f"{lang_name}", "CenterNotification",
                                 "CenterNotification", is_collabos=True, delay=True)

            self.coily_methods.click_center_pile_with_time_left_in_the_reservation()
            Report.logScreenshot(f"{lang_name}", "CenterNotificationMessage",
                                 "CenterNotificationMessage", is_collabos=True, delay=True)

            self.coily_methods.click_desk_limit_got_it_button()

            time.sleep(2)

            self.coily_methods.verify_countdown_icon_displayed()
            Report.logScreenshot(f"{lang_name}", "CountdownMessage",
                                 "CountdownMessage", is_collabos=True, delay=True)

            self.coily_methods.verify_session_is_over_v3(verify_message=False)
            Report.logScreenshot(f"{lang_name}", "SessionIsOverV3",
                                 "SessionIsOverV3", is_collabos=True, delay=True)

            # Disconnect Coily from laptop
            self._disconnect_coily()

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_active_reservations_for_user(correct_user)
            self.delete_all_calendar_event_for_the_user(correct_user_account_type, correct_user)
            self.delete_active_reservations_for_desk()
            self.clean_tune_connected_account()
            self.clean_existing_reservation_on_the_desk()

    def tc_localization_different_kind_of_booked_sessions(self, lang_name: str, lang_value: str, account_type: str):
        try:
            time.sleep(5)
            self.sync_portal_services.set_coily_settings(locale=lang_value, privacy_mode_enabled=False)
            time.sleep(5)
            self.sync_portal_services.change_auto_extend_value(None)

            work_account_credentials = prepare_work_account_credentials(account_type)

            reservation_0 = self._create_and_verify_session_in_progress(work_account_credentials,
                                                                           reservation_duration=random.randint(1, 6),
                                                                           verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "OngoingReservation",
                                 "OngoingReservation", is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_0[0])

            time.sleep(5)

            # Create a future reservation and check if it is displayed on Coily
            reservation_1 = self._create_and_verify_future_reservation_in_displayed(credentials=work_account_credentials,
                                                                                       reservation_delay=1,
                                                                                       reservation_time_duration=60,
                                                                                    verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "ReservationDelay1",
                                 "ReservationDelay1",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_1[0])

            time.sleep(10)

            reservation_2 = self._create_and_verify_future_reservation_in_displayed(
                credentials=work_account_credentials,
                reservation_delay=10,
                reservation_time_duration=60,
                verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "ReservationDelay10",
                                 "ReservationDelay10",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_2[0])

            time.sleep(10)

            reservation_3 = self._create_and_verify_future_reservation_in_displayed(
                credentials=work_account_credentials,
                reservation_delay=60,
                reservation_time_duration=60,
                verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "ReservationDelay60",
                                 "ReservationDelay60",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_3[0])

            time.sleep(10)

            reservation_5 = self._create_and_verify_future_reservation_in_displayed(
                credentials=work_account_credentials,
                reservation_delay=61,
                reservation_time_duration=60,
                verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "ReservationDelay61",
                                 "ReservationDelay61",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_5[0])

            time.sleep(10)

            reservation_6 = self._create_and_verify_future_reservation_in_displayed(
                credentials=work_account_credentials,
                reservation_delay=151,
                reservation_time_duration=60,
                verify_reservation=False)
            Report.logScreenshot(f"{lang_name}", "ReservationDelay151",
                                 "ReservationDelay151",
                                 is_collabos=True, delay=True)

            self.sync_portal_services.delete_reservation_by_reservation_id(reservation_id=reservation_6[0])

            time.sleep(10)

        except Exception as e:
            Report.logException(str(e), is_collabos=True)
        finally:
            self.delete_active_reservations_for_user(work_account_credentials)
            self.delete_all_calendar_event_for_the_user(account_type, work_account_credentials)
            self.delete_active_reservations_for_desk()
            self.clean_tune_connected_account()
            self.clean_existing_reservation_on_the_desk()


    def delete_active_reservations_for_user(self, user_credentials):
        """
        Delete all active reservations for the user.
        """
        self.sync_portal_services.delete_active_reservations_via_sync_api(user_credentials)

    def delete_active_reservations_for_desk(self):
        """
        Delete all active reservations for the desk.
        """
        self.sync_portal_services.delete_active_reservations_for_desk()

    def clean_the_desk_appium_driver_setup(self):
        """
        Disconnect Coily and click on "Release the desk" button if visible.
        Clean the appium driver setup.
        """
        self.clean_existing_reservation_on_the_desk()
        self.sync_portal_services.delete_active_reservations_for_desk()
        if global_variables.driver:
            global_variables.driver = None
        if global_variables.collabos_driver:
            global_variables.collabos_driver.quit()
            global_variables.collabos_driver = None
        if self.appium_service is not None:
            self.appium_service.stop()

    def clean_existing_reservation_on_the_desk(self):
        """
        Disconnect Coily and click on "Release the desk" button if visible
        """
        Report.logInfo("Clean the desk")
        time.sleep(5)
        disconnect_all()
        self.coily_methods.click_release_the_desk_if_visible()
