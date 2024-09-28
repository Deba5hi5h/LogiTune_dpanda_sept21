import time
from typing import Any, Callable, Iterable, List, Optional

import selenium.common.exceptions

from apps.tune.tune_elements import TuneElements, TuneSlider, TuneSwitcher
from apps.tune.TuneElectron import TuneElectron
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report


class DevicesParametersWrapper:
    def __init__(self, tune_app: TuneElectron, device_info_set: list, device_properties: Callable,
                 device_ui_capabilities: dict, device_default_values_func: Callable):
        self.device_info_set = device_info_set
        self.device_properties = device_properties
        self.device_ui_capabilities = device_ui_capabilities
        self.device_default_values_func = device_default_values_func
        self.update_tune_instance(tune_app)

    def update_tune_instance(self, tune_app: TuneElectron) -> None:
        for idx, camera in enumerate(self.device_info_set):
            default_values = self.device_default_values_func(camera.project_name)
            camera_caps = self.device_ui_capabilities.get(camera.project_name)
            setattr(self, f'device_{idx}', self.device_properties(
                tune_app, camera.name, camera.project_name, default_values, **camera_caps))

    def get_by_name(self, device_name: str) -> Any:
        attributes = list(self.__dir__())
        attributes = attributes[attributes.index('device_0'):attributes.index('__module__')]
        for attr in attributes:
            current_device = self.__getattribute__(attr)
            if current_device.name == device_name:
                return current_device
        raise NameError(f'Provided Device name is missing: {device_name}')


class PersistencyChecker:
    def __init__(self, tune_element: TuneElements):
        self.name = tune_element.name
        self.element = tune_element
        self.expected = None
        self.observed = None
        self.persisted = None

    def are_values_equal(self, margin_of_error: int = 0) -> None:
        margin_of_error = abs(margin_of_error)
        if self.expected is not None and self.observed is not None:
            if isinstance(self.expected, Iterable) and isinstance(self.observed, Iterable):
                self.persisted = True
                for values in list(zip(self.expected, self.observed)):
                    if not self._verify_equality(*values, margin_of_error=margin_of_error):
                        self.persisted = False
                        return
            else:
                self.persisted = self._verify_equality(self.expected, self.observed, margin_of_error)

    @staticmethod
    def _verify_equality(expected: int, observed: int, margin_of_error: int) -> bool:
        if margin_of_error > 0:
            return observed - margin_of_error <= expected <= observed + margin_of_error
        else:
            return expected == observed


class TuneDevicePersistency:
    def __init__(self, device_name: str, device_parameters_wrapper,
                 tune_app: Optional[TuneElectron] = None):
        self.device_parameters = list()
        self.tune_app = tune_app if tune_app else TuneElectron()
        self.tune_app.open_tune_app()
        self.tune_app.click_my_devices()
        self.device = device_parameters_wrapper(self.tune_app).get_by_name(device_name)

    def _get_expected_value(self,
                            tune_element: TuneElements,
                            min_value: Optional[int] = None,
                            max_value: Optional[int] = None) -> Optional[PersistencyChecker]:
        if tune_element is not None:
            tune_element.check_value()
            element_name = tune_element.name.lower().replace(' ', '_')
            default_value = self.device.default_values.get(element_name)
            expected_value = default_value
            while default_value == expected_value:
                if min_value or max_value:
                    expected_value = tune_element.set_random_value(min_value, max_value)
                else:
                    expected_value = tune_element.set_random_value()
                    if type(expected_value) == str:
                        if len(expected_value.split('\n')) > 1:  # It means that element consists of title and description
                            expected_value = expected_value.split('\n')[0]  # Take only title

            checked_value = tune_element.check_value()
            if isinstance(tune_element, TuneSlider) and tune_element.step is not None:
                assert expected_value == checked_value, \
                    f'Expected: {expected_value}, Observed: {checked_value}'
            persistency_checker = PersistencyChecker(tune_element)
            persistency_checker.expected = checked_value
            return persistency_checker

    @staticmethod
    def _set_switch(tune_switch: TuneSwitcher, value: bool) -> Optional[bool]:
        if tune_switch is not None:
            if value:
                tune_switch.switch_on()
                switch_value = True
            else:
                tune_switch.switch_off()
                switch_value = False
            time.sleep(0.5)
            assert switch_value == tune_switch.check_value(), f'Not able to set switch "{tune_switch.name}".'
            return switch_value

    @staticmethod
    def _compare_current_value_with_expected(tune_element: TuneElements,
                                             group: List[PersistencyChecker],
                                             margin_of_error: int = 0) -> None:
        if tune_element is not None:
            for element in group:
                if element and tune_element.name == element.name and tune_element == element.element:
                    try:
                        element.observed = tune_element.check_value()
                    except selenium.common.exceptions.TimeoutException:
                        tune_element.check_switch_dependency()
                        element.observed = tune_element.check_value()
                    element.are_values_equal(margin_of_error)
                    break

    def _set_and_get_switch_value(self, tune_switch: TuneSwitcher) -> Optional[PersistencyChecker]:
        if tune_switch is not None:
            tune_switch.check_value(silent_check=True)
            element_name = tune_switch.name.lower().replace('(', ' ').replace(')', ' ').strip().replace(' ', '_').replace('-', '_')
            if len(element_name.split()) > 1:       # It means that element consists of title and description
                element_name = element_name.split()[0]
            not_default_value = not self.device.default_values.get(element_name)
            switch_value = self._set_switch(tune_switch, not_default_value)
            persistency_checker = PersistencyChecker(tune_switch)
            persistency_checker.expected = switch_value
            return persistency_checker

    @staticmethod
    def _check_element_persistency(tune_element: TuneElements, group: List[PersistencyChecker]
                                   ) -> bool:
        if tune_element is not None:
            for element in group:
                if element and tune_element.name == element.name:
                    return element.persisted

    def _persistency_results(self) -> None:
        self.device_parameters = [element for element in self.device_parameters
                                  if element is not None]
        if all([result.persisted for result in self.device_parameters]):
            Report.logPass(f'All parameters of {self.device.name} persisted correctly')
        else:
            Report.logFail(f'Not all parameters of {self.device.name} persisted:')
            for element in self.device_parameters:
                if not element.persisted:
                    Report.logFail(f'"{element.name}" - Expected: {element.expected}, '
                                   f'Observed: {element.observed}')

    def _reconnect_device(self, acroname_automatic: bool) -> None:
        if acroname_automatic:
            time.sleep(4)
            disconnect_device(device_name=self.device.name)
            time.sleep(5)
            connect_device(device_name=self.device.name)
            time.sleep(7)
        else:
            reconnection_done = False
            while not reconnection_done:
                if input('Click "y" and ENTER to continue...') == 'y':
                    reconnection_done = True

    def check_persistency(self):
        pass
