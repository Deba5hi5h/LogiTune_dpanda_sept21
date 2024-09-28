from dataclasses import dataclass


@dataclass
class HeadsetInfo:
    name: str
    project_name: str


headset_info_set = [
    HeadsetInfo('Zone 300', 'zone_300'),
    HeadsetInfo('Zone 301', 'zone_301'),
    HeadsetInfo('Zone 305', 'zone_305'),
    HeadsetInfo('Zone 750', 'zone_750'),
    HeadsetInfo('Zone 900', 'zone_900'),
    HeadsetInfo('Zone 950', 'zone_950'),
    HeadsetInfo('Zone Vibe 125', 'zone_vibe_125'),
    HeadsetInfo('Zone Vibe 130', 'zone_vibe_130'),
    HeadsetInfo('Zone Vibe Wireless', 'zone_vibe_wireless'),
    HeadsetInfo('Zone Wired', 'zone_wired'),
    HeadsetInfo('Zone Wired Earbuds', 'zone_wired_earbuds'),
    HeadsetInfo('Zone Wireless', 'zone_wireless'),
    HeadsetInfo('Zone Wireless 2', 'zone_wireless_2'),
    HeadsetInfo('Zone Wireless Plus', 'zone_wireless_plus'),
    HeadsetInfo('H570e Mono', 'h570e_mono'),
    HeadsetInfo('H570e Stereo', 'h570e_stereo'), # to be fixed
]

