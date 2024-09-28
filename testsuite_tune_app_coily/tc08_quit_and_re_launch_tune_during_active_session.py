import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE
from base.base_coily import CoilyBase


class QuitAndRelaunchTuneDuringActiveSession(CoilyBase):

    def test_8001_VC_126331_quit_and_relaunch_tune_during_anonymous_walkin_session(self):
        self.coily_test_methods.tc_quit_and_relaunch_tune_during_active_session(session_type='walk-in',
                                                                           account_type='anonymous',
                                                                           credentials='')

    def test_8002_VC_126332_quit_and_relaunch_tune_during_identified_walkin_session(self):
        self.coily_test_methods.tc_quit_and_relaunch_tune_during_active_session(session_type='walk-in',
                                                                           account_type=GOOGLE,
                                                                           credentials=self.google_credentials)

    def test_8003_VC_126333_quit_and_relaunch_tune_during_booked_session(self):
        self.coily_test_methods.tc_quit_and_relaunch_tune_during_active_session(session_type='reserved',
                                                                           account_type=GOOGLE,
                                                                           credentials=self.google_credentials)


if __name__ == "__main__":
    unittest.main()
