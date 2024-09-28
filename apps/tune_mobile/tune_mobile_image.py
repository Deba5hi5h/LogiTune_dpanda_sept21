import imutils
import cv2
import pytesseract  # for OCR
from pytesseract import Output  # for specifying the output type of image_to_boxes

from base import global_variables


class TuneMobileImage():

    @staticmethod
    def get_coordinates(image_path: str):
        """
        Method to get coordinates

        :param :
        :return :
        """
        img = cv2.imread(image_path)

        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to greyscale

        blur = cv2.GaussianBlur(grey, (3, 3), 0)  # blur
        edges = cv2.Canny(blur, 0, 120)  # edges detection

        contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contours finding
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[0:5]  # contours sorting

        rects = list()
        for contour in contours:
            perimeter = cv2.arcLength(contour, closed=True)
            approx = cv2.approxPolyDP(contour, perimeter * 0.015, True)

            if len(approx) == 4:
                rect = approx
                rects.append(rect)

        if len(rects) == 5 or len(rects) == 4:
            detected = cv2.drawContours(img.copy(), [rects[0], rects[2]], -1, (0, 255, 0), 3)

            points_1 = rects[2].reshape(4, 2)
            accept_left_top_x = min([points_1[0][0], points_1[1][0], points_1[2][0], points_1[3][0]])
            accept_left_top_y = min([points_1[0][1], points_1[1][1], points_1[2][1], points_1[3][1]])
            accept_right_bottom_x = max([points_1[0][0], points_1[1][0], points_1[2][0], points_1[3][0]])
            accept_right_bottom_y = max([points_1[0][1], points_1[1][1], points_1[2][1], points_1[3][1]])
            x = accept_right_bottom_x - (accept_right_bottom_x-accept_left_top_x)/2
            y = accept_right_bottom_y - (accept_right_bottom_y-accept_left_top_y)/2
            return x, y

    @staticmethod
    def get_email_coordinates(image_path: str, email: str):
        """
        Method to get coordinates of email

        :param email:
        :return :
        """
        # Set the path to the Tesseract OCR engine (needed for Windows)
        pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.2_1/bin/tesseract'

        # Read screenshot and convert it to grayscale
        screenshot = cv2.imread(image_path)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Extract the bounding boxes for the text in the screenshot
        data = pytesseract.image_to_boxes(screenshot_gray, output_type=Output.DICT)
        h, w, c = screenshot.shape

        email = list(email)
        # Iterate through the bounding boxes
        try:
            for i in range(len(data['char'])):
                # Check if the text of the current bounding box is "Hello World"
                flag = False
                if data['char'][i] == email[0]:
                    flag = True
                    for j in range(len(email)):
                        if data['char'][i + j] != email[j]:
                            flag = False
                            break
                if flag:
                    # Calculate the x and y coordinates of the center of the bounding box
                    x = (data['left'][i] + data['right'][i]) / 2
                    y = (data['top'][i] + data['bottom'][i]) / 2
                    # Click the location
                    print("Clicked at", x, y)
                    # break  # stop looping through the bounding boxes
                    return x, h-y
        except:
            return 0, 0

    @staticmethod
    def get_knob_coordinates(image_path: str):
        """
        Method to get coordinates

        :param :
        :return :
        """
        img = cv2.imread(image_path)
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to greyscale

        blur = cv2.GaussianBlur(grey, (3, 3), 0)  # blur
        edges = cv2.Canny(blur, 0, 120)  # edges detection

        contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contours finding
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[0:5]  # contours sorting

        rects = list()
        for contour in contours:
            perimeter = cv2.arcLength(contour, closed=True)
            approx = cv2.approxPolyDP(contour, perimeter * 0.015, True)

            if len(approx) == 4:
                rect = approx
                rects.append(rect)

        detected = cv2.drawContours(img.copy(), [rects[0], rects[1]], -1, (0, 255, 0), 3)

        points_1 = rects[1].reshape(4, 2)
        accept_left_top_x = min([points_1[0][0], points_1[1][0], points_1[2][0], points_1[3][0]])
        accept_left_top_y = min([points_1[0][1], points_1[1][1], points_1[2][1], points_1[3][1]])
        accept_right_bottom_x = max([points_1[0][0], points_1[1][0], points_1[2][0], points_1[3][0]])
        accept_right_bottom_y = max([points_1[0][1], points_1[1][1], points_1[2][1], points_1[3][1]])
        print(accept_left_top_x, accept_left_top_y, accept_right_bottom_x, accept_right_bottom_y)
        x = accept_right_bottom_x
        y = accept_right_bottom_y
        return x, y

    @staticmethod
    def get_text_coordinates(image_path: str, text: str):
        """
        Method to get coordinates of email

        :param image_path: Path of image to find text coordinates
        :param text: text to find in the image
        :return :
        """
        # Set the path to the Tesseract OCR engine
        pytesseract.pytesseract.tesseract_cmd = global_variables.tesseract_cmd

        # Read screenshot and convert it to grayscale
        screenshot = cv2.imread(image_path)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Extract the bounding boxes for the text in the screenshot
        data = pytesseract.image_to_boxes(screenshot_gray, output_type=Output.DICT)
        h, w, c = screenshot.shape
        text = text.replace(' ', '')
        search_text = list(text)
        # Iterate through the bounding boxes
        try:
            for i in range(len(data['char'])):
                flag = False
                if data['char'][i] == search_text[0]:
                    flag = True
                    for j in range(len(search_text)):
                        if data['char'][i + j] != search_text[j]:
                            flag = False
                            break
                if flag:
                    # Calculate the x and y coordinates of the center of the bounding box
                    x = (data['left'][i] + data['right'][i]) / 2
                    y = (data['top'][i] + data['bottom'][i]) / 2
                    return x, h - y
        except:
            return 0, 0

