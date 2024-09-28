from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from apps.tune.base.desk_booking_base import Account
from apps.tune.TuneElectron import TuneElectron
from common.platform_helper import generate_random_string
from datetime import datetime, timedelta
from extentreport.report import Report
import random


class NotifyTeammatesScenarios(WorkAccountScenarios):

    def tc_notify_teammates_when_no_teams(self) -> None:
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
            self.tune_pages.people_team.click_back_button()
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            for user in randomly_selected_users_repr:
                Report.logInfo(f"Checking if user: {user} is visible in Notify Teammates list")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_teammate_visible(user),
                    log_pass=f"User {user} is visible as intended",
                    log_fail=f"User {user} is not visible"
                )
            Report.logInfo("Clicking Clear button if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            Report.logInfo("Checking if Skip Teammates button is visible")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_skip_button(),
                log_pass="Skip Teammates is visible as intended",
                log_fail="Skip teammates button not visible"
            )

            random_user = random.choice(randomly_selected_users_repr)
            Report.logInfo(f"Clicking on randomly selected user: {random_user}")
            self.tune_pages.notify_teammates.click_on_teammate_by_name(random_user)
            Report.logInfo(f"Checking if {random_user} user checkbox is selected")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_teammate_checkbox_in_status(random_user),
                log_pass=f"User: {random_user} is selected as intended",
                log_fail=f"User: {random_user} is not selected"
            )
            Report.logInfo(f"Checking if Notify Teammate button visible")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button(),
                log_pass=f"Notify button visible as intended",
                log_fail=f"Notify button not visible"
            )

            expected_one_teammate_text = "Notify teammate"

            Report.logInfo(f"Checking if Notify Teammate button has correct text: {expected_one_teammate_text}")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button_text(expected_one_teammate_text),
                log_pass=f"Button has correct text: {expected_one_teammate_text}",
                log_fail=f"Button has wrong text"
            )

            randomly_selected_users_repr.remove(random_user)
            next_random_users = random.sample(randomly_selected_users_repr,
                                              k=random.randint(1, len(randomly_selected_users_repr)))
            for usr in next_random_users:

                Report.logInfo(f"Clicking on randomly selected user: {usr}")
                self.tune_pages.notify_teammates.click_on_teammate_by_name(usr)

                Report.logInfo(f"Checking if {usr} user checkbox is selected")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_teammate_checkbox_in_status(usr),
                    log_pass=f"User: {usr} is selected as intended",
                    log_fail=f"User: {usr} is not selected"
                )

            Report.logInfo(f"Checking if Notify Teammate button visible")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button(),
                log_pass=f"Notify button visible as intended",
                log_fail=f"Notify button not visible"
            )

            expected_few_teammate_text = "Notify teammates"

            Report.logInfo(f"Checking if Notify Teammate button has correct text: {expected_few_teammate_text}")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button_text(expected_few_teammate_text),
                log_pass=f"Button has correct text: {expected_few_teammate_text}",
                log_fail=f"Button has wrong text"
            )

            expected_optional_message = "Notify with message"
            Report.logInfo(f"Checking if Notify Teammate button has correct text"
                           f"after filling optional message: {expected_optional_message}")
            self.tune_pages.notify_teammates.write_optional_message("test")
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button_text(expected_optional_message),
                log_pass=f"Button has correct text: {expected_optional_message}",
                log_fail=f"Button has wrong text"
            )

            Report.logInfo(f"Checking if Notify Teammate button has correct text"
                           f"after deleting optional message: {expected_few_teammate_text}")
            self.tune_pages.notify_teammates.clear_optional_message()
            expected_no_optional_message = "Notify teammates"
            self._assert(
                condition=self.tune_pages.notify_teammates.verify_notify_button_text(expected_no_optional_message),
                log_pass=f"Button has correct text: {expected_no_optional_message}",
                log_fail=f"Button has wrong text"
            )
        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notify_teammates_when_teams_created(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            users_repr = []
            for user in filtered_end_users:
                if user.get('name'):
                    users_repr.append(user['name'])
                else:
                    users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {users_repr}")

            teams_created = []

            for _ in range(team_to_create_number):
                self.tune_pages.people.click_new_team_button()

                team_name = generate_random_string(team_name_length)

                Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

                Report.logInfo(f"Typing generated string into team name input")
                self.tune_pages.people.input_team_name(team_name)
                Report.logInfo("Clicking CREATE button")
                self.tune_pages.people.click_create_team_button()
                self.tune_pages.people.wait_for_team_creation()
                Report.logInfo("Clicking Back to Teammates List People Page")
                self.tune_pages.people_team.click_add_teammates_button()

                users = []

                random_users_number = random.randint(2, 5)
                randomly_selected_users_repr = random.sample(users_repr, random_users_number)
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
                    users.append(user)

                teams_created.append({'name': team_name,
                                      'users': users})
                self.tune_pages.people_team_add_teammate.click_close_button()
                self.tune_pages.people_team.click_back_button()

            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            for team in teams_created:
                team_name = team.get('name')
                Report.logInfo(f"Checking if team {team_name} visible")
                self._assert(
                    condition=self.tune_pages.notify_teammates.verify_team_by_name(team_name),
                    log_pass=f"Team with name: {team_name}",
                    log_fail=f"Team with name: {team_name} not  visible"
                )

                Report.logInfo(f"Checking if team {team_name} checkbox is unchecked")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(team_name,
                                                                                                'unchecked'),
                    log_pass=f"Team with name: {team_name} check status is unchecked, OK",
                    log_fail=f"Team with name: {team_name} wrong check status"
                )

            Report.logInfo(f"Selecting team for all teammates selection")
            all_teammates_team = random.choice(teams_created)
            teams_created.remove(all_teammates_team)
            Report.logInfo(f"Team selected for all teammates choice: {all_teammates_team}")
            Report.logInfo(f"Selecting every teammate in team: {all_teammates_team}")
            all_teammates_team_name = all_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(all_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            all_teammates_team_members = all_teammates_team.get('users')

            for member in all_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Selecting team for teammates partial selection")
            partial_teammates_team = random.choice(teams_created)
            teams_created.remove(partial_teammates_team)
            Report.logInfo(f"Team selected for partial selection choice: {partial_teammates_team}")
            partial_teammates_team_name = partial_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(partial_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            partial_teammates_team_all_users = partial_teammates_team.get('users')
            partial_teammates_team_members = random.sample(partial_teammates_team_all_users,
                                                           k=len(partial_teammates_team_all_users) - 1)

            for member in partial_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notify_teammates_selection_persistency_in_other_bookings(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            users_repr = []
            for user in filtered_end_users:
                if user.get('name'):
                    users_repr.append(user['name'])
                else:
                    users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {users_repr}")

            teams_created = []

            for _ in range(team_to_create_number):
                self.tune_pages.people.click_new_team_button()

                team_name = generate_random_string(team_name_length)

                Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

                Report.logInfo(f"Typing generated string into team name input")
                self.tune_pages.people.input_team_name(team_name)
                Report.logInfo("Clicking CREATE button")
                self.tune_pages.people.click_create_team_button()
                self.tune_pages.people.wait_for_team_creation()
                Report.logInfo("Clicking Back to Teammates List People Page")
                self.tune_pages.people_team.click_add_teammates_button()

                users = []

                random_users_number = random.randint(2, 5)
                randomly_selected_users_repr = random.sample(users_repr, random_users_number)
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
                    users.append(user)

                teams_created.append({'name': team_name,
                                      'users': users})
                self.tune_pages.people_team_add_teammate.click_close_button()
                self.tune_pages.people_team.click_back_button()

            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            for team in teams_created:
                team_name = team.get('name')
                Report.logInfo(f"Checking if team {team_name} visible")
                self._assert(
                    condition=self.tune_pages.notify_teammates.verify_team_by_name(team_name),
                    log_pass=f"Team with name: {team_name}",
                    log_fail=f"Team with name: {team_name} not  visible"
                )

                Report.logInfo(f"Checking if team {team_name} checkbox is unchecked")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(team_name,
                                                                                                'unchecked'),
                    log_pass=f"Team with name: {team_name} check status is unchecked, OK",
                    log_fail=f"Team with name: {team_name} wrong check status"
                )

            Report.logInfo(f"Selecting team for all teammates selection")
            all_teammates_team = random.choice(teams_created)
            teams_created.remove(all_teammates_team)
            Report.logInfo(f"Team selected for all teammates choice: {all_teammates_team}")
            Report.logInfo(f"Selecting every teammate in team: {all_teammates_team}")
            all_teammates_team_name = all_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(all_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            all_teammates_team_members = all_teammates_team.get('users')

            for member in all_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Selecting team for teammates partial selection")
            partial_teammates_team = random.choice(teams_created)
            teams_created.remove(partial_teammates_team)
            Report.logInfo(f"Team selected for partial selection choice: {partial_teammates_team}")
            partial_teammates_team_name = partial_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(partial_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            partial_teammates_team_all_users = partial_teammates_team.get('users')
            partial_teammates_team_members = random.sample(partial_teammates_team_all_users,
                                                           k=len(partial_teammates_team_all_users) - 1)

            for member in partial_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )
            Report.logInfo("Clicking Notify Teammates button")
            self.tune_pages.notify_teammates.click_notify_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Creating another booking for other day and checking if the selection is persisting")
            self.tune_pages.home.click_open_calendar_button()
            self.tune_pages.home.click_calendar_day_by_datetime(datetime.now() + timedelta(days=1))
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Checking selection in other booking")
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notify_teammates_selection_persistency_after_relaunch(self) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            users_repr = []
            for user in filtered_end_users:
                if user.get('name'):
                    users_repr.append(user['name'])
                else:
                    users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {users_repr}")

            teams_created = []

            for _ in range(team_to_create_number):
                self.tune_pages.people.click_new_team_button()

                team_name = generate_random_string(team_name_length)

                Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

                Report.logInfo(f"Typing generated string into team name input")
                self.tune_pages.people.input_team_name(team_name)
                Report.logInfo("Clicking CREATE button")
                self.tune_pages.people.click_create_team_button()
                self.tune_pages.people.wait_for_team_creation()
                Report.logInfo("Clicking Back to Teammates List People Page")
                self.tune_pages.people_team.click_add_teammates_button()

                users = []

                random_users_number = random.randint(2, 5)
                randomly_selected_users_repr = random.sample(users_repr, random_users_number)
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
                    users.append(user)

                teams_created.append({'name': team_name,
                                      'users': users})
                self.tune_pages.people_team_add_teammate.click_close_button()
                self.tune_pages.people_team.click_back_button()

            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            for team in teams_created:
                team_name = team.get('name')
                Report.logInfo(f"Checking if team {team_name} visible")
                self._assert(
                    condition=self.tune_pages.notify_teammates.verify_team_by_name(team_name),
                    log_pass=f"Team with name: {team_name}",
                    log_fail=f"Team with name: {team_name} not  visible"
                )

                Report.logInfo(f"Checking if team {team_name} checkbox is unchecked")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(team_name,
                                                                                                'unchecked'),
                    log_pass=f"Team with name: {team_name} check status is unchecked, OK",
                    log_fail=f"Team with name: {team_name} wrong check status"
                )

            Report.logInfo(f"Selecting team for all teammates selection")
            all_teammates_team = random.choice(teams_created)
            teams_created.remove(all_teammates_team)
            Report.logInfo(f"Team selected for all teammates choice: {all_teammates_team}")
            Report.logInfo(f"Selecting every teammate in team: {all_teammates_team}")
            all_teammates_team_name = all_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(all_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            all_teammates_team_members = all_teammates_team.get('users')

            for member in all_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Selecting team for teammates partial selection")
            partial_teammates_team = random.choice(teams_created)
            teams_created.remove(partial_teammates_team)
            Report.logInfo(f"Team selected for partial selection choice: {partial_teammates_team}")
            partial_teammates_team_name = partial_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(partial_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            partial_teammates_team_all_users = partial_teammates_team.get('users')
            partial_teammates_team_members = random.sample(partial_teammates_team_all_users,
                                                           k=len(partial_teammates_team_all_users) - 1)

            for member in partial_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )
            Report.logInfo("Clicking Notify Teammates button")
            self.tune_pages.notify_teammates.click_notify_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Canceling previously created booking")
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_booking_details_button()
            self.tune_pages.home.click_end_booking_button()
            self.tune_pages.home.click_end_booking_confirm_yes_button()
            self.tune_pages.home.click_booking_cancelled_ok_button()
            Report.logInfo("Closing Logi Tune")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_quit()
            tune_app = TuneElectron()
            Report.logInfo("Opening Logi Tune")
            tune_app.open_tune_app()
            Report.logInfo("Creating booking after Logi Tune restart")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Checking selection in other booking")
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")

    def tc_notify_teammates_selection_persistency_after_relog(self, credentials: Account) -> None:
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

            filtered_end_users = [user for user in self.org_end_users if user.get('email') != self.logged_user_email]

            users_repr = []
            for user in filtered_end_users:
                if user.get('name'):
                    users_repr.append(user['name'])
                else:
                    users_repr.append(user['email'])

            Report.logInfo(f"Randomly selected users list: {users_repr}")

            teams_created = []

            for _ in range(team_to_create_number):
                self.tune_pages.people.click_new_team_button()

                team_name = generate_random_string(team_name_length)

                Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

                Report.logInfo(f"Typing generated string into team name input")
                self.tune_pages.people.input_team_name(team_name)
                Report.logInfo("Clicking CREATE button")
                self.tune_pages.people.click_create_team_button()
                self.tune_pages.people.wait_for_team_creation()
                Report.logInfo("Clicking Back to Teammates List People Page")
                self.tune_pages.people_team.click_add_teammates_button()

                users = []

                random_users_number = random.randint(2, 5)
                randomly_selected_users_repr = random.sample(users_repr, random_users_number)
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
                    users.append(user)

                teams_created.append({'name': team_name,
                                      'users': users})
                self.tune_pages.people_team_add_teammate.click_close_button()
                self.tune_pages.people_team.click_back_button()

            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()
            for team in teams_created:
                team_name = team.get('name')
                Report.logInfo(f"Checking if team {team_name} visible")
                self._assert(
                    condition=self.tune_pages.notify_teammates.verify_team_by_name(team_name),
                    log_pass=f"Team with name: {team_name}",
                    log_fail=f"Team with name: {team_name} not  visible"
                )

                Report.logInfo(f"Checking if team {team_name} checkbox is unchecked")
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(team_name,
                                                                                                'unchecked'),
                    log_pass=f"Team with name: {team_name} check status is unchecked, OK",
                    log_fail=f"Team with name: {team_name} wrong check status"
                )

            Report.logInfo(f"Selecting team for all teammates selection")
            all_teammates_team = random.choice(teams_created)
            teams_created.remove(all_teammates_team)
            Report.logInfo(f"Team selected for all teammates choice: {all_teammates_team}")
            Report.logInfo(f"Selecting every teammate in team: {all_teammates_team}")
            all_teammates_team_name = all_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(all_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            all_teammates_team_members = all_teammates_team.get('users')

            for member in all_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Selecting team for teammates partial selection")
            partial_teammates_team = random.choice(teams_created)
            teams_created.remove(partial_teammates_team)
            Report.logInfo(f"Team selected for partial selection choice: {partial_teammates_team}")
            partial_teammates_team_name = partial_teammates_team.get('name')
            self.tune_pages.notify_teammates.click_on_team_by_name(partial_teammates_team_name)
            Report.logInfo("Clicking clear if visible")
            if self.tune_pages.notify_teammates.verify_clear_button():
                self.tune_pages.notify_teammates.click_clear_button()

            partial_teammates_team_all_users = partial_teammates_team.get('users')
            partial_teammates_team_members = random.sample(partial_teammates_team_all_users,
                                                           k=len(partial_teammates_team_all_users) - 1)

            for member in partial_teammates_team_members:
                self.tune_pages.notify_teammates.click_on_teammate_by_name(member)

            self.tune_pages.notify_teammates.click_close_team()
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )

            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )
            Report.logInfo("Clicking Notify Teammates button")
            self.tune_pages.notify_teammates.click_notify_button()
            self.tune_pages.desk_successfully_booked.click_done_button()
            Report.logInfo("Canceling previously created booking")
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_booking_details_button()
            self.tune_pages.home.click_end_booking_button()
            self.tune_pages.home.click_end_booking_confirm_yes_button()
            self.tune_pages.home.click_booking_cancelled_ok_button()
            Report.logInfo("Disconnecting Logi Tune Account")
            self.disconnect_connected_account_if_needed()
            Report.logInfo("Checking if user not logged")
            self._assert(
                condition=self.tune_pages.home.verify_sign_in_button_displayed(),
                log_pass="User disconnected, OK",
                log_fail="User not disconnected, NOK"
            )
            Report.logInfo(f"Connecting to Work Account: {credentials.credentials.signin_payload.email}")
            self.connect_to_work_account_if_not_logged(**credentials)
            Report.logInfo("Creating booking after reconnecting Logi Tune Account")
            self.tune_pages.home.click_book_a_desk_button()
            self.tune_pages.home.click_by_location_and_preferences_button()

            Report.logInfo(f"Selecting floor: {self.floor}")
            self.tune_pages.desk_booking.click_book_a_desk_floor_location_button()
            self.tune_pages.desk_booking.select_floor_by_text(self.floor)
            self.tune_pages.home.wait_for_page_reload()
            self.tune_pages.desk_booking.click_collapsable_desks_list(self.area.upper())
            Report.logInfo(f"Selecting desk with name: {self.desk_name}")
            self.tune_pages.desk_booking.click_desk_by_desk_name(self.desk_name)
            self.tune_pages.desk_booking.click_book_button()
            Report.logInfo("Checking selection in other booking")
            Report.logInfo(f"Checking if team {all_teammates_team_name} checkbox is checked")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(all_teammates_team_name,
                                                                                            'checked'),
                log_pass=f"Team with name: {all_teammates_team_name} check status is checked, OK",
                log_fail=f"Team with name: {all_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if team {partial_teammates_team_name} checkbox is indeterminate")
            self._assert(
                condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(partial_teammates_team_name,
                                                                                            'indeterminate'),
                log_pass=f"Team with name: {partial_teammates_team_name} check status is indeterminate, OK",
                log_fail=f"Team with name: {partial_teammates_team_name} wrong check status"
            )
            Report.logInfo(f"Checking if remaining teams checkbox is unchecked")
            for team in teams_created:
                name = team.get('name')
                self._assert(
                    condition=self.tune_pages.notify_teammates.check_if_team_checkbox_in_status(name, 'unchecked'),
                    log_pass=f"Team with name: {name} check status is unchecked, OK",
                    log_fail=f"Team with name: {name} wrong check status"
                )

        except Exception as e:
            Report.logException(f"During test exception occured: {repr(e)}")