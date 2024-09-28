from dataclasses import dataclass
from typing import Optional


@dataclass
class ImageFilter:
    name: str
    auto_white_balance: bool
    brightness: int
    contrast: int
    saturation: int
    sharpness: int

    def verify_parameters(self, auto_white_balance: bool, brightness: int, contrast: int,
                          saturation: int, sharpness: int) -> Optional[str]:
        if self.auto_white_balance is auto_white_balance and self.brightness == brightness and \
           self.contrast == contrast and self.saturation == saturation and \
           self.sharpness == sharpness:
            return self.name


camera_filters = [
    ImageFilter(
        name='Bright',
        auto_white_balance=True,
        brightness=180,
        contrast=150,
        saturation=128,
        sharpness=128,
    ),
    ImageFilter(
        name='Blossom',
        auto_white_balance=False,
        brightness=128,
        contrast=128,
        saturation=102,
        sharpness=76,
    ),
    ImageFilter(
        name='Forest',
        auto_white_balance=False,
        brightness=140,
        contrast=128,
        saturation=51,
        sharpness=128,
    ),
    ImageFilter(
        name='Film',
        auto_white_balance=True,
        brightness=128,
        contrast=76,
        saturation=178,
        sharpness=255,
    ),
    ImageFilter(
        name='Glaze',
        auto_white_balance=False,
        brightness=128,
        contrast=153,
        saturation=140,
        sharpness=153,
    ),
    ImageFilter(
        name='Mono B',
        auto_white_balance=True,
        brightness=128,
        contrast=128,
        saturation=0,
        sharpness=128,
    ),
]
