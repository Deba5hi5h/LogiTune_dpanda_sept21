import logging
from apis.raiden_api import raiden_helper
from datetime import date, datetime
from tzlocal import get_localzone
import pytz

from common import (
    jasmine_config,
)

from extentreport.report import Report
from base import global_variables
import requests

log = logging.getLogger(__name__)


class JasmineMethods:
    org_id = None
    token = None

    def get_jasmine_room_agenda(
        self,
        role: str,
        jasmine_cert_path: str,
        jasmine_privatekey_path: str,
        room_id: str,
    ):
        """Method to get room agenda.

        Test:
             1. Query the API: To get room agenda
             GET ~/org/{org-id}/room/{room_id}/agenda

        """
        try:
            self.token = raiden_helper.signin_method(global_variables.config, role)
            self.org_id = raiden_helper.get_org_id(
                role, global_variables.config, self.token
            )

            # URL to get jasmine room agenda
            url = f"{global_variables.config.MTLS_API_BASE_URL}{jasmine_config.JASMINE_BOOKINGAPI_ORG_ENDPNT}{self.org_id}/room/{room_id}/agenda"

            response = requests.get(
                url, cert=(jasmine_cert_path, jasmine_privatekey_path)
            )
            Report.logInfo(f" Get agenda api status code:  {response.status_code}")
            jasmine_agenda_json_response = response.json()
            Report.logInfo(
                f" Get agenda api json response:  {jasmine_agenda_json_response}"
            )
            return jasmine_agenda_json_response

        except Exception as e:
            Report.logException(f"{e}")

    def validate_agenda_contains_room_booking_for_current_day(
        self,
        role: str,
        jasmine_cert_path: str,
        jasmine_privatekey_path: str,
        room_id: str,
    ):
        """Method to validate that the room booking is shown for current day.

        Test:
             1. Query the API: To get room agenda
             GET ~/org/{org-id}/room/{room_id}/agenda

        """
        try:
            jasmine_agenda_json_response = self.get_jasmine_room_agenda(
                role, jasmine_cert_path, jasmine_privatekey_path, room_id
            )

            jasmine_agenda_details = jasmine_agenda_json_response["bookings"]
            number_of_bookings = len(jasmine_agenda_details)

            if number_of_bookings > 0:
                for i in range(len(jasmine_agenda_details)):
                    booking_start_time = jasmine_agenda_details[i]["startTime"]
                    booking_start_time_str = (
                        booking_start_time[:10] + " " + booking_start_time[11:19]
                    )
                    booking_start_time_utc = datetime.strptime(
                        booking_start_time_str, "%Y-%m-%d %H:%M:%S"
                    )
                    local_timezone = get_localzone()
                    utc_zone = pytz.utc
                    booking_local_time = str(
                        booking_start_time_utc.replace(tzinfo=utc_zone).astimezone(
                            local_timezone
                        )
                    )
                    booking_date_local = booking_local_time[:10]
                    today = str(date.today())

                    # Validate if agenda created for current day
                    if today == booking_date_local:
                        Report.logPass(
                            f"Meeting for the current date is {jasmine_agenda_details}"
                        )
                        break
                    else:
                        Report.logFail(
                            f"There is no meeting scheduled for the current date"
                        )

        except Exception as e:
            Report.logException(f"{e}")

    def validate_agenda_contains_ad_hoc_room_booking(
        self,
        role: str,
        jasmine_cert_path: str,
        jasmine_privatekey_path: str,
        room_id: str,
        duration: float,
    ):
        """Method to get details associated with jasmine ad-hoc room booking.

        Test:
             1. Query the API: To get room agenda
             GET ~/org/{org-id}/room/{room_id}/agenda

        """
        try:
            jasmine_agenda_json_response = self.get_jasmine_room_agenda(
                role, jasmine_cert_path, jasmine_privatekey_path, room_id
            )

            jasmine_agenda_details = jasmine_agenda_json_response["bookings"]
            number_of_bookings = len(jasmine_agenda_details)

            if number_of_bookings > 0:
                for i in range(len(jasmine_agenda_details)):
                    booking_title = jasmine_agenda_details[i]["title"]
                    if booking_title == "Busy":
                        # Start time
                        booking_start_time = jasmine_agenda_details[i]["startTime"]
                        booking_start_time_str = (
                            booking_start_time[:10] + " " + booking_start_time[11:19]
                        )
                        booking_start_time_utc = datetime.strptime(
                            booking_start_time_str, "%Y-%m-%d %H:%M:%S"
                        )
                        local_timezone = get_localzone()
                        utc_zone = pytz.utc
                        booking_start_time_local_tz = booking_start_time_utc.replace(
                            tzinfo=utc_zone
                        ).astimezone(local_timezone)
                        booking_local_time = str(booking_start_time_local_tz)
                        booking_date_local = booking_local_time[:10]

                        # End time
                        booking_end_time = jasmine_agenda_details[i]["endTime"]
                        booking_end_time_str = (
                            booking_end_time[:10] + " " + booking_end_time[11:19]
                        )
                        booking_end_time_utc = datetime.strptime(
                            booking_end_time_str, "%Y-%m-%d %H:%M:%S"
                        )
                        booking_end_time_local_tz = booking_end_time_utc.replace(
                            tzinfo=utc_zone
                        ).astimezone(local_timezone)
                        difference = (
                            booking_end_time_local_tz - booking_start_time_local_tz
                        )
                        time_difference_in_seconds = difference.total_seconds()

                        today = str(date.today())
                        # Validate if ad-hoc booking is created for current day
                        if (
                            today == booking_date_local
                            and time_difference_in_seconds == duration
                        ):
                            Report.logPass(
                                f"Ad-hoc booking details: {jasmine_agenda_details[i]}"
                            )
                            return (
                                booking_start_time_local_tz,
                                booking_end_time_local_tz,
                            )
                else:
                    Report.logFail(
                        f"There is no ad-hoc booking in agenda for the current date and specified duration."
                    )

        except Exception as e:
            Report.logException(f"{e}")

    def validate_adjusted_end_time_after_cancellation_of_ad_hoc_booking(
        self,
        role: str,
        jasmine_cert_path: str,
        jasmine_privatekey_path: str,
        room_id: str,
        duration: float,
    ):
        """Method to get adjusted end time after cancellation of ad-hoc booking.

        Test:
             1. Query the API: To get room agenda
             GET ~/org/{org-id}/room/{room_id}/agenda

        """
        try:
            jasmine_agenda_json_response = self.get_jasmine_room_agenda(
                role, jasmine_cert_path, jasmine_privatekey_path, room_id
            )

            jasmine_agenda_details = jasmine_agenda_json_response["bookings"]
            number_of_bookings = len(jasmine_agenda_details)

            if number_of_bookings > 0:
                for i in range(len(jasmine_agenda_details)):
                    booking_title = jasmine_agenda_details[i]["title"]
                    if booking_title == "Busy":
                        # Start time
                        booking_start_time = jasmine_agenda_details[i]["startTime"]
                        booking_start_time_str = (
                            booking_start_time[:10] + " " + booking_start_time[11:19]
                        )
                        booking_start_time_utc = datetime.strptime(
                            booking_start_time_str, "%Y-%m-%d %H:%M:%S"
                        )
                        local_timezone = get_localzone()
                        utc_zone = pytz.utc
                        booking_start_time_local_tz = booking_start_time_utc.replace(
                            tzinfo=utc_zone
                        ).astimezone(local_timezone)
                        booking_local_time = str(booking_start_time_local_tz)
                        booking_date_local = booking_local_time[:10]

                        # End time
                        booking_end_time = jasmine_agenda_details[i]["endTime"]
                        booking_end_time_str = (
                            booking_end_time[:10] + " " + booking_end_time[11:19]
                        )
                        booking_end_time_utc = datetime.strptime(
                            booking_end_time_str, "%Y-%m-%d %H:%M:%S"
                        )
                        booking_end_time_local_tz = booking_end_time_utc.replace(
                            tzinfo=utc_zone
                        ).astimezone(local_timezone)
                        difference = (
                            booking_end_time_local_tz - booking_start_time_local_tz
                        )
                        time_difference_in_seconds = difference.total_seconds()

                        today = str(date.today())
                        # Validate if ad-hoc booking;s end time is adjusted after cancellation of ad hoc booking.
                        if (
                            today == booking_date_local
                            and (duration - time_difference_in_seconds) <= 60
                        ):
                            Report.logPass(
                                f"Ad-hoc booking details: {jasmine_agenda_details[i]}"
                            )
                            return (
                                booking_start_time_local_tz,
                                booking_end_time_local_tz,
                            )
                else:
                    Report.logFail(
                        f"There is no ad-hoc booking in agenda for the current date and specified duration."
                    )

        except Exception as e:
            Report.logException(f"{e}")
