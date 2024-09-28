import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class BookedSessions(CoilyBase):

    def test_4001_VC_112872_booked_google_session_and_user_not_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_user_not_logged_in(self.google_credentials)

    def test_4002_VC_112873_booked_microsoft_session_and_user_not_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_user_not_logged_in(self.microsoft_credentials)

    ###############################

    def test_4003_VC_112874_booked_google_session_and_google_user_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_user_logged_in(account_type=GOOGLE,
                                                                     credentials=self.google_credentials)

    def test_4004_VC_112875_booked_microsoft_session_and_microsoft_user_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_user_logged_in(account_type=MICROSOFT,
                                                                     credentials=self.microsoft_credentials)

    ###############################

    def test_4005_VC_112876_booked_google_session_and_google_user_logged_in_coily_reconnection(self):
        self.coily_test_methods.tc_booked_session_and_user_logged_in_coily_reconnection(account_type=GOOGLE,
                                                                                        credentials=
                                                                                        self.google_credentials)

    def test_4006_VC_112877_booked_microsoft_session_and_microsoft_user_logged_in_coily_reconnection(self):
        self.coily_test_methods.tc_booked_session_and_user_logged_in_coily_reconnection(account_type=MICROSOFT,
                                                                                        credentials=
                                                                                        self.microsoft_credentials)

    ###############################

    def test_4007_VC_112878_booked_google_session_and_microsoft_user_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_wrong_user_logged_in(
            work_account_type_wrong_user=GOOGLE,
            credentials_wrong_user=self.google_credentials,
            reservation_user_credentials=self.microsoft_credentials)

    def test_4008_VC_112879_booked_microsoft_session_and_google_user_logged_in(self):
        self.coily_test_methods.tc_booked_session_and_wrong_user_logged_in(
            work_account_type_wrong_user=MICROSOFT,
            credentials_wrong_user=self.microsoft_credentials,
            reservation_user_credentials=self.google_credentials)

    ###############################

    def test_4009_VC_112882_booked_google_session_reconnect_to_correct_pc_after_previously_connected_to_laptop_with_wrong_work_account(self):
        self.coily_test_methods.tc_booked_session_reconnect_to_laptop_with_correct_work_account_connected(
            work_account_type_wrong_user=MICROSOFT,
            work_account_type_correct_user=GOOGLE,
            credentials_wrong_user=self.microsoft_credentials,
            credentials_correct_user=self.google_credentials,
            reservation_user_credentials=self.google_credentials)

    def test_4010_VC_112883_booked_microsoft_session_reconnect_to_correct_pc_after_previously_connected_to_laptop_with_wrong_work_account(self):
        self.coily_test_methods.tc_booked_session_reconnect_to_laptop_with_correct_work_account_connected(
            work_account_type_wrong_user=GOOGLE,
            work_account_type_correct_user=MICROSOFT,
            credentials_wrong_user=self.google_credentials,
            credentials_correct_user=self.microsoft_credentials,
            reservation_user_credentials=self.microsoft_credentials)

    ###############################

    def test_4011_VC_112880_booked_google_session_correct_user_logged_in_after_previously_wrong_person_logged_in(self):
        self.coily_test_methods.tc_booked_session_correct_user_logged_in_after_previously_wrong_person_logged_in(
            work_account_type_wrong_user=MICROSOFT,
            work_account_type_correct_user=GOOGLE,
            credentials_wrong_user=self.microsoft_credentials,
            credentials_correct_user=self.google_credentials,
            reservation_user_credentials=self.google_credentials)

    def test_4012_VC_112881_booked_microsoft_session_correct_user_logged_in_after_previously_wrong_person_logged_in(self):
        self.coily_test_methods.tc_booked_session_correct_user_logged_in_after_previously_wrong_person_logged_in(
            work_account_type_wrong_user=GOOGLE,
            work_account_type_correct_user=MICROSOFT,
            credentials_wrong_user=self.google_credentials,
            credentials_correct_user=self.microsoft_credentials,
            reservation_user_credentials=self.microsoft_credentials)


if __name__ == "__main__":
    unittest.main()
