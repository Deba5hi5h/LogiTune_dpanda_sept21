import argparse
import time
import brainstem
from brainstem.result import Result
from common.framework_params import *

stem = brainstem.stem.USBHub3p()

def get_port_number(device_name: str):
    """
    Method to get the port number and serial number of the switch where device is connected
    device name should be same as device model name. Examples Rally Bar, Rally Bar Mini, MeetUp
    :param: device_name
    :return port_number, serial_number:
    """
    try:
        device_name = 'SWITCH_PORT_'+device_name.upper().replace(' ', '_').replace('-', '_').replace('+', '')
        switch_details = eval(device_name).split('|')
        port_number = int(switch_details[0])
        serial_number = eval('SWITCH_PORT_'+switch_details[1])
        return port_number, serial_number
    except:
        raise Exception('Device ' + device_name + ' not found')

def connect_device(device_name):
    port_number, serial_number = get_port_number(device_name)
    result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=serial_number)
    if result == (Result.NO_ERROR):
        stem.usb.setPortEnable(port_number)
    else:
        raise Exception('Switch Not found')
    stem.disconnect()

def disconnect_device(device_name):
    # Create USBHub2x4/USBHub3p object and connecting to the first module found

    # Locate and connect to the first object you find on USB
    # Easy way: 1=USB, 2=TCPIP
    port_number, serial_number = get_port_number(device_name)
    result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=serial_number)
    counter = 0
    while counter < 6:
        if result == 11:
            time.sleep(10)
            result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=serial_number)
            counter += 1
        else:
            break
    if result == (Result.NO_ERROR):
        time.sleep(2)
        stem.usb.setPortDisable(port_number)
        time.sleep(1)
    else:
        raise Exception('Switch Not found')
    stem.disconnect()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device", help="Device Name")
parser.add_argument("-c", "--connection", help="Device Connection")
args = parser.parse_args()
device_list = str(args.device).split(',')
connection = args.connection
for device in device_list:
    device = device.strip()
    if connection == 'Connect':
        connect_device(device)
    else:
        disconnect_device(device)