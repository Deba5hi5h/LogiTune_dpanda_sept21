from apps.tune.devices_base_helpers import DevicesParametersWrapper
from apps.tune.headset.headset_capabilities import headset_ui_capabilities
from apps.tune.headset.headset_default_values import get_headset_default_values
from apps.tune.headset.headset_info import headset_info_set
from apps.tune.headset.headset_locators import HeadsetLocators
from apps.tune.tune_elements import TuneElementsSelection, TuneDeviceName, TuneEqualizer, TuneSlider, TuneSwitcher, TuneNoiseCancellation
from apps.tune.TuneElectron import TuneElectron


class HeadsetProperties:
    def __init__(self,
                 tune_app: TuneElectron,
                 name: str,
                 project_name: str,
                 default_values: dict,
                 noise_cancellation_select: bool = False,
                 noise_cancellation_switch: bool = False,
                 sidetone: bool = False,
                 mic_level: bool = False,
                 advanced_call_clarity: bool = False,
                 equalizer: bool = False,
                 anti_startle_protection: bool = False,
                 dashboard_anti_startle_protection: bool = False,
                 noise_exposure_control: bool = False,
                 device_name: bool = False,
                 single_press: bool = False,        # Button functions options
                 double_press: bool = False,        # Button functions options
                 long_press: bool = False,          # Button functions options
                 sleep_settings: bool = False,
                 rotate_to_mute: bool = False,
                 transparency: bool = False,        # ANC button options
                 none: bool = False,                # ANC button options
                 noise_cancellation_low: bool = False,      # ANC button options
                 noise_cancellation_high: bool = False,     # ANC button options
                 auto_mute: bool = False,       # On-head detection options
                 auto_answer: bool = False,      # On-head detection options
                 auto_pause: bool = False,      # On-head detection options
                 touch_pad: bool = False,
                 voice_prompts_switch: bool = False,
                 voice_prompts_select: bool = False,
                 connection_priority: bool = False
                 ):
        self.name = name
        self.project_name = project_name
        self.default_values = default_values
        self.noise_cancellation_select = TuneNoiseCancellation(tune_app, **HeadsetLocators.noise_cancellation_select) \
            if noise_cancellation_select else None
        self.noise_cancellation_switch = TuneSwitcher(tune_app, **HeadsetLocators.noise_cancellation_switch) \
            if noise_cancellation_switch else None
        self.sidetone = TuneSlider(tune_app, **HeadsetLocators.sidetone) if sidetone else None
        self.mic_level = TuneSlider(tune_app, **HeadsetLocators.mic_level) if mic_level else None
        self.advanced_call_clarity = TuneElementsSelection(tune_app, **HeadsetLocators.advanced_call_clarity) \
            if advanced_call_clarity else None
        self.equalizer = TuneEqualizer(tune_app, **HeadsetLocators.equalizer) if equalizer else None
        self.anti_startle_protection = TuneSwitcher(tune_app, **HeadsetLocators.anti_startle_protection) \
            if anti_startle_protection else None
        self.dashboard_anti_startle_protection = TuneSwitcher(tune_app, **HeadsetLocators.dasboard_anti_startle_protection) \
            if dashboard_anti_startle_protection else None
        self.noise_exposure_control = TuneSwitcher(tune_app, **HeadsetLocators.noise_exposure_control) \
            if noise_exposure_control else None
        self.device_name = TuneDeviceName(tune_app, **HeadsetLocators.device_name) if device_name else None

        # Button functions
        self.single_press = TuneElementsSelection(tune_app, **HeadsetLocators.single_press) if single_press else None
        self.double_press = TuneElementsSelection(tune_app, **HeadsetLocators.double_press) if double_press else None
        self.long_press = TuneElementsSelection(tune_app, **HeadsetLocators.long_press) if long_press else None

        self.sleep_settings = TuneElementsSelection(tune_app, **HeadsetLocators.sleep_settings) \
            if sleep_settings else None
        self.rotate_to_mute = TuneSwitcher(tune_app, **HeadsetLocators.rotate_to_mute) if rotate_to_mute else None

        # ANC button options
        self.transparency = TuneSwitcher(tune_app, **HeadsetLocators.transparency) if transparency else None
        self.none = TuneSwitcher(tune_app, **HeadsetLocators.none) if none else None
        self.noise_cancellation_low = TuneSwitcher(tune_app, **HeadsetLocators.noise_cancellation_low) \
            if noise_cancellation_low else None
        self.noise_cancellation_high = TuneSwitcher(tune_app, **HeadsetLocators.noise_cancellation_high) \
            if noise_cancellation_high else None

        # On-head detection options
        self.auto_mute = TuneSwitcher(tune_app, **HeadsetLocators.auto_mute) if auto_mute else None
        self.auto_answer = TuneSwitcher(tune_app, **HeadsetLocators.auto_answer) if auto_answer else None
        self.auto_pause = TuneSwitcher(tune_app, **HeadsetLocators.auto_pause) if auto_pause else None

        self.touch_pad = TuneSwitcher(tune_app, **HeadsetLocators.touch_pad) if touch_pad else None
        self.voice_prompts_switch = TuneSwitcher(tune_app, **HeadsetLocators.voice_prompts_switch) \
            if voice_prompts_switch else None
        self.voice_prompts_select = TuneElementsSelection(tune_app, **HeadsetLocators.voice_prompts_select) \
            if voice_prompts_select else None
        self.connection_priority = TuneElementsSelection(tune_app, **HeadsetLocators.connection_priority) \
            if connection_priority else None


class HeadsetsParametersWrapper(DevicesParametersWrapper):
    def __init__(self, tune_app: TuneElectron):
        super().__init__(tune_app, headset_info_set, HeadsetProperties, headset_ui_capabilities,
                         get_headset_default_values)
