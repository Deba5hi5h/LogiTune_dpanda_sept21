import random

from apps.tune.base.desk_booking_base import Account
from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from extentreport.report import Report
from common.platform_helper import (generate_random_string, get_correct_time_format_based_on_system,
                                    tune_time_format_from_datetime_obj)

from datetime import datetime, timedelta


class PeopleTabScenarios(WorkAccountScenarios):

    def tc_teammate_order_everyone_tab(self):
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_everyone_tab_button()
            if self.tune_pages.people.verify_user_group_visible_by_name('Default'):
                Report.logInfo("Entering Default Group")
                self.tune_pages.people.click_user_group_visible_by_name("Default")

            Report.logInfo("Checking if teammates everyone list is in alphabetical order")
            self._assert(
                condition=self.tune_pages.people.verify_teammates_order(),
                log_pass="Teammates list is in alphabetical order",
                log_fail="Teammates list is not in alphabetical order"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammate_search_bar_everyone_tab(self):
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_everyone_tab_button()

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            teammates_random_number = random.randint(3, 10)

            randomly_selected_users = random.sample(filtered_end_users, k=teammates_random_number) \
                if len(filtered_end_users) > 5 else filtered_end_users

            for user in randomly_selected_users:

                user_name = user.get('name')
                user_email = user.get('email')
                user_repr = user_name or user_email

                self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

                Report.logInfo(f"Searching for user by full field{user_repr}")
                Report.logInfo(f"Typing '{user_repr}' in the search input")
                self.tune_pages.people.input_everyone_search_bar(user_repr)
                self.tune_pages.people.wait_search_to_load()
                self._assert(
                    condition=self.tune_pages.people.verify_searched_user(user=user_repr),
                    log_pass=f"User: {user_repr} searched witch success",
                    log_fail=f"User: {user_repr} not searched witch success"
                )
                if user_name and len(user_name.split(" ")) > 1:
                    user_first_name = user_name.split(' ')[0]
                    Report.logInfo(f"Searching for user by first name {user_first_name}")
                    Report.logInfo(f"Typing '{user_first_name}' in the search input")
                    self.tune_pages.people.input_everyone_search_bar(user_first_name)
                    self.tune_pages.people.wait_search_to_load()
                    self._assert(
                        condition=self.tune_pages.people.verify_searched_user(user=user_first_name),
                        log_pass=f"User: {user_name} searched by first name witch success",
                        log_fail=f"User: {user_name} not searched by first name witch success"
                    )

                    user_second_name = user_name.split(' ')[1]
                    Report.logInfo(f"Searching for user by second name {user_second_name}")
                    Report.logInfo(f"Typing '{user_second_name}' in the search input")
                    self.tune_pages.people.input_everyone_search_bar(user_second_name)
                    self.tune_pages.people.wait_search_to_load()
                    self._assert(
                        condition=self.tune_pages.people.verify_searched_user(user=user_second_name),
                        log_pass=f"User: {user_name} searched by second name witch success",
                        log_fail=f"User: {user_name} not searched by second name witch success"
                    )

            Report.logInfo(f"Searching for non-existing user")
            random_string = generate_random_string(random.randint(6, 15))
            Report.logInfo(f"Searching for randomly generated string: {random_string}")
            self.tune_pages.people.input_everyone_search_bar(random_string)
            self.tune_pages.people.wait_search_to_load()
            Report.logInfo(f"Checking if No results found for {random_string} is visible")
            self._assert(
                condition=self.tune_pages.people.verify_no_results_found_for_str(random_string),
                log_pass=f"No results found for {random_string} is visible",
                log_fail=f"No results found for {random_string} is not visible"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammate_search_profile_check(self):
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_everyone_tab_button()

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            teammates_random_number = random.randint(3, 10)

            randomly_selected_users = random.sample(filtered_end_users, k=teammates_random_number) \
                if len(filtered_end_users) > 5 else filtered_end_users

            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            for user in randomly_selected_users:
                self.tune_pages.home.wait_for_page_reload()

                user_name = user.get('name')
                user_email = user.get('email')
                user_groups = user.get('cohorts')
                user_repr = user_name or user_email

                Report.logInfo(f"Searching for user {user_repr}")
                Report.logInfo(f"Typing '{user_repr}' in the search input")
                self.tune_pages.people.input_everyone_search_bar(user_repr)
                self.tune_pages.people.wait_search_to_load()
                self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=user_repr)
                self.tune_pages.people.click_user_from_everyone_tab_by_name(user_name=user_repr, match_case=True)
                self.tune_pages.people_user.click_add_to_teammates_button()
                Report.logInfo("Verifying if Remove from teammates button is visible")
                self._assert(
                    condition=self.tune_pages.people_user.verify_remove_button_to_be_visible(),
                    log_pass="Remove from teammates button visible - user added",
                    log_fail="Remove from teammates is not visible - user was not added"
                )
                self.tune_pages.people_user.wait_for_refresh()
                if user_name:
                    Report.logInfo(f"Checking if user name: {user_name} is visible in User Profile")
                    self._assert(
                        condition=self.tune_pages.people_user.verify_user_profile_name_by_text(user_name),
                        log_pass=f"Label with text: {user_name} is visible",
                        log_fail=f"Label with text: {user_name} is not visible"
                    )
                Report.logInfo(f"Checking if user email: {user_email} is visible in User Profile")
                self._assert(
                    condition=self.tune_pages.people_user.verify_user_email_name_by_text(user_email),
                    log_pass=f"Label with text: {user_email} is visible",
                    log_fail=f"Label with text: {user_email} is not visible"
                )
                if "Default" in user_groups and len(user_groups) == 1:
                    Report.logInfo(f"Checking if group Default is visible in User's profile")
                    self._assert(
                        condition=self.tune_pages.people_user.verify_user_group_by_text("Default"),
                        log_pass=f"Label with text: 'Default' is visible",
                        log_fail=f"Label with text: 'Default' is not visible"
                    )
                Report.logInfo(f"Exiting user profile page")
                self.tune_pages.people_user.click_back_button()

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammates_add_from_everyone_tab(self):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            teammates_random_number = random.randint(3, 10)

            randomly_selected_users = random.sample(filtered_end_users, k=teammates_random_number) \
                if len(filtered_end_users) > 5 else filtered_end_users

            randomly_selected_users_repr = []
            for user in randomly_selected_users:
                if user.get('name'):
                    randomly_selected_users_repr.append(user['name'])
                else:
                    randomly_selected_users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {randomly_selected_users_repr}")

            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            for user in randomly_selected_users_repr:
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo(f"Searching for user {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people.input_everyone_search_bar(user)
                self.tune_pages.people.wait_search_to_load()
                self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=user)
                Report.logInfo(f"Entering profile for user: {user}")
                self.tune_pages.people.click_user_from_everyone_tab_by_name(user, match_case=True)
                Report.logInfo(f"Adding user: {user} to teammates list")
                self.tune_pages.people_user.click_add_to_teammates_button()

                Report.logInfo("Verifying if Remove from teammates button is visible")
                self._assert(
                    condition=self.tune_pages.people_user.verify_remove_button_to_be_visible(),
                    log_pass="Remove from teammates button visible - user added",
                    log_fail="Remove from teammates is not visible - user was not added"
                )
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo("Going back to teammates page")
                self.tune_pages.people_user.click_back_button()

            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Entering Teammates Tab page")
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo("Clicking All Teammates")
            self.tune_pages.people.verify_all_teammates_button()
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo(f"Checking if every user is visible in All Teammates Page")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list(randomly_selected_users_repr),
                log_pass="Every added teammate is visible on teammates list",
                log_fail="Not every added teammate is visible on teammates list"
            )
            Report.logInfo("Checking if teammates list has expected length")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list_length(randomly_selected_users_repr),
                log_pass="Visible teammates list has expected length",
                log_fail="Visible teammates list has not expected length"
            )
        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammates_add_from_all_teammates_page(self):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo("Entering All Teammates Page")
            self.tune_pages.people.verify_all_teammates_button()
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo("Clicking Add Teammates button")
            self.tune_pages.people_team.click_add_teammates_button()

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            randomly_selected_users = random.sample(filtered_end_users, k=5) if len(filtered_end_users) > 5 \
                else filtered_end_users

            randomly_selected_users_repr = []
            for user in randomly_selected_users:
                if user.get('name'):
                    randomly_selected_users_repr.append(user['name'])
                else:
                    randomly_selected_users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {randomly_selected_users_repr}")

            for user in randomly_selected_users_repr:
                if self.tune_pages.people_team_add_teammate.verify_delete_search_bar_input_button():
                    Report.logInfo(f"Clearing search input")
                    self.tune_pages.people_team_add_teammate.click_delete_search_bar_input_button()
                Report.logInfo(f"Searching for user {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people_team_add_teammate.input_search_bar(user)
                self.tune_pages.people_team_add_teammate.wait_users_search()
                self.tune_pages.people_team_add_teammate.verify_user_button_by_name(user_name=user)
                self.tune_pages.people_team_add_teammate.click_user_button_by_name(user_name=user,
                                                                                   match_case=True)
                self.tune_pages.people_team_add_teammate.verify_loader_not_visible()

            Report.logInfo("Leaving Add to teammates page")

            self.tune_pages.people_team_add_teammate.click_close_button()
            self.tune_pages.home.wait_for_page_reload()

            Report.logInfo(f"Checking if every user is visible in All Teammates Page")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list(randomly_selected_users_repr),
                log_pass="Every added teammate is visible on teammates list",
                log_fail="Not every added teammate is visible on teammates list"
            )
            Report.logInfo("Checking if teammates list has expected length")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list_length(randomly_selected_users_repr),
                log_pass="Visible teammates list has expected length",
                log_fail="Visible teammates list has not expected length"
            )
        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammates_remove_random_teammates_everyone_tab(self) -> None:

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()

            filtered_end_users = [user for user in self.org_end_users if
                                  user.get('email') != self.logged_user_email]

            teammates_random_number = random.randint(3, 10)

            randomly_selected_users = random.sample(filtered_end_users, k=teammates_random_number) \
                if len(filtered_end_users) > 5 else filtered_end_users

            randomly_selected_users_repr = []
            for user in randomly_selected_users:
                if user.get('name'):
                    randomly_selected_users_repr.append(user['name'])
                else:
                    randomly_selected_users_repr.append(user['email'])

            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo(f"Randomly selected users list: {randomly_selected_users_repr}")

            for user in randomly_selected_users_repr:
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo(f"Searching for user {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people.input_everyone_search_bar(user)
                self.tune_pages.people.wait_search_to_load()
                self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=user)
                Report.logInfo(f"Entering profile for user: {user}")
                self.tune_pages.people.click_user_from_everyone_tab_by_name(user, match_case=True)
                Report.logInfo(f"Adding user: {user} to teammates list")
                self.tune_pages.people_user.click_add_to_teammates_button()
                Report.logInfo("Verifying if Remove from teammates button is visible")
                self._assert(
                    condition=self.tune_pages.people_user.verify_remove_button_to_be_visible(),
                    log_pass="Remove from teammates button visible - user added",
                    log_fail="Remove from teammates is not visible - user was not added"
                )
                self.tune_pages.people_user.wait_for_refresh()
                Report.logInfo("Going back to teammates page")
                self.tune_pages.people_user.click_back_button()

            teammates_to_delete = random.sample(randomly_selected_users_repr,
                                                random.randint(1, teammates_random_number - 1))

            Report.logInfo(f"Teammates to delete: {teammates_to_delete}")
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            for user in teammates_to_delete:
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo(f"Searching for user to delete: {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people.input_everyone_search_bar(user)
                self.tune_pages.people.wait_search_to_load()
                self.tune_pages.people.verify_user_from_everyone_tab_by_name(user_name=user)
                Report.logInfo(f"Entering profile for user: {user}")
                self.tune_pages.people.click_user_from_everyone_tab_by_name(user, match_case=True)
                Report.logInfo(f"Removing teammate: {user}")
                self.tune_pages.people_user.click_remove_from_teammates_button()
                self.tune_pages.people_user.click_remove_from_teammates_button_confirm()
                self.tune_pages.people_user.wait_for_remove_button_to_be_not_visible()
                Report.logInfo(f"Checking if Add to teammates button is visible after removal for user: {user}")
                self._assert(
                    condition=self.tune_pages.people_user.verify_add_button_to_be_visible(),
                    log_pass=f"Add to teammates button is visible after user {user} removal",
                    log_fail=f"Add to teammates button is not visible - NOK"
                )
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo("Going back to teammates page")
                self.tune_pages.people_user.click_back_button()

            remaining_teammates = [teammate for teammate in randomly_selected_users_repr
                                   if teammate not in teammates_to_delete]

            Report.logInfo(f"Remaining teammates: {remaining_teammates}")

            Report.logInfo("Entering Teammates Tab page")
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo("Clicking All Teammates")
            self.tune_pages.people.verify_all_teammates_button()
            self.tune_pages.people.click_all_teammates_button()

            Report.logInfo(f"Checking if every remaining user is visible in All Teammates Page")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list(remaining_teammates),
                log_pass="Every added teammate is visible on teammates list",
                log_fail="Not every added teammate is visible on teammates list"
            )
            Report.logInfo("Checking if teammates list has expected length")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list_length(remaining_teammates),
                log_pass="Visible teammates list has expected length",
                log_fail="Visible teammates list has not expected length"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammates_remove_random_teammates_all_teammates_page(self):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo("Entering All Teammates Page")
            self.tune_pages.people.verify_all_teammates_button()
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo("Clicking Add Teammates button")
            self.tune_pages.people_team.click_add_teammates_button()

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            teammates_random_number = random.randint(3, 10)
            randomly_selected_users = random.sample(filtered_end_users, k=teammates_random_number) \
                if len(filtered_end_users) > 5 else filtered_end_users

            randomly_selected_users_repr = []
            for user in randomly_selected_users:
                if user.get('name'):
                    randomly_selected_users_repr.append(user['name'])
                else:
                    randomly_selected_users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {randomly_selected_users_repr}")

            for user in randomly_selected_users_repr:
                if self.tune_pages.people_team_add_teammate.verify_delete_search_bar_input_button():
                    Report.logInfo(f"Clearing search input")
                    self.tune_pages.people_team_add_teammate.click_delete_search_bar_input_button()
                Report.logInfo(f"Searching for user {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people_team_add_teammate.input_search_bar(user)
                self.tune_pages.people_team_add_teammate.wait_users_search()
                self.tune_pages.people_team_add_teammate.verify_user_button_by_name(user_name=user)
                Report.logInfo(f"Adding teammate with name: {user}")
                self.tune_pages.people_team_add_teammate.click_user_button_by_name(user_name=user,
                                                                                   match_case=True)
                self.tune_pages.people_team_add_teammate.verify_loader_not_visible()

            teammates_to_delete = random.sample(randomly_selected_users_repr,
                                                random.randint(1, teammates_random_number - 1))
            Report.logInfo(f"Teammates to delete: {teammates_to_delete}")

            for user in teammates_to_delete:
                if self.tune_pages.people_team_add_teammate.verify_delete_search_bar_input_button():
                    Report.logInfo(f"Clearing search input")
                    self.tune_pages.people_team_add_teammate.click_delete_search_bar_input_button()
                Report.logInfo(f"Searching for user {user}")
                Report.logInfo(f"Typing '{user}' in the search input")
                self.tune_pages.people_team_add_teammate.input_search_bar(user)
                self.tune_pages.people_team_add_teammate.wait_users_search()
                self.tune_pages.people_team_add_teammate.verify_user_button_by_name(user_name=user)
                Report.logInfo(f"Removing teammate with name: {user}")
                self.tune_pages.people_team_add_teammate.click_user_button_by_name(user_name=user,
                                                                                   match_case=True)
                self.tune_pages.people_team_add_teammate.verify_loader_not_visible()

            Report.logInfo("Leaving Add to teammates page")
            self.tune_pages.people_team_add_teammate.click_close_button()

            remaining_teammates = [teammate for teammate in randomly_selected_users_repr
                                   if teammate not in teammates_to_delete]

            Report.logInfo(f"Remaining teammates: {remaining_teammates}")

            Report.logInfo("Checking if teammates list has expected length")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list_length(remaining_teammates),
                log_pass="Visible teammates list has expected length",
                log_fail="Visible teammates list has not expected length"
            )

            Report.logInfo(f"Checking if every user is visible in All Teammates Page")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list(remaining_teammates),
                log_pass="Every added teammate is visible on teammates list",
                log_fail="Not every added teammate is visible on teammates list"
            )
        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_teammate_gets_new_booking(self, opposite_creds: Account):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]

            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email
            opposite_account_user_id = opposite_account.get('userId')

            Report.logInfo("Removing reservations for opposite user")
            self.sync_api_methods.delete_reservations_for_user(user_id=opposite_account_user_id)

            Report.logInfo(f"Adding opposite account: {opposite_account_repr} to teammate list")

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
            self.tune_pages.people_user.wait_for_refresh()
            Report.logInfo(f"Checking if user has no bookings in his list")
            self._assert(
                condition=self.tune_pages.people_user.verify_no_bookings_for_user(),
                log_fail="No upcoming bookings for user is not visible",
                log_pass="No upcoming bookings for user is visible as intended"
            )
            teammate_bookings = []
            teammate_bookings_number = random.randint(1, 5)
            for day_offset in range(teammate_bookings_number):
                booking_start_time = (datetime.now().replace(minute=0, second=0, microsecond=0) +
                                      timedelta(hours=1, days=day_offset))
                booking_duration = 120
                booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

                booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
                booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

                booking_date = booking_start_time.strftime(get_correct_time_format_based_on_system("%a, %b %_d"))

                booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                        user_id=opposite_account_user_id,
                                                                        org_id=self.org_id,
                                                                        start_time=booking_start_time,
                                                                        duration=booking_duration).json()
                Report.logResponse(repr(booking))
                Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")

                booking_id = booking['reservations'][0]['identifier']
                teammate_bookings.append({
                    "booking_id": booking_id,
                    "start": booking_start_time_tune,
                    "stop": booking_end_time_tune,
                    "date": "Today" if booking_start_time.day == datetime.now().day else booking_date
                })

            Report.logInfo("Refreshing User Page")
            self.tune_pages.people_user.click_refresh_button_and_wait_for_refresh()

            for booking_data in teammate_bookings:

                booking_date, booking_timestamps, booking_label = (
                    self.tune_pages.people_user.get_booking_data_by_booking_id(booking_data['booking_id']))
                Report.logInfo("Checking if Booking Date is valid")
                self._assert(
                    condition=booking_date == booking_data['date'],
                    log_pass="Correct date is visible on Teammate booking label",
                    log_fail=f"Not correct date is visible on Teammate booking label: "
                             f"{booking_date} != {booking_data['date']}"

                )

                Report.logInfo("Checking if Timestamps are valid")
                self._assert(
                    condition=booking_timestamps == f"{booking_data['start']} - {booking_data['stop']}",
                    log_pass="Correct timestamps are visible on Teammate booking label",
                    log_fail=f"Not correct timestamps are visible on Teammate booking label: "
                             f"{booking_timestamps} != {booking_data['start']} - {booking_data['stop']}"
                )

                Report.logInfo("Checking if Private booking label is visible")
                self._assert(
                    condition=booking_label == "Private booking",
                    log_pass="Private booking text is visible on Teammate booking label",
                    log_fail=f"Private booking text is not visible on Teammate booking label, "
                             f"{booking_label} is visible instead"
                )

            Report.logInfo("Changing booking visible desk setting to True")
            self._assert(
                condition=self.sync_api_methods.change_keep_bookings_visible(self.desk_id, True),
                log_pass="Booking visible setting successfully set to True",
                log_fail="Booking visible setting failed to set to True",
            )
            self.tune_pages.user_profile_page.wait_seconds_to_pass(15)
            Report.logInfo("Refreshing user profile")
            self.tune_pages.people_user.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Checking if Teammate Booking details are visible")

            for booking_data in teammate_bookings:
                _, _, booking_label = (
                    self.tune_pages.people_user.get_booking_data_by_booking_id(booking_data['booking_id']))

                label_condition = (self.building in booking_label
                                   and self.floor in booking_label
                                   and self.area in booking_label
                                   and self.desk_name in booking_label)

                self._assert(
                    condition=label_condition,
                    log_pass=f"All of the fields present in private booking label: {booking_label}",
                    log_fail=f"Not every of the field present in private booking label: {booking_label}"
                )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_book_next_to_teammate(self, opposite_creds: Account):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            Report.logInfo("Entering Everyone Tab Page")
            self.tune_pages.people.click_everyone_tab_button()

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

            Report.logInfo(f"Adding opposite account: {opposite_account_repr} to teammate list")

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
            self.tune_pages.people_user.wait_for_refresh()

            Report.logInfo(f"Checking if user has no bookings in his list")
            self._assert(
                condition=self.tune_pages.people_user.verify_no_bookings_for_user(),
                log_fail="No upcoming bookings for user is not visible",
                log_pass="No upcoming bookings for user is visible as intended"
            )
            teammate_bookings = []
            teammate_bookings_number = random.randint(1, 5)
            for day_offset in range(teammate_bookings_number):
                booking_start_time = (datetime.now().replace(minute=0, second=0, microsecond=0) +
                                      timedelta(hours=1, days=day_offset))
                booking_duration = 120
                booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

                booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
                booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

                booking_date = booking_start_time.strftime(get_correct_time_format_based_on_system("%a, %b %_d"))

                booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                        user_id=opposite_account_user_id,
                                                                        org_id=self.org_id,
                                                                        start_time=booking_start_time,
                                                                        duration=booking_duration).json()
                Report.logResponse(repr(booking))
                Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")

                booking_id = booking['reservations'][0]['identifier']
                teammate_bookings.append({
                    "start_date": booking_start_time,
                    "booking_id": booking_id,
                    "start": booking_start_time_tune,
                    "stop": booking_end_time_tune,
                    "date": "Today" if booking_start_time.day == datetime.now().day else booking_date
                })

            Report.logInfo("Refreshing User Page")
            self.tune_pages.people_user.click_refresh_button_and_wait_for_refresh()

            selected_booking = random.choice(teammate_bookings)

            start_date, booking_id, start, stop, date = selected_booking.values()

            Report.logInfo(f"Randomly selected booking to book next to is: {selected_booking}")

            Report.logInfo(f"Clicking on booking with data: {teammate_bookings}")
            self.tune_pages.people_user.click_booking_by_booking_id(booking_id)

            Report.logInfo(f"Collapsing desks from area: {self.area}")
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())

            selected_desk = random.choice(self.desk_sibling_name_list)
            Report.logInfo(f"Selecting desk randomly picked: {selected_desk}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(selected_desk)

            self.tune_pages.desk_booking.click_book_button()
            self.tune_pages.notify_teammates.click_skip_button()
            self.tune_pages.desk_successfully_booked.click_done_button()

            self.tune_pages.home.click_home_tab()

            Report.logInfo(f"Selecting day in calendar: {start}")
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(start_date)

            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()

            Report.logInfo("Checking if booking card is visible")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_displayed(),
                log_pass="Booking card is visible",
                log_fail="Booking card is not visible"
            )
            Report.logInfo(f"Checking if correct desk name: {selected_desk} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "desk_name", selected_desk,
                                                                            total_cards_number=1),
                log_fail=f"Desk name: {selected_desk} is not visible on Booking Card",
                log_pass=f"Desk name: {selected_desk} is visible on Booking Card"
            )

            Report.logInfo(f"Checking if correct location: {self.location} is visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "location_info", self.location,
                                                                            total_cards_number=1),
                log_fail=f"Location: {self.location} is not visible on Booking Card",
                log_pass=f"Location: {self.location} is visible on Booking Card"
            )

            timestamps = f"{start} - {stop}"

            Report.logInfo(f"Checking if correct timestamps: {timestamps} are visible on first booking card")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "timestamps", timestamps,
                                                                            total_cards_number=1),
                log_fail=f"Timestamp: {timestamps} is not visible on Booking Card",
                log_pass=f"Timestamp: {timestamps} is visible on Booking Card"
            )
            Report.logInfo(f"Checking if booking is highlighted with correct color")
            self._assert(
                condition=self.tune_pages.home.verify_booking_card_by_index(0, "color",
                                                                            self.tune_colors.color_future_today
                                                                            if date == "Today"
                                                                            else
                                                                            self.tune_colors.color_future_not_today,
                                                                            total_cards_number=1),
                log_fail=f"Booking card is not highlighted with correct color",
                log_pass=f"Booking card is highlighted with correct color"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_people_in_office_everyone_tab(self, opposite_creds: Account):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Clicking People in office button")
            self.tune_pages.home.click_teammates_in_office()
            Report.logInfo("Checking if No teammates in office label visible when no teammates for today")
            self._assert(
                condition=self.tune_pages.people_in_office.verify_no_teammates_in_office_label(),
                log_pass="No teammates in office visible when no teammates",
                log_fail="No teammates in office label not visible which is NOK"
            )
            Report.logInfo("Clicking Everyone Tab")
            self.tune_pages.people_in_office.click_everyone_tab()
            Report.logInfo("Clicking back to dashboard button")
            self.tune_pages.people_in_office.click_back_button()

            current_date = datetime.now()
            random_future_offset = random.randint(1, 4)
            random_future_date = current_date + timedelta(days=random_future_offset)
            random_future_date_formatted = random_future_date.strftime("%b, %d")

            Report.logInfo(f"Selecting future date in calendar {random_future_date_formatted}")
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(random_future_date)
            Report.logInfo("Clicking People in office button")
            self.tune_pages.home.click_teammates_in_office()
            Report.logInfo("Checking if No teammates in office label visible when no teammates for future date")
            self._assert(
                condition=self.tune_pages.people_in_office.verify_no_teammates_in_office_label(),
                log_pass="No teammates in office visible when no teammates",
                log_fail="No teammates in office label not visible which is NOK"
            )
            Report.logInfo("Clicking Everyone Tab")
            self.tune_pages.people_in_office.click_everyone_tab()
            Report.logInfo("Clicking back to dashboard button")
            self.tune_pages.people_in_office.click_back_button()

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

            Report.logInfo(f"Creating reservation for user {opposite_account_repr} for today "
                           f"and {random_future_date_formatted}")

            booking_duration = 120
            opposite_user_bookings = []

            for day in current_date, random_future_date:
                booking_start_time = day.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

                booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

                booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
                booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

                booking_date = booking_start_time.strftime(get_correct_time_format_based_on_system("%a, %b %_d"))

                booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                        user_id=opposite_account_user_id,
                                                                        org_id=self.org_id,
                                                                        start_time=booking_start_time,
                                                                        duration=booking_duration).json()
                Report.logResponse(repr(booking))
                Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")

                booking_id = booking['reservations'][0]['identifier']
                opposite_user_bookings.append({
                    "start_date": booking_start_time,
                    "booking_id": booking_id,
                    "start": booking_start_time_tune,
                    "stop": booking_end_time_tune,
                    "date": "Today" if booking_start_time.day == datetime.now().day else booking_date
                })

            for booking in opposite_user_bookings:
                Report.logInfo(f"Selecting date in calendar: {booking.get('date')}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(booking.get('start_date'))
                Report.logInfo("Entering People in office Page")
                self.tune_pages.home.click_teammates_in_office()
                Report.logInfo("Clicking everyone tab")
                self.tune_pages.people_in_office.click_everyone_tab()
                Report.logInfo("Checking if User with bookings visible")
                self._assert(
                    condition=self.tune_pages.people_in_office.verify_user_by_name_everyone(opposite_account_repr),
                    log_pass=f"User {opposite_account_repr} is visible",
                    log_fail=f"User {opposite_account_repr} is not visible"
                )
                booking_label = self.tune_pages.people_in_office.get_booking_data_by_user_id_everyone(opposite_account_user_id)
                booking_timestamps = f"{booking.get('start')} - {booking.get('stop')}"
                Report.logInfo(f"Checking if timestamps: {booking_timestamps} visible in booking")
                self._assert(
                    booking_timestamps in booking_label,
                    log_pass="Correct Timestamps visible in booking",
                    log_fail="Incorrect Timestamps in booking"
                )
                Report.logInfo(f"Checking if floor {self.floor} visible in booking")
                self._assert(
                    self.floor in booking_label,
                    log_pass=f"Floor {self.floor} visible in booking",
                    log_fail=f"Floor {self.floor} not visible in booking"
                )

                Report.logInfo(f"Checking if area {self.area} visible in booking")
                self._assert(
                    self.area in booking_label,
                    log_pass=f"Area {self.area} visible in booking",
                    log_fail=f"Area {self.area} not visible in booking"
                )

                Report.logInfo(f"Entering teammate profile: {opposite_account_repr}")
                self.tune_pages.people_in_office.click_user_by_name_everyone(opposite_account_repr)
                Report.logInfo(f"Verifying if booking for {booking.get('date')} is visible")
                self._assert(
                    condition=self.tune_pages.people_user.verify_booking_by_booking_id(booking.get('booking_id')),
                    log_pass="Booking is visible",
                    log_fail="Booking is not visible"
                )
                Report.logInfo(f"Clicking on the booking in User's profile")
                self.tune_pages.people_user.click_booking_by_booking_id(booking.get('booking_id'))
                Report.logInfo("Checking if booking next to teammate is possible")
                self._assert(
                    condition=self.tune_pages.desk_booking.verify_collapsable_desks_list(self.area.upper()),
                    log_pass="Booking page is visible with desk available",
                    log_fail="Booking page is not visible with desk available"
                )
                self.tune_pages.desk_booking.click_back_button()
                self.tune_pages.people_user.click_back_button()
                self.tune_pages.people_in_office.click_back_button()

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_people_in_office_teammates_tab(self, opposite_creds: Account):

        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Clicking People in office button")
            self.tune_pages.home.click_teammates_in_office()
            Report.logInfo("Checking if No teammates in office label visible when no teammates for today")
            self._assert(
                condition=self.tune_pages.people_in_office.verify_no_teammates_in_office_label(),
                log_pass="No teammates in office visible when no teammates",
                log_fail="No teammates in office label not visible which is NOK"
            )
            Report.logInfo("Clicking back to dashboard button")
            self.tune_pages.people_in_office.click_back_button()

            current_date = datetime.now()
            random_future_offset = random.randint(1, 4)
            random_future_date = current_date + timedelta(days=random_future_offset)
            random_future_date_formatted = random_future_date.strftime("%b, %d")

            Report.logInfo(f"Selecting future date in calendar {random_future_date_formatted}")
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(random_future_date)
            Report.logInfo("Clicking People in office button")
            self.tune_pages.home.click_teammates_in_office()
            Report.logInfo("Checking if No teammates in office label visible when no teammates for future date")
            self._assert(
                condition=self.tune_pages.people_in_office.verify_no_teammates_in_office_label(),
                log_pass="No teammates in office visible when no teammates",
                log_fail="No teammates in office label not visible which is NOK"
            )
            Report.logInfo("Clicking back to dashboard button")
            self.tune_pages.people_in_office.click_back_button()

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]

            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email
            opposite_account_user_id = opposite_account.get('userId')

            Report.logInfo("Removing reservations for opposite user")
            self.sync_api_methods.delete_reservations_for_user(user_id=opposite_account_user_id)

            Report.logInfo(f"Creating reservation for user {opposite_account_repr} for today "
                           f"and {random_future_date_formatted}")

            booking_duration = 120
            opposite_user_bookings = []

            for day in current_date, random_future_date:
                booking_start_time = day.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

                booking_end_time = booking_start_time + timedelta(minutes=booking_duration)

                booking_start_time_tune = tune_time_format_from_datetime_obj(booking_start_time)
                booking_end_time_tune = tune_time_format_from_datetime_obj(booking_end_time)

                booking_date = booking_start_time.strftime(get_correct_time_format_based_on_system("%a, %b %_d"))

                booking = self.sync_api_methods.create_booking_for_user(desk_id=self.desk_id,
                                                                        user_id=opposite_account_user_id,
                                                                        org_id=self.org_id,
                                                                        start_time=booking_start_time,
                                                                        duration=booking_duration).json()
                Report.logResponse(repr(booking))
                Report.logInfo(f"Booking for user {opposite_account_repr} created successfully")

                booking_id = booking['reservations'][0]['identifier']
                opposite_user_bookings.append({
                    "start_date": booking_start_time,
                    "booking_id": booking_id,
                    "start": booking_start_time_tune,
                    "stop": booking_end_time_tune,
                    "date": "Today" if booking_start_time.day == datetime.now().day else booking_date
                })

            Report.logInfo(f"Adding opposite account: {opposite_account_repr} to teammate list")

            self.tune_pages.home.click_people_tab()
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
            self.tune_pages.people_user.wait_for_refresh()
            self.tune_pages.people_user.click_back_button()
            self.tune_pages.home.click_home_tab()

            Report.logInfo("Changing booking visible desk setting to True")
            self._assert(
                condition=self.sync_api_methods.change_keep_bookings_visible(self.desk_id, True),
                log_pass="Booking visible setting successfully set to True",
                log_fail="Booking visible setting failed to set to True",
            )

            for booking in opposite_user_bookings:
                Report.logInfo(f"Selecting date in calendar: {booking.get('date')}")
                self.tune_pages.home.click_open_calendar_button()
                self.tune_pages.home.click_calendar_day_by_datetime(booking.get('start_date'))
                Report.logInfo("Entering People in office Page")
                self.tune_pages.home.click_teammates_in_office()
                Report.logInfo("Clicking Teammates tab")
                self.tune_pages.people_in_office.click_teammates_tab()
                Report.logInfo("Checking if User with bookings visible")
                self._assert(
                    condition=self.tune_pages.people_in_office.verify_user_by_name_teammates(opposite_account_repr),
                    log_pass=f"User {opposite_account_repr} is visible",
                    log_fail=f"User {opposite_account_repr} is not visible"
                )
                booking_label = self.tune_pages.people_in_office.get_booking_data_by_user_id_teammates(
                    opposite_account_user_id)
                booking_timestamps = f"{booking.get('start')} - {booking.get('stop')}"
                Report.logInfo(f"Checking if timestamps: {booking_timestamps} visible in booking")
                self._assert(
                    booking_timestamps in booking_label,
                    log_pass="Correct Timestamps visible in booking",
                    log_fail="Incorrect Timestamps in booking"
                )
                Report.logInfo(f"Checking if floor {self.floor} visible in booking")
                self._assert(
                    self.floor in booking_label,
                    log_pass=f"Floor {self.floor} visible in booking",
                    log_fail=f"Floor {self.floor} not visible in booking"
                )

                Report.logInfo(f"Checking if area {self.area} visible in booking")
                self._assert(
                    self.area in booking_label,
                    log_pass=f"Area {self.area} visible in booking",
                    log_fail=f"Area {self.area} not visible in booking"
                )

                Report.logInfo(f"Entering teammate profile: {opposite_account_repr}")
                self.tune_pages.people_in_office.click_user_by_name_teammates(opposite_account_repr)
                Report.logInfo(f"Verifying if booking for {booking.get('date')} is visible")
                self._assert(
                    condition=self.tune_pages.people_user.verify_booking_by_booking_id(booking.get('booking_id')),
                    log_pass="Booking is visible",
                    log_fail="Booking is not visible"
                )
                Report.logInfo(f"Clicking on the booking in User's profile")
                self.tune_pages.people_user.click_booking_by_booking_id(booking.get('booking_id'))
                Report.logInfo("Checking if booking next to teammate is possible")
                self._assert(
                    condition=self.tune_pages.desk_booking.verify_collapsable_desks_list(self.area.upper()),
                    log_pass="Booking page is visible with desk available",
                    log_fail="Booking page is not visible with desk available"
                )
                self.tune_pages.desk_booking.click_back_button()
                self.tune_pages.people_user.click_back_button()
                self.tune_pages.people_in_office.click_back_button()
                self.tune_pages.home.click_home_tab()

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")
