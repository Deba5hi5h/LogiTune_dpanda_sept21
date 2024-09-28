import random

from apps.tune.camera_streaming import initialize_camera_streaming
from apps.tune.tc_scenarios.base_scenarios import BaseScenarios
from extentreport.report import Report


class LightPagesScenarios(BaseScenarios):

    def tc_smart_activation_for_any_camera(self, device_name: str) -> None:
        self.tune_pages.home.click_devices_tab()
        self.tune_pages.home.click_device_button_by_name(device_name)
        available_cameras = self.tune_pages.light_page.get_available_cameras()
        Report.logInfo(f'Cameras available: {available_cameras}:')
        self.tune_pages.light_page.click_smart_activation_button()
        self.tune_pages.light_page.click_smart_activation_popup_any_camera_radio()
        self.tune_pages.light_page.click_smart_activation_popup_save_button()
        self._assert(
            self.tune_pages.light_page.verify_smart_activation_chosen_state('Any Camera'),
            log_pass='Smart Activation chosen to "Any Camera"',
            log_fail=f'Smart Activation was not set to "Any Camera"',
            screenshot_on_pass=True,
        )
        self.tune_pages.light_page.click_back_button()
        self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                 skip_exception=True)
        self._assert(
            self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
            log_pass=f'"{device_name}" switch has correct state - False',
            log_fail=f'"{device_name}" has wrong state - True, expected: False',
            screenshot_on_pass=True,
        )
        camera_stream = initialize_camera_streaming()
        already_streamed = list()
        for _ in range(min(2, len(available_cameras))):
            try:
                chosen_camera = random.choice(available_cameras)
                while chosen_camera in already_streamed:
                    chosen_camera = random.choice(available_cameras)
                Report.logInfo(f'Start stream for camera: {chosen_camera}')
                camera_stream.start_stream(chosen_camera)
                Report.logInfo(f'Camera started streaming: {chosen_camera}')
                self.tune_pages.home.wait_until_element_switched_by_name(device_name, True,
                                                                         skip_exception=True)
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is True,
                    log_pass=f'"{device_name}" switch has correct state during streaming - True. '
                             f'Camera: {chosen_camera}',
                    log_fail=f'"{device_name}" has wrong state during streaming - False, '
                             f'expected: True. Camera: {chosen_camera}',
                    screenshot_on_pass=True,
                )
                camera_stream.stop_stream()
                Report.logInfo(f'Camera stopped streaming: {chosen_camera}')
                self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                         skip_exception=True)
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
                    log_pass=f'"{device_name}" switch has correct state while not streaming '
                             f'- False. Camera: {chosen_camera}',
                    log_fail=f'"{device_name}" has wrong state while not streaming - True, '
                             f'expected: False. Camera: {chosen_camera}',
                    screenshot_on_pass=True,
                )
                already_streamed.append(chosen_camera)
            except AssertionError:
                Report.logInfo(f'Stopping camera stream after exception occurred')
                camera_stream.stop_stream()
        Report.logPass(f'Smart activation for "Any Camera" is working as expected')

    def tc_smart_activation_disabled(self, device_name: str) -> None:
        self.tune_pages.home.click_devices_tab()
        self.tune_pages.home.click_device_button_by_name(device_name)
        available_cameras = self.tune_pages.light_page.get_available_cameras()
        Report.logInfo(f'Cameras available: {available_cameras}:')
        self.tune_pages.light_page.click_smart_activation_button()
        self.tune_pages.light_page.click_smart_activation_popup_disabled_radio()
        self.tune_pages.light_page.click_smart_activation_popup_save_button()
        self._assert(
            self.tune_pages.light_page.verify_smart_activation_chosen_state('Disabled'),
            log_pass='Smart Activation chosen to "Disabled"',
            log_fail=f'Smart Activation was not set to "Disabled"',
            screenshot_on_pass=True,
        )
        self.tune_pages.light_page.click_back_button()
        self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                 skip_exception=True)
        self._assert(
            self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
            log_pass=f'"{device_name}" switch has correct state - False',
            log_fail=f'"{device_name}" has wrong state - True, expected: False',
            screenshot_on_pass=True,
        )
        camera_stream = initialize_camera_streaming()
        already_streamed = list()
        for _ in range(min(2, len(available_cameras))):
            try:
                chosen_camera = random.choice(available_cameras)
                while chosen_camera in already_streamed:
                    chosen_camera = random.choice(available_cameras)
                Report.logInfo(f'Start stream for camera: {chosen_camera}')
                camera_stream.start_stream(chosen_camera)
                Report.logInfo(f'Camera started streaming: {chosen_camera}')
                self.tune_pages.home.wait_until_element_switched_by_name(
                    device_name=device_name,
                    switch_value=True,
                    timeout=5,
                    skip_exception=True
                )
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
                    log_pass=f'"{device_name}" switch has correct state during streaming - False. '
                             f'Camera: {chosen_camera}',
                    log_fail=f'"{device_name}" has wrong state during streaming - True, '
                             f'expected: False. Camera: {chosen_camera}',
                    screenshot_on_pass=True,
                )
                camera_stream.stop_stream()
                Report.logInfo(f'Camera stopped streaming: {chosen_camera}')
                self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                         skip_exception=True)
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
                    log_pass=f'"{device_name}" switch has correct state while not streaming '
                             f'- False. Camera: {chosen_camera}',
                    log_fail=f'"{device_name}" has wrong state while not streaming - True, '
                             f'expected: False. Camera: {chosen_camera}',
                    screenshot_on_pass=True,
                )
                already_streamed.append(chosen_camera)
            except AssertionError:
                Report.logInfo(f'Stopping camera stream after exception occurred')
                camera_stream.stop_stream()
        Report.logPass(f'Smart activation "Disabled" is working as expected')

    def tc_smart_activation_for_chosen_cameras(self, device_name: str) -> None:
        self.tune_pages.home.click_devices_tab()
        self.tune_pages.home.click_device_button_by_name(device_name)
        try:
            available_cameras = self.tune_pages.light_page.get_available_cameras()
        except Exception as e:
            Report.logException('There is too little cameras available (Minimum 2)')
            raise e
        Report.logInfo(f'Cameras available: {available_cameras}:')
        self.tune_pages.light_page.click_smart_activation_button()
        chosen_camera = random.choice(available_cameras)
        Report.logInfo(f'Camera chosen for Smart Activation: {chosen_camera}')
        self.tune_pages.light_page.click_smart_activation_popup_available_cameras_checkbox_by_name(
            chosen_camera)
        self.tune_pages.light_page.click_smart_activation_popup_save_button()
        self._assert(
            self.tune_pages.light_page.verify_smart_activation_chosen_state(chosen_camera),
            log_pass=f'Smart Activation chosen to "{chosen_camera}"',
            log_fail=f'Smart Activation was not set to "{chosen_camera}"',
            screenshot_on_pass=True,
        )
        self.tune_pages.light_page.click_back_button()
        self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                 skip_exception=True)
        self._assert(
            self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
            log_pass=f'"{device_name}" switch has correct state - False',
            log_fail=f'"{device_name}" has wrong state - True, expected: False',
            screenshot_on_pass=True,
        )
        camera_stream = initialize_camera_streaming()
        to_stream = [chosen_camera]
        other_camera = random.choice(available_cameras)
        while other_camera in to_stream:
            other_camera = random.choice(available_cameras)
        to_stream.append(other_camera)
        random.shuffle(to_stream)
        for camera_name in to_stream:
            try:
                Report.logInfo(f'Start stream for camera: {camera_name}')
                camera_stream.start_stream(camera_name)
                Report.logInfo(f'Camera started streaming: {camera_name}')
                valid_state = True if camera_name == chosen_camera else False
                self.tune_pages.home.wait_until_element_switched_by_name(
                    device_name=device_name,
                    switch_value=True,
                    timeout=5,
                    skip_exception=True
                )
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is valid_state,
                    log_pass=f'"{device_name}" switch has correct state during streaming '
                             f'- {valid_state}. Camera: {camera_name}',
                    log_fail=f'"{device_name}" has wrong state during streaming - {not valid_state}, '
                             f'expected: {valid_state}. Camera: {camera_name}',
                    screenshot_on_pass=True,
                )
                camera_stream.stop_stream()
                Report.logInfo(f'Camera stopped streaming: {chosen_camera}')
                self.tune_pages.home.wait_until_element_switched_by_name(device_name, False,
                                                                         skip_exception=True)
                self._assert(
                    self.tune_pages.home.verify_device_switch_by_name(device_name) is False,
                    log_pass=f'"{device_name}" switch has correct state while not streaming'
                             f' - False. Camera: {camera_name}',
                    log_fail=f'"{device_name}" has wrong state while not streaming - True, '
                             f'expected: False. Camera: {camera_name}',
                    screenshot_on_pass=True,
                )
            except AssertionError:
                Report.logInfo(f'Stopping camera stream after exception occurred')
                camera_stream.stop_stream()
        Report.logPass(f'Smart activation for "{chosen_camera}" is working as expected')
