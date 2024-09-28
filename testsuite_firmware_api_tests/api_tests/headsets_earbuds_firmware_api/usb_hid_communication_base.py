import sys
import time
from typing import List

import hid
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import DeviceName


class UsbHidCommunicationBase:

    def __init__(self, device_name: str):
        self.device = None
        self.device_name = device_name

    def open_device_by_path(self, pid: int, usage_page: int) -> bool:
        """ Open usb hid connection to device by device path
        @param pid: USB Product id
        @param usage_page: Usage id number for usb device to open
        @return: True if connection open, otherwise False
        """
        dev_path = None

        try:
            all_devices = hid.enumerate()
            all_devices.sort(
                key=lambda x:
                (x['vendor_id'], x['product_id'], x.get('usage', 0)),
                reverse=True)
            for d in all_devices:
                if d['product_id'] == pid and (pid == 0xAF0 or pid == 0xAF1):
                    if d['usage_page'] == usage_page and self.device_name in d['product_string']:
                        dev_path = d['path']
                elif d['usage_page'] == usage_page and d['product_id'] == pid:
                    dev_path = d['path']

            if dev_path:
                return self._open_device_path(dev_path)

            Report.logException('Could not find device usb path')
            return False

        except Exception as ex:
            Report.logException(str(ex))
            raise ex

    def _open_device_path(self, dev_path, retry: int = 0, max_retries: int = 8):
        try:
            # Report.logInfo(f"Open device hid path. Retry no: {retry + 1}.")
            print(f"Open device hid path. Retry no: {retry + 1}.")
            self.device = hid.device()
            self.device.open_path(dev_path)
            return True
        except IOError as er:
            if retry <= max_retries:
                retry += 1
                time.sleep(2)
                return self._open_device_path(dev_path, retry)
            else:
                # Report.logException(f'Could not open device usb path: {er}')
                print(f'Could not open device usb path: {er}')
                self.close_device(True, False)
                return False


    def close_device(self, error: bool, device_open: bool) -> None:
        """ Close connection with USB HID device.

        @param error: True if error in usb, False if no errors
        @param device_open: True if connection opened, otherwise False
        @return: None
        """
        if device_open:
            self.device.close()
        if error:
            sys.exit(1)

    def send_hid_command(self,
                         command_to_send: List[int],
                         debug_text: str,
                         battery_notification_byte: int,
                         is_centippbridge: bool = False,
                         long_response_expected: bool = False,
                         timeout: int = 3000,
                         bufsize: int = 64,
                         litra_beam: bool = False) -> List[str]:
        """ Method allowing to send message to usb device.

        @param command_to_send: command to send to usb device
        @param debug_text: debug text to print in logger
        @param is_centippbridge: True if connection to secondary earbud
        @param long_response_expected: True if long response expected
        @return: received message from usb device
        """

        Report.logInfo(f"Command: {debug_text}")
        buf = [0] * bufsize

        for i in range(0, min(bufsize, len(command_to_send))):
            buf[i] = command_to_send[i]

        buf_raw_hex = []
        for value in command_to_send:
            buf_raw_hex.append(hex(value))
        Report.logInfo(f"Sending -> {buf_raw_hex}")

        try:
            self.device.write(buf)
            if litra_beam:
                return self.read_hid_response(timeout)
            if long_response_expected:
                return self.read_long_response(battery_notification_byte=battery_notification_byte,
                                               is_centippbridge=is_centippbridge)
            return self.read_response(battery_notification_byte=battery_notification_byte,
                                      is_centippbridge=is_centippbridge, timeout=timeout)
        except OSError as er:
            Report.logException(f"Send out report error: {er}")

    def write_hid_command(self,
                         command_to_send: List[int],
                         debug_text: str,
                         bufsize: int = 64) -> None:
        """ Method allowing to send message to usb device.

        @param command_to_send: command to send to usb device
        @param debug_text: debug text to print in logger
        @param is_centippbridge: True if connection to secondary earbud
        @param long_response_expected: True if long response expected
        @return: received message from usb device
        """

        Report.logInfo(f"Command: {debug_text}")
        buf = [0] * bufsize

        for i in range(0, min(bufsize, len(command_to_send))):
            buf[i] = command_to_send[i]

        buf_raw_hex = []
        for value in command_to_send:
            buf_raw_hex.append(hex(value))
        Report.logInfo(f"Sending -> {buf_raw_hex}")

        try:
            self.device.write(buf)
        except OSError as er:
            Report.logException(f"Send out report error: {er}")

    def read_hid_response(self, timeout: int = 3000) -> List[str]:
        bufsize = 64
        timeout_ms = timeout
        response = []
        response_try = 0
        try:

            is_response = False
            while not is_response:
                buf = self.device.read(bufsize, timeout_ms)
                response_try += 1
                # print(f'buf: {buf}')  # debug message

                if buf:
                    for char in buf:
                        response.append(f"{char:02x}")
                        is_response = True

                if response_try >= 10:
                    return response

            is_data = True
            while is_data:
                buf = self.device.read(bufsize, timeout_ms)
                # print(f'bufX: {buf}') # debug message
                if len(buf) == 0:
                    break

                for char in buf:
                    response.append(f"{char:02x}")

            Report.logInfo(f"Response -> {response}")

            return response

        except OSError as er:
            Report.logException(f"Get response error: {er}")


    def read_response(self, battery_notification_byte: int,
                      is_centippbridge: bool = False,
                      timeout: int = 3000) -> List[str]:
        """ Method to read response from usb device

        @param is_centippbridge: True if connection to secondary earbud
        @return: received message from usb device
        """
        bufsize = 64
        timeout_ms = timeout
        response = []
        response_try = 0
        try:

            is_response = False
            while not is_response:
                buf = self.device.read(bufsize, timeout_ms)
                response_try += 1
                print(f'buf: {buf}')  # debug message

                if buf and not self._is_mac_sync_bytes(buf):
                    if not (self._is_battery_notification(buf, battery_notification_byte) or self._is_anc_notification(
                            buf) or self._is_bt_conn_notification(buf)):
                        for char in buf[:buf[2] + 2 + 1]:
                            response.append(f"{char:02x}")
                            is_response = True

                if response_try >= 10:
                    return response

            is_data = True
            while is_data:
                buf = self.device.read(bufsize, timeout_ms)
                # print(f'bufX: {buf}') # debug message
                if len(buf) == 0:
                    break

                if buf and not self._is_mac_sync_bytes(buf):
                    if not (self._is_battery_notification(buf, battery_notification_byte) or self._is_anc_notification(
                            buf) or self._is_bt_conn_notification(buf)):
                        if is_centippbridge:
                            for char in buf[:buf[2] + 2 + 1]:
                                response.append(f"{char:02x}")
                        else:
                            for char in buf[3:buf[2] + 2 + 1]:
                                response.append(f"{char:02x}")

                if len(response) >= 6 and self._is_mac_sync_bytes(buf):
                    break

            Report.logInfo(f"Response -> {response}")

            return response

        except OSError as er:
            Report.logException(f"Get response error: {er}")

    def read_long_response(self, battery_notification_byte: int,
                           is_centippbridge: bool = False) -> List[str]:
        """ Method to read long response (in chunks) from usb device

        @param is_centippbridge: True if connection to secondary earbud
        @return: received message from usb device
        """
        bufsize = 256
        timeout_ms = 3000
        response = []
        data_len = None
        bad_bytes_count = 0

        try:
            is_response = False
            while not is_response:
                buf = self.device.read(bufsize, timeout_ms)
                # print(f'buf: {buf}') # debug message

                if not self._is_mac_sync_bytes(buf):
                    if not self._is_battery_notification(buf, battery_notification_byte):
                        for char in buf[:buf[2] + 2 + 1]:
                            response.append(f"{char:02x}")
                            data_len = buf[2]
                            is_response = True

            is_data = True
            while is_data:

                buf = self.device.read(bufsize, timeout_ms)
                # print(f'bufX: {buf}') # debug message
                if len(buf) == 0:
                    break

                if not self._is_mac_sync_bytes(buf):
                    if not self._is_battery_notification(buf, battery_notification_byte):
                        if is_centippbridge:
                            for char in buf[:buf[2] + 2 + 1]:
                                response.append(f"{char:02x}")
                        else:
                            for char in buf[4:buf[2] + 2 + 1]:
                                response.append(f"{char:02x}")
                        data_len += buf[2] - 1
                else:
                    bad_bytes_count += 1

                # print(f'bad_bytes_count: {bad_bytes_count}') # debug message
                if bad_bytes_count >= 10:
                    break

            response[2] = f"{data_len:02x}"
            Report.logInfo(f"Response -> {response}")

            return response
        except OSError as er:
            Report.logException(f"Get response error: {er}")

    def _is_battery_notification(self, data: List[int], battery_notification_byte: int) -> bool:
        """ Method to find if battery notification in inside the response
        message.

        @param data: Device response
        @param battery_notification_byte: feature id for battery notification
        @return: True if battery notification include, False otherwise
        """
        if self.device_name not in [DeviceName.logi_dock,
                                    DeviceName.zone_wired,
                                    DeviceName.zone_750,
                                    DeviceName.zone_wired_earbuds]:

            battery_event = [34, 241, 6, 0, battery_notification_byte, 0]
            secondary_earbuds_status = [34, 241, 11, 0, 2, 16, 0, 6, 0, 3, 0]

            t_data = []
            for chunk in data:
                t_data.append(f"{chunk:02x}")

            if self.device_name != DeviceName.zone_true_wireless:
                status = self._find_sub_list(battery_event, data)
                return status

            status = self._find_sub_list(battery_event, data)
            status_sec = self._find_sub_list(secondary_earbuds_status, data)
            return status or status_sec
        return False

    def _is_bt_conn_notification(self, data: List[int]) -> bool:
        """ Method to find if bt conn info in inside the response
        message.

        @param data: Device response
        @param bt_conn_info_notification_byte: feature id for battery notification
        @return: True if battery notification include, False otherwise
        """
        if self.device_name not in [DeviceName.logi_dock,
                                    DeviceName.zone_wired,
                                    DeviceName.zone_750,
                                    DeviceName.zone_wired_earbuds,
                                    DeviceName.zone_vibe_wireless,
                                    DeviceName.zone_vibe_130]:

            battery_event = [34, 241, 10, 0, 10]

            t_data = []
            for chunk in data:
                t_data.append(f"{chunk:02x}")

            if self.device_name != DeviceName.zone_true_wireless:
                status = self._find_sub_list(battery_event, data)
                return status

            status = self._find_sub_list(battery_event, data)
            return status
        return False

    def _is_anc_notification(self, data: List[int]) -> bool:
        """ Method to find if battery notification in inside the response
        message.

        @param data: Device responce
        @return: True if battery notification include, False otherwise
        """
        if self.device_name == DeviceName.zone_true_wireless:

            anc_notification_byte = 7

            battery_event = [34, 241, 4, 0, anc_notification_byte, 16]

            t_data = []
            for chunk in data:
                t_data.append(f"{chunk:02x}")

            status = self._find_sub_list(battery_event, data)
            return status
        return False

    @staticmethod
    def _find_sub_list(submessage, message):
        """ Method to find a message by its sub-message

        @param submessage: part of the message to find
        @param message: original message
        @return: True is submessage found in the original message
        """
        sll = len(submessage)
        for ind in (i for i, e in enumerate(message) if e == submessage[0]):
            if message[ind:ind + sll] == submessage:
                return True
        return False

    def _is_mac_sync_bytes(self, buf: List[int]):
        """ Check for some additional bytes which are visible only on M1 machine.
        """
        return buf in [[155, 0], [155, 1], [1, 0, 0], [1, 0, 1]]

    def power_on(self, pid: int, usage_page: int) -> None:
        """Method to turn headset power on via hid command

        @param pid: product id
        @param usage_page: usage page
        """
        # 101601
        command_power_on = [0x10, 0x16, 0x01]
        self.open_device_by_path(pid=pid, usage_page=usage_page)
        self.send_hid_command(command_to_send=command_power_on,
                              debug_text="power on",
                              battery_notification_byte=0,
                              is_centippbridge=False)

    def write_power_on_command(self, pid: int, usage_page: int) -> None:
        """Method to turn headset power on via hid command

        @param pid: product id
        @param usage_page: usage page
        """
        # 101601
        command_power_on = [0x10, 0x16, 0x01]
        self.open_device_by_path(pid=pid, usage_page=usage_page)
        self.write_hid_command(command_to_send=command_power_on,
                              debug_text="write power on comamnd")

    def power_off(self, pid: int, usage_page: int) -> None:
        """Method to turn headset power off via hid command

        @param pid: product id
        @param usage_page: usage page
        """
        # 101600
        command_power_off = [0x10, 0x16, 0x00]
        self.open_device_by_path(pid=pid, usage_page=usage_page)
        self.send_hid_command(command_to_send=command_power_off,
                              debug_text="power off",
                              battery_notification_byte=0,
                              is_centippbridge=False)

    def pairing(self, pid: int, usage_page: int) -> None:
        """Method to enter pairing mode via hid command

        @param pid: product id
        @param usage_page: usage page
        """
        # 101500
        command_pairing = [0x10, 0x15, 0x00]
        self.open_device_by_path(pid=pid, usage_page=usage_page)
        self.send_hid_command(command_to_send=command_pairing,
                              debug_text="pairing",
                              battery_notification_byte=0,
                              is_centippbridge=False)
