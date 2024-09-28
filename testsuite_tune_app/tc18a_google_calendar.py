import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.collabos.coily.tune_coily_config import GOOGLE
from apps.collabos.coily.utilities import prepare_tune_calendar_account_credentials
from apps.tune.tune_calendar_methods import CalendarMethods
from base.base_ui import UIBase


class GoogleCalendarTests(UIBase):
    tune_app = None
    calendar_methods = None
    account_credentials = prepare_tune_calendar_account_credentials(account_type=GOOGLE)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tune_app = TuneElectron()
        cls.calendar_methods = CalendarMethods(account_type=GOOGLE, tests_type='calendar')

        cls.tune_app.connect_tune_app()

        if not cls.tune_app.verify_home():
            cls.calendar_methods.enable_calendar()
            cls.tune_app.relaunch_tune_app()
        if not cls.calendar_methods.verify_sign_in_button_is_displayed():
            cls.calendar_methods.tc_disconnect_connected_account()

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        self.calendar_methods.delete_remaining_events()

    @classmethod
    def tearDownClass(cls) -> None:
        if not cls.calendar_methods.verify_sign_in_button_is_displayed():
            cls.calendar_methods.tc_disconnect_connected_account()
        super().tearDownClass()

    def test_18001_VC_116107_connect_to_google_calendar(self):
        self.calendar_methods.connect_to_work_or_agenda_account(account_type=GOOGLE,
                                                                test_type='calendar',
                                                                account_credentials=self.account_credentials)

    def test_18002_VC_116108_verify_event_presence_google(self):
        self.calendar_methods.tc_verify_event_presence()

    def test_18003_VC_116109_verify_event_absence_google(self):
        self.calendar_methods.tc_verify_event_absence()

    def test_18004_VC_116110_tc_verify_event_join_google(self):
        self.calendar_methods.tc_verify_event_countdown_label()

    def test_18005_VC_116111_verify_multiple_events_presence_google(self):
        self.calendar_methods.tc_verify_multiple_events_presence(number=10)

    def test_18006_VC_116112_verify_tomorrow_event_presence_google(self):
        self.calendar_methods.tc_verify_tomorrow_event_presence()

    def test_18007_VC_116113_verify_the_day_after_tomorrow_event_presence_google(self):
        self.calendar_methods.tc_verify_the_day_after_tomorrow_event_presence()

    def test_18008_VC_125109_verify_the_next_week_event_presence_google(self):
        self.calendar_methods.tc_verify_the_next_week_event_presence()

    def test_18009_VC_125110_verify_the_next_month_event_presence_google(self):
        self.calendar_methods.tc_verify_the_next_month_event_presence()

    def test_18010_VC_125111_verify_multiple_people_invited_number(self):
        self.calendar_methods.tc_verify_multiple_guests_invited_number(account_type=GOOGLE)

    def test_18011_VC_125112_verify_multiple_guests_invited_number_updated(self):
        self.calendar_methods.tc_verify_multiple_guests_invited_number_updated()

    def test_18012_VC_125113_verify_updated_event_change(self):
        if self.calendar_methods.verify_sign_in_button_is_displayed():
            self.calendar_methods.connect_to_work_or_agenda_account(account_type=GOOGLE,
                                                                    test_type='calendar',
                                                                    account_credentials=self.account_credentials)
        self.calendar_methods.tc_update_event_data()

    def test_18013_VC_116114_verify_disable_enable_google_calendar(self):
        self.calendar_methods.tc_verify_enable_disable_calendar()


if __name__ == "__main__":
    unittest.main()
