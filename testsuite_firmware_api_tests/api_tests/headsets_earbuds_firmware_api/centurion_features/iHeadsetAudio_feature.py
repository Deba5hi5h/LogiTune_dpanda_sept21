from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_ANC_CUSTOMIZATION_MODE,
    CMD_GET_ANC_STATUS,
    CMD_GET_MIC_MUTE_STATUS,
    CMD_GET_SIDETONE_LEVEL,
    CMD_SET_ANC,
    CMD_SET_ANC_CUSTOMIZATION_MODE,
    CMD_SET_MIC_MUTE_STATUS,
    CMD_SET_SIDETONE_LEVEL,
)


class HeadsetAudioFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0500_iHeadsetAudio.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_mic_mute(self, status):
        mic_mute_status = [
            CMD_SET_MIC_MUTE_STATUS[0],
            CMD_SET_MIC_MUTE_STATUS[1],
            CMD_SET_MIC_MUTE_STATUS[2],
            CMD_SET_MIC_MUTE_STATUS[3],
            CMD_SET_MIC_MUTE_STATUS[4],
            CMD_SET_MIC_MUTE_STATUS[5],
            status,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=mic_mute_status,
            command_name=f"Set Mic Mute status to {status}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Mic Mute status'")
        return response

    def get_mic_mute_status(self):
        return self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=CMD_GET_MIC_MUTE_STATUS,
            command_name="Get Mic Mute Status...",
        )

    def verify_not_supported_mic_mute_value(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail(
                "Error response for Not supported Mica value not found",
                screenshot=False,
            )

    def verify_get_mic_mute_status(self, response, status):
        payload_len = f"{3 + 1:02x}"
        mic_mute_status = f"{status:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == mic_mute_status, Report.logFail(
                f"Mic Mute status value {str(response[last_index + 1])} is not equal {mic_mute_status}"
            )
            Report.logPass("mic mute status value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_anc_state(self):
        return self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=CMD_GET_ANC_STATUS,
            command_name="Get ANC State...",
        )

    def get_current_anc_state(self):
        response = self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=CMD_GET_ANC_STATUS,
            command_name="Get Current ANC State...",
        )
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "04",
            "00",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "4d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            return response[last_index + 1]
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_anc_state(self, state):
        set_anc_state_cmd = [
            CMD_SET_ANC[0],
            CMD_SET_ANC[1],
            CMD_SET_ANC[2],
            CMD_SET_ANC[3],
            CMD_SET_ANC[4],
            CMD_SET_ANC[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=set_anc_state_cmd,
            command_name=f"Set ANC to {state}...",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for set 'Set ANC state'")
        return response

    def verify_get_anc_state(self, response, state):
        payload_len = f"{4:02x}"
        state_hex = f"{state:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "4d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            # if self.centurion.conn_type == ConnectionType.bt:
            #     self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == state_hex, Report.logFail(
                f"ANC state {response[last_index + 1]} is not equal to {state_hex}"
            )
            Report.logPass("ANC state value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_anc_state(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "5d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error response received.")

        else:
            assert False, Report.logFail("Error response for not supported ANC state not found", screenshot=False)

    def set_sidetone_level(self, sidetone_level):
        set_sidetone_level_cmd = [
            CMD_SET_SIDETONE_LEVEL[0],
            CMD_SET_SIDETONE_LEVEL[1],
            CMD_SET_SIDETONE_LEVEL[2],
            CMD_SET_SIDETONE_LEVEL[3],
            CMD_SET_SIDETONE_LEVEL[4],
            CMD_SET_SIDETONE_LEVEL[5],
            sidetone_level,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=set_sidetone_level_cmd,
            command_name=f"Set Sidetone Level... to {sidetone_level}",
        )
        return response

    def verify_error_on_set_sidetone_level(self, response):
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if self.centurion.device_name in [
            DeviceName.zone_true_wireless,
            DeviceName.zone_wired,
            DeviceName.zone_750,
            DeviceName.zone_wired_earbuds,
            DeviceName.bomberman_mono,
            DeviceName.bomberman_stereo
        ]:
            code = "02"
        else:
            code = "05"

        if last_index:
            assert response[last_index + 1] == code, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {code}"
            )
            Report.logPass("Correct error response received.")
        else:
            assert False, Report.logFail(
                "Error message for not supported sidetone level not found",
                screenshot=False,
            )

    def get_sidetone_level(self):
        return self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=CMD_GET_SIDETONE_LEVEL,
            command_name="Get Sidetone Level...",
        )

    def verify_get_sidetone_level(self, response, level):
        sublist = [
            "00",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "2d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == f"{level:02x}", Report.logFail(
                f"Sidetone level {response[last_index + 1]} is not equal to {level:02x}"
            )
            Report.logPass("Sidetone level value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_anc_customization_mode(self, mode):
        set_anc_customization_mode_cmd = [
            CMD_SET_ANC_CUSTOMIZATION_MODE[0],
            CMD_SET_ANC_CUSTOMIZATION_MODE[1],
            CMD_SET_ANC_CUSTOMIZATION_MODE[2],
            CMD_SET_ANC_CUSTOMIZATION_MODE[3],
            CMD_SET_ANC_CUSTOMIZATION_MODE[4],
            CMD_SET_ANC_CUSTOMIZATION_MODE[5],
            mode,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=set_anc_customization_mode_cmd,
            command_name=f"Set ANC Customization Mode... to {mode}",
        )
        return response

    def get_anc_customization_mode(self):
        return self.centurion.send_command(
            feature_name="iHeadsetAudio",
            command=CMD_GET_ANC_CUSTOMIZATION_MODE,
            command_name="Get ANC Customization Mode...",
        )

    def verify_get_anc_customization_mode(self, response, mode):
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "bd",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == f"{mode:02x}", Report.logFail(
                f"ANC Customization Mode {response[last_index + 1]} is not equal to {mode:02x}"
            )
            Report.logPass("ANC Customization Mode value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_set_wrong_anc_customization_mode(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetAudio'][4]:02x}",
            "cd",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail("Error response for not found", screenshot=False)
