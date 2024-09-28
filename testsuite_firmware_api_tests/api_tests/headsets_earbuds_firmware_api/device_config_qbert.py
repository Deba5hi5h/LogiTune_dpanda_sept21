import random

CONNECTED_DEVICES = 1

CONNECTED = '01'
NOT_CONNECTED = '00'

EQ_MODES_QBERT = {
                 3: [0x00, 0x00, 0x00, 0x00, 0x00],
                 5: [0x7f, 0x4c, 0x19, 0x19, 0x19],
                 8: [0x00, 0x19, 0x66, 0x7f, 0x4c],
                 4: [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    }

QBERT_EQ_PROFILES = {
    "Default": 0,
    "Podcast": 2,
    "Bass boost": 3
}


FEATURES_QBERT = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 2, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 4, 2, '0x02'],
    "iDeviceName": [1, 1, 0, 2, 3, '0x03'],
    "iGenericDFU": [1, 10, 0, 1, 4, '0x04'],
    "iThermalSensors": [1, 11, 0, 1, 5, '0x05'],
    "iCentPPBridge": [0, 3, 0, 1, 6, '0x06'],
    "iUSBHubControl": [1, 12, 0, 1, 7, '0x07'],
    "iEQSet": [2, 1, 0, 3, 8, '0x08'],
    "iVideoMute": [1, 14, 0, 2, 9, '0x09'],
    "iAmbientLED": [1, 13, 0, 3, 10, '0x0a'],
    "iBTSpeakerPhone": [3, 6, 0, 3, 11, '0x0b'],
    "iOneTouchJoin": [1, 15, 0, 1, 12, '0x0c'],
    "iEarcon": [1, 9, 0, 5, 13, '0x0d'],

}
