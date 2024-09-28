import unittest

from apps.tune.device_parameters_utilities import TuneEnv
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import INSTALLER
from common.ota_versions import TuneVersionGetter
from common.platform_helper import get_installer_version
from extentreport.report import Report


class TuneAppUpdate(UIBase):
    """
    Test class containing LogiTune App Update tests.
    """
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()

    @staticmethod
    def check_if_skip():
        tune_apps_versions = TuneVersionGetter().get_tune_version_all_branches().get('Logi Tune')
        qa = tune_apps_versions.get(TuneEnv.qa).get('version')
        Report.logInfo(f"INSTALLER version: {INSTALLER}")
        installer_version = get_installer_version()
        Report.logInfo(f"QA version: {qa}")
        Report.logInfo(f"Installer version: {INSTALLER}")
        if installer_version != qa:
            return True
        return False

    def test_2701_VC_114647_tune_app_prod_to_qa_update(self) -> None:
        if self.check_if_skip():
            Report.logSkip("Skipping because tested version != QA version")
            return self.skipTest("Skipping because tested version != QA version")
        self.tune_methods.tc_update_tune_app(TuneEnv.prod, TuneEnv.qa)

    def test_2702_VC_114648_tune_app_qa_to_dev2_update(self) -> None:
        if self.check_if_skip():
            Report.logSkip("Skipping because tested version != QA version")
            return self.skipTest("Skipping because tested version != QA version")
        self.tune_methods.tc_update_tune_app(TuneEnv.qa, TuneEnv.dev2)


if __name__ == "__main__":
    unittest.main()
