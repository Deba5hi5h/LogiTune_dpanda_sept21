from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_STATUS_THERMAL,
)


class ThermalSensorsFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x010B_iThermalSensors.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_status_thermal_sensors(self):
        return self.centurion.send_command(
            feature_name="iThermalSensors",
            command=CMD_GET_STATUS_THERMAL,
            command_name="Get Status Thermal Sensors...",
        )

    def verify_get_status_thermal_sensors(self, response):
        payload_len = f"{2 + 2:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iThermalSensors'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert 1 == 0, "Needs to be clarified what to check"

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
