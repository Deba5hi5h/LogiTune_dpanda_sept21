
import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class WalkInSessionInstallingTune(CoilyBase):

    def test_2001_VC_112858_booked_google_session_walk_in_enabled_tune_install_user_log_in(self):
        self.coily_test_methods.tc_walk_in_enabled_install_tune_log_in_to_work_account(
            work_account_type=GOOGLE,
            credentials=self.google_credentials)

    def test_2002_VC_112859_booked_google_session_walk_in_enabled_tune_install_user_log_in(self):
        self.coily_test_methods.tc_walk_in_enabled_install_tune_log_in_to_work_account(
            work_account_type=MICROSOFT,
            credentials=self.microsoft_credentials)


if __name__ == "__main__":
    unittest.main()
