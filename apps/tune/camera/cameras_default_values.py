import sys
from typing import Dict, Union


def get_camera_default_values(camera_name: str) -> Dict[str, Union[int, bool]]:
    current_os = 'win' if sys.platform.startswith('win') else 'mac'

    camera_default_values = {
        'brio_4k': {
            'fov': 90,
            'zoom': 100,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'hdr': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
            'pan_tilt_steps': 20,
        },
        'c920': {
            'zoom': 100,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
            'pan_tilt_steps': 20,
        },
        'c930e': {
            'zoom': 100,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
            'pan_tilt_steps': 20,
        },
        'cezanne': {
            'low_light_compensation': True,
            'auto_exposure': True,
            'auto_white_balance': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
        },
        'degas': {
            'low_light_compensation': True if current_os == 'win' else False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
        },
        'gauguin': {
            'fov': 90,
            'zoom': 100,
            'show_mode': True,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'hdr': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
            'pan_tilt_steps': 40,
        },
        'matisse': {
            'fov': 90,
            'zoom': 100,
            'show_mode': True,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'exposure_compensation': 128,
            'auto_white_balance': True,
            'temperature_compensation': 50,
            'hdr': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'vibrance': 128,
            'sharpness': 128,
            'pan_tilt_steps': 40,
        },
        'stream_cam': {
            'zoom': 100,
            'auto_focus': True,
            'low_light_compensation': False,
            'auto_exposure': True,
            'auto_white_balance': True,
            'hdr': True,
            'brightness': 128,
            'contrast': 128,
            'saturation': 128,
            'sharpness': 128,
            'pan_tilt_steps': 40,
        },
    }
    return camera_default_values.get(camera_name)