import json
import os
import random
import time
from abc import ABC, abstractmethod
from typing import Optional, Union, List

import google.auth.exceptions
import pytz
from tzlocal import get_localzone_name

from common.platform_helper import retry_request

import datefinder
from datetime import datetime, timedelta, date
import requests

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from apps.browser_methods import BrowserClass
from apps.collabos.coily.utilities import prepare_ms_api_credentials
from apps.tune.tune_browser import TuneBrowser
from base import global_variables
from base.base_ui import UIBase
from common.framework_params import GOOGLE_ACCOUNT, GOOGLE_PASSWORD
from threading import Thread

from extentreport.report import Report

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_TOKEN_PATH = r'apps/tune/token_calendar.json'
COILY_CALENDAR_PATH = r'apps/tune/token_coily.json'


class CalendarApi(ABC):

    @abstractmethod
    def create_event(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_event(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_all_day_event(self, *args, **kwargs):
        pass

    @abstractmethod
    def change_user_response_for_event(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_event_body(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_event(self, *args, **kwargs):
        pass

    @staticmethod
    def delete_remaining_events(self):
        pass

    @abstractmethod
    def get_events(self, *args, **kwargs):
        pass

    @staticmethod
    def update_attendees_list(self, *args, **kwargs):
        pass
    

class GoogleCalendarApi(UIBase, CalendarApi):

    def __init__(self, token_short_path=CALENDAR_TOKEN_PATH,
                 email=GOOGLE_ACCOUNT, password=GOOGLE_PASSWORD, employee_id=None):
        """
        Initialization method for Google Calendar API.
        Based on credentials.json (stored in apps/tune folder), it will download token.json if it does not exist
        by login to accounts using browser. This will be for the first time only
        Subsequent executions, token will be refreshed if it is expired. Refresh token will have life span of few years
        and hence not required to delete. Just need to refresh when expires.
        """
        super().__init__()
        self.creds = None

        token_path = os.path.join(UIBase.rootPath, token_short_path)
        credentials_path = os.path.join(UIBase.rootPath, 'apps/tune/credentials.json')
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not self.creds or not self.creds.valid:
            try:
                self.creds.refresh(Request())       # TODO: Does not work!
            except (google.auth.exceptions.RefreshError, AttributeError):
                # Executing this for the first time, need to enter credentials
                browser = BrowserClass()
                browser.prepare_opened_browser(guest_mode=True)
                time.sleep(5)
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                t1 = Thread(target=self._flow_method, args=(flow,))
                t1.daemon = True
                t1.start()
                driver = global_variables.driver
                global_variables.driver = browser.connect_to_google_accounts_browser_page()
                tune_browser = TuneBrowser()
                tune_browser.sign_in_to_google_token(email, password, employee_id)
                time.sleep(2)
                browser.close_all_browsers()
                global_variables.driver = driver
                with open(token_path, 'w') as token:
                    token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _flow_method(self, flow: InstalledAppFlow) -> None:
        self.creds = flow.run_local_server(port=0)

    def create_event_with_description(self, start_time: str, summary: str, duration: Union[int, float], time_zone: str,
                                      description: Optional[str] = None, location: Optional[str] = None) -> dict:
        """
        Method to create event in Google Calendar using Google API
        :param start_time
        :param summary
        :param duration
        :param time_zone
        :param description
        :param location
        :return dict
        """
        Report.logInfo(f"Creating calendar event {summary} starting at {start_time}")
        matches = list(datefinder.find_dates(start_time))
        if len(matches):
            start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': time_zone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return self.service.events().insert(calendarId='primary', body=event).execute()

    def create_event(self, start_time: datetime, summary: str, duration_min: int,
                     description: Optional[str] = None, location: Optional[str] = None,
                     attendees: Optional[List[dict]] = None, video_event: bool = True) -> dict:
        """
        Method to create event in Google Calendar using Google API
        :param start_time: e.g. 2023-06-09 14:38:07.322358, time will be extracted
        :param summary: event name
        :param duration_min: event duration in minutes
        :param description: event description
        :param location
        :param attendees
        :param video_event
        :return dict
        """
        time_zone = get_localzone_name()
        Report.logInfo(f"Creating calendar event '{summary}' starting at {start_time} "
                       f"for timezone {time_zone}")

        end_time = start_time + timedelta(minutes=duration_min)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': time_zone,
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(random.randint(1, 1000)),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
        }
        if attendees:
            attendees_list = []
            for attendee in attendees:
                attendees_list.append({"email": attendee})
            event['attendees'] = attendees_list

        return self.service.events().insert(calendarId='primary', conferenceDataVersion=1 if video_event else 0,
                                            body=event).execute()

    def create_all_day_event(self, start_time: date, summary: str, duration_days: int,
                             description: Optional[str] = None, location: Optional[str] = None,
                             attendees: Optional[List[dict]] = None, video_event: bool = True) -> dict:
        """
        Method to create event in Google Calendar using Google API
        :param start_time: e.g. 2023-06-09 14:38:07.322358, time will be extracted
        :param summary: event name
        :param duration_days: event duration in minutes
        :param description: event description
        :param location
        :param attendees
        :param video_event
        :return dict
        """
        time_zone = get_localzone_name()
        Report.logInfo(f"Creating calendar event '{summary}' starting at {start_time} "
                       f"for timezone {time_zone}")

        end_time = start_time + timedelta(days=duration_days)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'date': start_time.isoformat(),
                'timeZone': time_zone,
            },
            'end': {
                'date': end_time.isoformat(),
                'timeZone': time_zone,
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(random.randint(1, 1000)),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
        }
        if attendees:
            attendees_list = []
            for attendee in attendees:
                attendees_list.append({"email": attendee})
            event['attendees'] = attendees_list

        return self.service.events().insert(calendarId='primary', conferenceDataVersion=1 if video_event else 0,
                                            body=event).execute()

    def update_event(self, event_id: str, start_time: datetime, duration_min: int, summary: str
                     ) -> dict:
        """
        Method to update event from Google Calendar using Google API
        :param event_id
        :param start_time
        :param duration_min
        :param summary
        :return dict
        """
        Report.logInfo(f"Update calendar event with id {event_id}")
        time_zone = get_localzone_name()
        end_time = start_time + timedelta(minutes=duration_min)
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': time_zone,
            },
        }
        return self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()

    def patch_event(self, event_id: str, patch_data: dict) -> dict:
        """
        Method to update event from Google Calendar using Google API
        :param event_id
        :param patch_data
        :return dict
        """
        Report.logInfo(f"Patch calendar event with id {event_id}")

        return self.service.events().update(calendarId='primary', eventId=event_id, body=patch_data).execute()

    def change_user_response_for_event(self, event_id: str, user_mail: str, user_response: str) -> dict:

        return self.service.events().patch(
            calendarId='primary',
            eventId=event_id,
            body={"attendees": [{'email': user_mail, 'responseStatus': user_response}]}).execute()

    def update_event_body(self, event_id: str, event: dict, **kwargs) -> dict:
        """
        Method to update event from Google Calendar using Google API
        :param event_id
        :param event
        :return dict
        """
        for key, value in kwargs.items():
            event[key] = value
        Report.logInfo(f"Update calendar event with id {event_id}")
        return self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()

    def delete_event(self, event_id: str) -> None:
        """
        Method to delete event from Google Calendar using Google API
        :param event_id
        :return none
        """
        Report.logInfo(f"Deleting calendar event with id {event_id}")
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()

    def get_events(self) -> dict:
        """
        Method to get list of available event from Google Calendar using Google API
        :return dict
        """
        Report.logInfo("Getting list of available events from Google Calendar")
        return self.service.events().list(calendarId='primary', singleEvents=True).execute()

    def delete_remaining_events(self):
        try:
            events_response = self.get_events()
            events_remaining = events_response.get('items')
            if events_remaining:
                Report.logInfo(f'Delete remaining events: {len(events_remaining)} events remaining')
                for event in events_remaining:
                    self.delete_event(event.get('id'))
                new_events_response = self.get_events()
                if not new_events_response.get('items'):
                    Report.logInfo('All remaining events has been deleted')
                else:
                    Report.logInfo(f'It was not possible to delete all remaining events - '
                                   f'{len(new_events_response.get("items"))} left')
            else:
                Report.logInfo('There is no remaining events to be deleted')
        except Exception as e:
            Report.logException(e)

    def update_attendees_list(self, event_id: str, emails: list):
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()

        attendees = event.get('attendees', [])

        # Remove a random attendee
        if attendees:
            for atendee in attendees:
                if atendee.get('email') not in emails:
                    attendees.remove(atendee)

        # Update the event with the modified attendees list
        event['attendees'] = attendees
        self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()


