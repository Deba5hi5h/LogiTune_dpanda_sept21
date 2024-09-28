from apps.collabos.base_collabos_methods import CollabOsBaseMethods
from locators.nintendo_room_booking_locators import (
    RoomBookingMainPageLocators,
    RoomBookingDevicePinLocators,
    LogitechSettingsLocators,
    FloorMapLocators
)


class RoomBookingMainPage(CollabOsBaseMethods):
    def get_time(self) -> str:
        """
        Method to return the time from Room Booking idle page.

        :param :
        :return str: desk name
        """
        element = self.find_element_collabos(RoomBookingMainPageLocators.CLOCK)
        value = "text"
        time = element.get_attribute(value)
        return str(time)

    def get_availability_status(self) -> str:
        """
        Method to return the availability status from Room Booking page.

        :param :
        :return str: availability status
        """
        if self.verify_element_collabos(RoomBookingMainPageLocators.AVAILABILITY):
            element = self.find_element_collabos(
                RoomBookingMainPageLocators.AVAILABILITY
            )
            return str(element.get_attribute("text"))
        else:
            return "busy"

    def click_book_now(self):
        """
        Method to click Book Now button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.BOOK_NOW).click()
        return self

    def click_30_minutes(self):
        """
        Method to click 30 minutes button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.MINUTES_30).click()
        return self

    def click_1_hour(self):
        """
        Method to click 1 hour button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.HOUR_1).click()
        return self

    def click_2_hour(self):
        """
        Method to click 2 hours button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.HOUR_2).click()
        return self

    def click_check_mark(self):
        """
        Method to click Check mark button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.CHECK_MARK).click()
        return self

    def click_checkin(self):
        """
        Method to click Check in button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.CHECKIN).click()
        return self

    def verify_checkin_button(self) -> bool:
        """
        Method to check if Check in button displayed.

        :param :
        :return bool:
        """
        return self.verify_element_collabos(RoomBookingMainPageLocators.CHECKIN)

    def click_checkin_cancel(self):
        """
        Method to click Check in Cancel button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.CHECKIN_CANCEL).click()
        return self

    def click_checkin_confirm(self):
        """
        Method to click Check in Confirm button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.CHECKIN_CONFIRM).click()
        return self

    def click_release_room(self):
        """
        Method to click Release Room button from Room Booking page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.RELEASE_ROOM).click()
        return self

    def verify_release_room(self) -> bool:
        """
        Method to check if Release Room button displayed.

        :param :
        :return bool:
        """
        return self.verify_element_collabos(RoomBookingMainPageLocators.RELEASE_ROOM)

    def click_release_room_confirm(self):
        """
        Method to click Confirm button from Room Booking Release page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(
            RoomBookingMainPageLocators.RELEASE_ROOM_CONFIRM
        ).click()
        return self

    def click_release_room_cancel(self):
        """
        Method to click Cancel button from Room Booking Release page.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(
            RoomBookingMainPageLocators.RELEASE_ROOM_CANCEL
        ).click()
        return self

    def click_extend_booking(self):
        """
        Method to click on Extend Booking option from Room Booking page

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.EXTEND_BOOKING).click()
        return self

    def click_extend_booking_15_minutes(self):
        """
        Method to extend room booking by clicking +15 minutes.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(
            RoomBookingMainPageLocators.EXTEND_MINUTES_15
        ).click()
        return self

    def click_extend_booking_30_minutes(self):
        """
        Method to extend room booking by clicking +30 minutes.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(
            RoomBookingMainPageLocators.EXTEND_MINUTES_30
        ).click()
        return self

    def click_extend_booking_1_hour(self):
        """
        Method to extend room booking by clicking +1 hour.

        :param :
        :return RoomBookingMainPage:
        """
        self.find_element_collabos(RoomBookingMainPageLocators.EXTEND_HOUR_1).click()
        return self

    def get_first_agenda_item_meeting_title(self):
        """
        Method to get the meeting title of first agenda item.
        :param :
        :return str:
        """
        return self.find_element_collabos(
            RoomBookingMainPageLocators.FIRST_AGENDA_ITEM_TITLE
        ).text

    def get_first_agenda_item_meeting_organizer(self):
        """
        Method to get the meeting organizer name of first agenda item.
        :param :
        :return str:
        """
        return self.find_element_collabos(
            RoomBookingMainPageLocators.FIRST_AGENDA_ITEM_ORGANIZER
        ).text

    def get_first_agenda_item_meeting_time(self):
        """
        Method to get the meeting time of first agenda item.
        :param :
        :return str:
        """
        return self.find_element_collabos(
            RoomBookingMainPageLocators.FIRST_AGENDA_ITEM_TIME
        ).text

    def get_first_agenda_item_meeting_attendees_count(self):
        """
        Method to get the meeting attendees count of first agenda item.
        :param :
        :return str:
        """
        return self.find_element_collabos(
            RoomBookingMainPageLocators.FIRST_AGENDA_ITEM_ATTENDEES_COUNT
        ).text

    def view_settings_icon(self):
        """
        Method to look for settings icon.
        """
        self.find_element_collabos(RoomBookingMainPageLocators.OPEN_SETTINGS)
        return self

    def click_settings_icon(self):
        """
        Method to click settings icon.
        """
        self.find_element_collabos(RoomBookingMainPageLocators.OPEN_SETTINGS).click()
        return self

    def click_floor_map(self):
        """
        Method to click settings icon.
        """
        self.find_element_collabos(RoomBookingMainPageLocators.FLOOR_MAP).click()
        return self

    def view_main_screen(self):
        """
        Method to check for the presence of room name in main screen.
        """
        self.find_element_collabos(RoomBookingMainPageLocators.ROOM_NAME).click()
        return self


class RoomBookingDevicePinPage(CollabOsBaseMethods):
    def view_enter_device_pin_heading(self):
        """
        Method to look Enter device PIN heading.
        """
        self.find_element_collabos(RoomBookingDevicePinLocators.ENTER_DEVICE_PIN_TEXT)
        return self

    def click_close_button(self):
        """
        Method to click on close button.
        """
        self.find_element_collabos(RoomBookingDevicePinLocators.CLOSE).click()
        return self

    def enter_digit_associated_with_pin(self, digit: int):
        """
        Method to enter digit associated with pin

        :param digit:
        """
        self.find_element_collabos(
            RoomBookingDevicePinLocators.digit_n(digit=digit)
        ).click()
        return self


class LogitechSettingsPage(CollabOsBaseMethods):
    def view_logitech_settings_screen(self):
        """
        Method to look for Logitech Settings Screen.
        """
        self.find_element_collabos(LogitechSettingsLocators.LOGITECH_SETTINGS_TITLE)
        return self

    def click_on_logitech_settings_close_button(self):
        self.find_element_collabos(LogitechSettingsLocators.CLOSE).click()
        return self


class FloorMapPage(CollabOsBaseMethods):
    def view_map(self):
        """
        Method to look for Map
        """
        self.find_element_collabos(FloorMapLocators.FLOOR_MAP)
        return self

    def close_floor_map(self):
        """
        Method to click the close button associated with floor map page.
        """
        self.find_element_collabos(FloorMapLocators.CLOSE_FLOOR_MAP).click()
        return self

