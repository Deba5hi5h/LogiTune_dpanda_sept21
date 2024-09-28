# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem development package.
# See file LICENSE or go to https://acroname.com/software/brainstem-development-kit for full license details.
import time
import threading
import brainstem
import sys
# for easy access to error constants
from brainstem import discover
from brainstem.result import Result
from brainstem.link import Status
from common.framework_params import *
from extentreport.report import Report
from base import global_variables

mutex = threading.Lock()

report = Report()

if global_variables.USB_SWITCH == 8:
    stem = brainstem.stem.USBHub3p()
else:
    stem = brainstem.stem.USBHub2x4()


def stem_disconnect(retry: int = 3):
    with mutex:
        try:
            if retry == 0:
                print("Debug: Disconnecting failed", flush=True)
            time.sleep(0.5)
            stem.disconnect()
            while stem.getStatus() == Status.RUNNING:
                time.sleep(0.5)
            print(f"Debug: Disconnecting ok - Stem Status: {stem.getStatus()}", flush=True)

        except Exception as e:
            print(f"Exception: {e}, retrying")
            time.sleep(3)
            stem_disconnect(retry - 1)


def connect_to_stem_by_sn(serial_number: str):
    counter = 5
    while stem.getStatus() != Status.RUNNING and counter > 0:
        if counter == 0:
            raise Exception('Device not connected -> handling')
        counter -= 1
        usb_hub = discover.findModule(brainstem.link.Spec.USB, serial_number)
        if not usb_hub:
            time.sleep(5)
            continue
        if stem.connectFromSpec(usb_hub) != Result.NO_ERROR:
            time.sleep(5)


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
    if result == Result.NO_ERROR:
        time.sleep(2)
        stem.usb.setPortDisable(port_number)
        report.logPass("Device " + device_name + " unplugged")
        time.sleep(1)
    else:
        report.logException(f'Switch Not found - {result}')
        raise Exception('Switch Not found')
    stem.disconnect()


def disconnect_device_no_sleeps(device_name, retry: int = 3):
    stem_disconnect()
    if retry == 0:
        Report.logException(f"Maximum retries reached when disconnecting device {device_name}")
    start_time = time.time()
    try:
        port_number, serial_number = get_port_number(device_name)
        connect_to_stem_by_sn(serial_number)
        stem.hub.port[port_number].setEnabled(False)
        time.sleep(1)
        port_status = stem.hub.port[port_number].getEnabled()
        if not port_status.value:
            report.logInfo(f"Device {device_name} disconnected successfully")
        else:
            report.logException(f'Device {device_name} not disconnected successfully')
            raise Exception('Switch Not found')
        time.sleep(1)
        t = threading.Thread(target=stem_disconnect)
        t.start()
        print(f"--- %s seconds took to unplug in the device---" % (time.time() - start_time))
    except Exception as e:
        print(f"Retrying with retries left: {retry} - because: {e}")
        return disconnect_device_no_sleeps(device_name, retry - 1)


def connect_device(device_name, report_result=True):
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
    if result == Result.NO_ERROR:
        time.sleep(2)
        stem.usb.setPortEnable(port_number)
        if report_result:
            report.logPass("Device " + device_name + " plugged")
        time.sleep(1)
    else:
        if report_result:
            report.logException(f'Switch Not found - {result}')
        raise Exception('Switch Not found')
    stem.disconnect()


def connect_device_no_sleeps(device_name, retry: int = 3):
    stem_disconnect()
    if retry == 0:
        Report.logException(f"Maximum retries reached when disconnecting device {device_name}")
    start_time = time.time()
    try:
        port_number, serial_number = get_port_number(device_name)
        connect_to_stem_by_sn(serial_number)
        stem.hub.port[port_number].setEnabled(True)
        time.sleep(1)
        port_status = stem.hub.port[port_number].getEnabled()
        if port_status.value:
            report.logInfo(f"Device {device_name} connected successfully")
        else:
            report.logException(f'Switch Not found')
            raise Exception('Switch Not found')
        time.sleep(1)
        t = threading.Thread(target=stem_disconnect)
        t.start()
        print(f"--- %s seconds took to plug in the device---" % (time.time() - start_time))

    except Exception as e:
        print(f"Retrying with retries left: {retry} because {e}")
        return connect_device_no_sleeps(device_name, retry - 1)

def connect_device_by_port_number(port_number, hub_name, report_result=True):
    serial_number = eval('SWITCH_PORT_' + hub_name)
    result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=serial_number)
    counter = 0
    while counter < 6:
        if result == 11:
            time.sleep(10)
            result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=serial_number)
            counter += 1
        else:
            break
    if result == Result.NO_ERROR:
        time.sleep(2)
        stem.usb.setPortEnable(port_number)
        if report_result:
            report.logPass(f"Device connected to {port_number}|{serial_number} plugged")
        time.sleep(1)
    else:
        if report_result:
            report.logException(f'Switch Not found - {result}')
        raise Exception('Switch Not found')
    stem.disconnect()

