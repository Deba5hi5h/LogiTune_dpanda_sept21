import unittest

from apps.tune.device_parameters_utilities import TuneEnv
from apps.tune.tc_scenarios.appearance_scenarios import AppearanceScenarios
from apps.tune.base.base_testcase import TuneBaseTestCase
from common.framework_params import INSTALLER
from common.ota_versions import TuneVersionGetter
from extentreport.report import Report


class AppearanceTests(TuneBaseTestCase):

    @staticmethod
    def check_if_skip():
        update_version = (TuneVersionGetter().get_tune_version_all_branches().get('Logi Tune').
                          get(TuneEnv.qa).get('version'))
        if INSTALLER != update_version:
            return True
        return False

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=AppearanceScenarios)

    def setUp(self):
        super().setUp()
        self.tune_app.reopen_tune_app()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.tune_app.close_tune_app()

    def test_4001_VC_137565_check_apperance_mode_after_change_with_button(self):
        self.scenario.tc_check_apperance_mode_after_change_with_button()

    def test_4002_VC_137566_check_appearance_mode_applied_after_system_mode_changes(self):
        self.scenario.tc_check_appearance_mode_applied_after_system_mode_changes()

    def test_4003_VC_137567_check_appearance_mode_persistency_after_relaunch(self):
        self.scenario.tc_check_appearance_mode_persistency_after_relaunch()

    def test_4004_VC_137568_check_appearance_mode_persistency_after_update(self):
        if self.check_if_skip():
            Report.logSkip("Skipped because QA version differs from tested version")
            return self.skipTest("Skipped because QA version differs from tested version")
        self.scenario.tc_check_appearance_mode_persistency_after_update()


if __name__ == "__main__":
    unittest.main()
