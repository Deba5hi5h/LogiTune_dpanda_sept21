from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_EARCON_STATE,
    CMD_GET_LANGUAGE,
    CMD_GET_LANGUAGE_CAPABILITIES,
    CMD_SET_EARCON_STATE,
    CMD_SET_LANGUAGE,
)


class EarconFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0109_iEarcon.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_language(self):
        return self.centurion.send_command(
            feature_name="iEarcon",
            command=CMD_GET_LANGUAGE,
            command_name="Get Language...",
        )

    def set_language(self, language):
        set_language_cmd = [
            CMD_SET_LANGUAGE[0],
            CMD_SET_LANGUAGE[1],
            CMD_SET_LANGUAGE[2],
            CMD_SET_LANGUAGE[3],
            CMD_SET_LANGUAGE[4],
            CMD_SET_LANGUAGE[5],
            language,
        ]
        response = self.centurion.send_command(set_language_cmd, f"Set Language... to {language}")

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Language'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set Language'")
        return response

    def set_not_supported_language(self, language):
        set_language_cmd = [
            CMD_SET_LANGUAGE[0],
            CMD_SET_LANGUAGE[1],
            CMD_SET_LANGUAGE[2],
            CMD_SET_LANGUAGE[3],
            CMD_SET_LANGUAGE[4],
            CMD_SET_LANGUAGE[5],
            language,
        ]
        return self.centurion.send_command(
            feature_name="iEarcon",
            command=set_language_cmd,
            command_name=f"Set Language... to {language}",
        )

    def verify_set_not_supported_language(self, response):
        if self.centurion.device_name == DeviceName.zone_true_wireless:
            error_code = "0a"
        else:
            error_code = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iEarcon'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == error_code, Report.logFail(
                f"Returned error code {response[last_index + 1]} for not available language is not equal to {error_code}"
            )
            Report.logPass("Returned error code value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_get_language(self, response, language):
        payload_len = f"{3 + 1:02x}"
        lang = f"{language:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEarcon'][4]:02x}",
            "1d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == lang, Report.logFail(
                f"Language value {str(response[last_index + 1])} is not equal {lang}"
            )
            Report.logPass("Language value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_earcon_state(self, state):
        set_earcon_state = [
            CMD_SET_EARCON_STATE[0],
            CMD_SET_EARCON_STATE[1],
            CMD_SET_EARCON_STATE[2],
            CMD_SET_EARCON_STATE[3],
            CMD_SET_EARCON_STATE[4],
            CMD_SET_EARCON_STATE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iEarcon",
            command=set_earcon_state,
            command_name=f"Set Earcon state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Earcon State'")
        return response

    def get_earcon_state(self):
        return self.centurion.send_command(
            feature_name="iEarcon",
            command=CMD_GET_EARCON_STATE,
            command_name="Get Earcon state...",
        )

    def verify_get_earcon_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        earcon_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEarcon'][4]:02x}",
            "3d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == earcon_state, Report.logFail(
                f"Earcon state value {str(response[last_index + 1])} is not equal {earcon_state}"
            )
            Report.logPass("Earcon state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_earcon_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iEarcon'][4]:02x}",
            "2d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Returned error code is correct")
        else:
            assert False, Report.logFail(
                "Error message for not supported earcon value received",
                screenshot=False,
            )

    def get_language_capability(self):
        return self.centurion.send_command(
            feature_name="iEarcon",
            command=CMD_GET_LANGUAGE_CAPABILITIES,
            command_name="Get Language Capabilities...",
        )

    def verify_get_language_capability(self, response, device_name=None):
        payload_len = f"{3 + 4:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEarcon'][4]:02x}",
            "4d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            lang_cap_response = []
            for i in range(last_index + 1, last_index + 1 + 4):
                lang_cap_response.append(response[i])

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                lang = "05"
            else:
                lang = "01"

            assert (
                lang_cap_response[3] == lang
            ), f"Language Capability value {str(lang_cap_response[3])} has a wrong value. Only Eng is supported right now."
            Report.logPass("Language Capability value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