def disconnect_all():
    # time.sleep(10)
    specs = discover.findAllModules(brainstem.link.Spec.USB)
    for spec in specs:
        if spec.model == 21:
            continue
        result = stem.connectFromSpec(spec)
        counter = 0
        while counter < 15:
            if result == 11:
                time.sleep(1)
                result = stem.connectFromSpec(spec)
                counter += 1
            else:
                break
        if result == Result.NO_ERROR:
            for i in range(8):
                stem.usb.setPortDisable(i)
        else:
            report.logException('Switch Not found')
            raise Exception('Switch Not found')

        stem.disconnect()


def switch_all_to_opposite():
    current_attrs = sys.modules[__name__]
    current_attrs_dir = current_attrs.__dir__()
    master_serial_numbers = [current_attrs.__getattribute__(el) for el in current_attrs_dir if 'master' in el.lower()]
    specs = discover.findAllModules(brainstem.link.Spec.USB)
    filtered_specs = filter(lambda x: x.serial_number in master_serial_numbers, specs)
    counter = 5
    for spec in filtered_specs:
        while stem.getStatus() != Status.RUNNING and counter > 0:
            if counter == 0:
                raise Exception('Device not connected -> handling')
            counter -= 1
            stem.connectFromSpec(spec)

        result = stem.usb.getUpstreamState()
        if result.error == Result.NO_ERROR:
            if result.value == 0:
                print("Switching to Port 1")
                stem.usb.setUpstreamMode(1)
            else:
                print("Switching to Port 0")
                stem.usb.setUpstreamMode(0)
        else:
            print("Error determining new host port.")
        stem_disconnect()


def connect_all():
    specs = discover.findAllModules(brainstem.link.Spec.USB)
    for spec in specs:
        result = stem.connectFromSpec(spec)
        if result == Result.NO_ERROR:
            for i in range(8):
                stem.usb.setPortEnable(i)
        else:
            report.logException('Switch Not found')
            raise Exception('Switch Not found')
        stem.disconnect()


def get_port_number(device_name: str):
    """
    Method to get the port number and serial number of the switch where device is connected
    device name should be same as device model name. Examples Rally Bar, Rally Bar Mini, MeetUp
    :param: device_name
    :return port_number, serial_number:
    """
    try:
        device_name = 'SWITCH_PORT_' + device_name.upper().replace(' ', '_').replace('-', '_').replace('+', '')
        switch_details = eval(device_name).split('|')
        port_number = int(switch_details[0])
        serial_number = eval('SWITCH_PORT_' + switch_details[1])
        return port_number, serial_number
    except:
        raise Exception('Device ' + device_name + ' not found')


def check_switch_status():
    result = stem.discoverAndConnect(brainstem.link.Spec.USB)
    if result == Result.NO_ERROR:
        print("Switch Active")
        return True
    else:
        print("Switch not Active")
        return False


def release_switch():
    """
    Method to release the switch from connected host. This will be always for Master Switch
    :param:
    :return:
    """
    stem = brainstem.stem.USBHub3p()
    result = stem.discoverAndConnect(brainstem.link.Spec.USB, serial_number=SWITCH_PORT_MASTER2)
    if result == Result.NO_ERROR:
        print("Switch Active")
    else:
        print("Switch not Active and cannot be released")
        return
    result = stem.usb.getUpstreamState()
    if result.error == Result.NO_ERROR:
        if result.value == 0:
            print("Switching to Port 1")
            result = stem.usb.setUpstreamMode(1)
        else:
            print("Switching to Port 0")
            result = stem.usb.setUpstreamMode(0)
    else:
        print("Error determining new host port.")


def enable_port_if_not_connected(device_name):
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
    if result == Result.NO_ERROR:
        time.sleep(6)

        port_state_raw = stem.usb.getPortState(port_number)
        port_state = port_state_raw.value

        DEVICE_BIT_MASK = 0x800000
        device_attached = bool((port_state & DEVICE_BIT_MASK) >> 23)
        Report.logInfo(f"Device {device_name} status on port {port_number}: {device_attached}.")

        if not device_attached:
            Report.logInfo(f"Enable port {port_number}.")
            time.sleep(2)
            stem.usb.setPortEnable(port_number)
            Report.logInfo(f"Device {device_name} plugged in.")
            time.sleep(1)
            port_state_raw = stem.usb.getPortState(port_number)
            port_state = port_state_raw.value
            device_attached = bool((port_state & DEVICE_BIT_MASK) >> 23)
            Report.logInfo(f"Device {device_name} status on port {port_number}: {device_attached}.")
        time.sleep(1)
    else:
        Report.logInfo(f'Switch Not found - {result}. Continue test without switch.')
    stem.disconnect()


def list_visible_acronames() -> tuple:
    specs = discover.findAllModules(brainstem.link.Spec.USB)
    devices = []
    for spec in specs:
        devices.append(hex(spec.serial_number))
    return tuple(devices)


if __name__ == '__main__':
    disconnect_all()



