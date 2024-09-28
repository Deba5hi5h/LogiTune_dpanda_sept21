from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_AI_NOISE_REDUCTION,
    CMD_GET_AI_NOISE_REDUCTION,
)


class AINoiseReduction:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x060E_iAINoiseReduction.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_ai_noise_reduction_state(self, state):
        set_ai_noise_reduction_state = [
            CMD_SET_AI_NOISE_REDUCTION[0],
            CMD_SET_AI_NOISE_REDUCTION[1],
            CMD_SET_AI_NOISE_REDUCTION[2],
            CMD_SET_AI_NOISE_REDUCTION[3],
            CMD_SET_AI_NOISE_REDUCTION[4],
            CMD_SET_AI_NOISE_REDUCTION[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iAINoiseReduction",
            command=set_ai_noise_reduction_state,
            command_name=f"Set AI Noise reduction state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set AI Noise reduction'")
        return response

    def get_ai_noise_reduction_state(self):
        return self.centurion.send_command(
            feature_name="iAINoiseReduction",
            command=CMD_GET_AI_NOISE_REDUCTION,
            command_name="Get AI Noise Reduction state...",
        )

    def verify_get_ai_noise_reduction_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        ai_noise_reduction_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iAINoiseReduction'][4]:02x}",
            "2d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == ai_noise_reduction_state, Report.logFail(
                f"AI Noise reduction state value {str(response[last_index + 1])}  is not equal {ai_noise_reduction_state}"
            )
            Report.logPass("AI Noise reduction state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_ai_noise_reduction_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iAINoiseReduction'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code  {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Returned error code is correct")
        else:
            assert False, Report.logFail(
                "Error message for not supported ai noise reduction value received",
                screenshot=False,
            )
