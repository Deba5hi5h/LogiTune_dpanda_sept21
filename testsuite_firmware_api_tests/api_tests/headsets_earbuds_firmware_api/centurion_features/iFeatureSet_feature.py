from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import (
    ConnectionType,
    DeviceName,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_FEATURE_COUNT,
    CMD_GET_FEATURE_ID,
)


class FeatureSetFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0001_iFeatureSet.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_feature_count(self):
        return self.centurion.send_command(
            feature_name="iFeatureSet",
            command=CMD_GET_FEATURE_COUNT,
            command_name="Get Feature ID..." "Get Feature Count...",
        )

    def verify_feature_count(self, response, count):
        payload_len = f"{2 + 2:02x}"
        feature_count = f"{count:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "04",
            "00",
            f"{self.centurion.device_features['iFeatureSet'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == feature_count, Report.logFail(
                f"Feature count {response[last_index + 1]} is not equal to {feature_count}"
            )
            Report.logPass("Feature count value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def get_feature_id(self):
        if self.centurion.conn_type in [
            ConnectionType.dongle,
            ConnectionType.usb_dock,
        ] or self.centurion.device_name in [DeviceName.zone_true_wireless]:
            return self.centurion.send_command(
                feature_name="iFeatureSet",
                command=CMD_GET_FEATURE_ID,
                command_name="Get Feature ID...",
                long_response_expected=True,
            )

        return self.centurion.send_command(
            feature_name="iFeatureSet",
            command=CMD_GET_FEATURE_ID,
            command_name="Get Feature ID...",
        )

    def verify_get_feature_id(self, response, features):
        payload_len = f"{4 + 4 * (len(features)):02x}"

        if self.centurion.conn_type in [ConnectionType.dongle, ConnectionType.usb_dock]:
            if self.centurion.device_name in [
                DeviceName.zone_vibe_130,
                DeviceName.zone_vibe_wireless,
            ]:
                chunks = "00"
            else:
                chunks = "01"
        elif self.centurion.conn_type == ConnectionType.bt and self.centurion.device_name in [
            DeviceName.zone_true_wireless
        ]:
            chunks = "01"
        elif self.centurion.conn_type == ConnectionType.bt and self.centurion.device_name in [
            DeviceName.zone_vibe_100,
            DeviceName.zone_vibe_125,
            DeviceName.zone_vibe_130,
            DeviceName.zone_vibe_wireless,
        ]:
            chunks = "00"
        else:
            chunks = "00"

        sublist = [
            chunks,
            f"{self.centurion.device_features['iFeatureSet'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            features_id_response = []

            for i in range(last_index + 1, last_index + (len(features) - 1) * 4 + 2):
                features_id_response.append(response[i])

            features_len = f"{len(features):02x}"

            assert features_id_response[0] == features_len, Report.logFail(
                f"Feature count {str(features_id_response[0])} is not equal to {features_len}"
            )

            Report.logPass("Feature count value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
