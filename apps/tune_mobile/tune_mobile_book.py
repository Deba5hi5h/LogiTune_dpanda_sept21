import datetime
import time

from selenium.webdriver.common.by import By

from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_building import TuneMobileBuilding
from base import global_variables
from locators.tune_mobile.tune_mobile_book_locators import TuneMobileBookLocators


class TuneMobileBook(TuneMobile):
    building = TuneMobileBuilding()

    def click_by_location_and_preferences(self):
        """
        Method to click By Location and Preferences option

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.BY_LOCATION_AND_PREFERENCES).click()
        return self

    def verify_location_and_preferences(self) -> bool:
        """
        Method to verify 'By location and preferences' control shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.BY_LOCATION_AND_PREFERENCES)

    def click_near_teammate(self):
        """
        Method to click Near Teammate option

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.NEAR_TEAMMATE).click()
        return self

    def click_close(self):
        """
        Method to click close option

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.CLOSE).click()
        return self

    def click_back(self):
        """
        Method to click Back option

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.BACK).click()
        return self

    def verify_near_teammate(self) -> bool:
        """
        Method to verify 'Near teammate' control shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NEAR_TEAMMATE)

    def click_schedule(self):
        """
        Method to click schedule

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.SCHEDULE).click()
        return self

    def click_start_time(self):
        """
        Method to click Start Time

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.START_TIME).click()
        return self

    def click_end_time(self):
        """
        Method to click End Time

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.END_TIME).click()
        return self

    def click_check_in(self):
        """
        Method to click Check in button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.CHECK_IN_BUTTON).click()
        return self

    def click_decline(self):
        """
        Method to click Decline button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.DECLINE_BUTTON).click()
        return self

    def click_check_in_ok(self):
        """
        Method to click OK button on checked in screen

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.CHECK_IN_OK).click()
        return self

    def set_start_hour(self, hour: int):
        """
        Method to set start Hour

        :param :
        :return TuneMobileBook:
        """
        element = self.find_element(TuneMobileBookLocators.START_HOUR)
        i = 12
        while element.get_attribute('value') != f'{hour} o’clock' and i > 0:
            self.scroll_wheel(element)
            i -= 1
        return self

    def set_start_minute(self, minute: int):
        """
        Method to set start Minutue

        :param :
        :return TuneMobileBook:
        """
        if minute == 0:
            min = "00"
        else:
            min = str(minute)
        self.find_element(TuneMobileBookLocators.START_MINUTE).send_keys(min)
        return self

    def set_start_ampm(self, ampm: str):
        """
        Method to set start AM or PM

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.START_AMPM).send_keys(ampm)
        return self

    def set_end_hour(self, hour: int):
        """
        Method to set End Hour

        :param :
        :return TuneMobileBook:
        """
        element = self.find_element(TuneMobileBookLocators.END_HOUR)
        i = 12
        direction = "down"
        if hour > int(element.get_attribute('value').split(" ")[0]):
            direction = "up"
        while element.get_attribute('value') != f'{hour} o’clock' and i > 0:
            self.scroll_wheel(element, direction=direction)
            i -= 1
        return self

    def set_end_minute(self, minute: int):
        """
        Method to set End Minutue

        :param :
        :return TuneMobileBook:
        """
        if minute == 0:
            min = "00"
        else:
            min = str(minute)
        self.find_element(TuneMobileBookLocators.END_MINUTE).send_keys(min)
        return self

    def set_end_ampm(self, ampm: str):
        """
        Method to set End AM or PM

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.END_AMPM).send_keys(ampm)
        return self

    def click_desk(self, desk_name: str):
        """
        Method to click Desk

        :param desk_name:
        :return TuneMobileBook:
        """
        element = self.find_element(TuneMobileBookLocators.DESK, param=desk_name, visibility=False)
        i = 1
        while not element.is_displayed() and i < 10:
            self.swipe("up")
            i += 1
            time.sleep(1)
        self.find_element(TuneMobileBookLocators.DESK, param=desk_name).click()
        return self

    def click_book(self):
        """
        Method to click Book button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.BOOK).click()
        return self

    def verify_book_button(self) -> bool:
        """
        Method to verify Book button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.BOOK, timeout=2)

    def click_list(self):
        """
        Method to click List tab

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.LIST).click()
        return self

    def click_skip(self):
        """
        Method to click Skip button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.SKIP).click()
        return self

    def verify_skip(self) -> bool:
        """
        Method to verify Skip button shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.SKIP, timeout=2)

    def click_done(self):
        """
        Method to click Book button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.DONE).click()
        return self

    def click_calendar_icon(self):
        """
        Method to click Calendar icon to change the schedule

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.CALENDAR_ICON).click()
        return self

    def click_date(self, day:int = 0):
        """
        Method to click Date from the Schedule calendar

        :param day:
        :return TuneMobileBook:
        """
        current_date = datetime.datetime.now()
        date_to_click = current_date + datetime.timedelta(day)
        date = str(date_to_click.day)
        self.find_element(TuneMobileBookLocators.DATE, param=date).click()
        return self

    def click_floor_icon(self):
        """
        Method to click floor icon to change the floor

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.FLOOR).click()
        return self

    def select_floor_name(self, floor_name):
        """
        Method to click floor name to select the floor in change floor screen

        :param floor_name:
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.STATIC_TEXT, param=floor_name).click()
        return self

    def toggle_notify_teammate(self, teammate: str):
        """
        Method to click Notify teammate toggle

        :param teammate:
        :return TuneMobileBook:
        """
        if not self.verify_notify_toggle(teammate=teammate):
            self.find_element(TuneMobileBookLocators.NOTIFY_TEAMMATE_TOGGLE, param=teammate).click()
            time.sleep(2)
        return self

    def verify_notify_toggle(self, teammate: str) -> bool:
        """
        Method to verify toggle switch is ON

        :param teammate:
        :return bool:
        """
        el = self.find_element(TuneMobileBookLocators.NOTIFY_TEAMMATE_TOGGLE, param=teammate)
        if self.is_ios_device():
            return el.get_attribute("value") == '1'
        else:
            return el.get_attribute("checked") == 'true'

    def click_notify_teammate(self):
        """
        Method to click Notify teammate button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.NOTIFY_TEAMMATE_BUTTON).click()
        return self

    def click_notify_with_message(self):
        """
        Method to click Notify with message button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.NOTIFY_WITH_MESSAGE_BUTTON).click()
        return self

    def click_ok(self):
        """
        Method to click floor icon to change the floor

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.OK).click()
        return self

    def input_custom_message(self, custom_message: str):
        """
        Method to enter custom message

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.MESSAGE_TEXT_BOX).send_keys(custom_message)
        return self

    def verify_notify_teammates_screen(self) -> bool:
        """
        Method to verify Notify Teammates screen shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFY_TEAMMATES_SCREEN)

    def verify_notify_teammates_title(self) -> bool:
        """
        Method to verify 'No teammates added' message shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFY_TEAMMATES_TITLE)

    def verify_notify_teammates_button(self) -> bool:
        """
        Method to verify 'Notify Teammate' button shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFY_TEAMMATE_BUTTON)

    def verify_notify_with_message_button(self) -> bool:
        """
        Method to verify 'Notify with message' button shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFY_WITH_MESSAGE_BUTTON)

    def verify_include_message_text(self, count: int = 0) -> bool:
        """
        Method to verify 'Include message (count/128)' text shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.INCLUDE_MESSAGE_TEXT, param=str(count))

    def verify_message_textbox(self) -> bool:
        """
        Method to verify optional message textbox shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.MESSAGE_TEXT_BOX)

    def verify_notify_teammates_message(self) -> bool:
        """
        Method to verify 'Add people to teammates in order to notify them of your reservation' message shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFY_TEAMMATES_MESSAGE)

    def verify_notify_teammates_teammate_name(self, teammate_name) -> bool:
        """
        Method to verify Teammate name shown

        :param teammate_name:
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.STATIC_TEXT, param=teammate_name)

    def verify_desk_booked_screen(self, desk_name: str) -> bool:
        """
        Method to verify Desk booked screen shown

        :param desk_name:
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.DESK_BOOKED_SCREEN, param=desk_name)

    def verify_desk_booked_message(self) -> bool:
        """
        Method to verify 'Your desk will be waiting:' message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.DESK_BOOKED_MESSAE)

    def click_teammate_schedule(self, schedule: str):
        """
        Method to click on teammate's schedule while booking near teammate

        :param schedule:
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.DESK_BOOKED_SCHEDULE, param=schedule).click()
        return self

    def verify_desk_booked_schedule(self, schedule: str) -> bool:
        """
        Method to verify schedule displayed in desk booked screen

        :param schedule:
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.DESK_BOOKED_SCHEDULE, param=schedule, visibility=False)

    def verify_desk_booked_day(self, schedule: str, day: int = 0) -> bool:
        """
        Method to verify schedule displayed in desk booked screen

        :param schedule:
        :param day:
        :return bool:
        """
        value = 'value' if self.is_ios_device() else 'text'
        day_value = 'Today' if day == 0 else 'Tomorrow'
        el = self.find_element(TuneMobileBookLocators.DESK_BOOKED_SCHEDULE, param=schedule)
        el_text = str(el.get_attribute(value))
        return day_value in el_text

    def verify_check_in_message(self) -> bool:
        """
        Method to verify 'Are you trying to check in?' message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.CHECK_IN_MESSAGE)

    def verify_check_in_desk_name(self, desk_name: str) -> bool:
        """
        Method to verify correct desk name displayed in Check in screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.CHECK_IN_DESK_NAME, param=desk_name)

    def verify_check_in_success_message(self, desk_name: str) -> bool:
        """
        Method to verify Checked in to desk message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.CHECK_IN_SUCCESS_MESSAGE, param=desk_name)

    def verify_check_in_all_set(self) -> bool:
        """
        Method to verify You're all set! message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.ALL_SET_MESSAGE)

    def verify_teammate_notified_message(self) -> bool:
        """
        Method to verify Teammate notified message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.TEAMMATE_NOTIFIED_MESSAGE)

    def verify_custom_message(self, custom_message: str) -> bool:
        """
        Method to verify Custom message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.CUSTOM_MESSAE, param=custom_message)

    def verify_notification_sent_message(self) -> bool:
        """
        Method to verify Notification sent message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.NOTIFICATION_SENT_MESSAGE)

    def get_booking_start(self) -> str:
        """
        Method to get the booking start time from the booking screen

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.BOOKING_START)
        value = 'value' if self.is_ios_device() else 'text'
        element_value = str(element.get_attribute(value))
        if self.is_ios_device():
            return element_value.split(',')[1].split('-')[0].strip()
        else:
            return element_value.split("·")[1].strip()

    def get_booking_end(self) -> str:
        """
        Method to get the booking end time from the booking screen

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.BOOKING_END)
        value = 'value' if self.is_ios_device() else 'text'
        # return str(element.get_attribute(value)).strip()
        element_value = str(element.get_attribute(value))
        if self.is_ios_device():
            return element_value.split(',')[1].split('-')[1].strip()
        else:
            return element_value.strip()

    def get_current_schedule(self) -> str:
        """
        Method to get the current schedule from calendar screen

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.CURRENT_SCHEDULE)
        value = 'value' if self.is_ios_device() else 'text'
        return element.get_attribute(value)

    def drag_end_knob(self, drag_factor: float):
        """
        Method to drag the end time of the schedule

        :param :
        :return TuneMobileBook:
        """
        value = int(drag_factor * 70)
        element = self.find_element(TuneMobileBookLocators.END_KNOB, visibility=False)
        self.drag(element=element, direction="vertical", end=value)

    def drag_start_knob(self, drag_factor: float):
        """
        Method to drag the start time of the schedule

        :param :
        :return TuneMobileBook:
        """
        value = int(drag_factor * 70)
        element = self.find_element(TuneMobileBookLocators.START_KNOB, visibility=False)
        self.drag(element=element, direction="vertical", end=value)

    def drag_current_booking(self, drag_factor: float):
        """
        Method to drag current schedule in calendar

        :param :
        :return TuneMobileBook:
        """
        value = int(drag_factor * 90)
        element = self.find_element(TuneMobileBookLocators.CURRENT_SCHEDULE)
        self.drag(element=element, direction="vertical", end=value)

    def click_confirm(self):
        """
        Method to click confirm button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.CONFIRM).click()
        return self

    def click_update_booking(self):
        """
        Method to click update booking button

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileBookLocators.UPDATE_BOOKING).click()
        return self

    def verify_edit_booking(self) -> bool:
        """
        Method to verify edit booking screen shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.EDIT_BOOKING)

    def verify_booking_updated(self) -> bool:
        """
        Method to verify Booking updated popup screen shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBookLocators.BOOKING_UPDATED)

    def adjust_start_time(self, start_time: str):
        """
        Method to adjust the schedule start time in calendar view

        :param :
        :return TuneMobileBook:
        """
        schedule = self.get_current_schedule()
        start = schedule.split("-")[0].strip()
        self.drag_start_knob(drag_factor=self.get_hour_difference(start_time, start))
        for _ in range(30):
            schedule = self.get_current_schedule()
            start = schedule.split("-")[0].strip()
            if self.compare_time_values_equal(start, start_time):
                break
            time.sleep(2)
            if not self.verify_element(TuneMobileBookLocators.START_KNOB, timeout=1):
                self.swipe_screen(direction="vertical", start=0.3, end=0.5)
            if self.compare_time_values(start, start_time):
                self.drag_start_knob(drag_factor=-0.25)
            else:
                self.drag_start_knob(drag_factor=0.3)
        return self

    def adjust_end_time(self, end_time: str):
        """
        Method to adjust the schedule end time in calendar view

        :param :
        :return TuneMobileBook:
        """
        schedule = self.get_current_schedule()
        end = schedule.split("-")[1].strip()
        self.drag_end_knob(drag_factor=self.get_hour_difference(end_time, end)/2)
        for _ in range(30):
            schedule = self.get_current_schedule()
            end = schedule.split("-")[1].strip()
            if self.compare_time_values_equal(end, end_time):
                break
            time.sleep(2)
            if not self.verify_element(TuneMobileBookLocators.END_KNOB, timeout=1):
                self.swipe_screen(direction="vertical", start=0.5, end=0.3)
            if self.compare_time_values(end, end_time):
                self.drag_end_knob(drag_factor=-0.25)
            else:
                self.drag_end_knob(drag_factor=0.3)
        return self

    def compare_time_values(self, time1: str, time2: str) -> bool:
        """
        Method to compare two time values and return True if time1 > time2 else false

        :param :
        :return bool:
        """
        time1 = datetime.datetime.strptime(time1, '%I:%M %p').time()
        time2 = datetime.datetime.strptime(time2, '%I:%M %p').time()
        return True if time1 > time2 else False

    def compare_time_values_equal(self, time1: str, time2: str) -> bool:
        """
        Method to compare two time values are equal

        :param :
        :return bool:
        """
        time1 = datetime.datetime.strptime(time1, '%I:%M %p').time()
        time2 = datetime.datetime.strptime(time2, '%I:%M %p').time()
        t1 = time1.hour - time2.hour
        t2 = time2.hour - time1.hour
        return True if time1 == time2 else False

    def get_hour_difference(self, time1: str, time2: str) -> int:
        """
        Method to get hour difference between two time values

        :param :
        :return int:
        """
        time1 = datetime.datetime.strptime(time1, '%I:%M %p').time()
        time2 = datetime.datetime.strptime(time2, '%I:%M %p').time()
        return time1.hour - time2.hour

    def get_selected_building(self) -> str:
        """
        Method to get selected building name from the booking screen

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.BUILDING_NAME)
        value = 'value' if self.is_ios_device() else 'text'
        return element.get_attribute(value)

    def get_selected_floor(self) -> str:
        """
        Method to get selected floor name from the booking screen

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.FLOOR_NAME)
        value = 'value' if self.is_ios_device() else 'text'
        return element.get_attribute(value)

    def get_current_workspace(self, desk_name: str) -> str:
        """
        Method to get selected workspace for the desk from the booking screen

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileBookLocators.WORKSPACE_BY_DESK, param=desk_name)
        value = 'name' if self.is_ios_device() else 'text'
        workspace = str(element.get_attribute(value)).split('·')[0].strip()
        return workspace

    def click_workspace(self, workspace: str):
        """
        Method to click workspace in the booking screen

        :param workspace:
        :return TuneMobileBook:
        """
        if self.is_android_device():
            workspace = workspace.upper()
        self.find_element(TuneMobileBookLocators.WORKSPACE, param=workspace).click()
        return TuneMobileBook

    def change_building(self, site_name: str, building_name: str):
        """
        Method to change building name in the booking screen

        :param site_name:
        :param building_name:
        :return TuneMobileBook:
        """
        if not building_name == self.get_selected_building():
            self.find_element(TuneMobileBookLocators.BUILDING).click()
            self.building.change_building(site_name=site_name, building_name=building_name)
            time.sleep(2)
        return TuneMobileBook

    def change_floor(self, floor_name: str):
        """
        Method to change floor in the booking screen

        :param floor_name:
        :return TuneMobileBook:
        """
        if not floor_name == self.get_selected_floor():
            self.click_floor_icon()
            self.select_floor_name(floor_name=floor_name)
            if self.is_android_device():
                self.click_ok()
        return TuneMobileBook

    def set_start_time(self):
        """
        Method to click Calendar icon to change the schedule

        :param :
        :return TuneMobileBook:
        """

        driver = TuneMobile.driver
        el = driver.find_element(By.ID, "com.logitech.logue:id/book_desk_button_end_time")
        resource_id = el.get_attribute('resourceId')
        # script = f"document.getElementById('com.logitech.logue:id/title_text_view').innerText = 'Eng-Floor';"
        # script = f"arguments[0].setText('Today · 7:30 PM');"
        # driver.execute_script(script)
        # driver.execute_script("arguments[0].setAttribute('text', 'Eng-Floor');", el)
        el.text = '6:00 PM'
        # el.send_keys('Eng-Floor')
        # driver.execute_script('mobile: shell', {'command': 'input text "Today · 11:40 AM"', 'args': [el]})

        return self