class MicrosoftCalendarApi(UIBase, CalendarApi):
    def __init__(self, email: str, password: str) -> None:
        super().__init__()
        api_credentials = prepare_ms_api_credentials()
        self.access_token = self._get_access_token(client_id=api_credentials.get('client_id'),
                                                   client_secret=api_credentials.get('client_secret'),
                                                   tenant_id=api_credentials.get('tenant_id'),
                                                   username=email,
                                                   password=password)
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        self.organizer_email = email

    @staticmethod
    def _get_access_token(client_id, client_secret, username, password, tenant_id):
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
        resource_url = "https://graph.microsoft.com"

        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'resource': resource_url,
            'username': username,
            'password': password,
            'scope': 'https://graph.microsoft.com/.default'
        }

        response = retry_request.post(token_url, data=data, timeout=30)
        assert response.status_code == 200, response.text
        token = response.json().get('access_token')
        return token

    def create_event(self, start_time: datetime, summary: str, duration_min: int,
                     description: Optional[str] = None, location: Optional[str] = None,
                     attendees=None, video_event=True):

        if self.access_token:
            end_time = start_time + timedelta(minutes=duration_min)
            meeting = self._create_graph_api_meeting(summary, start_time, end_time, location, description, attendees,
                                                     video_event)
            return meeting
        return None

    def create_all_day_event(self, start_time: date, summary: str, duration_days: int,
                             description: Optional[str] = None, location: Optional[str] = None,
                             attendees=None, video_event=False):

        if self.access_token:

            end_time = start_time + timedelta(days=duration_days)
            meeting = self._create_graph_api_meeting(summary, start_time, end_time, location, description, attendees,
                                                     video_event, all_day=True)
            return meeting
        return None

    def _create_graph_api_meeting(self, subject, start_time, end_time, location, body, attendees, video_event,
                                  all_day=False):
        graph_api_url = "https://graph.microsoft.com/v1.0/me/events"

        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        data = {
            "subject": subject,
            "start": {"dateTime": start_time, "timeZone": get_localzone_name()},
            "end": {"dateTime": end_time, "timeZone": get_localzone_name()},
            "location": {"displayName": location},
            "body": {"content": body, "contentType": "HTML"},
            "attendees": [{"emailAddress": {"address": self.organizer_email}, "type": "required"}],
            "isOnlineMeeting": video_event,
            "onlineMeetingProvider": "teamsForBusiness" if video_event else None,
            "isAllDay": all_day,
        }

        if attendees:
            for attendee in attendees:
                data["attendees"].append({"emailAddress": {"address": attendee}, "type": "required"})

        response = retry_request.post(graph_api_url, headers=self.headers, json=data, timeout=30)

        if response.status_code == 201:

            data_dict = json.loads(response.text)
            print(f"Meeting {data_dict['id']} created successfully for user {self.organizer_email}")
            return data_dict
        else:
            print(f"Failed to create meeting. Status code: {response.status_code}, Error: {response.text}")
            return None

    @staticmethod
    def _get_current_timezone():
        # Get the current UTC time
        utc_now = datetime.utcnow()

        # Get the timezone aware datetime object
        timezone_aware_now = pytz.utc.localize(utc_now)

        # Get the timezone name
        timezone_name = timezone_aware_now.tzinfo.zone

        return timezone_name

    def update_event(self, event_id: str, start_time: datetime, duration_min: int, summary: str):
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"

        end_time = start_time + timedelta(minutes=duration_min)

        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        update_data = {
            "subject": summary,
            "start": {"dateTime": start_time, "timeZone": get_localzone_name()},
            "end": {"dateTime": end_time, "timeZone": get_localzone_name()},
        }

        response = retry_request.patch(graph_api_url, headers=self.headers, json=update_data, timeout=30)

        if response.status_code == 200:
            print("Event updated successfully.")
        else:
            print(f"Failed to update event. Status code: {response.status_code}, Error: {response.text}")

    def change_user_response_for_event(self, event_id: str, user_mail: str, user_response: str):
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
        return retry_request.patch(
            graph_api_url, headers=self.headers,
            json={'attendees': [{'emailAddress':  {'address': user_mail}, 'status': {'response': user_response}}]},
            timeout=30
        ).json()

    def update_event_body(self, event_id: str, event: dict, **kwargs):
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"

        update_data = {
            "subject": event["subject"],
            "start": event["start"],
            "end": event["end"],
            "location": event["location"],
            "body": event["body"],
            'attendees': event['attendees']
        }

        for key, value in kwargs.items():
            if key == 'attendees':
                for attendee in value:
                    update_data['attendees'].append({'emailAddress': {'address': attendee['email'], 'name': ''},
                                                     'status': {'response': 'none', 'time': '0001-01-01T00:00:00Z'},
                                                     'type': 'required'})
            elif key == 'duration_min':
                update_data['end'] = update_data['start'] + timedelta(minutes=value)
            else:
                update_data[key] = value

        response = retry_request.patch(graph_api_url, headers=self.headers, json=update_data, timeout=30)

        if response.status_code == 200:
            print("Event updated successfully.")
        else:
            print(f"Failed to update event. Status code: {response.status_code}, Error: {response.text}")

    def update_attendees_list(self, event_id: str, emails: list):
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"

        attendees = []
        for email in emails:
            attendees.append({'emailAddress': {'address': f'{email}'}})

        data = {
            'attendees': attendees
        }

        response = retry_request.patch(graph_api_url, headers=self.headers, json=data, timeout=30)

        if response.status_code == 200:
            print("Event updated successfully.")
        else:
            print(f"Failed to update event. Status code: {response.status_code}, Error: {response.text}")

    def delete_event(self, event_id: str):
        graph_api_url = f"https://graph.microsoft.com/v1.0/me/calendar/events/{event_id}"

        response = retry_request.delete(graph_api_url, headers=self.headers, timeout=30)

        if response.status_code == 204:
            print(f"Meeting with ID {event_id} deleted successfully.")
        else:
            print(
                f"Failed to delete meeting with ID {event_id}. Status code: {response.status_code}, Error: {response.text}")

    def get_events(self):
        graph_api_url = "https://graph.microsoft.com/v1.0/me/calendar/events"

        response = retry_request.get(graph_api_url, headers=self.headers, timeout=30)

        if response.status_code == 200:
            events = response.json().get('value', [])
            if events:
                print("All Events:")
                for event in events:
                    subject = event.get('subject', '')
                    start_time = event.get('start', {}).get('dateTime', '')
                    end_time = event.get('end', {}).get('dateTime', '')
                    location = event.get('location', {}).get('displayName', '')

                    print(f"Subject: {subject}")
                    print(f"Start Time: {start_time}")
                    print(f"End Time: {end_time}")
                    print(f"Location: {location}")
                    print("-----------------------------")
                return events
            else:
                print("No events found.")
        else:
            print(f"Failed to retrieve events. Status code: {response.status_code}, Error: {response.text}")

    def delete_remaining_events(self):
        graph_api_url = "https://graph.microsoft.com/v1.0/me/calendar/events"

        response = retry_request.get(graph_api_url, headers=self.headers, timeout=30)

        if response.status_code == 200:
            meetings = response.json().get('value', [])
            if meetings:
                for meeting in meetings:
                    meeting_id = meeting.get('id')
                    delete_url = f"https://graph.microsoft.com/v1.0/me/calendar/events/{meeting_id}"

                    delete_response = retry_request.delete(delete_url, headers=self.headers, timeout=30)

                    if delete_response.status_code == 204:
                        print(f"Meeting with ID {meeting_id} deleted successfully.")
                    else:
                        print(
                            f"Failed to delete meeting with ID {meeting_id}. Status code: {delete_response.status_code}, Error: {delete_response.text}")
            else:
                print("No meetings found to delete.")
        else:
            print(f"Failed to retrieve meetings. Status code: {response.status_code}, Error: {response.text}")


