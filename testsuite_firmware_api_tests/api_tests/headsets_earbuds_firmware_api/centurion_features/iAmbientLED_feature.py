from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_CANCEL_AMBIENT_LED,
    CMD_START_AMBIENT_LED,
    CMD_START_CUSTOM_AMBIENT_LED,
)


class AmbientLEDFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x010D_iAmbientLED.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_start_ambient_led(self):
        notification_action = 0x13
        red = 0x33
        green = 0x11
        blue = 0xFF
        duration = [0x00, 0x00, 0x27, 0x10]
        period = [0x13, 0x88]

        set_earcon_state = [
            CMD_START_AMBIENT_LED[0],
            CMD_START_AMBIENT_LED[2],
            CMD_START_AMBIENT_LED[1],
            CMD_START_AMBIENT_LED[3],
            CMD_START_AMBIENT_LED[4],
            CMD_START_AMBIENT_LED[5],
            notification_action,
            red,
            green,
            blue,
            duration[0],
            duration[1],
            duration[2],
            duration[3],
            period[0],
            period[1],
        ]
        response = self.centurion.send_command(
            feature_name="iAmbientLED",
            command=set_earcon_state,
            command_name=f"Set Start Ambient LED state to: notification_action:{notification_action},"
            f"red: {red},"
            f"green: {green},"
            f"blue: {blue},"
            f"duration: {duration},"
            f"period: {period}",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Ambient LED State'")
        return response

    def set_cancel_ambient_led(self, cmd_id_hex):

        cmd_id = int(cmd_id_hex, 16)

        set_earcon_state = [
            CMD_CANCEL_AMBIENT_LED[0],
            CMD_CANCEL_AMBIENT_LED[1],
            CMD_CANCEL_AMBIENT_LED[2],
            CMD_CANCEL_AMBIENT_LED[3],
            CMD_CANCEL_AMBIENT_LED[4],
            CMD_CANCEL_AMBIENT_LED[5],
            cmd_id,
        ]
        response = self.centurion.send_command(
            feature_name="iAmbientLED",
            command=set_earcon_state,
            command_name=f"Set Cancel Ambient LED for ID:{cmd_id_hex}",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Ambient LED State'")
        return response

    def set_start_custom_ambient_led(self):
        command_to_send = [
            CMD_START_CUSTOM_AMBIENT_LED[0],
            CMD_START_CUSTOM_AMBIENT_LED[1],
            CMD_START_CUSTOM_AMBIENT_LED[2],
            CMD_START_CUSTOM_AMBIENT_LED[3],
            CMD_START_CUSTOM_AMBIENT_LED[4],
            CMD_START_CUSTOM_AMBIENT_LED[5],
        ]
        return self.centurion.send_command(
            feature_name="iAmbientLED",
            command=command_to_send,
            command_name="Start Custome Ambient mode...",
        )
