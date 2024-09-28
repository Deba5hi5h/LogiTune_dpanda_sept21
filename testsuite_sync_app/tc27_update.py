import os
import unittest
from datetime import datetime
import time

import psutil

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.sync_app import SyncApp
from apps.sync.AppInstall import AppInstall
from apps.sync.sync_app_methods import SyncAppMethods
from base import global_variables
from base.base_ui import UIBase
from common.framework_params import INSTALLER, SYNC_PROD_VERSION1, SYNC_PROD_VERSION2
from common.json_helper import JsonHelper
from common.platform_helper import get_custom_platform
from common.usb_switch import disconnect_device
from extentreport.report import Report
from testsuite_sync_app.tc_methods import SyncTCMethods


class SyncUpdateThirdParty(UIBase):
    sync_app = SyncAppMethods()
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()
    sync_version1 = SYNC_PROD_VERSION1
    sync_version2 = SYNC_PROD_VERSION2
    app = AppInstall()

    def setUp(self) -> None:
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if 'WinAppDriver.exe' in proc.name():
                    print(f'Killing {proc.name()}')
                    proc.kill()
            os.system(str(UIBase.rootPath) + "\\WinApp\\winapp.bat")
        super(SyncUpdateThirdParty, self).setUp()

    def test_2706_VC_58236_tap_rally_swytch_sync_update(self):
        self.sync_update(["Tap", "Rally", "Swytch"])

    def test_2707_VC_58237_tap_rallycamera_swytch_sync_update(self):
        self.sync_update(["Tap", "Rally Camera", "Swytch"])

    def test_2708_VC_58238_swytch_meetup_tap_sync_update(self):
        self.sync_update(["Swytch", "MeetUp", "Tap"])

    def test_2709_VC_58239_tap_rallybar_swytch_scribe_sync_update(self):
        self.sync_update(["Tap", "Rally Bar", "Swytch", "Scribe"])

    def test_2710_VC_58241_tap_rallybarmini_swytch_scribe_sync_update(self):
        self.sync_update(["Tap", "Rally Bar Mini", "Swytch", "Scribe"])

    def test_2711_VC_58243_tap_c925e_sync_update(self):
        self.sync_update(["Tap", "C925e"])

    def test_2712_VC_58244_c930e_tap_swytch_sync_update(self):
        self.sync_update(["C930e", "Tap", "Swytch"])

    def test_2713_VC_58246_tap_group_sync_update(self):
        self.sync_update(["Tap", "Group"])

    def test_2714_VC_58250_tap_cc3000e_sync_update(self):
        self.sync_update(["Tap", "CC3000e"])

    def test_2715_VC_58247_tap_ptzpro2_sync_update(self):
        self.sync_update(["Tap", "PTZ Pro2"])

    def test_2716_VC_58254_tap_avervb342_sync_update(self):
        self.sync_update(["Tap", "AVer VB342"])

    def test_2717_VC_58258_tap_avervc520plus_sync_update(self):
        self.sync_update(["Tap", "AVer VC520+"])

    def test_2718_VC_58256_tap_yamahacs700_sync_update(self):
        self.sync_update(["Tap", "Yamaha CS-700"])

    def test_2719_VC_58257_tap_aver540_sync_update(self):
        self.sync_update(["Tap", "AVer 540"])

    def sync_update(self, device_list, update=True):
        global_variables.SYNC_FUTEN = 'futen-staging'
        right_sight_devices = ["Rally Bar Mini", "Rally Bar", "MeetUp", "Rally", "Rally Camera"]
        delayed_devices = ["Rally Bar Mini", "Rally Bar", "Scribe"]
        try:
            self.sync_methods.tc_install_sync_app(version=self.sync_version1)
            self.sync_app.open()
            self.connect_to_sync_portal()
            for device in device_list:
                self.sync_app.add_device(device_name=device)
            disconnect_device(device_list[0])
            time.sleep(5)
            if device_list[0] in delayed_devices:
                time.sleep(30)
            self.sync_app.home.click_room()
            devices_before_update = self.sync_app.home.get_number_of_nodes()
            Report.logPass("Devices before update", True)
            room_name = self.sync_app.home.get_room_name()
            self.sync_portal.verify_devices_added_in_sync_portal(device_list, room_name=room_name)
            # Second Install
            if not update:
                self.sync_app.close()
                time.sleep(2)
                if get_custom_platform() == "windows":
                    self.app.installApp(version=self.sync_version2)
                else:
                    self.app.install_sync_mac(version=self.sync_version2)
                self.sync_app.open()
                time.sleep(30)
                self.sync_app.home.click_room()
                devices_after_update = self.sync_app.home.get_number_of_nodes()
                Report.logPass("Devices before update", True)
                if devices_before_update == devices_after_update:
                    Report.logPass("Same devices exist after update", True)
                else:
                    Report.logWarning("After Sync update Device list is not same")
                for device in device_list:
                    self.sync_app.verify_device_displayed_in_sync_app(device_name=device)
                self.sync_portal.verify_devices_added_in_sync_portal(device_list, room_name=room_name)
            # Final Install
            for x in range(len(device_list)):
                if x == 0:
                    continue
                if device_list[x] in right_sight_devices:
                    self.sync_app.home.click_device_camera(device_name=device_list[x])
                    time.sleep(5)
                    self.sync_app.camera.disable_right_sight()
                    self.sync_app.verify_rightsight(enabled=False)

            self._sync_upate_from_menu()

            self.sync_app.open()
            time.sleep(70)
            self.sync_app.home.click_room()
            devices_after_update = self.sync_app.home.get_number_of_nodes()
            if devices_before_update == devices_after_update:
                Report.logPass("Same devices exist after update", True)
            else:
                Report.logFail("After Sync update Device list is not same")
            for device in device_list:
                self.sync_app.verify_device_displayed_in_sync_app(device_name=device)
            self.sync_portal.verify_devices_added_in_sync_portal(device_list, room_name=room_name)
            for x in range(len(device_list)):
                if x == 0:
                    continue
                if device_list[x] in right_sight_devices:
                    self.sync_app.home.click_device_camera(device_name=device_list[x])
                    self.sync_app.verify_rightsight(enabled=False)
                    self.sync_app.camera.enable_right_sight()
        except Exception as e:
            Report.logException(str(e))
        self.sync_app.close()

    def connect_to_sync_portal(self):
        now = datetime.now()
        room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        self.sync_app.rename_room(room_name=room_name).connect_to_sync_portal(config=global_variables.config,
                                                                              role=global_variables.SYNC_ROLE,
                                                                              org_name=org_name)

    def _sync_upate_from_menu(self):
        global_variables.SYNC_FUTEN = 'futen-staging-qa'
        if get_custom_platform() == "windows":
            sync_config = 'C:/ProgramData/Logitech/LogiSync/sync-config.json'
            JsonHelper.update_json(sync_config, 'futen,current', global_variables.SYNC_FUTEN)
            SyncApp.restart_sync_services()
            self.app.update_sync_from_menu()
        else:
            self.app.install_sync_mac(version=INSTALLER)


if __name__ == "__main__":
    unittest.main()
