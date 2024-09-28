from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_BATTERY_STATUS,
    CMD_GET_VOLTAGE_STATUS,
)


class BatterySOCFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0104_iBatterySOC.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_voltage_status(self):
        command_to_send = [
            CMD_GET_VOLTAGE_STATUS[0],
            CMD_GET_VOLTAGE_STATUS[1],
            CMD_GET_VOLTAGE_STATUS[2],
            CMD_GET_VOLTAGE_STATUS[3],
            CMD_GET_VOLTAGE_STATUS[4],
            CMD_GET_VOLTAGE_STATUS[5],
        ]
        return self.centurion.send_command(
            feature_name="iBatterySOC",
            command=command_to_send,
            command_name="Get Volatge Status...",
            long_response_expected=True,
        )  # possible fail

    def verify_get_voltage_status(self, response):
        payload_len = f"{3 + 8:02x}"
        sublist = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iBatterySOC'][4]:02x}",
            "1d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            voltage_response = []
            for i in range(last_index + 1, last_index + 8 + 1):
                voltage_response.append(response[i])

            batt_volt = int("".join(voltage_response[0:2]), 16)
            ntc_volt = int("".join(voltage_response[2:4]), 16)

            if self.centurion.device_name.startswith("Zone Vibe"):
                usb_volt = "".join(voltage_response[4:6])
                charge_current = "".join(voltage_response[6:8])

                assert 3300 <= batt_volt <= 4200, Report.logFail(f"BattVolt value {batt_volt} is out of range")
                Report.logPass("BattVolt value is correct")
                assert 572 <= ntc_volt <= 1304, Report.logFail(f"NTCVolt value {ntc_volt} is out of the range")
                Report.logPass("NTCVolt value is correct")
                assert usb_volt == "ffff", Report.logFail("USBVolt should return ffff as not supported")
                Report.logPass("USBVolt value is correct")
                assert charge_current == "ffff", Report.logFail("ChargeCurrent should return ffff as not supported")
                Report.logPass("ChargeCurrent value is correct")
            else:
                usb_volt = int("".join(voltage_response[4:6]))
                charge_current = int("".join(voltage_response[6:8]))

                assert 3300 <= batt_volt <= 4200, Report.logFail(f"BattVolt value {batt_volt} is out of range")
                Report.logPass("BattVolt value is correct")
                assert ntc_volt == 0, Report.logFail(f"NTCVolt value {ntc_volt} is out of range")
                Report.logPass("NTCVolt value is correct")
                assert 0 <= usb_volt <= 5000, Report.logFail(
                    f"USBVolt value {usb_volt} is out of range"
                )  # estimated value, no reqs
                Report.logPass("USBVolt value is correct")
                assert charge_current > 0, Report.logFail(
                    f"ChargeCurrent value {charge_current} is out of range"
                )  # estimated value, no reqs
                Report.logPass("ChargeCurrent value is correct")

    def get_battery_status(self):
        command_to_send = [
            CMD_GET_BATTERY_STATUS[0],
            CMD_GET_BATTERY_STATUS[1],
            CMD_GET_BATTERY_STATUS[2],
            CMD_GET_BATTERY_STATUS[3],
            CMD_GET_BATTERY_STATUS[4],
            CMD_GET_BATTERY_STATUS[5],
        ]
        response = self.centurion.send_command(
            feature_name="iBatterySOC",
            command=command_to_send,
            command_name="Get Battery Status...",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for set 'Set Sleep Timer'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set Sleep Timer'")

        return response

    def verify_get_battery_status(self, response):
        payload_len = f"{3 + 3:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iBatterySOC'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            battery_response = []
            for i in range(last_index + 1, last_index + 3 + 1):
                battery_response.append(response[i])

            real_soc = int(battery_response[0], 16)
            user_soc = int(battery_response[1], 16)
            assert real_soc <= 100, Report.logFail(f"Real SOC Battery value {real_soc} is out of range")
            Report.logPass("Real SOC Battery value is correct")
            assert user_soc <= 100, Report.logFail(f"User SOC Battery value {user_soc} is out of range")
            Report.logPass("User SOC Battery value is correct")
            assert battery_response[2] == "00" or response[2] == "03", Report.logFail(
                f"Charging state {battery_response[2]} is not equal for '00' or '03'"
            )
            Report.logPass("Charging state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