class OutlookCalendarDriver(UIBase):
    """
    A class contains methods to create / delete Outlook calendar events
    """
    def create_outlook_event(self, meeting_title: str) -> None:
        """
        Method to create event in Outlook Calendar using Google API
        :param meeting_title
        :return none
        """
        try:
            browser = BrowserClass()
            driver = global_variables.driver
            global_variables.driver = browser.connect_to_outlook_calendar_browser_page()
            tune_browser = TuneBrowser()
            time.sleep(5)
            Report.logInfo(f"Creating calendar event {meeting_title}")
            tune_browser.add_outlook_calendar_event(meeting_title)
            global_variables.driver = driver

        except Exception as e:
            Report.logException(str(e))

    def delete_outlook_event(self, meeting_title: str) -> None:
        """
        Method to delete event from Outlook Calendar using Google API
        :param meeting_title
        :return none
        """
        try:
            browser = BrowserClass()
            driver = global_variables.driver
            global_variables.driver = browser.connect_to_outlook_calendar_browser_page()
            tune_browser = TuneBrowser()
            time.sleep(5)
            Report.logInfo(f"Deleting calendar event with id {meeting_title}")
            tune_browser.del_outlook_calendar_event()
            global_variables.driver = driver

        except Exception as e:
            Report.logException(str(e))
