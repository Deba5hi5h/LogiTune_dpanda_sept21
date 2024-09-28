import subprocess
import argparse
import time
import dlipower

#Constants
USERNAME = "admin"
PASSWORD = "1234"

#Device Dictionary
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

def power_cycle_device(device_name: str)->None:
    """
    Method to power cycle device
    :param: device_name: Name of device
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

parser = argparse.ArgumentParser()
parser.add_argument("-d","--device", help="Device Name")
args = parser.parse_args()
device_list = str(args.device).split(',')
for device in device_list:
    device = device.replace(' ', '').lower()
    if device == 'rally':
        power_cycle_device('tablehub')
        power_cycle_device('displayhub')
    else:
        power_cycle_device(device)
