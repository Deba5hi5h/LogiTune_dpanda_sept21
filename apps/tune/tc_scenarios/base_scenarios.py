import time
from datetime import datetime, timedelta
from typing import Optional, Union, Tuple

from PIL import ImageColor
from selenium.webdriver.remote.webdriver import WebDriver

from apps.tune.api.api_methods import SyncApiMethods
from apps.tune.browser_login import TuneBrowserLogin
from apps.tune.calendar_api import (GoogleCalendarApi, MicrosoftCalendarApi, COILY_CALENDAR_PATH,
                                    CALENDAR_TOKEN_PATH)
from apps.tune.pages.all_pages import TunePages
from apps.tune.TuneElectron import TuneElectron
from base import global_variables
from base.base_settings import GOOGLE, MICROSOFT
from common.framework_params import COILY_BASECAMP_LOCATION, COILY_BASECAMP_NAME, COILY_DESK_ID
from common.platform_helper import get_correct_time_format_based_on_system
from extentreport.report import Report


class BaseColors:

    def __init__(self, appearance_mode: str):
        self.appearance_mode = appearance_mode

    APPEARANCE_MODE_COLORS = {
        'light': {
            "COLOR_CALENDAR_HOVER": "#814EFA",
            "COLOR_FUTURE_TODAY": "#814EFA",
            "COLOR_ONGOING": "#44A950",
            "COLOR_FUTURE_NOT_TODAY": "#6F7678",
            "COLOR_ABOUT_TO_EXPIRE": "#FF2947",
            "COLOR_ONGOING_NOT_CHECKED_IN": "#CC8310"
        },
        'dark': {
            "COLOR_CALENDAR_HOVER": "#9F8BFF",
            "COLOR_FUTURE_TODAY": "#9580FF",
            "COLOR_ONGOING": "#29CC52",
            "COLOR_FUTURE_NOT_TODAY": "#6F7678",
            "COLOR_ABOUT_TO_EXPIRE": "#FF6673",
            "COLOR_ONGOING_NOT_CHECKED_IN": "#CC8310"
        }
    }

    @staticmethod
    def hex_to_rgb(hex_string: str) -> str:
        return f'rgba{(*ImageColor.getcolor(hex_string, "RGB"), 1)}'

    @property
    def color_future_today(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode).get("COLOR_FUTURE_TODAY")
        return self.hex_to_rgb(hex_color)

    @property
    def color_future_not_today(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode
                                                    ).get("COLOR_FUTURE_NOT_TODAY")
        return self.hex_to_rgb(hex_color)

    @property
    def color_ongoing_not_checked_in(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode
                                                    ).get("COLOR_ONGOING_NOT_CHECKED_IN")
        return self.hex_to_rgb(hex_color)

    @property
    def color_expire(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode
                                                    ).get("COLOR_ABOUT_TO_EXPIRE")
        return self.hex_to_rgb(hex_color)

    @property
    def color_ongoing(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode).get("COLOR_ONGOING")
        return self.hex_to_rgb(hex_color)

    @property
    def color_calendar_hover(self) -> str:
        hex_color = self.APPEARANCE_MODE_COLORS.get(self.appearance_mode
                                                    ).get("COLOR_CALENDAR_HOVER")
        return self.hex_to_rgb(hex_color)


class BaseScenarios:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.tune_pages = TunePages(self.driver)

    @property
    def appearance_mode(self) -> str:
        return self.tune_pages.home.get_appearance_mode()

    @property
    def tune_colors(self) -> BaseColors:
        return BaseColors(self.appearance_mode)

    @staticmethod
    def _assert(condition: bool, log_pass: str, log_fail: str,
                screenshot_on_pass: bool = True, wait_before_assert: int = 0.5) -> None:
        time.sleep(wait_before_assert)
        assert condition, Report.logFail(log_fail)
        Report.logPass(log_pass, screenshot=screenshot_on_pass)


