import unittest
from typing import Optional

from base import global_variables
from common.email_notification import EmailNotification
from testsuite_tune_app.tc00_install import TuneInstall


def run_tests(testcases_to_run: list, retry: Optional[int] = None,
              send_mail_project_name: Optional[str] = None,
              mailing: Optional[bool] = True,
              install_tune: bool = False,
              test_category: Optional[str] = None):
    # Load Tests
    load_tests = [unittest.TestLoader().loadTestsFromTestCase(tc_item)
                  for tc_item in testcases_to_run]

    # Setup Suite
    setup_suite = [unittest.TestSuite(loaded_test) for loaded_test in load_tests]
    if install_tune:
        install_suite = unittest.TestSuite()
        install_suite.addTest(TuneInstall('test_001_VC_42593_install_logi_tune'))
        setup_suite = [install_suite, *setup_suite]

    # Run Suite
    if retry is not None:
        global_variables.retry_count = retry
    if mailing:
        global_variables.email_flag = True
        EmailNotification.send_job_email(project_name=send_mail_project_name)
    last_suite = setup_suite.pop(-1)
    global_variables.teardownFlag = False
    for suite in setup_suite:
        unittest.TextTestRunner().run(suite)
    global_variables.teardownFlag = True
    if test_category is not None:
        global_variables.test_category = test_category
    unittest.TextTestRunner().run(last_suite)


def run_sanity_tests(testcases_to_run: list, retry: Optional[int] = None,
              send_mail_project_name: Optional[str] = None):

    # Setup Suite
    setup_suite = [unittest.TestSuite(loaded_test) for loaded_test in testcases_to_run]

    # Run Suite
    if retry is not None:
        global_variables.retry_count = retry
    global_variables.email_flag = True
    EmailNotification.send_job_email(project_name=send_mail_project_name)
    last_suite = setup_suite.pop(-1)
    global_variables.teardownFlag = False
    for suite in setup_suite:
        unittest.TextTestRunner().run(suite)
    global_variables.teardownFlag = True
    unittest.TextTestRunner().run(last_suite)