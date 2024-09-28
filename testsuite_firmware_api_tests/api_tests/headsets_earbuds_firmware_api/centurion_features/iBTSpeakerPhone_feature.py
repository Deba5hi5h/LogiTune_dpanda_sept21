from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_SPEAKERPHONE_AUDIO_STATE,
    CMD_GET_SPEAKERPHONE_CONN_STATE,
    CMD_GET_SPEAKERPHONE_INFO,
    CMD_GET_SPEAKERPHONE_PAIRED_DEV_INFO,
    CMD_GET_SPEAKERPHONE_PAIRING_STATE,
)


class BTSpeakerPhoneFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0306_iBTSpeakerPhone.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_speakerphone_info(self):
        return self.centurion.send_command(
            feature_name="iBTSpeakerPhone",
            command=CMD_GET_SPEAKERPHONE_INFO,
            command_name=f"Get SpeakerPhone Info...",
        )

    def verify_get_speakerphone_info(self, response):
        assert 1 == 0, "Not implemented"

    def get_audio_state(self):
        return self.centurion.send_command(
            feature_name="iBTSpeakerPhone",
            command=CMD_GET_SPEAKERPHONE_AUDIO_STATE,
            command_name=f"Get SpeakerPhone Audio State...",
        )

    def verify_get_audio_state(self, response):
        assert 1 == 0, "Not implemented"

    def get_connection_state(self):
        return self.centurion.send_command(
            feature_name="iBTSpeakerPhone",
            command=CMD_GET_SPEAKERPHONE_CONN_STATE,
            command_name=f"Get SpeakerPhone Connection state...",
        )

    def verify_get_connection_state(self, response):
        assert 1 == 0, "Not implemented"

    def get_pairing_state(self):
        return self.centurion.send_command(
            feature_name="iBTSpeakerPhone",
            command=CMD_GET_SPEAKERPHONE_PAIRING_STATE,
            command_name=f"Get SpeakerPhone Pairing State...",
        )

    def verify_get_pairing_state(self, response):
        assert 1 == 0, "Not implemented"

    def get_paired_device_info(self):
        return self.centurion.send_command(
            feature_name="iBTSpeakerPhone",
            command=CMD_GET_SPEAKERPHONE_PAIRED_DEV_INFO,
            command_name=f"Get SpeakerPhone Paired Device Info...",
        )

    def verify_get_paired_device_info(self, response):
        assert 1 == 0, "Not implemented"
