import unittest
from datetime import datetime
import time

from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from common.usb_switch import disconnect_all, connect_device
from extentreport.report import Report

from testsuite_sync_app.tc_methods import SyncTCMethods


class FRE(UIBase):
    sync_app = SyncAppMethods()
    sync_methods = SyncTCMethods()
    sync_portal = SyncPortalAppMethods()

    def test_261_VC_40081_first_run_experience_install_rally(self):
        self.first_run_experience_install('Rally')
        disconnect_all()

    def test_262_VC_40082_first_run_experience_install_rally_camera(self):
        self.first_run_experience_install('Rally Camera')
        disconnect_all()

    def test_263_VC_40083_first_run_experience_install_meetup(self):
        self.first_run_experience_install('MeetUp')
        disconnect_all()

    def first_run_experience_install(self, device_name):
        self.sync_methods.tc_install_sync_app()
        try:
            self.sync_app.open(fre=True)
            self.sync_app.setup.click_get_started()
            self.sync_app.setup_connect_to_sync_portal()
            now = datetime.now()
            room_name = now.strftime("%Y%m%d%H%M%S") + " AutoRoom"
            self.sync_app.setup_room_name_seat_count(room_name=room_name)
            self.sync_app.verify_what_would_you_like_to_setup()
            connect_device(device_name)
            time.sleep(10)
            self.sync_app.verify_device_setup(device_name=device_name)
            self.sync_app.verify_sync_setup_complete_and_share_analytics()
            if self.sync_app.home.verify_device_displayed(device_name=device_name):
                Report.logPass(f"{device_name} displayed in Sync App")
            else:
                Report.logFail(f"{device_name} not displayed in Sync App")
            self.sync_app.close()
            self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name)
        except Exception as e:
            Report.logException(str(e))


if __name__ == "__main__":
    unittest.main()
