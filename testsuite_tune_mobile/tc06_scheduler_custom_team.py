import unittest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data


class SchedulerCustomTeam(MobileBase):
    tc_methods = TuneMobileTests()
    teammate_added = True

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Custom Team"
        super(SchedulerCustomTeam, cls).setUpClass()
        if global_variables.reportInstance is None:
            global_variables.reportInstance = global_variables.extent.createTest("People Setup", "Test Case Details")
        cls.tc_methods.close()
        cls.tc_methods.open_app()
        if not cls.tc_methods.dashboard.verify_home():
            cls.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.user_email(), verification=False,
                                                  site_name=TuneMobileConfig.site(),
                                                  building_name=TuneMobileConfig.building(),
                                                  teammates=test_data.tc_signin_teammates)

    def test_6001_VC_128149_custom_team_all_teammates(self):
        self.tc_methods.tc_custom_team_all_teammates()

    def test_6002_VC_128150_custom_team_create_new_team(self):
        self.tc_methods.tc_custom_team_create_new_team(team_name="Test1")

    def test_6003_VC_128152_custom_team_add_teammates_screen(self):
        self.tc_methods.tc_custom_team_add_teammates_screen(team_name="Test1")

    def test_6004_VC_128154_custom_team_multiple_teams(self):
        self.tc_methods.tc_custom_team_multiple_teams(team_name1="Test1", team_name2="Test2",
                                                      teammates1=['Naveen xavier', 'Uday Handi'],
                                                      teammates2=['Mamata T A', 'Uday Handi'])

    def test_6005_VC_128155_custom_team_all_teammates_search(self):
        self.tc_methods.tc_custom_team_all_teammates_search(team_name="Test1")

    def test_6006_VC_128157_custom_team_team_member_profile(self):
        self.tc_methods.tc_custom_team_team_member_profile(team_name1="Test1", team_name2="Test2",
                                                           teammates1=['Naveen xavier', 'Uday Handi'],
                                                           teammates2=['Mamata T A', 'Uday Handi'])

    def test_6007_VC_128153_custom_team_add_teammates_from_groups(self):
        self.tc_methods.tc_custom_team_add_teammates_from_groups(team_name="Custom_Team")

    def test_6008_VC_128156_custom_team_add_teammates_to_all_teammates(self):
        self.tc_methods.tc_custom_team_add_teammates_to_all_teammates()

    def test_6009_VC_128158_custom_team_teammate_with_bookings(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_custom_team_teammate_with_bookings(team_name="qa-team",
                                                              desk_name=TuneMobileConfig.user_desk(),
                                                              start=start, end=end, day=0)

    def test_6010_VC_130489_custom_team_teammate_with_no_bookings(self):
        self.tc_methods.tc_custom_team_teammate_with_no_bookings(team_name="dev-team")

    def test_6011_VC_128159_custom_team_update_name(self):
        self.tc_methods.tc_custom_team_update_name(team_name="dev-team", new_team="QA-Team")

    def test_6012_VC_130491_custom_team_edit_remove_teammates(self):
        self.tc_methods.tc_custom_team_edit_remove_teammates(team_name="teammate-count", count=6)

    def test_6013_VC_128161_custom_team_edit_delete_team(self):
        self.tc_methods.tc_custom_team_edit_delete_team(team_name="eng-team")

    def test_6014_VC_128162_custom_team_profile_remove_from_teammates(self):
        self.tc_methods.tc_custom_team_profile_remove_from_teammates(team_name1="custom1", team_name2="custom2")

    def test_6015_VC_128163_custom_team_manage_teams_add(self):
        self.tc_methods.tc_custom_team_manage_teams_add(team_name1="custom1", team_name2="custom2")

    def test_6016_VC_128164_custom_team_manage_teams_remove(self):
        self.tc_methods.tc_custom_team_manage_teams_remove(team_name="Logitech IT")

    def test_6017_VC_128165_custom_team_manage_teams_new_team(self):
        self.tc_methods.tc_custom_team_manage_teams_new_team(team_name="Mobile QA", new_team="Mobile Dev")


if __name__ == "__main__":
    unittest.main()
