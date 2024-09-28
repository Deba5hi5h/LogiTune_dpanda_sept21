'''
:Module Name: **IPSwitchHelper**
Controlling the IP switch & getting the Status
Curl Command : https://www.digital-loggers.com/curl.html
Git Repo : https://github.com/dwighthubbard/python-dlipower/blob/master/dlipower/dlipower.py

'''
import time

import dlipower
import logging
import common.platform_helper as platform_helper

log = logging.getLogger(__name__)

# IP is the Hostname. Make sure that the IP Switch and
# host computer that runs the tests are in same network.
# IP = "192.168.0.100"
USERNAME = "admin"
PASSWORD = "1234"

device_dict = {
        "tap": {
            "ip": "172.28.213.6",
            "port": 1,
        },
        "slave1": {
            "ip": "172.28.213.6",
            "port": 2,
        },
        "group": {
            "ip": "172.28.213.6",
            "port": 3,
        },
        "avervc520": {
            "ip": "172.28.213.6",
            "port": 4,
        },
        "master": {
            "ip": "172.28.213.6",
            "port": 5,
        },
        "slave2": {
            "ip": "172.28.213.6",
            "port": 6,
        },
        "avervb342": {
            "ip": "172.28.213.6",
            "port": 7,
        },
        "cc3000e": {
            "ip": "172.28.213.6",
            "port": 8,
        },
        "swytch": {
            "ip": "172.28.213.5",
            "port": 1,
        },
        "tapscheduler": {
            "ip": "172.28.213.5",
            "port": 3,
        },
        "scribe": {
            "ip": "172.28.213.5",
            "port": 4,
        },
        "rallybarmini": {
            "ip": "172.28.213.5",
            "port": 5,
        },
        "winmaster2": {
            "ip": "172.28.213.5",
            "port": 6,
        },
        "macmaster2": {
            "ip": "172.28.213.5",
            "port": 7,
        },
        "meetup": {
            "ip": "172.28.213.5",
            "port": 8,
        },
        "yamahaycs700": {
            "ip": "172.28.213.7",
            "port": 1,
        },
        "aver540": {
            "ip": "172.28.213.7",
            "port": 2,
        },
        "ptzpro2": {
            "ip": "172.28.213.7",
            "port": 3,
        },
        "logidock": {
            "ip": "172.28.213.7",
            "port": 4,
        },
        "rallybar": {
            "ip": "172.28.213.7",
            "port": 5,
        },
        "rallycamera": {
            "ip": "172.28.213.7",
            "port": 6,
        },
        "displayhub": {
            "ip": "172.28.213.7",
            "port": 7,
        },
        "tablehub": {
            "ip": "172.28.213.7",
            "port": 8,
        },
        "TuneMacMaster": {
            "ip": "172.28.213.10",
            "port": 2,
        },
        "TuneMacMaster2": {
            "ip": "172.28.213.10",
            "port": 3,
        },
        "TuneMacSlave1": {
            "ip": "172.28.213.10",
            "port": 4,
        },
        "TuneMacSlave2": {
            "ip": "172.28.213.10",
            "port": 6,
        },
        "TuneWinMaster": {
            "ip": "172.28.213.9",
            "port": 1,
        },
        "TuneWinMaster2": {
            "ip": "172.28.213.9",
            "port": 2,
        },
        "TuneWinSlave1": {
            "ip": "172.28.213.9",
            "port": 3,
        },
        "TuneWin11": {
            "ip": "172.28.213.9",
            "port": 4,
        },
        "TuneWin10": {
            "ip": "172.28.213.9",
            "port": 5,
        },
        "TuneWinSlave2": {
            "ip": "172.28.213.9",
            "port": 6,
        },
        "RaidenTapScheduler": {
            "ip": "172.28.213.8",
            "port": 1,
        },
        "RaidenFlexDesk": {
            "ip": "172.28.213.8",
            "port": 2,
        },
        "RaidenRallyBar": {
            "ip": "172.28.213.8",
            "port": 3,
        },
        "RaidenRallyBarMini": {
            "ip": "172.28.213.8",
            "port": 4,
        },
        "RaidenRallyBarMiniDevice": {
            "ip": "172.28.213.8",
            "port": 5,
        },
        "RaidenWinMaster": {
            "ip": "172.28.213.11",
            "port": 1,
        },
        "RaidenTapIP": {
            "ip": "172.28.213.11",
            "port": 2,
        },
        "RaidenRoomMate": {
            "ip": "172.28.213.11",
            "port": 3,
        },
        "RaidenSight": {
            "ip": "172.28.213.11",
            "port": 5,
        }
    }

class IPSwitchHelper:
    '''
    Connect the devices to IP Switch. The values of switch_dict are based on the
    serial number of power socket for the connected device.
    '''

    @staticmethod
    def switch_on(device_name):
        '''
        Switching ON device, the device_name that is set in Power Switch
        :param device_name:
        :return:
        '''
        try:
            switch = dlipower.PowerSwitch(hostname=device_dict[device_name]["ip"],
                                          userid=USERNAME,
                                          password=PASSWORD)
            switch.on(device_dict[device_name]["port"])

        except Exception as e:
            log.error('Failed to switch on: {}'.format(e))
            raise e

    @staticmethod
    def switch_off(device_name):
        '''
        Switching OFF device, the device_name that is set in Power Switch
        :param device_name:
        :return:
        '''
        try:
            switch = dlipower.PowerSwitch(hostname=device_dict[device_name]["ip"],
                                          userid=USERNAME,
                                          password=PASSWORD)
            switch.off(device_dict[device_name]["port"])

        except Exception as e:
            log.error('Failed to switch off: {}'.format(e))
            raise e

    @staticmethod
    def power_cycle_device(device_name: str) -> None:
        """
        Method to power cycle device
        :param: device_name: Name of device that is set in Power Switch
        :return: None
            """
        try:
            switch = dlipower.PowerSwitch(hostname=device_dict[device_name]["ip"],
                                          userid=USERNAME,
                                          password=PASSWORD)
            switch.off(device_dict[device_name]["port"])
            print(f'{device_name} - Powered Off')
            time.sleep(5)
            switch.on(device_dict[device_name]["port"])
            print(f'{device_name} - Powered ON')
        except Exception as e:
            print(f'Failed to restart device: {e}')
            raise e