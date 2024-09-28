import inspect
import logging
import cv2
import os
import time
import traceback
from datetime import datetime
from PIL import Image
from base import global_variables
from extentreport.ExtentManager import ExtentReport
from uuid import uuid1

log = logging.getLogger(__name__)

class Report():
    @staticmethod
    def logPass(logText, screenshot=False, is_collabos=False):
        log.info(logText)
        if not global_variables.reportInstance:
            return
        screenshotLink = ""
        if screenshot:
            screenshotLink = Report.get_screenshot(is_collabos=is_collabos)
        if screenshotLink == "":
            global_variables.reportInstance.log(ExtentReport.Status.PASS, "<b style=\"color:Green\">" + logText + "</b>")
        else:
            global_variables.reportInstance.log(ExtentReport.Status.PASS, "<b style=\"color:Green\">" +logText+ "</b>", screenshotLink)

    @staticmethod
    def logInfo(logText, screenshot=False, color=None, bold=None, is_collabos=False):
        if bold:
            logText = f'\033[1m{logText}\033[0m'

        log.info(logText)

        if not global_variables.reportInstance:
            return
        if color:
            logText = f'<b style=\"color:{color}\">{logText}</b>'
        screenshotLink = ""
        if screenshot:
            screenshotLink = Report.get_screenshot(is_collabos=is_collabos)
        if screenshotLink == "":
            global_variables.reportInstance.log(ExtentReport.Status.INFO, logText)
        else:
            global_variables.reportInstance.log(ExtentReport.Status.INFO, logText, screenshotLink)

    @staticmethod
    def logInfoWithCustomSS(logText, screenshot=None, color=None, bold=None):
        if bold:
            logText = f'\033[1m{logText}\033[0m'
        log.info(logText)
        if not global_variables.reportInstance:
            return
        if color:
            logText = f'<b style=\"color:{color}\">{logText}</b>'
        if screenshot is None:
            global_variables.reportInstance.log(ExtentReport.Status.INFO, logText)
        else:
            # Resize the screenshot to half of its original size
            screenshot = cv2.resize(screenshot, (0, 0), fx=0.5, fy=0.5)
            screenshot_filename = f'{uuid1()}.jpg'  # Change file extension to .jpg
            screenshot_dir = os.path.join(global_variables.reportPath, screenshot_filename)
            cv2.imwrite(screenshot_dir, screenshot,
                        [cv2.IMWRITE_JPEG_QUALITY, 80])  # Compressing the image
            screenshot_link = ExtentReport.MediaEntityBuilder.createScreenCaptureFromPath(
                screenshot_filename).build()
            global_variables.reportInstance.log(ExtentReport.Status.INFO, logText, screenshot_link)

    @staticmethod
    def logWarning(logText, screenshot=False, is_collabos=False):
        log.warning(logText)
        if not global_variables.reportInstance:
            return
        screenshotLink = ""
        if screenshot:
            screenshotLink = Report.get_screenshot(is_collabos=is_collabos)
        if screenshotLink == "":
            global_variables.reportInstance.log(ExtentReport.Status.INFO, "<b style=\"color:Yellow\">" + logText + "</b>")
        else:
            global_variables.reportInstance.log(ExtentReport.Status.INFO,
                                                "<b style=\"color:Yellow\">" + logText + "</b>", screenshotLink)

    @staticmethod
    def logSkip(logText):
        global_variables.testStatus = "Skip"
        global_variables.reportInstance.log(ExtentReport.Status.SKIP, logText)
        log.info(logText)

    @staticmethod
    def logFail(logText, screenshot=True, is_collabos=False) -> str:
        global_variables.testStatus = "Fail"
        screenshotLink = Report.get_screenshot(is_collabos=is_collabos)
        if screenshotLink == "" or not screenshot:
            global_variables.reportInstance.log(ExtentReport.Status.FAIL, "<b style=\"color:Red\">"+logText+"</b>")
        else:
            global_variables.reportInstance.log(ExtentReport.Status.FAIL, "<b style=\"color:Red\">"+logText+"</b>", screenshotLink)
        log.error(logText)
        if global_variables.email_failed:
            test_case = inspect.stack()[1][3]
            if test_case != "tearDown":
                global_variables.email_details = f"{global_variables.email_details}<b style=\"color:Blue\">" \
                                                  f"{test_case}</b> - <b style=\"color:Red\">{logText}</b><br>"
        return logText

    @staticmethod
    def logException(logText, is_collabos=False) -> str:
        global_variables.testStatus = "Fail"
        if logText != 'None':
            screenshotLink = Report.get_screenshot(is_collabos=is_collabos)
            if screenshotLink == "":
                global_variables.reportInstance.log(ExtentReport.Status.FAIL, "<details>" +
                                                    "<summary style=\"color:Red\">Exception Occured</summary>" +
                                                    "<p>" + logText + " </p>" +
                                                    str(traceback.format_stack()).replace('\\n', '<br>') +
                                                    "</details>")
            else:
                global_variables.reportInstance.log(ExtentReport.Status.FAIL, "<details>" +
                                                    "<summary style=\"color:Red\">Exception Occured</summary>" +
                                                    "<p>" + logText + " </p>" +
                                                    str(traceback.format_stack()).replace('\\n', '<br>') +
                                                    "</details>", screenshotLink)

            log.error(f'[EXCEPTION IN: {inspect.getouterframes(inspect.currentframe())[1].function}'
                      f'()] - {str(logText)}')
        return logText

    @staticmethod
    def logResponse(logText):
        global_variables.reportInstance.log(ExtentReport.Status.INFO, "<details>" +
                                            "<summary>API Response</summary>" +
                                            "<p>" + str(logText).replace('\n', '<br>') + " </p>" +
                                            "</details>")

    @staticmethod
    def logRequest(logText):
        global_variables.reportInstance.log(ExtentReport.Status.INFO, "<details>" +
                                            "<summary>API Request</summary>" +
                                            "<p>" + str(logText).replace('\\n', '<br>') + "</p>"
                                                                                          "</details>")

    @staticmethod
    def logScreenshot(folder: str, screenshot_name: str, logText: str, is_collabos=False, delay=False):
        if delay:
            time.sleep(2)
        driver = global_variables.collabos_driver if is_collabos else global_variables.driver
        image_path = f"{global_variables.reportPath}/{folder}"
        if not os.path.exists(image_path): os.makedirs(image_path)
        driver.save_screenshot(f"{image_path}/{screenshot_name}.jpg")
        screenshotLink = ExtentReport.MediaEntityBuilder.createScreenCaptureFromPath(f"{folder}/{screenshot_name}.jpg").build()
        global_variables.reportInstance.log(ExtentReport.Status.PASS,
                                            "<b style=\"color:Green\">" + logText + "</b>", screenshotLink)
        print(f"Made screenshot: {screenshot_name}")
        if delay:
            time.sleep(1)

    @staticmethod
    def get_screenshot(is_collabos=False):
        try:
            now = datetime.now()
            screenshotFile = now.strftime("%Y_%m_%d_%H_%M_%S" + ".png")
            driver = global_variables.collabos_driver if is_collabos else global_variables.driver
            driver.save_screenshot(global_variables.reportPath + "/" + screenshotFile)
            screenshotLink = ExtentReport.MediaEntityBuilder.createScreenCaptureFromPath(screenshotFile).build()
            return(screenshotLink)
        except:
            return("")

    @staticmethod
    def get_element_screenshot(element, name, factor: int = 3):
        try:
            if name == None:
                now = datetime.now()
                screenshotFile = now.strftime("%Y_%m_%d_%H_%M_%S" + ".png")
            else:
                screenshotFile = name+".png"
            element.screenshot(global_variables.reportPath + "/"+ screenshotFile)
            screenshotFile = Report.hi_def_image(screenshotFile, factor=factor)
            screenshotLink = ExtentReport.MediaEntityBuilder.createScreenCaptureFromPath(screenshotFile).build()
            global_variables.reportInstance.log(ExtentReport.Status.PASS,
                                                "<b style=\"color:Green\">Element Screenshot</b>", screenshotLink)
            return(global_variables.reportPath + "/"+ screenshotFile)
        except:
            return("")

    @staticmethod
    def optimize_screenshot_image(image):
        try:
            im = Image.open(global_variables.reportPath + "/"+ image)
            rgb_im = im.convert('RGB')
            jpg_image = os.path.splitext(image)[0] + '.jpg'
            if im.size[0] < 1000:
                im = rgb_im.resize((int(im.size[0]*0.39), int(im.size[1]*0.39)), Image.ANTIALIAS)
            else:
                im = rgb_im.resize((int(im.size[0]*0.3), int(im.size[1]*0.3)), Image.ANTIALIAS)
            im.save(global_variables.reportPath + "/"+ jpg_image, optimize=True, quality=75)
            os.remove(global_variables.reportPath + "/"+ image)
            return jpg_image
        except Exception as e:
            Report.logWarning("Error converting image")
            return image

    @staticmethod
    def hi_def_image(image, factor: int = 3):
        try:
            im = Image.open(global_variables.reportPath + "/" + image)
            rgb_im = im.convert('RGB')
            jpg_image = os.path.splitext(image)[0] + '.jpg'
            im = rgb_im.resize((int(im.size[0] * factor), int(im.size[1] * factor)), Image.ANTIALIAS)
            im.save(global_variables.reportPath + "/" + jpg_image, optimize=True, quality=100)
            os.remove(global_variables.reportPath + "/" + image)
            return jpg_image
        except Exception as e:
            Report.logWarning("Error converting image")
            return image

