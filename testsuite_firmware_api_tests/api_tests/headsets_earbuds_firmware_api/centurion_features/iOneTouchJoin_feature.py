from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import *


class OneTouchJoinFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x010F_iOneTouchJoin.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_led_state(self):
        return self.centurion.send_command(
            feature_name="iOneTouchJoin",
            command=CMD_GET_LED_STATE,
            command_name=f"Get LED state",
        )

    def verify_get_led_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        led_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iOneTouchJoin'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert (
                response[last_index + 1] == led_state
            ), f"LED state value {str(response[last_index + 1])} is not equal {led_state}"
            Report.logPass("LED state status value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_led_state(self, state):
        set_earcon_state = [
            CMD_SET_LED_STATE[0],
            CMD_SET_LED_STATE[1],
            CMD_SET_LED_STATE[2],
            CMD_SET_LED_STATE[3],
            CMD_SET_LED_STATE[4],
            CMD_SET_LED_STATE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iOneTouchJoin",
            command=set_earcon_state,
            command_name=f"Set LED state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set LED State'")
        return response
