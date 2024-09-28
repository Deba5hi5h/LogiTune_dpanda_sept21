from apps.tune.devices_base_helpers import DevicesParametersWrapper
from apps.tune.streaming_light.streaming_light_locators import StreamingLightLocators
from apps.tune.streaming_light.streaming_light_capabilities import streaming_light_ui_capabilities
from apps.tune.streaming_light.streaming_light_default_values import get_streaming_light_default_values
from apps.tune.streaming_light.streaming_light_info import streaming_light_info_set
from apps.tune.tune_elements import TuneSlider, TuneSwitcher
from apps.tune.TuneElectron import TuneElectron


class StreamingLightProperties:
    def __init__(self,
                 tune_app: TuneElectron,
                 name: str,
                 project_name: str,
                 default_values: dict,
                 power_on: bool = False,
                 light_temperature: bool = False,
                 light_brightness: bool = False):
        self.name = name
        self.project_name = project_name
        self.default_values = default_values
        self.power_on = TuneSwitcher(tune_app, **StreamingLightLocators.power_on) if power_on else None
        self.light_temperature = TuneSlider(tune_app, **StreamingLightLocators.light_temperature) if light_temperature else None
        self.light_brightness = TuneSlider(tune_app, **StreamingLightLocators.light_brightness) if light_brightness else None


class StreamingLightParametersWrapper(DevicesParametersWrapper):

    def __init__(self, tune_app: TuneElectron):
        super().__init__(tune_app, streaming_light_info_set, StreamingLightProperties, streaming_light_ui_capabilities,
                         get_streaming_light_default_values)
