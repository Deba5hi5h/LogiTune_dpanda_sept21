from apps.collabos.nintendo.nintendo_methods import NintendoMethods
from apis.raiden_api.raiden_api_room_booking_methods import SyncPortalRoomBookingMethods
from apis.jasmine_api.jasmine_api_methods import JasmineMethods
from extentreport.report import Report
from datetime import datetime
from tzlocal import get_localzone
import pytz
import time


class JasmineTCMethods:
    def __init__(self, nintendo_methods: NintendoMethods):
        self.nintendo_methods: NintendoMethods = nintendo_methods
        self.appium_service = self.nintendo_methods.appium_service
        self.jasmine_methods = JasmineMethods()
        self.sync_portal_methods = SyncPortalRoomBookingMethods()
        self.role = "OrgAdmin"
        self.room_name = "Jasmine UI Auto Room"
        self.adhoc_booking_start_time = datetime.now()
        self.adhoc_booking_end_time = datetime.now()
        self.adhoc_booking_extended_time = datetime.now()
        self.adhoc_booking_adjusted_end_time = datetime.now()

    def tc_ad_hoc_booking_1_hour(self):
        """Ad hoc room booking for 1 hour.
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room : Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happens daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.

        Test:
            1. Let room booking settings allow ad-hoc bookings
            2. Check the desk availability.If desk is available, book the desk for 1 hour.
            3. Validate that the room goes to occupied state via Jasmine UI.
            4. Verify that the ad-hoc booking is shown in the jasmine booking API response.

        """
        try:
            # Step 1: Let room booking settings allow ad-hoc bookings
            Report.logInfo(logText="Let room booking settings allow ad-hoc bookings")
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 2: Check the desk availability. If desk is available, book the desk for 1 hour.
            Report.logInfo(
                logText="Check the desk availability. If desk is available, book the desk for 1 hour."
            )
            availability_status = self.nintendo_methods.home.get_availability_status()
            if availability_status == "busy":
                Report.logFail(
                    logText="Room is busy", screenshot=True, is_collabos=True
                )
            Report.logInfo(
                logText="Room is available", screenshot=True, is_collabos=True
            )
            self.nintendo_methods.home.click_book_now()
            self.nintendo_methods.home.click_1_hour()

            # Step 3a: Validate that the room goes to occupied state via Jasmine UI.
            Report.logInfo(
                logText="Validate that the room goes to occupied state via Jasmine UI."
            )
            if self.nintendo_methods.home.verify_release_room():
                Report.logPass(
                    logText="Room booked for 1 hour", screenshot=True, is_collabos=True
                )
            else:
                Report.logFail(
                    logText="Room is available", screenshot=True, is_collabos=True
                )

            # Step 4: Verify that the ad-hoc booking of 1 hour is shown in the jasmine booking API response.
            # Provision a Tap Scheduler device to the same room.
            Report.logInfo(logText="Provision a Tap Scheduler device to the same room.")
            (
                room_id,
                device_id,
                cert_path,
                pkey_path,
            ) = self.sync_portal_methods.provision_nintendo_to_an_existing_room(
                self.role, self.room_name
            )
            Report.logInfo(
                logText="Verify that the ad-hoc booking of 1 hour is shown in the jasmine booking API response."
            )
            (
                self.adhoc_booking_start_time,
                self.adhoc_booking_end_time,
            ) = self.jasmine_methods.validate_agenda_contains_ad_hoc_room_booking(
                self.role, cert_path, pkey_path, room_id, 3600
            )
            Report.logInfo(
                f"Start time of ad-hoc booking is {self.adhoc_booking_start_time}"
            )
            Report.logInfo(
                f"End time of ad-hoc booking is {self.adhoc_booking_end_time}"
            )
            # Deprovision the Tap Scheduler device.
            Report.logInfo(logText="Deprovision the Tap Scheduler device")
            self.sync_portal_methods.deprovision_device(self.role, room_id, device_id)

        except Exception as e:
            Report.logException(f"{e}")

    def tc_extend_room_booking_15_minutes(self):
        """Extend the room booking by +15 minutes
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room: Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happens daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.
            4. Room is booked and it is in occupied state.

        Test:
            1. Let room booking settings allow ad-hoc bookings
            2. Check the desk availability. If desk is occupied, extend the booking by +15 minutes.
            3. Validate that the room booking is extended in Jasmine UI.
            4. Verify that the ad-hoc booking is extended and shown in the jasmine booking API response.

        """
        try:
            # Step 1: Let room booking settings allow ad-hoc bookings
            Report.logInfo(logText="Let room booking settings allow ad-hoc bookings")
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 2: Check the desk availability. If desk is occupied, extend the booking by +15 minutes.
            Report.logInfo(
                logText="Check the desk availability. If desk is occupied, extend the booking by +15 minutes."
            )
            availability_status = self.nintendo_methods.home.get_availability_status()
            if availability_status != "busy":
                Report.logFail(
                    logText="Room is available", screenshot=True, is_collabos=True
                )
            Report.logInfo(logText="Room is busy", screenshot=True, is_collabos=True)
            self.nintendo_methods.home.click_extend_booking()
            self.nintendo_methods.home.click_extend_booking_15_minutes()

            # Step 3a: Validate that the room booking is extended in Jasmine UI
            Report.logInfo(
                logText="Validate that the room booking is extended in Jasmine UI"
            )
            if self.nintendo_methods.home.verify_release_room():
                Report.logPass(
                    logText="Room Booking extended by 15 minutes",
                    screenshot=True,
                    is_collabos=True,
                )
            else:
                Report.logFail(
                    logText="Room Booking is not extended",
                    screenshot=True,
                    is_collabos=True,
                )

            # Step 4: Verify that the ad-hoc booking of 1 hour 15 min is shown in the jasmine booking API response.
            # Provision a Tap Scheduler device to the same room.
            Report.logInfo(logText="Provision a Tap Scheduler device to the same room.")
            (
                room_id,
                device_id,
                cert_path,
                pkey_path,
            ) = self.sync_portal_methods.provision_nintendo_to_an_existing_room(
                self.role, self.room_name
            )
            Report.logInfo(
                logText="Verify that the ad-hoc booking of 1 hour 15 min is shown in the jasmine booking API response."
            )
            (
                self.adhoc_booking_start_time,
                self.adhoc_booking_extended_time,
            ) = self.jasmine_methods.validate_agenda_contains_ad_hoc_room_booking(
                self.role, cert_path, pkey_path, room_id, 4500
            )
            Report.logInfo(
                f"Start time of ad-hoc booking is {self.adhoc_booking_start_time}"
            )
            Report.logInfo(
                f"End time of ad-hoc booking after extension by 15 min is {self.adhoc_booking_extended_time}"
            )

            Report.logInfo(logText="Deprovision Tap Scheduler device")
            self.sync_portal_methods.deprovision_device(self.role, room_id, device_id)

        except Exception as e:
            Report.logException(f"{e}")

    def tc_release_room(self):
        """Release room
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room: Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happens daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.
            4. Room is booked and it is in occupied state.


        Test:
            1. Let room booking settings allow ad-hoc bookings
            2. Check the desk availability. If desk is occupied, check for Release room button. Click on
            Release room.
            3. Check room changes to Available state.

        """
        try:
            # Step 1: Let room booking settings allow ad-hoc bookings
            Report.logInfo(logText="Let room booking settings allow ad-hoc bookings")
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 2: Check the desk availability. If desk is occupied, check for Release room button. Click on
            # Release room.
            Report.logInfo(
                logText="Check the desk availability. If desk is occupied, check for Release room button. Click on Release room."
            )
            availability_status = self.nintendo_methods.home.get_availability_status()
            if availability_status != "busy":
                Report.logFail(
                    logText="Room is available", screenshot=True, is_collabos=True
                )
            Report.logInfo(logText="Room is busy", screenshot=True, is_collabos=True)
            self.nintendo_methods.home.click_release_room()
            self.nintendo_methods.home.click_release_room_confirm()
            current_time = datetime.now()
            local_timezone = get_localzone()
            utc_zone = pytz.utc
            current_time_local = current_time.replace(tzinfo=utc_zone).astimezone(
                local_timezone
            )

            # Step 3a: Check room changes to Available state.
            Report.logInfo(logText="Check room changes to Available state.")
            availability_status = self.nintendo_methods.home.get_availability_status()
            assert availability_status != "busy", "Room is busy"
            if availability_status != "busy":
                Report.logPass(
                    logText="Room is available", screenshot=True, is_collabos=True
                )
            else:
                Report.logFail(
                    logText="Room is busy", screenshot=True, is_collabos=True
                )

            # Step 3b: Verify that the ad-hoc booking's end time gets adjusted in the jasmine booking API response.
            Report.logInfo(logText="Provision a Tap Scheduler device to the same room.")
            (
                room_id,
                device_id,
                cert_path,
                pkey_path,
            ) = self.sync_portal_methods.provision_nintendo_to_an_existing_room(
                self.role, self.room_name
            )
            Report.logInfo(
                logText="Verify that the ad-hoc booking's end time gets adjusted in the jasmine booking API response."
            )
            duration = (
                current_time_local - self.adhoc_booking_start_time
            ).total_seconds()
            (
                self.adhoc_booking_start_time,
                self.adhoc_booking_adjusted_end_time,
            ) = self.jasmine_methods.validate_adjusted_end_time_after_cancellation_of_ad_hoc_booking(
                self.role, cert_path, pkey_path, room_id, duration
            )
            Report.logInfo(
                f"Start time of ad-hoc booking is {self.adhoc_booking_start_time}"
            )
            Report.logInfo(
                f"Adjusted End time of ad-hoc booking after cancellation is {self.adhoc_booking_adjusted_end_time}"
            )
            Report.logInfo(logText="Deprovision Tap Scheduler device")
            self.sync_portal_methods.deprovision_device(self.role, room_id, device_id)

        except Exception as e:
            Report.logException(f"{e}")

    def tc_get_first_agenda_item_details(self):
        """Get first agenda item details associated with meeting room.
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room: Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happens daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.

        Test:
            1. Let room booking settings allow ad-hoc bookings
            2. Verify that the meeting details: meeting name, organizer, attendees count & time is shown in the agenda UI.
            3. Verify that the meeting details are shown in the agenda API response.

        """
        try:
            # Step 1: Let room booking settings allow ad-hoc bookings
            Report.logInfo(logText="Let room booking settings allow ad-hoc bookings")
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 2:  Verify that the meeting details: meeting name, organizer, attendees count & time is shown in the
            # agenda.
            Report.logInfo(
                logText="Verify that the meeting details: meeting name, organizer, attendees count & time is shown in the agenda."
            )
            expected_agenda_item_details = {
                "meeting-title": "Automation testing",
                "meeting-organizer": "by Logi QA User 5",
                "meeting-time": "11:00 – 11:30 PM",
                "meeting-attendees-count": "1",
            }
            first_agenda_item_details = {
                "meeting-title": self.nintendo_methods.home.get_first_agenda_item_meeting_title(),
                "meeting-organizer": self.nintendo_methods.home.get_first_agenda_item_meeting_organizer(),
                "meeting-time": self.nintendo_methods.home.get_first_agenda_item_meeting_time(),
                "meeting-attendees-count": self.nintendo_methods.home.get_first_agenda_item_meeting_attendees_count(),
            }
            for key, value in expected_agenda_item_details.items():
                if first_agenda_item_details[key] == str(value):
                    Report.logPass(
                        logText=f"{key} of first agenda item is {value}",
                        screenshot=True,
                        is_collabos=True,
                    )
                else:
                    Report.logFail(
                        logText=f"{key} of first agenda item is incorrect",
                        screenshot=True,
                        is_collabos=True,
                    )

            # Step 3: Verify that the meeting details are shown in the agenda API response.
            Report.logInfo(logText="Provision a Tap Scheduler device to the same room.")
            (
                room_id,
                device_id,
                cert_path,
                pkey_path,
            ) = self.sync_portal_methods.provision_nintendo_to_an_existing_room(
                self.role, self.room_name
            )
            Report.logInfo(
                logText="Verify that the meeting details are shown in the agenda API response."
            )
            self.jasmine_methods.validate_agenda_contains_room_booking_for_current_day(
                self.role, cert_path, pkey_path, room_id
            )
            Report.logInfo(logText="Deprovision Tap Scheduler device")
            self.sync_portal_methods.deprovision_device(self.role, room_id, device_id)

        except Exception as e:
            Report.logException(f"{e}")

    def tc_configure_settings_pin(self):
        """Configure Settings PIN via Sync Portal and verify on Tap Scheduler to access Logitech Settings using the settings PIN.
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room: Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happen daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.

        Test:
           1. Enable Require a PIN code to access system settings option in Sync Portal and configure the 4 digit pin as 1234.
           2. Navigate to Nintendo home screen. Click on Settings icon.
           3. Look for 'Enter device PIN' heading. Do not perform any action for minimum 30 seconds and the settings
              pin page auto-closes. Click on Settings icon to view Enter device PIN page.
           4. Click on Close button.
           5. Verify that user is re-directed to home screen by looking for Settings icon.
           6. Click on Settings icon.
           7. Enter the code: 1234.
           8. Verify that Logitech settings screen is opened.
           9. Close the Logitech settings screen.
           10. Disable Settings PIN and set the room booking settings back to the default values via Sync Portal.
           11. Navigate to Nintendo home screen. Click on Settings icon.
           12. Logitech Settings screen is shown.
           13. Close the Logitech Settings screen.
           14. Main Screen is shown.
        """
        try:
            # Step 1: Enable Require a PIN code to access system settings option in Sync Portal and configure the
            # 4 digit pin as 1234.
            code = "1234"
            Report.logInfo(logText=f"Set the settings pin for group to {code}")
            self.sync_portal_methods.set_settings_pin_for_group(
                role=self.role, code=code
            )

            # Step 2: Go to Nintendo home screen. Click on Settings icon.
            self.nintendo_methods.home.click_settings_icon()
            Report.logInfo(
                logText="Clicked on Settings icon", screenshot=True, is_collabos=True
            )

            # Step 3a: Look for 'Enter device PIN' heading.
            self.nintendo_methods.pin.view_enter_device_pin_heading()
            Report.logInfo(
                logText="Enter device PIN page is shown",
                screenshot=True,
                is_collabos=True,
            )

            # Step 3b: Do not perform any action for minimum 30 seconds.
            Report.logInfo(
                logText="Do not perform any action for minimum 30 seconds."
            )
            time.sleep(35)

            # Step 3c: Settings PIN page auto-closes and returns to the main screen.
            self.nintendo_methods.home.view_main_screen()
            Report.logInfo(
                logText="Settings PIN auto-closes after 30 seconds of no-activity and returns to the main screen.",
                screenshot=True, is_collabos=True
            )

            # Step 3d: Go to Nintendo home screen. Click on Settings icon.
            self.nintendo_methods.home.click_settings_icon()
            Report.logInfo(
                logText="Clicked on Settings icon", screenshot=True, is_collabos=True
            )

            # Step 3e: Look for 'Enter device PIN' heading.
            self.nintendo_methods.pin.view_enter_device_pin_heading()
            Report.logInfo(
                logText="Enter device PIN page is shown",
                screenshot=True,
                is_collabos=True,
            )

            # Step 4: Click on Close button.
            self.nintendo_methods.pin.click_close_button()
            Report.logInfo(
                logText="Clicked on Close button", screenshot=True, is_collabos=True
            )

            # Step 5: Verify that user is re-directed to home screen by looking for Settings icon.
            self.nintendo_methods.home.view_settings_icon()
            Report.logInfo(
                logText="Viewed Settings icon", screenshot=True, is_collabos=True
            )

            # Step 6: Click on Settings icon.
            self.nintendo_methods.home.click_settings_icon()
            Report.logInfo(
                logText="Clicked on Settings icon", screenshot=True, is_collabos=True
            )

            # Step 7: Enter the code: 1234
            for char in code:
                self.nintendo_methods.pin.enter_digit_associated_with_pin(int(char))
                Report.logInfo(
                    logText=f"Clicked on digit {char}",
                    screenshot=True,
                    is_collabos=True,
                )

            # Step 8: Verify that Logitech Settings screen is opened.
            self.nintendo_methods.logi_settings.view_logitech_settings_screen()
            Report.logInfo(
                logText="Check that Logitech Settings screen is opened",
                screenshot=True,
                is_collabos=True,
            )

            # Step 9: Click on the logitech settings Close icon.
            self.nintendo_methods.logi_settings.click_on_logitech_settings_close_button()
            Report.logInfo(
                logText="Clicked on the logitech settings Close icon.",
                screenshot=True,
                is_collabos=True,
            )

            # Step 10: Set the room booking back to the default values.
            Report.logInfo(
                logText="Set the room booking back to the default values.",
                screenshot=True,
                is_collabos=True,
            )
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 11: Click on Settings icon.
            self.nintendo_methods.home.click_settings_icon()
            Report.logInfo(
                logText="Clicked on Settings icon", screenshot=True, is_collabos=True
            )

            # Step 12: Verify that Logitech Settings screen is opened.
            self.nintendo_methods.logi_settings.view_logitech_settings_screen()
            Report.logInfo(
                logText="Check that Logitech Settings screen is opened",
                screenshot=True,
                is_collabos=True
            )

            # Step 13: Click on the logitech settings Close icon.
            self.nintendo_methods.logi_settings.click_on_logitech_settings_close_button()
            Report.logInfo(
                logText="Clicked on the logitech settings Close icon.",
                screenshot=True,
                is_collabos=True
            )

            # Step 14:  Main screen is shown.
            self.nintendo_methods.home.view_main_screen()
            Report.logInfo(
                logText="Main screen is shown", screenshot=True,
                is_collabos=True
            )

        except Exception as e:
            Report.logException(f"{e}")

    def tc_view_floor_map_containing_the_meeting_room(self):
        """View room, desks and point of interests on floor map page.
        Setup:
            1. Provision Tap Scheduler running Logitech Room Booking application to Sync Portal
                meeting room: Jasmine UI Auto Room.
            2. Let the meeting room is connected to the calendar room resource - M365 Logi QA Room 3.
            3. Let there is 1 scheduled recurring meeting at 11:00 PM - 11:30 PM local time that happens daily with
               meeting name: Automation testing and meeting organizer: Logi QA User 5.
            4. Let the room located in Floor 1 is plotted on the map in Sync Portal.

        Test:
           1. Set the room booking settings to default in Sync Portal
           2. Click on Floor map button on main screen of Tap Scheduler.
           3. Do not perform any action for 30 seconds.
           4. Floor map page auto-closes and returns to the main screen.
           5. Click on Floor map.
           6. Check for the presence of map containing room, desks and point of interests.
           7. Click on Close button.
           8. Main screen is shown.
        """
        try:
            # Step 1: Set the room booking settings to default in Sync Portal
            Report.logInfo(logText="Set the room booking settings to default in Sync Portal")
            self.sync_portal_methods.set_group_room_booking_settings_to_default(
                role=self.role
            )

            # Step 2: Click on Floor map button on main screen of Tap Scheduler.
            self.nintendo_methods.home.click_floor_map()
            Report.logInfo(
                logText="Clicked Floor map button", screenshot=True, is_collabos=True
            )

            # Step 3: Do not perform any action for minimum 30 seconds.
            Report.logInfo(
                logText="Do not perform any action for minimum 30 seconds."
            )
            time.sleep(35)

            # Step 4: Floor map page auto-closes and returns to the main screen.
            self.nintendo_methods.home.view_main_screen()
            Report.logInfo(
                logText="Floor map page auto-closes after 30 seconds of no-activity and returns to the main screen.", screenshot=True, is_collabos=True
            )

            # Step 5: Click on Floor map.
            self.nintendo_methods.home.click_floor_map()
            Report.logInfo(
                logText="Clicked Floor map button", screenshot=True, is_collabos=True
            )

            # Step 6: Check for the presence of map containing room, desks and point of interests.
            self.nintendo_methods.floor_map.view_map()
            Report.logInfo(
                logText="Check for the presence of map containing room, desks and point of interests.", screenshot=True, is_collabos=True
            )

            # Step 7: Click on Close button associated with floor map.
            self.nintendo_methods.floor_map.close_floor_map()
            Report.logInfo(
                logText="Click on Close button associated with floor map.", screenshot=True,
                is_collabos=True
            )

            # Step 8:  Main screen is shown.
            self.nintendo_methods.home.view_main_screen()
            Report.logInfo(
                logText="Main screen is shown", screenshot=True,
                is_collabos=True
            )

        except Exception as e:
            Report.logException(f"{e}")
