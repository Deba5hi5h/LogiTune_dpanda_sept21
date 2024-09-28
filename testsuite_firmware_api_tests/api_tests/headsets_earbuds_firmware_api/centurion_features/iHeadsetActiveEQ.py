from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_HEADSET_ACTIVE_EQ, CMD_GET_HEADSET_ACTIVE_EQ,
)


class HeadsetActiveEQFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0514_iHeadsetActiveEQ.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_headset_active_eq(self, state, key, value):
        set_headset_active_eq = [
            CMD_SET_HEADSET_ACTIVE_EQ[0],
            CMD_SET_HEADSET_ACTIVE_EQ[1],
            CMD_SET_HEADSET_ACTIVE_EQ[2],
            CMD_SET_HEADSET_ACTIVE_EQ[3],
            CMD_SET_HEADSET_ACTIVE_EQ[4],
            CMD_SET_HEADSET_ACTIVE_EQ[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetActiveEQ",
            command=set_headset_active_eq,
            command_name=f"Set HeadsetActive Eq to: {state}",
        )

        assert len(response) > 0, Report.logFail(
            "Empty response_raw returned for 'Set Headset Active Eq'")

        sublist_to_check = []
        if state == 0:
            Report.logInfo(f"Verify that Eq profile {key} and values: {value} returned.")
            sublist_to_check.append(key)
            sublist_to_check = sublist_to_check + value
            sublist = []
            for b in sublist_to_check:
                hex_value = f"{b:02x}"
                sublist.append(hex_value)
            x, y = self.centurion.find_sub_list(sublist, response)
            assert x is not None and y is not None, Report.logFail("Wrong Eq profile returned.")
        elif state == 1:
            Report.logInfo(f"Verify that flat peq returned.")
            sublist_to_check = [0] * 21
            sublist = []
            for b in sublist_to_check:
                hex_value = f"{b:02x}"
                sublist.append(hex_value)
            x, y = self.centurion.find_sub_list(sublist, response)
            assert x is not None and y is not None, Report.logFail("Wrong peq profile returned.")

        return response

    def get_headset_active_eq(self):
        return self.centurion.send_command(
            feature_name="iHeadsetActiveEQ",
            command=CMD_GET_HEADSET_ACTIVE_EQ,
            command_name="Get Headset Active Eq...",
        )

    def verify_get_headset_active_eq(self, response, state):
        payload_len = f"{3 + 1:02x}"
        headset_active_eq = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetActiveEQ'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(
            sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index,
                                                   response_len)

            assert response[
                last_index + 1] == headset_active_eq, Report.logFail(
                    f"Headset Active Eq state value {str(response[last_index + 1])} is not equal {headset_active_eq}"
                )
            Report.logPass("Headset Active Eq value is correct")
        else:
            assert False, Report.logFail("Response pattern not found",
                                         screenshot=False)

    def verify_not_supported_headset_active_eq(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetActiveEQ'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(
            sublist, response)

        if last_index:
            assert response[
                last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                    f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
                )
            Report.logPass("Returned error code is correct")
        else:
            assert False, Report.logFail(
                "Error message for not supported Headset Active Eq value received",
                screenshot=False,
            )
