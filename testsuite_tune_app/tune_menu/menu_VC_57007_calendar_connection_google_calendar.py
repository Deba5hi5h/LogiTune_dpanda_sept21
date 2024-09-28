import logging
import os
import unittest

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestGoogleCalendar(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def setUp(self):
        """
        setUp: Sign in Google account for Google Calendar connection test
        """
        try:
            super(TestGoogleCalendar, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            self.tunesApp = TuneElectron()
            self.tuneMethods = TuneUIMethods()

            self.tuneMethods.tc_connect_to_calendar()

        except Exception as e:
            log.error('Unable to setUp VC57007')
            raise e

    def tearDown(self):
        """
        tearDown: Disconnect Google connection to reset Tune to default status after test and delete token.json
        generated during test
        """
        # Disconnect Google account
        self.tuneMethods.tc_disconnect_calendar()

        # Delete token.json generated during this test
        token_path = os.path.join(UIBase.rootPath, 'apps/tune/token.json')
        if os.path.exists(token_path):
            os.remove(token_path)

        if self.tunesApp:
            self.tunesApp.close_tune_app()

        super(TestGoogleCalendar, self).tearDown()

    def test_XXX_VC_57007_google_calendar_add_delete_event(self):
        """Verification of Tune event status page
        This test creates a Google Calendar event and then deletes it, it
        will fail if the event status doesn't show the corresponding events
        """
        try:
            self.tuneMethods.tc_verify_events()
        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGoogleCalendar)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
