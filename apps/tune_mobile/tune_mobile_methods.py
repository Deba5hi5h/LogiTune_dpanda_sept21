import time
from datetime import datetime, timedelta
import deepdiff
import numpy
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from apps.browser_methods import BrowserClass
from apps.collabos.collabos_base import CollabOsBase
from apps.raiden.sync_portal_login import SyncPortalLogin
from apps.raiden.sync_portal_methods import SyncPortalMethods
from apps.collabos.coily.coily_methods import TuneCoilyMethods
from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.phone_settings import PhoneSettings
from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_advanced_call_clarity import TuneMobileAdvancedCallClarity
from apps.tune_mobile.tune_mobile_anc import TuneMobileANC
from apps.tune_mobile.tune_mobile_book import TuneMobileBook
from apps.tune_mobile.tune_mobile_building import TuneMobileBuilding
from apps.tune_mobile.tune_mobile_button_functions import TuneMobileButtonFunctions
from apps.tune_mobile.tune_mobile_connected_devices import TuneMobileConnectedDevices
from apps.tune_mobile.tune_mobile_dashboard import TuneMobileDashboard
from apps.tune_mobile.tune_mobile_device_name import TuneMobileDeviceName
from apps.tune_mobile.tune_mobile_equalizer import TuneMobileEqualizer
from apps.tune_mobile.tune_mobile_headset_language import TuneMobileHeadsetLanguage
from apps.tune_mobile.tune_mobile_health_and_safety import TuneMobileHealthAndSafety
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from apps.tune_mobile.tune_mobile_image import TuneMobileImage
from apps.tune_mobile.tune_mobile_notification import TuneMobileNotification
from apps.tune_mobile.tune_mobile_on_head_detection import TuneMobileOnHeadDetection
from apps.tune_mobile.tune_mobile_people import TuneMobilePeople
from apps.tune_mobile.tune_mobile_personal_eq import TuneMobilePersonalEq
from apps.tune_mobile.tune_mobile_profile import TuneMobileProfile
from apps.tune_mobile.tune_mobile_raiden_api import TuneMobileRaidenApi
from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
from apps.tune_mobile.tune_mobile_sidetone import TuneMobileSidetone
from apps.tune_mobile.tune_mobile_sleep_settings import TuneMobileSleepSettings
from apps.tune_mobile.tune_mobile_touch_pad import TuneMobileTouchPad
from apps.tune_mobile.tune_mobile_voice_prompts import TuneMobileVoicePrompts
from base import global_variables, base_settings
from base.base_mobile import MobileBase
from base.listener import CustomBrowserListener
from extentreport.report import Report
from testsuite_tune_mobile import test_data


