import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestAboutPage(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def test_XXX_VC_97991_assert_about_page(self):
        try:
            self.tunesApp = TuneElectron()
            self.tunesApp.open_tune_app()

            self.tunesApp.click_tune_menu()
            about_menu_page = self.tunesApp.click_about_menu()

            about_menu_page.assert_about_page()

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAboutPage)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
