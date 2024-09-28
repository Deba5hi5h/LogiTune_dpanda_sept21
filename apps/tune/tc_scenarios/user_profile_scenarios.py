import random

from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from common.framework_params import COILY_BASECAMP_NAME
from extentreport.report import Report


class UserProfileScenarios(WorkAccountScenarios):

    def tc_user_profile_page_check(self, credentials) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_user_profile_button()
            Report.logInfo("Checking if username label is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_profile_name(),
                log_pass="User profile label visible on page",
                log_fail="User profile label not visible on page"
            )

            user_name = credentials['signin_payload']['name']
            user_surname = credentials['signin_payload']['surname']

            user_creds = f"{user_name} {user_surname}"

            Report.logInfo(f"Checking if correct username ({user_creds}) is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_profile_name_by_text(user_creds),
                log_pass=f"Correct username {user_creds} is visible",
                log_fail=f"Username {user_creds} is not visible on page"
            )
            Report.logInfo("Checking if Basecamp label is visible on page")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_profile_basecamp_name(),
                log_pass="Basecamp label is visible on page",
                log_fail="Basecamp name is not visible on page"
            )

            basecamp_name = COILY_BASECAMP_NAME

            Report.logInfo(f"Checking if Basecamp name: {basecamp_name} is visible on User Page")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_basecamp_name_by_text(basecamp_name),
                log_pass=f"Basecamp name: {basecamp_name} is visible in User Page",
                log_fail=f"Basecamp name: {basecamp_name} is not visible in User Page"
            )

            Report.logInfo(f"Checking if Keep bookings hidden switch is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_keep_bookings_hidden_button(),
                log_pass=f"Keep bookings hidden switch is visible in User Profile Page",
                log_fail=f"Keep bookings hidden switch is not visible in User Profile Page"
            )

            Report.logInfo(f"Checking if Calendar and meetings button is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_calendar_and_meetings_button(),
                log_pass=f"Calendar and meetings button is visible in User Profile Page",
                log_fail=f"Calendar and meetings button is not visible in User Profile Page"
            )

            Report.logInfo(f"Checking if Notifications button is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_notifications_button(),
                log_pass=f"Notifications button is visible in User Profile Page",
                log_fail=f"Notifications button is not visible in User Profile Page"
            )

            Report.logInfo(f"Checking if Connected Account button is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_connected_account_button(),
                log_pass=f"Connected Account button is visible in User Profile Page",
                log_fail=f"Connected Account button is not visible in User Profile Page"
            )

            Report.logInfo(f"Checking if Privacy and usage button is visible")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_privacy_settings_button(),
                log_pass=f"Privacy and usage button is visible in User Profile Page",
                log_fail=f"Privacy and usage button is not visible in User Profile Page"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_user_profile_page_default_building_change(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_user_profile_button()

            basecamp_name = COILY_BASECAMP_NAME

            Report.logInfo(f"Checking if Basecamp name: {basecamp_name} is visible on User Page before change")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_basecamp_name_by_text(basecamp_name),
                log_pass=f"Basecamp name: {basecamp_name} is visible in User Page",
                log_fail=f"Basecamp name: {basecamp_name} is not visible in User Page"
            )

            self.tune_pages.user_profile_page.click_basecamp_button()

            org_info = self.sync_api_methods.get_org_info(self.org_id).json()
            site_buildings = {k: v for k, v in org_info['groups']['loc'][self.site].items() if type(v) is dict}
            building_siblings = [details.get("$label") or building for building, details in site_buildings.items() if
                                 type(details) is dict]
            building_siblings = [building for building in building_siblings if building != self.building]
            sibling = random.choice(building_siblings)
            self.tune_pages.basecamp.click_chosen_basecamp(sibling)

            Report.logInfo(f"Checking if Basecamp name: {sibling} is visible on User Page after change")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_basecamp_name_by_text(sibling),
                log_pass=f"Basecamp name: {sibling} is visible in User Page",
                log_fail=f"Basecamp name: {sibling} is not visible in User Page"
            )

            self.tune_pages.user_profile_page.click_basecamp_button()
            self.tune_pages.basecamp.click_chosen_basecamp(self.building)

            Report.logInfo(f"Checking if Basecamp name: {basecamp_name} is visible on User Page "
                           f"after change to default")
            self._assert(
                condition=self.tune_pages.user_profile_page.verify_basecamp_name_by_text(basecamp_name),
                log_pass=f"Basecamp name: {basecamp_name} is visible in User Page",
                log_fail=f"Basecamp name: {basecamp_name} is not visible in User Page"
            )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_user_profile_page_keep_bookings_private_check(self) -> None:

        # TODO finish when co-booking methods will be available
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_user_profile_button()
            bookings_hidden = self.tune_pages.user_profile_page.check_keep_bookings_hidden()
            Report.logInfo(f"Current Keep Bookings Private button status is: {bookings_hidden}")
            if bookings_hidden:
                self.tune_pages.user_profile_page.click_keep_bookings_hidden_button()
            self.tune_pages.home.wait_for_page_reload()
            changed_bookings_hidden = self.tune_pages.user_profile_page.check_keep_bookings_hidden()
            Report.logInfo(f"Button state after change: {changed_bookings_hidden}")
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_user_profile_page_default_building_change_and_book(self) -> None:

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_user_profile_button()

            site_buildings = self.sync_api_methods.get_org_info(self.org_id).json()['groups']['loc'][self.site]
            building_siblings = [building for building in site_buildings.keys() if building != self.building]
            sibling = "Ghost-" + self.building
            Report.logInfo("Checking if Ghost building in siblings")
            self._assert(
                condition=sibling in building_siblings,
                log_pass="Sibling builiding visible",
                log_fail="Sibling building not visible"
            )

            self.tune_pages.user_profile_page.click_basecamp_button()
            self.tune_pages.basecamp.click_chosen_basecamp(sibling)
            self.tune_pages.user_profile_page.click_back_to_dashboard_button()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()
            if self.tune_pages.desk_booking.verify_no_desks_available_label():
                Report.logInfo("No desks available clicking OK")
            self._assert(
                condition=self.tune_pages.desk_booking.verify_default_book_a_desk_office_location_text(sibling),
                log_pass=f"Desk ({sibling}) is visible as default when booking a desk",
                log_fail=f"Desk ({sibling}) is not visible as default when booking a desk"
            )
            self.tune_pages.desk_booking.verify_no_desks_available_label()
            self.tune_pages.desk_booking.click_back_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_user_profile_button()
            self.tune_pages.user_profile_page.click_basecamp_button()
            self.tune_pages.basecamp.click_chosen_basecamp(self.building)

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")
