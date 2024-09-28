import unittest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data


class SchedulerPeople(MobileBase):
    tc_methods = TuneMobileTests()
    teammate_added = False

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Dashboard People"
        super(SchedulerPeople, cls).setUpClass()
        if global_variables.reportInstance is None:
            global_variables.reportInstance = global_variables.extent.createTest("People Setup", "Test Case Details")
        cls.tc_methods.close()
        cls.tc_methods.open_app()
        if not cls.tc_methods.dashboard.verify_home():
            cls.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.user_email(), verification=False,
                                                  site_name=TuneMobileConfig.site(),
                                                  building_name=TuneMobileConfig.building(),
                                                  teammates=test_data.tc_signin_teammates)

    def test_3001_VC_90724_people_teammates(self):
        self.tc_methods.tc_people_teammates()

    def test_3002_VC_104625_people_remove_teammate(self):
        self.tc_methods.tc_people_remove_teammate()

    def test_3003_VC_90720_people_screen(self):
        self.tc_methods.tc_people_screen()

    def test_3004_VC_90721_people_everyone(self):
        self.tc_methods.tc_people_everyone()

    def test_3005_VC_90722_people_everyone_add_teammate(self):
        self.tc_methods.tc_people_everyone_add_teammate()

    def test_3006_VC_104626_people_everyone_remove_teammate(self):
        self.tc_methods.tc_people_everyone_remove_teammate()

    def test_3007_VC_104609_people_teammate_view_search_by_first_name(self):
        self.tc_methods.tc_people_teammates_search(name=True, email=False)

    def test_3008_VC_104611_people_teammate_view_search_by_email(self):
        self.tc_methods.tc_people_teammates_search(name=False, email=True)

    def test_3009_VC_109161_people_teammate_view_search_by_last_name(self):
        temp = test_data.tc_people_teammates_search
        test_data.tc_people_teammates_search = ['xavier', 'Handi']
        self.tc_methods.tc_people_teammates_search(name=True, email=False)
        test_data.tc_people_teammates_search = temp

    def test_3010_VC_104618_people_everyone_view_search_by_first_name(self):
        self.tc_methods.tc_people_everyone_search(name=True, email=False)

    def test_3011_VC_104620_people_everyone_view_search_by_email(self):
        self.tc_methods.tc_people_everyone_search(name=False, email=True)

    def test_3012_VC_104619_people_everyone_view_search_by_last_name(self):
        temp = test_data.tc_people_teammates_search
        test_data.tc_people_teammates_search = ['xavier']
        self.tc_methods.tc_people_everyone_search(name=True, email=False)
        test_data.tc_people_teammates_search = temp

    def test_3013_VC_123227_people_everyone_view_person_profile(self):
        self.tc_methods.tc_people_everyone_person_profile(email=TuneMobileConfig.teammate_email())

    def test_3014_VC_123228_people_everyone_add_to_teammates_profile(self):
        self.tc_methods.tc_people_everyone_add_to_teammates_profile(user_name="gTeammate2 Gt2")

    def test_3015_VC_123229_people_teammate_remove_from_teammates_profile(self):
        self.tc_methods.tc_people_teammate_remove_from_teammates_profile(user_name="gTeammate2 Gt2")

    def test_3016_VC_104606_people_teammate_with_no_bookings(self):
        self.tc_methods.tc_people_teammate_with_no_bookings()

    def test_3017_VC_104630_people_in_office_no_bookings(self):
        self.tc_methods.tc_people_in_office_no_bookings()

    def test_3018_VC_104631_people_in_office_teammate_booked_current_date(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_people_in_office_teammate_booked(desk_name=TuneMobileConfig.user_desk(), start=start,
                                                            end=end, day=0,
                                                            teammate=True)

    def test_3019_VC_104632_people_in_office_teammate_booked_future_date(self):
        start, end = "8:00 AM", "10:00 AM"
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_people_in_office_teammate_booked(desk_name=TuneMobileConfig.user_desk(),
                                                            start=start, end=end, day=1, teammate=True)

    def test_3020_VC_104633_people_in_office_others_booked_current_date(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_people_in_office_teammate_booked(desk_name=TuneMobileConfig.user_desk(),
                                                            start=start, end=end, day=0, teammate=False)
        #Also covers VC-100976

    def test_3021_VC_104634_people_in_office_others_booked_future_date(self):
        start, end = "8:00 AM", "10:00 AM"
        self.tc_methods.tc_people_in_office_teammate_booked(desk_name=TuneMobileConfig.user_desk(),
                                                            start=start, end=end, day=1, teammate=False)
        #Also covers VC-100976

    def test_3022_VC_112717_teammates_nearby_teammate_booked_current_date(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_teammates_nearby_teammate_booked(user_desk=TuneMobileConfig.user_desk(),
                                                            teammate_desk=TuneMobileConfig.nearest_desk(),
                                                            other_desk=TuneMobileConfig.second_nearest_desk(),
                                                            start=start, end=end, day=0)

    def test_3023_VC_112718_teammates_nearby_teammate_booked_future_date(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_teammates_nearby_teammate_booked(user_desk=TuneMobileConfig.user_desk(),
                                                            teammate_desk=TuneMobileConfig.nearest_desk(),
                                                            other_desk=TuneMobileConfig.second_nearest_desk(),
                                                            start=start, end=end, day=1)

    def test_3024_VC_112719_teammates_nearby_teammate_booked_different_floor(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_teammates_nearby_teammate_booked(user_desk=TuneMobileConfig.user_desk(),
                                                            teammate_desk=TuneMobileConfig.different_floor_desk1(),
                                                            other_desk=TuneMobileConfig.different_floor_desk2(),
                                                            start=start, end=end, day=0, nearby=False)

    def test_3025_VC_112720_teammates_nearby_teammate_booked_different_area(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        if not SchedulerPeople.teammate_added:
            teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            SchedulerPeople.teammate_added = self.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])
        self.tc_methods.tc_teammates_nearby_teammate_booked(user_desk=TuneMobileConfig.user_desk(),
                                                            teammate_desk=TuneMobileConfig.different_area_desk1(),
                                                            other_desk=TuneMobileConfig.different_area_desk2(),
                                                            start=start, end=end, day=0, nearby=False)


if __name__ == "__main__":
    unittest.main()
