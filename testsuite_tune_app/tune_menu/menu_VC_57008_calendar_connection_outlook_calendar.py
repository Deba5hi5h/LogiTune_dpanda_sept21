import logging
import os
import unittest

from apps.tune.calendar_api import OutlookCalendarDriver
from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron
from apps.tune.tune_ui_methods import TuneUIMethods

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestOutlookCalendar(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def setUp(self):
        """
        setUp: Sign in Outlook account for Outlook Calendar connection test
        """
        try:
            super(TestOutlookCalendar, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))
            calendar_api = OutlookCalendarDriver()
            self.tunesApp = TuneElectron()
            self.tuneMethods = TuneUIMethods()

            self.tuneMethods.tc_connect_to_outlook_calendar()

        except Exception as e:
            log.error('Unable to setUp VC57008')
            raise e

    def tearDown(self):
        """
        tearDown: Disconnect Outlook connection to reset Tune to default status after test, closing browser
        """
        self.tuneMethods.tc_disconnect_calendar()

        if self.tunesApp:
            self.tunesApp.close_tune_app()

        super(TestOutlookCalendar, self).tearDown()

    def test_XXX_VC_57008_outlook_calendar_add_delete_event(self):
        """Verification of Tune event status page
        This test creates an Outlook Calendar event and then deletes it, it
        will fail if the event status doesn't show the corresponding events
        """
        try:
            self.tuneMethods.tc_verify_outlook_calendar_event()
            self.tuneMethods.tc_verify_outlook_disconnect_reconnect_event_status()

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOutlookCalendar)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
