from framework_params import settings
from common.usb_switch import connect_device_by_port_number

devices = settings.config['SWITCH_PORT']

for k, v in devices.items():
    charge_flag = not k.upper().split('_')[-1] == "CHARGE"
    if charge_flag:
        try:
            port, hub = v.split("|")
            connect_device_by_port_number(int(port), hub)
        except Exception as e:
            print(e)
