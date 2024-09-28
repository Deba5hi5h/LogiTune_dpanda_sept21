from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_BAND_INFO,
    CMD_GET_EQ,
    CMD_GET_EQ_MODES,
    CMD_SET_EQ,
)


class EQSetFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0201_iEQSet.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_eq_mode(self):
        return self.centurion.send_command(
            feature_name="iEQSet",
            command=CMD_GET_EQ,
            command_name="Get EQ Parameters...",
        )

    def verify_get_eq_mode(self, response, mode, bands):
        payload_len = f"{3 + 6:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEQSet'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == f"{mode:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} is not equal to {mode:02x}"
            )
            assert response[last_index + 2] == f"{bands[0]:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} Gain[0] value {str(response[last_index + 2])} is not equal to {bands[0]:02x}"
            )
            assert response[last_index + 3] == f"{bands[1]:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} Gain[1] value {str(response[last_index + 3])} is not equal to {bands[1]:02x}"
            )
            assert response[last_index + 4] == f"{bands[2]:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} Gain[2] value {str(response[last_index + 4])} is not equal to {bands[2]:02x}"
            )
            assert response[last_index + 5] == f"{bands[3]:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} Gain[3] value {str(response[last_index + 5])} is not equal to {bands[3]:02x}"
            )
            assert response[last_index + 6] == f"{bands[4]:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} Gain[4] value {str(response[last_index + 6])} is not equal to {bands[4]:02x}"
            )
            Report.logPass("Gain values are correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_eq_profile(self, response, mode):
        payload_len = f"{3 + 6:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iEQSet'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == f"{mode:02x}", Report.logFail(
                f"Mode value {str(response[last_index + 1])} is not equal to {mode:02x}"
            )
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_eq_modes(self):
        return self.centurion.send_command(
            feature_name="iEQSet",
            command=CMD_GET_EQ_MODES,
            command_name="Get EQ Modes...",
        )

    def verify_get_eq_modes(self, response, modes):
        payload_len = f"{3 + 5:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEQSet'][4]:02x}",
            "2d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert int(response[last_index + 1], 16) == len(modes.keys()), Report.logFail(
                f"Length of returned modes {int(response[last_index + 1], 16)} is not equal to supported modes {len(modes.keys())}"
            )
            for i in range(1, len(modes.keys()) + 1):
                assert int(response[last_index + 1 + i], 16) in modes.keys(), Report.logFail(
                    f"Mode {int(response[last_index + 1 + i], 16)} not in supported eq modes {modes.keys()}"
                )
            Report.logPass("EQ modes values are correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_eq_mode(self, mode, bands):
        set_eq_mode_cmd = [
            CMD_SET_EQ[0],
            CMD_SET_EQ[1],
            CMD_SET_EQ[2],
            CMD_SET_EQ[3],
            CMD_SET_EQ[4],
            CMD_SET_EQ[5],
            mode,
            bands[0],
            bands[1],
            bands[2],
            bands[3],
            bands[4],
        ]
        response = self.centurion.send_command(
            feature_name="iEQSet",
            command=set_eq_mode_cmd,
            command_name=f"Set EQ Mode to {mode}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for set 'Set EQ modes'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set EQ modes'")
        return response

    def get_band_info(self):
        return self.centurion.send_command(
            feature_name="iEQSet",
            command=CMD_GET_BAND_INFO,
            command_name="Get Band Info...",
        )

    def verify_get_band_info(self, response):
        payload_len = f"{14:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iEQSet'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "05", Report.logFail(
                f"Band Info count {response[last_index + 1]} is not equal to 05"
            )
            Report.logPass("Band info count value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
