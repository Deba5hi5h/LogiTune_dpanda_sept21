from apps.tune.pages.base_page import WebDriver

from apps.tune.pages.basecamp_page import TuneBasecampPage
from apps.tune.pages.connected_account_settings_page import TuneConnectedAccountSettingsPage
from apps.tune.pages.desk_booking_page import TuneDeskBookingPage
from apps.tune.pages.desk_booking_time_selection_page import TuneDeskBookingTimeSelectionPage
from apps.tune.pages.desk_successfully_booked_page import TuneDeskSuccessfullyBookedPage
from apps.tune.pages.header_page import TuneHeaderPage
from apps.tune.pages.home_page import TuneHomePage
from apps.tune.pages.light_page import TuneLightPage
from apps.tune.pages.notify_teammates_page import TuneNotifyTeammatesPage
from apps.tune.pages.onboarding_page import TuneOnboardingPage
from apps.tune.pages.people_page import TunePeoplePage
from apps.tune.pages.people_team_add_teammates_page import TunePeopleTeamAddTeammatesPage
from apps.tune.pages.people_team_page import TunePeopleTeamPage
from apps.tune.pages.people_team_edit_page import TunePeopleTeamEditPage
from apps.tune.pages.people_teams_edit_page import TunePeopleTeamsEditPage
from apps.tune.pages.settings_page import TuneSettingsPage
from apps.tune.pages.sign_in_page import TuneSignInPage
from apps.tune.pages.meeting_details_page import TuneMeetingDetailPage
from apps.tune.pages.user_profile_page import TuneUserProfilePage
from apps.tune.pages.calendar_and_meetings_page import TuneCalendarAndMeetingsPage
from apps.tune.pages.notifications_page import TuneNotificationsPage
from apps.tune.pages.about_page import TuneAboutPage
from apps.tune.pages.people_user_page import TunePeopleUserPage
from apps.tune.pages.people_user_manage_teams_page import TunePeopleUserManageTeamsPage
from apps.tune.pages.people_in_office_page import TunePeopleInOfficePage
from apps.tune.pages.maps_page import TuneMapsPage
from apps.tune.pages.desk_on_map_page import TuneDeskOnMapPage
from apps.tune.pages.desk_successfully_transferred_page import TuneDeskSuccessfullyTransferredPage


class TunePages:
    def __init__(self, driver: WebDriver):
        self.about_page = TuneAboutPage(driver)
        self.basecamp = TuneBasecampPage(driver)
        self.connected_account_settings = TuneConnectedAccountSettingsPage(driver)
        self.desk_booking = TuneDeskBookingPage(driver)
        self.desk_booking_time_selection = TuneDeskBookingTimeSelectionPage(driver)
        self.desk_successfully_booked = TuneDeskSuccessfullyBookedPage(driver)
        self.header = TuneHeaderPage(driver)
        self.home = TuneHomePage(driver)
        self.light_page = TuneLightPage(driver)
        self.meeting_detail_page = TuneMeetingDetailPage(driver)
        self.notify_teammates = TuneNotifyTeammatesPage(driver)
        self.onboarding = TuneOnboardingPage(driver)
        self.people = TunePeoplePage(driver)
        self.people_team = TunePeopleTeamPage(driver)
        self.people_team_add_teammate = TunePeopleTeamAddTeammatesPage(driver)
        self.people_team_edit = TunePeopleTeamEditPage(driver)
        self.people_teams_edit = TunePeopleTeamsEditPage(driver)
        self.people_user = TunePeopleUserPage(driver)
        self.people_user_manage_teams = TunePeopleUserManageTeamsPage(driver)
        self.people_in_office = TunePeopleInOfficePage(driver)
        self.settings = TuneSettingsPage(driver)
        self.sign_in = TuneSignInPage(driver)
        self.maps = TuneMapsPage(driver)
        self.desk_on_map = TuneDeskOnMapPage(driver)
        self.desk_transferred = TuneDeskSuccessfullyTransferredPage(driver)
        self.user_profile_page = TuneUserProfilePage(driver)
        self.calendar_and_meetings_page = TuneCalendarAndMeetingsPage(driver)
        self.notifications_page = TuneNotificationsPage(driver)
