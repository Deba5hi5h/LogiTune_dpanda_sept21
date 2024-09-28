
import unittest

from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from base.base_coily import CoilyBase


class CoilySettingsInLogiTune(CoilyBase):

    def tearDown(self):
        self.coily_test_methods.sync_portal_services.set_coily_settings(
            agenda_enabled=True, privacy_mode_enabled=False, time_format="12", screen_brightness=255
        )
        self.coily_test_methods.set_tune_with_sync()
        super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_7001_VC_129105_coily_settings_anonymous_session_check_with_sync_portal(self):
        self.coily_test_methods.tc_settings_anonymous_session_check_with_sync_portal()

    def test_7002_VC_129106_coily_identified_session_change_time_format_on_coily_settings_page(self):
        self.coily_test_methods.tc_identified_session_change_time_format_on_coily_settings_page(account_type=GOOGLE)

    def test_7003_VC_129107_settings_interaction_tune_desktop_coily_settings_with_coily_settings_page(self):
        self.coily_test_methods.tc_settings_interaction_tune_desktop_coily_settings_with_coily_settings_page(
            account_type=GOOGLE)

    def test_7004_VC_129108_identified_session_change_away_message(self):
        self.coily_test_methods.tc_identified_session_change_away_message(account_type=GOOGLE)

    def test_7005_VC_129109_coily_identified_session_privacy_mode_change_visible_on_identified_page(self):
        self.coily_test_methods.tc_coily_identified_session_privacy_mode_change_visible_on_identified_page(
            account_type=GOOGLE)

    def test_7006_VC_129110_coily_identified_session_brightness_in_tune_menu(self):
        self.coily_test_methods.tc_coily_identified_session_brightrness_in_tune_menu(account_type=GOOGLE)

    def test_7007_VC_137870_coily_identified_session_change_time_format_on_coily_settings_page(self):
        self.coily_test_methods.tc_identified_session_change_time_format_on_coily_settings_page(account_type=MICROSOFT)

    def test_7008_VC_137869_settings_interaction_tune_desktop_coily_settings_with_coily_settings_page(self):
        self.coily_test_methods.tc_settings_interaction_tune_desktop_coily_settings_with_coily_settings_page(
            account_type=MICROSOFT)

    def test_7009_VC_137868_identified_session_change_away_message(self):
        self.coily_test_methods.tc_identified_session_change_away_message(account_type=MICROSOFT)

    def test_7010_VC_137867_coily_identified_session_privacy_mode_change_visible_on_identified_page(self):
        self.coily_test_methods.tc_coily_identified_session_privacy_mode_change_visible_on_identified_page(
            account_type=MICROSOFT)
 
    def test_7011_VC_137866_coily_identified_session_brightness_in_tune_menu(self):
        self.coily_test_methods.tc_coily_identified_session_brightrness_in_tune_menu(account_type=MICROSOFT)


if __name__ == "__main__":
    unittest.main()
