from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_ZAXXON_CHARGING_CASE_INFO,
)


class ZaxxonChargingCaseInfoFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0512_iZaxxonChargingCaseInfo.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_zaxxon_charging_case_info(self):
        return self.centurion.send_command(
            feature_name="iZaxxonChargingCaseInfo",
            command=CMD_GET_ZAXXON_CHARGING_CASE_INFO,
            command_name="Get Zaxxon Charging Case Info...",
        )

    def verify_get_zaxxon_charging_case_info(self, response, state):
        pass
