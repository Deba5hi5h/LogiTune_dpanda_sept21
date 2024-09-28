import time
import random
from datetime import datetime

import deepdiff
from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from base import global_variables
from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile_methods import TuneMobileMethods
from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_tune_mobile import test_data


class TuneMobileTests(TuneMobileMethods):

    def tc_equalizer_presets(self, headset: str):
        """
        Method to verify default Preset controls

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            eq = home.click_equalizer()
            self.verify_equalizer_options()
            eq.click_bass_boost()
            time.sleep(2)
            self.verify_equalizer_preset("Bass Boost")
            eq_value = eq.click_back().get_equalizer_value()
            verification = (eq_value.lower() == "bass boost")
            self.report_displayed_or_not(f"Correct EQ value Bass Boost", verification)
            eq = home.click_equalizer().click_volume_boost()
            time.sleep(2)
            self.verify_equalizer_preset("Volume Boost")
            eq_value = eq.click_back().get_equalizer_value()
            verification = (eq_value.lower() == "volume boost")
            self.report_displayed_or_not(f"Correct EQ value Volume Boost", verification)
            eq = home.click_equalizer().click_podcast()
            time.sleep(2)
            self.verify_equalizer_preset("Podcast")
            eq_value = eq.click_back().get_equalizer_value()
            verification = (eq_value.lower() == "podcast")
            self.report_displayed_or_not(f"Correct EQ value Podcast", verification)
            eq = home.click_equalizer().click_default()
            time.sleep(2)
            self.verify_equalizer_preset("Default")
            eq_value = eq.click_back().get_equalizer_value()
            verification = (eq_value.lower() == "default")
            self.report_displayed_or_not(f"Correct EQ value Default", verification)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_customize_equalizer_presets(self, headset: str):
        """
        Method to verify Customizing Equalizer Presets

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            eq = home.click_equalizer()
            if eq.verify_edit_presets_displayed():
                self.delete_all_custom_equalizers()
            eq.adjust_eq_slider1(value=20).adjust_eq_slider2(value=-20)
            self.report_displayed_or_not("Save Custom EQ Preset", eq.verify_save_custom_preset_displayed())
            eq.click_save_custom_preset()
            self.report_displayed_or_not("Custom EQ Preset - Close button", eq.verify_close_preset_displayed())
            self.report_displayed_or_not("Custom EQ Preset - Surprise Me", eq.verify_surprise_me_displayed(),
                                         screenshot=False)
            self.report_displayed_or_not("Custom EQ Preset - Text field", eq.verify_preset_name_textfield_displayed(),
                                         screenshot=False)
            eq.click_surprise_me()
            name = eq.get_preset_name()
            self.report_displayed_or_not(f"Custom EQ Preset - Surprise Me name '{name}'", name != "")
            eq.click_close_preset()
            time.sleep(2)
            eq.click_save_custom_preset().type_preset_name("Test1").click_save_button()
            self.report_displayed_or_not("Custom EQ Preset - Test1", eq.verify_custom_preset("Test1"))
            value = eq.click_back().get_equalizer_value()
            self.report_displayed_or_not("Home Screen EQ - Test1", value == "Test1")
            home.click_equalizer()
            self.delete_custom_equalizer("Test1")
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_customize_equalizer_presets_without_save(self, headset: str):
        """
        Method to verify Customizing Equalizer Presets

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            eq = home.click_equalizer()
            if eq.verify_edit_presets_displayed():
                self.delete_all_custom_equalizers()
            eq.adjust_eq_slider1(value=20).adjust_eq_slider2(value=-20).adjust_eq_slider3(-10) \
                .adjust_eq_slider4(10).adjust_eq_slider5(20)
            value = eq.click_back().get_equalizer_value()
            self.report_displayed_or_not("Home Screen EQ - Custom", value == "Custom")
            home.click_equalizer().click_default().click_back()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_equalizer_preset_limit(self, headset):
        """
        Method to verify Max 3 Custom Equalizer Presets can be added

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            eq = home.click_equalizer()
            if eq.verify_edit_presets_displayed():
                self.delete_all_custom_equalizers()
            self.create_custom_equalizer("Test1", 50, -50)
            self.create_custom_equalizer("Test2", 0, 0, -50)
            self.create_custom_equalizer("Test3", 0, 0, 0, 50)
            self.create_custom_equalizer("Test4", 0, 0, 0, 0, -50, preset_limit=True)
            self.delete_all_custom_equalizers()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_edit_custom_equalizer(self, headset: str):
        """
        Method to Edit and delete custom equalizer

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            preset_name = "Test1"
            eq = home.click_equalizer()
            if eq.verify_edit_presets_displayed():
                self.delete_all_custom_equalizers()
            self.create_custom_equalizer(preset_name, 50, -50)
            self.report_displayed_or_not("Edit Presets button", eq.verify_edit_presets_displayed())
            self.delete_custom_equalizer(preset_name)
            verification = not eq.verify_custom_preset(preset_name=preset_name)
            self.report_displayed_or_not(f"Deleted custom preset {preset_name}", verification, displayed=False)
            self.report_displayed_or_not("Edit Presets button", not eq.verify_edit_presets_displayed(), displayed=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_device_name(self, headset: str):
        """
        Method to update and verify device name

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            displayed = home.click_device_name().get_device_name_value()
            self.report_displayed_or_not(f"Same Device Name {headset}", headset == displayed)
            self.report_displayed_or_not(f"Surprise Me", self.device_name.verify_surprise_me_displayed())
            self.report_displayed_or_not(f"Text Field", self.device_name.verify_device_name_textfield_displayed())
            self.report_displayed_or_not(f"Update button", self.device_name.verify_update_button_displayed())
            new_device_name = self.device_name.click_surprise_me().click_close().get_device_name_value()
            if headset.lower() == new_device_name.lower():
                Report.logPass("Device Name not changed on clicking on close without Update")
            else:
                Report.logFail("Device Name updated on clicking close without Update")
            self.home.click_device_name().type_device_name("Zone 1").click_update()
            time.sleep(1)
            new_device_name = self.home.get_device_name_value()
            self.report_displayed_or_not(f"Updated Device Name Zone 1", new_device_name == "Zone 1")
            self.close()
            self.open_app()
            for _ in range(3):
                self.home.click_device_name().type_device_name(headset).click_update()
                device_name = self.home.get_device_name_value()
                if headset == device_name:
                    break
            self.close()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_sidetone(self, headset: str):
        """
        Method to update and verify device name

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            home.click_sidetone()
            if self.sidetone.verify_ok_button():
                self.sidetone.click_ok()
            if self.sidetone.verify_allow_button():
                self.sidetone.click_allow()
            self.report_displayed_or_not(f"Sidetone Done button", self.sidetone.verify_done_button())
            self.report_displayed_or_not(f"Sidetone Information", self.sidetone.verify_sidetone_info())
            self.report_displayed_or_not(f"Sidetone Slider", self.sidetone.verify_sidetone_slider())
            self.report_displayed_or_not(f"Sidetone 50%", self.sidetone.verify_sidetone_percentage(value=50))
            for sidetone_value in [0, 20, 80, 100, 50]:
                self.sidetone.adjust_sidetone_slider(value=sidetone_value)
                if self.is_ios_device():
                    self.report_displayed_or_not(f"Sidetone adjustment to {sidetone_value}%",
                                                 self.sidetone.verify_sidetone_percentage(value=sidetone_value))
                self.sidetone.click_done()
                time.sleep(1)
                sidetone_home = self.home.get_sidetone_value()
                self.report_displayed_or_not(f"Adjusted Sidetone value {sidetone_value}% in Home screen",
                                             f"{sidetone_home}" == f"{sidetone_value}%")
                self.home.click_sidetone()
            self.sidetone.click_done()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_sleep_settings(self, headset: str):
        """
        Method to update and verify device name

        :param headset:
        :return :
        """
        try:
            home = self.open_app()
            if not self.is_correct_headset_connected(headset):
                raise Exception("Incorrect headset connected")
            home.click_sleep_settings()
            time.sleep(1)
            self.report_displayed_or_not(f"Sleep Settings Save button", self.sleep_settings.verify_save_button())
            self.report_displayed_or_not(f"Sleep Settings Close button", self.sleep_settings.verify_close_button())
            self.report_displayed_or_not(f"Sleep Settings Never", self.sleep_settings.verify_never_radio())
            for minutes in [5, 10, 15, 30]:
                self.report_displayed_or_not(f"Sleep Settings {minutes} minutes",
                                             self.sleep_settings.verify_minutes_radio(minutes), screenshot=False)
                self.sleep_settings.click_minutes_radio(minutes).click_save()
                time.sleep(1)
                sleep_value = self.home.get_sleep_settings_value()
                self.report_displayed_or_not(f"Saved Sleep Settings {minutes} minutes in Home screen",
                                             sleep_value == f"{minutes} minutes")
                self.home.click_sleep_settings()
                time.sleep(1)
            for hours in [1, 2, 4]:
                self.report_displayed_or_not(f"Sleep Settings {hours} hours",
                                             self.sleep_settings.verify_hours_radio(hours), screenshot=False)
                self.sleep_settings.click_hours_radio(hours).click_save()
                time.sleep(1)
                sleep_value = self.home.get_sleep_settings_value()
                self.report_displayed_or_not(f"Saved Sleep Settings {hours} hours in Home screen",
                                             sleep_value in f"{hours} hours")
                self.home.click_sleep_settings()
                time.sleep(1)
            self.sleep_settings.click_close()
            time.sleep(1)
            sleep_value = self.home.get_sleep_settings_value()
            self.home.click_sleep_settings()
            time.sleep(1)
            updated_sleep_value = self.sleep_settings.click_minutes_radio(5).click_close().get_sleep_settings_value()
            if sleep_value == updated_sleep_value:
                Report.logPass("Sleep settings not changed on clicking close without Save")
            else:
                Report.logFail("Sleep settings updated on clicking close without Save")
            self.home.click_sleep_settings()
            time.sleep(1)
            self.sleep_settings.click_never_radio().click_save()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_localization_navigation(self, headset: str):
        """
        Method to navigate through different screens for a language and take screenshot

        :param headset:
        :return :`
        """
        try:
            # self.phone_settings.open()
            # self.phone_settings.disconnect_all_bluetooth_devices()
            # self.phone_settings.close()
            # self.open_app()
            # time.sleep(3)
            # Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "NoDevicesConnected",
            #                      "No Devices Connected")
            # self.home.click_settings_no_device()
            # time.sleep(1)
            # Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "NoDevicesSettings", "Home->Settings")
            # self.close()
            # self.phone_settings.open()
            # self.phone_settings.connect_bluetooth_device(headset)
            # self.phone_settings.close()
            self.open()
            time.sleep(5)
            self.is_correct_headset_connected(headset)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Home", "Home")
            self.swipe_screen("vertical", 0.8, 0.2)
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Home_scrolldown", "Home_scrolldown")
            self.swipe_screen("vertical", 0.3, 0.8)
            self.home.click_equalizer()
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Equalizer", "Home->Equalizer")
            self.equalizer.click_back().click_device_name()
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "DeviceName", "Home->Device Name")
            self.device_name.click_close()
            time.sleep(1)
            self.home.click_connected_devices()
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "ConnectedDevices",
                                 "Home->Connected Devices")
            self.connected_devices.click_back().click_sleep_settings()
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "SleepSettings", "Home->Sleep Settings")
            self.sleep_settings.click_close()
            if headset.lower() in ["zone wireless 2"]:
                self.home.click_anc_buttion_options()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "ANC_button_options",
                                     "Home->ANC button_options")
                self.anc_button_options.click_short_press()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "ANC_button_options_short_press",
                                     "Home->ANC button_options->Short press")
                self.anc_button_options.click_back()
                self.anc_button_options.click_back()
                self.home.click_on_head_detection()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "On_head_detection",
                                     "Home->On-head detection")
                self.on_head_detection.click_back()
                self.home.click_touch_pad()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Touch_pad",
                                     "Home->Touch Pad")
                self.touch_pad.click_back()
                self.home.click_voice_prompts()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Voice_prompts",
                                     "Home->Voice Prompts")
                self.voice_prompts.click_close()
                self.home.click_health_and_safety()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Health_and_safety",
                                     "Home->Health and Safety")
                self.health_and_safety.click_back()
                self.home.click_personal_eq_toggle()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Personal_EQ",
                                     "Home->Personal EQ")
                self.personal_eq.click_start()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Personal_EQ_Next1",
                                     "Home->Personal EQ Next1")
                for i in range(2, 7):
                    self.personal_eq.click_next_step()
                    time.sleep(1)
                    Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", f"Personal_EQ_Next{i}",
                                         f"Home->Personal EQ Next{i}")
                for _ in range(6):
                    time.sleep(1)
                    self.personal_eq.click_back()
            if headset.lower() in ["zone wireless plus", "zone vibe 130", "zone vibe 100",
                                   "zone vibe wireless", "zone wireless 2"]:
                self.home.click_sidetone()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Sidetone", "Home->Sidetone")
                if self.is_ios_device():
                    self.sidetone.click_done()
                else:
                    time.sleep(2)
                    self.sidetone.click_close()
                if headset.lower() in ["zone wireless 2"]:
                    self.home.click_advanced_call_clarity()
                    time.sleep(1)
                    Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Advanced_call_clarity",
                                         "Home->Advanced call clarity")
                    self.advanced_call_clarity.click_close()
                self.home.click_headset_language()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "HeadsetLanguage",
                                     "Home->Headset Language")
                self.headset_language.click_back()
            if headset.lower() in ["zone true wireless"]:
                self.home.click_button_functions()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "ButtonFunctionsLeftEarBud",
                                     "Home->Button Functions->Left Ear Bud")
                self.button_functions.click_short_press()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "LeftEarBudShortPress",
                                     "Home->Button Functions->Left Ear Bud->Short Press")
                self.button_functions.click_close().click_long_press()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "LeftEarBudLongPress",
                                     "Home->Button Functions->Left Ear Bud->Long Press")
                self.button_functions.click_close().click_double_tap()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "LeftEarBudDoubleTap",
                                     "Home->Button Functions->Left Ear Bud->Double Tap")
                self.button_functions.click_close().click_right_ear_bud()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "ButtonFunctionsRightEarBud",
                                     "Home->Button Functions->Right Ear Bud")
                self.button_functions.click_short_press()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "RightEarBudShortPress",
                                     "Home->Button Functions->Right Ear Bud->Short Press")
                self.button_functions.click_close().click_long_press()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "RightEarBudLongPress",
                                     "Home->Button Functions->Right Ear Bud->Long Press")
                self.button_functions.click_close().click_double_tap()
                time.sleep(1)
                Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "RightEarBudDoubleTap",
                                     "Home->Button Functions->Right Ear Bud->Double Tap")
                self.button_functions.click_close().click_back()
            self.home.click_settings()
            time.sleep(1)
            Report.logScreenshot(f"{headset}{tune_mobile_config.lanngauge}", "Settings", "Home->Settings")
            self.settings.click_back()
            self.close()
        except Exception as e:
            Report.logException(str(e))
            global_variables.driver.quit()
            global_variables.driver = None
        # self.phone_settings.open()
        # self.phone_settings.disconnect_all_bluetooth_devices()
        # self.phone_settings.close()

    def tc_people_teammates(self):
        """
        Method to validate Teammates functionality under People

        :param :
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates()
            self.report_displayed_or_not("No Teammates added message", self.people.verify_no_teammates_message())
            self.people.click_back().click_everyone()
            time.sleep(1)
            for name in test_data.tc_people_teammates:
                self.people.type_in_search(name)
                self.people.click_teammate(name)
                self.people.click_add_to_team().click_add().click_done()
                self.people.click_back()
                # Workaround for Android Bug
                if self.is_ios_device():
                # Workaround for Android Bug
                    self.people.click_clear_search()
            self.people.click_teammates().click_all_teammates()
            for name in test_data.tc_people_teammates:
                self.validate_search(search_text=name)
                self.validate_search(search_text=name[:3])
                # self.validate_search(search_text=name[-3:])
            self.people.remove_all_teammates().click_back()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_remove_teammate(self):
        """
        Method to validate Remove Teammates functionality under People

        :param :
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates()
            self.people.click_back().click_everyone()
            time.sleep(1)
            for name in test_data.tc_people_teammates:
                self.people.type_in_search(name)
                self.people.click_teammate(name)
                self.people.click_add_to_team().click_add().click_done()
                self.people.click_back()
                # Workaround for Android Bug
                if self.is_ios_device():
                # Workaround for Android Bug
                    self.people.click_clear_search()
            self.people.click_teammates().click_all_teammates()
            self.people.type_in_search(test_data.tc_people_teammates[2])
            self.validate_remove_teammate(test_data.tc_people_teammates[2])
            self.people.click_clear_search()
            self.validate_remove_teammate(test_data.tc_people_teammates[1])
            self.people.remove_all_teammates().click_back()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_screen(self):
        """
        Method to validate People screen

        :param :
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_people()
            self.report_displayed_or_not("People navigation button highlighted",
                                         self.dashboard.verify_people_navigation_highlighted())
            self.report_displayed_or_not("Teammates Tab selected", self.people.verify_teammates_tab_selected())
            self.people.click_all_teammates()
            self.report_displayed_or_not("Search control", self.people.verify_search_control_displayed(), warning=True)
            self.people.click_back()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone(self):
        """
        Method to validate Everyone tab functionality under People

        :param :
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_everyone()
            self.people.scroll_to_top()
            self.report_displayed_or_not("Search control", self.people.verify_search_control_displayed())
            for name in test_data.tc_people_everyone:
                self.validate_search(search_text=name, teammates=False)
                self.validate_search(search_text=name[:3], teammates=False)
            self.validate_search(search_text="junk@text", no_results=True)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone_add_teammate(self, remove_teammates: bool = True):
        """
        Method to validate adding teammate functionality from Everyone tab under People

        :param remove_teammates: (False if only to add teammates and don't remove)
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates().click_back()
            self.people.click_everyone()
            time.sleep(1)
            names = random.sample(test_data.tc_people_everyone, 2)
            for name in names:
                self.people.type_in_search(name)
                self.people.click_teammate(name)
                self.people.click_add_to_team().click_add().click_done()
                self.people.click_back()
                # Workaround for Android Bug
                if self.is_ios_device():
                # Workaround for Android Bug
                    self.people.click_clear_search()
            self.people.click_teammates().click_all_teammates()
            teammates = self.people.get_teammates_list()
            result = deepdiff.DeepDiff(names, teammates, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass("All added teammates displayed")
            else:
                Report.logFail("Not all teammates displayed")
            if remove_teammates:
                self.people.remove_all_teammates()
            self.people.click_back()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone_remove_teammate(self):
        """
        Method to validate Remove Teammates functionality from Everyone tab under People

        :param :
        :return :
        """
        try:
            self.tc_people_everyone_add_teammate(remove_teammates=False)
            names = self.people.click_all_teammates().get_teammates_list()
            self.people.click_back()
            for name in names:
                self.people.click_everyone()
                if self.people.verify_clear_search():
                    self.people.click_clear_search()
                self.people.type_in_search(name)
                self.validate_remove_teammate(teammate=name, everyone_tab=True)
                self.people.click_back()


        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_connect_to_calendar(self, email: str, site_name: str, building_name: str, teammates: list,
                               google: bool = True, verification: bool = True, teammate_phone: bool = False):
        """
        Method to validate connect to calendar feature

        :param email:
        :param google:
        :param site_name:
        :param building_name:
        :param verification:
        :param teammate_phone:
        :return :`
        """
        try:
            ui_base = UIBase()
            self.open_app()
            if self.dashboard.verify_home():  # Disconnect if already connected to Calendar
                self.tc_profile_work_account(google=google, verification=False)
            self.settings.click_signin()
            if verification:
                self.report_displayed_or_not("Connect your work account", self.settings.verify_sign_in_screen())
                self.report_displayed_or_not(
                    "I agree that I have read and accept the Terms of Use and the Privacy Policy.",
                    self.settings.verify_privacy_policy_message(), warning=True)
                self.report_displayed_or_not("Privacy policy checkbox", self.settings.verify_privacy_policy_checkbox())
            ui_base.start_performance_test()
            self.settings.enable_privacy_policy_checkbox()
            if google:
                self.sign_in_to_google_account(email=email, verification=verification)
            else:
                self.sign_in_to_microsoft_account(email=email, verification=verification)
            self.settings.click_continue()
            if verification:
                self.report_displayed_or_not("Let's choose a basecamp screen",
                                             self.settings.verify_booking_basecamp_screen(), warning=True)
                self.verify_signin_building(site_name=site_name, building_name=building_name)
            self.building.change_building(site_name=site_name, building_name=building_name)
            if verification:
                self.report_displayed_or_not("Who’s on your team? screen",
                                             self.settings.verify_booking_whos_on_your_team_screen())
                self.report_displayed_or_not("Add coworkers as teammates so you can see their location in the office",
                                             self.settings.verify_booking_whos_on_your_team_message(), warning=True)
                self.verify_signin_teammates(teammates=teammates, verification=verification)
            else:
                self.settings.click_skip()
            ui_base.end_performance_test("Sign-in")
            if self.is_android_device():
                if self.settings.verify_ok():
                    self.settings.click_ok().click_allow()
            if verification:
                self.dashboard.click_people()
                time.sleep(1)
                self.people.click_all_teammates()
                teammates_list = self.people.get_teammates_list()
                result = deepdiff.DeepDiff(teammates, teammates_list, ignore_string_case=True, ignore_order=True)
                self.report_displayed_or_not("All teammates added during sign-in", len(result) == 0)
                self.people.remove_all_teammates().click_back()

        except Exception as e:
            Report.logException(str(e))
            if self.is_android_device():
                if self.settings.verify_signin_close():
                    self.settings.click_signin_close()
            # Clean up
            self.close()
            self.open_app(teammate=teammate_phone)
            if self.settings.verify_signin():
                return
            if self.settings.verify_continue(timeout=10):
                self.settings.click_continue()
                self.building.change_building(site_name=site_name, building_name=building_name)
            if self.settings.verify_confirm():
                self.settings.click_confirm()
            if self.settings.verify_continue():
                self.settings.click_continue()
            if self.settings.verify_done():
                self.settings.click_done()

    def tc_profile_work_account(self, google: bool = True, verification: bool = True):
        """
        Method to validate Profile Work account

        :param google:
        :param verification:
        :return :`
        """
        try:
            ui_base = UIBase()
            self.open_app()
            ui_base.start_performance_test()
            self.dashboard.click_home().click_profile().click_work_account()
            if verification:
                if google:
                    self.report_displayed_or_not("Google Calendar", self.profile.verify_google_calendar())
                else:
                    self.report_displayed_or_not("Office 365 Calendar", self.profile.verify_o365_calendar())
                self.report_displayed_or_not("Connected", self.profile.verify_connected())
                self.report_displayed_or_not("Disconnect Button", self.profile.verify_disconnect_button())
                self.profile.click_disconnect()
                self.report_displayed_or_not("Disconnect work account?", self.profile.verify_disconnect_work_account())
                self.report_displayed_or_not("Disconnect Button", self.profile.verify_confirm_disconnect_button())
                self.report_displayed_or_not("Cancel Button", self.profile.verify_cancel_button())
                self.profile.click_cancel()
                if self.profile.verify_connected():
                    Report.logPass("Work account not disconnected on tapping Cancel", True)
                else:
                    Report.logFail("Work account disconnected on tapping Cancel")
            self.profile.click_disconnect().click_confirm_disconnect()
            self.report_displayed_or_not("Successful logout screen", self.settings.verify_signin())
            ui_base.end_performance_test("Sign-out")
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_connect_to_calendar_skip(self, email: str, site_name: str = None, building_name: str = None,
                                    google: bool = True):
        """
        Method to validate connect to calendar feature when skipping from Basecamp or Choose teammate screen

        :param email:
        :param google:
        :return :`
        """
        try:
            self.open_app()
            if self.dashboard.verify_home():  # Disconnect if already connected to Calendar
                self.tc_profile_work_account(google=google, verification=False)
            self.settings.click_signin()
            # self.open_app().click_settings().click_signin()
            self.settings.enable_privacy_policy_checkbox()
            if google:
                self.sign_in_to_google_account(email=email, verification=False)
            else:
                self.sign_in_to_microsoft_account(email=email, verification=False)
            self.settings.click_continue()
            self.building.change_building(site_name=site_name, building_name=building_name)
            self.settings.click_skip()
            dashboard_building = self.dashboard.get_dashboard_building()
            self.report_displayed_or_not(f"Default building {building_name}", building_name == dashboard_building)
            self.dashboard.click_people().click_all_teammates()
            self.report_displayed_or_not("No Teammates added message", self.people.verify_no_teammates_message())
            self.people.click_back()
            self.tc_profile_work_account(verification=False)

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_connect_to_calendar_no_access(self, email: str, google: bool = True):
        """
        Method to validate connect to calendar feature when skipping from Basecamp or Choose teammate screen

        :param email:
        :param google:
        :return :`
        """
        user_group = self.raiden_api.get_end_user_group(user_email=email)
        try:
            self.raiden_api.delete_end_user(user_email=email)
            self.open_app()
            if self.dashboard.verify_home():  # Disconnect if already connected to Calendar
                self.tc_profile_work_account(google=google, verification=False)
            self.settings.click_signin()
            self.settings.enable_privacy_policy_checkbox()
            if google:
                self.sign_in_to_google_account(email=email, verification=False)
            else:
                self.sign_in_to_microsoft_account(email=email, verification=False, auth=False)
            self.report_displayed_or_not("No Access screen", self.settings.verify_no_access_title())
            self.report_displayed_or_not("No Access message", self.settings.verify_no_access_message())
            self.report_displayed_or_not("Got it button", self.settings.verify_got_it())
            self.settings.click_got_it()
            # Workaround for Bug in iOS
            if self.is_ios_device():
                self.settings.click_back()
            # Workaround for Bug in iOS
            self.report_displayed_or_not("Clicking on got it button, settings screen",
                                         self.settings.verify_signin())

        except Exception as e:
            Report.logException(str(e))
            try:
                if self.settings.verify_continue():
                    self.settings.click_continue()
                    self.building.change_building(site_name="Mobile QA", building_name="Logi-SJ")
                    self.settings.click_skip()
                self.close()
            except Exception as e:
                pass
        self.raiden_api.add_end_user(user_email=email)
        self.raiden_api.update_end_user_group(user_email=email, group_name=user_group[0])

    def tc_user_with_no_basecamp(self, email: str, google: bool = True):
        """
        Method to validate connect to calendar feature when signing-in with user with no basecamp assigned

        :param email:
        :param google:
        :return :`
        """
        groups = "Mobile QA"
        try:
            # groups = self.change_user_group(user=email, group="No Basecamp")
            groups = self.raiden_api.get_end_user_group(user_email=email)
            self.raiden_api.update_end_user_group(user_email=email, group_name="No Basecamp")
            self.open_app()
            if self.dashboard.verify_home():  # Disconnect if already connected to Calendar
                self.tc_profile_work_account(google=google, verification=False)
            self.settings.click_signin()
            # self.open_app().click_settings().click_signin()
            self.settings.enable_privacy_policy_checkbox()
            if google:
                self.sign_in_to_google_account(email=email, verification=False)
            else:
                self.sign_in_to_microsoft_account(email=email, verification=False, auth=False)
            self.report_displayed_or_not("No Basecamp screen", self.settings.verify_no_basecamp_title())
            self.report_displayed_or_not("No Basecamp message", self.settings.verify_no_basecamp_message())
            self.report_displayed_or_not("Got it button", self.settings.verify_got_it())
            self.settings.click_got_it()
            # Workaround for Bug in iOS
            if self.is_ios_device():
                self.settings.click_back()
            # Workaround for Bug in iOS
            self.report_displayed_or_not("Clicking on got it button, Settings screen",
                                         self.settings.verify_signin())
        except Exception as e:
            Report.logException(str(e))
            self.close()
        # self.change_user_group(user=email, group=groups)
        self.raiden_api.update_end_user_group(user_email=email, group_name=groups[0])

    def connect_to_calendar_existing_teammates_account(self, email: str, site_name: str, building_name: str,
                                                       teammates: list, google: bool = True):
        """
        Method to validate connect to calendar feature when signing-in with user who has added teammates previously

        :param email:
        :param google:
        :param site_name:
        :param building_name:
        :return :`
        """
        try:
            self.tc_connect_to_calendar(email=email, site_name=site_name, building_name=building_name,
                                        teammates=teammates, google=google, verification=False)
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates().click_back()
            self.people.click_everyone()
            time.sleep(1)
            for name in teammates:
                self.people.type_in_search(name)
                self.people.click_teammate(name)
                self.people.click_add_to_team().click_add().click_done()
                self.people.click_back()
                # Workaround for Android Bug
                if self.is_ios_device():
                # Workaround for Android Bug
                    self.people.click_clear_search()
            self.tc_profile_work_account(google=google, verification=False)
            self.tc_connect_to_calendar(email=email, site_name=site_name, building_name=building_name,
                                        teammates=teammates, google=google, verification=False)
            self.dashboard.click_people().click_all_teammates()
            teammates_list = self.people.get_teammates_list()
            result = deepdiff.DeepDiff(teammates, teammates_list, ignore_string_case=True, ignore_order=True)
            self.report_displayed_or_not("All teammates added with previous sign-in", len(result) == 0)
            self.people.remove_all_teammates().click_back()
            self.tc_profile_work_account(google=google, verification=False)

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_teammates_search(self, name: bool = True, email: bool = False):
        """
        Method to validate Teammates search functionality under People

        :param name:
        :param email:
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates().click_back()
            self.people.click_everyone()
            time.sleep(1)
            email_list = []
            for teammate_name in test_data.tc_people_teammates_search:
                if self.people.verify_clear_search():
                    self.people.click_clear_search()
                self.people.type_in_search(teammate_name)
                self.people.click_teammate(teammate_name)
                if email:
                    email_list.append(self.people.get_teammate_email(teammate_name=teammate_name))
                self.people.click_add_to_team().click_add().click_done()
                self.people.click_back()
            self.people.click_teammates().click_all_teammates()
            search_list = test_data.tc_people_teammates_search if name else email_list
            for search_text in search_list:
                self.validate_search(search_text=search_text, email=email)
                self.validate_search(search_text=search_text[:3], email=email)
                search_str = search_text[1:4] if name else search_text[3:8]
                self.validate_search(search_text=search_str, email=email, no_results=True)
            self.people.remove_all_teammates().click_back()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone_search(self, name: bool = True, email: bool = False):
        """
        Method to validate Everyone search functionality under People

        :param name:
        :param email:
        :return :`
        """
        try:
            sync_user_groups = self.raiden_api.get_active_user_groups()
            self.open_app()
            self.dashboard.click_people().click_everyone()
            if self.people.verify_clear_search():
                self.people.click_clear_search()
            # Workaround for Android bug
            if self.is_android_device():
                self.people.type_in_search("")
            # Workaround for Android bug
            time.sleep(1)
            mobile_user_groups = self.people.get_user_groups_list()
            result = deepdiff.DeepDiff(sync_user_groups, mobile_user_groups, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"User groups displayed correctly as per Sync Portal - {sync_user_groups}")
            else:
                Report.logFail(f"User groups not displayed correctly as per Sync Portal - "
                               f"{mobile_user_groups} vs {sync_user_groups}")

            search_list = test_data.tc_people_teammates_search if name else test_data.tc_people_email
            for search_text in search_list:
                self.validate_search(search_text=search_text, email=email, teammates=False)
                self.validate_search(search_text=search_text[:3], email=email, teammates=False)
                self.validate_search(search_text=search_text[3:8], email=email, no_results=True, teammates=False)

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_search_all_users(self):
        """
        Method to validate Everyone search functionality under People

        :param name:
        :param email:
        :return :`
        """
        try:
            search_list = self.raiden_api.get_all_end_user_names()
            self.open_app()
            self.dashboard.click_people().click_everyone()
            time.sleep(1)
            i = 0
            for search_text in search_list:
                i += 1
                print(i)
                flag = False
                self.people.type_in_search(search_text)
                results = self.people.get_people_list()
                for result in results:
                    search_result = result.lower()
                    if search_text.lower() == search_result:
                        flag = True
                        break
                if flag:
                    Report.logPass(f"Correct search results displayed for {search_text}")
                else:
                    Report.logFail(f"Incorrect search results displayed for {search_text}")
                self.people.click_clear_search()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_book_validate(self):
        """
        Method to validate booking calendar

        :param email:
        :param google:
        :return :`
        """
        try:

            self.open_app()
            self.dashboard.click_book().click_by_location_and_preferences()
            self.book.click_calendar_icon()
            time.sleep(2)
            self.validate_booking_drag(start_drag=1, end_drag=2)
            self.validate_booking_drag(start_drag=-0.5, end_drag=-0.5)
            self.validate_booking_drag(2)
            self.validate_booking_drag(-0.5)
            self.book.click_confirm()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_book_screen_controls(self):
        """
        Method to book a desk by location

        :param desk_name:
        :param day:
        :return :`
        """
        try:
            self.open_app()
            self.dashboard.click_book()
            verification = self.book.verify_location_and_preferences()
            self.report_displayed_or_not("By location and preferences control", verification=verification)
            verification = self.book.verify_near_teammate()
            self.report_displayed_or_not("Near teammate control", verification=verification)
            self.book.click_close()

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_book_by_location(self, desk_name: str, day: int, start: str, end: str):
        """
        Method to book a desk by location

        :param desk_name:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day)
            future_booking = True if (day == 0 and self.is_ios_device() and start != '') or day > 0 else False
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=future_booking, verification=False)

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_cancel_booking(self, desk_name: str, day: int, start: str, end: str):
        """
        Method to book a desk by location

        :param desk_name:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False)
            future_booking = True if (day == 0 and self.is_ios_device() and start != '') or day > 0 else False
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=future_booking, verification=True)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_check_in_booking(self, desk_name: str, day: int, start: str, end: str, teammates=None):
        """
        Method to book a desk by location

        :param desk_name:
        :param day:
        :return :`
        """
        try:
            ip = self.adb_connect_coily_desk(desk_name=desk_name)
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            if teammates is not None:
                self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates()
                self.people.click_add_teammates()
                time.sleep(1)
                for name in teammates:
                    self.people.type_in_search(name)
                    self.people.click_add(name)
                    self.people.click_clear_search()
                self.people.click_done().click_back()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day,
                                       verification=True, notify_teammate=True)
            self.coily_check_in(coily_ip=ip)
            self.check_in_desk(desk_name=desk_name)
            Report.logPass("Coily checked-in screen", screenshot=True, is_collabos=True)
            self.cancel_booking(desk_name=desk_name, day=day, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_teammate_with_message_during_booking(self, desk_name: str, day: int, start: str, end: str,
                                                       custom_message: str = None):
        """
        Method to book a desk notify teammate with custom message

        :param desk_name:
        :param day:
        :param start:
        :param end:
        :param custom_message:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day,
                                       verification=False, notify_teammate=True, custom_message=custom_message)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=False, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_teammate_with_message_edit_booking(self, desk_name: str, day: int, start: str, end: str,
                                                     custom_message: str = None):
        """
        Method to notify teammate with custom message after booking desk using booking popup

        :param desk_name:
        :param day:
        :param start:
        :param end:
        :param custom_message:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False)
            self.notify_teammate_booking_popup(desk_name=desk_name, custom_message=custom_message)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=False, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_teammate_second_time_edit_booking(self, desk_name: str, day: int, start: str, end: str,
                                                    custom_message: str = None):
        """
        Method to notify teammate with custom message after booking desk using booking popup

        :param desk_name:
        :param day:
        :param start:
        :param end:
        :param custom_message:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False)
            self.notify_teammate_booking_popup(desk_name=desk_name, custom_message=custom_message)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.notify_teammate_booking_popup(desk_name=desk_name, custom_message=custom_message)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=False, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_teammate_emoji(self, desk_name: str, day: int, start: str, end: str,
                                 custom_message: str = None, emoji_count: int = 0):
        """
        Method to notify teammate with emoji message

        :param desk_name:
        :param day:
        :param start:
        :param end:
        :param custom_message:
        :param emoji_count:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            reservation_id = self.book_desk_through_sync_portal(email=TuneMobileConfig.user_email(),
                                                                desk_name=desk_name,
                                                                start=start, end=end, day=day)
            self.open_app()
            self.notify_teammate_booking_popup(desk_name=desk_name, custom_message=custom_message,
                                               emoji_count=emoji_count)
            self.book.click_done()
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_teammate_emoji_text(self, desk_name: str, day: int, start: str, end: str,
                                      custom_message: str = None, emoji_count: int = 0):
        """
        Method to notify teammate with emoji message

        :param desk_name:
        :param day:
        :param start:
        :param end:
        :param custom_message:
        :param emoji_count:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False,
                                       notify_teammate=True, custom_message=custom_message, emoji_count=emoji_count)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification(custom_message=custom_message)
            self.close()
            self.open_app()
            self.cancel_booking(desk_name=desk_name, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_setup_clear_notifications(self):
        """
        Method to clear all notifications before starting notifications tests

        :param :
        :return :
        """
        self.open_app()
        if self.dashboard.click_notification().verify_clear_all():
            self.notification.click_clear_all().click_confirm_clear_all()
        self.notification.click_close()

    def tc_setup_add_teammate(self, teammates) -> bool:
        """
        Method to add teammates

        :param :
        :return :
        """
        self.open_app()
        self.dashboard.click_people().click_all_teammates().remove_all_teammates()
        self.people.click_add_teammates()
        for name in teammates:
            self.people.type_in_search(name)
            self.people.click_add(name)
            self.people.click_clear_search()
        self.people.click_done().click_back()
        return True

    def tc_notify_no_active_notifications(self):
        """
        Method to no active notifications screen

        :param :
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_notification()
            verification = self.notification.verify_no_active_notifications()
            self.report_displayed_or_not("No Active Notifications", verification=verification)
            self.notification.click_close()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_admin_creates_booking(self, email: str, desk_name: str, start: str, end: str, day=0):
        """
        Method to create booking from Sync Portal and verify booking card and notification

        :param email:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :return :
        """
        try:

            reservation_id = self.book_desk_through_sync_portal(email=email, desk_name=desk_name, start=start, end=end,
                                                                day=day)
            self.open_app()
            if self.get_platform_name() == "Android" and self.get_platform_version() in ("13"):
                self.dashboard.click_people()
                self.dashboard.click_home()
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)
            self.verify_admin_creates_booking_notification()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_admin_cancels_booking(self, email: str, desk_name: str, start: str, end: str, day=0):
        """
        Method to delete booking from Sync Portal and verify booking card and notification

        :param email:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :return :
        """
        try:
            reservation_id = self.book_desk_through_sync_portal(email=email, desk_name=desk_name, start=start, end=end,
                                                                day=day)
            self.open_app()
            if self.get_platform_name() == "Android" and self.get_platform_version() in ("13"):
                self.dashboard.click_people()
                self.dashboard.click_home()
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
            time.sleep(5)
            if self.get_platform_name() == "Android" and self.get_platform_version() in ("13"):
                self.dashboard.click_people()
                self.dashboard.click_home()
            if not self.dashboard.verify_booking_card_desk_name(desk_name=desk_name, timeout=2):
                Report.logPass("Booking removed when admin deletes session", screenshot=True)
            else:
                Report.logFail("Booking not removed when admin deletes session")
            self.dashboard.click_notification()
            self.verify_admin_cancels_booking_notification()
            verification = self.notification.verify_show_expired_notifications()
            self.report_displayed_or_not("Show expired notifications", verification=verification)
            verification = self.notification.verify_clear_all()
            self.report_displayed_or_not("Clear All link", verification=verification)
            self.notification.click_show_expired_notifications()
            verification = self.notification.verify_admin_booked_description()
            self.report_displayed_or_not("A desk booking made on your behalf by an administrator", verification)
            verification = self.notification.verify_hide_expired_notifications()
            self.report_displayed_or_not("Hide expired notifications", verification=verification)
            self.notification.click_hide_expired_notifications()
            verification = self.notification.verify_show_expired_notifications()
            self.report_displayed_or_not("Show expired notifications", verification=verification)
            self.notification.click_clear_all().click_confirm_clear_all()
            verification = self.notification.verify_no_active_notifications()
            self.report_displayed_or_not("No Active Notifications", verification=verification)
            self.notification.click_close()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_admin_updates_booking(self, email: str, desk_name: str, start: str, end: str,
                                 updated_start: str, updated_end: str, day: int = 0, updated_day: int = 0):
        """
        Method to delete booking from Sync Portal and verify booking card and notification

        :param email:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :return :
        """
        try:
            reservation_id = self.book_desk_through_sync_portal(email=email, desk_name=desk_name,
                                                                start=start, end=end, day=day)
            self.open_app()
            if self.get_platform_name() == "Android" and self.get_platform_version() in ("13"):
                self.dashboard.click_people()
                self.dashboard.click_home()
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)
            self.dashboard.click_notification().click_clear_all().click_confirm_clear_all().click_close()
            self.update_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id,
                                                    start=updated_start, end=updated_end, day=updated_day)

            time.sleep(5)
            if self.get_platform_name() == "Android" and self.get_platform_version() in ("13"):
                self.dashboard.click_people()
                self.dashboard.click_home()
            self.verify_booking_card(desk_name=desk_name, start=updated_start, end=updated_end)
            self.dashboard.click_notification()
            self.verify_admin_updates_booking_notification(desk_name=desk_name, start=updated_start, end=updated_end)
            self.notification.click_close()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_check_in_required(self, desk_name: str, day: int, start: str, end: str):
        """
        Method to book a desk by location and validate check in required notification

        :param desk_name:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False)
            self.dashboard.click_notification()
            self.verify_check_in_booking_notification(desk_name=desk_name, start=start, end=end)
            self.notification.click_close()
            self.cancel_booking(desk_name=desk_name, day=day, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_book_near_teammate(self, teammate_email: str, teammate_desk: str, desk_name: str,
                              start: str, end: str, day=0, notify_teammate: bool = False, verification: bool = True):
        """
        Method to create booking from Sync Portal and verify booking card and notification

        :param teammate_email:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param notify_teammate:
        :param verification:
        :return :
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            reservation_id = self.book_desk_through_sync_portal(email=teammate_email, desk_name=teammate_desk,
                                                                start=start, end=end, day=day)
            teammate = self.raiden_api.get_user_name_by_email(email=teammate_email)
            self.open_app()
            teammate_name = self.raiden_api.get_user_name_by_email(email=teammate_email)
            self.tc_setup_add_teammate(teammates=[teammate_name])
            self.book_desk_near_teammate(teammate=teammate, desk_name=desk_name, start=start, end=end, day=day,
                                         notify_teammate=notify_teammate, verification=verification)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=True, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_book_near_teammate_from_people_screen(self, teammate_email: str, teammate_desk: str, desk_name: str,
                                                 start: str, end: str, day=0, notify_teammate: bool = False,
                                                 office: bool = False):
        """
        Method to create booking from Sync Portal and verify booking card and notification

        :param teammate_email:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param notify_teammate:
        :return :
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            reservation_id = self.book_desk_through_sync_portal(email=teammate_email, desk_name=teammate_desk,
                                                                start=start, end=end, day=day)
            teammate = self.raiden_api.get_user_name_by_email(email=teammate_email)
            self.open_app()
            self.book_desk_near_teammate_from_people_screen(teammate=teammate, desk_name=desk_name, start=start,
                                                            end=end, day=day,
                                                            notify_teammate=notify_teammate, office=office)
            self.close()
            self.open_app(teammate=True)
            self.verify_teammate_desk_booking_notification()
            self.close()
            self.open_app()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=True, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_cancel_and_rebook(self, desk_name: str, day: int, start: str, end: str):
        """
        Method to book a desk by location

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=False)
            future_booking = True if (day == 0 and self.is_ios_device() and start != '') or day > 0 else False
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=future_booking, verification=False)
            self.book_desk_by_location(desk_name=desk_name, start=start, end=end, day=day, verification=True)
            future_booking = True if (day == 0 and self.is_ios_device() and start != '') or day > 0 else False
            self.cancel_booking(desk_name=desk_name, day=day, future_booking=future_booking, verification=False)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_modify_booking_to_future_date(self, email: str, desk_name: str, day: int, start: str, end: str):
        """
        Method to modify booking to future date

        :param email:
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_date(day=0)
            reservation_id = self.book_desk_through_sync_portal(email=email, desk_name=desk_name, start=start, end=end)
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)
            self.edit_booking(desk_name=desk_name, start='', end='', day=day)
            self.dashboard.click_date(day=day)
            self.verify_booking_card(desk_name=desk_name, start=start, end=end)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_notify_no_teammates_added(self, desk_name: str, day: int, start: str, end: str):
        """
        Method to modify booking to future date

        :param email:
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            self.open_app()
            self.dashboard.click_people().remove_all_teammates()
            self.tc_book_by_location(desk_name=desk_name, day=day, start=start, end=end)

        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_entire_booking_card_clickable(self, email: str, desk_name: str, day: int, start: str, end: str):
        """
        Method to modify booking to future date

        :param email:
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :
        """
        try:
            reservation_id = self.book_desk_through_sync_portal(email=email, desk_name=desk_name,
                                                                start=start, end=end, day=day)
            self.open_app()
            self.dashboard.click_date(day=day)
            floor = self.dashboard.get_booking_card_floor(desk_name=desk_name)
            area = self.dashboard.get_booking_card_area(desk_name=desk_name)
            self.dashboard.click_desk_name(desk_name=desk_name)
            self.verify_modify_booking_screen(desk_name=desk_name, start=start, end=end, future_booking=True)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)


        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone_person_profile(self, email: str):
        """
        Method to validate Everyone search functionality under People

        :param email:
        :return :`
        """
        try:
            desk_name = "SW-QA-Desk1"
            start, end = self.get_start_end_time(booking_duration=1)
            start = datetime.now().strftime("%I:%M %p").lstrip('0')
            self.raiden_api.delete_bookings_for_user(email=email)
            reservation = self.book_desk_through_sync_portal(email=email, desk_name=desk_name,
                                                             start=start, end=end, day=0)

            user_name = self.raiden_api.get_user_name_by_email(email=email)
            self.open_app()
            self.dashboard.click_people().click_everyone()
            if self.people.verify_clear_search():
                self.people.click_clear_search()
            self.people.type_in_search(user_name)
            self.people.click_teammate(teammate=user_name)
            verification = email == self.people.get_teammate_email(teammate_name=user_name)
            self.report_displayed_or_not(f"Email {email}", verification=verification)
            self.verify_people_booking_profile(desk_name=desk_name, start=start, end=end, day=0)
            verification = self.people.verify_locate_on_map()
            self.report_displayed_or_not(f"Locate on Maps", verification=verification)
            self.people.click_back()
            # Workaround for Android Bug
            if self.is_ios_device():
            # Workaround for Android Bug
                self.people.click_clear_search()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_everyone_add_to_teammates_profile(self, user_name: str):
        """
        Method to validate add to teammate in person profile screen

        :param user_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_everyone()
            if self.people.verify_clear_search():
                self.people.click_clear_search()
            self.people.type_in_search(user_name).click_teammate(teammate=user_name)
            verification = self.people.verify_add_to_team()
            self.report_displayed_or_not(f"Add to Team", verification=verification)
            self.people.click_add_to_team()
            verification = self.people.verify_add()
            self.report_displayed_or_not(f"Add button next to All teammates", verification=verification)
            self.people.click_add()
            verification = self.people.verify_remove_manage_teams_screen()
            self.report_displayed_or_not(f"Tapping on Add, Remove button", verification=verification)
            self.people.click_remove_button()
            self.people.click_remove()
            self.people.click_done()
            self.people.click_back()
            # Workaround for Android Bug
            if self.is_ios_device():
            # Workaround for Android Bug
                self.people.click_clear_search()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_teammate_remove_from_teammates_profile(self, user_name: str):
        """
        Method to validate remove from Teammates in person profile screen

        :param user_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_everyone()
            if self.people.verify_clear_search():
                self.people.click_clear_search()
            self.people.type_in_search(user_name)
            self.people.click_teammate(teammate=user_name)
            self.people.click_add_to_team().click_add().click_done()
            self.people.click_back()
            # Workaround for Android Bug
            # self.people.click_clear_search()
            if self.is_ios_device():
                self.people.click_clear_search()
            else:
                self.people.type_in_search("")
            # Workaround for Android Bug
            self.people.click_teammates().click_all_teammates().click_teammate(teammate=user_name)
            verification = self.people.verify_remove_from_teams()
            self.report_displayed_or_not(f"Remove from team button", verification=verification)
            # verification = self.people.verify_favorite_icon()
            # self.report_displayed_or_not(f"Favorite icon", verification=verification)
            self.people.click_remove_from_team().click_remove()
            self.people.click_back().click_back()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_teammate_cancels_booking_notification(self, teammate_email: str, teammate_desk: str, desk_name: str,
                                                 day: int, start: str, end: str):
        """
        Method to book a desk by location

        :param teammate_email:
        :param teammate_desk:
        :param desk_name:
        :param day:
        :param start:
        :param end:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            reservation_id = self.book_desk_through_sync_portal(email=teammate_email, desk_name=teammate_desk,
                                                                start=start, end=end, day=day)
            teammate_name = self.raiden_api.get_user_name_by_email(email=teammate_email)
            self.open_app()
            self.book_desk_near_teammate(teammate=teammate_name, desk_name=desk_name, start=start, end=end, day=day,
                                         notify_teammate=False, verification=False)
            self.tc_setup_clear_notifications()
            self.delete_booking_through_sync_portal(desk_name=teammate_desk, reservation_id=reservation_id)
            self.open_app()
            self.verify_teammate_cancels_booking_notification(teammate_name=teammate_name, desk_name=desk_name,
                                                              start=start, end=end)
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_teammate_modifies_booking_notification(self, teammate_email: str, teammate_desk: str, desk_name: str,
                                                  day: int, start: str, end: str):
        """
        Method to book a desk by location

        :param teammate_email:
        :param teammate_desk:
        :param desk_name:
        :param day:
        :param start:
        :param end:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            reservation_id = self.book_desk_through_sync_portal(email=teammate_email, desk_name=teammate_desk,
                                                                start=start, end=end, day=day)
            teammate_name = self.raiden_api.get_user_name_by_email(email=teammate_email)
            self.open_app()
            self.book_desk_near_teammate(teammate=teammate_name, desk_name=desk_name, start=start, end=end, day=day,
                                         notify_teammate=False, verification=False)
            self.tc_setup_clear_notifications()
            start, end = self.get_start_end_time(booking_duration=2)
            self.update_booking_through_sync_portal(desk_name=teammate_desk, reservation_id=reservation_id,
                                                    start=start, end=end, day=day)
            self.verify_teammate_changed_booking_notification(teammate_name=teammate_name)
            self.delete_booking_through_sync_portal(desk_name=teammate_desk, reservation_id=reservation_id)
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_teammate_with_no_bookings(self):
        """
        Method to validate teammate view when no bookings

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.teammate_email())
            teammate_name = self.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            self.open_app()
            self.tc_setup_add_teammate(teammates=[teammate_name])
            self.people.click_all_teammates().click_teammate(teammate=teammate_name)
            verification = self.people.verify_no_upcoming_booking()
            self.report_displayed_or_not("There are no upcoming bookings for this user. - message", verification)
            self.people.click_back().click_back()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_in_office_no_bookings(self):
        """
        Method to validate teammate view when no bookings

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.teammate_email())
            teammate_name = self.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            self.open_app()
            self.tc_setup_add_teammate(teammates=[teammate_name])
            self.dashboard.click_home()
            for day in [0, 1]:
                self.dashboard.click_date(day=day)
                verification = self.people.verify_no_teammates_in_office()
                self.report_displayed_or_not("No Teammates in office message", verification)
                self.dashboard.click_teammates_in_office()
                verification = self.people.verify_no_teammates_in_office()
                self.report_displayed_or_not("Teammates - No Teammates in office message", verification)
                self.people.click_everyone()
                verification = self.people.verify_no_people_in_office()
                self.report_displayed_or_not("Everyone - No people in office message", verification)
                self.people.click_back()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_in_office_teammate_booked(self, desk_name: str, start: str, end: str, day: int = 0,
                                            teammate: bool = True):
        """
        Method to click on people in office from Dashboard and validate booking for teammate

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param teammate:
        :return :`
        """
        try:
            email = TuneMobileConfig.teammate_email() if teammate else TuneMobileConfig.other_email()
            self.raiden_api.delete_bookings_for_user(email=email)
            reservation_id = self.book_desk_through_sync_portal(email=email,
                                                                desk_name=desk_name, start=start, end=end, day=day)
            teammate_name = self.raiden_api.get_user_name_by_email(email=email)
            self.open_app()
            self.dashboard.click_home()
            self.validate_teammates_in_office(user_name=teammate_name, desk_name=desk_name, start=start, end=end,
                                              day=day, teammate=teammate)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_people_in_office_others_booked(self, desk_name: str, start: str, end: str, day: int = 0):
        """
        Method to click on teammates in office from Dashboard and validate booking for other user

        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.other_email())
            reservation_id = self.book_desk_through_sync_portal(email=TuneMobileConfig.other_email(),
                                                                desk_name=desk_name, start=start, end=end, day=day)
            teammate_name = self.raiden_api.get_user_name_by_email(email=TuneMobileConfig.other_email())
            self.open_app()
            self.tc_setup_add_teammate(teammates=[teammate_name])
            self.dashboard.click_home()
            self.validate_teammates_in_office(user_name=teammate_name, desk_name=desk_name, start=start, end=end,
                                              day=day, teammate=True)
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_teammates_nearby_teammate_booked(self, user_desk: str, teammate_desk: str, other_desk: str,
                                            start: str, end: str, day: int = 0, nearby: bool = True):
        """
        Method to click on teammates near by from booking popup and validate nearby teammate booking

        :param user_desk:
        :param teammate_desk:
        :param other_desk:
        :param start:
        :param end:
        :param day:
        :param teammate:
        :return :`
        """
        try:
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.teammate_email())
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.other_email())
            self.raiden_api.delete_bookings_for_user(email=TuneMobileConfig.user_email())
            user_reservation = self.book_desk_through_sync_portal(email=TuneMobileConfig.user_email(),
                                                                  desk_name=user_desk, start=start, end=end,
                                                                  day=day)
            teammate_reservation = self.book_desk_through_sync_portal(email=TuneMobileConfig.teammate_email(),
                                                                      desk_name=teammate_desk, start=start, end=end,
                                                                      day=day)
            other_reservation = self.book_desk_through_sync_portal(email=TuneMobileConfig.other_email(),
                                                                   desk_name=other_desk, start=start, end=end, day=day)
            teammate_name = self.raiden_api.get_user_name_by_email(email=TuneMobileConfig.teammate_email())
            other_name = self.raiden_api.get_user_name_by_email(email=TuneMobileConfig.other_email())
            self.open_app()
            self.dashboard.click_home()
            self.validate_teammates_nearby(teammate_name=teammate_name, other_name=other_name,
                                           user_desk=user_desk, teammate_desk=teammate_desk, other_desk=other_desk,
                                           start=start, end=end, day=day, nearby=nearby)
            self.delete_booking_through_sync_portal(desk_name=user_desk, reservation_id=user_reservation)
            self.delete_booking_through_sync_portal(desk_name=teammate_desk, reservation_id=teammate_reservation)
            self.delete_booking_through_sync_portal(desk_name=other_desk, reservation_id=other_reservation)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_all_teammates(self):
        """
        Method to validate All Teammates under People

        :param :
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_teammates().click_all_teammates().remove_all_teammates()
            self.people.click_back()
            time.sleep(1)
            verification = self.people.verify_all_teammates()
            self.report_displayed_or_not("All Teammates", verification)
            verification = self.people.verify_new_team()
            self.report_displayed_or_not("New Team button", verification)
            self.people.click_all_teammates()
            verification = self.people.verify_no_teammates_message()
            self.report_displayed_or_not("No Teammates added message", verification)
            verification = self.people.verify_add_teammates_message()
            self.report_displayed_or_not("Add people to teammates in order to see their location in the office message",
                                         verification)
            verification = self.people.verify_add_teammates()
            self.report_displayed_or_not("Add teammates button", verification)
            self.verify_add_teammates_screen()
            self.people.click_back()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_create_new_team(self, team_name: str):
        """
        Method to validate Create New team functionality

        :param team_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people()
            self.create_custom_team(team_name=team_name)
            self.people.remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_add_teammates_screen(self, team_name: str):
        """
        Method to validate Add Teammates screen from custom team

        :param team_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people()
            self.create_custom_team(team_name=team_name, validation=False)
            self.people.click_custom_team(team_name=team_name)
            self.verify_add_teammates_screen()
            self.people.click_back()
            self.people.remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_multiple_teams(self, team_name1: str, team_name2: str, teammates1: list, teammates2: list):
        """
        Method to validate Add Teammates screen from custom team

        :param team_name1:
        :param team_name2:
        :param teammates1:
        :param teammates2:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            self.create_custom_team(team_name=team_name1, validation=False)
            self.create_custom_team(team_name=team_name2, validation=False)
            self.add_teammates_to_custom_team(team_name1, teammates1, False)
            self.add_teammates_to_custom_team(team_name2, teammates2, False)
            teammates1_added = self.people.click_custom_team(team_name1).get_teammates_list(custom_team=True)
            result = deepdiff.DeepDiff(teammates1_added, teammates1, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All teammates displayed in {team_name1} - {teammates1_added}", True)
            else:
                Report.logFail(f"All teammates not displayed correctly - {teammates1_added} vs {teammates1}")
            teammates2_added = self.people.click_back().click_custom_team(team_name2).get_teammates_list(
                custom_team=True)
            result = deepdiff.DeepDiff(teammates2_added, teammates2, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All teammates displayed in {team_name2} - {teammates2_added}", True)
            else:
                Report.logFail(f"All teammates not displayed correctly - {teammates2_added} vs {teammates2}")
            all_teammates = teammates1 + list(set(teammates2) - set(teammates1))
            added_teammates = self.people.click_back().click_all_teammates().get_teammates_list()
            result = deepdiff.DeepDiff(all_teammates, added_teammates, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All Added teammates with no duplicates displayed - {added_teammates}", True)
            else:
                Report.logFail(f"All teammates not displayed correctly - {all_teammates} vs {added_teammates}")
            self.people.remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_all_teammates_search(self, team_name: str):
        """
        Method to validate Add Teammates screen from custom team

        :param team_name:
        :param team_name2:
        :param teammates1:
        :param teammates2:
        :return :
        """
        try:
            search_list = self.raiden_api.get_all_end_user_names()
            teammates = random.sample(search_list, 10)
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            self.create_custom_team(team_name=team_name, validation=False)
            self.add_teammates_to_custom_team(team_name, teammates, False)
            self.people.click_all_teammates()
            self.report_displayed_or_not("Search Bar", self.people.verify_search_control_displayed())
            self.validate_search(search_text=teammates[1][:3])
            self.validate_search(search_text="%*#", no_results=True)
            self.people.click_back()
            self.people.click_custom_team(team_name=team_name)
            self.report_displayed_or_not("No Search Bar", not self.people.verify_search_control_displayed())
            self.people.click_back().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_team_member_profile(self, team_name1: str, team_name2: str, teammates1: list, teammates2: list):
        """
        Method to validate Add Teammates screen from custom team
        :param team_name1:
        :param team_name2:
        :param teammates1:
        :param teammates2:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            self.create_custom_team(team_name=team_name1, validation=False)
            self.create_custom_team(team_name=team_name2, validation=False)
            self.add_teammates_to_custom_team(team_name1, teammates1, False)
            self.add_teammates_to_custom_team(team_name2, teammates2, False)
            self.people.click_custom_team(team_name=team_name1)
            for teammate in teammates1:
                self.people.click_teammate(teammate, booking=True)
                count = 2 if teammate in teammates2 else 1
                self.report_displayed_or_not("Manage Teams", self.people.verify_manage_teams())
                self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
                self.report_displayed_or_not(f"Remove from team button", self.people.verify_remove_from_teams())
                self.report_displayed_or_not(f"Back Arrow", self.people.verify_back())
                self.people.click_back()
            self.people.click_back().click_all_teammates()
            self.people.remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_add_teammates_from_groups(self, team_name: str):
        """
        Method to validate Add Teammates to custom team from Sync Portal groups functionality
        :param team_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            self.create_custom_team(team_name=team_name, validation=False)
            self.people.click_custom_team(team_name=team_name).click_add_teammates()
            groups = self.people.get_user_groups_list(add_teammates=True)
            teammates = []
            for group in groups:
                self.people.click_group(group_name=group)
                users = self.people.get_teammates_list(custom_team=True)
                self.people.click_add(users[0])
                self.report_displayed_or_not(f"ADDED button shown for {users[0]}", self.people.verify_added(users[0]))
                teammates.append(users[0])
                self.people.click_back_to_custom_team()
            self.people.click_done()
            teammates_added = self.people.get_teammates_list(custom_team=True)
            result = deepdiff.DeepDiff(teammates_added, teammates, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All teammates displayed in {team_name} - {teammates_added}", True)
            else:
                Report.logFail(f"All teammates not displayed correctly - {teammates_added} vs {teammates}")
            added_teammates = self.people.click_back().click_all_teammates().get_teammates_list()
            result = deepdiff.DeepDiff(teammates, added_teammates, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All Added teammates displayed in All teammates - {added_teammates}", True)
            else:
                Report.logFail(
                    f"All teammates not displayed correctly in All teammates - {teammates} vs {added_teammates}")
            self.people.remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_add_teammates_to_all_teammates(self):
        """
        Method to validate Add Teammates to All Teammates from Sync Portal groups functionality
        :param :
        :return :
        """
        try:
            team_name = "team_name"
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            for i in range(1, 4):
                self.create_custom_team(team_name=f"{team_name}_{i}", validation=False)
            self.people.click_all_teammates().click_add_teammates()
            teammates = []
            self.people.click_group(group_name="Default")
            users = self.people.get_teammates_list(custom_team=True)
            for i in range(5):
                self.people.click_add(users[i])
                teammates.append(users[i])
                time.sleep(1)
            self.people.click_done()
            added_teammates = self.people.get_teammates_list()
            result = deepdiff.DeepDiff(teammates, added_teammates, ignore_string_case=True, ignore_order=True)
            if len(result) == 0:
                Report.logPass(f"All Added teammates displayed in All teammates - {added_teammates}", True)
            else:
                Report.logFail(
                    f"All teammates not displayed correctly in All teammates - {teammates} vs {added_teammates}")
            self.people.click_back()
            for i in range(1, 3):
                self.people.click_custom_team(team_name=f"{team_name}_{i}")
                self.report_displayed_or_not(f"For custom team {team_name}_{i}, This team is empty",
                                             self.people.verify_team_empty())
                self.people.click_back()
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_teammate_with_bookings(self, team_name: str, desk_name: str, start: str, end: str, day: int = 0):
        """
        Method to validate teammate bookings in custom group
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :param team_name:
        :return :
        """
        try:
            email = TuneMobileConfig.teammate_email()
            teammate_name = self.raiden_api.get_user_name_by_email(email=email)
            self.tc_setup_custom_team_add_teammate(team_name=team_name, teammates=[teammate_name])
            self.raiden_api.delete_bookings_for_user(email=email)
            reservation_id = self.book_desk_through_sync_portal(email=email,
                                                                desk_name=desk_name, start=start, end=end, day=day)
            self.people.click_custom_team(team_name=team_name).click_teammate(teammate=teammate_name, booking=True)
            self.verify_people_booking_profile(desk_name=desk_name, start=start, end=end, day=day)
            self.people.click_back().click_back()
            self.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation_id)
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_teammate_with_no_bookings(self, team_name: str):
        """
        Method to validate teammate with no bookings in custom group
        :param team_name:
        :return :
        """
        try:
            email = TuneMobileConfig.teammate_email()
            teammate_name = self.raiden_api.get_user_name_by_email(email=email)
            self.tc_setup_custom_team_add_teammate(team_name=team_name, teammates=[teammate_name])
            self.raiden_api.delete_bookings_for_user(email=email)
            self.people.click_custom_team(team_name=team_name).click_teammate(teammate=teammate_name, booking=True)
            verification = self.people.verify_no_upcoming_booking()
            self.report_displayed_or_not("There are no upcoming bookings for this user. - message", verification)
            self.people.click_back().click_back()
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_update_name(self, team_name: str, new_team: str):
        """
        Method to validate update custom group name
        :param team_name:
        :param new_team:
        :return :
        """
        try:
            email = TuneMobileConfig.teammate_email()
            teammate_name = self.raiden_api.get_user_name_by_email(email=email)
            teammates = [teammate_name]
            self.tc_setup_custom_team_add_teammate(team_name=team_name, teammates=teammates)
            self.people.click_custom_team(team_name=team_name)
            self.verify_update_team_name(team_name=team_name, new_team=new_team, teammates=teammates)
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_setup_custom_team_add_teammate(self, team_name: str, teammates) -> bool:
        """
        Method to create custom team and add teammates

        :param :
        :return :
        """
        self.open_app()
        self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        self.create_custom_team(team_name=team_name, validation=False)
        self.add_teammates_to_custom_team(team_name=team_name, teammates=teammates, verification=False)
        return True

    def tc_custom_team_edit_remove_teammates(self, team_name: str, count: int):
        """
        Method to validate additional teammate count displayed next to custom team and checking count after removing
        few teammates
        :param team_name:
        :param count:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            teammates = self.tc_setup_custom_team_with_n_teammates(team_name=team_name, count=count)
            additional_teammates_count = len(teammates) - 3
            verification = self.people.get_custom_team_teammate_count(team_name) == additional_teammates_count
            self.report_displayed_or_not(f"Correct additional teammate count {additional_teammates_count}", verification)
            self.people.click_custom_team(team_name=team_name).click_edit()
            deleted_teammates = []
            for i in range(2):
                deleted_teammates.append(teammates[i])
                self.people.click_delete_icon(teammate_name=teammates[i])
                time.sleep(1)
            self.people.click_team_name_tick_mark()
            updated_teammates = self.people.get_teammates_list(custom_team=True)
            if deleted_teammates not in teammates:
                Report.logPass(f"Deleted teammates {deleted_teammates} are not shown in custom team")
            else:
                Report.logFail(f"Deleted teammates {deleted_teammates} are still shown in custom team")
            self.people.click_back()
            additional_teammates_count = len(updated_teammates) - 3
            verification = self.people.get_custom_team_teammate_count(team_name) == additional_teammates_count
            self.report_displayed_or_not(f"Correct additional teammate count {additional_teammates_count}",
                                         verification)
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_edit_delete_team(self, team_name: str):
        """
        Method to validate deleting custom team
        :param team_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            self.create_custom_team(team_name=team_name, validation=False)
            self.people.click_custom_team(team_name=team_name)
            self.verify_delete_team_name(team_name=team_name)
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_profile_remove_from_teammates(self, team_name1: str, team_name2: str):
        """
        Method to validate removing custom group teammate from profile screen
        :param team_name1:
        :param team_name2:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            teammates = self.tc_setup_custom_team_with_n_teammates(team_name=team_name1, count=1)
            self.tc_setup_custom_team_with_n_teammates(team_name=team_name2, count=1)
            self.people.click_custom_team(team_name=team_name1)
            self.validate_remove_teammate(teammate=teammates[0], custom=True)
            self.people.click_back()
            self.people.click_custom_team(team_name=team_name2)
            users = self.people.get_teammates_list()
            verification = not teammates[0] in users
            self.report_displayed_or_not(f"Deleted teammate {teammates[0]}", verification, displayed=False)
            self.people.click_back()
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_manage_teams_add(self, team_name1: str, team_name2: str):
        """
        Method to validate Manage Teams screen from profile and add to team
        :param team_name1:
        :param team_name2:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            teammates = self.tc_setup_custom_team_with_n_teammates(team_name=team_name1, count=1)
            self.create_custom_team(team_name=team_name2, validation=False)
            self.people.click_custom_team(team_name1).click_teammate(teammates[0], booking=True)
            count = 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_manage_teams()
            self.report_displayed_or_not("Done button", self.people.verify_done())
            self.report_displayed_or_not("All teammates", self.people.verify_team_title("All teammates"))
            self.report_displayed_or_not(f"{team_name1}", self.people.verify_team_title(team_name1))
            self.report_displayed_or_not(f"{team_name2}", self.people.verify_team_title(team_name2))
            self.report_displayed_or_not(f"Remove button next to {team_name1}",
                                         self.people.verify_remove_manage_teams_screen(team_name1))
            self.report_displayed_or_not(f"Add button next to {team_name2}", self.people.verify_add(team_name2))
            self.report_displayed_or_not(f"New Team button", self.people.verify_new_team())
            self.people.click_add(team_name2)
            self.report_displayed_or_not(f"Remove button next to {team_name2}",
                                         self.people.verify_remove_manage_teams_screen(team_name2))
            self.people.click_done()
            count += 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_back().click_back()
            self.people.click_custom_team(team_name2)
            self.report_displayed_or_not(f"{teammates[0]} in {team_name2}", self.people.verify_user_name(teammates[0]))
            self.people.click_back()
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_manage_teams_remove(self, team_name: str):
        """
        Method to validate Manage Teams screen from profile and remove from team and all teammates
        :param team_name:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            teammates = self.tc_setup_custom_team_with_n_teammates(team_name=team_name, count=1)
            self.people.click_custom_team(team_name).click_teammate(teammates[0], booking=True)
            count = 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_manage_teams()
            all_teammates_people_count = self.people.get_people_count_in_team("All teammates")
            team_people_count = self.people.get_people_count_in_team(team_name)
            self.people.click_remove_button(team_name)
            self.report_displayed_or_not(f"Add button next to {team_name}", self.people.verify_add(team_name))
            team_people_count_updated = self.people.get_people_count_in_team(team_name)
            self.report_displayed_or_not(f"Correct people count {team_people_count_updated} for {team_name}",
                                         team_people_count_updated == team_people_count - 1)
            self.people.click_remove_button().click_remove()
            self.report_displayed_or_not(f"Add button next to All teammates", self.people.verify_add("All teammates"))
            all_teammates_count_updated = self.people.get_people_count_in_team("All teammates")
            self.report_displayed_or_not(f"Correct people count {all_teammates_count_updated} for All teammates",
                                         all_teammates_count_updated == all_teammates_people_count - 1)
            self.people.click_done()
            count -= 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_back().click_back()

            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_custom_team_manage_teams_new_team(self, team_name: str, new_team: str):
        """
        Method to validate Manage Teams screen from profile and add teammate to new team
        :param team_name:
        :param new_team:
        :return :
        """
        try:
            self.open_app()
            self.dashboard.click_people().click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
            teammates = self.tc_setup_custom_team_with_n_teammates(team_name=team_name, count=1)
            self.people.click_custom_team(team_name).click_teammate(teammates[0], booking=True)
            count = 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_manage_teams().click_new_team()
            if not self.people.verify_create():  # Workaround for iOS 13 and Android 11 bug
                self.people.click_return_key()
            self.people.type_team_name(team_name=new_team).click_create()
            team_people_count = self.people.get_people_count_in_team(new_team)
            self.report_displayed_or_not(f"Correct people count {team_people_count} for {new_team}",
                                         team_people_count == 1)
            self.people.click_done()
            count += 1
            self.report_displayed_or_not(f"Correct Team count {count}", count == self.people.get_team_count())
            self.people.click_back().click_back()
            self.report_displayed_or_not(f"New team {new_team}", self.people.verify_custom_team(team_name=new_team))
            self.people.click_all_teammates().remove_all_teammates().click_back().remove_all_teams()
        except Exception as e:
            Report.logException(str(e))
            self.close()

    def tc_setup_custom_team_with_n_teammates(self, team_name: str, count: int) -> list:
        """
        Method to create custom team and add teammates

        :param team_name:
        :param count:
        :return list:
        """
        users = self.raiden_api.get_all_end_user_names()
        teammates = random.sample(users, count)
        self.open_app()
        self.create_custom_team(team_name=team_name, validation=False)
        self.add_teammates_to_custom_team(team_name, teammates, False)
        return teammates

    def book_desk_through_sync_portal(self, email: str, desk_name: str, start: str, end: str, day: int = 0) -> str:
        """
        Method to book desk through Sync Portal (Raiden API)

        :param email:
        :param desk_name:
        :param start:
        :param end:
        :param day:
        :return :
        """
        self.raiden_api.delete_bookings_for_user(email=email)
        self.delete_all_bookings_through_sync_portal(desk_name=desk_name)
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        return self.raiden_api.create_booking(email_id=email, site=site, building=building, floor=floor,
                                              area=area, desk_name=desk_name, start=start, end=end, day=day)

    def delete_booking_through_sync_portal(self, desk_name: str, reservation_id: str):
        """
        Method to delete booking through Sync Portal (Raiden API)

        :param desk_name:
        :param reservation_id:
        :return :
        """
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        self.raiden_api.delete_booking(site=site, building=building, floor=floor, area=area,
                                       desk_name=desk_name, reservation_id=reservation_id)

    def update_booking_through_sync_portal(self, desk_name: str, reservation_id: str, start: str, end: str,
                                           day: int = 0):
        """
        Method to delete booking through Sync Portal (Raiden API)

        :param desk_name:
        :param reservation_id:
        :param start:
        :param end:
        :param day:
        :return :
        """
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        self.raiden_api.update_booking(site=site, building=building, floor=floor, area=area, desk_name=desk_name,
                                       reservation_id=reservation_id, start=start, end=end, day=day)

    def adb_connect_coily_desk(self, desk_name: str) -> str:
        """
        Method to connect coily device associated with desk using adb

        :param desk_name:
        :return coily_ip:
        """
        site = self.get_desk_site(desk_name=desk_name)
        building = self.get_desk_building(desk_name=desk_name)
        floor = self.get_desk_floor(desk_name=desk_name)
        area = self.get_desk_workspace(desk_name=desk_name)
        coily_ip = self.raiden_api.get_ip_address_of_coily(site=site, building=building, floor=floor,
                                                           area=area, desk_name=desk_name)
        from apps.collabos.coily.utilities import check_and_connect_device
        check_and_connect_device(coily_ip, disconnect_existing_adb=False)
        return coily_ip

    def validate_booking_drag(self, drag_value: float = None, start_drag: float = None, end_drag: float = None):
        schedule = self.book.get_current_schedule()
        start1 = schedule.split("-")[0].strip()
        end1 = schedule.split("-")[1].strip()
        if drag_value is not None:
            self.book.drag_current_booking(drag_value)
        else:
            self.book.drag_end_knob(end_drag)
            self.book.drag_start_knob(start_drag)
        schedule = self.book.get_current_schedule()
        start2 = schedule.split("-")[0].strip()
        end2 = schedule.split("-")[1].strip()
        if drag_value is not None:
            end_drag = start_drag = drag_value
        start = self.compare_time_values(start2, start1) if start_drag > 0 else self.compare_time_values(start1, start2)
        end = self.compare_time_values(end2, end1) if end_drag > 0 else self.compare_time_values(end1, end2)
        if start:
            Report.logPass("Start time changed correctly in the direction of drag")
        else:
            Report.logFail("Start time did not change correctly in the direction of drag")
        if end:
            Report.logPass("End time changed correctly in the direction of drag")
        else:
            Report.logFail("End time did not change correctly in the direction of drag")
