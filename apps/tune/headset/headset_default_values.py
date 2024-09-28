from dataclasses import dataclass
import sys
from typing import Dict, Optional, Tuple, Union


@dataclass
class EqualizerPreset:
    name: str
    default_values: Tuple[int, int, int, int, int]
    default_values_wired: Optional[Tuple[int, int, int, int, int]] = None

    def verify_parameters(self, *sliders: int) -> Optional[str]:
        for idx, slider_value in enumerate(sliders):
            if self.__getattribute__(f'slider_{idx}') != slider_value:
                return None
        return self.name


def get_headset_default_values(headset_name: str) -> Dict[str, Union[int, bool]]:
    current_os = 'win' if sys.platform.startswith('win') else 'mac'

    headset_default_values = {
        'zone_300': {
            'sidetone': 40,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone 300',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_301': {
            'sidetone': 40,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone 300',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_305': {
            'sidetone': 40,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone 300',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_750': {
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_900': {
            'noise_cancellation_switch': False,
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Logi Zone 900',
            'single_press': 'Microsoft Teams',
            'double_press': 'Play / Pause',
            'long_press': 'Voice Assistant (Mobile)',
            'sleep_settings': '1 Hour',
            'rotate_to_mute': True,
            'voice_prompts': True,
            'connection_priority': 'Stable connection'
        },
        'zone_vibe_125': {
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone Vibe 125',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_vibe_130': {
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone Vibe 125',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_vibe_wireless': {
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone Vibe Wireless',
            'sleep_settings': '30 minutes',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_wired': {
            'sidetone': 70,
            'mic_level': 100,
            'equalizer': 'Default',
            'rotate_to_mute': True,
            'voice_prompts': True
        },
        'zone_wired_earbuds': {
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'voice_prompts': True
        },
        'zone_wireless': {
            'noise_cancellation_switch': False,
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone Wireless',
            'single_press': 'Microsoft Teams',
            'double_press': 'Play / Pause',
            'long_press': 'Voice Assistant (Mobile)',
            'sleep_settings': '1 Hour',
            'rotate_to_mute': True,
            'voice_prompts': True,
            'connection_priority': 'Stable connection'
        },
        'zone_wireless_2': {
            'noise_cancellation': 'noiseCancellationHigh',
            'sidetone': 50,
            'mic_level': 100,
            'advanced_call_clarity': 'Off',
            'equalizer': 'Default',
            'anti_startle_protection': False,
            'noise_exposure_control': False,
            'device_name': 'Zone Wireless 2',
            'sleep_settings': '1 Hour',
            'rotate_to_mute': True,
            'transparency': True,
            'none': False,
            'noise_cancellation_low': False,
            'noise_cancellation_high': True,
            'auto_mute': False,
            'auto_answer': False,
            'auto_pause': True,
            'touch_pad': True,
            'voice_prompts': 'Voice'
        },
        'zone_wireless_plus': {
            'noise_cancellation_switch': False,
            'sidetone': 50,
            'mic_level': 100,
            'equalizer': 'Default',
            'device_name': 'Zone Wireless',
            'single_press': 'Microsoft Teams',
            'double_press': 'Play / Pause',
            'long_press': 'Voice Assistant (Mobile)',
            'sleep_settings': '1 Hour',
            'rotate_to_mute': True,
            'voice_prompts': True,
            'connection_priority': 'Stable connection'
        },
        'zone_950': {
            'noise_cancellation': 'noiseCancellationHigh',
            'sidetone': 50,
            'mic_level': 100,
            'advanced_call_clarity': 'Off',
            'equalizer': 'Default',
            'anti_startle_protection': False,
            'noise_exposure_control': False,
            'device_name': 'Zone 950',
            'sleep_settings': '1 Hour',
            'rotate_to_mute': True,
            'transparency': True,
            'none': False,
            'noise_cancellation_low': False,
            'noise_cancellation_high': True,
            'auto_mute': False,
            'auto_answer': False,
            'auto_pause': True,
            'touch_pad': True,
            'voice_prompts': 'Voice'
        },
        'h570e_mono': {
            'sidetone': 70,
            'mic_level': 87,
            'voice_prompts': True,
            'dashboard_anti_startle_protection': False,
        },
        'h570e_stereo': {
            'sidetone': 70,
            'mic_level': 87,
            'voice_prompts': True,
            'dashboard_anti_startle_protection': False,
        },
    }

    return headset_default_values.get(headset_name)


equalizers_presets = [
    EqualizerPreset(
        name='Default',
        default_values=(0, 0, 0, 0, 0),
    ),
    EqualizerPreset(
        name='Volume boost',
        default_values=(100, 100, 100, 100, 100),
    ),
    EqualizerPreset(
        name='Podcast',
        default_values=(0, 19, 80, 100, 59),
        default_values_wired=(-50, -25, 50, 25, 17),
    ),
    EqualizerPreset(
        name='Bass boost',
        default_values=(100, 59, 19, 19, 19),
        default_values_wired=(67, 0, 0, 0, 0),
    ),
]
