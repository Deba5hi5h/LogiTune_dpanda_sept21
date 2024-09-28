from base.jasmine_base import JasmineBase
import unittest


class JasmineBookings(JasmineBase):
    def test_2001_VC_135264_ad_hoc_booking_1_hour(self):
        self.jasmine_tc_methods.tc_ad_hoc_booking_1_hour()

    def test_2002_VC_135265_extend_booking_15_minutes(self):
        self.jasmine_tc_methods.tc_extend_room_booking_15_minutes()

    def test_2003_VC_135266_release_room_booking(self):
        self.jasmine_tc_methods.tc_release_room()


if __name__ == "__main__":
    unittest.main()
