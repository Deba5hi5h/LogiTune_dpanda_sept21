from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_ENABLE_EVENT,
    CMD_GET_HDMI_MODE,
    CMD_GET_PORT_INFO,
    CMD_GET_PORT_STATUS,
    CMD_SET_HDMI_MODE,
    CMD_SET_PORT_POWER,
)


class USBHubControlFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x010C_iUSBHubControl.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_hdmi_state(self, state):
        set_hdmi_cmd = [
            CMD_SET_HDMI_MODE[0],
            CMD_SET_HDMI_MODE[1],
            CMD_SET_HDMI_MODE[2],
            CMD_SET_HDMI_MODE[3],
            CMD_SET_HDMI_MODE[4],
            CMD_SET_HDMI_MODE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=set_hdmi_cmd,
            command_name=f"Set HDMI state to {state}...",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Language'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set HDMI state'")
        return response

    def get_hdmi_state(self):
        return self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=CMD_GET_HDMI_MODE,
            command_name="Get HDMI State...",
        )

    def verify_get_hdmi_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        hdmi_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iUSBHubControl'][4]:02x}",
            "1d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == hdmi_state, Report.logFail(
                f"HDMI state value {str(response[last_index + 1])} is not equal {hdmi_state}"
            )
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_port_info(self):
        return self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=CMD_GET_PORT_INFO,
            command_name="Get Port Info...",
        )

    def verify_get_port_info(self, response):
        payload_len = f"{3 + 8:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iUSBHubControl'][4]:02x}",
            "2d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            present = ["1", "1", "1", "1", "1", "1", "0", "0"]
            present_hex = f"{int(''.join(present), 2):02x}"
            power_control = ["0", "0", "0", "0", "0", "1", "0", "0"]
            power_control_hex = f"{int(''.join(power_control), 2):02x}"
            assert response[last_index + 1] == present_hex, Report.logFail(
                f"Present bytes {str(response[last_index + 1])} are not equal {present_hex}"
            )
            Report.logPass("Present bytes value is correct")
            assert response[last_index + 5] == power_control_hex, Report.logFail(
                f"Power Control bytes {str(response[last_index + 5])} are not equal {power_control_hex}"
            )
            Report.logPass("Power Control bytes value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_port_status(self):
        return self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=CMD_GET_PORT_STATUS,
            command_name="Get Port Status...",
        )

    def verify_get_port_status(self):
        assert 1 == 0

    def set_enable_event(self, state):
        set_hdmi_cmd = [
            CMD_ENABLE_EVENT[0],
            CMD_ENABLE_EVENT[1],
            CMD_ENABLE_EVENT[2],
            CMD_ENABLE_EVENT[3],
            CMD_ENABLE_EVENT[4],
            CMD_ENABLE_EVENT[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=set_hdmi_cmd,
            command_name=f"Set Enable Event to {state}...",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Enable Event'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set Enable Event'")
        return response

    def set_port_power(self):
        power_control = ["0", "0", "0", "0", "0", "1", "0", "0"]
        power_control_b = int("".join(power_control), 2)
        set_hdmi_cmd = [
            CMD_SET_PORT_POWER[0],
            CMD_SET_PORT_POWER[1],
            CMD_SET_PORT_POWER[2],
            CMD_SET_PORT_POWER[3],
            CMD_SET_PORT_POWER[4],
            CMD_SET_PORT_POWER[5],
            power_control_b,
            CMD_SET_PORT_POWER[7],
            CMD_SET_PORT_POWER[8],
            CMD_SET_PORT_POWER[9],
        ]
        response = self.centurion.send_command(
            feature_name="iUSBHubControl",
            command=set_hdmi_cmd,
            command_name=f"Set Power Port to {power_control_b}...",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Power Port'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set Power Port'")
        return response
