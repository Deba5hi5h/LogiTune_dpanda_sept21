device = {
    "Rally Bar": {
                    "ip_address": "172.28.213.230",
                    "user_name": "admin",
                    "password": "Logi@3456",
                    "power": "RaidenRallyBar"
                  },

}


class RaidenConfig():
    @staticmethod
    def get_ip_address(device_name: str) -> str:
        """
        Method to get IP address of the device in test
        :param device_name:
        :return str:
        """
        return device.get(device_name).get("ip_address")

    @staticmethod
    def get_user_name(device_name: str) -> str:
        """
        Method to get LNA Username of the device in test
        :param device_name:
        :return str:
        """
        return device.get(device_name).get("user_name")

    @staticmethod
    def get_password(device_name: str) -> str:
        """
        Method to get LNA Password of the device in test
        :param device_name:
        :return str:
        """
        return device.get(device_name).get("password")
    @staticmethod
    def get_power_port(device_name: str) -> str:
        """
        Method to get Power port name of the device in test
        :param device_name:
        :return str:
        """
        return device.get(device_name).get("power")