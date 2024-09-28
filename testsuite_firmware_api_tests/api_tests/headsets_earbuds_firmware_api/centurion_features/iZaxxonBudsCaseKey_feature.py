from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_BUDS_CASE_AES_KEY,
)


class ZaxxonBudsCaseKeyFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0511_iZaxxonBudsCaseKey.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_buds_case_aes_key(self):
        return self.centurion.send_command(
            feature_name="iZaxxonBudsCaseKey",
            command=CMD_GET_BUDS_CASE_AES_KEY,
            command_name="Get Buds Case Aes Kay...",
            long_response_expected=True,
        )

    def verify_get_buds_case_aes_key(self, response):
        payload_len = f"{3 + 16 + 1:02x}"
        if self.centurion.conn_type in [ConnectionType.dongle, ConnectionType.usb_dock]:
            data_chunk = "01"
        else:
            data_chunk = "00"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            data_chunk,
            f"{self.centurion.device_features['iZaxxonBudsCaseKey'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == "10", f"Count value {str(response[last_index + 1])} is not equal to '10'"
            for i in range(1, 13):
                assert response[last_index + 1 + i] != "00"
            for i in range(13, 17):
                assert response[last_index + 1 + i] == "00"  # zaxxon
            Report.logPass("Buds AES keys value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)
