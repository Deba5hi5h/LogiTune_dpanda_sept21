from apps.collabos.collabos_base import CollabOsBase, EventFiringWebDriver



class NintendoConnect(CollabOsBase):

    def connect_to_room_booking_app(self, port, device_sn, device_ip) -> EventFiringWebDriver:
        """
        Method to open Room Booking application

        :param :
        :return :
        """
        return self.connect_to_collabos_app(port=port, device_sn=device_sn, device_ip=device_ip)
