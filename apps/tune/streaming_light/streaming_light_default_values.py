import sys
from typing import Dict, Union


def get_streaming_light_default_values(streaming_light_name: str) -> Dict[str, Union[int, bool]]:
    current_os = 'win' if sys.platform.startswith('win') else 'mac'

    streaming_light_default_values = {
        'litra_beam': {
            'power_on': False,
            'light_temperature': -6500,
            'light_brightness': 30,
        },
        'litra_glow': {
            'power_on': False,
            'light_temperature': -6500,
            'light_brightness': 30,
        },
    }
    return streaming_light_default_values.get(streaming_light_name)
