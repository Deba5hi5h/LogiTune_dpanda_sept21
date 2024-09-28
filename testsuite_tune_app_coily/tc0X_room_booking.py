from base.base_nintendo import NintendoBase


class RoomBookingTestsX(NintendoBase):

    def test_3001_VC_112860_walk_in_session_enabled_user_not_logged_in(self):
        self.nintendo_test_methods.verify_room_booking_time()