import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestQuit(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def test_XXX_VC_97993_assert_quit(self):
        try:
            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()

            self.tunesApp.click_tune_menu()
            self.tunesApp.click_quit_menu()

            # start to verify the process kill
            self.tunesApp.verify_tune_processes_are_active()

            # open Tune again
            self.tunesApp.open_tune_app()
            self.tunesApp.verify_tune_is_running()

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuit)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
