from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_GET_TOUCH_SENSOR_STATE, CMD_SET_TOUCH_SENSOR_STATE,
)


class TouchSensorFeature:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0111_iTouchSensor.md
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def set_touch_sensor_state(self, state):
        set_touch_sensor = [
            CMD_SET_TOUCH_SENSOR_STATE[0],
            CMD_SET_TOUCH_SENSOR_STATE[1],
            CMD_SET_TOUCH_SENSOR_STATE[2],
            CMD_SET_TOUCH_SENSOR_STATE[3],
            CMD_SET_TOUCH_SENSOR_STATE[4],
            CMD_SET_TOUCH_SENSOR_STATE[5],
            state,
        ]
        response = self.centurion.send_command(
            feature_name="iTouchSensor",
            command=set_touch_sensor,
            command_name=f"Set Touch Sensor State to: {state}",
        )

        assert len(response) > 0, Report.logFail("Empty response_raw returned for 'Set Touch Sensor State'")
        return response

    def get_touch_sensor_state(self):
        return self.centurion.send_command(
            feature_name="iTouchSensor",
            command=CMD_GET_TOUCH_SENSOR_STATE,
            command_name="Get Touch Sensor State...",
        )

    def verify_get_touch_sensor_state(self, response, state):
        payload_len = f"{3 + 1:02x}"
        touch_sensor_state = f"{state:02x}"
        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            payload_len,
            "00",
            f"{self.centurion.device_features['iTouchSensor'][4]:02x}",
            "0d",
        ]

        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            response_len = 2 + int(payload_len, 16)
            if self.centurion.conn_type == ConnectionType.bt:
                self.centurion.verify_response_crc(response, first_index, response_len)

            assert response[last_index + 1] == touch_sensor_state, Report.logFail(
                f"Touch Sensor State state value {str(response[last_index + 1])} is not equal {touch_sensor_state}"
            )
            Report.logPass("Touch Sensor State value is correct")
        else:
            assert False, Report.logFail("Response pattern not found", screenshot=False)

    def verify_not_supported_touch_sensor_state(self, response):
        CENTPP_INVALID_PARAM = "05"

        sublist = [
            self.centurion.msg_sync_words[1][0],
            self.centurion.msg_sync_words[1][1],
            "05",
            "00",
            "ff",
            f"{self.centurion.device_features['iTouchSensor'][4]:02x}",
            "1d",
        ]
        first_index, last_index = self.centurion.find_sub_list(sublist, response)

        if last_index:
            assert response[last_index + 1] == CENTPP_INVALID_PARAM, Report.logFail(
                f"Returned error code {response[last_index + 1]} for Not supported feature is not equal to {CENTPP_INVALID_PARAM}"
            )
            Report.logPass("Returned error code is correct")
        else:
            assert False, Report.logFail(
                "Error message for not supported Touch Sensor State value received",
                screenshot=False,
            )
