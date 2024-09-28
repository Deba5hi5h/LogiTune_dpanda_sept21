import sys
from typing import List

import serial

from common.platform_helper import get_custom_platform
from extentreport.report import Report


class SerialCommunicationBase:
    """ Base to class to communicate via COM port.

    """
    def __init__(self):
        self.port_assigned = None

    def init_port(self, port: str) -> bool:
        """ Initialize serial port

        @param port: port number
        @return:
        """
        if self.port_assigned is not None:
            self.port_assigned.close()
            self.port_assigned = None

        try:
            self.port_assigned = serial.Serial()
            self.port_assigned.port = port
            self.port_assigned.baudrate = 115200
            self.port_assigned.bytesize = serial.EIGHTBITS
            self.port_assigned.parity = serial.PARITY_NONE
            self.port_assigned.stopbits = serial.STOPBITS_ONE
            self.port_assigned.rtscts = True
            self.port_assigned.timeout = 1
            if get_custom_platform() == 'macos':
                self.port_assigned.timeout = 2
            print(f"Is the port opened: {self.port_assigned.is_open}")
            if self.port_assigned.is_open:
                self.port_assigned.close()
            self.port_assigned.open()

            self.port_assigned.flushInput()
            self.port_assigned.flushOutput()
            return True

        except serial.SerialException:
            Report.logException('Could not open serial port!')
            Report.logException('Make sure that you have a SPP connection '
                                'between the Test PC and DUT and the comport '
                                'is selected properly')

            self.exit_port(True, False)
            return False

    def exit_port(self, error: bool, is_port_opened: bool) -> None:
        """ Method to close the COM port.

        @param error: indicate if COM port error occurred
        @param is_port_opened: is com port opened
        @return: None
        """
        if is_port_opened:
            self.port_assigned.close()
        if error:
            sys.exit(1)

    def send_command_over_serial(self,
                                 command: List[int],
                                 text: str) -> List[str]:
        """ Send command over serial port

        @param command: Command to send
        @param text: debug text
        @return:
        """
        Report.logInfo(f"Command: {text}")
        print_data = []
        for value in command:
            print_data.append(hex(value))
        Report.logInfo(f"Sending -> {print_data}")
        self.port_assigned.write(command)
        return self.wait_for_response()

    def wait_for_response(self) -> List[str]:
        """ Wait for HCI response_raw from controller

        @return: received message on the COM port
        """
        data = self.port_assigned.read(256)
        print_data = []
        for char in data:
            print_data.append(hex(char))
        Report.logInfo(f"Response -> {print_data}")
        response = []
        for char in data:
            response.append(f"{char:02x}")
        return response
