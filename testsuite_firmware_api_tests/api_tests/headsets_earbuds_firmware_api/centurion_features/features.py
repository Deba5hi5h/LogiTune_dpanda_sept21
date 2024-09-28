from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.LitraBeam import \
    LitraBeamFeatures
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAINoiseReduction import (
    AINoiseReduction,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAmbientLED_feature import (
    AmbientLEDFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAntiStartle import (
    AntiStartle,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAutoSleep_feature import (
    AutoSleepFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iBatterySOC_feature import (
    BatterySOCFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iBluetoothCtrl_feature import (
    BluetoothCrtlFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iBTSpeakerPhone_feature import (
    BTSpeakerPhoneFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iCentPPBridge_feature import (
    CentPPBridgeFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iDeviceInfo_feature import (
    DeviceInfoFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iDeviceName_feature import (
    DeviceNameFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iEarcon_feature import (
    EarconFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iEQSet_feature import (
    EQSetFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iFeatureSet_feature import (
    FeatureSetFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iHeadsetActiveEQ import \
    HeadsetActiveEQFeature
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iHeadsetAudio_feature import (
    HeadsetAudioFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iHeadsetBtConnInfo_feature import (
    HeadsetBtConnInfoFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iHeadsetMisc_feature import (
    HeadsetMicsFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iNoiseExposure import (
    NoiseExposure,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iOneTouchJoin_feature import (
    OneTouchJoinFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iRoot_feature import (
    RootFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iThermalSensors_feature import (
    ThermalSensorsFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iTWBudsInEarDetection_feature import (
    TWBudsInEarDetectionFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iTWBudsRoleSwitching_feature import (
    TWBudsRoleSwitchingFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iTouchSensor import \
    TouchSensorFeature
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iUSBHubControl_feature import (
    USBHubControlFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iVideoMute_feature import (
    VideoMuteFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iZaxxonBudsCaseKey_feature import (
    ZaxxonBudsCaseKeyFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iZaxxonChargingCaseInfo_feature import (
    ZaxxonChargingCaseInfoFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iZaxxonStartGaiaOta import (
    ZaxxonStartGaiaOtaFeature,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAutoCallAnswer import (
    AutoCallAnswer,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iAutoMuteOnCall import (
    AutoMuteOnCall,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iFitsAudiogram import (
    FitsAudiogram,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.iHeadsetParaEQ import (
    HeadsetParaEQ,
)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.Quadrun import \
    QuadrunFeatures


class Features:
    def __init__(self, centurion):
        self.root_feature = RootFeature(centurion)
        self.feature_set_feature = FeatureSetFeature(centurion)
        self.cent_pp_bridge_feature = CentPPBridgeFeature(centurion)
        self.device_info_feature = DeviceInfoFeature(centurion)
        self.device_name_feature = DeviceNameFeature(centurion)
        self.eqset_feature = EQSetFeature(centurion)
        self.auto_sleep_feature = AutoSleepFeature(centurion)
        self.headset_audio_feature = HeadsetAudioFeature(centurion)
        self.headset_bt_conn_info_feature = HeadsetBtConnInfoFeature(centurion)
        self.headset_misc_feature = HeadsetMicsFeature(centurion)
        self.earcon_feature = EarconFeature(centurion)
        self.battery_SOC_feature = BatterySOCFeature(centurion)
        self.zaxxon_bud_case_key_feature = ZaxxonBudsCaseKeyFeature(centurion)
        self.tw_role_switching_feature = TWBudsRoleSwitchingFeature(centurion)
        self.tw_in_ear_detection_feature = TWBudsInEarDetectionFeature(centurion)
        self.bluetooth_crtl_feature = BluetoothCrtlFeature(centurion)
        self.thermal_sensors = ThermalSensorsFeature(centurion)
        self.usb_control = USBHubControlFeature(centurion)
        self.video_mute = VideoMuteFeature(centurion)
        self.ambient_led = AmbientLEDFeature(centurion)
        self.speaker_phone = BTSpeakerPhoneFeature(centurion)
        self.one_touch_join = OneTouchJoinFeature(centurion)
        self.zaxxon_charge_case_info = ZaxxonChargingCaseInfoFeature(centurion)
        self.zaxxon_start_gaia_ota = ZaxxonStartGaiaOtaFeature(centurion)
        self.ai_noise_reduction = AINoiseReduction(centurion)
        self.anti_startle = AntiStartle(centurion)
        self.noise_exposure = NoiseExposure(centurion)
        self.auto_call_answer = AutoCallAnswer(centurion)
        self.auto_mute_on_call = AutoMuteOnCall(centurion)
        self.fits_audiogram = FitsAudiogram(centurion)
        self.headset_para_eq = HeadsetParaEQ(centurion)
        self.touch_sensor_state = TouchSensorFeature(centurion)
        self.headset_active_eq = HeadsetActiveEQFeature(centurion)
        self.quadrun = QuadrunFeatures(centurion)
        self.litra_beam = LitraBeamFeatures(centurion)
