from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_AUTO_MUTE_ON_CALL,
    CMD_GET_AUTO_MUTE_ON_CALL,
)


class AutoMuteOnCall:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0610_iAutoMuteOnCall.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_auto_mute_on_call(self, state):
        set_auto_mute_on_call = [
            CMD_SET_AUTO_MUTE_ON_CALL[0],
            CMD_SET_AUTO_MUTE_ON_CALL[1],
            CMD_SET_AUTO_MUTE_ON_CALL[2],
            CMD_SET_AUTO_MUTE_ON_CALL[3],
            CMD_SET_AUTO_MUTE_ON_CALL[4],
            CMD_SET_AUTO_MUTE_ON_CALL[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iAutoMuteOnCall",
            command=set_auto_mute_on_call,
            command_name=f"Set Auto Mute On Call state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Auto Mute On Call'")
        return response

    def get_auto_mute_on_call(self):
        return self.centurion.send_command(
            feature_name="iAutoMuteOnCall",
            command=CMD_GET_AUTO_MUTE_ON_CALL,
            command_name="Get Auto Mute On Call state...",
        )

    def verify_get_auto_mute_on_call(self, response, state):
        payload_len = f"{3 + 1:02x}"
        auto_mute_on_call = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iAutoMuteOnCall'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == auto_mute_on_call, Report.logFail(
                f"Auto Mute On Call state value {str(response[last_index + 1])} is not equal {auto_mute_on_call}"
            )
            Report.logPass("Auto Mute On Call state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_auto_mute_on_call_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iAutoMuteOnCall'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Returned error code is correct")
        else:
            assert False, Report.logFail(
                "Error message for not supported Auto Mute On Call value received",
                screenshot=False,
            )
