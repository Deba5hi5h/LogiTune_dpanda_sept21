import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods
from base.base_ui import UIBase


class CalendarIntegration(UIBase):
    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()

    def setUp(self) -> None:
        self.tune_methods.tune_app.connect_tune_app()
        if not self.tune_methods.tune_app.verify_calendar_connect_now():
            self.tune_methods.tc_disconnect_calendar_account()

    def test_181_VC_xxxx_connect_to_outlook_calendar(self):
        self.tune_methods.tc_connect_to_outlook_calendar(guest_mode=True)

    def test_182_VC_xxx_verify_outlook_event(self):
        self.tune_methods.tc_verify_outlook_calendar_event()


if __name__ == "__main__":
    unittest.main()
