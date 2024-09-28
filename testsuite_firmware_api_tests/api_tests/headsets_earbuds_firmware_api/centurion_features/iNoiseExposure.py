from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_NOISE_EXPOSURE,
    CMD_GET_NOISE_EXPOSURE,
)


class NoiseExposure:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x060D_iNoiseExposure.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_noise_exposure_state(self, state):
        set_noise_exposure_state = [
            CMD_SET_NOISE_EXPOSURE[0],
            CMD_SET_NOISE_EXPOSURE[1],
            CMD_SET_NOISE_EXPOSURE[2],
            CMD_SET_NOISE_EXPOSURE[3],
            CMD_SET_NOISE_EXPOSURE[4],
            CMD_SET_NOISE_EXPOSURE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iNoiseExposure",
            command=set_noise_exposure_state,
            command_name=f"Set Noise Exposure state to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Noise Exposure'")
        return response

    def get_noise_exposure_state(self):
        return self.centurion.send_command(
            feature_name="iNoiseExposure",
            command=CMD_GET_NOISE_EXPOSURE,
            command_name="Get Noise Exposure state...",
        )

    def verify_get_noise_exposure_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        noise_exposure_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iNoiseExposure'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == noise_exposure_state, Report.logFail(
                f"Noise Exposure state value {str(response[last_index + 1])} is not equal {noise_exposure_state}"
            )
            Report.logPass("Noise Exposure state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_noise_exposure_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iNoiseExposure'][4]:02x}",
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
                "Error message for not supported Noise Exposure value received",
                screenshot=False,
            )
