from selenium.webdriver.support.events import AbstractEventListener
from extentreport.report import Report
from base.base_ui import UIBase

class CustomListener(AbstractEventListener):
    object = None
    def after_change_value_of(self, element, driver):
        if not UIBase.report_flag:
            UIBase.report_flag = True
            return
        if UIBase.elementName != "":
            Report.logInfo(f'Typing "{element.text}" in element {UIBase.elementName}')
            UIBase.elementName = ""
            return("")
        elif UIBase.send_keys_value != "":
            Report.logInfo(f'Typing "{UIBase.send_keys_value}" in element {element.tag_name}')
            UIBase.elementName = ""
            return("")
        else:
            Report.logInfo(f'Typing "{element.text}" in element {element.tag_name}')

    def before_click(self, element, driver):
        if not UIBase.report_flag:
            UIBase.report_flag = True
            return
        if UIBase.elementName != "":
            Report.logInfo("Clicking on element " + UIBase.elementName)
            UIBase.elementName = ""
            return("")
        if element.text!="":
            Report.logInfo("Clicking on element "+element.text)
        else:
            # self.report.logInfo("Clicking on element " + element.tag_name)
            Report.logInfo("Clicking on element " + self.object)

    def after_find(self, by, value, driver):
        self.object = value

    def after_navigate_to(self, url, driver):
        Report.logInfo("Launching " + url)

    # def on_exception(self, exception, driver):
    #     self.report.logException(str(exception))

class CustomBrowserListener(AbstractEventListener):
    object = None
    report = Report()
    def after_change_value_of(self, element, driver):
        if not UIBase.report_flag:
            UIBase.report_flag = True
            return
        if UIBase.elementName != "":
            Report.logInfo('Typing "' + UIBase.elementName + '" in element ' + element.tag_name)
            UIBase.elementName = ""
            return("")
        Report.logInfo('Typing "'+str(element.get_attribute("Value"))+ '" in element '+str(element.get_attribute("name")))
        # self.report.logInfo('Typing "'+element.text+ '" in element ' + self.object)

    def before_click(self, element, driver):
        if not UIBase.report_flag:
            UIBase.report_flag = True
            return
        if UIBase.elementName != "":
            Report.logInfo("Clicking on element " + UIBase.elementName)
            UIBase.elementName = ""
            return("")
        if element.text!="":
            Report.logInfo("Clicking on element "+element.text)
        else:
            Report.logInfo("Clicking on element " + self.object)

    def after_find(self, by, value, driver):
        self.object = value

    def after_navigate_to(self, url, driver):
        Report.logInfo("Launching " + url)

    # def on_exception(self, exception, driver):
    #     self.report.logException(str(exception))