import base64
import cv2
import json
import queue
import re
import random
import subprocess
import sys
import time
import numpy as np

from io import BytesIO
from subprocess import check_output
from threading import Thread
from typing import Dict, List, Optional, TextIO, Tuple, Union
from datetime import datetime
from base import global_variables
from apps.tune.camera.camera import CamerasParametersWrapper, CameraProperties
from apps.tune.camera.camera_filters import camera_filters
from apps.tune.camera.camera_locators import CameraWindows
from apps.tune.devices_base_helpers import TuneDevicePersistency
from apps.tune.helpers import exception_handler
from apps.tune.tune_elements import TuneElements, TuneElementsClass
from apps.tune.TuneElectron import TuneElectron
from common.image_settings import calculate_image_properties
from common.platform_helper import get_custom_platform
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from locators.tunes_ui_locators import TunesAppLocators


class TuneCameraMethods:
    def __init__(self, camera_name: str, tune_app: Optional[TuneElectron] = None):
        self.tune_app = tune_app if tune_app else TuneElectron()
        self.camera: CameraProperties = CamerasParametersWrapper(
            self.tune_app).get_by_name(camera_name)

    def _open_camera_settings(self, connect_cam: bool = False, image_adjustments_tab: bool = False,
                              restart_tune: bool = True):
        if restart_tune:
            self.tune_app.open_tune_app()
        try:
            self.tune_app.click_my_devices()
        except AttributeError as e:
            print(repr(e))
        if connect_cam:
            connect_device(self.camera.name)
            time.sleep(7)
        try:
            self.tune_app.click_device(self.camera.name)
        except Exception as e:
            print(repr(e))
        time.sleep(2)
        if image_adjustments_tab:
            self.tune_app.click_image_adjustment()

    def _verify_filter_applied(self) -> Optional[str]:
        self.tune_app.click_adjustments_tab()
        params = ['auto_white_balance', 'brightness', 'contrast', 'saturation', 'sharpness']
        filter_applied = {param: None for param in params}
        filter_name = None
        for param in params:
            filter_applied[param] = self.camera.__getattribute__(param).check_value()
        for camera_filter in camera_filters:
            filter_name = camera_filter.verify_parameters(**filter_applied)
            if filter_name:
                break
        self.tune_app.click_color_filters_tab()
        return filter_name

    def _click_restart_to_default(self):
        try:
            self.tune_app.click_adjustments_reset_to_default()
        except Exception as e:
            self.tune_app.click_adjustments_dropdown_button()
            self.tune_app.click_adjustments_reset_to_default()

    def _factory_reset_camera(self):
        try:
            self.tune_app.click_back_from_image_adjustments()
        except Exception as e:
            print(f'_factory_reset_camera error: {repr(e)}')
        self.tune_app.click_info_button()
        self.tune_app.click_factory_reset()
        time.sleep(1)
        self.tune_app.click_proceed_to_factory_reset()
        time.sleep(2)
        if not self.tune_app.verify_element(TunesAppLocators.MY_DEVICES):
            disconnect_device(device_name=self.camera.name)
            time.sleep(5)
            connect_device(device_name=self.camera.name)
        time.sleep(7)

    def _change_parameters_to_different_than_default(self, default_parameters: dict):
        for parameter_name, parameter_value in default_parameters.items():
            if isinstance(parameter_value, bool):
                if parameter_value == self.camera.__getattribute__(parameter_name).check_value():
                    self.camera.__getattribute__(parameter_name).toggle()
                Report.logInfo(f'Parameter "{parameter_name}" '
                               f'value toggled to {not parameter_value}')
            else:
                new_value = parameter_value
                while new_value == parameter_value:
                    new_value = self.camera.__getattribute__(parameter_name).set_random_value()
                Report.logInfo(f'Parameter "{parameter_name}" value changed to {new_value}')

    def _verify_default_parameters_values(self, default_parameters: dict, invalid_values: dict
                                          ) -> None:
        for parameter_name, parameter_value in default_parameters.items():
            value_after_reset = self.camera.__getattribute__(parameter_name).check_value()
            if value_after_reset != parameter_value:
                invalid_values[parameter_name] = {'expected': parameter_value,
                                                  'observed': value_after_reset}
            self._report_result(
                value_after_reset == parameter_value,
                f'Valid reset to default of "{parameter_name}" value - {parameter_value}',
                f'Invalid reset to default of "{parameter_name}" value - '
                f'Expected: {parameter_value}, Observed: {value_after_reset}'
            )

    def _divide_parameters(self) -> Tuple[Dict[str, Union[bool, int]], Dict[str, Union[bool, int]]]:
        camera_settings = dict()
        image_adjustments = dict()
        for parameter_name, default_value in self.camera.default_values.items():
            if parameter_name == 'pan_tilt_steps':
                continue
            if parameter_name in ('fov', 'zoom', 'show_mode'):
                camera_settings[parameter_name] = default_value
            else:
                image_adjustments[parameter_name] = default_value
        return camera_settings, image_adjustments

    def _get_previous_camera_settings(self, valid_parameters: list, previous_value: dict):
        if 'fov' in valid_parameters:
            previous_value['fov'] = self.camera.fov.set_random_fov()
        if 'zoom' in valid_parameters:
            previous_value['zoom'] = self.camera.zoom.set_random_value()
        if 'show_mode' in valid_parameters:
            self.camera.show_mode.switch_off()
            previous_value['show_mode'] = False

    def _verify_default_camera_settings(self, valid_parameters: list, previous_value: dict):
        if 'fov' in valid_parameters:
            fov_after_reset = self.camera.fov.check_value()
            self._report_result(
                fov_after_reset == 90,
                f'Valid reset to default of Field of View - '
                f'Prev: {previous_value.get("fov")}°, Current: {fov_after_reset}°',
                f'Invalid reset to default of FOV - Expected: 90°, Observed: {fov_after_reset}°'
            )
        if 'zoom' in valid_parameters:
            zoom_after_reset = self.camera.zoom.check_value()
            self._report_result(
                zoom_after_reset == 100,
                f'Valid reset to default of Zoom - '
                f'Prev: {previous_value.get("zoom")}, Current: {zoom_after_reset}',
                f'Invalid reset to default of Zoom - Expected: 100, Observed: {zoom_after_reset}'
            )
        if 'show_mode' in valid_parameters:
            show_mode_after_reset = self.camera.show_mode.check_value()
            self._report_result(
                previous_value.get('show_mode') != show_mode_after_reset
                and show_mode_after_reset is True,
                f'Valid reset to default of Show Mode - '
                f'Prev: {previous_value.get("show_mode")}, Current: {show_mode_after_reset}',
                f'Invalid reset to default of Show Mode - '
                f'Expected: True, Observed: {show_mode_after_reset}'
            )

    def _get_previous_image_adjustments(self, valid_parameters: list, previous_value: dict):
        switches = ['low_light_compensation', 'focus', 'exposure',
                    'white_balance', 'hdr']
        sliders = ['brightness', 'contrast', 'saturation', 'sharpness']
        valid_switches = [switch for switch in switches if switch in valid_parameters]
        valid_sliders = [slider for slider in sliders if slider in valid_parameters]
        for switch in valid_switches:
            if switch == 'low_light_compensation' and self.camera.project_name not in (
                    'cezanne', 'degas'):
                self.camera.__getattribute__(switch).switch_on()
            else:
                self.camera.__getattribute__(switch).switch_off()
            previous_value[switch] = self.camera.__getattribute__(switch).check_value()

        for slider in valid_sliders:
            slider_value = 128
            while slider_value == 128:
                slider_value = self.camera.__getattribute__(slider).change_value_randomly()
            previous_value[slider] = self.camera.__getattribute__(slider).check_value()

    def _verify_default_image_adjustments(self, valid_parameters: list, previous_value: dict):
        switches = ['low_light_compensation', 'focus', 'exposure',
                    'white_balance', 'hdr']
        sliders = ['brightness', 'contrast', 'saturation', 'sharpness']
        valid_switches = [switch for switch in switches if switch in valid_parameters]
        valid_sliders = [slider for slider in sliders if slider in valid_parameters]

        for switch in valid_switches:
            name = self.camera.__getattribute__(switch).name
            after_reset = self.camera.__getattribute__(switch).check_value()
            if switch == 'low_light_compensation' and self.camera.project_name not in (
                    'cezanne', 'degas'):
                valid_value = False
            else:
                valid_value = True
            self._report_result(
                after_reset is valid_value,
                f'Valid reset to default of {name} - '
                f'Prev: {previous_value.get(switch)}, Current: {after_reset}',
                f'Invalid reset to default of {name} - '
                f'Expected: {valid_value}, Observed: {after_reset}'
            )

        for slider in valid_sliders:
            name = self.camera.__getattribute__(slider).name
            after_reset = self.camera.__getattribute__(slider).check_value()
            self._report_result(
                after_reset == 128,
                f'Valid reset to default of {name} - '
                f'Prev: {previous_value.get(slider)}, Current: {after_reset}',
                f'Invalid reset to default of {name} - Expected: 128, Observed: {after_reset}'
            )

    @staticmethod
    def _report_result(condition: bool, pass_msg: str, fail_msg: str, screenshot: bool = False
                       ) -> None:
        if condition:
            Report.logPass(pass_msg, screenshot=screenshot)
        else:
            Report.logFail(fail_msg)

    def _get_valid_parameters(self) -> dict:
        output = dict()
        for name, attr in self.camera.__dict__.items():
            for tune_element in TuneElementsClass:
                if isinstance(attr, tune_element):
                    output[name] = attr
        return output

    def _validate_visibility_in_window(self, window_name: str, parameters: List[TuneElements]
                                       ) -> None:
        window_parameters = list()
        for parameter in parameters:
            if parameter.window_name == window_name:
                window_parameters.append(parameter)
        for parameter in window_parameters:
            self._report_result(parameter.is_visible(), f'{parameter.name} displayed',
                                f'{parameter.name} not displayed')

    def _check_mic_prompts(self, mic_state: bool):
        mic_state = 'enable' if mic_state else 'disable'
        default_prompt_title = 'Built-in Microphone'
        default_prompt_message = f'To {mic_state} built-in microphone, a device reboot is required.'
        manual_reconnect_title = 'Reconnect the device'
        manual_reconnect_message = 'Unplug and replug the device to complete the process.'
        auto_reconnect_title = 'Rebooting device'
        auto_reconnect_message = 'This may take a few seconds, please wait.'
        time.sleep(0.5)
        prompt_title = self.tune_app.look_element(TunesAppLocators.MIC_REBOOT_TITLE).text
        prompt_message = self.tune_app.look_element(TunesAppLocators.MIC_REBOOT_MESSAGE).text
        self._report_result(default_prompt_title == prompt_title,
                            f'Valid title shown in prompt',
                            f'Invalid title: {prompt_title}\nShould be: {default_prompt_title}')
        self._report_result(default_prompt_message == prompt_message,
                            f'Valid message shown in prompt',
                            f'Invalid message: {prompt_message}\n'
                            f'Should be: {default_prompt_message}')
        self.tune_app.look_element(TunesAppLocators.MIC_REBOOT).click()
        time.sleep(0.1)
        reconnect_message = self.tune_app.look_element(TunesAppLocators.MIC_REBOOT_MESSAGE).text
        reconnect_title = self.tune_app.look_element(TunesAppLocators.MIC_REBOOT_TITLE).text
        if reconnect_title == manual_reconnect_title:
            valid_reconnect_title = manual_reconnect_title
            valid_reconnect_message = manual_reconnect_message
        elif reconnect_title == auto_reconnect_title:
            valid_reconnect_title = auto_reconnect_title
            valid_reconnect_message = auto_reconnect_message
        else:
            raise NameError(f'Invalid title for reconnecting prompt: {reconnect_title}')
        self._report_result(reconnect_title == valid_reconnect_title,
                            f'Valid title shown in reconnect prompt',
                            f'Invalid title: {reconnect_title}\n'
                            f'Should be: {valid_reconnect_title}')
        self._report_result(reconnect_message == valid_reconnect_message,
                            f'Valid message shown in reconnect prompt',
                            f'Invalid message: {reconnect_message}\n'
                            f'Should be: {valid_reconnect_message}')
        if reconnect_title == manual_reconnect_title:
            disconnect_device(self.camera.name)
            time.sleep(5)
            connect_device(self.camera.name)
        self.tune_app.verify_element(TunesAppLocators.SUPPORTED_DEVICES_BUTTON,
                                     wait_for_visibility=True)
        self.tune_app.verify_device_name_displayed(self.camera.name)
        time.sleep(2)

    def _verify_microphone_shown_in_system(self, mic_should_be_shown: bool = True,
                                           retries: int = 20) -> bool:
        result = False
        current_os = get_custom_platform()
        if current_os == 'windows':
            command = "powershell.exe Get-PnpDevice -Class 'AudioEndpoint' -Status 'OK'"
        elif current_os == 'macos':
            command = "system_profiler SPAudioDataType"
        else:
            raise OSError('Linux is not supported!')

        for _ in range(retries):
            system_audio_data = None
            try:
                system_audio_data = check_output(command.split(' '))
                try:
                    system_audio_data = system_audio_data.decode('utf-8')
                except UnicodeDecodeError:
                    system_audio_data = system_audio_data.decode('latin-1')
                if not ((self.camera.name.lower() in system_audio_data.lower())
                        ^ mic_should_be_shown):  # XNOR logic check
                    Report.logInfo(f'Microphone {"" if mic_should_be_shown else "not "}visible '
                                   f'as expected:\n{system_audio_data}')
                    result = True
                    break
            except subprocess.CalledProcessError:
                if not mic_should_be_shown:
                    Report.logInfo(f'Microphone {"" if mic_should_be_shown else "not "}visible '
                                   f'as expected:\n{system_audio_data}')
                    result = True
                    break
                else:
                    Report.logException(f'There was an issue with getting System Audio data!')
            except Exception as e:
                Report.logInfo(f'While verifying microphone state in the system, '
                               f'exception occurred: {e}\n'
                               f'Output: {system_audio_data}')
            time.sleep(1)
        if not result:
            system_audio_data = check_output(command.split(' ')).decode('utf-8')
            Report.logInfo(f'Something went wrong, system audio report: \n{system_audio_data}')
        return result

    def change_built_in_microphone(self, mic_turned_on: bool = True) -> bool:
        self._open_camera_settings()
        if self.camera.built_in_microphone.check_value() != mic_turned_on:
            Report.logInfo(f'Built-in microphone has wrong value, trying to change it to '
                           f'{"ON" if mic_turned_on else "OFF"}')
            self.camera.built_in_microphone.toggle()
            self.tune_app.look_element(TunesAppLocators.MIC_REBOOT).click()
            self.tune_app.verify_element(TunesAppLocators.SUPPORTED_DEVICES_BUTTON,
                                         wait_for_visibility=True)
            self.tune_app.verify_device_name_displayed(self.camera.name)
            time.sleep(2)
            self._open_camera_settings(restart_tune=False)
            result = self.camera.built_in_microphone.check_value() == mic_turned_on
            self._report_result(result,
                                f'Built-in microphone value changed properly to '
                                f'{"ON" if mic_turned_on else "OFF"}',
                                f'Built-in microphone failed to change its value')
            return result
        else:
            Report.logInfo(f'Built-in microphone already has valid state')
            return True

    @exception_handler
    def tc_connect_webcam_and_verify_parameters(self):
        self._open_camera_settings(connect_cam=True)
        self._report_result(self.tune_app.verify_device_connected() and
                            self.tune_app.verify_device_name_displayed(self.camera.name),
                            f'{self.camera.name} - Connected displayed',
                            f'{self.camera.name} - Connected not displayed')
        valid_parameters = self._get_valid_parameters()
        if 'zoom' in valid_parameters:
            while self.camera.zoom.check_value() == 100:
                self.camera.zoom.set_random_value()
        valid_parameters = list(valid_parameters.values())
        self._validate_visibility_in_window(CameraWindows.camera_settings, valid_parameters)
        self.tune_app.click_image_adjustment()
        self._validate_visibility_in_window(CameraWindows.image_adjustments, valid_parameters)
        try:
            self._factory_reset_camera()
        except Exception as e:
            Report.logInfo(f'Unable to factory reset the camera: {e}')

    @exception_handler
    def tc_built_in_microphone(self):
        self._open_camera_settings()
        for _ in range(2):
            mic_state = self.camera.built_in_microphone.toggle()
            self._check_mic_prompts(mic_state)
            self._open_camera_settings(restart_tune=False)
            mic_state_after_change = self.camera.built_in_microphone.check_value()
            self._report_result(mic_state == mic_state_after_change,
                                f'Microphone value changed properly!',
                                f'Microphone value has not changed - Expected: {mic_state}, '
                                f'Observed: {mic_state_after_change}')
            self._report_result(self._verify_microphone_shown_in_system(mic_state),
                                f'Microphone is {"" if mic_state else "not "}'
                                f'visible in the system as expected!',
                                f'Wrong microphone report from the system - Expected: {mic_state},'
                                f'Observed: {not mic_state}')

    @staticmethod
    def _check_zoom_between_two_frames(frame_original: bytes, frame_zoomed: bytes
                                       ) -> Tuple[int, np.array]:
        img_original = cv2.imdecode(frame_original, cv2.IMREAD_GRAYSCALE)
        img_zoomed = cv2.imdecode(frame_zoomed, cv2.IMREAD_GRAYSCALE)

        sift = cv2.SIFT_create()

        kp1, des1 = sift.detectAndCompute(img_original, None)
        kp2, des2 = sift.detectAndCompute(img_zoomed, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.2 * n.distance:
                good.append(m)
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 2)

        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 3.0)
        scale_x = np.sqrt(H[0, 0] ** 2 + H[1, 0] ** 2)
        scale_y = np.sqrt(H[0, 1] ** 2 + H[1, 1] ** 2)
        zoom_factor = (scale_x + scale_y) / 2
        h, w = img_zoomed.shape
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
        transformed_corners = cv2.perspectiveTransform(corners, H)
        match_lines = cv2.drawMatchesKnn(img_original, kp1, img_zoomed, kp2, [[el] for el in good],
                                         None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        Report.logInfoWithCustomSS(f'Found filtered matches: {len(good)}', match_lines)

        return 1 / zoom_factor, transformed_corners

    def _get_current_camera_video_frame(self) -> np.array:
        time.sleep(2)
        video_element = self.tune_app.driver.find_element('xpath', '//video')

        script = """
            var video = arguments[0];
            var canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            return canvas.toDataURL('image/png').substring(22);  // Remove the data:image/png;base64, part
        """
        temp = self.tune_app.driver.execute_script(script, video_element)
        captured_img = base64.b64decode(temp)
        return np.frombuffer(captured_img, np.uint8)

    def _capture_frame_to_directory(self, name: str = None) -> str:
        frame_bytes = self._get_current_camera_video_frame()
        img = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)
        image_path = global_variables.reportPath + '/' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S" + ".png")
        cv2.imwrite(image_path, img)
        return image_path

    @staticmethod
    def _get_middle_point_of_polygon(polygon: np.ndarray) -> Tuple[int, ...]:
        return tuple(map(int, np.mean(polygon, axis=0).tolist()[0]))

    @staticmethod
    def _get_resized_img_in_b64(img_array: np.ndarray) -> str:
        resized_img = cv2.resize(img_array, (360, 205), interpolation=cv2.INTER_AREA)
        is_success, buffer = cv2.imencode(".jpg", resized_img)

        io_buf = BytesIO(buffer)
        return base64.b64encode(io_buf.getvalue()).decode("utf-8")

    @exception_handler
    def tc_pan_tilt(self, retry: int = 3):
        if retry == 0:
            Report.logException("There was no way to find match between Zooms. Probably bad view.")
            return
        self._open_camera_settings()
        if self.camera.fov is not None:
            Report.logInfo("Setting FoV to 90 deg")
            self.camera.fov.set_fov(90)
        Report.logInfo("Checking current zoom value")
        current_zoom_value = self.camera.zoom.check_value()
        Report.logInfo(f"Current Zoom Value is: {current_zoom_value}")
        if current_zoom_value != self.camera.zoom.min_border:
            Report.logInfo(f"Setting Camera zoom value to {self.camera.zoom.min_border}")
            self.camera.zoom.change_to_exact_value(self.camera.zoom.min_border)
        Report.logInfo(f"Checking if Zoom value is {self.camera.zoom.min_border}")
        self._report_result(
            self.camera.zoom.check_value() == self.camera.zoom.min_border,
            pass_msg=f"Starting Zoom value is {self.camera.zoom.min_border} as intended",
            fail_msg=f"Starting Zoom value differs from {self.camera.zoom.min_border} which is NOK",
            screenshot=True
        )

        time.sleep(5)
        not_zoomed_frame = self._get_current_camera_video_frame()
        img_not_zoomed = cv2.imdecode(not_zoomed_frame, cv2.IMREAD_COLOR)
        size_x, size_y = img_not_zoomed.shape[1::-1]

        set_zoom_value = self.camera.zoom.change_to_exact_value(random.randint(200, 350))
        Report.logInfo(f"Zoom value set to: {set_zoom_value}", screenshot=True)

        values_to_check = ((random.randint(0, 100), random.randint(0, 100), ) for _ in range(5))

        for percent_x, percent_y in values_to_check:
            img_not_zoomed_copy = np.copy(img_not_zoomed)
            Report.logInfo(f"Testing Pan-Tilt percent x: {percent_x}, percent y: {percent_y}")
            self.camera.pan_tilt.set_draggable_position_percent(percent_x, percent_y)
            Report.logInfo(f"Pan Tilt Desired position set to: x: {percent_x}% and y: {percent_y}%", screenshot=True)

            zoomed_frame = self._get_current_camera_video_frame()
            try:
                zoom_factor, corners = self._check_zoom_between_two_frames(
                    not_zoomed_frame, zoomed_frame)
            except cv2.error:
                Report.logInfo("Was not able to find Zoom match -> retrying")
                return self.tc_pan_tilt(retry - 1)

            middle_point = self._get_middle_point_of_polygon(corners)

            points = corners.reshape(-1, 2)

            x_min, y_min = np.min(points, axis=0)
            x_max, y_max = np.max(points, axis=0)

            zoomed_width = x_max - x_min
            zoomed_height = y_max - y_min

            zoomed_middle_x, zoomed_middle_y = middle_point

            observed_percent_x = (zoomed_middle_x - zoomed_width/2)/(size_x - zoomed_width) * 100
            observed_percent_y = (zoomed_middle_y - zoomed_height/2)/(size_y - zoomed_height) * 100

            cv2.circle(img_not_zoomed_copy, tuple(map(int, middle_point)),
                       color=(0, 255, 0), radius=8, thickness=-1)

            cv2.polylines(img_not_zoomed_copy, [np.int32(corners)],
                          True, (0, 255, 0), 3, cv2.LINE_AA)

            Report.logInfoWithCustomSS(f'Zoomed image center', screenshot=img_not_zoomed_copy)
            Report.logInfo(f"Zoom factor is: {zoom_factor}")

            Report.logInfoWithCustomSS(f'Zoomed image center', screenshot=img_not_zoomed_copy)

            Report.logInfo(f"Expected percent x: {percent_x}%, observed percent x: {observed_percent_x}%, "
                           f"Expected percent y: {percent_y}%, observed percent y: {observed_percent_y}%")

            max_error = 5

            zoom_condition = (abs(percent_x - observed_percent_x) < max_error
                              and abs(percent_y - observed_percent_y) < max_error)

            self._report_result(
                condition=zoom_condition,
                pass_msg=f"Observed Pan Tilt position matches maximum error: {max_error}%",
                fail_msg=f"Observed Pan Tilt position does not match maximum error {max_error}%"
            )

    @exception_handler
    def tc_zoom_in_out(self, retry: int = 3):
        if retry == 0:
            Report.logException("There was no way to find match between Zooms. Probably bad view.")
            return
        self._open_camera_settings()
        if self.camera.fov is not None:
            Report.logInfo("Setting FoV to 90 deg")
            self.camera.fov.set_fov(90)

        Report.logInfo("Checking current zoom value")
        current_zoom_value = self.camera.zoom.check_value()
        Report.logInfo(f"Current Zoom Value is: {current_zoom_value}")
        if current_zoom_value != self.camera.zoom.min_border:
            Report.logInfo(f"Setting Camera zoom value to {self.camera.zoom.min_border}")
            self.camera.zoom.change_to_exact_value(self.camera.zoom.min_border)
        Report.logInfo(f"Checking if Zoom value is {self.camera.zoom.min_border}")
        self._report_result(
            self.camera.zoom.check_value() == self.camera.zoom.min_border,
            pass_msg=f"Starting Zoom value is {self.camera.zoom.min_border} as intended",
            fail_msg=f"Starting Zoom value differs from {self.camera.zoom.min_border} which is NOK",
            screenshot=True
        )

        time.sleep(5)
        not_zoomed_frame = self._get_current_camera_video_frame()

        step = self.camera.zoom.step if self.camera.zoom.step else 20
        start_zoom_value = self.camera.zoom.change_value_randomly()
        while not self.camera.zoom.min_border + step < start_zoom_value < self.camera.zoom.max_border:
            start_zoom_value = self.camera.zoom.change_value_randomly()
        time.sleep(5)
        Report.logInfo(f"Zoom value set to: {start_zoom_value}", screenshot=True)

        zoomed_frame = self._get_current_camera_video_frame()
        try:
            zoom_factor, corners = self._check_zoom_between_two_frames(not_zoomed_frame,
                                                                       zoomed_frame)
        except cv2.error:
            Report.logInfo("Was not able to find Zoom match -> retrying")
            return self.tc_zoom_in_out(retry-1)

        img_original_color = cv2.imdecode(not_zoomed_frame, cv2.IMREAD_COLOR)
        cv2.polylines(img_original_color, [np.int32(corners)],
                      True, (0, 255, 0), 3, cv2.LINE_AA)

        Report.logInfoWithCustomSS(f'Zoomed image center', screenshot=img_original_color)
        Report.logInfo(f"Zoom factor is: {zoom_factor}")

        low_expected_zoom = start_zoom_value - 40
        high_expected_zoom = start_zoom_value + 40

        self._report_result(condition=low_expected_zoom < zoom_factor * 100 < high_expected_zoom,
                            pass_msg="Noticed zoom matches expected zoom with error margin",
                            fail_msg="Noticed zoom does not match expected zoom with error margin")

        self.camera.zoom.change_to_exact_value(
            (start_zoom_value + self.camera.zoom.min_border) // 2)
        current_zoom_value = self.camera.zoom.check_value()
        time.sleep(5)

        self._report_result(
            current_zoom_value < start_zoom_value,
            f'Zoom decreased from {start_zoom_value} to {current_zoom_value}',
            f"Zoom hasn't decreased. {start_zoom_value} < {current_zoom_value}"
        )
        second_zoomed_frame = self._get_current_camera_video_frame()
        try:
            second_zoom_factor, second_corners = (
                self._check_zoom_between_two_frames(not_zoomed_frame, second_zoomed_frame))
        except cv2.error:
            Report.logInfo("Was not able to find Zoom match -> retrying")
            return self.tc_zoom_in_out(retry - 1)
        Report.logInfo(f"Zoom factor is: {second_zoom_factor}")

        cv2.polylines(img_original_color, [np.int32(second_corners)],
                      True, (0, 0, 255), 3, cv2.LINE_AA)

        Report.logInfoWithCustomSS(f'Zoomed image center', screenshot=img_original_color)

        low_expected_zoom = current_zoom_value - 40
        high_expected_zoom = current_zoom_value + 40

        self._report_result(
            condition=low_expected_zoom < second_zoom_factor * 100 < high_expected_zoom,
            pass_msg="Noticed zoom matches expected zoom with error margin",
            fail_msg="Noticed zoom does not match expected zoom with error margin"
        )

        self._report_result(
            condition=second_zoom_factor < zoom_factor,
            pass_msg="Visible zoom is lower after decrease which is OK",
            fail_msg="Visible zoom is not lower after zoom decrease which is NOK"
        )

    @exception_handler
    def tc_field_of_view(self):
        self._open_camera_settings()
        for _ in range(3):
            current_value = self.camera.fov.check_value()
            new_value = self.camera.fov.set_random_fov()
            time.sleep(2)
            new_value_check = self.camera.fov.check_value()
            self._report_result(current_value != new_value,
                                f'Changing FOV from {current_value}° to {new_value}°',
                                f"FOV hasn't been changed. "
                                f"Expected: {new_value}°, Observed: {current_value}°")
            self._report_result(new_value_check == new_value,
                                f'Field of View {new_value_check}° selected',
                                f'Field of View {new_value}° not selected, '
                                f'observed: {new_value_check}°')

    @exception_handler
    def tc_auto_focus(self):
        self._open_camera_settings(image_adjustments_tab=True)
        time.sleep(2)
        self.camera.auto_focus.switch_off()
        self._report_result(not self.camera.auto_focus.check_value(),
                            'Auto Focus is disabled', 'Auto Focus is enabled')
        self._report_result(self.camera.manual_focus.is_visible(),
                            'Manual focus displayed', 'Manual focus not displayed')
        self.camera.manual_focus.change_value(int(self.camera.manual_focus.max_border / 2))
        time.sleep(1)
        manual_focus_img = self._capture_frame_to_directory()
        manual_sharpness = calculate_image_properties(manual_focus_img).sharpness
        self.camera.auto_focus.switch_on()
        time.sleep(2)
        auto_focus_img = self._capture_frame_to_directory()
        auto_sharpness = calculate_image_properties(auto_focus_img).sharpness
        self._report_result(auto_sharpness > manual_sharpness,
                            'Sharpness reduced after manual focus adjustment',
                            'Sharpness not reduced after manual focus adjustment')
        time.sleep(1)
        self._report_result(self.camera.auto_focus.check_value(),
                            'Auto Focus is enabled', 'Auto Focus is disabled')
        self._report_result(
            not self.camera.manual_focus.is_slider_visible(do_not_switch_to_dependent=True),
            'Manual focus not displayed', 'Manual focus displayed'
        )

    @exception_handler
    def tc_color_filter(self):
        # color_filters = ['Bright', 'Blossom', 'Forest', 'Film', 'Glaze', 'Mono B']
        color_filters = [camera_filter.name for camera_filter in camera_filters]
        self._open_camera_settings(image_adjustments_tab=True)
        self.tune_app.click_color_filters_tab()
        time.sleep(2)
        self.tune_app.click_color_filter('Original')
        time.sleep(2)
        self._capture_frame_to_directory(name='Original')
        for color_filter in color_filters:
            self._report_result(self.tune_app.verify_color_filter_displayed(color_filter),
                                f'{color_filter} color filter present',
                                f'{color_filter} color filter not present')
            self.tune_app.click_color_filter(color_filter)
            time.sleep(2)
            self._capture_frame_to_directory(name=color_filter)
            filter_applied = self._verify_filter_applied()
            self._report_result(color_filter == filter_applied,
                                f'Video stream changed as per correct filter - {color_filter}',
                                f'Video stream changed as per incorrect filter - '
                                f'{filter_applied} instead of {color_filter}')
            time.sleep(2)
        self.tune_app.click_color_filter('Original')

    @exception_handler
    def tc_image_settings(self):
        self._open_camera_settings(image_adjustments_tab=True)
        time.sleep(2)
        image_settings = ['brightness', 'contrast', 'saturation', 'vibrance', 'sharpness']
        original_img = self._capture_frame_to_directory()
        original_settings = calculate_image_properties(original_img)
        Report.logInfo(f'Original image settings before changing:\n'
                       f'- Brightness: {original_settings.brightness},\n'
                       f'- Contrast: {original_settings.contrast},\n'
                       f'- Saturation: {original_settings.saturation},\n'
                       f'- Vibrance: {original_settings.vibrance},\n'
                       f'- Sharpness: {original_settings.sharpness}')

        for setting in image_settings:
            current_setting = self.camera.__getattribute__(setting)
            if current_setting is None:
                Report.logInfo(f'"{setting.capitalize()}" is not available for this camera')
                continue
            self._report_result(current_setting.is_visible(),
                                f'{current_setting.name} is visible',
                                f'{current_setting.name} is not visible')
            previous_value = current_setting.check_value()
            current_value = current_setting.change_value_randomly(minimal_change=50)
            current_value_visible = current_setting.check_value()
            self._report_result(abs(current_value_visible - previous_value) >= 50,
                                f"{setting} slider value changed to: {current_value_visible} correctly",
                                f"{setting} slider value: {current_value_visible} - NOK")

            time.sleep(3)
            updated_img = self._capture_frame_to_directory()
            updated_settings = calculate_image_properties(updated_img)
            Report.logInfo(f'Image {current_setting.name} setting updated:\n'
                           f'- Brightness: {updated_settings.brightness},\n'
                           f'- Contrast: {updated_settings.contrast},\n'
                           f'- Saturation: {updated_settings.saturation},\n'
                           f'- Vibrance: {updated_settings.vibrance},\n'
                           f'- Sharpness: {updated_settings.sharpness}')
            original_setting = original_settings.__getattribute__(setting)
            updated_setting = updated_settings.__getattribute__(setting)
            Report.logInfo(f'{setting.capitalize()} change:\n'
                           f'- Slider: {abs(previous_value - current_value)}\n'
                           f'- Image: {abs(original_setting - updated_setting)}')
            condition = original_setting > updated_setting if \
                previous_value > current_value else original_setting < updated_setting
            self._report_result(condition,
                                f'Image setting: {current_setting.name} changed correctly',
                                f'Image setting: {current_setting.name} has not changed properly - '
                                f'Original: {original_setting}, '
                                f'Updated: {updated_setting}')
            original_settings = updated_settings

    @exception_handler
    def tc_hdr(self):
        self._open_camera_settings(image_adjustments_tab=True)
        for _ in range(2):
            start_hdr_value = self.camera.hdr.check_value()
            self.camera.hdr.toggle()
            time.sleep(2)
            current_hdr_value = self.camera.hdr.check_value()
            self._report_result(
                start_hdr_value != current_hdr_value,
                f'HDR state changed and is {"ON" if current_hdr_value else "OFF"}',
                f'HDR has not changed and is {"ON" if current_hdr_value else "OFF"}'
            )
            self.tune_app.click_back_from_image_adjustments()
            time.sleep(3)
            self.tune_app.click_image_adjustment()
            time.sleep(2)
            previous_hdr_value = current_hdr_value
            current_hdr_value = self.camera.hdr.check_value()
            self._report_result(
                previous_hdr_value == current_hdr_value,
                f'HDR state persisted and is {"ON" if current_hdr_value else "OFF"}',
                f'HDR has not persisted and is {"ON" if current_hdr_value else "OFF"}'
            )

    @exception_handler
    def tc_anti_flicker(self):
        self._open_camera_settings(image_adjustments_tab=True)
        anti_flicker_values = ['NTSC 60Hz', 'PAL 50Hz']
        for anti_flicker_value in anti_flicker_values:
            self.camera.anti_flicker.select_and_save(anti_flicker_value)
            time.sleep(3)
            self._report_result(anti_flicker_value in self.camera.anti_flicker.check_value(),
                                f'Anti-flicker setting saved successfully to {anti_flicker_value}',
                                f'Anti-flicker setting not saved to {anti_flicker_value}')
            self.tune_app.click_back_from_image_adjustments()
            time.sleep(3)
            self.tune_app.click_image_adjustment()
            time.sleep(3)
            self._report_result(anti_flicker_value in self.camera.anti_flicker.check_value(),
                                f'Anti-flicker setting persisted as {anti_flicker_value}',
                                f'Anti-flicker setting not persisted as {anti_flicker_value}')

    @exception_handler
    def tc_restart_to_default(self):
        self._open_camera_settings(image_adjustments_tab=True)
        previous_value = dict()
        valid_parameters = list(self._get_valid_parameters().keys())

        self._get_previous_image_adjustments(valid_parameters, previous_value)
        time.sleep(3)
        self._click_restart_to_default()
        time.sleep(2)
        self._verify_default_image_adjustments(valid_parameters, previous_value)

    @exception_handler
    def tc_about_camera(self):
        self._open_camera_settings()
        self.tune_app.click_info_button()
        time.sleep(1)
        self._report_result(
            self.tune_app.verify_device_name_displayed(device_name=self.camera.name),
            f"{self.camera.name} - displayed in About",
            f"{self.camera.name} - not displayed in About"
        )
        self._report_result(
            self.tune_app.verify_more_details_displayed(),
            "More details link displayed in About",
            "More details link not displayed in About"
        )
        self._report_result(
            self.tune_app.verify_factory_reset_displayed(),
            "Factory reset button displayed in About",
            "Factory reset button not displayed in About"
        )

    @exception_handler
    def tc_factory_reset(self):
        invalid_values = dict()
        self._open_camera_settings()

        default_values_camera_settings, default_values_image_adjustments = self._divide_parameters()
        self._change_parameters_to_different_than_default(default_values_camera_settings)
        self.tune_app.click_image_adjustment()
        self._change_parameters_to_different_than_default(default_values_image_adjustments)

        time.sleep(5)
        self._factory_reset_camera()
        self._open_camera_settings(restart_tune=False)

        self._verify_default_parameters_values(default_values_camera_settings, invalid_values)
        self.tune_app.click_image_adjustment()
        self._verify_default_parameters_values(default_values_image_adjustments, invalid_values)

        self._report_result(
            not invalid_values,
            f'All parameters have expected value after Factory Reset',
            f'Invalid values after Factory Reset:\n'
            f'{json.dumps(invalid_values, indent=2)}'
        )


class TuneCameraPersistency(TuneDevicePersistency):
    def __init__(self, camera_name: str, tune_app: Optional[TuneElectron] = None):
        super().__init__(camera_name, CamerasParametersWrapper, tune_app)
        self.camera: CameraProperties = self.device

    def _get_expected_values_from_camera_settings(self) -> None:
        time.sleep(10)
        self.device_parameters.append(self._get_expected_value(self.camera.fov))
        self.device_parameters.append(self._get_expected_value(self.camera.zoom))
        # self.device_parameters.append(self._get_expected_value(self.camera.pan_tilt))
        self.device_parameters.append(self._set_and_get_switch_value(self.camera.show_mode))

    def _get_expected_values_from_image_adjustments(self) -> None:
        time.sleep(0.5)
        self.device_parameters.append(self._set_and_get_switch_value(self.camera.hdr))
        self.device_parameters.append(self._set_and_get_switch_value(self.camera.auto_focus))
        self.device_parameters.append(self._get_expected_value(self.camera.manual_focus))
        self._set_switch(self.camera.auto_exposure, True)
        self.device_parameters.append(self._get_expected_value(self.camera.exposure_compensation))
        self.device_parameters.append(self._set_and_get_switch_value(
            self.camera.low_light_compensation))
        self.device_parameters.append(self._set_and_get_switch_value(self.camera.auto_exposure))
        self.device_parameters.append(self._get_expected_value(self.camera.manual_exposure))
        self.device_parameters.append(self._get_expected_value(self.camera.gain))
        self.device_parameters.append(self._get_expected_value(self.camera.shutter_speed))
        self.device_parameters.append(self._get_expected_value(self.camera.iso))
        self.device_parameters.append(self._get_expected_value(
            self.camera.temperature_compensation))
        self.device_parameters.append(self._set_and_get_switch_value(
            self.camera.auto_white_balance))
        self.device_parameters.append(self._get_expected_value(self.camera.temperature))
        self.device_parameters.append(self._get_expected_value(self.camera.tint))
        self.device_parameters.append(self._get_expected_value(self.camera.anti_flicker))
        self.device_parameters.append(self._get_expected_value(self.camera.brightness))
        self.device_parameters.append(self._get_expected_value(self.camera.contrast))
        self.device_parameters.append(self._get_expected_value(self.camera.saturation))
        self.device_parameters.append(self._get_expected_value(self.camera.vibrance))
        self.device_parameters.append(self._get_expected_value(self.camera.sharpness))

    def _check_if_values_from_camera_settings_persisted(self) -> None:
        time.sleep(3)
        self._compare_current_value_with_expected(self.camera.fov, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.zoom, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.pan_tilt, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.show_mode, self.device_parameters)

    def _check_if_values_from_image_adjustments_persisted(self) -> None:
        time.sleep(0.5)
        self._compare_current_value_with_expected(self.camera.hdr, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.auto_focus, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.manual_focus,
                                                  self.device_parameters)
        self._compare_current_value_with_expected(self.camera.auto_exposure, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.manual_exposure, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.gain, self.device_parameters,
                                                  margin_of_error=1)
        self._compare_current_value_with_expected(self.camera.shutter_speed, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.iso, self.device_parameters)
        self._set_switch(self.camera.auto_exposure, True)
        self._compare_current_value_with_expected(self.camera.exposure_compensation,
                                                  self.device_parameters)
        self._compare_current_value_with_expected(self.camera.low_light_compensation,
                                                  self.device_parameters)
        self._compare_current_value_with_expected(self.camera.auto_white_balance,
                                                  self.device_parameters)
        self._compare_current_value_with_expected(self.camera.temperature, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.tint, self.device_parameters)
        self._set_switch(self.camera.auto_white_balance, True)
        self._compare_current_value_with_expected(self.camera.temperature_compensation,
                                                  self.device_parameters)
        self._compare_current_value_with_expected(self.camera.anti_flicker, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.brightness, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.contrast, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.saturation, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.vibrance, self.device_parameters)
        self._compare_current_value_with_expected(self.camera.sharpness, self.device_parameters)

    def check_persistency(self, acroname_automatic: bool = True) -> None:
        self._set_random_camera_adjustments()
        self._reconnect_device(acroname_automatic)
        self._get_camera_adjustments()

    def _set_random_camera_adjustments(self) -> None:
        self.tune_app.click_device(self.camera.name)
        self._get_expected_values_from_camera_settings()
        self.tune_app.click_image_adjustment()
        self._get_expected_values_from_image_adjustments()

    def _get_camera_adjustments(self):
        self.tune_app.click_device(self.camera.name)
        self._check_if_values_from_camera_settings_persisted()
        self.tune_app.click_image_adjustment()
        self._check_if_values_from_image_adjustments_persisted()
        self._persistency_results()


class RendererParser:
    queue = queue.Queue()

    def __init__(self):
        self._run_reader()

    def get_from_queue(self):
        return self.queue.get()

    def temp_get_message(self):
        message = self.get_from_queue()
        print(json.dumps(message, indent=2))
        # if 'responseHandler' in message.get('header'):
        #     if 'uvc_camera_settings' in message.get('path') and message.get('verb') == 'GET':
        #         print('UVC CAMERA SETTINGS:\n', json.dumps(message.get('payload'), indent=2))
        #     elif 'uvc_video_settings' in message.get('path') and message.get('verb') == 'GET':
        #         print('UVC VIDEO SETTINGS:\n', json.dumps(message.get('payload'), indent=2))

    def _run_reader(self):
        thread = Thread(target=RendererReader, args=(self.queue, ))
        thread.daemon = True
        thread.start()


class RendererReader:
    _win_path = r'C:\ProgramData\Logitech\Tune\UI\renderer.log'
    _mac_path = r'/Users/Shared/logitune/UI/renderer.log'
    renderer_path = _win_path if sys.platform.startswith('win') else _mac_path

    def __init__(self, message_queue: queue.Queue):
        self.message_queue = message_queue
        self.curly_count = 0
        self._run()

    def _run(self):
        buffer = list()
        with open(self.renderer_path, 'r') as file:
            for current_line in self._read_new_line(file):
                buffer = self._put_message_to_queue(current_line, buffer)

    def _count_curly_brackets(self, log_line: str):
        self.curly_count += log_line.count('{')
        self.curly_count -= log_line.count('}')

    def _parse_message_and_put_in_queue(self, buffer: list):
        try:
            json_data = self._transform_message(buffer)
            if json_data:
                if isinstance(list(json_data.keys())[0], int):
                    messages = self._unpack_jsons(json_data)
                    for message in messages:
                        if message not in self.message_queue.queue:
                            self.message_queue.put(message)
                else:
                    if json_data not in self.message_queue.queue:
                        self.message_queue.put(json_data)
        except Exception as e:
            print(repr(e), e)

    def _put_message_to_queue(self, log_line: str, buffer: list):
        pattern = r'^\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{1,2}:\d{1,2} [A-Z]{2} \| \d{1,3} \|'
        is_new_message = re.search(pattern, log_line)
        self._count_curly_brackets(log_line)
        if is_new_message is None:
            buffer.append(log_line)
            if self.curly_count == 0:
                self._parse_message_and_put_in_queue(buffer)
            return buffer
        else:
            return [log_line]

    def _transform_message(self, buffer: List[str]) -> dict:
        pattern = r'(\{(.*)\})'
        message = ''.join([line.replace('\n', '') for line in buffer]).strip()
        if message:
            json_ready_data = re.search(pattern, message)
            if json_ready_data:
                json_ready_data = json_ready_data.group(0)
                json_data = self._parse_multiple_jsons(json_ready_data)
                header = message.replace(json_ready_data, '')
                json_data['header'] = header
                return json_data
            else:
                return {"header": message}

    def _parse_multiple_jsons(self, json_string: str, valid_jsons: Optional[List[dict]] = None
                              ) -> dict:
        try:
            if valid_jsons is None:
                return json.loads(json_string)
            else:
                if json.loads(json_string):
                    valid_jsons.append(json.loads(json_string))
                if len(valid_jsons) == 1:
                    return valid_jsons[0]
                else:
                    return {idx: item for idx, item in enumerate(valid_jsons)}
        except json.decoder.JSONDecodeError as e:
            index = int(re.search(r'\(char (\d{1,20})\)', str(e)).group(1))
            if valid_jsons is None:
                valid_jsons = [json.loads(json_string[:index])]
            else:
                valid_jsons.append(json.loads(json_string[:index]))
            if json_string[index:][0] == ',':
                index += 1
            return self._parse_multiple_jsons(json_string[index:], valid_jsons)

    @staticmethod
    def _unpack_jsons(packed_jsons: dict) -> List[dict]:
        output = list()
        for key, message in packed_jsons.items():
            if key != 'header':
                message['header'] = packed_jsons.get('header')
                output.append(message)
        return output

    @staticmethod
    def _read_new_line(renderer_file: TextIO):
        renderer_file.seek(0, 2)
        while True:
            line = renderer_file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line


if __name__ == '__main__':
    parser = RendererParser()
    for i in range(1000000):
        parser.temp_get_message()
        # print(parser.get_from_queue())
    # from testsuite_tune_app.update_easteregg.device_parameters import gauguin
    #
    # for i in range(10):
    #     tune = TuneCameraPersistency(gauguin.device_name)
    #     tune.check_persistency()
    #     tune.tune_app.close_tune_app()
