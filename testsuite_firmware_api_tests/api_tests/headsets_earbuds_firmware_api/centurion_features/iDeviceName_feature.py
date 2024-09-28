from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_DEFAULT_NAME,
    CMD_GET_MAX_NAME_LENGTH,
    CMD_GET_NAME,
    CMD_SET_NAME,
)


class DeviceNameFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0101_iDeviceName.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def verify_name(self, response, name, max_length):
        payload_len = f"{5 + len(name):02x}"
        name_len = f"{len(name):02x}"
        max_length = f"{max_length:02x}"

        if self.centurion.conn_type == ConnectionType.dongle and self.centurion.device_name in [
            DeviceName.zone_vibe_wireless,
            DeviceName.zone_vibe_130,
            DeviceName.zone_wireless_2,
            DeviceName.zone_950,
            DeviceName.zone_305
        ]:
            data_chunk = "00"

        elif self.centurion.conn_type == ConnectionType.dongle and self.centurion.device_name not in [
            DeviceName.zone_wired,
            DeviceName.zone_750,
            DeviceName.zone_wired_earbuds,
        ]:
            if len(name) < 14:
                data_chunk = "00"
            else:
                data_chunk = "01"
        elif self.centurion.conn_type == ConnectionType.usb_dock and name_len == max_length:
            data_chunk = "01"
        else:
            data_chunk = "00"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            data_chunk,
            f"{self.centurion.device_features['iDeviceName'][4]:02x}",
            "0d",
            max_length,
            name_len,
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            name_response = []
            for i in range(last_index + 1, last_index + len(name) + 1):
                tmp = bytes.fromhex(response[i])
                name_response.append(tmp.decode("ASCII"))

            assert name == "".join(name_response), Report.logFail(f'{name} is not equal to {"".join(name_response)}')
            Report.logPass("Device name value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_device_name(self):
        return self.centurion.send_command(
            feature_name="iDeviceName",
            command=CMD_GET_NAME,
            command_name="Get Name...",
            long_response_expected=True,
        )

    def set_device_name(self, name):
        payload_len = 4 + len(name)
        name_len = len(name)
        set_name = [
            CMD_SET_NAME[0],
            CMD_SET_NAME[1],
            payload_len,
            CMD_SET_NAME[3],
            CMD_SET_NAME[4],
            CMD_SET_NAME[5],
            name_len,
        ]

        for c in name:
            set_name.append(ord(c))

        response = self.centurion.send_command(
            feature_name="iDeviceName",
            command=set_name,
            command_name=f"Set Device Name to {name}",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for set 'Set Device Name'")
        return response

    def get_default_device_name(self):
        return self.centurion.send_command(
            feature_name="iDeviceName",
            command=CMD_GET_DEFAULT_NAME,
            command_name="Get Default Device Name...",
            long_response_expected=True,
        )

    def verify_default_name(self, response, name):
        payload_len = f"{4 + len(name):02x}"
        name_len = f"{len(name):02x}"
        if (
            self.centurion.conn_type == ConnectionType.dongle
            and self.centurion.device_name == DeviceName.zone_true_wireless
        ):
            data_chunk = "01"
        else:
            data_chunk = "00"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            data_chunk,
            f"{self.centurion.device_features['iDeviceName'][4]:02x}",
            "2d",
            name_len,
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            name_response = []
            for i in range(last_index + 1, last_index + len(name) + 1):
                tmp = bytes.fromhex(response[i])
                name_response.append(tmp.decode("ASCII"))
            assert name == "".join(name_response), Report.logFail(f'{name} is not equal to {"".join(name_response)}')
            Report.logPass("Default name value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_max_name_length(self):
        return self.centurion.send_command(
            feature_name="iDeviceName",
            command=CMD_GET_MAX_NAME_LENGTH,
            command_name="Get Max Name Length...",
        )

    def verify_device_name_max_lenght(self, response, max_length):
        payload_len = f"{4:02x}"
        max_length = f"{max_length:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iDeviceName'][4]:02x}",
            "3d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)
            assert max_length == response[last_index + 1], Report.logFail(
                f"{max_length} is not equal to {response[last_index + 1]}"
            )
            Report.logPass("Device name max length value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_error_for_setting_too_long_name(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iDeviceName'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for too long device name is not equal to {CENTPP_INVALID_PARAM}"
            )
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
