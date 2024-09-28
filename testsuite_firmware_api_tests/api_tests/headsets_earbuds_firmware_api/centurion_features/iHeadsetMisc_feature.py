from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_FACTORY_RESET_DEVICE,
    CMD_GET_BUTTON_GEN_SETTINGS,
    CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY,
    CMD_GET_DO_NOT_DISTRUB_MODE_CMD,
    CMD_GET_MIC_BOOM_CMD,
    CMD_GET_VOICE_NOTIF_STATUS,
    CMD_RESET_BUTTON_CUSTOMIZATION_SETTINGS,
    CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY,
    CMD_SET_DO_NOT_DISTRUB_MODE_CMD,
    CMD_SET_MIC_BOOM_CMD,
    CMD_SET_VOICE_NOTIF_STATUS,
)


class HeadsetMicsFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0502_iHeadsetMisc.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_do_not_disturb_mode(self):
        return self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_GET_DO_NOT_DISTRUB_MODE_CMD,
            command_name="Get Do Not Disturb Mode...",
        )

    def verify_get_do_not_disturb_mode(self, response, mode):
        payload_len = f"{3 + 1:02x}"
        mode_status = f"{mode:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == mode_status, Report.logFail(
                f"Do not disturb mode status value {str(response[last_index + 1])} is not equal {mode_status}"
            )
            Report.logPass(f"Correct response for mode '{mode}' received.")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_do_not_disturb_mode(self, mode):
        cmd_do_not_distrurb_mode_cmd = [
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[0],
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[1],
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[2],
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[3],
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[4],
            CMD_SET_DO_NOT_DISTRUB_MODE_CMD[5],
            mode,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=cmd_do_not_distrurb_mode_cmd,
            command_name=f"Set Do Not Disturb Mode to {mode}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Do Not Disturb'")
        return response

    def verify_not_supported_do_not_disturb_mode_state(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error response value received.")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_voice_notification_status(self, state):
        voice_notification_status = [
            CMD_SET_VOICE_NOTIF_STATUS[0],
            CMD_SET_VOICE_NOTIF_STATUS[1],
            CMD_SET_VOICE_NOTIF_STATUS[2],
            CMD_SET_VOICE_NOTIF_STATUS[3],
            CMD_SET_VOICE_NOTIF_STATUS[4],
            CMD_SET_VOICE_NOTIF_STATUS[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=voice_notification_status,
            command_name=f"Set Voice Notification status to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Voice Notification Status'")
        return response

    def get_voice_notification_status(self):
        return self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_GET_VOICE_NOTIF_STATUS,
            command_name="Get Voice Notification Status...",
        )

    def verify_get_voice_notification_status(self, response, status):
        payload_len = f"{3 + 1:02x}"
        voice_notification_status = f"{status:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "2d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            # if self.centurion.conn_type == ConnectionType.bt:
            #     self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == voice_notification_status, Report.logFail(
                f"Voice notification status value {str(response[last_index + 1])} is not equal {voice_notification_status}"
            )
            Report.logPass(f"Voice notification value '{status}' is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_voice_notification_status(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error code received.")
        else:
            assert False, Report.logFail(
                "Error message for not supported voice notification status not found",
                screenshot=False,
            )

    def factory_reset_device(self):
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_FACTORY_RESET_DEVICE,
            command_name="Factory Reset Device...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Factory reset'")
        assert "ff" not in response, Report.logFail("Response should not consist of errors")
        return response

    def get_button_general_settings(self):
        return self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_GET_BUTTON_GEN_SETTINGS,
            command_name="Get Button General Settings...",
        )

    def verify_get_button_general_settings(
        self,
        response,
        button_index,
        long_press,
        short_press,
        tripple_press,
        double_press,
    ):
        if self.centurion.device_name == DeviceName.zone_true_wireless:
            payload_len = f"{3 + 5:02x}"
        else:
            payload_len = f"{3 + 3:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "9d",
        ]
        long_short_press = f"{long_press * 16 + short_press:02x}"
        tripple_double_press = f"{double_press * 16 + double_press:02x}"

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        button_index_hex = f"{button_index:02x}"
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            if button_index == 0:
                assert response[last_index + 1 + 1] == long_short_press, Report.logFail(
                    f"Long - Short Capability for button '{button_index}': {response[last_index + 1 + 1]} is not equal to {long_short_press}"
                )
                Report.logPass(f"Long - Short Capability for button '{button_index}' value is correct")
                assert response[last_index + 1 + 2][1] == tripple_double_press[1], Report.logFail(
                    f"Double Capability for button '{button_index}': {response[last_index + 1 + 2]} is not equal to {tripple_double_press}"
                )
                Report.logPass(f"Double Capability for button '{button_index}' value is correct")
            elif button_index == 1:
                assert response[last_index + 1 + 3] == long_short_press, Report.logFail(
                    f"Long - Short Capability for button '{button_index}': {response[last_index + 1 + 3]} is not equal to {long_short_press}"
                )
                Report.logPass(f"Long - Short Capability for button '{button_index}' value is correct")
                assert response[last_index + 1 + 4][1] == tripple_double_press[1], Report.logFail(
                    f"Double Capability for button '{button_index}': {response[last_index + 1 + 4]} is not equal to {tripple_double_press}"
                )
                Report.logPass(f"Double Capability for button '{button_index}' value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_button_individual_capability(self, button_index):
        button_ind_cap_cmd = [
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[0],
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[1],
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[2],
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[3],
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[4],
            CMD_GET_BUTTON_INDIVIDUAL_CAPABILITY[5],
            button_index,
        ]
        return self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=button_ind_cap_cmd,
            command_name=f"Get Button Individual Capability for Button Index {button_index}...",
        )

    def verify_get_button_individual_capability(self, response, button_index, buttons):
        payload_len = f"{3 + 8:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "ad",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        button_index = f"{button_index:02x}"
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            for i in range(1, 9):
                assert response[last_index + i] == buttons[button_index][i - 1], Report.logFail(
                    f"Supported functions for button index '{button_index}': {response[last_index + i]} is not equal to '{buttons[button_index][i - 1]}'"
                )
            Report.logPass("Supported functions values are correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_response_for_capability_for_wrong_button(self, response):
        if self.centurion.device_name == DeviceName.zone_true_wireless:
            CENTPP_INVALID_PARAM = "03"
        else:
            CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "ad",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error message received")
        else:
            assert False, Report.logFail("Response for capability for wrong button not found", screenshot=False)

    def set_button_customization_settings(self, btn_index, long_press, short_press, tripple_press, double_press):
        set_btn_ind_cap_cmd = [
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[0],
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[1],
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[2],
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[3],
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[4],
            CMD_SET_BUTTON_INDIVIDUAL_CAPABILITY[5],
            btn_index,
            long_press * 16 + short_press,
            tripple_press * 16 + double_press,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=set_btn_ind_cap_cmd,
            command_name="Set Button Customization Settings for button '{}'... to {} {}".format(
                btn_index,
                hex(long_press * 16 + short_press),
                hex(tripple_press * 16 + double_press),
            ),
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Button Customization Settings'")
        return response

    def verify_error_for_setting_wrong_capablity_to_the_button(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "bd",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Correct error message received")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def reset_button_customization_settings(self):
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_RESET_BUTTON_CUSTOMIZATION_SETTINGS,
            command_name="Reset Button Customization Settings",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Reset Customization Settings'")
        assert "ff" not in response, Report.logFail("Error returned for 'Reset Customization Settings'")
        return response

    def set_mic_boom_status(self, state):
        voice_notification_status = [
            CMD_SET_MIC_BOOM_CMD[0],
            CMD_SET_MIC_BOOM_CMD[1],
            CMD_SET_MIC_BOOM_CMD[2],
            CMD_SET_MIC_BOOM_CMD[3],
            CMD_SET_MIC_BOOM_CMD[4],
            CMD_SET_MIC_BOOM_CMD[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=voice_notification_status,
            command_name=f"Set Mic Boom status to {state}...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set  Mic Boom status'")
        return response

    def get_mic_boom_status(self):
        return self.centurion.send_command(
            feature_name="iHeadsetMisc",
            command=CMD_GET_MIC_BOOM_CMD,
            command_name="Get  Mic Boom status...",
        )

    def verify_mic_boom_status(self, response, status):
        payload_len = f"{3 + 1:02x}"
        voice_notification_status = f"{status:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "5d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            # if self.centurion.conn_type == ConnectionType.bt:
            #     self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == voice_notification_status, Report.logFail(
                f"Mic Boom status value {str(response[last_index + 1])} is not equal {voice_notification_status}"
            )
            Report.logPass("Mic Boom value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_mic_boom_status(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetMisc'][4]:02x}",
            "6d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail(
                "Error message for not supported mic boom status not found",
                screenshot=False,
            )
