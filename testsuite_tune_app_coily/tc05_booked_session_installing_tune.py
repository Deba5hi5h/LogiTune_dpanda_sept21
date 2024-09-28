
import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class BookedSessionsNoTune(CoilyBase):

    def test_5001_VC_112870_booked_google_session_walk_in_disabled_tune_install_user_log_in(self):
        self.coily_test_methods.tc_booked_session_walk_in_disabled_tune_install_user_log_in(
            work_account_type=GOOGLE,
            credentials=self.google_credentials)

    def test_5002_VC_112871_booked_microsoft_session_and_user_not_logged_in(self):
        self.coily_test_methods.tc_booked_session_walk_in_disabled_tune_install_user_log_in(
            work_account_type=MICROSOFT,
            credentials=self.microsoft_credentials)


if __name__ == "__main__":
    unittest.main()
