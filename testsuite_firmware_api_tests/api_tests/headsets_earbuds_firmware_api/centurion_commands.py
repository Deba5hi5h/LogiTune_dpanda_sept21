
import copy
import time
from typing import List, Tuple, Dict, Optional

from extentreport.report import Report

from .crc import calculate_crc, calculate_crc_for_response
from .device_config_bomberman_mono import FEATURES_BOMBERMAN_MONO
from .device_config_bomberman_stereo import FEATURES_BOMBERMAN_STEREO
from .device_config_litra_beam import FEATURES_LITRA_BEAM
from .device_config_quadrun import FEATURES_QUADRUN
from .device_config_zone_950 import FEATURES_ZONE_950
from .device_config_zone_wireless_2 import FEATURES_ZONE_WIRELESS_2
from .device_config_qbert import FEATURES_QBERT
from .device_config_zaxxon import FEATURES_ZAXXON
from .device_config_zone900 import FEATURES_ZONE900
from .device_config_zone_750 import FEATURES_ZONE_750
from .device_config_zone_vibe_100 import FEATURES_ZONE_VIBE_100
from .device_config_zone_vibe_125 import FEATURES_ZONE_VIBE_125
from .device_config_zone_vibe_130 import FEATURES_ZONE_VIBE_130
from .device_config_zone_vibe_wireless import FEATURES_ZONE_VIBE_WIRELESS
from .device_config_zone_wired import FEATURES_ZWIRED
from .device_config_zone_wired_earbuds import FEATURES_ZONE_WIRED_EARBUDS
from .device_config_zonewireless import FEATURES_ZONEWIRELESS
from .device_config_zonewirelessplus import FEATURES_ZONEWIRELESSPLUS
from .device_config_zone_300 import FEATURES_ZONE_300
from .device_config_zone_305 import FEATURES_ZONE_305
from .serial_communication_base import SerialCommunicationBase
from .usb_hid_communication_base import UsbHidCommunicationBase
from ..device_api_names import ConnectionType, DeviceName


