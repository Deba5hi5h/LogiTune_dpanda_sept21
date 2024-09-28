# -*- coding: utf-8 -*-
import time
import serial
import serial.tools.list_ports
from extentreport.report import Report

# Acroname relay cmd in hex
ry_port_1_on = [0x65]
ry_port_1_off = [0x6F]
ry_port_2_on = [0x66]
ry_port_2_off = [0x70]
ry_port_3_on = [0x67]
ry_port_3_off = [0x71]
ry_port_4_on = [0x68]
ry_port_4_off = [0x72]
ry_port_5_on = [0x69]
ry_port_5_off = [0x73]
ry_port_6_on = [0x6A]
ry_port_6_off = [0x74]
ry_port_7_on = [0x6B]
ry_port_7_off = [0x75]
ry_port_8_on = [0x6C]
ry_port_8_off = [0x76]
ry_port_all_on = [0x64]
ry_port_all_off = [0x6E]
ry_get_serial_number = [0x38]  # return 8 bytes of ASCII


class GenericRelayControl():
    """
    A class contains methods to control Acroname relay board
    It's to mimic the behavior like pressing / pushing buttons on devices
    Communicate with relay board through COM port
    It needs to pre-configure corresponding ports on relay connected to the specific button in properties.LOCAL
    """

    def __init__(self):
        """
        Initialization method for Generic relay control.
        :param none
        :return none
        """
        self.ser = None

    def get_relay_com_port(self, device_relay_serial_number: int) -> str:
        """
        Method to get COM port of relay connected to devices
        :param device_relay_serial_number: serial number of the relay connected to DUT
        :return relay_com_port
        """
        # Scan all ports
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            Report.logInfo(f"{port}: {desc} [{hwid}]")
            if ("USB Serial Device" in desc) or ("USB-RLY08" in desc):
                Report.logInfo(f"Open serial port {port} and read the serial number of the relay connected to device")
                ser = serial.Serial(port=port, baudrate=9600, bytesize=8, parity='N', timeout=1)
                # Read serial number from relay board
                ser.write(ry_get_serial_number)
                line = ser.readline()
                line = line.decode('utf-8')
                line = line[0:7]
                line = int(line, 16)
                ser.read_all()
                # Return COM port connected to DUT
                if str(line) == str(device_relay_serial_number):
                    relay_com_port = port
                    Report.logInfo(f"COM port of relay connected to device is {relay_com_port}")
                    return relay_com_port
            else:
                Report.logInfo(f"String USB Serial Device is not found in description of COM port list")
                continue

    def connect_relay(self, relay_com_port: str) -> None:
        """
        Method to connect to COM port of relay connected to devices
        :param relay_com_port: COM port of the relay connected to PC
        :return relay_com_port
        """
        Report.logInfo(f"Connect to COM port: {relay_com_port}")
        self.ser = serial.Serial(port=relay_com_port, baudrate=9600, bytesize=8, parity='N', timeout=1)

    def disconnect_relay(self) -> None:
        """
        Method to close communication with COM port of relay connected to devices
        :param none
        :return none
        """
        Report.logInfo(f"Close COM port communication")
        self.ser.close()

    def press_btn(self, relay_port: str, press_time: float) -> None:
        """
        Method to press the button of devices
        :param relay_port: port on relay connected to the specific button of device
        :param press_time: time duration to press the button
        :return none
        """
        Report.logInfo(f"Press button with relay port: {relay_port}")
        relay_port = int(relay_port)
        if relay_port == 1:
            self.ser.write(ry_port_1_on)
            time.sleep(press_time)
            self.ser.write(ry_port_1_off)
        elif relay_port == 2:
            self.ser.write(ry_port_2_on)
            time.sleep(press_time)
            self.ser.write(ry_port_2_off)
        elif relay_port == 3:
            self.ser.write(ry_port_3_on)
            time.sleep(press_time)
            self.ser.write(ry_port_3_off)
        elif relay_port == 4:
            self.ser.write(ry_port_4_on)
            time.sleep(press_time)
            self.ser.write(ry_port_4_off)
        elif relay_port == 5:
            self.ser.write(ry_port_5_on)
            time.sleep(press_time)
            self.ser.write(ry_port_5_off)
        elif relay_port == 6:
            self.ser.write(ry_port_6_on)
            time.sleep(press_time)
            self.ser.write(ry_port_6_off)
        elif relay_port == 7:
            self.ser.write(ry_port_7_on)
            time.sleep(press_time)
            self.ser.write(ry_port_7_off)
        elif relay_port == 8:
            self.ser.write(ry_port_8_on)
            time.sleep(press_time)
            self.ser.write(ry_port_8_off)
        else:
            Report.logInfo(f"Unable to press button with relay port: {relay_port}")

    def press_btn_all_ports_on(self) -> None:
        """
        Method to make all relay ports power on
        :param none
        :return none
        """
        Report.logInfo("Relay port all on")
        self.ser.write(ry_port_all_on)

    def press_btn_all_ports_off(self) -> None:
        """
        Method to make all relay ports power off
        :param none
        :return none
        """
        Report.logInfo("Relay port all off")
        self.ser.write(ry_port_all_off)
