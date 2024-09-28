import random

CONNECTED_DEVICES = 1

CONNECTED = '01'
NOT_CONNECTED = '00'

EQ_MODES = {
                 3: [0x00, 0x00, 0x00, 0x00, 0x00],
                 5: [0x7f, 0x4c, 0x19, 0x19, 0x19],
                 8: [0x00, 0x19, 0x66, 0x7f, 0x4c],
                 4: [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    }

ZONE_900_EQ_PROFILES = {
    "Default": 0,
    "Volume boost": 1,
    "Podcast": 2,
    "Bass boost": 3,
    "Custom": 4
}

ZONE_900_BUTTONS_ACTIONS = {
    "single_press": {
        "default": "Microsoft Teams",
        "functions": ["Play / Pause", "Microsoft Teams", "Voice Assistant (Mobile)", "Headset Status Report"]
    },
    "double_press": {
        "default": "Play / Pause",
        "functions": ["Play / Pause", "Next Track", "Voice Assistant (Mobile)", "Headset Status Report"]
    },
    "long_press": {
        "default": "Voice Assistant (Mobile)",
        "functions": ["Voice Assistant (Mobile)", "Headset Status Report"]
    }
}

ZONE_900_BUTTONS_MAPPING = {
    "Play / Pause": 0,
    "Next Track": 1,
    "Previous Track": 2,
    "Microsoft Teams": 3,
    "Voice Assistant (Mobile)": 4,
    "Headset Status Report": 5
}

DEFAULT_BUTTONS_GENERAL_SETTINGS = {0: [4, 3, 0, 0]}

BUTTONS_CAPABILITIES = {'00': ['00', '39', '00', '30', '00', '33', '00', '00'],
                        '01': ['00', '00', '00', '00', '00', '00', '00', '00']}

BUTTONS_CAPABILITIES_BY_FUNCTIONS = {0: [[4, 5], [3, 0, 4, 5], [0], [0, 1, 4, 5]]}


FEATURES_ZONE900 = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 1, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 1, 2, '0x02'],
    "iDeviceName": [1, 1, 0, 1, 3, '0x03'],
    "iBatterySOC": [1, 4, 0, 1, 4, '0x04'],
    "iEQSet": [2, 1, 0, 1, 5, '0x05'],
    "iBluetoothCtrl": [3, 3, 0, 1, 6, '0x06'],
    "iHeadsetAudio": [5, 0, 0, 2, 7, '0x07'],
    "iHeadsetBtConnInfo": [5, 1, 0, 1, 8, '0x08'],
    "iHeadsetMisc": [5, 2, 0, 1, 9, '0x09'],
    "iHeadsetOTA": [5, 3, 0, 1, 10, '0x0a'],
    "iAutoSleep": [1, 8, 0, 1, 11, '0x0b'],
    "iEarcon": [1, 9, 0, 1, 12, '0x0c'],
}


