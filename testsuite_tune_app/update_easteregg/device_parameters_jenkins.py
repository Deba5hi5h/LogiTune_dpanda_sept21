'''
Copy this file and change its extension from .TEMPLATE to .py
'''

from apps.tune.device_parameters_utilities import Device, TuneEnv
from common.framework_params import JENKINS_REPEATS

is_acroname_available = True


"""
    H750e Mono
    baseline_device_version='1.31.0',
    target_device_version='1.32.0',
"""
bomberman_mono = Device(
    device_name='H570e Mono',
    ota_api_product_name='BombermanMono',
    baseline_device_version='1.39.0',
    target_device_version='1.40.0',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    H750e Stereo
    baseline_device_version='1.31.0',
    target_device_version='1.32.0',
"""
bomberman_stereo = Device(
    device_name='H570e Stereo',
    ota_api_product_name='BombermanStereo',
    baseline_device_version='1.39.0',
    target_device_version='1.40.0',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Brio 4K
    baseline_device_version='2.0.56',
    target_device_version='2.0.58',
    baseline_eeprom_version='1.18',
    target_eeprom_version='1.18',
"""
brio4k = Device(
    device_name='Brio',
    ota_api_product_name='Brio',
    baseline_device_version='2.0.58',
    target_device_version='2.0.64',
    baseline_eeprom_version='1.18',
    target_eeprom_version='1.18',
    jenkins_tune_env=TuneEnv.qa,
    repeats=JENKINS_REPEATS,
)

"""
    C930e
    baseline_device_version='8.0.928',
    target_device_version='8.0.929',
"""
c930e = Device(
    device_name='C930e',
    ota_api_product_name='C930E',
    baseline_device_version='8.0.928',
    target_device_version='8.0.929',
    jenkins_tune_env=TuneEnv.prod,
    repeats=JENKINS_REPEATS,
)

"""
    Brio 100/101/105
    baseline_device_version='1.1.4',
    target_device_version='1.1.4',
"""
cezanne = Device(
    device_name='Brio 105',
    ota_api_product_name='Cezanne',
    baseline_device_version='1.1.4',
    target_device_version='1.1.4',
    jenkins_tune_env=TuneEnv.qa,
    repeats=JENKINS_REPEATS,
)

"""
    Brio 300/301/305
    baseline_device_version='3.0.9020',
    target_device_version='3.0.21',
"""
degas = Device(
    device_name='Brio 305',
    ota_api_product_name='Degas',
    baseline_device_version='1.0.37',
    target_device_version='1.0.9037',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Brio 500/501/505
    baseline_device_version='1.0.225',
    target_device_version='1.0.234',
"""
gauguin = Device(
    device_name='Brio 505',
    ota_api_product_name='Gauguin',
    baseline_device_version='1.0.328',
    target_device_version='9.0.173',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    MX Brio/MX Brio 705 for Business
    baseline_device_version='1.0.63',
    target_device_version='1.0.64',
"""
matisse = Device(
    device_name='MX Brio',
    ota_api_product_name='Matisse',
    baseline_device_version='1.0.390',
    target_device_version='8.0.159',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Litra Beam
    baseline_device_version='1.2.69',
    target_device_version='1.2.70',
"""
litra_beam = Device(
    device_name='Litra Beam',
    ota_api_product_name='LitraBeam',
    baseline_device_version='1.2.69',
    target_device_version='1.2.71',
    jenkins_tune_env=TuneEnv.qa,
    repeats=JENKINS_REPEATS,
)

"""
    Logi Dock
    baseline_device_version='1.0.94',
    target_device_version='1.0.97',
"""
logi_dock = Device(
    device_name='Logi Dock',
    ota_api_product_name='Qbert',
    baseline_device_version='1.6.28',
    target_device_version='1.6.30',
    jenkins_tune_env=TuneEnv.qa,
    repeats=JENKINS_REPEATS,
)

"""
    Zone 300
    baseline_device_version='0.8.1',
    target_device_version='0.8.2',
"""
zone_300 = Device(
    device_name='Zone 300',
    ota_api_product_name='KrullRetail',
    baseline_device_version='',
    target_device_version='',
    repeats=3,
)

"""
    Zone 301
    baseline_device_version='0.8.1',
    target_device_version='0.8.2',
"""
zone_301 = Device(
    device_name='Zone 301',
    ota_api_product_name='KrullAmazon',
    baseline_device_version='',
    target_device_version='',
    repeats=3,
)

"""
    Zone 305
    baseline_device_version='0.8.1',
    target_device_version='0.8.2',
"""
zone_305 = Device(
    device_name='Zone 305',
    ota_api_product_name='Krull',
    baseline_device_version='0.8.36',
    baseline_dongle_version='2.48.1',
    target_device_version='0.8.37',
    target_dongle_version='91.48.1',
    repeats=3,
)

"""
    Zone 750
    baseline_device_version='1.36.0',
    target_device_version='1.39.0',
"""
zone_750 = Device(
    device_name='Zone 750',
    ota_api_product_name='Zone750',
    baseline_device_version='1.37.0',
    target_device_version='1.42.0',
    jenkins_tune_env=TuneEnv.qa,
    repeats=JENKINS_REPEATS,
)

"""
    Zone 900
    baseline_device_version='1.86.1',
    baseline_dongle_version='1.86.1',
    target_device_version='1.87.0',
    target_dongle_version='1.87.0',
"""
zone_900 = Device(
    device_name='Zone 900',
    ota_api_product_name='Zone900',
    baseline_device_version='1.88.1',
    baseline_dongle_version='1.88.1',
    target_device_version='1.88.2',
    target_dongle_version='1.88.2',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone 950
    baseline_device_version='1.3.36',
    baseline_tahiti_version='4.24.5.1',
    baseline_dongle_version='1.84.1',
    target_device_version='1.3.141',
    target_tahiti_version='4.24.5.2',
    target_dongle_version='4.84.1',
"""
zone_950 = Device(
    device_name='Zone 950',
    ota_api_product_name='Zone950',
    baseline_device_version='1.3.60',
    baseline_tahiti_version='4.24.7.6',
    baseline_dongle_version='2.45.1',
    target_device_version='1.3.165',
    target_tahiti_version='4.24.7.7',
    target_dongle_version='91.45.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)


"""
    Zone True Wireless
    baseline_device_version='5.07',
    baseline_dongle_version='1.87.6',
    target_device_version='5.08',
    target_dongle_version='1.87.7',
"""
zone_true_wireless = Device(
    device_name='Zone True Wireless',
    ota_api_product_name='Zaxxon',
    baseline_device_version='5.99',
    baseline_dongle_version='1.88.6',
    target_device_version='6.23',
    target_dongle_version='1.88.10',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Vibe 100
    baseline_device_version='1.3.0',
    target_device_version='1.4.0',
"""
zone_vibe_100 = Device(
    device_name='Zone Vibe 100',
    ota_api_product_name='ZoneVibe100',
    baseline_device_version='1.38.0',
    target_device_version='1.38.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Vibe 125
    baseline_device_version='1.3.0',
    baseline_dongle_version='2.7.0',
    target_device_version='1.4.0',
    target_dongle_version='2.8.0',
"""
zone_vibe_125 = Device(
    device_name='Zone Vibe 125',
    ota_api_product_name='Enduro',
    baseline_device_version='1.38.0',
    baseline_dongle_version='2.11.0',
    target_device_version='1.38.1',
    target_dongle_version='2.11.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Vibe 130
    baseline_device_version='1.3.0',
    baseline_dongle_version='2.7.0',
    target_device_version='1.4.0',
    target_dongle_version='2.8.0',
    dongle_address='046D_0AF0_2207MH01ECL86EE13A6D3744',
"""
zone_vibe_130 = Device(
    device_name='Zone Vibe 130',
    ota_api_product_name='ZoneVibe130',
    baseline_device_version='1.38.0',
    baseline_dongle_version='2.33.1',
    target_device_version='1.38.1',
    target_dongle_version='91.33.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
    dongle_address='xyz',
)

"""
    Zone Vibe Wireless
    baseline_device_version='1.3.0',
    baseline_dongle_version='2.7.0',
    target_device_version='1.4.0',
    target_dongle_version='2.8.0',
    dongle_address='046D_0AF0_2207MH01ECL86EE13A6D3744',
"""
zone_vibe_wireless = Device(
    device_name='Zone Vibe Wireless',
    ota_api_product_name='ZoneVibeWireless',
    baseline_device_version='1.38.0',
    baseline_dongle_version='2.33.1',
    target_device_version='1.38.1',
    target_dongle_version='91.33.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
    dongle_address='zyx',
)

"""
    Zone Wired
    baseline_device_version='1.28',
    target_device_version='1.36',
"""
zone_wired = Device(
    device_name='Zone Wired',
    ota_api_product_name='ZoneWired',
    baseline_device_version='1.44',
    target_device_version='1.45',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Wired Earbuds
    baseline_device_version='1.40.0',
    target_device_version='1.41.0',
"""
zone_wired_earbuds = Device(
    device_name='Zone Wired Earbuds',
    ota_api_product_name='Tetris',
    baseline_device_version='1.40.0',
    target_device_version='1.41.0',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Wireless
    baseline_device_version='1.74.0',
    baseline_dongle_version='1.74.0',
    target_device_version='1.86.1',
    target_dongle_version='1.86.1',
"""
zone_wireless = Device(
    device_name='Zone Wireless',
    ota_api_product_name='ZoneWireless',
    baseline_device_version='1.88.1',
    baseline_dongle_version='1.88.1',
    target_device_version='1.88.2',
    target_dongle_version='1.88.2',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Wireless 2
    baseline_device_version='1.3.26',
    baseline_tahiti_version='4.24.4.45',
    baseline_dongle_version='1.80.1',
    target_device_version='1.3.124',
    target_tahiti_version='4.24.4.48',
    target_dongle_version='4.80.1',
"""
zone_wireless_2 = Device(
    device_name='Zone Wireless 2',
    ota_api_product_name='Cybermorph',
    baseline_device_version='1.3.60',
    baseline_tahiti_version='4.24.7.6',
    baseline_dongle_version='2.45.1',
    target_device_version='1.3.165',
    target_tahiti_version='4.24.7.6',
    target_dongle_version='91.45.1',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)

"""
    Zone Wireless Plus
    baseline_device_version='1.86.1',
    baseline_dongle_version='1.86.1',
    target_device_version='1.87.0',
    target_dongle_version='1.87.3',
"""
zone_wireless_plus = Device(
    device_name='Zone Wireless Plus',
    ota_api_product_name='ZoneWirelessPlus',
    baseline_device_version='1.88.1',
    baseline_dongle_version='1.88.1',
    target_device_version='1.88.2',
    target_dongle_version='1.88.2',
    jenkins_tune_env=TuneEnv.dev,
    repeats=JENKINS_REPEATS,
)
