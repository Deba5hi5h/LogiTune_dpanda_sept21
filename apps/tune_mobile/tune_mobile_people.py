import os
import time

from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile import TuneMobile
from base import global_variables
from extentreport.report import Report
from locators.tune_mobile.tune_mobile_people_locators import TuneMobilePeopleLocators


class TuneMobilePeople(TuneMobile):

    def click_teammates(self):
        """
        Method to click Teammates tab

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.TEAMMATES_TAB).click()
        return self

    def click_all_teammates(self):
        """
        Method to click All Teammates

        :param :
        :return TuneMobilePeople:
        """
        time.sleep(1)
        try:
            self.find_element(TuneMobilePeopleLocators.ALL_TEAMMATES).click()
            if not self.verify_add_teammates():
                self.find_element(TuneMobilePeopleLocators.ALL_TEAMMATES).click()
        except:
            self.find_element(TuneMobilePeopleLocators.ALL_TEAMMATES).click()
            if not self.verify_add_teammates():
                self.find_element(TuneMobilePeopleLocators.ALL_TEAMMATES).click()
        return self

    def verify_all_teammates(self) -> bool:
        """
        Method to verify All Teammates displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ALL_TEAMMATES)

    def click_new_team(self):
        """
        Method to click New Team button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.NEW_TEAM).click()
        return self

    def verify_new_team(self) -> bool:
        """
        Method to verify New Team button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NEW_TEAM)

    def click_add_teammates(self):
        """
        Method to click Add Teammates

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.ADD_TEAMMATES).click()
        return self

    def verify_add_teammates(self) -> bool:
        """
        Method to Verify Add Teammates button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADD_TEAMMATES, timeout=5)

    def click_edit(self):
        """
        Method to click Edit

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.EDIT).click()
        return self

    def click_delete_icon(self, teammate_name: str):
        """
        Method to click delete icon

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.DELETE_ICON, param=teammate_name, timeout=15).click()

    def verify_delete_icon(self, teammate_name: str) -> bool:
        """
        Method to verify delete icon next to teammate

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DELETE_ICON, param=teammate_name, timeout=2)

    def click_everyone(self):
        """
        Method to click All tab

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.EVERYONE_TAB).click()
        return self

    def click_bookmark(self):
        """
        Method to click bookmark icon

        :param teammate:
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.BOOKMARK).click()
        return self

    def click_remove_from_team(self):
        """
        Method to click remove from team

        :param teammate:
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.REMOVE_FROM_TEAMS).click()
        return self

    def click_add_to_team(self):
        """
        Method to click Add to team

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.ADD_TO_TEAM).click()
        return self

    def click_add(self, group_name: str = "All teammates"):
        """
        Method to click Add next to group name

        :param group_name:
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.ADD, param=group_name).click()
        return self

    def verify_added(self, teammate: str) -> bool:
        """
        Method to verify ADDED button displayed next to teammate

        :param teammate:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADDED, param=teammate)

    def click_remove_button(self, group_name: str = "All teammates"):
        """
        Method to click Remove next to group name

        :param group_name:
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.REMOVE_BUTTON, param=group_name).click()
        return self

    def click_done(self):
        """
        Method to click Done

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.DONE).click()
        return self

    def verify_done(self) -> bool:
        """
        Method to verify Done button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DONE)

    def click_teammate(self, teammate: str, booking: bool = False):
        """
        Method to click teammate name

        :param teammate:
        :return TuneMobilePeople:
        """
        if not booking:
            self.scroll_to_top()
        for _ in range(5):
            if self.verify_element(TuneMobilePeopleLocators.TEAMMATE, param=teammate, timeout=1):
                break
            if self.is_ios_device():
                self.swipe_screen(direction="vertical", start=0.8, end=0.3)
            else:
                self.swipe_screen(direction="vertical", start=0.7, end=0.4)
        self.find_element(TuneMobilePeopleLocators.TEAMMATE, param=teammate, timeout=1).click()
        return self

    def click_group(self, group_name: str):
        """
        Method to click Sync Portal group name
        :param teammate:
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.GROUP_NAME, param=group_name).click()
        return self

    def click_remove(self):
        """
        Method to click Remove button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.REMOVE).click()
        return self

    def click_cancel(self):
        """
        Method to click Cancel button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.CANCEL).click()
        return self

    def click_back(self):
        """
        Method to click Back button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.BACK).click()
        return self

    def verify_back(self) -> bool:
        """
        Method to verify Back button

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.BACK)

    def click_back_to_custom_team(self):
        """
        Method to click Back to custom team button
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.BACK_TO_CUSTOM).click()
        return self

    def verify_back_to_custom_team(self) -> bool:
        """
        Method to verify Back button which navigates back to custom team
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.BACK_TO_CUSTOM)

    def type_in_search(self, search_text: str):
        """
        Method to type in search text field

        :param search_text:
        :return TuneMobilePeople:
        """
        # Need to uncomment below line once bug is fixed with case sensitive issue
        # search_text = search_text.lower()
        # self.scroll_to_top()
        if self.is_ios_device():
            self.find_element(TuneMobilePeopleLocators.SEARCH).send_keys(search_text + "\n")
        else:
            # self.find_element(TuneMobilePeopleLocators.SEARCH).send_keys(search_text)
            # Workaround for Android bug
            el = self.find_element(TuneMobilePeopleLocators.SEARCH)
            el.clear()
            el.send_keys(search_text)
            # global_variables.driver.press_keycode(66)
        return self

    def verify_search(self) -> bool:
        """
        Method to verify search text field displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.SEARCH)

    def click_clear_search(self):
        """
        Method to click clear search button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.CLEAR_SEARCH).click()
        return self

    def verify_add_to_team(self) -> bool:
        """
        Method to verify add to team button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADD_TO_TEAM, timeout=3)

    def verify_add(self, group_name: str = "All teammates") -> bool:
        """
        Method to verify add button displayed next to group

        :param group_name:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADD, param=group_name, timeout=2)

    def verify_remove_manage_teams_screen(self, group_name: str = "All teammates") -> bool:
        """
        Method to verify Remove button displayed next to group

        :param group_name:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.REMOVE_BUTTON, param=group_name, timeout=3)

    def verify_edit(self) -> bool:
        """
        Method to verify Edit link displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.EDIT, timeout=2)

    def verify_remove_from_teams(self) -> bool:
        """
        Method to verify remove from team button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.REMOVE_FROM_TEAMS, timeout=3)

    def verify_favorite_icon(self) -> bool:
        """
        Method to verify favorite icon displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.FAVORITE_ICON, timeout=3)

    def verify_locate_on_map(self) -> bool:
        """
        Method to verify locate on map displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.LOCATE_ON_MAP, timeout=3)

    def verify_clear_search(self) -> bool:
        """
        Method to verify clear search icon displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CLEAR_SEARCH, timeout=1)

    def verify_remove_message(self) -> bool:
        """
        Method to verify message displayed for removing teammate

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.REMOVE_MESSAGE)

    def verify_teammate_message(self) -> bool:
        """
        Method to verify message displayed for teammate list visible only to you

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAMMATE_MESSAGE)

    def verify_cancel_button(self) -> bool:
        """
        Method to verify Cancel button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CANCEL)

    def verify_remove_button(self) -> bool:
        """
        Method to verify Remove button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.REMOVE)

    def verify_no_results_message(self) -> bool:
        """
        Method to verify message displayed for no search results

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_RESULTS_MESSAGE)

    def verify_no_teammates_message(self) -> bool:
        """
        Method to verify message displayed for no teammates added

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_TEAMMATES_MESSAGE)

    def verify_add_teammates_message(self) -> bool:
        """
        Method to verify message displayed for add teammates

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADD_TEAMMATES_MESSAGE, timeout=1)

    def verify_teammates_tab_selected(self) -> bool:
        """
        Method to verify People navigation button highlighted

        :param :
        :return bool:
        """
        if self.is_android_device():
            return self.find_element(TuneMobilePeopleLocators.TEAMMATES_TAB).is_selected()
        return True  # Not supported for iOS and is skipped

    def verify_search_control_displayed(self) -> bool:
        """
        Method to verify Search control displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.SEARCH, timeout=1)

    def verify_teammates_title(self) -> bool:
        """
        Method to verify Teammates title displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAMMATE_TITLE, timeout=1)

    def verify_user_name(self, user_name: str) -> bool:
        """
        Method to verify User or Teammate Name displayed

        :param user_name:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.STATIC_TEXT, param=user_name, timeout=2)

    def verify_user_booking(self, start: str, end: str, floor: str, area: str, desk_name: str) -> bool:
        """
        Method to verify User or Teammate booking details displayed

        :param start:
        :param end:
        :param floor:
        :param area:
        :param desk_name:
        :return bool:
        """
        booking = f"{start} - {end} · {floor} · {area} · {desk_name}"
        return self.verify_element(TuneMobilePeopleLocators.STATIC_TEXT, param=booking, timeout=2)

    def verify_no_upcoming_booking(self) -> bool:
        """
        Method to verify message displayed - There are no upcoming bookings for this user.

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_UPCOMING_BOOKING, timeout=2)

    def verify_no_teammates_in_office(self) -> bool:
        """
        Method to verify message displayed - No teammates in the office.

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_TEAMMATES_IN_OFFICE, timeout=2)

    def verify_no_people_in_office(self) -> bool:
        """
        Method to verify message displayed - No people in the office.

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_PEOPLE_IN_OFFICE, timeout=2)

    def verify_no_teammates_in_area(self) -> bool:
        """
        Method to verify message displayed - No teammates in this area.

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_TEAMMATES_IN_AREA, timeout=2)

    def verify_no_people_in_area(self) -> bool:
        """
        Method to verify message displayed - No people in this area.

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.NO_PEOPLE_IN_AREA, timeout=2)

    def remove_all_teammates(self):
        """
        Method to remove all teammates

        :param :
        :return TuneMobilePeople:
        """
        teammates = self.get_teammates_list()
        if len(teammates) > 0:
            Report.logInfo("Removing all teammates")
            self.click_edit()
            for teammate in teammates:
                self.click_delete_icon(teammate_name=teammate)
                self.click_remove()
                time.sleep(1)
        return self

    def get_people_list(self) -> list:
        """
        Method to get all names listed

        :param :
        :return list:
        """
        people = []
        time.sleep(1)
        value = 'value' if self.is_ios_device() else 'text'
        names = self.find_elements(TuneMobilePeopleLocators.PEOPLE_LIST, timeout=2)
        for name in names[:8]:
            if tune_mobile_config.phone == "OnePlus":
                people.append(name.text)
            else:
                people.append(name.get_attribute(value))
        return people

    def get_teammates_list(self, custom_team: bool = False) -> list:
        """
        Method to get all names listed

        :param :
        :return list:
        """
        people = []
        time.sleep(1)
        value = 'value' if self.is_ios_device() else 'text'
        if custom_team:
            names = self.find_elements(TuneMobilePeopleLocators.CUSTOM_TEAM_TEAMMATES_LIST, timeout=2)
        else:
            names = self.find_elements(TuneMobilePeopleLocators.TEAMMATES_LIST, timeout=2)
        for name in names[:15]:
            if tune_mobile_config.phone == "OnePlus":
                people.append(name.text)
            else:
                people.append(name.get_attribute(value))
        return people

    def get_user_groups_list(self, add_teammates: bool = False) -> list:
        """
        Method to get all user groups listed in Everyone tab

        :param add_teammates:
        :return list:
        """
        groups = []
        time.sleep(1)
        value = 'value' if self.is_ios_device() else 'text'
        if add_teammates:
            names = self.find_elements(TuneMobilePeopleLocators.ADD_TEAMMATES_GROUPS_LIST, timeout=2)
        else:
            names = self.find_elements(TuneMobilePeopleLocators.USER_GROUPS_LIST, timeout=2)
        for name in names[:8]:
            groups.append(str(name.get_attribute(value)).split("·")[0].strip())
        return groups

    def scroll_to_top(self):
        """
        Method to scroll to top of list

        :param :
        :return list:
        """
        for _ in range(10):
            if self.verify_search_control_displayed():
                break
            self.swipe_screen('vertical', 0.2, 0.8)

    def get_teammate_email(self, teammate_name: str) -> str:
        """
        Method to get email from teammate screen

        :param :
        :return str:
        """
        time.sleep(1)
        value = 'value' if self.is_ios_device() else 'text'
        name = self.find_element(TuneMobilePeopleLocators.TEAMMATE_EMAIL, param=teammate_name, timeout=2)
        return name.get_attribute(value)

    def verify_create_new_team(self) -> bool:
        """
        Method to verify Create new team title displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CREATE_NEW_TEAM, timeout=2)

    def click_create(self):
        """
        Method to click Create button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.CREATE).click()
        return self

    def verify_create(self) -> bool:
        """
        Method to verify Create button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CREATE, timeout=2)

    def click_return_key(self):
        """
        Method to click keyboard return key

        :param :
        :return TuneMobilePeople:
        """
        if self.is_android_device():
            global_variables.driver.press_keycode(111)
        else:
            self.find_element(TuneMobilePeopleLocators.RETURN_KEY).click()
        return self

    def verify_create_enabled(self) -> bool:
        """
        Method to verify Create button displayed

        :param :
        :return bool:
        """
        el = self.find_element(TuneMobilePeopleLocators.CREATE)
        return str(el.get_attribute("enabled")) == "true"

    def type_team_name(self, team_name: str):
        """
        Method to type team_name in text field

        :param team_name:
        :return TuneMobilePeople:
        """
        el = self.find_element(TuneMobilePeopleLocators.TEAM_NAME_TEXTFIELD)
        if self.is_ios_device():
            el.clear()
        el.send_keys(team_name)
        return self

    def verify_team_name_text_field(self) -> bool:
        """
        Method to verify Team Name text field displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAM_NAME_TEXTFIELD)

    def verify_close(self) -> bool:
        """
        Method to verify Close button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CLOSE)

    def click_close(self):
        """
        Method to click Close button from bottom sheet

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.CLOSE).click()
        return self

    def verify_team_title(self, team_name: str) -> bool:
        """
        Method to verify team name title displayed

        :param team_name:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.STATIC_TEXT, param=team_name)

    def verify_team_empty(self) -> bool:
        """
        Method to verify The team is empty message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAM_EMPTY)

    def verify_add_few_teammates(self) -> bool:
        """
        Method to verify Let’s add a few teammates message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.ADD_FEW_TEAMMATES)

    def click_custom_team(self, team_name: str):
        """
        Method to verify Custom team group name displayed

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.CUSTOM_TEAM, param=team_name).click()
        return self

    def verify_custom_team(self, team_name: str) -> bool:
        """
        Method to verify Custom team group name displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.CUSTOM_TEAM, param=team_name, timeout=5)

    def click_edit_teams(self):
        """
        Method to click Edit Teams button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.EDIT_TEAMS).click()
        return self

    def verify_edit_teams(self) -> bool:
        """
        Method to verify Edit Teams button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.EDIT_TEAMS, timeout=2)

    def click_delete_button(self):
        """
        Method to click Delete button

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.DELETE_BUTTON).click()
        return self

    def verify_delete_button(self) -> bool:
        """
        Method to verify Delete button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DELETE_BUTTON, timeout=2)

    def remove_all_teams(self):
        """
        Method to remove all teams

        :param :
        :return TuneMobilePeople:
        """
        time.sleep(1)
        self.swipe_screen(direction="vertical", start=0.7, end=0.3)
        if self.verify_edit_teams():
            Report.logInfo("Removing all Teams")
            self.click_edit_teams()
            delete_buttons = self.find_elements(TuneMobilePeopleLocators.DELETE_ALL_TEAMS)
            while len(delete_buttons) > 0:
                delete_buttons[0].click()
                self.click_delete_button()
                delete_buttons = self.find_elements(TuneMobilePeopleLocators.DELETE_ALL_TEAMS, timeout=2)
            self.click_done()
        return self

    def click_manage_teams(self):
        """
        Method to click Manage Teams button
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.MANAGE_TEAMS).click()
        return self

    def verify_manage_teams(self) -> bool:
        """
        Method to verify Manage Teams button displayed
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.MANAGE_TEAMS, timeout=2)

    def click_team_name_edit(self):
        """
        Method to click edit button next to team name
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.TEAM_NAME_EDIT).click()
        return self

    def verify_team_name_edit(self) -> bool:
        """
        Method to verify edit button next to team name
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAM_NAME_EDIT, timeout=2)

    def click_team_name_update(self):
        """
        Method to click update button from bottom sheet
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.TEAM_NAME_UPDATE).click()
        return self

    def verify_team_name_update(self) -> bool:
        """
        Method to verify update button displayed in bottom sheet
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAM_NAME_UPDATE, timeout=2)

    def is_team_name_update_enabled(self) -> bool:
        """
        Method to verify update button is enabled
        :param :
        :return bool:
        """
        el = self.find_element(TuneMobilePeopleLocators.TEAM_NAME_UPDATE)
        return el.get_attribute('enabled') == 'true'

    def click_delete_team(self):
        """
        Method to click delete team button
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.DELETE_TEAM).click()
        return self

    def verify_delete_team(self) -> bool:
        """
        Method to verify delete button displayed
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DELETE_TEAM, timeout=2)

    def verify_team_name_tick_mark(self) -> bool:
        """
        Method to verify tick mark displayed next to team name
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.TEAM_NAME_TICK_MARK, timeout=2)

    def click_team_name_tick_mark(self):
        """
        Method to click tick mark displayed next to team name
        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobilePeopleLocators.TEAM_NAME_TICK_MARK).click()
        return self

    def verify_delete_team_message(self) -> bool:
        """
        Method to verify message - Teammates will be removed from the team. This change is visible only for you.
        :param :
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DELETE_TEAM_MESSAGE, timeout=2)

    def verify_delete_team_confirmation(self, team_name: str) -> bool:
        """
        Method to verify message - Delete the <name> team?
        :param team_name:
        :return bool:
        """
        return self.verify_element(TuneMobilePeopleLocators.DELETE_TEAM_CONFIRM, param=team_name, timeout=2)

    def get_team_count(self) -> int:
        """
        Method to get number of teams user is added
        :param :
        :return int:
        """
        el = self.find_element(TuneMobilePeopleLocators.TEAM_COUNT)
        value = 'text' if self.is_android_device() else 'value'
        return int(el.get_attribute(value))

    def get_custom_team_teammate_count(self, team_name: str) -> int:
        """
        Method to get number of additional teammate count displayed next to custom team
        :param team_name:
        :return int:
        """
        el = self.find_element(TuneMobilePeopleLocators.CUSTOM_TEAM_TEAMMATE_COUNT, param=team_name)
        value = 'text' if self.is_android_device() else 'value'
        count = str(el.get_attribute(value)).replace('+', '')
        return int(count)

    def get_people_count_in_team(self, team_name: str) -> int:
        """
        Method to get count of people displayed under team
        :param team_name:
        :return int:
        """
        el = self.find_element(TuneMobilePeopleLocators.PEOPLE_COUNT_IN_TEAM, param=team_name)
        value = 'text' if self.is_android_device() else 'value'
        people_count = str(el.get_attribute(value))
        if people_count.lower() == "empty":
            return 0
        else:
            return int((people_count).split(' ')[0])
