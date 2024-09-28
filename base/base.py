import logging
import os
import psutil
import unittest

from base import global_variables
from common.zephyr_execution_path import Hsinchu
from common.framework_params import DASHBOARD_PUBLISH, JIRA_UPDATE, PROJECT
from common import log_helper
from common.platform_helper import get_custom_platform, get_cpu_vendor, get_installer_version
from common.JiraLibrary import JiraAPI
from extentreport.ExtentManager import ExtentReport
from extentreport.report import Report
from extentreport.dashboard import dashboardAPI

if PROJECT == "LogiTune":
    from common.platform_helper import get_current_system_version, get_platform
    jira = JiraAPI()


log = logging.getLogger(__name__)


class Base(unittest.TestCase):

    logdirectory = log_helper._setup_logging()


    @classmethod
    def setUpClass(cls) -> None:

        global_variables.extentReport = ExtentReport(Base.logdirectory)  # Support for Extent Report
        global_variables.extent = global_variables.extentReport.get_extent_report()  # Support for Extent Report
        if PROJECT == "LogiTune":
            current_testing_machine = (f"Report Tune: {get_installer_version()} {global_variables.test_category} "
                                       f"{get_custom_platform()}{get_current_system_version()}-{get_cpu_vendor()}")
            global_variables.extentReport.htmlReporter.config().setReportName(current_testing_machine)
            global_variables.extentReport.htmlReporter.config().setDocumentTitle(current_testing_machine)

        global_variables.setupFlag = False
        global_variables.reportPath = Base.logdirectory  # Dashboard Support

        #Close USB Hub Tool if open
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if 'HubTool.exe' in proc.name():
                    os.system("Taskkill /IM HubTool.exe")
        else:
            os.system('pkill HubTool')

        if JIRA_UPDATE:
            global_variables.jira = JiraAPI()


    @classmethod
    def tearDownClass(cls) -> None:
        if global_variables.teardownFlag:
            global_variables.extentReport.shutdown_jvm()  # Support for Extent Report
            if DASHBOARD_PUBLISH:
                cls.dashboard = dashboardAPI()
                if PROJECT.upper() == 'LOGITUNE':
                    cls.dashboard.add_tune_report(
                        passed=global_variables.passed,
                        failed=global_variables.failed,
                        blocked=0,
                        skipped=global_variables.skipped
                    )
                else:
                    cls.dashboard.add_report(passed=global_variables.passed,
                                             failed=global_variables.failed,
                                             blocked=0, skipped=global_variables.skipped)


    @classmethod
    def banner(cls, msg):
        """
        This method prints noticeable banner text into the log file.

        :param msg: ``Messages to be printed``
        :type msg: ``string``
        :return: ``None``
        """
        try:
            logging.info('*' * 80)
            logging.info('*** {:^72} ***'.format(msg))
            logging.info('*' * 80)
            # TO-DO: Remove the below comment when all the tests in the suite use the extent report.
            global_variables.reportInstance.log(ExtentReport.Status.INFO, msg)

        except Exception as e:
            logging.error('Error has been thrown: {}'.format(e))
            raise e

    def setUp(self) -> None:
        global_variables.testStatus = "Pass"
        testName = self.__getattribute__("_testMethodName") #self.id().split(".")
        global_variables.reportInstance = global_variables.extent.createTest(testName, "Test Case Details")

    def tearDown(self) -> None:
        retry_count = 1
        while retry_count <= int(global_variables.retry_count) \
                and global_variables.testStatus.upper() == "FAIL" \
                and global_variables.retry_test:
            global_variables.extent.flush()
            global_variables.testStatus = "Pass"
            self.test_status = True
            retry_test = f'{self.__getattribute__("_testMethodName")}_retry{retry_count}'
            # self.test_name = retry_test
            global_variables.reportInstance = global_variables.extent.createTest(retry_test, "Test Case Details")
            eval(f'self.{self.__getattribute__("_testMethodName")}()')
            retry_count += 1
        global_variables.retry_test = True
        testcase_name = self.__getattribute__("_testMethodName")
        splitted_test_case_name = testcase_name.split("_")
        jira_id = splitted_test_case_name[2] + "-" + splitted_test_case_name[3]

        comment = None

        # get members from class
        cycle_name = getattr(self, 'cycle_name', None) or getattr(self, 'device_name', None)
        conn_type = getattr(self, 'conn_type', None)

        try:
            if PROJECT == 'Hsinchu':
                # only update JIRA if JIRA_UPDATE is set to True
                if not JIRA_UPDATE:
                    raise Exception("JIRA_UPDATE is not set to True")

                if cycle_name is None:
                    raise Exception("device_name and cycle_name is not set in class")

                # getting firmware version required tune_app instance in class
                tune_app = getattr(self, 'tune_app', None)
                if (conn_type and tune_app) is None:
                    Report.logInfo("tune_app is not set in class, it may cause firmware version not found")

                execution_path = Hsinchu(cycle=cycle_name, conn_type=conn_type, tune_app=tune_app)
                comment = execution_path.build(jira_id)

                Report.logInfo(f"[Jira Zephyr] Execution of '{execution_path.cycle_name} / {execution_path.folder_name}' created in Jira")

                # for broken testcases, we need to write fail to zephyr
                if hasattr(self._outcome, 'errors') and len(self._outcome.errors):
                    global_variables.jira.execute_test(jira_id, "FAIL", comment)
                    global_variables.extent.flush()  # Support for Extent Report
                    return

        except Exception as e:
            Report.logWarning(f"[Jira Zephyr] Failed to create '{cycle_name} / {conn_type}' in Jira: {e}")

        if str(global_variables.testStatus).upper() == "PASS":
            if JIRA_UPDATE:
                global_variables.jira.execute_test(jira_id, "PASS", comment)
            Report.logPass("Test Case Passed")
            global_variables.passed = global_variables.passed + 1
        elif str(global_variables.testStatus).upper() == "FAIL":
            if JIRA_UPDATE:
                global_variables.jira.execute_test(jira_id, "FAIL", comment)
            if PROJECT == 'LogiTune':
                platform = get_custom_platform()
                cpu_vendor_info = get_cpu_vendor()
                if platform == "windows":
                    jira_platform = "Win"
                else:
                    jira_platform = "Mac"
                print(f"platform: {platform} {jira_id}")
                system_version = f"{jira_platform}{get_current_system_version()}-{cpu_vendor_info}"
                prev_res = jira.tune_check_previous_results_on_platform(tc_id=jira_id,
                                                                        system_platform=system_version)
                prev_str = "Previous results on this platform:"
                for k, v in prev_res:
                    prev_str += f"<br> {k}: {v}"
                Report.logInfo(prev_str)

                prev_defects = jira.tune_check_previous_defects_on_platform(tc_id=jira_id,
                                                                            system_platform=system_version)
                if prev_defects:
                    prev_defects_keys = [el['key'] for el in prev_defects[0]]
                    jira.add_defects_to_execution(jira_id, prev_defects_keys)
                else:
                    jira.add_comment_to_execution(jira_id, "Result under investigation")
            Report.logFail("Test Case Failed")
            global_variables.failed = global_variables.failed + 1
            global_variables.extent.flush()  # Support for Extent Report
            assert False
        elif str(global_variables.testStatus).upper() == "SKIP":
            if JIRA_UPDATE:
                global_variables.jira.execute_test(jira_id, "SKIPPED", comment)
            Report.logInfo("Test Case Skipped")
            global_variables.skipped = global_variables.skipped + 1
        global_variables.extent.flush()  # Support for Extent Report
