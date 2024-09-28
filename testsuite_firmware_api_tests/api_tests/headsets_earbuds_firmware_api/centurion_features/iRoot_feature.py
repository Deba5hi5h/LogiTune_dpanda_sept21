from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_FEATURE,
    CMD_GET_PROTOCOL_VERSION,
)


class RootFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0000_iRoot.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_not_supported_feature(self, feature):
        command = [
            CMD_GET_FEATURE[0],
            CMD_GET_FEATURE[1],
            CMD_GET_FEATURE[2],
            CMD_GET_FEATURE[3],
            CMD_GET_FEATURE[4],
            CMD_GET_FEATURE[5],
            feature[0],
            feature[1],
        ]
        response = self.centurion.send_command(
            feature_name="iRoot",
            command=command,
            command_name="Not supported feature ...",
        )
        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Get not supported feature'")
        return response

    def verify_not_supported_feature(self, response):
        if self.centurion.device_name in [DeviceName.zone_true_wireless,
                                        DeviceName.bomberman_mono,
                                        DeviceName.bomberman_stereo]:
            ERROR_CODE = "05"
        elif self.centurion.device_name in [
            DeviceName.zone_wired,
            DeviceName.zone_750,
            DeviceName.zone_wired_earbuds,
        ]:
            ERROR_CODE = "02"
        else:
            ERROR_CODE = "01"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iRoot'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, 7)
            assert response[last_index + 1] == ERROR_CODE, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {ERROR_CODE}"
            )
            Report.logPass("Correct error code received.")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_not_existing_feature(self):
        NOT_EXISTING_FEATURE = [0x0F, 0x0F]
        command = [
            CMD_GET_FEATURE[0],
            CMD_GET_FEATURE[1],
            CMD_GET_FEATURE[2],
            CMD_GET_FEATURE[3],
            CMD_GET_FEATURE[4],
            CMD_GET_FEATURE[5],
            NOT_EXISTING_FEATURE[0],
            NOT_EXISTING_FEATURE[1],
        ]
        return self.centurion.send_command(
            feature_name="iRoot",
            command=command,
            command_name="Not existing feature ...",
        )

    def verify_not_existing_feature(self, response):
        if self.centurion.device_name in [DeviceName.zone_true_wireless,
                                          DeviceName.bomberman_mono,
                                          DeviceName.bomberman_stereo]:
            ERROR_CODE = "05"
        elif self.centurion.device_name == [
            DeviceName.zone_wired,
            DeviceName.zone_750,
            DeviceName.zone_wired_earbuds,
        ]:
            ERROR_CODE = "02"
        else:
            ERROR_CODE = "01"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iRoot'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, 7)
            assert response[last_index + 1] == ERROR_CODE, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {ERROR_CODE}"
            )
            Report.logPass("Correct error log received.")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_features(self, features):
        response = {}
        for key, value in features.items():
            command = [
                CMD_GET_FEATURE[0],
                CMD_GET_FEATURE[1],
                CMD_GET_FEATURE[2],
                CMD_GET_FEATURE[3],
                CMD_GET_FEATURE[4],
                CMD_GET_FEATURE[5],
                value[0],
                value[1],
            ]
            tmp = self.centurion.send_command(feature_name="iRoot", command=command, command_name=key + " ...")
            response[key] = tmp
        return response

    def verify_get_features_responses(self, response, features):
        for key, value in response.items():
            payload_len = f"{3 + 3:02x}"

            sublist = [
                self.centurion.msg_sync_words[1][0],
                self.centurion.msg_sync_words[1][1],
                payload_len,
                "00",
                f"{self.centurion.device_features['iRoot'][4]:02x}",
                "0d",
            ]

            first_index, last_index = self.centurion.find_sub_list(sublist, value)

            if last_index:
                response_len = 2 + int(payload_len, 16)
                if self.centurion.conn_type == ConnectionType.bt:
                    self.centurion.verify_response_crc(value, first_index, response_len)

                feature_response = []
                for i in range(last_index + 1, last_index + 3 + 1):
                    feature_response.append(value[i])

                Report.logInfo(f"Check response for feature: {key}")
                assert feature_response[0] == features[key][5][-2:], Report.logFail(
                    f"Feature index for {key} : {str(feature_response[0])} is not equal to: {str(features[key][5][-2:])}"
                )
                Report.logPass("Feature index value is correct")
                assert feature_response[1] == f"{features[key][2]:02x}", Report.logFail(
                    f"Feature desc for {key} : {str(feature_response[1])} is not equal to: {features[key][2]:02x}"
                )
                Report.logPass("Feature desc value is correct")
                assert feature_response[2] == f"{features[key][3]:02x}", Report.logFail(
                    f"Feature version for {key} : {str(feature_response[2])} is not equal to: {features[key][3]:02x}"
                )
                Report.logPass("feature version value is correct")

    def get_protocol_version(self):
        return self.centurion.send_command(
            feature_name="iRoot",
            command=CMD_GET_PROTOCOL_VERSION,
            command_name="Get Protocol Version...",
        )

    def verify_protocol_version(self, response):
        payload_len = f"{3 + 3:02x}"
        protocol_version = "01"
        target_host_software = "20"  # Logitech

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iRoot'][4]:02x}",
            "1d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            protocol_response = []
            for i in range(last_index + 1, last_index + 3 + 1):
                protocol_response.append(response[i])

            assert protocol_response[0] == protocol_version, Report.logFail(
                f"Protocol version: {protocol_response[0]} is not equal to {protocol_version}"
            )
            Report.logPass("Protocol version value is correct")
            assert protocol_response[1] == target_host_software, Report.logFail(
                f"Target Host SW: {protocol_response[1]} is not equal to {target_host_software}"
            )
            Report.logPass("Target Host SW value is correct")

        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
