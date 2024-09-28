from jpype import *
from datetime import datetime
import os
from pathlib import Path

from common.platform_helper import get_custom_platform


class ExtentReport():
    currentDirectory = os.path.dirname(__file__)
    rootPath = Path(currentDirectory).parent
    classpath = str(rootPath) + '/extentreport/extentreports-4.0.5.jar;' + str(
        rootPath) + '/extentreport/freemarker-2.3.23.jar;' + str(rootPath) + '/extentreport/bson-3.3.0.jar'
    if get_custom_platform() != "windows":
        classpath = str(classpath).replace(";", ":")

    if not isJVMStarted():
        startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)
    ExtentReports = JClass('com.aventstack.extentreports.ExtentReports')
    ExtentTest = JClass('com.aventstack.extentreports.ExtentTest')
    ExtentHtmlReporter = JClass('com.aventstack.extentreports.reporter.ExtentHtmlReporter')
    MediaEntityBuilder = JClass('com.aventstack.extentreports.MediaEntityBuilder')
    Status = JClass('com.aventstack.extentreports.Status')

    def __init__(self, reportPath):
        self.htmlReporter = self.ExtentHtmlReporter(reportPath + "/Test_Report.html")
        self.htmlReporter.loadXMLConfig(str(self.rootPath)+'/extentreport/ReportsConfig.xml')
        self.htmlReporter.config().setCSS(".r-img { width: 3%; }");

    def get_extent_report(self):
        extent = self.ExtentReports()
        extent.attachReporter(self.htmlReporter)
        return extent

    def shutdown_jvm(self):
        shutdownJVM()
