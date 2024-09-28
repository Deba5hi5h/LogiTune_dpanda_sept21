import unittest

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report

import tkinter
from tkinter import messagebox


class SyncUpdate(UIBase):
    sync_app = SyncAppMethods()
    sync_portal = SyncPortalAppMethods()
    video_devices = ["MeetUp", "Rally", "Rally Camera", "Rally Bar", "Rally Bar Mini", "Scribe"]
    audio_devices = ["MeetUp", "Rally", "Rally Bar", "Rally Bar Mini"]
    bluetooth_devices = ["Rally Bar", "Rally Bar Mini"]

    def test_261_VC_66516_tap_swytch_connect_guest_pc(self):  # Mapped to Rally camera related test
        self.sync_connect_guest_pc("Rally Bar")

    def sync_connect_guest_pc(self, device_name):

        try:
            root = tkinter.Tk()
            root.withdraw()
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.add_device(device_name=device_name)
            Report.logInfo("Connecting Guest PC")
            messagebox.showinfo("Sync App Automation", "Connect Guest PC")
            self.sync_app.home.click_device("Swytch")
            flag = self.sync_app.device.verify_swytch_connected_to_external_pc_message_displayed(displayed=True)
            self.sync_app.report_displayed_or_not("Swytch is connected to an external computer message", flag)
            self.sync_app.home.click_device(device_name=device_name)
            flag = self.sync_app.device.verify_swytch_byod_device_status_message_displayed(displayed=True)
            self.sync_app.report_displayed_or_not("Status unknown since the device has been connected to an "
                                                  "external computer message", flag)
            if device_name in self.video_devices:
                self.sync_app.home.click_device_camera(device_name=device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag)
            if device_name in self.audio_devices:
                self.sync_app.home.click_device_audio(device_name=device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag)
            if device_name in self.bluetooth_devices:
                self.sync_app.home.click_device_connectivity(device_name=device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag)
            self.verify_swytch_device_in_sync_portal(device_name=device_name, room_name=room_name, byod=True)
            Report.logInfo("Disconnecting Guest PC")
            messagebox.showinfo("Sync App Automation", "Disconnect Guest PC")
            self.sync_app.home.click_device("Swytch")
            flag = self.sync_app.device.verify_swytch_connected_to_external_pc_message_displayed(displayed=True)
            self.sync_app.report_displayed_or_not("Swytch is connected to an external computer message", flag,
                                                  displayed=False)
            self.sync_app.home.click_device(device_name)
            flag = self.sync_app.device.verify_swytch_byod_device_status_message_displayed(displayed=True)
            self.sync_app.report_displayed_or_not("Status unknown since the device has been connected to an "
                                                  "external computer message", flag, displayed=False)
            if device_name in self.video_devices:
                self.sync_app.home.click_device(device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag,
                                                      displayed=False)
            if device_name in self.audio_devices:
                self.sync_app.home.click_device_audio(device_name=device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag,
                                                      displayed=False)
            if device_name in self.bluetooth_devices:
                self.sync_app.home.click_device_connectivity(device_name=device_name)
                flag = self.sync_app.device.verify_swytch_byod_device_settings_message_displayed(displayed=True)
                self.sync_app.report_displayed_or_not("Settings can not be modified now since the device has been "
                                                      "connected to an external computer message", flag,
                                                      displayed=False)
            self.verify_swytch_device_in_sync_portal(device_name=device_name, room_name=room_name, byod=False)
            self.sync_app.forget_device(device_name=device_name)
        except Exception as e:
            Report.logException(str(e))

    def verify_swytch_device_in_sync_portal(self, device_name, room_name, byod):
        driver = global_variables.driver
        try:
            room = self.sync_portal.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                                       role=global_variables.SYNC_ROLE,
                                                                       room_name=room_name).select_device("Swytch")

            if byod:
                if room.verify_swytch_connected_to_external_pc_message_displayed():
                    Report.logPass("Swytch is connected to an external computer message displayed", True)
                else:
                    Report.logFail("Swytch is connected to an external computer message not displayed")
            else:
                if room.verify_swytch_connected_to_external_pc_message_displayed(displayed=False):
                    Report.logPass("Swytch is connected to an external computer message removed", True)
                else:
                    Report.logFail("Swytch is connected to an external computer message still displayed")
            if device_name in self.audio_devices:
                room.select_device_audio(device_name=device_name)
                if byod:
                    if room.verify_swytch_byod_device_settings_message_displayed():
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message displayed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message not displayed")
                else:
                    if room.verify_swytch_byod_device_settings_message_displayed(displayed=False):
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message removed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message still displayed")

            if device_name in self.video_devices:
                room.select_device_camera(device_name=device_name)
                if byod:
                    if room.verify_swytch_byod_device_settings_message_displayed():
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message displayed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message not displayed")
                else:
                    if room.verify_swytch_byod_device_settings_message_displayed(displayed=False):
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message removed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message still displayed")
            if device_name in self.bluetooth_devices:
                room.select_device_connectivity(device_name=device_name)
                if byod:
                    if room.verify_swytch_byod_device_settings_message_displayed():
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message displayed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message not displayed")
                else:
                    if room.verify_swytch_byod_device_settings_message_displayed(displayed=False):
                        Report.logPass("Settings can not be modified now since the device has been connected "
                                       "to an external computer message removed", True)
                    else:
                        Report.logFail("Settings can not be modified now since the device has been connected "
                                       "to an external computer message still displayed")
            self.sync_portal.browser.close_browser()
        except Exception as e:
            Report.logException(str(e))
        global_variables.driver = driver


if __name__ == "__main__":
    unittest.main()
