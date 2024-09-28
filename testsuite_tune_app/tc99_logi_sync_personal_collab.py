
import unittest

from apps.tune.TuneElectron import TuneElectron
from apps.tune.logi_sync_personal_collab.install_logi_sync_personal_collab import InstallLogiSyncPersonalCollab
from apps.tune.logi_sync_personal_collab.tc_tune_sync_personal_collab_scenarios import TuneSyncScenarios
from base.base_ui import UIBase
from extentreport.report import Report


class LogiSyncPersonalCollab(UIBase):

    tune_sync_methods = TuneSyncScenarios()
    tune_app = TuneElectron()

    @classmethod
    def tearDownClass(cls) -> None:
        Report.logInfo("Uninstall Personal CollabOS at the end of the suite")
        installer = InstallLogiSyncPersonalCollab()
        result = installer.uninstall_logi_sync_personal_collab()
        assert result is True, Report.logFail("Personal CollabOS not uninstalled correctly.")
        super(LogiSyncPersonalCollab, cls).tearDownClass()

    def test_9901_VC_144324_install_personal_device_service(self) -> None:
        self.tune_sync_methods.tc_install_personal_devices_service()

    def test_9902_VC_144325_verify_device_detection_in_personal_room(self) -> None:
        self.tune_sync_methods.tc_verify_device_detection_in_personal_room()

    def test_9903_VC_144326_tc_uninstall_personal_device_service(self) -> None:
        self.tune_sync_methods.tc_uninstall_logi_sync_personal_collab_service()


if __name__ == "__main__":
    unittest.main()
