from dataclasses import dataclass


@dataclass
class CameraInfo:
    name: str
    project_name: str


cameras_info_set = [
    CameraInfo('Brio', 'brio_4k'),
    CameraInfo('Brio 95', 'cezanne'),
    CameraInfo('Brio 100', 'cezanne'),
    CameraInfo('Brio 101', 'cezanne'),
    CameraInfo('Brio 105', 'cezanne'),
    CameraInfo('Brio 1080p Webcam', 'degas'),
    CameraInfo('Brio 300', 'degas'),
    CameraInfo('Brio 301', 'degas'),
    CameraInfo('Brio 305', 'degas'),
    CameraInfo('Brio 500', 'gauguin'),
    CameraInfo('Brio 501', 'gauguin'),
    CameraInfo('Brio 505', 'gauguin'),
    CameraInfo('MX Brio', 'matisse'),
    CameraInfo('Brio 701', 'matisse'),
    CameraInfo('MX Brio 705 for Business', 'matisse'),
    CameraInfo('C920 HD Pro Webcam', 'c920'),
    CameraInfo('C920e', 'c920'),
    CameraInfo('C930e', 'c930e'),
    CameraInfo('StreamCam', 'stream_cam'),
]
