import datetime
import time

from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile import TuneMobile
from locators.tune_mobile.tune_mobile_dashboard_locators import TuneMobileDashboardLocators


class TuneMobileDashboard(TuneMobile):

    def click_home(self):
        """
        Method to click Home

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.HOME).click()
        return self

    def click_profile(self):
        """
        Method to click Profile icon

        :param :
        :return TuneMobileProfile:
        """
        self.find_element(TuneMobileDashboardLocators.PROFILE).click()
        from apps.tune_mobile.tune_mobile_profile import TuneMobileProfile
        return TuneMobileProfile()

    def click_notification(self):
        """
        Method to click Notification icon

        :param :
        :return TuneMobileProfile:
        """
        if self.verify_element(TuneMobileDashboardLocators.NOTIFICATION_UNREAD, timeout=10):
            self.find_element(TuneMobileDashboardLocators.NOTIFICATION_UNREAD).click()
        else:
            self.find_element(TuneMobileDashboardLocators.NOTIFICATION).click()
        from apps.tune_mobile.tune_mobile_notification import TuneMobileNotification
        return TuneMobileNotification()

    def click_book(self):
        """
        Method to click Book control

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileDashboardLocators.BOOK).click()
        from apps.tune_mobile.tune_mobile_book import TuneMobileBook
        return TuneMobileBook()

    def click_people(self):
        """
        Method to click Book control

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobileDashboardLocators.PEOPLE).click()
        from apps.tune_mobile.tune_mobile_people import TuneMobilePeople
        return TuneMobilePeople()

    def click_maps(self):
        """
        Method to click Map control

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobileDashboardLocators.MAPS).click()
        from apps.tune_mobile.tune_mobile_people import TuneMobilePeople
        return TuneMobilePeople()

    def click_teammates_in_office(self):
        """
        Method to click Teammates in office

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobileDashboardLocators.TEAMMATES_IN_OFFICE).click()
        from apps.tune_mobile.tune_mobile_people import TuneMobilePeople
        return TuneMobilePeople()

    def click_details(self, desk_name):
        """
        Method to click Details button on booked desk

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_DETAILS, param=desk_name).click()
        return self

    def click_desk_name(self, desk_name: str):
        """
        Method to click desk name from booking card on Dashboard

        :param desk_name:
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_DESK_NAME, param=desk_name).click()
        return self

    def click_edit_booking(self):
        """
        Method to click Edit Booking button on booking details screen

        :param :
        :return TuneMobileBook:
        """
        self.find_element(TuneMobileDashboardLocators.EDIT_BOOKING).click()
        from apps.tune_mobile.tune_mobile_book import TuneMobileBook
        return TuneMobileBook()

    def click_notify_teammates(self):
        """
        Method to click Notify Teammates on booking pop up screen

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.NOTIFY_TEAMMATES).click()
        return self

    def click_cancel_session(self):
        """
        Method to click Cancel session button on Modify booking confirmation

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.CANCEL_SESSION).click()
        return self

    def click_end_session(self):
        """
        Method to click End session button on Modify booking confirmation

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.END_SESSION).click()
        return self

    def click_yes_cancel(self):
        """
        Method to click Yes, Cancel button on booking cancel dialog

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.YES_CANCEL).click()
        return self

    def click_yes_end(self):
        """
        Method to click Yes, End button on booking cancel dialog

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.YES_END).click()
        return self

    def click_no_keep(self):
        """
        Method to click No, Keep button on booking cancel dialog

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.NO_KEEP).click()
        return self

    def click_bottom_sheet_close(self):
        """
        Method to click close button on bottom sheet

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.CLOSE_BOTTOM_SHEET).click()
        return self

    def click_ok(self):
        """
        Method to click OK button on bottom sheet

        :param :
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.OK).click()
        return self

    def verify_people_navigation_highlighted(self) -> bool:
        """
        Method to verify People navigation button highlighted

        :param :
        :return bool:
        """
        return self.find_element(TuneMobileDashboardLocators.PEOPLE).is_selected()

    def verify_booking_card_desk_name(self, desk_name: str, timeout: int = tune_mobile_config.implicit_wait):
        """
        Method to verify desk name in booking card on Dashboard

        :param desk_name:
        :return TuneMobileDashboard:
        """
        return self.verify_element(TuneMobileDashboardLocators.BOOKING_CARD_DESK_NAME, param=desk_name, timeout=timeout)

    def verify_booking_card_schedule(self, desk_name: str, start: str, end: str):
        """
        Method to verify schedule in booking card on Dashboard

        :param desk_name:
        :param start:
        :param end:
        :return bool:
        """
        schedule = f"{start} - {end}"
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_SCHEDULE, param=desk_name, visibility=False)
        value = 'value' if self.is_ios_device() else 'text'
        return True if schedule == str(element.get_attribute(value)).strip() else False

    def verify_booking_card_location(self, desk_name: str, building: str, floor: str, area: str):
        """
        Method to verify location in booking card on Dashboard

        :param desk_name:
        :param building:
        :param floor:
        :param area:
        :return bool:
        """
        location = f"{building}・{floor}・{area}"
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_LOCATION, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return True if location.lower() == element.get_attribute(value).lower() else False

    def verify_mofify_booking_desk_image(self):
        """
        Method to verify desk image in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.MODIFY_BOOKING_DESK_IMAGE)

    def verify_modify_booking_desk_name(self, desk_name: str):
        """
        Method to verify desk name in modify booking screen bottom sheet

        :param desk_name:
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.MODIFY_BOOKING_DESK_NAME, param=desk_name)

    def verify_modify_booking_location(self, floor: str, area: str):
        """
        Method to verify location in modify booking screen bottom sheet

        :param floor:
        :param area:
        :return bool:
        """
        location = f"{floor}・{area}"
        if self.is_android_device():
            location = location.upper().replace('・', ' ・ ')
        return self.verify_element(TuneMobileDashboardLocators.MODIFY_BOOKING_LOCATION, param=location)

    def verify_modify_booking_schedule(self, start: str, end: str):
        """
        Method to verify schedule in modify booking screen bottom sheet

        :param start:
        :param end:
        :return bool:
        """
        schedule = f"{start} - {end}"
        return self.verify_element(TuneMobileDashboardLocators.MODIFY_BOOKING_SCHEDULE, param=schedule)

    def verify_edit_booking(self):
        """
        Method to verify edit booking button in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.EDIT_BOOKING)

    def verify_cancel_session(self):
        """
        Method to verify cancel session button in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.CANCEL_SESSION)

    def verify_end_session(self):
        """
        Method to verify end session button in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.END_SESSION)

    def verify_show_on_maps(self):
        """
        Method to verify show on maps in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.SHOW_ON_MAPS)

    def click_teammates_near_by(self):
        """
        Method to click teammates near by in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        self.find_element(TuneMobileDashboardLocators.TEAMMATES_NEAR_BY).click()
        return self

    def verify_teammates_near_by(self):
        """
        Method to verify teammates near by in modify booking screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.TEAMMATES_NEAR_BY)

    def verify_cancel_session_message(self):
        """
        Method to verify message dispalyed in cancel session screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.CANCEL_SESSION_MESSAGE)

    def verify_end_session_message(self):
        """
        Method to verify message dispalyed in end session screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.END_SESSION_MESSAGE)

    def verify_release_desk_message(self):
        """
        Method to verify message dispalyed for releasing desk in cancel/end session screen bottom sheet

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.RELEASE_DESK_MESSAE)

    def verify_booking_cancelled_confirmation(self):
        """
        Method to verify message booking cancelled displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.BOOKING_CANCELLED_CONFIRMATION)

    def verify_booking_cancelled_message(self):
        """
        Method to verify message You're all set! displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.BOOKING_CANCELLED_MESSAGE)

    def get_booking_card_building(self, desk_name: str) -> str:
        """
        Method to get buidling name displayed in booking card on Dashboard

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_LOCATION, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).split('・')[0].strip()

    def get_booking_card_floor(self, desk_name: str) -> str:
        """
        Method to get floor name displayed in booking card on Dashboard

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_LOCATION, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).split('・')[1].strip()

    def get_booking_card_area(self, desk_name: str) -> str:
        """
        Method to get workspace/ara name displayed in booking card on Dashboard

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_LOCATION, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).split('・')[2].strip()

    def get_booking_card_schedule_start(self, desk_name: str) -> str:
        """
        Method to get schedule start displayed in booking card on Dashboard

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_SCHEDULE, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).split('-')[0].strip()

    def get_booking_card_schedule_end(self, desk_name: str) -> str:
        """
        Method to get schedule end displayed in booking card on Dashboard

        :param desk_name:
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BOOKING_CARD_SCHEDULE, param=desk_name)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).split('-')[1].strip()

    def get_dashboard_building(self) -> str:
        """
        Method to get Building name displayed on Dashboard

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileDashboardLocators.BUILDING)
        value = 'value' if self.is_ios_device() else 'text'
        dashboard = element.get_attribute(value)
        building = str(dashboard).split("·")[0].strip()
        return building

    def get_dashboard_occupancy(self) -> int:
        """
        Method to get Building name displayed on Dashboard

        :param :
        :return int:
        """
        element = self.find_element(TuneMobileDashboardLocators.BUILDING)
        value = 'value' if self.is_ios_device() else 'text'
        dashboard = element.get_attribute(value)
        occupancy = str(dashboard).split("·")[1].strip().split("%")[0]
        return int(occupancy)

    def click_date(self, day:int = 0):
        """
        Method to click Date from the Schedule calendar

        :param day:
        :return TuneMobileDashboard:
        """
        current_date = datetime.datetime.now()
        date_to_click = current_date + datetime.timedelta(day)
        date = str(date_to_click.day)
        if not self.verify_element(TuneMobileDashboardLocators.DATE, param=date, timeout=5):
            self.click_expand_calendar()
        self.find_element(TuneMobileDashboardLocators.DATE, param=date).click()
        return self

    def click_expand_calendar(self):
        """
        Method to click expand calendar button

        :param day:
        :return TuneMobileDashboard:
        """
        self.find_element(TuneMobileDashboardLocators.EXPAND_CALENDAR).click()
        return self

    def verify_home(self) -> bool:
        """
        Method to verify Home displayed on Dashboard

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileDashboardLocators.HOME, timeout=10)
