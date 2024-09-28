import unittest

from base.base_ui import UIBase
from base import global_variables
from common.framework_params import JIRA_UPDATE
from extentreport.report import Report


class FwuStressBase(UIBase):

    @classmethod
    def setUpClass(cls) -> None:
        super(FwuStressBase, cls).setUpClass()
        cls.results = []
        cls.ids = []
        cls.retries = 0

    @classmethod
    def tearDownClass(cls) -> None:
        jira_id = list(set(cls.ids))[0]
        print(f'jira_id: {jira_id}')

        print(f'results: {cls.results}')
        # If there is one fail in whole Stress suite tests then whole test will be marked as failed
        if "FAIL" in cls.results:
            test_status = 'FAIL'
        else:
            test_status = 'PASS'

        if test_status == "PASS":
            if JIRA_UPDATE:
                global_variables.jira.execute_test(jira_id, "PASS", comment=cls.results)
        elif test_status == "FAIL":
            if JIRA_UPDATE:
                global_variables.jira.execute_test(jira_id, "FAIL", comment=cls.results)

        super(FwuStressBase, cls).tearDownClass()

    def tearDown(self) -> None:
        testcase_name = self.__getattribute__("_testMethodName")
        print("Completed Test: " + testcase_name)
        print(f"get test status: {str(global_variables.testStatus).upper()}")
        self.results.append(str(global_variables.testStatus).upper())

        global_variables.extent.flush()  # Support for Extent Report
        splitted_test_case_name = testcase_name.split("_")
        jira_id = splitted_test_case_name[2] + "-" + splitted_test_case_name[3]
        self.ids.append(jira_id)

        if str(global_variables.testStatus).upper() == "PASS":
            Report.logPass("Test Case Passed")
            global_variables.passed = global_variables.passed + 1
        elif str(global_variables.testStatus).upper() == "FAIL":
            Report.logFail("Test Case Failed")
            global_variables.failed = global_variables.failed + 1
            assert False

        try:
            if not UIBase.logi_tune_flag:
                global_variables.driver.quit()
        except:
            print("Application is already closed")

    def retry_if_failed(self, input_method, *args, retries: int = 1,  **kwargs):
        try:
            output = input_method(*args, **kwargs)
        except Exception as e:
            if self.retries < retries:
                self.retries += 1
                Report.logException(f'Exception: {str(e)}, Retrying for {retries} time...')
                return self.retry_if_failed(input_method, *args, retries=retries, **kwargs)
            else:
                self.retries = 0
                Report.logException(f'Exception: {str(e)}, Max retries exceeded')
                raise e
        self.retries = 0
        return output
