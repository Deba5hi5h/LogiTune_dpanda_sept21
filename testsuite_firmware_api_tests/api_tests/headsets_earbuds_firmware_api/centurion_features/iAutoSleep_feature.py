from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_SLEEP_TIMER,
    CMD_SET_SLEEP_TIMER,
    CMD_START_CUSTOM_AMBIENT_LED,
)


class AutoSleepFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0108_iAutoSleep.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_sleep_timer(self):
        command_to_send = [
            CMD_GET_SLEEP_TIMER[0],
            CMD_GET_SLEEP_TIMER[1],
            CMD_GET_SLEEP_TIMER[2],
            CMD_GET_SLEEP_TIMER[3],
            CMD_GET_SLEEP_TIMER[4],
            CMD_GET_SLEEP_TIMER[5],
        ]
        return self.centurion.send_command(
            feature_name="iAutoSleep",
            command=command_to_send,
            command_name="Get Sleep Timer",
        )

    def verify_sleep_timer(self, response, timer):
        payload_len = f"{4:02x}"
        sleep_timer = f"{timer:02x}"
        sublist = [
            "00",
            f"{self.centurion.device_features['iAutoSleep'][4]:02x}",
            "0d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)
        if last_index:
            response_len = 2 + int(payload_len, 16)
            # if self.centurion.conn_type == ConnectionType.bt:
            #     self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == sleep_timer, Report.logFail(
                f"Sleep timer{response[last_index + 1]} is not equal to {sleep_timer}"
            )
            Report.logPass("Returned value for a sleep time is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def set_sleep_timer(self, sleep_min):
        set_sleep_timer_cmd = [
            CMD_SET_SLEEP_TIMER[0],
            CMD_SET_SLEEP_TIMER[1],
            CMD_SET_SLEEP_TIMER[2],
            CMD_SET_SLEEP_TIMER[3],
            CMD_SET_SLEEP_TIMER[4],
            CMD_SET_SLEEP_TIMER[5],
            sleep_min,
        ]
        response = self.centurion.send_command(
            feature_name="iAutoSleep",
            command=set_sleep_timer_cmd,
            command_name=f"Set Sleep Timer to {sleep_min}",
        )

        assert len(response) > 0, Report.logException("Empty response_raw returned for set 'Set Sleep Timer'")
        assert "ff" not in response, Report.logFail("Error returned for 'Set Sleep Timer'")
        return response

    def set_never_sleep_timer(self) -> None:
        """Method to set Sleep Timeout equal to Never (0).

        @return: None
        """
        self.set_sleep_timer(0)
        response = self.get_sleep_timer()
        self.verify_sleep_timer(response, 0)
