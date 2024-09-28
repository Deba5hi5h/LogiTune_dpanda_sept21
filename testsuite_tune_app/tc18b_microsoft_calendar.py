import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.collabos.coily.tune_coily_config import MICROSOFT
from apps.collabos.coily.utilities import prepare_tune_calendar_account_credentials
from apps.tune.tune_calendar_methods import CalendarMethods
from base.base_ui import UIBase


class MicrosoftCalendarTests(UIBase):
    tune_app = None
    calendar_methods = None
    account_credentials = prepare_tune_calendar_account_credentials(account_type=MICROSOFT)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.tune_app = TuneElectron()
        cls.calendar_methods = CalendarMethods(account_type=MICROSOFT, tests_type='calendar')
        cls.calendar_methods.delete_remaining_events()

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

    def test_18101_VC_130670_connect_to_microsoft_calendar(self):
        self.calendar_methods.connect_to_work_or_agenda_account(account_type=MICROSOFT,
                                                                test_type='calendar',
                                                                account_credentials=self.account_credentials)

    def test_18102_VC_130671_verify_event_presence_microsoft(self):
        self.calendar_methods.tc_verify_event_presence()

    def test_18103_VC_130672_verify_event_absence_microsoft(self):
        self.calendar_methods.tc_verify_event_absence()

    def test_18104_VC_130673_tc_verify_event_join_microsoft(self):
        self.calendar_methods.tc_verify_event_countdown_label()

    def test_18105_VC_130674_verify_multiple_events_presence_microsoft(self):
        self.calendar_methods.tc_verify_multiple_events_presence(number=10)

    def test_18106_VC_130675_verify_tomorrow_event_presence_microsoft(self):
        self.calendar_methods.tc_verify_tomorrow_event_presence()

    def test_18107_VC_130676_verify_the_day_after_tomorrow_event_presence_microsoft(self):
        self.calendar_methods.tc_verify_the_day_after_tomorrow_event_presence()

    def test_18108_VC_130678_verify_the_next_week_event_presence_microsoft(self):
        self.calendar_methods.tc_verify_the_next_week_event_presence()

    def test_18109_VC_130679_verify_the_next_month_event_presence_microsoft(self):
        self.calendar_methods.tc_verify_the_next_month_event_presence()

    def test_18110_VC_130680_verify_multiple_people_invited_number(self):
        self.calendar_methods.tc_verify_multiple_guests_invited_number(account_type=MICROSOFT)

    def test_18111_VC_130681_verify_multiple_guests_invited_number_updated(self):
        self.calendar_methods.tc_verify_multiple_guests_invited_number_updated()

    def test_18112_VC_130682_verify_updated_event_change(self):
        if self.calendar_methods.verify_sign_in_button_is_displayed():
            self.calendar_methods.connect_to_work_or_agenda_account(account_type=MICROSOFT,
                                                                    test_type='calendar',
                                                                    account_credentials=self.account_credentials)
        self.calendar_methods.tc_update_event_data()

    def test_18113_VC_130677_verify_disable_enable_microsoft_calendar(self):
        self.calendar_methods.tc_verify_enable_disable_calendar()


if __name__ == "__main__":
    unittest.main()
