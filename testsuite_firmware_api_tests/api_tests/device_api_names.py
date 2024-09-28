from dataclasses import dataclass


@dataclass()
class DeviceName():
    zone_true_wireless: str = "Zone True Wireless"
    zone_900: str = "Zone 900"
    zone_wireless_plus: str = "Zone Wireless Plus"
    zone_wireless: str = "Zone Wireless"
    logi_dock: str = "Logi Dock"
    zone_vibe_100: str = "Zone Vibe 100"
    zone_vibe_125: str = "Zone Vibe 125"
    zone_vibe_130: str = "Zone Vibe 130"
    zone_vibe_wireless: str = "Zone Vibe Wireless"
    zone_wired: str = "Zone Wired"
    zone_750: str = "Zone 750"
    zone_wired_earbuds: str = "Zone Wired Earbuds"
    zone_wireless_2: str = "Zone Wireless 2"
    zone_950: str = "Zone 950"
    quadrun_wo_headset: str = "Zone Receiver"
    litra_beam: str = "Litra Beam"
    zone_300: str = "Zone 300"
    zone_301: str = "Zone 301"
    zone_305: str = "Zone 305"
    bomberman_mono: str = "H570e Mono"
    bomberman_stereo: str = "H570e Stereo"
    hid_pid_list = {
        zone_true_wireless: 0x0AEA,
        zone_900: 0x0ADA,
        zone_wireless_plus: 0x0AA8,
        zone_wireless: 0x0A90,
        zone_vibe_125: 0x0AEE,
        zone_vibe_130: 0x0AF0,
        zone_vibe_wireless: 0x0AF0,
        zone_wired: 0x0AAD,
        zone_750: 0x0ADE,
        zone_wired_earbuds: 0x0AC8,
        logi_dock: 0x0ACC,
        zone_wireless_2: 0x0AF0,
        zone_950: 0x0AF0,
        quadrun_wo_headset: 0x0AF1,
        litra_beam: 0xC901,
        zone_300: 0x032d,
        zone_305: 0x0AF0,
        bomberman_mono: 0xB17,
        bomberman_stereo: 0xB16
    }


@dataclass
class ConnectionType:
    usb_dock: str = 'usb_dock'
    bt: str = 'bt'
    # Some headsets won't generate COM port that needs to verify features by tune UI ex.Zone 900, Zone wireless
    bt_ui: str = 'bt_ui'
    dongle: str = 'dongle'
    quadrun: str = 'quadrun'
    litra_beam: str = 'litra_beam'
