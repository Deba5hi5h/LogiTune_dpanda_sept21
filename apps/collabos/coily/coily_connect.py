
from apps.collabos.collabos_base import CollabOsBase


class CoilyConnect(CollabOsBase):

    def connect_to_scheduler_app(self, port, device_sn, device_ip):
        """
        Method to open Room Booking application

        :param :
        :return :
        """
        return self.connect_to_collabos_app(port=port, device_sn=device_sn, device_ip=device_ip)
