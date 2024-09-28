from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_BT_STATE,
    CMD_SET_DISCOVERABLE_STATE,
)


class BluetoothCrtlFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0303_iBluetoothCtrl.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_bt_state(self):
        command_to_send = [
            CMD_GET_BT_STATE[0],
            CMD_GET_BT_STATE[1],
            CMD_GET_BT_STATE[2],
            CMD_GET_BT_STATE[3],
            CMD_GET_BT_STATE[4],
            CMD_GET_BT_STATE[5],
        ]
        return self.centurion.send_command(
            feature_name="iBluetoothCtrl",
            command=command_to_send,
            command_name="Get BT State...",
        )

    def verify_get_bt_state(self, response, state):
        payload_len = f"{4:02x}"
        notification_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "04",
            "00",
            f"{self.centurion.device_features['iBluetoothCtrl'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == notification_state, Report.logFail(
                f"Get BT State {response[last_index + 1]} is not equal to {notification_state}"
            )
            Report.logPass("BT state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_discoverable_state(self):
        command_to_send = [
            CMD_SET_DISCOVERABLE_STATE[0],
            CMD_SET_DISCOVERABLE_STATE[1],
            CMD_SET_DISCOVERABLE_STATE[2],
            CMD_SET_DISCOVERABLE_STATE[3],
            CMD_SET_DISCOVERABLE_STATE[4],
            CMD_SET_DISCOVERABLE_STATE[5],
        ]
        response = self.centurion.send_command(
            feature_name="iBluetoothCtrl",
            command=command_to_send,
            command_name="Set discoverable State...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Discoverable state'")
        assert "ff" not in response, Report.logFail("Response should not consist of errors")
        return response
