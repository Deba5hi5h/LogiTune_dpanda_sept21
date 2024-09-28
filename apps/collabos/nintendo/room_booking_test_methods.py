from apps.collabos.nintendo.nintendo_methods import NintendoMethods


class RoomBookingTests:

    def __init__(self, nintendo_methods: NintendoMethods):
        self.nintendo_methods: NintendoMethods = nintendo_methods
        self.appium_service = self.nintendo_methods.appium_service


    def verify_room_booking_time(self):
        x = self.nintendo_methods.get_time_from_main_page()
        print(x)