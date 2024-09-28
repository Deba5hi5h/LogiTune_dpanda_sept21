from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from apps.collabos.coily.utilities import prepare_tune_calendar_account_credentials, prepare_work_account_credentials
from apps.tune.tune_ui_methods import TuneUIMethods
from locators.tunes_ui_locators import TunesAppLocators
from typing import Optional
from apps.tune.calendar_api import GoogleCalendarApi, CALENDAR_TOKEN_PATH, MicrosoftCalendarApi, \
    COILY_CALENDAR_PATH
from datetime import datetime, timedelta, time as dt_time
from extentreport.report import Report

import random
import string
import time
import re


class CalendarMethods(TuneUIMethods):
    def __init__(self, account_type, tests_type, credentials=None):
        super().__init__()

        if not credentials:
            if account_type == GOOGLE:
                credentials = prepare_tune_calendar_account_credentials(account_type=GOOGLE) \
                    if tests_type == 'calendar' \
                    else prepare_work_account_credentials(account_type=GOOGLE)
            else:
                credentials = prepare_tune_calendar_account_credentials(
                    account_type=MICROSOFT) if tests_type == 'calendar' \
                    else prepare_work_account_credentials(account_type=MICROSOFT)

        if account_type == GOOGLE:
            token_path = CALENDAR_TOKEN_PATH if tests_type == 'calendar' else COILY_CALENDAR_PATH
            self.calendar_api = GoogleCalendarApi(
                token_short_path=token_path,
                email=credentials['signin_payload']['email'],
                password=credentials['signin_payload']['password'],
                employee_id=credentials['signin_payload']['employee_id']
            )
        else:
            self.calendar_api = MicrosoftCalendarApi(email=credentials['signin_payload']['email'],
                                                     password=credentials['signin_payload']['password'])

    def tc_verify_event_presence(self):
        """
        account: google or microsoft
        """
        event = None
        try:
            meeting_title = f'Test event: {datetime.now()}'
            start_time = datetime.now() + timedelta(minutes=30)
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=30)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()
            if self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=20):
                Report.logPass(f"Event {meeting_title} displayed in Logi Tune", True)
            else:
                Report.logFail(f"Event {meeting_title} not displayed in Logi Tune", screenshot=True)

        except Exception as e:
            Report.logException(str(e))
        finally:
            self.calendar_api.delete_event(event_id=event['id'])

    def delete_remaining_events(self):
        self.calendar_api.delete_remaining_events()

    def tc_verify_multiple_events_presence(self, number: int):
        """
        account: google or microsoft
        """
        try:
            titles_events = list()

            for _ in range(number):
                meeting_title = f'Test event: {datetime.now()}'
                start_time = datetime.now() + timedelta(minutes=random.randint(5, 30))
                duration = random.randint(5, 30)
                event = self.calendar_api.create_event(
                    start_time=start_time, summary=meeting_title, duration_min=duration)
                titles_events.append((meeting_title, event))

            # print(titles_events)
            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            for title, event in titles_events:
                if self.tune_app.verify_meeting_title(meeting_title=title, timeout=20):
                    Report.logPass(f"Event {title} displayed in Logi Tune", True)
                else:
                    Report.logFail(f"Event {title} not displayed in Logi Tune", screenshot=True)

                self.calendar_api.delete_event(event_id=event['id'])

        except Exception as e:
            Report.logException(str(e))

    def _click_day_in_calendar(self, offset: int, collapse: Optional[bool] = True):
        today_index = (datetime.now().weekday() + 1) % 7
        if collapse:
            day_button_list = self.tune_app.look_all_elements(TunesAppLocators.CALENDAR_DAY_LABEL)[7:]
            Report.logInfo(f'Collapsing calendar')
            self.tune_app.look_element(TunesAppLocators.COLLAPSE_CALENDAR).click()
            time.sleep(0.3)
            self.tune_app.look_element(TunesAppLocators.COLLAPSE_CALENDAR_CLOSE, wait_for_visibility=True)
            day_button_list[offset + today_index].click()
        else:
            day_button_list = self.tune_app.look_all_elements(TunesAppLocators.CALENDAR_DAY_LABEL)[:7]
            day_button_list[offset + today_index].click()

    def _click_today_in_calendar(self):

        self._click_day_in_calendar(offset=0, collapse=True)

    def _verify_event_presence_for_particular_day(self,
                                                  target_day: datetime,
                                                  collapse: Optional[bool] = True):
        """
        account: google or microsoft
        """
        event = None
        try:
            meeting_title = f'Test event: {target_day.now().hour}:{target_day.now().minute}:{target_day.now().second}'
            time_delta_days = (target_day.date() - datetime.now().date()).days
            start_time = target_day
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=2)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            self._click_day_in_calendar(offset=time_delta_days, collapse=collapse)
            self.tune_app.click_refresh_calendar_button()

            meeting_element = self.tune_app.verify_meeting_title(meeting_title, timeout=10)

            if meeting_element:
                Report.logPass(f'The meeting {meeting_title} set for day today + {target_day} is displayed')
            else:
                Report.logFail(f'The meeting {meeting_title} set for day today + {target_day} is NOT displayed',
                               screenshot=True)
        except Exception as e:
            Report.logException(str(e))
        finally:
            self.calendar_api.delete_event(event_id=event['id'])
            self._click_today_in_calendar()

    def tc_verify_tomorrow_event_presence(self):
        """
        account: google or microsoft
        """
        target_day = datetime.now() + timedelta(days=1)
        self._verify_event_presence_for_particular_day(target_day=target_day,
                                                       collapse=True)

    def tc_verify_the_day_after_tomorrow_event_presence(self):
        """
        account: google or microsoft
        """
        target_day = datetime.now() + timedelta(days=2)
        self._verify_event_presence_for_particular_day(target_day=target_day)

    def tc_verify_the_next_week_event_presence(self):

        """
        account: google or microsoft
        """
        target_day = datetime.now() + timedelta(days=7)
        self._verify_event_presence_for_particular_day(target_day=target_day)

    def tc_verify_the_next_month_event_presence(self):

        """
        account: google or microsoft
        """
        time_now = datetime.now()
        current_month = time_now.month
        next_month = current_month + 1 if current_month != 12 else 1
        next_year = time_now.year if current_month != 12 else time_now.year + 1
        target_day = datetime(year=next_year, month=next_month, day=1,
                              hour=time_now.hour, minute=time_now.minute)

        self._verify_event_presence_for_particular_day(target_day=target_day)

    @staticmethod
    def generate_random_string(length: Optional[int]) -> str:
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def generate_random_mail(self):
        return self.generate_random_string(random.randint(3, 8)) \
            + "@testlogi" \
            + "." \
            + random.choice(['eu', 'com', 'pl'])

    def tc_verify_multiple_guests_invited_number(self, account_type):

        """
           account: google or microsoft
           """
        event = None
        time_now = datetime.now()
        guests_number = random.randint(2, 5)
        guests_email_list = [self.generate_random_mail() for _ in range(guests_number)]

        try:
            meeting_title = f'Test event: {time_now.hour}:{time_now.minute}:{time_now.second}'

            start_time = time_now + timedelta(minutes=5)
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=2,
                attendees=guests_email_list
            )

            if account_type == GOOGLE:
                hangout_link = event.get('hangoutLink', None)
                meeting_link = event.get('htmlLink', None)
            else:
                hangout_link = event.get('onlineMeeting', None).get('joinUrl')
                meeting_link = event.get('webLink', None)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self._click_today_in_calendar()
            self.tune_app.click_refresh_calendar_button(
            )

            meeting_element = self.tune_app.verify_meeting_title(meeting_title)
            attendees = self.tune_app.look_element(TunesAppLocators.ATTENDEES_NUMBER)
            no_of_invited = int(attendees.text)
            Report.logInfo(f"Number of invited people: {no_of_invited}")

            if meeting_element:
                if no_of_invited == guests_number + 1:
                    Report.logPass(f'The meeting {meeting_title} set for day today + {time_now} '
                                   'is displayed and number of invited people match', screenshot=True)
                else:
                    Report.logFail(f'The meeting {meeting_title} set for day today + {time_now} '
                                   'is displayed and number of invited people don\'t match',
                                   screenshot=True)
            else:
                Report.logFail(f'The meeting {meeting_title} set for day today + {time_now} is NOT displayed',
                               screenshot=True)

            meeting_element.click()

            details = self.tune_app.look_element(TunesAppLocators.CALENDAR_OPEN_DETAILS).get_attribute("title")

            if meeting_link == details:
                Report.logPass(f'The meeting {meeting_title} detail link matches event\'s link', screenshot=True)
            else:
                Report.logFail(f'The meeting {meeting_title} detail link does not match event\'s link',
                               screenshot=True)

            copy_link = self.tune_app.look_element(TunesAppLocators.MEETING_COPY_LINK_URL).get_attribute("title")
            if copy_link == hangout_link:
                Report.logPass(f'The meeting {meeting_title} meeting link matches event\'s link', screenshot=True)
            else:
                Report.logFail(f'The meeting {meeting_title} meeting link does not match event\'s link',
                               screenshot=True)
                
            # guest_email_list_parsed = set([el["email"] for el in guests_email_list])
            guest_email_list_parsed = set(guests_email_list)
            invited_people_tune_wd = self.tune_app.look_all_elements(TunesAppLocators.CALENDAR_ATTENDEE_LABEL)
            invited_people_tune = set(el.text for el in invited_people_tune_wd)
            if guest_email_list_parsed.issubset(invited_people_tune):
                Report.logPass(f'All invited people are present on tune list', screenshot=True)
            else:
                Report.logFail(f'Not Every invited person is present on tune list',
                               screenshot=True)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if event:
                self.calendar_api.delete_event(event_id=event['id'])
            self.tune_app.look_element(TunesAppLocators.MEETING_DETAIL_BUTTON_BACK).click()

    def create_event_for_coily_agenda_verification(self, meeting_title, start_time, meeting_duration_min=60,
                                                   guests_email_list=None):
        try:

            start_time = start_time
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=meeting_duration_min,
                attendees=guests_email_list
            )
            return event['id']
        except Exception as e:
            Report.logException(str(e))

    def create_all_day_event_for_coily_agenda_verification(self, meeting_title, start_time, meeting_duration_days=1,
                                                           guests_email_list=None, location: Optional[str] = None, description: Optional[str] = None):
        try:

            event = self.calendar_api.create_all_day_event(
                start_time=start_time, summary=meeting_title, duration_days=meeting_duration_days,
                attendees=guests_email_list, location=location,description=description
            )
            return event['id']
        except Exception as e:
            Report.logException(str(e))

    def delete_coily_meeting_by_event_id(self, event_id):
        try:
            self.calendar_api.delete_event(event_id=event_id)
        except Exception as e:
            Report.logException(str(e))

    def tc_verify_multiple_guests_invited_number_updated(self):

        """
           account: google or microsoft
           """
        event = None
        time_now = datetime.now()
        guests_number = random.randint(2, 5)
        guests_email_list = [self.generate_random_mail() for _ in range(guests_number)]

        try:
            meeting_title = f'Test event: {time_now.hour}:{time_now.minute}:{time_now.second}'

            start_time = time_now + timedelta(minutes=5)
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=10,
                attendees=guests_email_list
            )
            guests_email_dict = [{"email": x} for x in guests_email_list]

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self._click_today_in_calendar()
            self.tune_app.click_refresh_calendar_button()

            meeting_element = self.tune_app.verify_meeting_title(meeting_title)
            attendees = self.tune_app.look_element(TunesAppLocators.ATTENDEES_NUMBER)

            no_of_invited_before_update = int(attendees.text)
            Report.logInfo(f"Number of invited people before update: {no_of_invited_before_update}",
                           screenshot=True)
            meeting_element.click()
            meeting_page = self.tune_app.verify_element(TunesAppLocators.MEETING_DETAIL_MEETING_TITLE)
            if meeting_page:
                meeting_title_page_title = self.tune_app.look_element(
                    TunesAppLocators.MEETING_DETAIL_MEETING_TITLE).text
                if meeting_title == meeting_title_page_title:
                    Report.logPass("Meeting title in meeting details page matches")
                else:
                    Report.logFail("Meeting title in meeting details page does not match")
            else:
                Report.logFail("Meeting details page not loaded")

            Report.logInfo("Checking invited people list before update", screenshot=True)
            guest_email_list_parsed = set([el["email"] for el in guests_email_dict])

            invited_people_tune_wd = self.tune_app.look_all_elements(TunesAppLocators.CALENDAR_ATTENDEE_LABEL)
            invited_people_tune = set(el.text for el in invited_people_tune_wd)

            if not guest_email_list_parsed.issubset(invited_people_tune):
                Report.logFail("Invited people list is not correct before event update",
                               screenshot=True)

            self.tune_app.look_element(TunesAppLocators.MEETING_DETAIL_BUTTON_BACK).click()

            popped_rand = random.choice(guests_email_list)
            updated_attendees = [attendee for attendee in guests_email_list if attendee != popped_rand]
            for attendee in guests_email_dict:
                if attendee['email'] == popped_rand:
                    guests_email_dict.remove(attendee)
                    break

            Report.logInfo(f'Updating number of invited people')
            self.calendar_api.update_attendees_list(event_id=event['id'], emails=updated_attendees)
            time.sleep(1)
            self.tune_app.click_refresh_calendar_button()
            time.sleep(2)

            attendees_after_update = self.tune_app.look_element(TunesAppLocators.ATTENDEES_NUMBER)
            no_of_invited_after_update = int(attendees_after_update.text)
            Report.logInfo(f"Number of invited people after update: {no_of_invited_after_update}",
                           screenshot=True)

            if no_of_invited_after_update + 1 == no_of_invited_before_update:
                Report.logPass("Number of invited people after update match")
            else:
                Report.logFail("Number of invited people after update not match",
                               screenshot=True)
            meeting_element = self.tune_app.verify_meeting_title(meeting_title)
            meeting_element.click()
            after_update_invited_people_tune_wd = (
                self.tune_app.look_all_elements(TunesAppLocators.CALENDAR_ATTENDEE_LABEL))
            after_update_invited_people_tune = set(el.text for el in after_update_invited_people_tune_wd)
            if set([el["email"] for el in guests_email_dict]).issubset(after_update_invited_people_tune):
                Report.logPass("Invited people list is correct after event update", screenshot=True)
            else:
                Report.logFail("Invited people list is not correct after event update",
                               screenshot=True)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tune_app.verify_element(TunesAppLocators.MEETING_DETAIL_BUTTON_BACK):
                self.tune_app.look_element(TunesAppLocators.MEETING_DETAIL_BUTTON_BACK).click()
            if event:
                self.calendar_api.delete_remaining_events()

    def tc_verify_event_absence(self):
        """
        account: google or microsoft
        """
        event = None
        try:
            meeting_title = f'Test event: {datetime.now()}'

            start_time = datetime.now() + timedelta(minutes=30)
            event = self.calendar_api.create_event(
                start_time=start_time, summary=meeting_title, duration_min=30)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            if self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=20):
                self.calendar_api.delete_event(event_id=event['id'])
                time.sleep(3)
                self.tune_app.click_refresh_calendar_button()

                if not self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=5):
                    Report.logPass(f"Event {meeting_title} deleted and not displayed in Logi Tune")
                else:
                    Report.logFail(f"Deleting event {meeting_title} FAILED. "
                                   f"The event still visible in Logi Tune.", True)
            else:
                Report.logFail(f"Deleting event {meeting_title} could not be verified "
                               f"because the event was not displayed in Logi Tune", True)

        except Exception as e:
            Report.logException(str(e))

    @staticmethod
    def _wait_until(hour: int, minute: int):
        Report.logInfo(f'Waiting until {hour:02d}:{minute:02d}.')
        while datetime.now().time() < dt_time(hour=hour, minute=minute):
            time.sleep(1)
        time.sleep(15)
        Report.logInfo(f'Time now: {datetime.now().hour:02d}:'
                       f'{datetime.now().minute:02d}:{datetime.now().second:02d}')

    def tc_verify_event_countdown_label(self):
        """
        account: google or microsoft
        """
        try:
            meeting_start_min = 2
            meeting_duration_min = 2
            now = datetime.now()

            title = f'Test event: {datetime.now()}'
            start_time = now + timedelta(minutes=meeting_start_min)
            end_time = now + timedelta(minutes=meeting_start_min + meeting_duration_min)

            self.calendar_api.create_event(
                start_time=start_time, summary=title, duration_min=meeting_duration_min)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            # Verify start meeting
            time.sleep(5)
            label = self.tune_app.get_meeting_countdown_label_text(title)
            verify_label = len(re.findall('in [1,2] min', label))
            if verify_label:
                Report.logPass('Label "in [1,2] min" displayed properly before the meeting')
            else:
                Report.logFail(f'Label "in [1,2] min" NOT displayed properly before the meeting. '
                               f'There is "{label}" instead.', screenshot=True)

            button_text = self.tune_app.get_join_button_text(title)
            if button_text == 'JOIN EARLY':
                Report.logPass('Button "JOIN EARLY" displayed properly before the meeting')
            else:
                Report.logFail(f'Button "JOIN EARLY" NOT displayed properly before the meeting. '
                               f'There is {button_text} instead.', screenshot=True)

            # Verify now
            self._wait_until(start_time.hour, start_time.minute)
            label = self.tune_app.get_meeting_countdown_label_text(title)
            if label == 'Now':
                Report.logPass('Label "Now" displayed properly during the meeting')
            else:
                Report.logFail(f'Label "Now" NOT displayed properly during the meeting. '
                               f'There is "{label}" instead.', screenshot=True)

            button_text = self.tune_app.get_join_button_text(title)
            if button_text == 'JOIN NOW':
                Report.logPass('Button "JOIN NOW" displayed properly during the meeting')
            else:
                Report.logFail(f'Button "JOIN NOW" displayed properly during the meeting. '
                               f'There is {button_text} instead.', screenshot=True)

            # Verify end meeting
            self._wait_until(end_time.hour, end_time.minute - 1)
            label = self.tune_app.get_meeting_countdown_label_text(title)
            if label == '1 min left':
                Report.logPass('Label "1 min left" displayed properly during the meeting')
            else:
                Report.logFail(f'Label "1 min left" NOT displayed properly during the meeting. '
                               f'There is "{label}" instead.', screenshot=True)

            button_text = self.tune_app.get_join_button_text(title)
            if button_text == 'JOIN NOW':
                Report.logPass('Button "JOIN NOW" displayed properly during the meeting')
            else:
                Report.logFail(f'Button "JOIN NOW" displayed properly during the meeting. '
                               f'There is {button_text} instead.', screenshot=True)

        except Exception as e:
            Report.logException(str(e))

    def tc_update_event_data(self):
        """
        account: google or microsoft
        """
        output = None
        pattern = '%I:%M %p'
        try:
            meeting_start_min = 30
            meeting_duration_min = 30
            now = datetime.now()

            title = f'Test event: {datetime.now()}'
            start_time = now + timedelta(minutes=meeting_start_min)
            end_time = now + timedelta(minutes=meeting_start_min + meeting_duration_min)

            output = self.calendar_api.create_event(
                start_time=start_time, summary=title, duration_min=meeting_duration_min)

            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_refresh_calendar_button()

            # Verify start meeting
            time.sleep(5)
            label = self.tune_app.get_meeting_countdown_label_text(title)
            verify_label = len(re.findall(r'in \d{1,2} min', label))
            if verify_label:
                Report.logPass(f'Label "{label}" displayed properly before the meeting')
            else:
                Report.logFail(f'Label NOT displayed properly before the meeting. '
                               f'There is "{label}" instead.', screenshot=True)

            time_label = self.tune_app.get_meeting_time_duration_label_text(title)
            if time_label:
                start_event_time, end_event_time = [datetime.strptime(timestamp.strip(), pattern)
                                                    for timestamp in time_label.split('-')]
                if start_event_time.hour == start_time.hour and \
                        start_event_time.minute == start_time.minute:
                    Report.logPass(f'Event start time is same as set during event creation - '
                                   f'"{start_time.strftime(pattern)}"')
                else:
                    Report.logFail(f'Event start time is different from the one set during event '
                                   f'creation - Expected: "{start_time.strftime(pattern)}", '
                                   f'Observed: "{start_event_time.strftime(pattern)}"',
                                   screenshot=True)
                if end_event_time.hour == end_time.hour and \
                        end_event_time.minute == end_time.minute:
                    Report.logPass(f'Event end time is same as set during event creation - '
                                   f'"{end_time.strftime(pattern)}"')
                else:
                    Report.logFail(f'Event end time is different from the one set during event '
                                   f'creation - Expected: "{end_time.strftime(pattern)}", '
                                   f'Observed: "{end_event_time.strftime(pattern)}"',
                                   screenshot=True)

            meeting_start_min = 45
            meeting_duration_min = 45
            new_start_time = now + timedelta(minutes=meeting_start_min)
            new_end_time = now + timedelta(minutes=meeting_start_min + meeting_duration_min)
            Report.logInfo(f'Updating event to start at {new_start_time.strftime(pattern)}, '
                           f'and should lasts {meeting_duration_min} minutes.')

            output = self.calendar_api.update_event(event_id=output.get('id'),
                                                    start_time=new_start_time,
                                                    duration_min=meeting_duration_min,
                                                    summary=title)

            time.sleep(5)
            self.tune_app.click_refresh_calendar_button()
            time.sleep(5)

            # Verify now
            label = self.tune_app.get_meeting_countdown_label_text(title)
            verify_label = len(re.findall(r'in \d{1,2} min', label))
            if verify_label:
                Report.logPass(f'Label "{label}" displayed properly before the meeting')
            else:
                Report.logFail(f'Label NOT displayed properly before the meeting. '
                               f'There is "{label}" instead.', screenshot=True)

            time_label = self.tune_app.get_meeting_time_duration_label_text(title)
            if time_label:
                pattern = '%I:%M %p'
                start_event_time, end_event_time = [datetime.strptime(timestamp.strip(), pattern)
                                                    for timestamp in time_label.split('-')]
                if start_event_time.hour == new_start_time.hour and \
                        start_event_time.minute == new_start_time.minute:
                    Report.logPass(f'Event start time is same as set during event creation - '
                                   f'"{new_start_time.strftime(pattern)}"')
                else:
                    Report.logFail(f'Event start time is different from the one set during event '
                                   f'creation - Expected: "{new_start_time.strftime(pattern)}", '
                                   f'Observed: "{start_event_time.strftime(pattern)}"',
                                   screenshot=True)
                if end_event_time.hour == new_end_time.hour and \
                        end_event_time.minute == new_end_time.minute:
                    Report.logPass(f'Event end time is same as set during event creation - '
                                   f'"{new_end_time.strftime(pattern)}"')
                else:
                    Report.logFail(f'Event end time is different from the one set during event '
                                   f'creation - Expected: "{new_end_time.strftime(pattern)}", '
                                   f'Observed: "{end_event_time.strftime(pattern)}"',
                                   screenshot=True)

        except Exception as e:
            Report.logException(str(e))
        finally:
            self.calendar_api.delete_remaining_events()

    def tc_verify_enable_disable_calendar(self):
        """
        account: google or microsoft
        """
        try:
            self.disable_calendar()
            time.sleep(10)

            if not self.tune_app.verify_home():
                Report.logPass('After disabling calendar no Agenda is visible')
            else:
                Report.logFail('After disabling calendar Agenda is still visible', screenshot=True)

            self.tune_app.relaunch_tune_app()
            self.enable_calendar()
            self.tune_app.relaunch_tune_app()
            time.sleep(10)

            if self.tune_app.verify_sign_int_button_is_displayed():
                Report.logPass('After disable/enable calendar sequence no account is logged in')
            else:
                Report.logFail(f'After disable/enable calendar sequence there is logged in account', screenshot=True)
        except Exception as e:
            Report.logException(str(e))

    def disable_calendar(self):
        self.tune_app.click_tune_menu()
        self.tune_app.click_app_settings()
        self.tune_app.click_calendar_and_meetings()
        time.sleep(0.5)
        self.tune_app.click_disable_calendar()
        time.sleep(0.5)
        self.tune_app.click_disable_and_relaunch_app()

    def enable_calendar(self):
        self.tune_app.click_tune_menu()
        self.tune_app.click_app_settings()
        self.tune_app.click_calendar_and_meetings()
        time.sleep(0.5)
        self.tune_app.click_enable_and_relaunch_app()

