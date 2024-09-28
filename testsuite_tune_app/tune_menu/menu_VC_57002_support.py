import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestSupport(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def setUp(self):
        """
        setUp: print testcase title to log and initiate classes
        """
        try:
            super(TestSupport, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            self.tunesApp = TuneElectron()
            self.tuneMethods = TuneUIMethods()

        except Exception as e:
            log.error('Unable to setUp VC57002')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it is still opened
        """
        if self.tunesApp:
            self.tunesApp.close_tune_app()

        super(TestSupport, self).tearDown()

    def test_XXX_VC_97990_menu_support_webpage_pop_up(self):
        """Verification of Support link
        This test clicks on Support button on Tune menu, it
        will fail if the Support webpage doesn't show up in browser
        """
        try:
            self.tuneMethods.tc_verify_support_webpage()

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSupport)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