class WorkAccountScenarios(BaseScenarios):

    COILY_CALENDAR_PATH = COILY_CALENDAR_PATH
    TUNE_CALENDAR_PATH = CALENDAR_TOKEN_PATH

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.browser_login = TuneBrowserLogin()
        self.sync_api_methods = SyncApiMethods()

        self.desk_id = COILY_DESK_ID
        self.org_id = self.sync_api_methods.org_id
        self.org_name = self.sync_api_methods.org_name
        self.desk_info = self.sync_api_methods.get_desk_info(self.org_id, self.desk_id).json()
        if self.desk_info.get('statusCode') and self.desk_info.get('statusCode') == 403:
            raise ConnectionRefusedError(f'Status Code: {self.desk_info.get('statusCode')} - '
                                         f'Provided user: {self.sync_api_methods.email} '
                                         f'has no access to this endpoint.')
        self.desk_name = self.desk_info.get('name')
        self.group = self.desk_info.get('group')
        self.group_desk_list = self.sync_api_methods.algolia.get_desks_in_group(self.org_id,
                                                                                self.group)
        self.group_desk_list_names = [el.get('name') for el in self.group_desk_list]
        self.desk_sibling_name_list = [desk for desk in self.group_desk_list_names if
                                       desk != self.desk_name]
        self.site, self.building, self.floor, self.area = self.group[1:-2].split('/')
        self.location = " · ".join([self.building, self.floor, self.area])
        self.logged_user_email = None

        org_end_users = self.sync_api_methods.algolia.get_end_users_in_org(self.org_id)
        org_end_users_dict = {el.get('name') or el.get('email'): el for el in org_end_users}
        self.org_end_users = list(org_end_users_dict.values())

    @property
    def default_booking_timestamps(self) -> Tuple[str, str]:

        start_time = datetime.now().strftime(get_correct_time_format_based_on_system(f"%_I:%M %p"))

        time_part_zeros = {"minute": 0,
                           "second": 0,
                           "microsecond": 0}

        default_booking_finish_time = datetime.now().replace(**{"hour": 17, **time_part_zeros})
        current_time = datetime.now()

        if default_booking_finish_time.timestamp() - current_time.timestamp() > 3600:
            end_time = "5:00 PM"
        else:
            end_time_raw = (current_time + timedelta(hours=2)).replace(**time_part_zeros)
            if end_time_raw.day > datetime.now().day:
                end_time = "11:59 PM"
            else:
                end_time = end_time_raw.strftime(
                    get_correct_time_format_based_on_system(f"%_I:%M %p"))
        return start_time, end_time

    def _get_calendar_instance_based_on_creds(self, provider: str, credentials: dict
                                              ) -> Union[GoogleCalendarApi, MicrosoftCalendarApi]:

        if provider == GOOGLE:
            coily_user = credentials.get('coily_user')
            calendar_api = GoogleCalendarApi(
                token_short_path=self.COILY_CALENDAR_PATH
                if coily_user else self.TUNE_CALENDAR_PATH,
                email=credentials['signin_payload']['email'],
                password=credentials['signin_payload']['password'],
                employee_id=credentials['signin_payload']['employee_id']
            )
        else:
            calendar_api = MicrosoftCalendarApi(email=credentials['signin_payload']['email'],
                                                password=credentials['signin_payload']['password'])
        return calendar_api

    def tc_login_to_work_account(self, provider: str, credentials: Optional[dict] = None) -> None:
        """
        Method to connect to work account
        :param provider: String to choose which provider (Google or Outlook) should be used
        :param credentials: Dictionary which consist of name, surname, email and password stored in
        config file on s3
        :return none
        """
        try:
            if self._connect_to_work_account(provider, credentials):
                Report.logPass(f'Logging in to {provider.capitalize()} '
                               f'Work Account finished with success!')
            else:
                Report.logException('Logged in with wrong account - it must to be Work Account!')
        except Exception as e:
            Report.logInfo(f'Exception tc_login_to_work_account: {repr(e)}')
        finally:
            self.browser_login.close_all_browsers()
            time.sleep(3)

    def create_calendar_event(self, provider: str, credentials: dict,
                              event_data: dict) -> Optional[dict]:

        calendar_api = self._get_calendar_instance_based_on_creds(provider, credentials)

        summary = event_data.get("summary")
        start_time = event_data.get("start_time")
        duration = event_data.get("duration")
        attendees = event_data.get("attendees")
        video_event = event_data.get("video_event", True)

        event = calendar_api.create_event(
            start_time=start_time,
            summary=summary,
            duration_min=duration,
            attendees=attendees,
            video_event=video_event
        )
        return event

    def create_calendar_all_day_event(self, provider: str, credentials: dict,
                                      event_data: dict) -> dict:
        calendar_api = self._get_calendar_instance_based_on_creds(provider, credentials)

        summary = event_data.get("summary")
        start_time = event_data.get("start_time")
        duration = event_data.get("duration")
        attendees = event_data.get("attendees")
        video_event = event_data.get("video_event", True)

        event = calendar_api.create_all_day_event(
            start_time=start_time,
            summary=summary,
            duration_days=duration,
            attendees=attendees,
            video_event=video_event
        )
        return event

    def edit_event_response_for_owner(self, provider: str, credentials: dict, event_id: str,
                                      event_response: str) -> dict:
        calendar_api = self._get_calendar_instance_based_on_creds(provider, credentials)

        return calendar_api.change_user_response_for_event(
            event_id, credentials['signin_payload']['email'], event_response)

    def delete_calendar_events(self, provider, credentials: dict) -> None:
        calendar_api = self._get_calendar_instance_based_on_creds(provider, credentials)
        calendar_api.delete_remaining_events()

    def end_occupying_of_the_desk_if_needed(self) -> None:
        self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
        if self.tune_pages.home.verify_booking_card_displayed():
            self._end_occupying_of_the_desk()

    def connect_to_work_account_if_not_logged(self, provider: str,
                                              credentials: Optional[dict] = None,
                                              retry: Optional[int] = 0) -> None:
        if retry == 3:
            Report.logException(f"Connecting to Work Account failed after {retry} attempts.")
            return
        tune_app = TuneElectron()
        try:
            self.tune_pages.home.click_home_tab()
            self.logged_user_email = credentials['signin_payload']['email']
            if self.tune_pages.home.verify_sign_in_button_displayed():
                self._connect_to_work_account(provider, credentials)
            self.tune_pages.home.click_home_tab()
            if self.tune_pages.home.verify_sign_in_button_displayed():
                raise Exception("Sign in button displayed after logging procedure, "
                                "raising exception.")
        except Exception as e:
            Report.logInfo(f"Connecting to {provider} work account Failed: {str(e)}, retrying...")
            tune_app.reopen_tune_app()
            self.connect_to_work_account_if_not_logged(provider, credentials, retry + 1)

    def disconnect_connected_account_if_needed(self) -> None:
        self.tune_pages.home.click_home_tab()
        if not self.tune_pages.home.verify_sign_in_button_displayed():
            self._disconnect_connected_account()

    def _connect_to_work_account(self,  provider: str, credentials: Optional[dict] = None) -> bool:
        if provider not in (GOOGLE, MICROSOFT):
            Report.logException(f'Wrong provider: {provider} - '
                                f'should be "{GOOGLE}" or "{MICROSOFT}"')
        if provider == GOOGLE:
            if credentials is not None:
                email = credentials.get('signin_payload').get('email')
                password = credentials.get('signin_payload').get('password')
                employee_id = credentials.get('signin_payload').get('employee_id')
                coily_user = credentials.get('coily_user')
                GoogleCalendarApi(
                    self.COILY_CALENDAR_PATH if coily_user else self.TUNE_CALENDAR_PATH,
                    email=email,
                    password=password,
                    employee_id=employee_id
                )
            else:
                GoogleCalendarApi(self.TUNE_CALENDAR_PATH)
        time.sleep(1)
        self.browser_login.prepare_opened_browser(guest_mode=True)
        time.sleep(7)
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_sign_in_button()
        self.tune_pages.sign_in.click_privacy_policy_agreement_button()
        self._login_to_work_account(provider, credentials)
        global_variables.driver = self.driver
        if self.tune_pages.onboarding.verify_presence_of_onboarding_page():
            self.tune_pages.onboarding.click_continue_button()
            self.tune_pages.basecamp.search_for_basecamp(COILY_BASECAMP_LOCATION)
            self.tune_pages.basecamp.click_chosen_basecamp(COILY_BASECAMP_NAME)
            self.tune_pages.onboarding.click_skip_button_teammates()
            return True
        return False

    def _disconnect_connected_account(self) -> None:
        self.tune_pages.header.click_settings_dropdown_button()
        self.tune_pages.header.click_popup_settings_button()
        self.tune_pages.settings.click_connected_account_button()
        self.tune_pages.connected_account_settings.click_disconnect_account_button()
        self.tune_pages.connected_account_settings.click_popup_disconnect_button()
        self.tune_pages.connected_account_settings.wait_for_disconnect()

    def _end_occupying_of_the_desk(self) -> None:
        self.tune_pages.home.click_home_tab()
        self.tune_pages.home.click_booking_details_button()
        self.tune_pages.home.click_end_booking_button()
        self.tune_pages.home.click_end_booking_confirm_yes_button()
        self.tune_pages.home.click_booking_cancelled_ok_button()

    def _login_to_work_account(self, provider: str, credentials: Optional[dict] = None,
                               retry: bool = False) -> None:
        if provider == GOOGLE:
            self.tune_pages.sign_in.click_google_account_button()
            result = self.browser_login.sign_in_to_google_work_account(credentials)
        else:
            self.tune_pages.sign_in.click_outlook_account_button()
            result = self.browser_login.sign_in_to_outlook_work_account(credentials)
        if not result:
            if retry:
                self._login_to_work_account(provider, credentials, retry=True)
            else:
                Report.logException(f'Unable to login to {provider.upper()} Work Account')
                raise ConnectionError(f'_login_to_work_account - '
                                      f'Unable to login to {provider.upper()} Work Account')
        Report.logInfo(f'RESULTS FOR LOGIN TO {provider.upper()} WORK ACCOUNT IS: {result}')
