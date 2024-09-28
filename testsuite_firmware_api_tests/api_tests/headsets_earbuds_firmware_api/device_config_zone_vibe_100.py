import random

CONNECTED_DEVICES = 1

ZONE_VIBE_100_PROFILES = {
    "Default": 0,
    "Volume boost": 1,
    "Podcast": 2,
    "Bass boost": 3,
    "Custom": 4
}

CONNECTED = '01'
NOT_CONNECTED = '00'

EQ_MODES = {
                 3: [0x00, 0x00, 0x00, 0x00, 0x00],
                 5: [0x7f, 0x4c, 0x19, 0x19, 0x19],
                 8: [0x00, 0x19, 0x66, 0x7f, 0x4c],
                 4: [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    }

FEATURES_ZONE_VIBE_100 = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 1, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 1, 2, '0x02'],
    "iDeviceName": [1, 1, 0, 1, 3, '0x03'],
    "iBatterySOC": [1, 4, 0, 1, 4, '0x04'],
    "iAutoSleep": [1, 8, 0, 1, 5, '0x05'],
    "iEarcon": [1, 9, 0, 1, 6, '0x06'],
    "iEQSet": [2, 1, 0, 1, 7, '0x07'],
    "iBluetoothCtrl": [3, 3, 0, 1, 8, '0x08'],
    "iHeadsetAudio": [5, 0, 0, 1, 9, '0x09'],
    "iHeadsetBtConnInfo": [5, 1, 0, 1, 10, '0x0a'],
    "iHeadsetMisc": [5, 2, 0, 1, 11, '0x0b'],
}


