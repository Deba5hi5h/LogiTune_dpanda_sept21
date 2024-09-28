import random

from apps.tune.base.desk_booking_base import Account
from apps.tune.tc_scenarios.base_scenarios import WorkAccountScenarios
from extentreport.report import Report
from common.platform_helper import generate_random_string


class TeamCreationScenarios(WorkAccountScenarios):

    def tc_create_team_input_team_name_check(self):
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            self.tune_pages.people.click_new_team_button()

            max_allowed_chars = 30

            max_allowed_random = generate_random_string(max_allowed_chars)

            Report.logInfo(f"Generated random string with {max_allowed_chars}: {max_allowed_random}")

            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(max_allowed_random)
            Report.logInfo("Checking if Create button is enabled")
            self._assert(
                condition=self.tune_pages.people.verify_create_team_button_enabled(),
                log_pass="Create team button is enabled as intended",
                log_fail="Create team button is disabled which is NOK"
            )

            min_not_allowed_random = generate_random_string(max_allowed_chars + 1)

            Report.logInfo(f"Generated random not allowed: {min_not_allowed_random}")
            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(min_not_allowed_random)
            Report.logInfo("Checking if Create button is not enabled")
            self._assert(
                condition=self.tune_pages.people.verify_create_team_button_enabled() is False,
                log_pass="Create team button is disabled as intended",
                log_fail="Create team button is enabled which is NOK"
            )
            max_len_exceeded_text = "The character limit has been exceeded"
            Report.logInfo(f"Checking if text: {max_len_exceeded_text} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(max_len_exceeded_text),
                log_pass=f"Alert {max_len_exceeded_text} is visible",
                log_fail=f"Alert {max_len_exceeded_text} is not visible"
            )
            empty_field_text = "The field cannot be left empty"
            Report.logInfo(f"Clearing Team Name input")
            self.tune_pages.people.clear_input_team_name()
            Report.logInfo("Checking if Create button is not enabled")
            self._assert(
                condition=self.tune_pages.people.verify_create_team_button_enabled() is False,
                log_pass="Create team button is disabled as intended",
                log_fail="Create team button is enabled which is NOK"
            )
            Report.logInfo(f"Checking if text: {empty_field_text} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(empty_field_text),
                log_pass=f"Alert {empty_field_text} is visible",
                log_fail=f"Alert {empty_field_text} is not visible"
            )
            Report.logInfo("Entering special characters and checking if not allowed")
            special_chars_string = "/%&{}"
            self.tune_pages.people.input_team_name(special_chars_string)
            chars_alert = f"Character {' '.join(list(special_chars_string))} are not allowed"

            Report.logInfo("Checking if Create button is not enabled")
            self._assert(
                condition=self.tune_pages.people.verify_create_team_button_enabled() is False,
                log_pass="Create team button is disabled as intended",
                log_fail="Create team button is enabled which is NOK"
            )

            Report.logInfo(f"Checking if text: {chars_alert} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(chars_alert),
                log_pass=f"Alert {chars_alert} is visible",
                log_fail=f"Alert {chars_alert} is not visible"
            )
            Report.logInfo("Checking if create two teams with same name is not possible")
            Report.logInfo(f"Creating team with name: {max_allowed_random}")
            self.tune_pages.people.input_team_name(max_allowed_random)
            Report.logInfo("Clicking CREATE button")
            self.tune_pages.people.click_create_team_button()
            self.tune_pages.people.wait_for_team_creation()
            Report.logInfo("Clicking Back to Teammates List People Page")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo(f"Checking if team {max_allowed_random} is visible")
            Report.logInfo(f"Attempting to create second team with same name: {max_allowed_random}")
            self.tune_pages.people.click_new_team_button()
            self.tune_pages.people.input_team_name(max_allowed_random)
            Report.logInfo("Checking if Create button is not enabled")
            self._assert(
                condition=self.tune_pages.people.verify_create_team_button_enabled() is False,
                log_pass="Create team button is disabled as intended",
                log_fail="Create team button is enabled which is NOK"
            )
            already_exists_alert = "Name already exists"
            Report.logInfo(f"Checking if text: {already_exists_alert} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(already_exists_alert),
                log_pass=f"Alert {already_exists_alert} is visible",
                log_fail=f"Alert {already_exists_alert} is not visible"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

        finally:
            self.tune_pages.people.click_close_create_team_button()

    def tc_edit_team_input_team_name_check(self):
        try:

            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            self.tune_pages.people.click_new_team_button()
            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_name = generate_random_string(team_name_length)

            Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(team_name)
            Report.logInfo("Clicking CREATE button")
            self.tune_pages.people.click_create_team_button()
            self.tune_pages.people.wait_for_team_creation()
            Report.logInfo("Clicking Back to Teammates List People Page")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo(f"Entering created team: {team_name} Page")
            self.tune_pages.people.click_team_button_by_team_name(team_name)
            Report.logInfo("Clicking Edit Button")
            self.tune_pages.people_team.click_edit_button()
            Report.logInfo("Clicking Edit Name Button")
            self.tune_pages.people_team_edit.click_edit_team_name_button()

            min_not_allowed_random = generate_random_string(max_allowed_chars + 1)

            Report.logInfo(f"Generated random not allowed: {min_not_allowed_random}")
            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(min_not_allowed_random)
            Report.logInfo("Checking if Update button is not enabled")
            self._assert(
                condition=self.tune_pages.people_team_edit.verify_update_team_button_enabled() is False,
                log_pass="Update team button is disabled as intended",
                log_fail="Update team button is enabled which is NOK"
            )
            max_len_exceeded_text = "The character limit has been exceeded"
            Report.logInfo(f"Checking if text: {max_len_exceeded_text} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(max_len_exceeded_text),
                log_pass=f"Alert {max_len_exceeded_text} is visible",
                log_fail=f"Alert {max_len_exceeded_text} is not visible"
            )
            empty_field_text = "The field cannot be left empty"
            Report.logInfo(f"Clearing Team Name input")
            self.tune_pages.people.clear_input_team_name()
            Report.logInfo("Checking if Update button is not enabled")
            self._assert(
                condition=self.tune_pages.people_team_edit.verify_update_team_button_enabled() is False,
                log_pass="Update team button is disabled as intended",
                log_fail="Update team button is enabled which is NOK"
            )
            Report.logInfo(f"Checking if text: {empty_field_text} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(empty_field_text),
                log_pass=f"Alert {empty_field_text} is visible",
                log_fail=f"Alert {empty_field_text} is not visible"
            )
            Report.logInfo("Entering special characters and checking if not allowed")
            special_chars_string = "/%&{}"
            self.tune_pages.people.input_team_name(special_chars_string)
            chars_alert = f"Character {' '.join(list(special_chars_string))} are not allowed"

            Report.logInfo("Checking if Update button is not enabled")
            self._assert(
                condition=self.tune_pages.people_team_edit.verify_update_team_button_enabled() is False,
                log_pass="Update team button is disabled as intended",
                log_fail="Update team button is enabled which is NOK"
            )

            Report.logInfo(f"Checking if text: {chars_alert} is visible")

            self._assert(
                condition=self.tune_pages.people.verify_input_alert(chars_alert),
                log_pass=f"Alert {chars_alert} is visible",
                log_fail=f"Alert {chars_alert} is not visible"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_edit_team_team_delete(self):
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo("Clicking New Team Button")
            self.tune_pages.people.click_new_team_button()
            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_name = generate_random_string(team_name_length)

            Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(team_name)
            Report.logInfo("Clicking CREATE button")
            self.tune_pages.people.click_create_team_button()
            self.tune_pages.people.wait_for_team_creation()
            Report.logInfo("Clicking Back to Teammates List People Page")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo(f"Checking if team {team_name} has been created")
            self._assert(
                condition=self.tune_pages.people.verify_team_by_team_name(team_name),
                log_pass=f"Team {team_name} has been created with success",
                log_fail=f"Team {team_name} not created"
            )
            Report.logInfo(f"Entering created team: {team_name} Page")
            self.tune_pages.people.click_team_button_by_team_name(team_name)
            Report.logInfo("Clicking Edit Button")
            self.tune_pages.people_team.click_edit_button()
            Report.logInfo("Clicking Delete Button")
            self.tune_pages.people_team_edit.click_delete_team_button()
            Report.logInfo("Clicking Cancel Button")
            self.tune_pages.people_team_edit.click_popup_delete_team_cancel_button()
            Report.logInfo("Clicking Delete Button")
            self.tune_pages.people_team_edit.click_delete_team_button()
            Report.logInfo("Clicking Cancel Button Again")
            self.tune_pages.people_team_edit.click_popup_delete_team_delete_button()
            self.tune_pages.people_team_edit.wait_for_team_to_be_deleted()
            Report.logInfo("Checking if removed team is not visible in People-> Teammates Page")
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self._assert(
                condition=self.tune_pages.people.verify_team_not_visible_by_team_name(team_name),
                log_pass=f"Previously removed team: {team_name} is not visible as intended",
                log_fail=f"Previously removed team: {team_name} is visible which is NOK",
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_custom_team_teammate_add(self, opposite_creds: Account):
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

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
                self.tune_pages.people_team.click_back_button()
                teams_created.append(team_name)

            Report.logInfo("Checking if created teams are visible in Tune")
            for team in teams_created:
                Report.logInfo(f"Checking if team {team} is visible")
                self._assert(
                    condition=self.tune_pages.people.verify_team_by_team_name(team),
                    log_pass=f"Team with name {team} is visible in Tune",
                    log_fail=f"Team with name {team} is not visible in Tune"
                )

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]

            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email

            Report.logInfo(f"Entering Everyone Tab")
            self.tune_pages.people.click_everyone_tab_button()
            if self.tune_pages.people.verify_user_group_visible_by_name('Default'):
                self.tune_pages.people.click_user_group_visible_by_name('Default')

            Report.logInfo(f"Adding opposite account: {opposite_account_repr} to teammate list")

            Report.logInfo(f"Searching for user {opposite_account_repr}")
            Report.logInfo(f"Typing '{opposite_account_repr}' in the search input")
            self.tune_pages.people.input_everyone_search_bar(opposite_account_repr)
            self.tune_pages.people.wait_search_to_load()
            Report.logInfo(f"Entering profile for user: {opposite_account_repr}")
            self.tune_pages.people.click_user_from_everyone_tab_by_name(opposite_account_repr, match_case=True)
            Report.logInfo(f"Adding user: {opposite_account_repr} to teammates list")
            self.tune_pages.people_user.click_add_to_teammates_button()
            self.tune_pages.home.wait_for_page_reload()
            Report.logInfo("Entering Manage Teams Page")
            self.tune_pages.people_user.click_manage_teams_button()
            for team in teams_created:
                Report.logInfo(f"Adding user to team: {team}")
                self.tune_pages.people_user_manage_teams.click_team_action_button_for_team_with_name(team)
                self.tune_pages.home.wait_for_page_reload()
            Report.logInfo("Exiting Manage Teams Page")
            self.tune_pages.people_user_manage_teams.click_done_button()
            Report.logInfo("Checking if User's current teams number is correct")
            teams_number = len(teams_created)
            self._assert(
                condition=self.tune_pages.people_user.verify_user_teams_number(teams_number),
                log_pass=f"Current user's teams number is: {teams_number} which is OK",
                log_fail=f"Current user's teams number is NOK"
            )
            Report.logInfo("Exiting User Profile Page")
            self.tune_pages.people_user.click_back_button()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            Report.logInfo("Click Teammates Tab button")
            self.tune_pages.people.click_teammates_tab_button()
            for team in teams_created:
                self.tune_pages.home.wait_for_page_reload()
                Report.logInfo(f"Entering Team Named: {team}")
                self.tune_pages.people.click_team_button_by_team_name(team)
                Report.logInfo(f"Checking if {opposite_account_repr} is visible in team")
                self._assert(
                    condition=self.tune_pages.people_team.verify_teammate_by_name(opposite_account_repr),
                    log_pass=f"Teammate: {opposite_account_repr} visible in team: {team}",
                    log_fail=f"Teammate: {opposite_account_repr} not visible in team {team}"
                )
                Report.logInfo("Clicking back to dashboard button")
                self.tune_pages.people_team.click_back_button()
            Report.logInfo("Entering All Teammates Page")
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo(f"Checking if {opposite_account_repr} is visible in All Teammates Page")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammate_by_name(opposite_account_repr),
                log_pass=f"Teammate: {opposite_account_repr} visible in All Teammates",
                log_fail=f"Teammate: {opposite_account_repr} not visible in All Teammates"
            )
            Report.logInfo("Checking if All Teammates contains only 1 Teammate as intended")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammates_list_length([opposite_account_repr]),
                log_pass=f"All Teammates list contains only 1 Teammate as intended",
                log_fail=f"All Teammates list length is NOK"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def tc_custom_team_teammate_remove(self, opposite_creds: Account):
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            team_to_create_number = random.randint(3, 5)

            teams_created = []

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]
            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email

            for _ in range(team_to_create_number):
                self.tune_pages.people.click_new_team_button()

                team_name = generate_random_string(team_name_length)

                Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

                Report.logInfo(f"Typing generated string into team name input")
                self.tune_pages.people.input_team_name(team_name)
                Report.logInfo("Clicking CREATE button")
                self.tune_pages.people.click_create_team_button()
                self.tune_pages.people.wait_for_team_creation()
                Report.logInfo("Clicking Add Teammates Button")
                self.tune_pages.people_team.click_add_teammates_button()
                Report.logInfo(f"Searching for teammate:  {opposite_account_repr}")
                self.tune_pages.people_team_add_teammate.input_search_bar(opposite_account_repr)
                Report.logInfo("Clicking Add Button")
                self.tune_pages.people_team_add_teammate.click_user_button_by_name(opposite_account_repr,
                                                                                   match_case=True)
                self.tune_pages.people_team_add_teammate.verify_loader_not_visible()
                Report.logInfo("Exiting Add Teammates Page")
                self.tune_pages.people_team_add_teammate.click_close_button()

                Report.logInfo("Clicking Back to Teammates List People Page")
                self.tune_pages.people_team.click_back_button()
                teams_created.append(team_name)

            Report.logInfo("Checking if created teams are visible in Tune")
            for team in teams_created:
                Report.logInfo(f"Checking if team {team} is visible")
                self._assert(
                    condition=self.tune_pages.people.verify_team_by_team_name(team),
                    log_pass=f"Team with name {team} is visible in Tune",
                    log_fail=f"Team with name {team} is not visible in Tune"
                )
            Report.logInfo("Entering All Teammates Page")
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo(f"Entering Teammate profile: {opposite_account_repr}")
            self.tune_pages.people_team.click_user_button_by_name(opposite_account_repr)
            Report.logInfo(f"Clicking Manage Teams Button for user: {opposite_account_repr}")
            self.tune_pages.people_user.click_manage_teams_button()
            teams_to_remove = random.sample(teams_created, k=random.randint(1, team_to_create_number - 1))
            remaining_teams = set(teams_created).difference(set(teams_to_remove))
            Report.logInfo(f"Randomly selected teams to remove: {teams_to_remove}")
            for team in teams_to_remove:
                self.tune_pages.people_user_manage_teams.click_team_action_button_for_team_with_name(team)
                self.tune_pages.home.wait_for_page_reload()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.people_user_manage_teams.click_done_button()
            remaining_teams_len = len(remaining_teams)
            Report.logInfo(f"Checking if user's teams number is OK: {remaining_teams_len}")
            self._assert(
                condition=self.tune_pages.people_user.verify_user_teams_number(remaining_teams_len),
                log_pass=f"User's remaining teams number: {remaining_teams_len} which is OK",
                log_fail="User's remaining teams NOK"
            )
            Report.logInfo("Clicking back to All Teammates button")
            self.tune_pages.people_user.click_back_button()
            Report.logInfo("Clicking back to Dashboard button")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo("Click Teammates Tab button")
            self.tune_pages.people.click_teammates_tab_button()
            for team in remaining_teams:
                Report.logInfo(f"Entering remaining team {team}")
                self.tune_pages.people.click_team_button_by_team_name(team)
                Report.logInfo(f"Checking if {opposite_account_repr} visible in team {team}")
                self._assert(
                    condition=self.tune_pages.people_team.verify_teammate_by_name(opposite_account_repr),
                    log_pass=f"{opposite_account_repr} visible in team {team}",
                    log_fail=f"{opposite_account_repr} not visible in team {team}"
                )
                self.tune_pages.people_team.click_back_button()

            Report.logInfo("Entering All Teammates Page")
            self.tune_pages.people.click_all_teammates_button()
            Report.logInfo(f"Entering Teammate profile: {opposite_account_repr}")
            self.tune_pages.people_team.click_user_button_by_name(opposite_account_repr)
            Report.logInfo(f"Clicking Manage Teams Button for user: {opposite_account_repr}")
            self.tune_pages.people_user.click_manage_teams_button()
            Report.logInfo(f"Removing remaining teams for user: {remaining_teams}")
            for team in remaining_teams:
                self.tune_pages.people_user_manage_teams.click_team_action_button_for_team_with_name(team)
                self.tune_pages.home.wait_for_page_reload()
            Report.logInfo("Clicking Done Button")
            self.tune_pages.people_user_manage_teams.click_done_button()
            Report.logInfo(f"Checking if user's teams number is OK: 0")
            self._assert(
                condition=self.tune_pages.people_user.verify_user_teams_number(0),
                log_pass=f"User's remaining teams number: 0 which is OK",
                log_fail="User's remaining teams NOK"
            )
            Report.logInfo("Clicking back to All Teammates button")
            self.tune_pages.people_user.click_back_button()
            Report.logInfo("Clicking back to Dashboard button")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo("Checking if user is not visible in any created custom team team")
            Report.logInfo("Click Teammates Tab button")
            self.tune_pages.people.click_teammates_tab_button()
            for team in teams_created:
                Report.logInfo(f"Entering remaining team {team}")
                self.tune_pages.people.click_team_button_by_team_name(team)
                Report.logInfo(f"Checking if {opposite_account_repr} is not visible in team {team}")
                self._assert(
                    condition=self.tune_pages.people_team.verify_teammate_not_visible_by_name(opposite_account_repr),
                    log_pass=f"{opposite_account_repr} not visible in team {team}",
                    log_fail=f"{opposite_account_repr} visible in team {team}"
                )
                self.tune_pages.people_team.click_back_button()
        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

    def custom_team_create_team_from_manage_teams_page(self, opposite_creds: Account):
        try:
            self.tune_pages.home.click_home_tab()
            self.tune_pages.home.click_refresh_button_and_wait_for_refresh()
            self.tune_pages.home.click_people_tab()
            self.tune_pages.people.click_teammates_tab_button()

            max_allowed_chars = 30
            team_name_length = random.randint(5, max_allowed_chars)

            opposite_account_email = opposite_creds.credentials.signin_payload.email
            opposite_account = [usr for usr in self.org_end_users if usr.get('email') == opposite_account_email][0]
            opposite_account_name = opposite_account.get('name')
            opposite_account_repr = opposite_account_name or opposite_account_email

            self.tune_pages.people.click_new_team_button()

            team_name = generate_random_string(team_name_length)

            Report.logInfo(f"Generated random string with {team_name}: {team_name_length}")

            Report.logInfo(f"Typing generated string into team name input")
            self.tune_pages.people.input_team_name(team_name)
            Report.logInfo("Clicking CREATE button")
            self.tune_pages.people.click_create_team_button()
            self.tune_pages.people.wait_for_team_creation()
            Report.logInfo("Clicking Add Teammates Button")
            self.tune_pages.people_team.click_add_teammates_button()
            Report.logInfo(f"Searching for teammate:  {opposite_account_repr}")
            self.tune_pages.people_team_add_teammate.input_search_bar(opposite_account_repr)
            Report.logInfo("Clicking Add Button")
            self.tune_pages.people_team_add_teammate.click_user_button_by_name(opposite_account_repr,
                                                                               match_case=True)
            self.tune_pages.people_team_add_teammate.verify_loader_not_visible()
            Report.logInfo("Exiting Add Teammates Page")
            self.tune_pages.people_team_add_teammate.click_close_button()

            Report.logInfo("Clicking Back to Teammates List People Page")
            self.tune_pages.people_team.click_back_button()

            Report.logInfo(f"Checking if team {team_name} is visible")
            self._assert(
                condition=self.tune_pages.people.verify_team_by_team_name(team_name),
                log_pass=f"Team with name {team_name} is visible in Tune",
                log_fail=f"Team with name {team_name} is not visible in Tune"
            )
            Report.logInfo(f"Clicking on team: {team_name}")
            self.tune_pages.people.click_team_button_by_team_name(team_name)
            Report.logInfo(f"Clicking on user {opposite_account_repr}")
            self.tune_pages.people_team.click_user_button_by_name(opposite_account_repr)
            Report.logInfo(f"Clicking on Manage Teams Button for user {opposite_account_repr}")
            self.tune_pages.people_user.click_manage_teams_button()
            Report.logInfo(f"Clicking New Team Button on Manage Teams Page")
            self.tune_pages.people_user_manage_teams.click_new_team_button()
            new_team_name = generate_random_string(random.randint(2, max_allowed_chars))
            Report.logInfo(f"Creating new team with random name: {new_team_name}")
            self.tune_pages.people_user_manage_teams.input_team_name(new_team_name)
            self.tune_pages.people_user_manage_teams.click_create_team_button()
            Report.logInfo(f"Checking if created team is visible on manage teams page")
            self._assert(
                condition=self.tune_pages.people_user_manage_teams.verify_team_visible(new_team_name),
                log_pass=f"Previously created team {new_team_name} is visible",
                log_fail=f"Previously created team {new_team_name} is not visible"
            )
            Report.logInfo("Checking if created team contains 1 teammate")
            self._assert(
                condition=self.tune_pages.people_user_manage_teams.verify_teammates_number_for_team(new_team_name, 1),
                log_pass=f"Number of teammates for team {new_team_name} is OK",
                log_fail="Number of teammates for team is NOK"
            )
            Report.logInfo("Clicking Done button")
            self.tune_pages.people_user_manage_teams.click_done_button()
            Report.logInfo("Clicking back from user profile button")
            self.tune_pages.people_user.click_back_button()
            Report.logInfo("Clicking back from Team View button")
            self.tune_pages.people_team.click_back_button()
            Report.logInfo("Clicking Teammates Tab")
            self.tune_pages.people.click_teammates_tab_button()
            Report.logInfo(f"Checking if created team is visible main teams page")
            self._assert(
                condition=self.tune_pages.people.verify_team_by_team_name(new_team_name),
                log_pass=f"Previously created team {new_team_name} is visible",
                log_fail=f"Previously created team {new_team_name} is not visible"
            )
            Report.logInfo(f"Clicking on team {new_team_name}")
            self.tune_pages.people.click_team_button_by_team_name(new_team_name, match_case=True)
            Report.logInfo(f"Check if user {opposite_account_repr} is visible in team {new_team_name}")
            self._assert(
                condition=self.tune_pages.people_team.verify_teammate_by_name(opposite_account_repr),
                log_pass=f"User {opposite_account_repr} is visible in team: {new_team_name}",
                log_fail=f"User {opposite_account_repr} is not visible in team: {new_team_name}"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")
