import random
import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class EarlyCheckInToBookedSession(CoilyBase):

    def test_6001_VC_119857_anonymous_user_checks_in_less_less_30_minutes_before_some_booked_session(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.google_credentials,
              wrong_user_account_type=None,
              wrong_user='anonymous',
              reservation_delay=random.randint(5, 29))

    def test_6002_VC_119858_anonymous_user_checks_in_more_than_30_but_less_than_60_minutes_before_some_booked_session(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.microsoft_credentials,
              wrong_user_account_type=None,
              wrong_user='anonymous',
              reservation_delay=random.randint(35, 59))

    def test_6003_VC_119859_anonymous_user_checks_in_more_than_60_minutes_before_some_booked_session(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.google_credentials,
              wrong_user_account_type=None,
              wrong_user='anonymous',
              reservation_delay=random.randint(65, 250))

    def test_6004_VC_119860_identified_user_B_checks_in_less_than_30_minutes_before_future_booked_session_for_user_A(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.google_credentials,
              wrong_user_account_type=MICROSOFT,
              wrong_user=self.microsoft_credentials,
              reservation_delay=random.randint(5, 29))

    def test_6005_VC_119861_identified_user_B_checks_in_more_than_30_but_less_than_60_minutes_before_future_booked_session_for_user_A(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.microsoft_credentials,
              wrong_user_account_type=GOOGLE,
              wrong_user=self.google_credentials,
              reservation_delay=random.randint(35, 59))

    def test_6006_VC_119862_identified_user_B_checks_in_more_than_60_minutes_before_future_booked_session_for_user_A(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session(
              correct_user=self.microsoft_credentials,
              wrong_user_account_type=GOOGLE,
              wrong_user=self.google_credentials,
              reservation_delay=random.randint(65, 250))

    def test_6007_VC_119863_identified_user_A_checks_in_less_than_30_minutes_before_his_future_booked_session(self):
        self.coily_test_methods.tc_user_checks_in_before_some_booked_session(
              user_account_type=GOOGLE,
              user_credentials=self.google_credentials,
              reservation_delay=random.randint(5, 29))

    def test_6008_VC_119864_identified_user_A_checks_in_more_than_30_minutes_before_his_future_booked_session(self):
        self.coily_test_methods.tc_user_checks_in_before_some_booked_session(
              user_account_type=MICROSOFT,
              user_credentials=self.microsoft_credentials,
              reservation_delay=random.randint(35, 250))

    def test_6009_VC_119865_identified_user_A_checks_in_less_than_30_minutes_before_his_future_booked_session_when_walk_in_session_is_disabled(self):
        self.coily_test_methods.tc_user_checks_in_before_some_booked_session_when_walk_in_disabled(
              user_account_type=MICROSOFT,
              user_credentials=self.microsoft_credentials,
              reservation_delay=random.randint(5, 29))

    def test_6010_VC_119866_identified_user_A_checks_in_more_than_30_minutes_before_his_future_booked_session_when_walk_in_session_is_disabled(self):
        self.coily_test_methods.tc_user_checks_in_before_some_booked_session_when_walk_in_disabled(
              user_account_type=GOOGLE,
              user_credentials=self.google_credentials,
              reservation_delay=random.randint(35, 250))

    def test_6011_VC_121067_anonymous_user_checks_in_less_less_30_minutes_before_some_booked_session_and_waits_till_end_of_reservation(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session_end_waits_till_the_end(
              correct_user_account_type=GOOGLE,
              correct_user=self.google_credentials,
              wrong_user_account_type=None,
              wrong_user='anonymous',
              reservation_delay=5)

    def test_6012_VC_121068_identified_user_B_checks_in_less_than_30_minutes_before_future_booked_session_for_user_A_and_waits_till_end_of_reservation(self):
        self.coily_test_methods.tc_wrong_user_checks_in_before_some_booked_session_end_waits_till_the_end(
              correct_user_account_type=MICROSOFT,
              correct_user=self.microsoft_credentials,
              wrong_user_account_type=GOOGLE,
              wrong_user=self.google_credentials,
              reservation_delay=5)


if __name__ == "__main__":
    unittest.main()
