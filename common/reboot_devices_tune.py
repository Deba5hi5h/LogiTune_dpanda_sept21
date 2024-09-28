import dlipower
from dataclasses import dataclass
from argparse import ArgumentParser


@dataclass
class PowerSwitch:
    name: str
    IP: str
    USERNAME: str
    PASSWORD: str


tune_power_switches = {
    'Cracow': PowerSwitch('Tune Cracow', '172.17.54.107', 'admin', 'PSW1234@!'),
    'TuneWin': PowerSwitch('Tune Windows', '172.28.213.9', 'admin', '1234'),
    'TuneMac': PowerSwitch('Tune Mac', '172.28.213.10', 'admin', '1234'),
}

if __name__ == "__main__":
    try:
        arg_parser = ArgumentParser()
        arg_parser.add_argument('-l', '--lab', help="Lab Name")
        arg_parser.add_argument('-o', '--outlets', help="Outlet Name")

        args = arg_parser.parse_args()
        selected_power_switch = tune_power_switches.get(args.lab)
        if selected_power_switch:
            outlets = [el.strip() for el in args.outlets.split(',')]
            power_switch = dlipower.PowerSwitch(userid=selected_power_switch.USERNAME,
                                                password=selected_power_switch.PASSWORD,
                                                hostname=selected_power_switch.IP)

            for index in range(1, 9):
                current_outlet_name = power_switch.get_outlet_name(index)
                if current_outlet_name in outlets:
                    print(f"Rebooting switch for {args.lab} - {current_outlet_name}")
                    power_switch.cycle(index)
                    print(power_switch.status(index))
    except Exception as e:
        print(e)


