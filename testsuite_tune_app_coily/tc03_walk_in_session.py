
import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class WalkInSession(CoilyBase):

    def test_3001_VC_112860_walk_in_session_enabled_user_not_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_enabled_user_not_logged_in()

    ###############################

    def test_3002_VC_112861_walk_in_session_disabled_user_not_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_disabled_user_not_logged_in()

    ###############################

    def test_3003_VC_112862_walk_in_session_enabled_google_user_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_enabled_user_logged_in(account_type=GOOGLE)

    def test_3004_VC_112863_walk_in_session_enabled_microsoft_user_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_enabled_user_logged_in(account_type=MICROSOFT)

    ###############################

    def test_3005_VC_112864_walk_in_session_disabled_google_user_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_disabled_user_logged_in(account_type=GOOGLE)

    def test_3006_VC_112865_walk_in_session_disabled_microsoft_user_logged_in(self):
        self.coily_test_methods.tc_walk_in_session_disabled_user_logged_in(account_type=MICROSOFT)

    ###############################

    def test_3007_VC_112866_walk_in_session_enabled_google_user_logged_in_coily_reconnection(self):
        self.coily_test_methods.tc_walk_in_session_enabled_user_logged_in_coily_reconnection(account_type=GOOGLE)

    def test_3008_VC_112867_walk_in_session_enabled_microsoft_user_logged_in_coily_reconnection(self):
        self.coily_test_methods.tc_walk_in_session_enabled_user_logged_in_coily_reconnection(account_type=MICROSOFT)

    ###############################

    def test_3009_VC_112868_walk_in_session_is_over_on_google_user_disconnect(self):
        self.coily_test_methods.tc_walk_in_session_over_on_work_account_account_disconnection(account_type=GOOGLE)

    def test_3010_VC_112869_walk_in_session_is_over_on_microsoft_user_disconnect(self):
        self.coily_test_methods.tc_walk_in_session_over_on_work_account_account_disconnection(account_type=MICROSOFT)

    def test_3011_VC_143215_walk_in_session_disabled_book_button_check_google(self):
        self.coily_test_methods.tc_walk_in_session_disabled_book_button_check(account_type=GOOGLE)

    def test_3012_VC_143216_walk_in_session_disabled_book_button_check_microsoft(self):
        self.coily_test_methods.tc_walk_in_session_disabled_book_button_check(account_type=MICROSOFT)

    def test_3013_VC_143218_walk_in_session_different_desk_booked_google(self):
        self.coily_test_methods.tc_walk_in_session_different_desk_booked(account_type=GOOGLE)

    def test_3014_VC_143217_walk_in_session_different_desk_booked_microsoft(self):
        self.coily_test_methods.tc_walk_in_session_different_desk_booked(account_type=MICROSOFT)


if __name__ == "__main__":
    unittest.main()