class TuneMobileMethods(TuneMobile):
    home = TuneMobileHome()
    dashboard = TuneMobileDashboard()
    people = TuneMobilePeople()
    profile = TuneMobileProfile()
    notification = TuneMobileNotification()
    building = TuneMobileBuilding()
    equalizer = TuneMobileEqualizer()
    connected_devices = TuneMobileConnectedDevices()
    sidetone = TuneMobileSidetone()
    advanced_call_clarity = TuneMobileAdvancedCallClarity()
    anc_button_options = TuneMobileANC()
    on_head_detection = TuneMobileOnHeadDetection()
    touch_pad = TuneMobileTouchPad()
    voice_prompts = TuneMobileVoicePrompts()
    health_and_safety = TuneMobileHealthAndSafety()
    personal_eq = TuneMobilePersonalEq()
    sleep_settings = TuneMobileSleepSettings()
    headset_language = TuneMobileHeadsetLanguage()
    settings = TuneMobileSettings()
    device_name = TuneMobileDeviceName()
    button_functions = TuneMobileButtonFunctions()
    book = TuneMobileBook()
    phone_settings = PhoneSettings()
    sync_portal = SyncPortalMethods()
    raiden_api = TuneMobileRaidenApi()
    coily = TuneCoilyMethods()
    collabos = CollabOsBase()
    base_settings.BROWSER = 'safari'

    def open_app(self, teammate: bool = False):
        if global_variables.driver is None:
            global_variables.driver = self.open(teammate=teammate)
        else:
            self.home.click_back()
        return TuneMobileHome()

    def change_language(self, language: str):
        """
        Method to change language for LogiTune

        :param language:
        :return TuneMobileMethods:
        """
        tune_mobile_config.lanngauge = language
        if MobileBase.is_ios_device():
            self.phone_settings.change_language_ios(language)
        else:
            if language.lower() == "english":
                tune_mobile_config.locale = "EN"
            elif language.lower() == "italian":
                tune_mobile_config.locale = "IT"
            elif language.lower() == "french":
                tune_mobile_config.locale = "FR"
            elif language.lower() == "german":
                tune_mobile_config.locale = "DE"
            elif language.lower() == "spanish":
                tune_mobile_config.locale = "es"
            elif language.lower() == "portuguese":
                tune_mobile_config.locale = "PT"

    def get_desk_site(self, desk_name: str) -> str:
        """
        Method to get the site where desk is located

        :param desk_name:
        :return str:
        """
        try:
            return test_data.desks[desk_name]["site"]
        except KeyError as e:
            Report.logException(f"{desk_name} not found")

    def get_desk_building(self, desk_name: str) -> str:
        """
        Method to get the building where desk is located

        :param desk_name:
        :return str:
        """
        try:
            return test_data.desks[desk_name]["building"]
        except KeyError as e:
            Report.logException(f"{desk_name} not found")

    def get_desk_floor(self, desk_name: str) -> str:
        """
        Method to get the floor where desk is located

        :param desk_name:
        :return str:
        """
        try:
            return test_data.desks[desk_name]["floor"]
        except KeyError as e:
            Report.logException(f"{desk_name} not found")

    def get_desk_workspace(self, desk_name: str) -> str:
        """
        Method to get the workspace where desk is located

        :param desk_name:
        :return str:
        """
        try:
            return test_data.desks[desk_name]["workspace"]
        except KeyError as e:
            Report.logException(f"{desk_name} not found")

    def book_desk_by_location(self, desk_name: str, start: str, end: str, day=0, verification: bool = True,
                              notify_teammate: bool = False, custom_message: str = None, emoji_count: int = 0):
        """
        Method to Book a desk desk_name by location with start_in time for duration

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param verification:
        :param notify_teammate:
        :param custom_message:
        :param emoji_count:
        :return TuneMobileMethods:
        """
        self.delete_all_bookings_through_sync_portal(desk_name=desk_name)
        teammates = ''
        if verification or notify_teammate:
            teammates = self.dashboard.click_people().click_teammates().click_all_teammates().get_teammates_list()
            self.people.click_back()
        self.dashboard.click_home()
        # if day > 0:
        #     self.dashboard.click_expand_calendar()
        self.dashboard.click_date(day=day)
        self.dashboard.click_book().click_by_location_and_preferences()
        self._book_desk(desk_name, start, end, teammates, verification=verification,
                        notify_teammate=notify_teammate, custom_message=custom_message, emoji_count=emoji_count)
        return self

    def book_desk_near_teammate(self, teammate: str, desk_name: str, start: str, end: str, day=0,
                                verification: bool = True, notify_teammate: bool = False, custom_message: str = None):
        """
        Method to Book a desk desk_name by location with start_in time for duration

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param teammate:
        :param verification:
        :return TuneMobileMethods:
        """
        self.delete_all_bookings_through_sync_portal(desk_name=desk_name)
        teammates = ''
        if verification or notify_teammate:
            teammates = self.dashboard.click_people().click_teammates().click_all_teammates().get_teammates_list()
            self.people.click_back()
        self.dashboard.click_home()
        self.dashboard.click_date(day=day)
        self.dashboard.click_book().click_near_teammate()
        if self.people.verify_no_teammates_in_office(): #Some times booking by teammate not updated - workaround
            self.people.click_back()
            self.dashboard.click_book().click_near_teammate()
        self.people.click_teammate(teammate=teammate, booking=True)
        self.book.click_teammate_schedule(schedule=f"{start} - {end}")
        if self.is_android_device():
            if not self.book.verify_book_button():
                self.book.click_back().click_teammate_schedule(schedule=f"{start} - {end}")
        self._book_desk(desk_name, start, end, teammates, verification=verification,
                        notify_teammate=notify_teammate, custom_message=custom_message,
                        change_schedule=False, change_desk=False)
        return self

    def book_desk_near_teammate_from_people_screen(self, teammate: str, desk_name: str, start: str, end: str, day=0,
                                verification: bool = True, notify_teammate: bool = False, custom_message: str = None,
                                                   office: bool = False):
        """
        Method to Book a desk desk_name near teammate from People screen

        :param teammate:
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param verification:
        :param notify_teammate:
        :param custom_message:
        :param office:
        :return TuneMobileMethods:
        """
        self.delete_all_bookings_through_sync_portal(desk_name=desk_name)
        teammates = ''
        if verification or notify_teammate:
            teammates = self.dashboard.click_people().click_teammates().click_all_teammates().get_teammates_list()
            self.people.click_back()
        self.dashboard.click_home()
        self.dashboard.click_date(day=day)
        if office:
            self.dashboard.click_teammates_in_office()
        else:
            self.dashboard.click_people().click_all_teammates()
        self.people.click_teammate(teammate=teammate, booking=True)
        self.verify_people_booking_profile(desk_name=desk_name, start=start, end=end, day=day)
        self.book.click_teammate_schedule(schedule=f"{start} - {end}")
        if self.is_android_device():
            if not self.book.verify_book_button():
                self.book.click_back().click_teammate_schedule(schedule=f"{start} - {end}")
        self._book_desk(desk_name, start, end, teammates, verification=verification,
                        notify_teammate=notify_teammate, custom_message=custom_message,
                        change_schedule=False, change_desk=False)
        return self

    def verify_people_booking_profile(self, desk_name: str, start: str, end: str, day=0):
        """
        Method to Book a desk desk_name near teammate from People screen

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return TuneMobileMethods:
        """
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        # location = f"{building} · {floor} · {area}" if self.is_android_device() else f"{building}"
        location = f"{building}"
        verification = self.book.verify_desk_booked_schedule(schedule=f"{start} - {end}")
        self.report_displayed_or_not(f"Schedule {start} - {end}", verification=verification)
        verification = self.book.verify_desk_booked_schedule(schedule=location)
        self.report_displayed_or_not(f"Location - {location}", verification=verification)
        verification = self.book.verify_desk_booked_day(schedule=f"{start} - {end}", day=day)
        day_value = "Today" if day == 0 else "Tomorrow"
        self.report_displayed_or_not(f"Day {day_value}", verification=verification)

    def _book_desk(self, desk_name: str, start: str, end: str, teammates, verification: bool = True,
                   notify_teammate: bool = False, custom_message: str = None, change_schedule: bool = True,
                   change_desk: bool = True, emoji_count: int = 0):
        """
        Method to Book a desk desk_name by location with start_in time for duration

        :param desk_name:
        :param start:
        :param end:
        :param teammates:
        :param verification:
        :return :
        """
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        if self.is_ios_device() and start != '' and change_schedule:
            time.sleep(2)
            self.book.click_calendar_icon()
            time.sleep(2)
            if self.compare_time_values(end, '5:00 PM'):
                self.book.adjust_end_time(end)
                self.book.adjust_start_time(start)
            else:
                self.book.adjust_start_time(start)
                self.book.adjust_end_time(end)
            self.book.click_confirm()
        if change_desk:
            self.book.click_list()
            if building != self.book.get_selected_building():
                self.book.change_building(site_name=site, building_name=building)
            if floor != self.book.get_selected_floor():
                self.book.change_floor(floor_name=floor)
            self.book.click_workspace(workspace=area)
            self.book.click_desk(desk_name)
            start = self.book.get_booking_start()
            end = self.book.get_booking_end()
        self.book.click_book()
        if verification:
            verification = self.book.verify_notify_teammates_screen()
            self.report_displayed_or_not(f"Notify Teammates screen", verification)
            if len(teammates) == 0:
                verification = self.book.verify_notify_teammates_title()
                self.report_displayed_or_not(f"No teammates added", verification)
                verification = self.book.verify_notify_teammates_message()
                self.report_displayed_or_not(f"Add people to teammates message", verification)
            else:
                for teammate in teammates:
                    verification = self.book.verify_notify_teammates_teammate_name(teammate_name=teammate)
                    self.report_displayed_or_not(f"Teammate Name: {teammate}", verification)
        if notify_teammate:
            self.notifify_teammate_flow(teammates=teammates, custom_message=custom_message, emoji_count=emoji_count)
        else:
            if self.book.verify_skip():
                self.book.click_skip()
            else:
                self.book.click_notify_teammate()
        if verification:
            verification = self.book.verify_desk_booked_screen(desk_name=desk_name)
            self.report_displayed_or_not(f"Desk {desk_name} booked screen", verification)
            verification = self.book.verify_desk_booked_message()
            self.report_displayed_or_not(f"Your desk will be waiting message", verification, screenshot=False)
            verification = self.book.verify_desk_booked_schedule(schedule=f'{start} - {end}')
            if not verification:
                s1 = int(start.split(':')[1].split(' ')[0]) + 1
                if s1 < 10:
                    s1 = f"0{s1}"
                start = f"{start.split(':')[0]}:{s1} {start.split(' ')[1]}"
                verification = self.book.verify_desk_booked_schedule(schedule=f'{start} - {end}')
            self.report_displayed_or_not(f"Schedule {start} - {end}", verification, screenshot=False)
            if notify_teammate:
                verification = self.book.verify_teammate_notified_message()
                self.report_displayed_or_not("Teammate notifified message", verification, screenshot=False)
                verification = self.book.verify_notification_sent_message()
                self.report_displayed_or_not("Notification sent to teammate message", verification, screenshot=False)
        if notify_teammate and custom_message is not None:
            verification = self.book.verify_custom_message(custom_message=custom_message)
            self.report_displayed_or_not(f"{custom_message} message", verification, screenshot=False)
        self.book.click_done()
        if self.settings.verify_continue():
            self.settings.click_continue()
        if verification:
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)

    def verify_booking_card(self, desk_name: str, start: str, end: str):
        """
        Method to verify booking card details

        :param :
        :return bool:
        """
        self.dashboard.click_home()
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        time.sleep(2)
        verification = self.dashboard.verify_booking_card_desk_name(desk_name)
        self.report_displayed_or_not(f"Booking card: Desk Name {desk_name}", verification)
        verification = self.dashboard.verify_booking_card_location(desk_name=desk_name, building=building,
                                                                   floor=floor, area=area)
        self.report_displayed_or_not(f"Booking card: Location {building} {floor} {area}", verification)
        verification = self.dashboard.verify_booking_card_schedule(desk_name=desk_name, start=start, end=end)
        self.report_displayed_or_not(f"Booking card: Schedule", verification)

    def notifify_teammate_flow(self, teammates, custom_message: str = None, emoji_count: int = 0):
        """
        Method to 'Notify Teammate flow' and notify teammate with custom text

        :param teammates:
        :param custom_message:
        :param emoji_count:
        :return bool:
        """
        for teammate in teammates:
            self.book.toggle_notify_teammate(teammate=teammate)
        verification = self.book.verify_notify_teammates_button()
        self.report_displayed_or_not("Notify Teammates button", verification=verification)
        verification = self.book.verify_message_textbox()
        self.report_displayed_or_not("Optional message textbox", verification=verification)
        verification = self.book.verify_include_message_text()
        self.report_displayed_or_not("Include message (0/128)", verification=verification)
        if custom_message is not None:
            self.book.input_custom_message(custom_message=custom_message)
            verification = self.book.verify_notify_with_message_button()
            self.report_displayed_or_not("Notify with message button", verification=verification)
            char_count = len(custom_message)
            # if self.is_ios_device():
            char_count += emoji_count*3
            char_count = 128 if char_count >= 128 else char_count
            verification = self.book.verify_include_message_text(count=char_count)
            self.report_displayed_or_not(f"Include message ({char_count}/128)", verification=verification)
            self.book.click_notify_with_message()
        else:
            self.book.click_notify_teammate()

    def notify_teammate_booking_popup(self, desk_name: str, custom_message: str = None, emoji_count: int = 0):
        """
        Method to 'Notify Teammate' from edit booking with custom message

        :param custom_message:
        :param emoji_count:
        :return bool:
        """
        teammates = self.dashboard.click_people().click_teammates().click_all_teammates().get_teammates_list()
        self.people.click_back()
        self.dashboard.click_home()
        self.dashboard.click_details(desk_name=desk_name)
        self.dashboard.click_notify_teammates()
        self.notifify_teammate_flow(teammates=teammates, custom_message=custom_message, emoji_count=emoji_count)

    def get_start_end_time(self, booking_duration: int = 2):
        def min_rounder(t):
            min = t.minute
            return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour + 1)
                    + timedelta(hours=t.minute // 30))

        t = datetime.now()
        start_time = min_rounder(t)
        end_time = min_rounder(t + timedelta(hours=booking_duration))
        start = start_time.strftime("%I:%M %p").lstrip('0')
        end = end_time.strftime("%I:%M %p").lstrip('0')
        print(start)
        print(end)
        return start, end

    def compare_time_values(self, time1: str, time2: str) -> bool:
        """
        Method to compare two time values and return True if time1 > time2 else false

        :param :
        :return bool:
        """
        time1 = datetime.strptime(time1, '%I:%M %p').time()
        time2 = datetime.strptime(time2, '%I:%M %p').time()
        return True if time1 > time2 else False

    def cancel_booking(self, desk_name: str, day: int = 0, future_booking: bool = False, verification: bool = True):
        """
        Method to End current booking or Cancel Future booking

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param future_booking:
        :param verification:
        :return TuneMobileMethods:
        """
        self.dashboard.click_date(day=day)
        if verification:
            floor = self.dashboard.get_booking_card_floor(desk_name=desk_name)
            area = self.dashboard.get_booking_card_area(desk_name=desk_name)
            start = self.dashboard.get_booking_card_schedule_start(desk_name=desk_name)
            end = self.dashboard.get_booking_card_schedule_end(desk_name=desk_name)
        self.dashboard.click_details(desk_name=desk_name)
        if verification:
            self.verify_modify_booking_screen(desk_name=desk_name, start=start, end=end, future_booking=future_booking)
            self.dashboard.click_details(desk_name=desk_name)
        if future_booking:
            self.dashboard.click_cancel_session().click_yes_cancel()
        else:
            self.dashboard.click_end_session().click_yes_end()
        if verification:
            verification = self.dashboard.verify_booking_cancelled_confirmation()
            self.report_displayed_or_not(f"Booking cancelled message", verification)
            verification = self.dashboard.verify_booking_cancelled_message()
            self.report_displayed_or_not(f"You're all set! message", verification, screenshot=False)
        self.dashboard.click_ok()
        if not self.dashboard.verify_booking_card_desk_name(desk_name=desk_name, timeout=2):
            Report.logPass("Booking removed on tapping Yes button", screenshot=True)
        else:
            Report.logFail("Booking not removed on tapping Yes button")
        return self

    def edit_booking(self, desk_name: str, start: str, end: str, day: int = 0,
                     future_booking: bool = True, verification: bool = True):
        """
        Method to End current booking or Cancel Future booking

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param future_booking:
        :param verification:
        :return TuneMobileMethods:
        """
        self.dashboard.click_details(desk_name=desk_name)
        self.dashboard.click_edit_booking()
        if verification:
            condition = self.book.verify_edit_booking()
            self.report_displayed_or_not("Edit Booking screen", verification=condition)
        if not future_booking:
            pass
            #Add verification for calendar not displayed
        self.book.click_date(day=day)
        if start != '':
            self.book.adjust_start_time(start_time=start)
        if end != '':
            self.book.adjust_end_time(end_time=end)
        self.book.click_update_booking()
        if verification:
            condition = self.book.verify_booking_updated()
            self.report_displayed_or_not("Booking updated screen", verification=condition)
        self.book.click_ok()
        return self

    def check_in_desk(self, desk_name: str):
        """
        Method to check in desk from Tune Mobile

        :param desk_name:
        :return TuneMobileMethods:
        """
        verification = self.book.verify_check_in_message()
        self.report_displayed_or_not("Message - Are you trying to check in?", verification)
        verification = self.book.verify_check_in_desk_name(desk_name=desk_name)
        self.report_displayed_or_not(f"Correct Desk Name - {desk_name}", verification, screenshot=False)
        self.book.click_check_in()
        time.sleep(2)
        verification = self.book.verify_check_in_success_message(desk_name=desk_name)
        self.report_displayed_or_not(f"Message - Checked in to desk {desk_name}", verification)
        verification = self.book.verify_check_in_all_set()
        self.report_displayed_or_not(f"Message - You're all set!", verification, screenshot=False)
        self.book.click_check_in_ok()
        return self

    def coily_check_in(self, coily_ip: str):
        """
        Method to check 0in desk from Coily

        :param coily_ip:
        :return TuneMobileMethods:
        """
        self.collabos.connect_to_collabos_app(device_ip=coily_ip, port=tune_mobile_config.port)
        Report.logPass("Coily Booked desk screen", screenshot=True, is_collabos=True)
        self.coily.home.click_check_in()
        self.coily.home.click_back()
        time.sleep(2)
        return self

    def verify_modify_booking_screen(self, desk_name: str, start: str, end: str, future_booking: bool = False,
                                     cancel_booking: bool = True):
        """
        Method to End current booking or Cancel Future booking

        :param desk_name:
        :param start:
        :param end:
        :param future_booking:
        :param cancel_booking:
        :return TuneMobileMethods:
        """
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        verification = self.dashboard.verify_mofify_booking_desk_image()
        self.report_displayed_or_not("Modify Booking: Desk image", verification)
        verification = self.dashboard.verify_modify_booking_desk_name(desk_name=desk_name)
        self.report_displayed_or_not(f"Modify Booking: Desk name {desk_name}", verification, screenshot=False)
        verification = self.dashboard.verify_modify_booking_location(floor=floor, area=area)
        self.report_displayed_or_not(f"Modify Booking: Location {floor} {area}", verification, screenshot=False)
        if start != '' and self.is_android_device():
            verification = self.dashboard.verify_modify_booking_schedule(start=start, end=end)
            self.report_displayed_or_not(f"Modify Booking: Schedule {start}-{end}", verification, screenshot=False)
        verification = self.dashboard.verify_edit_booking()
        self.report_displayed_or_not(f"Modify Booking: Edit Booking button", verification, screenshot=False)
        verification = self.dashboard.verify_show_on_maps()
        self.report_displayed_or_not(f"Modify Booking: Show on maps", verification, screenshot=False)
        verification = self.dashboard.verify_teammates_near_by()
        self.report_displayed_or_not(f"Modify Booking: Teammates nearby", verification, screenshot=False)
        if cancel_booking:
            if future_booking:
                verification = self.dashboard.verify_cancel_session()
                self.report_displayed_or_not(f"Modify Booking: Cancel session button", verification, screenshot=False)
                self.dashboard.click_cancel_session()
                verification = self.dashboard.verify_cancel_session_message()
                self.report_displayed_or_not(f"Cancel session: Cancel your booking message", verification)
            else:
                verification = self.dashboard.verify_end_session()
                self.report_displayed_or_not(f"Modify Booking: End session button", verification, screenshot=False)
                self.dashboard.click_end_session()
                verification = self.dashboard.verify_end_session_message()
                self.report_displayed_or_not(f"End session: End your booking message", verification)
            self.dashboard.click_no_keep()
            if self.is_android_device():
                self.dashboard.click_bottom_sheet_close()
            if self.dashboard.verify_booking_card_desk_name(desk_name=desk_name):
                Report.logPass("Booking not removed on tapping No button", screenshot=True)
            else:
                Report.logFail("Booking removed on tapping No button")
        else:
            self.dashboard.click_bottom_sheet_close()
        return self

    def validate_teammates_in_office(self, user_name: str, desk_name: str, start: str, end: str,
                                     day: int = 0, teammate: bool = True):
        """
        Method to validate teammates in office and Booked desk details

        :param :
        :return TuneMobileMethods:
        """
        self.dashboard.click_date(day=day).click_teammates_in_office()
        if self.is_android_device():
            if self.people.verify_no_teammates_in_office():
                self.people.click_back()
                self.dashboard.click_teammates_in_office()
        if not teammate:
            self.people.click_everyone()
        self._validate_teammate_booking(user_name=user_name, desk_name=desk_name, start=start, end=end, day=day)
        self.people.click_back()

    def validate_teammates_nearby(self, teammate_name: str, other_name: str,
                                  user_desk: str, teammate_desk: str, other_desk: str,
                                  start: str, end: str, day: int = 0, nearby: bool = True):
        """
        Method to validate teammates in office and Booked desk details

        :param teammate_name:
        :param other_name:
        :param user_desk:
        :param teammate_desk:
        :param other_desk:
        :param start:
        :param end:
        :param day:
        :param nearby:
        :return TuneMobileMethods:
        """
        self.dashboard.click_date(day=day).click_details(desk_name=user_desk).click_teammates_near_by()
        if nearby:
            self._validate_teammate_booking(user_name=teammate_name, desk_name=teammate_desk, start=start, end=end, day=day)
            self.people.click_everyone()
            self._validate_teammate_booking(user_name=other_name, desk_name=other_desk, start=start, end=end, day=day)
        else:
            verification = self.people.verify_no_teammates_in_area()
            self.report_displayed_or_not("No Teammates in this area", verification)
            self.people.click_everyone()
            verification = self.people.verify_no_people_in_area()
            self.report_displayed_or_not("No People in this area", verification)
        self.people.click_back()
        if self.is_android_device():
            self.dashboard.click_bottom_sheet_close()
        return self

    def _validate_teammate_booking(self, user_name: str, desk_name: str, start: str, end: str, day: int = 0):
        """
        Method to validate teammate Booked desk details

        :param :
        :return TuneMobileMethods:
        """
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        verification = self.people.verify_user_name(user_name=user_name)
        self.report_displayed_or_not(f"Name {user_name}", verification)
        if self.is_android_device():
            # Workaround Issue with iOS Locator, remove condition after fix
            verification = self.people.verify_user_booking(start=start, end=end, floor=floor, area=area,
                                                           desk_name=desk_name)
            self.report_displayed_or_not(f"Booking details", verification)
        self.people.click_teammate(teammate=user_name, booking=True)
        self.verify_people_booking_profile(desk_name=desk_name, start=start, end=end, day=day)
        self.people.click_back()

    def verify_equalizer_options(self):
        """
        Method to verify default Equalizer options

        :param :
        :return TuneMobileMethods:
        """
        verification = self.equalizer.verify_default_option()
        self.report_displayed_or_not("Eualizer option: Default", verification)
        verification = self.equalizer.verify_volume_boost_option()
        self.report_displayed_or_not("Eualizer option: Volume Boost", verification, screenshot=False)
        verification = self.equalizer.verify_podcast_option()
        self.report_displayed_or_not("Eualizer option: Podcast", verification, screenshot=False)
        verification = self.equalizer.verify_bass_boost_option()
        self.report_displayed_or_not("Eualizer option: Bass Boost", verification)
        verification = self.equalizer.verify_custom_option()
        self.report_displayed_or_not("Eualizer option: Custom", verification, screenshot=False)
        return self

    def verify_equalizer_preset(self, preset: str):
        """
        Method to verify Slider Values are set correctly based on Preset

        :param preset:
        :return TuneMobileMethods:
        """
        factor = 6 if MobileBase.device.lower() == "iphone15" else 0
        eq1_value = self.equalizer.get_eq_slider1_value() + factor
        eq2_value = self.equalizer.get_eq_slider2_value() + factor
        eq3_value = self.equalizer.get_eq_slider3_value() + factor
        eq4_value = self.equalizer.get_eq_slider4_value() + factor
        eq5_value = self.equalizer.get_eq_slider5_value() + factor

        if preset.lower() == "default":
            verification = not any([eq1_value, eq2_value, eq3_value, eq4_value, eq5_value])
            self.report_displayed_or_not("Correct Preset values for Defauilt EQ", verification)
        elif preset.lower() == "volume boost":
            verification = (eq1_value == eq2_value == eq3_value == eq4_value == eq5_value == 81) if self.is_ios_device() \
                else (eq1_value == eq2_value == eq3_value == eq4_value == eq5_value == 127)
            self.report_displayed_or_not("Correct Preset values for Volume Boost EQ", verification)
        elif preset.lower() == "podcast":
            verification = (eq1_value == 0 and eq2_value == 18 and eq3_value == 73 and
                            eq4_value == 81 and eq5_value == 55) if self.is_ios_device() else \
                (eq1_value == 0 and eq2_value == 25 and eq3_value == 102 and eq4_value == 127 and eq5_value == 76)
            self.report_displayed_or_not("Correct Preset values for Podcast EQ", verification)
        elif preset.lower() == "bass boost":
            verification = (eq1_value == 81 and
                            eq2_value == 55 and eq3_value == eq4_value == eq5_value == 18) if self.is_ios_device() else \
                (eq1_value == 127 and eq2_value == 76 and eq3_value == eq4_value == eq5_value == 25)
            self.report_displayed_or_not("Correct Preset values for Bass Boost EQ", verification)
        return self

    def create_custom_equalizer(self, preset_name: str, eq1_value: int = 0, eq2_value: int = 0,
                                eq3_value: int = 0, eq4_value: int = 0, eq5_value: int = 0, preset_limit=False):
        """
        Method to verify Slider Values are set correctly based on Preset

        :param eq1_value:
        :param eq2_value:
        :param preset_limit:
        :param eq5_value:
        :param eq4_value:
        :param eq3_value:
        :param preset_name:
        :return TuneMobileMethods:
        """
        self.equalizer.click_default()
        self.equalizer.adjust_eq_slider1(eq1_value)
        self.equalizer.adjust_eq_slider2(eq2_value)
        self.equalizer.adjust_eq_slider3(eq3_value)
        self.equalizer.adjust_eq_slider4(eq4_value)
        self.equalizer.adjust_eq_slider5(eq5_value)
        self.equalizer.click_save_custom_preset()
        if preset_limit:
            self.report_displayed_or_not(f"Preset limit pop up", self.equalizer.verify_preset_limit_popup())
            self.report_displayed_or_not(f"Preset limit message", self.equalizer.verify_preset_limit_message())
            self.equalizer.click_got_it()
        else:
            self.equalizer.type_preset_name(preset_name).click_save_button()
        return self

    def delete_custom_equalizer(self, preset_name: str):
        """
        Method to delete custom equalizer

        :param preset_name:
        :return TuneMobileMethods:
        """
        self.equalizer.click_edit_presets().click_delete_preset(preset_name)
        time.sleep(2)
        if self.equalizer.verify_done_displayed():
            self.equalizer.click_done()
        return self

    def delete_all_custom_equalizers(self):
        """
        Method to delete all custom presets

        :param preset_name:
        :return TuneMobileMethods:
        """
        self.equalizer.click_edit_presets().click_all_delete_presets()
        time.sleep(2)
        if self.equalizer.verify_done_displayed():
            self.equalizer.click_done()
        return self

    def is_correct_headset_connected(self, headset: str) -> bool:
        """
        Method to verify correct headset is connected to app

        :param headset:
        :return bool:
        """
        try:
            name = self.home.get_device_name_value()
            if name == headset:
                return True
            self.close()
            self.phone_settings.open()
            self.phone_settings.disconnect_all_bluetooth_devices()
            self.phone_settings.connect_bluetooth_device(headset)
            self.phone_settings.close()
            name = self.open_app().get_device_name_value()
            if name == headset:
                return True
            else:
                return False
        except Exception as e:
            self.phone_settings.open()
            self.phone_settings.disconnect_all_bluetooth_devices()
            self.phone_settings.connect_bluetooth_device(headset)
            self.phone_settings.close()
            return False

    def validate_search(self, search_text: str, no_results: bool = False, teammates: bool = True, email: bool = False):
        """
        Method to validate correct search results displayed

        :param search_text:
        :return :
        """
        if self.people.verify_clear_search():
            self.people.click_clear_search()
        original_list = self.people.get_teammates_list() if teammates else self.people.get_user_groups_list()
        self.people.type_in_search(search_text)
        if no_results:
            self.report_displayed_or_not(f"No search results message for {search_text}",
                                         self.people.verify_no_results_message())
        else:
            results = self.people.get_teammates_list() if teammates else self.people.get_people_list()
            if len(results) == 0:
                flag = False
            else:
                flag = True
                for result in results:
                    search_result = result.lower()
                    if email:
                        email_result = self.people.click_teammate(result).get_teammate_email(result)
                        self.people.click_back()
                        search_result = email_result.lower()
                    if search_text.lower() in search_result or search_text.lower() in result.lower():
                        continue
                    else:
                        Report.logFail(f"Incorrect search result {search_result} for {search_text}")
                        flag = False
            if flag:
                Report.logPass(f"Correct search results displayed for {search_text}", True)
            else:
                Report.logFail(f"Incorrect search results displayed for {search_text}")
        # Workaround for Android bug
        if self.is_ios_device():
            self.people.click_clear_search()
        else:
            self.people.type_in_search("")
        # Workaround for Android bug
        if teammates:
            # self.people.scroll_to_top()
            # time.sleep(1)
            search_clear_list = self.people.get_teammates_list()
            result = deepdiff.DeepDiff(original_list, search_clear_list, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass("All teammates displayed on clearing search text")
            else:
                Report.logFail("Not all teammates displayed on clearing search text")
        else:
            search_clear_list = self.people.get_user_groups_list()
            result = deepdiff.DeepDiff(original_list, search_clear_list, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass("Groups displayed correctly on clearing search text")
            else:
                Report.logFail("Groups not displayed correctly on clearing search text")

    def validate_remove_teammate(self, teammate: str, everyone_tab: bool = False, custom: bool = False):
        """
        Method to validate remove teammate functionality

        :param teammate:
        :param everyone_tab:
        :param custom:
        :return :
        """
        self.people.click_teammate(teammate=teammate, booking=custom).click_remove_from_team()
        self.report_displayed_or_not("Remove Teammate message", self.people.verify_remove_message())
        self.report_displayed_or_not("Your list of Teammates is only visible to you",
                                     self.people.verify_remove_message())
        self.report_displayed_or_not("Cancel button", self.people.verify_cancel_button())
        self.report_displayed_or_not("Remove button", self.people.verify_remove_button())
        self.people.click_cancel()
        if everyone_tab:
            self.people.click_back().click_teammates().click_all_teammates()
        else:
            self.people.click_back()
        teammates = self.people.get_teammates_list(custom_team=custom)
        if teammate in teammates:
            Report.logPass(f"Teammate {teammate} not removed on tapping Cancel", True)
        else:
            Report.logFail(f"Teammate {teammate} removed on tapping Cancel")
        if everyone_tab:
            self.people.click_back().click_everyone()
        self.people.click_teammate(teammate=teammate, booking=custom).click_remove_from_team().click_remove()
        if everyone_tab:
            self.people.click_back().click_teammates().click_all_teammates()
        else:
            self.people.click_back()
        teammates = self.people.get_teammates_list(custom_team=custom)
        if teammate in teammates:
            Report.logFail(f"Teammate {teammate} not removed on tapping Remove")
        else:
            Report.logPass(f"Teammate {teammate} removed on tapping Remove")

    def sign_in_to_google_account(self, email: str, verification: bool = True):
        """
        Method to sign in to google account

        :param email:
        :return :
        """
        self.settings.click_google()
        if self.is_ios_device():
            self.settings.click_continue()
        if verification:
            self.report_displayed_or_not("Sign in with Google screen",
                                         self.settings.verify_sign_in_with_google_screen())
        if self.is_android_device() and self.settings.verify_dismiss():
            self.settings.click_dismiss()
        self.settings.click_google_email(email=email)
        if "gmail.com" in email.lower():
            self.settings.click_continue(timeout=15)
            self.report_displayed_or_not("Logi Tune wants access to your Google Account",
                                         self.settings.verify_google_access_message())
            self.swipe_screen('vertical', 0.8, 0.2)
            if not self.settings.verify_continue():
                self.swipe_screen('vertical', 0.8, 0.2)
            self.settings.click_continue()
            if self.is_android_device() and not self.settings.verify_booking_welcome_screen() \
                    and self.settings.verify_continue():
                self.settings.click_continue()
        else:
            self.settings.click_continue()
            self.report_displayed_or_not("Logi Tune wants access to your Google Account",
                                         self.settings.verify_google_allow_message())
            self.swipe_screen('vertical', 0.8, 0.2)
            self.settings.click_allow()
        time.sleep(2)
        if verification:
            self.report_displayed_or_not("Welcome to Logitech Desk Booking",
                                         self.settings.verify_booking_welcome_screen())
            self.report_displayed_or_not(
                "Book desks in the office, find where your teammates sit, check your agenda, join meetings, and manage Logitech devices.",
                self.settings.verify_booking_welcome_screen())

    def sign_in_to_microsoft_account(self, email: str, verification: bool = True, auth: bool = False):
        """
        Method to sign in to google account

        :param email:
        :return :
        """
        try:
            self.settings.click_microsoft()
            if self.is_ios_device():
                self.settings.click_continue()
            self.report_displayed_or_not("Sign in with Microsoft screen",
                                         self.settings.verify_sign_in_with_microsoft_screen())
            self.settings.type_microsoft_email(email=email)
            if self.settings.verify_microsoft_access_message():
                self.report_displayed_or_not("Permissions requested message",
                                             self.settings.verify_microsoft_access_message())
                self.swipe_screen('vertical', 0.8, 0.2)
                if auth:
                    self.settings.click_ask_later()
                self.settings.click_accept(timeout=15)
            time.sleep(3)
            if not self.settings.verify_booking_welcome_screen():
                time.sleep(15)
            if verification:
                self.report_displayed_or_not("Welcome to Logitech Desk Booking",
                                             self.settings.verify_booking_welcome_screen())
                self.report_displayed_or_not(
                    "Book desks in the office, find where your teammates sit, check your agenda, join meetings, and manage Logitech devices.",
                    self.settings.verify_booking_welcome_screen())
        except:
            if self.is_android_device():
                Report.logScreenshot(folder="images", screenshot_name="accept", logText="MS")
                x, y = TuneMobileImage.get_coordinates(image_path=f"{global_variables.reportPath}/images/accept.jpg")
                self.tap_by_coordinates(x=x, y=y)
                time.sleep(3)

    def verify_signin_building(self, site_name: str, building_name: str):
        """
        Method to verify building screen during Sign in

        :param site_name:
        :param building_name:
        :return :
        """
        self.report_displayed_or_not("Search bar", self.building.verify_search())

    def verify_signin_teammates(self, teammates: list, verification=True):
        """
        Method to verify Teammates screen during Sign in

        :param teammates:
        :return :
        """
        self.settings.click_continue()
        if verification:
            self.report_displayed_or_not("Search bar", self.people.verify_search_control_displayed())
            self.report_displayed_or_not("Teammates title", self.people.verify_teammates_title())
        for teammate in teammates:
            self.people.type_in_search(search_text=teammate)
            self.people.click_teammate(teammate=teammate)
            self.people.click_clear_search()
        self.settings.click_done()

    def change_user_group(self, user: str, group: str):
        """
        Method to update user group

        :param user:
        :param group: (string separated by comma for multiple groups)
        :return :
        """
        self.sync_portal.login_to_sync_portal(config=global_variables.config, role="AladdinOwner")
        groups = self.sync_portal.change_end_user_group(user=user, group=group)
        self.sync_portal.browser.close_browser()
        global_variables.driver = None
        return groups

    def get_active_user_groups(self):
        """
        Method to get active end user groups in Sync Portal

        :param :
        :return :
        """
        if global_variables.driver is not None:
            global_variables.driver.quit()
        self.sync_portal.login_to_sync_portal(config=global_variables.config, role="AladdinOwner")
        groups = self.sync_portal.get_active_end_user_groups()
        self.sync_portal.browser.close_browser()
        global_variables.driver = None
        return groups

    def _login_to_sync_portal(self):
        """
        Method to log in to Sync Portal

        :param :
        :return :
        """
        browser = BrowserClass()
        browser.prepare_opened_browser()
        driverRaw = browser.connect_to_current_browser_page()
        global_variables.driver = EventFiringWebDriver(driverRaw, CustomBrowserListener())
        global_variables.driver.maximize_window()
        global_variables.driver.get(global_variables.config.BASE_URL)
        if not self.sync_portal.inventory.verify_search_box_displayed():
            SyncPortalLogin().login(config=global_variables.config, role="AladdinOwner")

    def _close_sync_portal(self):
        """
        Method to log in to Sync Portal

        :param :
        :return :
        """
        global_variables.driver.close()
        global_variables.driver.quit()
        global_variables.driver = None

    def verify_teammate_desk_booking_notification(self, custom_message: str = None):
        """
        Method to verify notification received for teammate desk booking

        :param custom_message:
        :return :
        """
        self.dashboard.click_notification()
        verification = self.notification.verify_book_nearby_button()
        self.report_displayed_or_not("Book Desk Nearby button", verification)
        if custom_message is None:
            verification = self.notification.verify_book_nearby_description()
            self.report_displayed_or_not("Would you like to book a desk near teammate", verification)
        else:
            verification = self.notification.verify_custom_message(custom_message=custom_message[0:128])
            message = numpy.unicode(custom_message.encode('utf-8'), 'utf-8')
            self.report_displayed_or_not(f"{message}", verification)
        self.notification.click_clear_all().click_confirm_clear_all()
        self.notification.click_close()

    def verify_teammate_cancels_booking_notification(self, teammate_name: str, desk_name: str, start: str, end: str):
        """
        Method to verify notification received for teammate cancels booking

        :param teammate_name:
        :param desk_name:
        :param start:
        :param end:
        :return :
        """
        self.dashboard.click_notification()
        verification = self.notification.verify_modify_booking_button()
        self.report_displayed_or_not("Modify Booking button", verification)
        verification = self.notification.verify_teammate_cancelled_message(teammate_name=teammate_name)
        self.report_displayed_or_not(f"{teammate_name} cancelled their booking", verification)
        verification = self.notification.verify_teammate_cancelled_description()
        self.report_displayed_or_not("Would you like to modify your booking?", verification)
        self.notification.click_modify_booking()
        self.verify_modify_booking_screen(desk_name=desk_name, start=start, end=end, cancel_booking=False)
        self.notification.click_clear_all().click_confirm_clear_all()
        self.notification.click_close()

    def verify_teammate_changed_booking_notification(self, teammate_name: str):
        """
        Method to verify notification received for teammate updates booking

        :param teammate_name:
        :return :
        """
        self.dashboard.click_notification()
        verification = self.notification.verify_teammate_changed_message(teammate_name=teammate_name)
        self.report_displayed_or_not(f"{teammate_name} changed a desk booking", verification)
        self.notification.click_clear_all().click_confirm_clear_all()
        self.notification.click_close()

    def verify_admin_creates_booking_notification(self):
        """
        Method to verify notification received for booking created by admin

        :param :
        :return :
        """
        self.dashboard.click_notification()
        verification = self.notification.verify_review_booking_button()
        self.report_displayed_or_not("Review Booking button", verification)
        verification = self.notification.verify_admin_booked_description()
        self.report_displayed_or_not("A desk booking made on your behalf by an administrator", verification)
        self.notification.click_close()

    def verify_admin_cancels_booking_notification(self):
        """
        Method to verify notification received for booking cancels by admin

        :param :
        :return :
        """
        verification = self.notification.verify_book_a_new_desk_button()
        self.report_displayed_or_not("Book A New Desk button", verification)
        verification = self.notification.verify_admin_cancelled_description()
        self.report_displayed_or_not("Your booking was cancelled by an administrator", verification, screenshot=False)
        verification = self.notification.verify_book_new_desk_description()
        self.report_displayed_or_not("Would you like to book a new desk?", verification, screenshot=False)
        self.notification.click_dismiss_notification()

    def verify_admin_updates_booking_notification(self, desk_name: str, start: str, end: str):
        """
        Method to verify notification received for booking updates by admin

        :param desk_name:
        :param start:
        :param end:
        :return :
        """
        verification = self.notification.verify_review_booking_button()
        self.report_displayed_or_not("Review Booking button", verification)
        verification = self.notification.verify_admin_updated_description()
        self.report_displayed_or_not("Your desk booking has been modified by an administrator", verification, screenshot=False)
        verification = self.notification.verify_review_booking_description()
        self.report_displayed_or_not("Review your updated booking and make any necessary changes", verification, screenshot=False)
        self.notification.click_review_booking()
        self.verify_modify_booking_screen(desk_name=desk_name, start=start, end=end, cancel_booking=False)
        self.notification.click_dismiss_notification()

    def verify_check_in_booking_notification(self, desk_name: str, start: str, end: str):
        """
        Method to verify notification received for booking updates by admin

        :param desk_name:
        :param start:
        :param end:
        :return :
        """
        verification = self.notification.verify_check_in_notification()
        self.report_displayed_or_not("You need to check-in at the desk", verification, screenshot=False)
        verification = self.notification.verify_check_in_description()
        self.report_displayed_or_not("To not lose your reservation, confirm it at the desk. Need to review or "
                                     "change your booking?", verification, screenshot=False)
        verification = self.notification.verify_modify_booking_button()
        self.report_displayed_or_not("Modify Booking button", verification)
        self.notification.click_modify_booking()
        self.verify_modify_booking_screen(desk_name=desk_name, start=start, end=end, cancel_booking=False)
        self.notification.click_dismiss_notification()

    def delete_all_bookings_through_sync_portal(self, desk_name: str):
        """
        Method to delete booking through Sync Portal (Raiden API)

        :param desk_name:
        :return :
        """
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        self.raiden_api.delete_bookings_for_desk(site=site, building=building, floor=floor, area=area,
                                                 desk_name=desk_name)

    def create_custom_team(self, team_name: str, validation: bool = True):
        """
        Method to create custom team from people screen

        :param team_name:
        :param verification:
        :return :
        """
        self.people.click_teammates().click_new_team()
        if not self.people.verify_create(): #Workaround for iOS 13 and Android 11 bug
            self.people.click_return_key()
        if validation:
            verification = self.people.verify_create_new_team()
            self.report_displayed_or_not("Create New Team title", verification)
            verification = self.people.verify_close()
            self.report_displayed_or_not("Close button", verification)
            verification = not self.people.verify_create_enabled()
            self.report_enabled_or_disabled("Create button", verification, False)
            verification = self.people.verify_team_name_text_field()
            self.report_displayed_or_not("Team name textfield", verification)
        self.people.type_team_name(team_name=team_name)
        if validation:
            verification = self.people.verify_create_enabled()
            self.report_enabled_or_disabled("Create button", verification, True)
        self.people.click_create()
        if validation:
            verification = self.people.verify_team_title(team_name=team_name)
            self.report_displayed_or_not(f"Team name {team_name}", verification)
            verification = self.people.verify_team_empty()
            self.report_displayed_or_not("The team is empty message", verification)
            verification = self.people.verify_add_few_teammates()
            self.report_displayed_or_not("Let’s add a few teammates message", verification)
            verification = self.people.verify_back()
            self.report_displayed_or_not("Back button", verification)
            verification = self.people.verify_add_teammates()
            self.report_displayed_or_not("Add teammates button", verification)
        self.people.click_back()
        verification = self.people.verify_custom_team(team_name=team_name)
        self.report_displayed_or_not(f"Custom team group {team_name}", verification)

    def verify_add_teammates_screen(self):
        """
        Method to validate Search Bar, Groups, Done button displayed in add teammates screen

        :param :
        :return :
        """
        self.people.click_add_teammates()
        verification = self.people.verify_done()
        self.report_displayed_or_not("Done button", verification)
        verification = self.people.verify_search()
        self.report_displayed_or_not("Search bar", verification)
        sync_user_groups = self.raiden_api.get_active_user_groups()
        mobile_user_groups = self.people.get_user_groups_list(add_teammates=True)
        result = deepdiff.DeepDiff(sync_user_groups, mobile_user_groups, ignore_string_case=True, ignore_order=True)
        if len(result) == 0:
            Report.logPass(f"User groups displayed correctly as per Sync Portal - {sync_user_groups}")
        else:
            Report.logFail(f"User groups not displayed correctly as per Sync Portal - "
                           f"{mobile_user_groups} vs {sync_user_groups}")
        self.people.click_done()

    def add_teammates_to_custom_team(self, team_name: str, teammates: list, verification: bool = True):
        """
        Method to add teammates to custom team

        :param team_name:
        :param teammates:
        :param verification:
        :return :
        """
        self.people.click_custom_team(team_name=team_name).click_add_teammates()
        for teammate in teammates:
            self.people.type_in_search(teammate).click_add(teammate)
            if verification:
                self.report_displayed_or_not(f'"ADDED" button next to {teammate}', self.people.verify_added(teammate))
            self.people.click_clear_search()
        self.people.click_done().click_back()

    def verify_update_team_name(self, team_name: str, new_team: str, teammates):
        """
        Method to validate Update button, Tick Mark, Edit button. delete icon next to teammate in edit team screen

        :param team_name:
        :param new_team:
        :param teammates: list of teammates
        :return :
        """
        self.people.click_edit()
        verification = self.people.verify_team_name_edit()
        self.report_displayed_or_not("Edit team button", verification)
        verification = self.people.verify_team_name_tick_mark()
        self.report_displayed_or_not("Tick Mark", verification)
        for name in teammates:
            verification = self.people.verify_delete_icon(teammate_name=name)
            self.report_displayed_or_not(f"Delete icon next to {name}", verification)
        verification = self.people.verify_delete_team()
        self.report_displayed_or_not("Delete team button", verification)
        self.people.click_team_name_edit()
        if not self.people.verify_team_name_update(): #Workaround for iOS 13 and Android 11 bug
            self.people.click_return_key()
        verification = not self.people.is_team_name_update_enabled()
        self.report_displayed_or_not("Disabled Update button", verification)
        self.people.type_team_name(team_name=new_team)
        verification = self.people.is_team_name_update_enabled()
        self.report_displayed_or_not("Update button enabled", verification)
        self.people.click_close()
        verification = self.people.verify_team_title(team_name=team_name)
        self.report_displayed_or_not(f"Original team name {team_name}", verification)
        self.people.click_team_name_edit()
        self.people.type_team_name(team_name=new_team)
        if not self.people.verify_team_name_update(): #Workaround for iOS 13 and Android 11 bug
            self.people.click_return_key()
        self.people.click_team_name_update()
        verification = self.people.verify_team_title(team_name=new_team)
        self.report_displayed_or_not(f"Updated team name {new_team}", verification)
        self.people.click_back()
        verification = self.people.verify_custom_team(team_name=new_team)
        self.report_displayed_or_not(f"Updated team name {new_team} in Teammates", verification)

    def verify_delete_team_name(self, team_name: str):
        """
        Method to validate delete custom team functionality

        :param team_name:
        :return :
        """
        self.people.click_edit().click_delete_team()
        verification = self.people.verify_delete_button()
        self.report_displayed_or_not("Delete button", verification)
        verification = self.people.verify_cancel_button()
        self.report_displayed_or_not("Cancel button", verification)
        verification = self.people.verify_delete_team_confirmation(team_name=team_name)
        self.report_displayed_or_not(f"Message - Delete the {team_name} team?", verification)
        verification = self.people.verify_delete_team_message()
        self.report_displayed_or_not("Message - Teammates will be removed from the team. This change is visible "
                                     "only for you.", verification)
        self.people.click_cancel()
        verification = self.people.verify_team_title(team_name=team_name)
        self.report_displayed_or_not(f"On Cancel, {team_name}", verification)
        self.people.click_delete_team().click_delete_button()
        verification = not self.people.verify_custom_team(team_name=team_name)
        self.report_displayed_or_not(f"Deleted team {team_name}", verification, displayed=False)

    @staticmethod
    def report_enabled_or_disabled(attribute: str, verification: bool, status: bool):
        value = "Enabled" if status else "Disabled"
        if verification:
            Report.logPass(f"{attribute} is {value}", True)
        else:
            Report.logFail(f"{attribute} is not {value}")

    @staticmethod
    def report_displayed_or_not(attribute: str, verification: bool, displayed: bool = True,
                                screenshot: bool = True, warning: bool = False):
        value = " " if displayed else " not "
        fail = " not " if displayed else " "
        if verification:
            Report.logPass(f"{attribute}{value}displayed", screenshot)
        else:
            if warning:
                Report.logWarning(f"{attribute}{fail}displayed")
            else:
                Report.logFail(f"{attribute}{fail}displayed")
