from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_REG_APP_IDS,
    CMD_GET_UNMUTE_MODE,
    CMD_GET_VIDEO_MUTE_STATE,
    CMD_SET_UNMUTE_MODE,
)


class VideoMuteFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x010E_iVideoMute.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_unmute_mode(self, mode):
        return self.centurion.send_command(
            feature_name="iVideoMute",
            command=CMD_SET_UNMUTE_MODE,
            command_name=f"Set Unmute Mode to {mode}...",
        )

    def get_unmute_mode(self):
        return self.centurion.send_command(
            feature_name="iVideoMute",
            command=CMD_GET_UNMUTE_MODE,
            command_name="Get Unmute mode...",
        )

    def verify_get_unumte_mode(self, response):
        assert 1 == 0

    def get_registered_app_ids(self):
        return self.centurion.send_command(
            feature_name="iVideoMute",
            command=CMD_GET_REG_APP_IDS,
            command_name="Get Unmute mode...",
        )

    def verify_get_registered_app_ids(self, response):
        assert 1 == 0

    def get_video_mute_state(self):
        return self.centurion.send_command(
            feature_name="iVideoMute",
            command=CMD_GET_VIDEO_MUTE_STATE,
            command_name="Get Unmute mode...",
        )

    def verify_get_video_mute_state(self, response):
        assert 1 == 0
