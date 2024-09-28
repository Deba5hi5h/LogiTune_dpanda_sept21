from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import *


class CentPPBridgeFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0003_iCentPPBridge.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_connection_info(self):
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=CMD_GET_CON_INFO,
            command_name="Get Conenction Info...",
        )

    def verify_get_connection_info(self, response):
        payload_len = f"{3 + 5:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iCentPPBridge'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            connection_info_response = []
            for i in range(last_index + 1, last_index + 5 + 1):
                connection_info_response.append(response[i])
            assert connection_info_response[4] == "00", Report.logFail(
                f"Transport value {str(connection_info_response[4])} is not equal for '00'"
            )
            Report.logPass("Transport value value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_protocol_version_from_secondary_earbud(self):
        second_fragment = [0x00, 0x04, 0x00, 0x00, 0x1F, 0xDA]
        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get protocol Version from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_protocol_version_from_secondary_earbud(self, response):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]
        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 6:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "06",
            "00",
        ]
        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        protocol_version = "01"
        target_host_software = "20"  # Logitech

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "00", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: '00'"
            )
            Report.logPass("Feature index value is correct")
            assert response[last_index + 2] == "1f", Report.logFail(
                f"Function value: {response[last_index + 2]} is not equal to function value: '1f'"
            )
            Report.logPass("Function value is correct")
            assert response[last_index + 3] == protocol_version, Report.logFail(
                f"Protocol version: {response[last_index + 3]} is not equal to {protocol_version}"
            )
            Report.logPass("Protocol value is correct")
            assert response[last_index + 4] == target_host_software, Report.logFail(
                f"Target Host SW: {response[last_index + 4]} is not equal to {target_host_software}"
            )
            Report.logPass("Target Host SW value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_features_from_secondary_earbud(self):
        from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zaxxon import (
            FEATURES_SECONDARY_EARBUD_ZAXXON,
        )

        response = {}
        for key, value in FEATURES_SECONDARY_EARBUD_ZAXXON.items():
            second_fragment = [0x00, 0x05, 0x00, 0x00, 0x0F, value[0], value[1]]

            data_len = 3 + len(second_fragment)
            first_fragment = [
                self.centurion.msg_sync_words[0][0],
                self.centurion.msg_sync_words[0][1],
                data_len,
                0x00,
                0x02,
                0x1F,
            ]
            cmd = first_fragment + second_fragment

            tmp = self.centurion.send_command(
                feature_name="iCentPPBridge",
                command=cmd,
                command_name=key + " ...",
                is_centippbridge=True,
            )
            response[key] = tmp

        return response

    def verify_get_features_from_secondary_earbud(self, responses):
        from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zaxxon import (
            FEATURES_SECONDARY_EARBUD_ZAXXON,
        )

        for key, value in responses.items():
            icentppbridge_response = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                "03",
                "00",
                "02",
                "1f",
            ]

            assert self.centurion.find_sub_list(icentppbridge_response, value) is not None, Report.logFail(
                "Missing response_raw for iCentPPBridge command"
            )

            payload_len = f"{4 + 1 + 6:02x}"
            sub_response = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                payload_len,
                "00",
                "02",
                "10",
                "00",
                "06",
                "00",
            ]

            first_index, last_index = self.centurion.find_sub_list(sub_response, value)

            if last_index:
                response_len = 2 + int(payload_len, 16)
                if self.centurion.conn_type == ConnectionType.bt:
                    self.centurion.verify_response_crc(value, first_index, response_len)

                assert value[last_index + 1] == "00", Report.logFail(
                    f"Feature index: {value[last_index + 1]} is not equal to feature index: '00'"
                )
                Report.logPass("Feature index value is correct")
                assert value[last_index + 2] == "0f", Report.logFail(
                    f"Feature value: {value[last_index + 2]} is not equal to function value: '0f'"
                )
                Report.logPass("Feature value is correct")

                assert value[last_index + 3] == FEATURES_SECONDARY_EARBUD_ZAXXON[key][5][-2:], Report.logFail(
                    f"Feature index for {key}: {str(value[last_index + 2])} is not equal to: {str(FEATURES_SECONDARY_EARBUD_ZAXXON[key][5][-2:])}"
                )
                Report.logPass("Feature index value is correct")
                assert value[last_index + 4] == f"{FEATURES_SECONDARY_EARBUD_ZAXXON[key][2]:02x}", Report.logFail(
                    f"Feature desc for {key}: {str(value[last_index + 4])} is not equal to: {FEATURES_SECONDARY_EARBUD_ZAXXON[key][2]:02x}"
                )
                Report.logPass("Feature description value is correct")
                assert value[last_index + 5] == f"{FEATURES_SECONDARY_EARBUD_ZAXXON[key][3]:02x}", Report.logFail(
                    f"Feature version for {key}: {str(value[last_index + 5])} is not equal to: {FEATURES_SECONDARY_EARBUD_ZAXXON[key][3]:02x}"
                )
                Report.logPass("Feature version value is correct")

            else:
                assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_feature_count_from_secondary_earbud(self):
        second_fragment = [0x00, 0x03, 0x00, 0x01, 0x0F]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get feature count from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_feature_count_from_secondary_earbud(self, response):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 4:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "04",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "01", Report.logFail(
                f"Feature index: {response[last_index + 1]}is not equal to feature index: '01'"
            )
            Report.logPass("Feature index value is correct")

            assert response[last_index + 2] == "0f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: '0f'"
            )
            Report.logPass("Feature version value is correct")

            assert response[last_index + 3] == "04", Report.logFail(
                f"Feature count: {response[last_index + 3]} is not equal to '04'"
            )
            Report.logPass("Feature count value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_feature_id_from_secondary_earbud(self):
        second_fragment = [0x00, 0x04, 0x00, 0x01, 0x1F, 0x00]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get feature id from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_feature_id_from_secondary_earbud(self, response):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]
        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 20:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "14",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "01", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: '01'"
            )
            Report.logPass("Feature index value is correct")

            assert response[last_index + 2] == "1f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: '1f'"
            )
            Report.logPass("Feature value is correct")

            assert response[last_index + 3] == "04", Report.logFail(
                f"Feature count: {response[last_index + 3]} is not equal to '04'"
            )
            Report.logPass("Feature count value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_get_feature_id_from_secondary_earbud_dongle(self, response):
        # TODO temporary method to verify feature id from secondary earbuds
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]
        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "12",
            "01",
            "02",
            "10",
            "00",
            "14",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:

            assert response[last_index + 1] == "01", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 01"
            )
            Report.logPass("Feature index value is correct")

            assert response[last_index + 2] == "1f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: 1f"
            )
            Report.logPass("Feature value is correct")

            assert response[last_index + 3] == "04", Report.logFail(
                f"Feature count: {response[last_index + 3]} is not equal to 04"
            )
            Report.logPass("Feature count value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_serial_number_from_secondary_earbud(self):
        second_fragment = [0x00, 0x03, 0x00, 0x02, 0x2F]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get serial number from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_serial_number_from_secondary_earbud(self, response, serial_number):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 16:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "10",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "02", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 02"
            )
            Report.logPass("Feature index value is correct")
            assert response[last_index + 2] == "2f", Report.logFail(
                f"Feature value: {response[last_index + 2]}  is not equal to function value: 2f"
            )
            Report.logPass("Feature value is correct")

            serial_number_response = []
            for i in range(last_index + 4, last_index + 4 + len(serial_number)):
                tmp = bytes.fromhex(response[i])
                serial_number_response.append(tmp.decode("ASCII"))
            assert "".join(serial_number_response) == serial_number, Report.logFail(
                f'{"".join(serial_number_response)} is not equal to {serial_number}'
            )

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_get_serial_number_from_secondary_earbud_dongle(self, response, serial_number):
        # TODO temporary method to verify serial number from secondary earbuds
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 16:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "12",
            "01",
            "02",
            "10",
            "00",
            "10",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:

            assert response[last_index + 1] == "02", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 02"
            )
            Report.logPass("Feature index value is correct")
            assert response[last_index + 2] == "2f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: 2f"
            )
            Report.logPass("Feature value is correct")

            serial_number_response = []
            for i in range(last_index + 4, last_index + 4 + 9):
                tmp = bytes.fromhex(response[i])
                serial_number_response.append(tmp.decode("ASCII"))
            for i in range(last_index + 17, len(response)):
                tmp = bytes.fromhex(response[i])
                serial_number_response.append(tmp.decode("ASCII"))
            assert "".join(serial_number_response) == serial_number, Report.logFail(
                f'{"".join(serial_number_response)} is not equal to {serial_number}'
            )

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_firmware_version_from_secondary_earbud(self):
        second_fragment = [0x00, 0x03, 0x00, 0x02, 0x1F]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get firmware version from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_firmware_version_from_secondary_earbud(self, response, fw_version):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 7:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "07",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "02", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 02"
            )
            Report.logPass("Feature index value is correct")
            assert response[last_index + 2] == "1f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: 1f"
            )
            Report.logPass("Feature value is correct")
            versions = fw_version.split(".")
            fw_version_response = []
            for i in range(last_index + 3, last_index + 3 + len(versions)):
                fw_version_response.append(str(int("0x{}".format(response[i]), 0)))

            assert ".".join(fw_version_response) == fw_version, Report.logFail(
                f'{".".join(fw_version_response)} is not equal to {fw_version}'
            )
            Report.logPass("Firmware version value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_hardware_info_from_secondary_earbud(self):
        second_fragment = [0x00, 0x03, 0x00, 0x02, 0x0F]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get hardware info from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_hardware_info_from_secondary_earbud(self, response):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 11:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "0b",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "02", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 02"
            )
            Report.logPass("Firmware index value is correct")
            assert response[last_index + 2] == "0f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: 0f"
            )
            Report.logPass("Firmware value is correct")
            model_id = "10"  # zaxxon
            hw_revision = "01"

            assert response[last_index + 3] == model_id, Report.logFail(
                f"Model ID: {response[last_index + 3]} is not equal to {model_id}"
            )
            Report.logPass("Model ID value is correct")
            assert response[last_index + 4] == hw_revision, Report.logFail(
                f"HW Revision {response[last_index + 4]} is not equal to {hw_revision}"
            )
            Report.logPass("HW Revision value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_battery_status_from_secondary_earbud(self):
        second_fragment = [0x00, 0x03, 0x00, 0x03, 0x0F]

        data_len = 3 + len(second_fragment)
        first_fragment = [
            self.centurion.msg_sync_words[0][0],
            self.centurion.msg_sync_words[0][1],
            data_len,
            0x00,
            0x02,
            0x1F,
        ]
        cmd = first_fragment + second_fragment
        return self.centurion.send_command(
            feature_name="iCentPPBridge",
            command=cmd,
            command_name="Get battery status from secondary earbud...",
            is_centippbridge=True,
        )

    def verify_get_battery_status_from_secondary_earbud(self, response):
        icentppbridge_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "03",
            "00",
            "02",
            "1f",
        ]

        assert self.centurion.find_sub_list(icentppbridge_response, response) is not None, Report.logFail(
            "Missing response_raw for iCentPPBridge command"
        )

        payload_len = f"{4 + 1 + 6:02x}"
        sub_response = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            "02",
            "10",
            "00",
            "06",
            "00",
        ]

        first_index, last_index = self.centurion.find_sub_list(sub_response, response)
        Report.logInfo(f"First index: {first_index}, Last index: {last_index}")
        Report.logInfo(f"Response to find: {sub_response}")

        if last_index:

            assert response[last_index + 1] == "03", Report.logFail(
                f"Feature index: {response[last_index + 1]} is not equal to feature index: 03)"
            )
            Report.logPass("Firmware index value is correct")
            assert response[last_index + 2] == "0f", Report.logFail(
                f"Feature value: {response[last_index + 2]} is not equal to function value: 0f"
            )
            Report.logPass("Firmware value is correct")

            real_soc = int(response[last_index + 3], 16)
            user_soc = int(response[last_index + 4], 16)
            assert real_soc <= 100, Report.logFail(f"Real SOC Battery value {str(real_soc)} is out of range")
            Report.logPass("Real SOC Battery value is correct")
            assert user_soc <= 100, Report.logFail(f"User SOC Battery value {str(user_soc)} is out of range")
            Report.logPass("User SOC Battery value is correct")
            assert response[last_index + 5] == "00" or response[2] == "03", Report.logFail(
                f"Charging state {str(response[last_index + 5])} is not equal for '00' or '03'"
            )
            Report.logPass("Charging state value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
