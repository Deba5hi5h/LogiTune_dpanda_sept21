import random

CONNECTED_DEVICES = 1

CONNECTED = '01'
NOT_CONNECTED = '00'
MAX_LEN_NAME = 31

EQ_MODES = {
                 3: [0x00, 0x00, 0x00, 0x00, 0x00],
                 5: [0x7f, 0x4c, 0x19, 0x19, 0x19],
                 8: [0x00, 0x19, 0x66, 0x7f, 0x4c],
                 4: [random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)]
    }

ZONE_TRUE_WIRELESS_EQ_PROFILES = {
    "Default": 3,
    "Volume boost": 4,
    "Podcast": 4,
    "Bass boost": 4,
    "Custom": 4
}

DEFAULT_BUTTONS_GENERAL_SETTINGS = {0: [1, 0, 0, 7],
                                    1: [4, 3, 0, 7]}

BUTTONS_CAPABILITIES = {'00': ['00', '8b', '03', '92', '00', '83', '00', '00'],
                        '01': ['00', '08', '03', '18', '00', '83', '00', '00']}

BUTTONS_CAPABILITIES_BY_FUNCTIONS = {0: [[1, 4, 7, 8, 9], [0, 1, 7], [0], [0, 1, 7]],
                                     1: [[3, 4, 8, 9], [3], [0], [0, 1, 7]]}


FEATURES_ZAXXON = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 2, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iCentPPBridge": [0, 3, 0, 1, 2, '0x02'],
    "iDeviceInfo": [1, 0, 0, 1, 3, '0x03'],
    "iDeviceName": [1, 1, 0, 2, 4, '0x04'],
    "iEQSet": [2, 1, 0, 4, 5, '0x05'],
    "iAutoSleep": [1, 8, 0, 2, 6, '0x06'],
    "iHeadsetAudio": [5, 0, 0,  3, 7, '0x07'],
    "iHeadsetBtConnInfo": [5, 1, 0, 1, 8, '0x08'],
    "iHeadsetMisc": [5, 2, 0, 1, 9, '0x09'],
    "iEarcon": [1, 9, 0, 4, 10, '0x0a'],
    "iBatterySOC": [1, 4, 0, 3, 11, '0x0b'],
    "iZaxxonBudsCaseKey": [5, 17, 0, 1, 12, '0x0c'],
    "iTWBudsRoleSwitching": [6, 20, 0, 2, 13, '0x0d'],
    "iTWBudsInEarDetection": [6, 19, 0, 1, 14, '0x0e'],
    "iZaxxonChargingCaseInfo": [5, 12, 0, 1, 15, '0x0f'],
    "iZaxxonStartGaiaOta": [5, 13, 0, 1, 16, '0x10'],
    "iTWBudsInTheCase": [6, 12, 0, 1, 17, '0x11']
}

FEATURES_SET_ZAXXON = [[0, 0], [0, 1], [0, 3], [1, 0], [1, 1], [2, 1], [1, 8], [5, 0], [5, 1], [5, 2], [1, 9], [1, 4], [5, 3], [5, 17], [6, 20], [6, 19]]

FEATURES_SECONDARY_EARBUD_ZAXXON = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 2, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 1, 2, '0x02'],
    "iBatterySOC": [1, 4, 0, 3, 3, '0x03'],
}
