from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_NOTIFICATION_STATE,
    CMD_GET_ROLE,
    CMD_SET_NOTIFICATION_STATE,
)


class TWBudsRoleSwitchingFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0614_iTWBudsRoleSwitching.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_role(self):
        return self.centurion.send_command(
            feature_name="iTWBudsRoleSwitching",
            command=CMD_GET_ROLE,
            command_name="Get Role...",
        )

    def verify_get_role(self, response):
        payload_len = f"{3 + 1:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iTWBudsRoleSwitching'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "01", Report.logFail(
                f"Role {str(response[last_index + 1])} is not equal to '01'"
            )
            Report.logPass("Role value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_notification_state(self, state):
        set_notification_cmd = [
            CMD_SET_NOTIFICATION_STATE[0],
            CMD_SET_NOTIFICATION_STATE[1],
            CMD_SET_NOTIFICATION_STATE[2],
            CMD_SET_NOTIFICATION_STATE[3],
            CMD_SET_NOTIFICATION_STATE[4],
            CMD_SET_NOTIFICATION_STATE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iTWBudsRoleSwitching",
            command=set_notification_cmd,
            command_name=f"Set Notification State... to {state}",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Notification Status'")
        return response

    def get_notification_state(self):
        return self.centurion.send_command(
            feature_name="iTWBudsRoleSwitching",
            command=CMD_GET_NOTIFICATION_STATE,
            command_name="Get Notification State...",
        )

    def verify_get_notification_state(self, response, state):
        payload_len = f"{4:02x}"
        notification_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iTWBudsRoleSwitching'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == notification_state, Report.logFail(
                f"Notification state {response[last_index + 1]} is not equal to {notification_state}"
            )
            Report.logPass("Notification state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_notification_status(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iTWBudsRoleSwitching'][4]:02x}",
            "2d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error code received.")
        else:
            assert False, Report.logFail(
                "Error message for not supported notification status not found",
                screenshot=False,
            )
