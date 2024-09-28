from apps.tune.camera.camera_locators import CameraLocators
from apps.tune.camera.camera_capabilities import camera_ui_capabilities
from apps.tune.camera.cameras_default_values import get_camera_default_values
from apps.tune.camera.cameras_info import cameras_info_set
from apps.tune.devices_base_helpers import DevicesParametersWrapper
from apps.tune.tune_elements import TuneFov, TunePanTilt, TuneElementsSelection, TuneSlider, \
    TuneSwitcher
from apps.tune.TuneElectron import TuneElectron


class CameraProperties:

    def __init__(self,
                 tune_app: TuneElectron,
                 name: str,
                 project_name: str,
                 default_values: dict,
                 pan_tilt: bool = False,
                 fov: bool = False,
                 zoom: bool = False,
                 show_mode: bool = False,
                 built_in_microphone: bool = False,
                 auto_focus: bool = False,
                 manual_focus: bool = False,
                 auto_exposure: bool = False,
                 manual_exposure: bool = False,
                 gain: bool = False,
                 shutter_speed: bool = False,
                 iso: bool = False,
                 exposure_compensation: bool = False,
                 low_light_compensation: bool = False,
                 auto_white_balance: bool = False,
                 temperature_compensation: bool = False,
                 temperature: bool = False,
                 tint: bool = False,
                 hdr: bool = False,
                 anti_flicker: bool = False,
                 brightness: bool = False,
                 contrast: bool = False,
                 saturation: bool = False,
                 vibrance: bool = False,
                 sharpness: bool = False,
                 ):
        self.name = name
        self.project_name = project_name
        self.default_values = default_values
        self.pan_tilt = TunePanTilt(tune_app, **CameraLocators.pan_tilt) if pan_tilt else None
        self.fov = TuneFov(tune_app, **CameraLocators.fov) if fov else None
        self.zoom = TuneSlider(tune_app, **CameraLocators.zoom) if zoom else None
        self.show_mode = TuneSwitcher(tune_app, **CameraLocators.show_mode) if show_mode else None
        self.built_in_microphone = TuneSwitcher(tune_app, **CameraLocators.built_in_microphone
                                                ) if built_in_microphone else None
        self.hdr = TuneSwitcher(tune_app, **CameraLocators.hdr) if hdr else None
        self.anti_flicker = TuneElementsSelection(tune_app, **CameraLocators.anti_flicker
                                                  ) if anti_flicker else None
        self.auto_focus = TuneSwitcher(tune_app, **CameraLocators.auto_focus) if auto_focus else None
        self.manual_focus = TuneSlider(tune_app, dependent_on_switch=(self.auto_focus, False),
                                       **CameraLocators.manual_focus) if manual_focus else None
        self.auto_exposure = TuneSwitcher(tune_app, **CameraLocators.auto_exposure
                                          ) if auto_exposure else None
        self.manual_exposure = TuneSlider(tune_app, dependent_on_switch=(self.auto_exposure, False),
                                          **CameraLocators.manual_exposure) if manual_exposure else None
        self.gain = TuneSlider(tune_app, dependent_on_switch=(self.auto_exposure, False),
                               **CameraLocators.gain) if gain else None
        self.shutter_speed = TuneSlider(tune_app, dependent_on_switch=(self.auto_exposure, False),
                                        **CameraLocators.shutter_speed) if shutter_speed else None
        self.iso = TuneSlider(tune_app, dependent_on_switch=(self.auto_exposure, False),
                              **CameraLocators.iso) if iso else None
        self.exposure_compensation = TuneSlider(tune_app,
                                                dependent_on_switch=(self.auto_exposure, True),
                                                **CameraLocators.exposure_compensation
                                                ) if exposure_compensation else None
        self.low_light_compensation = TuneSwitcher(tune_app,
                                                   dependent_on_switch=(self.auto_exposure, True),
                                                   **CameraLocators.low_light_compensation
                                                   ) if low_light_compensation else None
        self.auto_white_balance = TuneSwitcher(tune_app, **CameraLocators.auto_white_balance
                                               ) if auto_white_balance else None
        self.temperature_compensation = TuneSlider(tune_app,
                                                   dependent_on_switch=(
                                                       self.auto_white_balance, True),
                                                   **CameraLocators.temperature_compensation
                                                   ) if temperature_compensation else None
        self.temperature = TuneSlider(tune_app,
                                      dependent_on_switch=(self.auto_white_balance, False),
                                      **CameraLocators.temperature) if temperature else None
        self.tint = TuneSlider(tune_app, dependent_on_switch=(self.auto_white_balance, False),
                               **CameraLocators.tint) if tint else None
        self.brightness = TuneSlider(tune_app, **CameraLocators.brightness) if brightness else None
        self.contrast = TuneSlider(tune_app, **CameraLocators.contrast) if contrast else None
        self.saturation = TuneSlider(tune_app, **CameraLocators.saturation) if saturation else None
        self.vibrance = TuneSlider(tune_app, **CameraLocators.vibrance) if vibrance else None
        self.sharpness = TuneSlider(tune_app, **CameraLocators.sharpness) if sharpness else None


class CamerasParametersWrapper(DevicesParametersWrapper):

    def __init__(self, tune_app: TuneElectron):
        super().__init__(tune_app, cameras_info_set, CameraProperties, camera_ui_capabilities,
                         get_camera_default_values)


