from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_ZAXXON_START_GAIA_OTA,
)


class ZaxxonStartGaiaOtaFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0513_iZaxxonStartGaiaOta.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_zaxxon_start_gaia_ota(self):
        return self.centurion.send_command(
            feature_name="iZaxxonStartGaiaOta",
            command=CMD_ZAXXON_START_GAIA_OTA,
            command_name="Start Gaia OTA...",
        )

    def verify_get_zaxxon_start_gaia_ota(self, response, state):
        pass
