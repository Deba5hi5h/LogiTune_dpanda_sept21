from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_FIRMWARE_VERSION,
    CMD_GET_HARDWARE_INFO,
    CMD_GET_SERIAL_NUMBER,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.crc import (
    calculate_crc,
    calculate_crc_for_response,
)


class DeviceInfoFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0100_iDeviceInfo.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_hardware_info(self):
        return self.centurion.send_command(
            feature_name="iDeviceInfo",
            command=CMD_GET_HARDWARE_INFO,
            command_name="Get Hardware Info...",
        )

    def verify_hardware_info(self, response, model_id, hw_revision, color_code=None):
        """0	- Model ID
        1	- HardwareRev
        2	- ColorCode (MSB)
        3	- ColorCode (LSB)
        4	- Reserved (MSB)
        5	- Reserved
        6	- Reserved
        7	- Reserved (LSB)
            - WiFi Region (bit 0)"""

        if self.centurion.device_name in [DeviceName.zone_wireless_2, DeviceName.zone_950]:
            payload_len = f"{4 + 8:02x}"
        else:
            payload_len = f"{3 + 8:02x}"


        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iDeviceInfo'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                res_crc_high, res_crc_low = calculate_crc_for_response(
                    response[first_index : first_index + response_len + 1]
                )
                assert response[first_index + response_len + 1] == f"{res_crc_low:02x}"
                assert response[first_index + response_len + 2] == f"{res_crc_high:02x}"

            hw_info_response = []
            for i in range(last_index + 1, last_index + 8 + 1):
                hw_info_response.append(response[i])

            assert hw_info_response[0] == model_id, Report.logFail(
                "Model ID: " + hw_info_response[0] + " is not equal to " + model_id
            )
            Report.logPass("Model ID value is correct")
            assert hw_info_response[1] == hw_revision, Report.logFail(
                "HW Revision" + hw_info_response[1] + " is not equal to " + hw_revision
            )
            Report.logPass("HW Revision value is correct")
            if color_code:
                assert hw_info_response[2] + hw_info_response[3] == color_code, Report.logFail(
                    f"Color Code for {DeviceName.zone_true_wireless}: {hw_info_response[2] + hw_info_response[3]} is not equal to {color_code}"
                )
                Report.logPass("Color code value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_firmware_version(self):
        return self.centurion.send_command(
            feature_name="iDeviceInfo",
            command=CMD_GET_FIRMWARE_VERSION,
            command_name="Get Firmware Version...",
        )

    def verify_firmware_version(self, response, fw_version):
        versions = fw_version.split(".")
        if self.centurion.device_name in [DeviceName.zone_wireless_2, DeviceName.zone_950]:
            payload_len = f"{4 + len(versions):02x}"
        else:
            payload_len = f"{3 + len(versions):02x}"
        version_len = len(versions)
        if self.centurion.device_name == DeviceName.logi_dock:
            sublist = [
                "00",
                f"{self.centurion.device_features['iDeviceInfo'][4]:02x}",
                "1d",
            ]
            if int(versions[2]) > 255:
                version_len = len(versions) + 1
        else:
            sublist = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                payload_len,
                "00",
                f"{self.centurion.device_features['iDeviceInfo'][4]:02x}",
                "1d",
            ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            fw_version_response = []
            if self.centurion.device_name == DeviceName.logi_dock and int(versions[2]) > 255:
                fw_version_response.append(str(int("0x{}".format(response[last_index + 1]), 0)))
                fw_version_response.append(str(int("0x{}".format(response[last_index + 2]), 0)))
                msb_lsb = response[last_index + 3] + response[last_index + 4]
                fw_version_response.append(str(int(msb_lsb, 16)))
            else:
                for i in range(last_index + 1, last_index + version_len + 1):
                    fw_version_response.append(str(int("0x{}".format(response[i]), 0)))
            assert ".".join(fw_version_response) == fw_version, Report.logFail(
                f'{".".join(fw_version_response)} is not equal to {fw_version}'
            )
            Report.logPass("FW version value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_serial_number(self):
        return self.centurion.send_command(
            feature_name="iDeviceInfo",
            command=CMD_GET_SERIAL_NUMBER,
            command_name="Get Serial Number...",
        )

    def verify_serial_number(self, response, serial_number):
        payload_len = f"{4 + len(serial_number):02x}"
        serial_number_len = f"{len(serial_number):02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iDeviceInfo'][4]:02x}",
            "2d",
            serial_number_len,
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            serial_number_response = []
            for i in range(last_index + 1, last_index + len(serial_number) + 1):
                tmp = bytes.fromhex(response[i])
                serial_number_response.append(tmp.decode("ASCII"))
            assert "".join(serial_number_response) == serial_number, Report.logFail(
                f'{"".join(serial_number_response)} is not equal to {serial_number}'
            )
            Report.logPass("Serial number value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
