import random

CONNECTED_DEVICES = 1

ZONE_950_PROFILES = {
    "Default": 0,
    "Volume boost": 1,
    "Podcast": 2,
    "Bass boost": 3,
    "Custom": 4
}

CONNECTED = '01'
NOT_CONNECTED = '00'
MAX_LEN_NAME = 31

EQ_MODES = {
                 3: [0x00, 0x00, 0x00, 0x00, 0x00],
                 5: [0x7f, 0x4c, 0x19, 0x19, 0x19],
                 8: [0x00, 0x19, 0x66, 0x7f, 0x4c],
                 4: [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    }


FEATURES_ZONE_950 = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 1, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 6, 2, '0x02'],
    "iDeviceName": [1, 1, 0, 1, 3, '0x03'],
    "iEQSet": [2, 1, 0, 6, 4, '0x04'],
    "iAutoSleep": [1, 8, 0, 2, 5, '0x05'],
    "iHeadsetAudio": [5, 0, 0, 5, 6, '0x06'],
    "iHeadsetBtConnInfo": [5, 1, 0, 1, 7, '0x07'],
    "iHeadsetMisc": [5, 2, 0, 3, 8, '0x08'],
    "iEarcon": [1, 9, 0, 2, 9, '0x09'],
    "iBatterySOC": [1, 4, 0, 3, 10, '0x0a'],
    "iAntiStartle": [6, 12, 0, 1, 11, '0x0b'],
    "iNoiseExposure": [6, 13, 0, 1, 12, '0x0c'],
    "iAINoiseReduction": [6, 14, 0, 2, 13, '0x0d'],
    "iAutoCallAnswer": [6, 15, 0, 1, 14, '0x0e'],
    "iAutoMuteOnCall": [6, 16, 0, 1, 15, '0x0f'],
    "iTWBudsInEarDetection": [6, 19, 0, 1, 16, '0x10'],
    "iFitsAudiogram": [7, 2, 0, 3, 17, '0x11'],
    "iHeadsetParaEQ": [5, 4, 0, 3, 18, '0x12'],
    "iHeadsetActiveEQ": [5, 20, 0, 2, 19, '0x13'],
    "iTouchSensor": [1, 17, 0, 1, 20, '0x14'],
    "iCompanionChipDFU": [1, 18, 0, 2, 21, '0x15'],
}


