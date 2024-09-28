
from common.platform_helper import get_pc_host_name

FEATURES_ZWIRED = {
    # feature_name : [FEATURE_ID_MSB, FEATURE_ID_LSB, FEATURE_DESC, VERSION, FEATURE_INDEX_INT, FEATURE_INDEX_HEX]
    "iRoot": [0, 0, 0, 1, 0, '0x00'],
    "iFeatureSet": [0, 1, 0, 1, 1, '0x01'],
    "iDeviceInfo": [1, 0, 0, 1, 2, '0x02'],
    "iDeviceName": [1, 1, 0, 1, 3, '0x03'],

    "iHeadsetAudio": [5, 0, 0, 1, 4, '0x04'],
    "iHeadsetMisc": [5, 2, 0, 1, 5, '0x05'],
    "iHeadsetParaEQ": [5, 4, 0, 1, 6, '0x06'],
}
