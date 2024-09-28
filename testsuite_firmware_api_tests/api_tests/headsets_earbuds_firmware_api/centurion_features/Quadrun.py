from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.hid_commands_raw import \
    CMD_BT_STATUS_INDICATION, CMD_CLEAR_PAGE, CMD_CLEAR_PDL, CMD_CONNECT_DEVICE, CMD_DISCONNECT_DEVICE, \
    CMD_ENTER_DFU_MODE, CMD_EXIT_DEVICE_TEST_MODE, \
    CMD_GET_COLOR_CODE, \
    CMD_GET_LED_DUTY_CYCLE, \
    CMD_GET_PRODUCT_SERIAL_NUMBER, \
    CMD_GET_QUADRUN_FW_VERSION, CMD_GET_STATUS_REQUEST, \
    CMD_LOCK_DEVICE, CMD_READ_BT_ADDR_OF_PAIRED_HEADSET, CMD_SET_COLOR_CODE, CMD_SET_DEVICE_TEST_MODE, \
    CMD_SET_PAGE_SCAN, \
    CMD_SET_PAIRING_MODE, CMD_SET_VENDOR_MODE, CMD_UNLOCK_DEVICE


class QuadrunFeatures:
    """
    https://docs.google.com/document/d/1VIiN1xXC8lPlF2GADMH6rbtK1TcDcVqFA2O28dAhKK0/edit
    """

    def __init__(self, centurion):
        self.centurion = centurion

    def verify_command_confirmation(self, response):
        ack = ['03', '00', '00']

        first, last = self.centurion.find_sub_list(ack, response)

        assert first is not None and last is not None, Report.logException("Command confirmation not found in response.")

    def get_quadrun_fw_version(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_GET_QUADRUN_FW_VERSION,
            command_name="Start Quadrun FW version...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_firmware_version(self, response, fw_version):
        dongle_ver_len = len(fw_version.split("."))

        dongle_fw_ver_response = []
        for i in range(1, 1 + dongle_ver_len):
            dongle_fw_ver_response.append(response[i].lstrip('0'))
        assert ".".join(dongle_fw_ver_response) == fw_version, Report.logFail(
            f'{".".join(dongle_fw_ver_response)} is not equal to {fw_version}'
        )
        Report.logPass("Dongle FW version value is correct")

    def get_led_cycle_duty(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_GET_LED_DUTY_CYCLE,
            command_name="GET Led cycle duty...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def clear_pdl(self):
        return self.centurion.send_quadrun_command(
            command=CMD_CLEAR_PDL,
            command_name="Clear PDL...",
        )

    def read_bt_address_of_paired_headset(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_READ_BT_ADDR_OF_PAIRED_HEADSET,
            command_name="Read BT Address of paired headset...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def get_status_request(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_GET_STATUS_REQUEST,
            command_name="Get status request...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def get_color_code(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_GET_COLOR_CODE,
            command_name="Get color code...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_get_color_code(self, response, color_code):
        assert int(response[4]) == color_code[0] and int(response[5]) == color_code[1], Report.logFail(
            f"Color Code for Quadrun dongle: {response[4] + response[5]} is not equal to {color_code}"
        )

        Report.logPass("Color code value is correct")

    def get_product_serial_number(self):
        response =  self.centurion.send_quadrun_command(
            command=CMD_GET_PRODUCT_SERIAL_NUMBER,
            command_name="Get product serial number...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_get_product_serial_number(self, response, serial_number):
        serial_number_response = []
        for i in range(3, 3 + len(serial_number)):
            tmp = bytes.fromhex(response[i])
            serial_number_response.append(tmp.decode("ASCII"))
        assert "".join(serial_number_response) == serial_number, Report.logFail(
            f'{"".join(serial_number_response)} is not equal to {serial_number}'
        )
        Report.logPass("Serial number value is correct")

    def set_device_test_mode(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_SET_DEVICE_TEST_MODE,
            command_name="Set device test mode...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def exit_device_test_mode(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_EXIT_DEVICE_TEST_MODE,
            command_name="Exit device test mode...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def bt_status_indication(self, state):
        command = [
            CMD_BT_STATUS_INDICATION[0],
            CMD_BT_STATUS_INDICATION[1],
            state,
        ]
        response = self.centurion.send_quadrun_command(
            command=command,
            command_name=f"BT Status indication: {state}",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def set_pairing_mode(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_SET_PAIRING_MODE,
            command_name="Set pairing mode...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_set_pairing_mode(self, response):
        ack = ['02', '00', '04']

        first, last = self.centurion.find_sub_list(ack, response)

        assert first is not None and last is not None, Report.logException(
            "Command confirmation not found in response.")

    def set_page_scan(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_SET_PAGE_SCAN,
            command_name="Set page scan...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def verify_set_page_scan(self, response):
        ack = ['02', '00']

        first, last = self.centurion.find_sub_list(ack, response)

        assert first is not None and last is not None, Report.logException(
            "Command confirmation not found in response.")

    def clear_page(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_CLEAR_PAGE,
            command_name="Clear page...",
        )

        assert response, Report.logFail("Empty response!")
        return response

    def disconnect_device(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_DISCONNECT_DEVICE,
            command_name="Disconnect device...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def connect_device(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_CONNECT_DEVICE,
            command_name="Connect device...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def set_color_code(self, color_name, color_code):
        command = [
            CMD_SET_COLOR_CODE[0],
            CMD_SET_COLOR_CODE[1],
            CMD_SET_COLOR_CODE[2],
            CMD_SET_COLOR_CODE[3],
            color_code[0],
            color_code[1]
        ]
        response = self.centurion.send_quadrun_command(
            command=command,
            command_name=f"Set color {color_name}: {color_code}",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def lock_device(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_LOCK_DEVICE,
            command_name="Lock device...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def unlock_device(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_UNLOCK_DEVICE,
            command_name="Unlock device...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def vendor_mode(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_SET_VENDOR_MODE,
            command_name="Set vendor mode...",
        )
        assert response, Report.logFail("Empty response!")
        return response

    def enter_dfu_mode(self):
        response = self.centurion.send_quadrun_command(
            command=CMD_ENTER_DFU_MODE,
            command_name="Enter DFU mode...",
        )
        assert response, Report.logFail("Empty response!")
        return response
