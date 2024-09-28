from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_AUDIO_ACTIVE_DEVICE,
    CMD_CONNECTED_DEVICE_INFO,
    CMD_CONNECTED_DEVICE_NUMBER,
    CMD_GET_A2DP_MUTE_STATUS,
    CMD_GET_DEVICE_CONNECT_STATUS,
    CMD_GET_DEVICE_CONNECTED_NAME,
    CMD_GET_DONGLE_FW_VERSION,
    CMD_GET_PDL_DEVICE_INFO,
    CMD_GET_PDL_DEVICE_NUMBER,
    CMD_REMOVE_DEVICE_FROM_PDL,
    CMD_SET_A2DP_MUTE_STATUS,
)


class HeadsetBtConnInfoFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0501_iHeadsetBtConnInfo.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_connected_device_number(self):
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=CMD_CONNECTED_DEVICE_NUMBER,
            command_name="Connected Device Number...",
        )

    def verify_get_connected_device_number(self, response, connected_devices):
        payload_len = f"{4:02x}"
        connected_devices_count = f"{connected_devices:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == connected_devices_count, Report.logFail(
                f"Number of connected devices {response[last_index + 1]} is not equal to {connected_devices_count}"
            )
            Report.logPass("Number of connected devices value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_connected_device_info(self, connected_devices_length):
        responses = {}
        for i in range(0, connected_devices_length):
            get_connected_device_info_cmd = [
                CMD_CONNECTED_DEVICE_INFO[0],
                CMD_CONNECTED_DEVICE_INFO[1],
                CMD_CONNECTED_DEVICE_INFO[2],
                CMD_CONNECTED_DEVICE_INFO[3],
                CMD_CONNECTED_DEVICE_INFO[4],
                CMD_CONNECTED_DEVICE_INFO[5],
                i,
            ]
            response = self.centurion.send_command(
                feature_name="iHeadsetBtConnInfo",
                command=get_connected_device_info_cmd,
                command_name=f"Connected Device Number {i}...",
            )
            responses[i] = response
        return responses

    def get_bt_address_from_get_connected_device_info_response(self, response):
        response = response[0]
        payload_len = f"{3 + 7:02x}"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "1d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            bt_address = []
            for i in range(last_index + 2, last_index + 7 + 1):
                bt_address.append(int(response[i], 16))

            return bt_address
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_get_connected_device_info(self, response):
        for key, value in response.items():
            payload_len = f"{3 + 7:02x}"

            sublist = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                payload_len,
                "00",
                f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
                "1d",
            ]
            device_types = ["00", "01"]  # Firmware limitation

            first_index, last_index = self.centurion.find_sub_list(sublist, value)

            if last_index:
                response_len = 2 + int(payload_len, 16)
                if self.centurion.conn_type == ConnectionType.bt:
                    self.centurion.verify_response_crc(value, first_index, response_len)

                pdl_devices_info_response = []
                for i in range(last_index + 1, last_index + 7 + 1):
                    pdl_devices_info_response.append(value[i])

                assert pdl_devices_info_response[0] in device_types, Report.logFail(
                    f"Device info {str(key)}: {str(pdl_devices_info_response[0])} is not equal to 00 or 02"
                )
                Report.logPass("Get connected device info value is correct")
            else:
                assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_device_connected_name(self, bt_address):
        get_device_connected_name_cmd = [
            CMD_GET_DEVICE_CONNECTED_NAME[0],
            CMD_GET_DEVICE_CONNECTED_NAME[1],
            CMD_GET_DEVICE_CONNECTED_NAME[2],
            CMD_GET_DEVICE_CONNECTED_NAME[3],
            CMD_GET_DEVICE_CONNECTED_NAME[4],
            CMD_GET_DEVICE_CONNECTED_NAME[5],
            bt_address[0],
            bt_address[1],
            bt_address[2],
            bt_address[3],
            bt_address[4],
            bt_address[5],
        ]
        if self.centurion.conn_type == ConnectionType.dongle:
            return self.centurion.send_command(
                feature_name="iHeadsetBtConnInfo",
                command=get_device_connected_name_cmd,
                command_name=f"Get Device Connected Name for BT address {bt_address}...",
                long_response_expected=True,
            )
        else:
            return self.centurion.send_command(
                feature_name="iHeadsetBtConnInfo",
                command=get_device_connected_name_cmd,
                command_name=f"Get Device Connected Name for BT address {bt_address}...",
            )

    def verify_get_device_connected_name(self, response, name):
        payload_len = f"{5 + len(name):02x}"
        if self.centurion.device_name.startswith("Zone Vibe") or self.centurion.device_name in DeviceName.zone_300:
            max_len = "20"
        elif self.centurion.device_name in [
            DeviceName.zone_wireless_2,
            DeviceName.zone_950,
        ]:
            max_len = "1f"
        elif self.centurion.device_name in [
            DeviceName.zone_900,
            DeviceName.zone_wireless_plus,
        ]:
            max_len = "1e"
        else:
            max_len = "1f"

        if self.centurion.conn_type == ConnectionType.dongle and self.centurion.device_name not in [
            DeviceName.zone_vibe_wireless,
            DeviceName.zone_vibe_130,
            DeviceName.zone_wireless_2,
            DeviceName.zone_950
        ]:
            chunks = "01"
        else:
            chunks = "00"

        msg_len = f"{3 + 2 + len(name):02x}"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            msg_len,
            chunks,
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "2d",
            max_len,
        ]
        Report.logPass(f"sublist: {sublist}")
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        Report.logPass(f"first index: {first_index}, last index: {last_index}")
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            len_name_hex = f"{len(name):02x}"
            assert response[last_index + 1] == len_name_hex, Report.logFail(
                f"Returned len() of device name '{response[last_index + 1]}' is not equal to '{len_name_hex}'"
            )

            name_response = []
            for i in range(last_index + 2, last_index + 2 + len(name)):
                tmp = bytes.fromhex(response[i])
                name_response.append(tmp.decode("ASCII"))
            assert name == "".join(name_response), Report.logFail(f'{name} is not equal to {"".join(name_response)}')
            Report.logPass("Connected device name value is correct")

        else:
            assert False, "Response pattern not found. Probably wrong Device Name returned."

    def get_device_connected_status(self, bt_address):
        get_device_connected_cmd = [
            CMD_GET_DEVICE_CONNECT_STATUS[0],
            CMD_GET_DEVICE_CONNECT_STATUS[1],
            CMD_GET_DEVICE_CONNECT_STATUS[2],
            CMD_GET_DEVICE_CONNECT_STATUS[3],
            CMD_GET_DEVICE_CONNECT_STATUS[4],
            CMD_GET_DEVICE_CONNECT_STATUS[5],
            bt_address[0],
            bt_address[1],
            bt_address[2],
            bt_address[3],
            bt_address[4],
            bt_address[5],
        ]
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=get_device_connected_cmd,
            command_name=f"Get Device Connected status for BT address {bt_address}...",
        )

    def verify_get_device_connected_status(self, response, status):
        payload_len = f"{4:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == status, Report.logFail(
                f"Status of connected devices {response[last_index + 1]} is not equal to {status}"
            )
            Report.logPass("Status of connected devices value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_audio_active_device(self):
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=CMD_AUDIO_ACTIVE_DEVICE,
            command_name="Get Audio Active Device...",
        )

    def verify_get_audio_active_device(self, response, bt_address, status):
        payload_len = f"{10:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "4d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 7] == status, Report.logFail(
                f"Status of audio active device {response[last_index + 7]} is not equal to {status}"
            )
            Report.logPass("Status of active device value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_dongle_fw_version(self):
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=CMD_GET_DONGLE_FW_VERSION,
            command_name="Get Dongle FW Version...",
        )

    def verify_get_dongle_fw_version(self, response, dongle_fw_version):
        dongle_ver_len = len(dongle_fw_version.split("."))
        payload_len = f"{3 + 6:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "6d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            dongle_fw_ver_response = []
            for i in range(last_index + 1 + 2, last_index + dongle_ver_len + 2 + 1):
                dongle_fw_ver_response.append(str(int(response[i], 16)))
            assert ".".join(dongle_fw_ver_response) == dongle_fw_version, Report.logFail(
                f'{".".join(dongle_fw_ver_response)} is not equal to {dongle_fw_version}'
            )
            Report.logPass("Dongle FW version value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_error_message_on_get_driver_fw_version(self, response):
        CENTPP_INVALID_PARAM = "0a"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "6d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported A2DP mute status is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail(
                "Error message for not supported A2DP mute status not found",
                screenshot=False,
            )

    def get_A2DP_mute_status(self, bt_address):
        get_A2DP_mute_status_cmd = [
            CMD_GET_A2DP_MUTE_STATUS[0],
            CMD_GET_A2DP_MUTE_STATUS[1],
            CMD_GET_A2DP_MUTE_STATUS[2],
            CMD_GET_A2DP_MUTE_STATUS[3],
            CMD_GET_A2DP_MUTE_STATUS[4],
            CMD_GET_A2DP_MUTE_STATUS[5],
            bt_address[0],
            bt_address[1],
            bt_address[2],
            bt_address[3],
            bt_address[4],
            bt_address[5],
        ]
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=get_A2DP_mute_status_cmd,
            command_name=f"Get A2DP Mute Status for BT address {bt_address}...",
        )

    def set_A2DP_mute_status(self, bt_address, status):
        get_A2DP_mute_status_cmd = [
            CMD_SET_A2DP_MUTE_STATUS[0],
            CMD_SET_A2DP_MUTE_STATUS[1],
            CMD_SET_A2DP_MUTE_STATUS[2],
            CMD_SET_A2DP_MUTE_STATUS[3],
            CMD_SET_A2DP_MUTE_STATUS[4],
            CMD_SET_A2DP_MUTE_STATUS[5],
            bt_address[0],
            bt_address[1],
            bt_address[2],
            bt_address[3],
            bt_address[4],
            bt_address[5],
            status,
        ]
        response = self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=get_A2DP_mute_status_cmd,
            command_name=f"Set A2DP Mute Status for BT address {bt_address} to {status}...",
        )
        assert len(response) > 0, "Empty response_raw returned for set 'Set A2DP Mute Status'"
        return response

    def verify_get_A2DP_mute_status(self, response, status):
        payload_len = f"{3 + 1:02x}"
        mic_mute_status = f"{status:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "7d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == mic_mute_status, Report.logFail(
                f"A2DP Mute status value {str(response[last_index + 1])} is not equal {mic_mute_status}"
            )
            Report.logPass("A2DP Mute status value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_get_A2DP_mute_status_cybermorh(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "7d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported A2DP mute status is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail(
                "Error message for not supported A2DP mute status not found",
                screenshot=False,
            )

    def verify_not_supported_A2DP_mu_status(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "8d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported A2DP mute status is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail(
                "Error message for not supported A2DP mute status not found",
                screenshot=False,
            )

    def get_pdl_device_number(self):
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=CMD_GET_PDL_DEVICE_NUMBER,
            command_name="Get PDL Device Number...",
        )

    def get_length_of_pdl(self, response):
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "04",
            "00",
            f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
            "9d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            return int(response[last_index + 1])
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_pdl_devices_info(self, pdl_length):
        responses = {}
        for i in range(0, pdl_length):
            get_pdl_device_info_cmd = [
                CMD_GET_PDL_DEVICE_INFO[0],
                CMD_GET_PDL_DEVICE_INFO[1],
                CMD_GET_PDL_DEVICE_INFO[2],
                CMD_GET_PDL_DEVICE_INFO[3],
                CMD_GET_PDL_DEVICE_INFO[4],
                CMD_GET_PDL_DEVICE_INFO[5],
                i,
            ]
            response = self.centurion.send_command(
                feature_name="iHeadsetBtConnInfo",
                command=get_pdl_device_info_cmd,
                command_name=f"Get PDL Device INFO: {i}...",
            )
            responses[i] = response
        return responses

    def verify_pdl_devices_info(self, response):
        for key, value in response.items():
            Report.logInfo(f"Verify response for device no: {key}")
            payload_len = f"{3 + 7:02x}"
            sublist = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                payload_len,
                "00",
                f"{self.centurion.device_features['iHeadsetBtConnInfo'][4]:02x}",
                "ad",
            ]
            device_types = ["00", "01"]  # Firmware limitation
            first_index, last_index = self.centurion.find_sub_list(sublist, value)
            if last_index:
                response_len = 2 + int(payload_len, 16)
                if self.centurion.conn_type == ConnectionType.bt:
                    self.centurion.verify_response_crc(value, first_index, response_len)

                pdl_devices_info_response = []
                for i in range(last_index + 1, last_index + 7 + 1):
                    pdl_devices_info_response.append(value[i])

                assert pdl_devices_info_response[0] in device_types, Report.logFail(
                    f"PDL Device info {str(key)}:  {str(pdl_devices_info_response[0])} is not equal to 00 or 02"
                )
                Report.logPass("PDL device info value is correct")
            else:
                assert False, Report.logFail("Response pattern not found", screenshot=False)

    def remove_device_from_pdl(self):
        return self.centurion.send_command(
            feature_name="iHeadsetBtConnInfo",
            command=CMD_REMOVE_DEVICE_FROM_PDL,
            command_name="Remove Device from PDL...",
        )
