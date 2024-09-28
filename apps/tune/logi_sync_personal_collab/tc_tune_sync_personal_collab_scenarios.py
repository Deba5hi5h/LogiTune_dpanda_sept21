import socket

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.tune.TuneElectron import TuneElectron
from apps.tune.logi_sync_personal_collab.tune_sync_personal_collab_methods import TuneSyncPersonalCollab
from apps.tune.tune_ui_methods import TuneUIMethods
from base import global_variables
from base.base_ui import UIBase
from common.platform_helper import get_pc_name
from extentreport.report import Report


class TuneSyncScenarios(UIBase):
    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()
    sync_portal = SyncPortalAppMethods()
    tune_sync_personal_collab = TuneSyncPersonalCollab()

    def tc_install_personal_devices_service(self) -> None:
        try:
            self.tune_methods.tc_install_logi_sync_personal_collab_service()
            self.tune_sync_personal_collab.tc_verify_personal_room_in_sync_portal(get_pc_name())
        except Exception as e:
            Report.logException(str(e))

    def tc_verify_device_detection_in_personal_room(self) -> None:
        try:
            # available_devices = ['Brio', 'Brio 105', 'Brio 305', 'Brio 505', 'MX Brio 705 for Business', 'C930e', 'C920e', 'StreamCam', 'Brio 100', 'Brio 101', 'Brio 300', 'Brio 301', 'Brio 500', 'Brio 501', 'MX Brio', 'Zone 305', 'Zone true Wireless', 'Zone Vibe 125', 'Zone Vibe Wireless', 'Zone Wired', 'Zone Wired Earbuds', 'Zone Wireless', 'Zone Wireless Plus', 'Zone Wireless2', 'Zone 300', 'Zone 301', 'Zone 750', 'Zone 900', 'Zone 950', 'Zone Vibe 100', 'Zone Vibe 130', 'Logi Dock', 'Litra Beam']
            available_devices = global_variables.tune_available_devices
            self.tune_sync_personal_collab.tc_verify_personal_device_detected_in_tune_and_sync_portal(available_devices,
                                                                                                      get_pc_name())
            print(f'global_variables.testStatus: {global_variables.testStatus}')
        except Exception as e:
            Report.logException(str(e))

    def tc_uninstall_logi_sync_personal_collab_service(self) -> None:
        try:
            self.tune_methods.tc_uninstall_logi_sync_personal_collab_service()
        except Exception as e:
            Report.logException(str(e))

