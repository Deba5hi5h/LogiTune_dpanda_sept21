from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_EAR_DETECTION_STATE_CMD,
    CMD_SET_EAR_DETECTION_STATE_CMD,
)


class TWBudsInEarDetectionFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0613_iTWBudsInEarDetection.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_ear_detection_state(self, state):
        set_notification_cmd = [
            CMD_SET_EAR_DETECTION_STATE_CMD[0],
            CMD_SET_EAR_DETECTION_STATE_CMD[1],
            CMD_SET_EAR_DETECTION_STATE_CMD[2],
            CMD_SET_EAR_DETECTION_STATE_CMD[3],
            CMD_SET_EAR_DETECTION_STATE_CMD[4],
            CMD_SET_EAR_DETECTION_STATE_CMD[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iTWBudsInEarDetection",
            command=set_notification_cmd,
            command_name=f"Set Ear Detection State to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Ear Detection State'")
        return response

    def get_ear_detection_state(self):
        return self.centurion.send_command(
            feature_name="iTWBudsInEarDetection",
            command=CMD_GET_EAR_DETECTION_STATE_CMD,
            command_name="Get Ear Detection State...",
        )

    def verify_get_ear_detection_state(self, response, state):
        payload_len = f"{4:02x}"
        notification_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "04",
            "00",
            f"{self.centurion.device_features['iTWBudsInEarDetection'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert (
                response[last_index + 1] == notification_state
            ), f"Ear Detection State {response[last_index + 1]} is not equal to {notification_state}"
            Report.logPass("Ear detection State value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_set_ear_detection_state(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iTWBudsInEarDetection'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error code received.")
        else:
            assert False, Report.logFail(
                "Error message for not supported set ear detection state not found",
                screenshot=False,
            )
