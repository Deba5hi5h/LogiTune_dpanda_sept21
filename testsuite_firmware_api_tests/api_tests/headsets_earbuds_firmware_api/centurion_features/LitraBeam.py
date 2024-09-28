from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.hidpp_commands_raw import GET_BRIGHTNESS_INFO, \
    GET_COLOR_TEMPERATURE_INFO, GET_POWER_STATE, \
    SET_POWER_ON, \
    SET_POWER_OFF, GET_BRIGHTNESS, GET_COLOR_TEMPERATURE, SET_BRIGHTNESS, SET_COLOR_TEMPERATURE


class LitraBeamFeatures:
    """
    API methods to control Litra Beam device.
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def get_power_state(self):
        response = self.centurion.send_litra_beam_command(
            command=GET_POWER_STATE,
            command_name="Get Power state...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_power_state(self, response, value):
        assert int(response[4], 16) == value, Report.logFail(
            f"Litra Beam power state: {response[4]} is not equal to {value}"
        )

        Report.logPass("Brightness value is correct.")

    def set_power_on(self):
        response = self.centurion.send_litra_beam_command(
            command=SET_POWER_ON,
            command_name="Set Power ON...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def set_power_off(self):
        response = self.centurion.send_litra_beam_command(
            command=SET_POWER_OFF,
            command_name="Set Power OFF...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def get_brightness_info(self):
        response = self.centurion.send_litra_beam_command(
            command=GET_BRIGHTNESS_INFO,
            command_name="Get Brightness info...",
        )

        assert response, Report.logFail("Empty response!")

        min_value = int(response[5] + response[6], 16)
        max_value = int(response[7] + response[8], 16)
        resolution = int(response[9], 16)
        max_levels = int(response[10], 16)
        has_events = int(response[11], 16)
        has_linear_levels = int(response[12], 16)
        has_non_linear_levels = int(response[13], 16)
        has_dynamic_maximum = int(response[14], 16)

        return min_value, max_value

    def get_brightness(self):
        response = self.centurion.send_litra_beam_command(
            command=GET_BRIGHTNESS,
            command_name="Get Brightness value...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_brightness(self, response, value):
        value_in_bytes = self._int_to_list_of_bytes(value)
        assert int(response[4], 16) == value_in_bytes[0] and int(response[5], 16) == value_in_bytes[1], Report.logFail(
            f"Litra Beam brightness: {response[4] + response[5]} is not equal to {value_in_bytes}"
        )

        Report.logPass("Brightness value is correct.")

    def set_brightness(self, value):
        value_in_bytes = self._int_to_list_of_bytes(value)
        command = [
            SET_BRIGHTNESS[0],
            SET_BRIGHTNESS[1],
            SET_BRIGHTNESS[2],
            SET_BRIGHTNESS[3],
            value_in_bytes[0],
            value_in_bytes[1],
        ]
        response = self.centurion.send_litra_beam_command(
            command=command,
            command_name=f"Set Brightness to: {value}",
        )
        assert response, Report.logFail("Empty response!")
        return response

    @staticmethod
    def _int_to_list_of_bytes(num: int) -> list:
        """Converts an integer into a list of two bytes."""
        if num > 65535 or num < 0:
            raise ValueError("Number must be between 0 and 65535")
        high_byte = (num & 0xFF00) >> 8
        low_byte = num & 0xFF
        return [high_byte, low_byte]

    def get_color_temperature_info(self):
        response = self.centurion.send_litra_beam_command(
            command=GET_COLOR_TEMPERATURE_INFO,
            command_name="Get Color Temperature info...",
        )

        assert response, Report.logFail("Empty response!")

        min_value = int(response[5] + response[6], 16)
        max_value = int(response[7] + response[8], 16)
        resolution = int(response[9], 16)
        max_levels = int(response[10], 16)
        has_events = int(response[11], 16)
        has_linear_levels = int(response[12], 16)
        has_non_linear_levels = int(response[13], 16)
        has_dynamic_maximum = int(response[14], 16)

        return min_value, max_value

    def get_color_temperature(self):
        response = self.centurion.send_litra_beam_command(
            command=GET_COLOR_TEMPERATURE,
            command_name="Get Color Temperature value...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_color_temperature(self, response, value):
        value_in_bytes = self._int_to_list_of_bytes(value)
        assert int(response[4], 16) == value_in_bytes[0] and int(response[5], 16) == value_in_bytes[1], Report.logFail(
            f"Litra Beam color temperature: {response[4] + response[5]} is not equal to {value_in_bytes}"
        )

        Report.logPass("Brightness value is correct.")

    def set_color_temperature(self, value):
        value_in_bytes = self._int_to_list_of_bytes(value)
        command = [
            SET_COLOR_TEMPERATURE[0],
            SET_COLOR_TEMPERATURE[1],
            SET_COLOR_TEMPERATURE[2],
            SET_COLOR_TEMPERATURE[3],
            value_in_bytes[0],
            value_in_bytes[1],
        ]
        response = self.centurion.send_litra_beam_command(
            command=command,
            command_name=f"Set Color Temperature to: {value}",
        )
        assert response, Report.logFail("Empty response!")
        return response

