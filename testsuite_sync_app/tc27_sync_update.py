import os
import time
import unittest

import psutil

from apps.meeting.google_meet import GoogleMeet
from apps.sync.AppInstall import AppInstall
from apps.sync.sync_app import SyncApp
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from base.base_ui import UIBase
from common.framework_params import INSTALLER, SYNC_PROD_VERSION1, SYNC_PROD_VERSION2
from common.json_helper import JsonHelper
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_all
from extentreport.report import Report
from testsuite_sync_app.tc_methods import SyncTCMethods
from common.image_settings import compare_images


class SyncUpdate(UIBase):
    sync_app = SyncAppMethods()
    sync_methods = SyncTCMethods()
    sync_version1 = SYNC_PROD_VERSION1
    sync_version2 = SYNC_PROD_VERSION2
    sync_current = INSTALLER
    app = AppInstall()

    def setUp(self) -> None:
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if 'WinAppDriver.exe' in proc.name():
                    print(f'Killing {proc.name()}')
                    proc.kill()
            os.system(str(UIBase.rootPath) + "\\WinApp\\winapp.bat")
            time.sleep(5)
        super(SyncUpdate, self).setUp()

    def test_2701_VC_130992_sync_update_with_rallybar(self):
        self._sync_update_flow(device_name="Rally Bar")

    def test_2702_VC_130994_sync_update_with_rallybar_mini(self):
        self._sync_update_flow(device_name="Rally Bar Mini")

    def test_2703_VC_130995_sync_update_with_meetup(self):
        self._sync_update_flow(device_name="MeetUp")

    def test_2704_VC_130996_sync_update_with_rallycamera(self):
        self._sync_update_flow(device_name="Rally Camera")

    def test_2705_VC_130997_sync_update_with_rally(self):
        self._sync_update_flow(device_name="Rally")

    def _sync_update_flow(self, device_name):
        global_variables.SYNC_FUTEN = 'futen-staging'
        testName = self.__getattribute__("_testMethodName")
        self._sync_prod_install()
        self._device_settings(device_name=device_name)
        prod1 = self._stream_in_google_meet(f'{device_name}_prod1')
        global_variables.extent.flush()
        global_variables.reportInstance = global_variables.extent.createTest(f'{testName}_update_from_menu',
                                                                             "Test Case Details")
        global_variables.SYNC_FUTEN = 'futen-staging-qa'
        self._sync_upate_from_menu()
        self._device_settings_verification(device_name=device_name)
        prod2 = self._stream_in_google_meet(f'{device_name}_prod2')
        if compare_images(prod1, prod2):
            Report.logPass("Images from the Google Meet Video stream before and after the update are identical")
        else:
            Report.logFail("Images from the Google Meet Video stream before and after the update are not identical",
                           False)
        global_variables.extent.flush()
        global_variables.reportInstance = global_variables.extent.createTest(f'{testName}_update_from_room',
                                                                             "Test Case Details")
        # global_variables.SYNC_FUTEN = 'futen-staging-qa'
        # self._sync_upate_from_room()
        # self._device_settings_verification(device_name=device_name)
        # current = self._stream_in_google_meet(f'{device_name}_current')
        # if compare_images(prod2, current):
        #     Report.logPass("Images from the Google Meet Video stream before and after the update are identical")
        # else:
        #     Report.logFail("Images from the Google Meet Video stream before and after the update are not identical",
        #                    False)
        # Reset Device settings
        global_variables.extent.flush()
        global_variables.reportInstance = global_variables.extent.createTest(f'{testName}_reset',
                                                                             "Test Case Details")
        self._reset_device_settings_and_remove(device_name=device_name)

    def _sync_prod_install(self):
        self.sync_methods.tc_install_sync_app(version=self.sync_version1)
        self.sync_methods.tc_connect_to_sync_portal()

    def _sync_upate_from_menu(self):
        if get_custom_platform() == "windows":
            sync_config = 'C:/ProgramData/Logitech/LogiSync/sync-config.json'
            JsonHelper.update_json(sync_config, 'futen,current', global_variables.SYNC_FUTEN)
            SyncApp.restart_sync_services()
            self.app.update_sync_from_menu()
        else:
            self.app.install_sync_mac(version=self.sync_version2)

    def _sync_upate_from_room(self):
        if get_custom_platform() == "windows":
            sync_config = 'C:/ProgramData/Logitech/LogiSync/sync-config.json'
            JsonHelper.update_json(sync_config, 'futen,current', global_variables.SYNC_FUTEN)
            SyncApp.restart_sync_services()
            self.app.update_sync_from_room()
        else:
            self.app.install_sync_mac(version=self.sync_version2)

    def _device_settings(self, device_name):
        self.sync_app.open()
        self.sync_app.add_device(device_name=device_name)
        self.sync_app.home.click_device_camera(device_name=device_name).expand_manual_color_settings()
        global_variables.BRIGHTNESS = self.sync_app.camera.set_color_value("brightness", 70)
        global_variables.CONTRAST = self.sync_app.camera.set_color_value("contrast", 20)
        global_variables.SATURATION = self.sync_app.camera.set_color_value("saturation", 20)
        global_variables.SHARPNESS = self.sync_app.camera.set_color_value("sharpness", 10)

        # RightSight 2
        self.sync_app.home.click_device_camera(device_name=device_name)
        if device_name in ["Rally Bar", "Rally Bar Mini"]:
            self.sync_app.camera.click_speaker_view().disable_picture_in_picture()
        else:
            self.sync_app.camera.enable_right_sight().click_on_call_start()

        # Audio Controls
        if device_name in ["Rally Bar", "Rally Bar Mini"]:
            self.sync_app.home.click_device_audio(device_name=device_name) \
                .enable_speaker_boost() \
                .disable_ai_noise_suppression(). \
                click_reverb_control_disabled(). \
                click_microphone_eq_bass_boost(). \
                click_speaker_eq_voice_boost()
            self.sync_app.verify_speaker_boost(enabled=True) \
                .verify_ai_noise_suppression(enabled=False) \
                .verify_reverb_control_disabled(selected=True) \
                .verify_microphone_eq_bass_boost(selected=True) \
                .verify_speaker_eq_voice_boost(selected=True)

        self.sync_app.close()

    def _device_settings_verification(self, device_name):
        self.sync_app.open().click_device_camera(device_name=device_name) \
            .expand_manual_color_settings()
        self.sync_app.verify_manual_color_setting("brightness", global_variables.BRIGHTNESS)
        self.sync_app.verify_manual_color_setting("contrast", global_variables.CONTRAST)
        self.sync_app.verify_manual_color_setting("saturation", global_variables.SATURATION)
        self.sync_app.verify_manual_color_setting("sharpness", global_variables.SHARPNESS)

        # RightSight 2
        self.sync_app.home.click_device_camera(device_name=device_name)
        if device_name in ["Rally Bar", "Rally Bar Mini"]:
            self.sync_app.verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=False)
        else:
            self.sync_app.verify_on_call_start(selected=True)

        # Audio Controls
        if device_name in ["Rally Bar", "Rally Bar Mini"]:
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_boost(enabled=True) \
                .verify_ai_noise_suppression(enabled=False) \
                .verify_reverb_control_disabled(selected=True) \
                .verify_microphone_eq_bass_boost(selected=True) \
                .verify_speaker_eq_voice_boost(selected=True)

        self.sync_app.close()

    def _stream_in_google_meet(self, image_name):
        try:
            meet = GoogleMeet()
            sync_driver = global_variables.driver
            meet.create_new_meeting()
            screenshot = meet.capture_video_stream(image_name)
            meet.leave_meeting()
            global_variables.driver = sync_driver
            return screenshot
        except Exception as e:
            Report.logException(str(e))

    def _reset_device_settings_and_remove(self, device_name):
        self.sync_app.open().click_device_camera(device_name=device_name) \
            .expand_manual_color_settings() \
            .click_reset_manual_color_settings()
        if device_name in ["Rally Bar", "Rally Bar Mini"]:
            self.sync_app.camera.click_speaker_view().enable_picture_in_picture().click_group_view()
            self.sync_app.home.click_device_audio(device_name=device_name) \
                .disable_speaker_boost() \
                .enable_ai_noise_suppression() \
                .click_reverb_control_normal() \
                .click_microphone_eq_normal() \
                .click_speaker_eq_normal()
        else:
            self.sync_app.camera.enable_right_sight().click_dynamic()
        self.sync_app.forget_problem_device(device_name=device_name)
        self.sync_app.close()


if __name__ == "__main__":
    unittest.main()
