from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_ANTI_STARTLE,
    CMD_GET_ANTI_STARTLE,
)


class AntiStartle:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x060C_iAntiStartle.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_anti_startle(self, state):
        set_anti_startle = [
            CMD_SET_ANTI_STARTLE[0],
            CMD_SET_ANTI_STARTLE[1],
            CMD_SET_ANTI_STARTLE[2],
            CMD_SET_ANTI_STARTLE[3],
            CMD_SET_ANTI_STARTLE[4],
            CMD_SET_ANTI_STARTLE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iAntiStartle",
            command=set_anti_startle,
            command_name=f"Set Anti Startle state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Anti Startle'")
        return response

    def get_anti_startle(self):
        return self.centurion.send_command(
            feature_name="iAntiStartle",
            command=CMD_GET_ANTI_STARTLE,
            command_name="Get Anti Startle state...",
        )

    def verify_get_anti_startle(self, response, state):
        payload_len = f"{3 + 1:02x}"
        anti_startle = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iAntiStartle'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == anti_startle, Report.logFail(
                f"Anti Startle state value {str(response[last_index + 1])} is not equal {anti_startle}"
            )
            Report.logPass("Anti Startle state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_anti_startle_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iAntiStartle'][4]:02x}",
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
                "Error message for not supported Anti Startle value received",
                screenshot=False,
            )
