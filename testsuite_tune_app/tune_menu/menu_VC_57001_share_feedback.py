import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestShareFeedback(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def setUp(self):
        """
        setUp: print testcase title to log and initiate classes
        """
        try:
            super(TestShareFeedback, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            self.tunesApp = TuneElectron()
            self.tuneMethods = TuneUIMethods()

        except Exception as e:
            log.error('Unable to setUp VC57001')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it is still opened
        """
        if self.tunesApp:
            self.tunesApp.close_tune_app()

        super(TestShareFeedback, self).tearDown()

    def test_XXX_VC_97989_menu_share_feedback_webpage_pop_up(self):
        """Verification of Share feedback link
        This test clicks on Share feedback button on Tune menu, it
        will fail if the Share feedback webpage doesn't show up in browser
        and Give feedback button isn't on the webpage
        """
        try:
            self.tuneMethods.tc_verify_share_feedback_webpage()

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestShareFeedback)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
