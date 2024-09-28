import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class AgendaInteractionsDuringActiveSession(CoilyBase):

    def test_9001_VC_131683_add_and_remove_google_events_during_identified_walk_in_session(self):
        self.coily_test_methods.tc_add_and_remove_events_during_identified_session(session_type='walk-in',
                                                                              account_type=GOOGLE,
                                                                              credentials=self.google_credentials)

    def test_9002_VC_131684_add_and_remove_microsoft_events_during_identified_walk_in_session(self):
        self.coily_test_methods.tc_add_and_remove_events_during_identified_session(session_type='walk-in',
                                                                              account_type=MICROSOFT,
                                                                              credentials=self.microsoft_credentials)

    def test_9003_VC_131685_add_and_remove_google_events_during_reserved_session(self):
        self.coily_test_methods.tc_add_and_remove_events_during_identified_session(session_type='reserved',
                                                                              account_type=GOOGLE,
                                                                              credentials=self.google_credentials)

    def test_9004_VC_131687_add_and_remove_microsoft_events_during_reserved_session(self):
        self.coily_test_methods.tc_add_and_remove_events_during_identified_session(session_type='reserved',
                                                                              account_type=MICROSOFT,
                                                                              credentials=self.microsoft_credentials)


if __name__ == "__main__":
    unittest.main()