class CenturionCommands:
    """ Class consisting methods to communicate with BT or USB device.
    """

    def __init__(self, device_name: str, conn_type: str, com_port: Optional[str] = None):
        self.conn_type = conn_type
        self.device_name = device_name
        self.com_port = com_port
        self.connection_opened = self.open_connection(self.conn_type)
        self.msg_sync_words = self._prepare_message_sync_words(self.conn_type)
        self.device_features = self._prepare_device_features_list(self.device_name)
        self.x = 3

    @staticmethod
    def _prepare_message_sync_words(conn_type: str) -> Tuple[List[int], List[str]]:
        """
        Prepare Message Sync Words

        This method prepares sync words based on the provided connection type.

        Args:
            conn_type (str): The type of connection. Should be one of the following:
                - bt: Bluetooth connection
                - dongle: Dongle connection
                - usb_dock: USB dock connection
                - litra_beam: Litra Beam connection

        Returns:
            Tuple[List[int], List[str]]: A tuple containing two lists:
                - sync_word (List[int]): A list of two integers representing the sync words in hexadecimal format.
                - sync_word_str (List[str]): A list of two strings representing the sync words in hexadecimal format.
        """
        if conn_type == ConnectionType.bt:
            sync_word = [0x13, 0xa0]
        elif conn_type == ConnectionType.dongle:
            sync_word = [0x22, 0xf1]
        elif conn_type == ConnectionType.usb_dock:
            sync_word = [0x1, 0x11]
        elif conn_type == ConnectionType.litra_beam:
            sync_word = [0x10, 0xFF]
        else:
            sync_word = [0x00, 0x00]

        sync_word_str = [f"{sync_word[0]:02x}", f"{sync_word[1]:02x}"]

        return sync_word, sync_word_str

    @staticmethod
    def _prepare_device_features_list(device_name: str) -> Dict:
        """

        Prepare Device Features List

        Parameters:
        - device_name (str): The name of the device for which to prepare the features list.

        Returns:
        - features (Dict): The prepared features list for the given device name.

        """
        all_features = {
            DeviceName.zone_true_wireless: FEATURES_ZAXXON,
            DeviceName.zone_900: FEATURES_ZONE900,
            DeviceName.zone_wireless_plus: FEATURES_ZONEWIRELESSPLUS,
            DeviceName.zone_wireless: FEATURES_ZONEWIRELESS,
            DeviceName.zone_vibe_100: FEATURES_ZONE_VIBE_100,
            DeviceName.zone_vibe_125: FEATURES_ZONE_VIBE_125,
            DeviceName.zone_vibe_130: FEATURES_ZONE_VIBE_130,
            DeviceName.zone_vibe_wireless: FEATURES_ZONE_VIBE_WIRELESS,
            DeviceName.logi_dock: FEATURES_QBERT,
            DeviceName.zone_wired: FEATURES_ZWIRED,
            DeviceName.zone_750: FEATURES_ZONE_750,
            DeviceName.zone_wired_earbuds: FEATURES_ZONE_WIRED_EARBUDS,
            DeviceName.zone_wireless_2: FEATURES_ZONE_WIRELESS_2,
            DeviceName.zone_950: FEATURES_ZONE_950,
            DeviceName.quadrun_wo_headset: FEATURES_QUADRUN,
            DeviceName.litra_beam: FEATURES_LITRA_BEAM,
            DeviceName.zone_300: FEATURES_ZONE_300,
            DeviceName.zone_305: FEATURES_ZONE_305,
            DeviceName.bomberman_mono: FEATURES_BOMBERMAN_MONO,
            DeviceName.bomberman_stereo: FEATURES_BOMBERMAN_STEREO,
        }

        features = all_features.get(device_name, [])
        return features

    def open_connection(self, conn_type: str) -> bool:
        """ Method to open connection with the BT or USB device.

        @param conn_type: describes type of the connection
        @return: True if connection established, False otherwise
        """
        if conn_type == ConnectionType.dongle:
            self.usb_hid_comm_base = UsbHidCommunicationBase(device_name=self.device_name)
            return self.usb_hid_comm_base.open_device_by_path(DeviceName.hid_pid_list[self.device_name], usage_page=65363)
        if conn_type in [ConnectionType.quadrun, ConnectionType.usb_dock]:
            self.usb_hid_comm_base = UsbHidCommunicationBase(device_name=self.device_name)
            return self.usb_hid_comm_base.open_device_by_path(DeviceName.hid_pid_list[self.device_name], usage_page=65440)
        if conn_type == ConnectionType.litra_beam:
            self.usb_hid_comm_base = UsbHidCommunicationBase(device_name=self.device_name)
            return self.usb_hid_comm_base.open_device_by_path(DeviceName.hid_pid_list[self.device_name],
                                                              usage_page=65347)

        self.serial_comm_base = SerialCommunicationBase()
        return self.serial_comm_base.init_port(self.com_port)

    def send_command(self,
                     feature_name: str,
                     command: List[int],
                     command_name: str,
                     is_centippbridge: bool = False,
                     long_response_expected: bool = False) -> Optional[List[str]]:
        """ Method to send Centurion++ command to BT or USB device

        @param feature_name: feature name
        @param command: Centurion++ command to send
        @param command_name: debug text describing the method
        @param is_centippbridge: message to secondary earbud
        @param long_response_expected: is long response expected (for USB
        devices)
        @return:
        """
        time.sleep(1)
        new_command = command.copy()
        new_command[0] = self.msg_sync_words[0][0]
        new_command[1] = self.msg_sync_words[0][1]
        new_command[4] = self.device_features[feature_name][4]
        if self.device_name not in [DeviceName.logi_dock,
                                    DeviceName.zone_wired,
                                    DeviceName.zone_750,
                                    DeviceName.zone_wired_earbuds,
                                    DeviceName.bomberman_mono,
                                    DeviceName.bomberman_stereo]:
            battery_notification_byte = self.device_features['iBatterySOC'][4]
        else:
            battery_notification_byte = None

        if self.connection_opened:
            if self.conn_type == ConnectionType.bt:
                command_to_send = copy.deepcopy(new_command)
                crc_high, crc_low = calculate_crc(new_command)
                command_to_send.append(crc_low)
                command_to_send.append(crc_high)
                response = self.serial_comm_base.send_command_over_serial(
                    command=command_to_send,
                    text=f"{command_name}")
                return response

            command_to_send = copy.deepcopy(new_command)
            response = self.usb_hid_comm_base.send_hid_command(
                command_to_send=command_to_send,
                debug_text=f"{command_name}",
                battery_notification_byte=battery_notification_byte,
                is_centippbridge=is_centippbridge,
                long_response_expected=long_response_expected)

            return response
        return None

    def send_quadrun_command(self,
                             command: List[int],
                             command_name: str) -> Optional[List[str]]:
        """ Method to send Centurion++ command to BT or USB device

        @param command: HID command to send
        @param command_name: debug text describing the method
        @return:
        """
        time.sleep(1)
        new_command = command.copy()

        if self.connection_opened:
            command_to_send = copy.deepcopy(new_command)
            response = self.usb_hid_comm_base.send_hid_command(
                command_to_send=command_to_send,
                debug_text=f"{command_name}",
                battery_notification_byte=0,
                timeout=1000)
            return response
        return None

    def send_litra_beam_command(self,
                             command: List[int],
                             command_name: str) -> Optional[List[str]]:
        """ Method to send Centurion++ command to BT or USB device

        @param command: HID++ command to send
        @param command_name: debug text describing the method
        @return:
        """
        time.sleep(1)
        new_command = command.copy()

        if self.connection_opened:
            command_to_send = copy.deepcopy(new_command)
            response = self.usb_hid_comm_base.send_hid_command(
                command_to_send=command_to_send,
                debug_text=command_name,
                battery_notification_byte=0,
                timeout=1000,
                bufsize=32,
                litra_beam=True)
            return response
        return None

    def close_port(self) -> None:
        """ Method to close connection with USB device

        @return: None
        """
        if self.connection_opened:
            if self.conn_type == ConnectionType.bt:
                self.serial_comm_base.exit_port(False, True)
            else:
                self.usb_hid_comm_base.close_device(False, True)

    @staticmethod
    def find_sub_list(submessage: List[str], message: List[str]):
        """ Method to find a message by its sub-message

        @param submessage: part of the message to find
        @param message: original message
        @return:
        """
        sll = len(submessage)
        for ind in (i for i, e in enumerate(message) if e == submessage[0]):
            if message[ind:ind + sll] == submessage:
                return ind, ind + sll - 1
        return None, None

    @staticmethod
    def verify_response_crc(response_raw: List[int], first_index: int,
                            response_len: int) -> None:
        """ Method to verify message CRC.

        @param response_raw: Message received from the device
        @param first_index: first index of the final message
        @param response_len: lenght of the response
        @return: None
        """
        # print(f"response_raw: {response_raw}")
        # print(f"first_index: {first_index}")
        # print(f"response_len: {response_len}")
        res_crc_high, res_crc_low = calculate_crc_for_response(
            response_raw[first_index:first_index + response_len + 1])
        assert response_raw[first_index + response_len + 1] == f"{res_crc_low:02x}", \
            f"Low crc byte {response_raw[first_index + response_len + 1]} is " \
           f"not equal to {hex(res_crc_low)}"

        assert response_raw[first_index + response_len + 2] == f"{res_crc_high:02x}", \
            f"High crc byte {response_raw[first_index + response_len + 2]} " \
            f"is not equal to {hex(res_crc_high)}"
        Report.logPass("Response CRC is correct", screenshot=False)
