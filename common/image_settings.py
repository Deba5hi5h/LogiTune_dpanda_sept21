import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class ImageSettings:
    brightness: float
    contrast: float
    saturation: float
    vibrance: float
    sharpness: float


def get_image_settings(img) -> tuple:
    """
    This method retrieves the image settings.
    :param img: full path to image
    :return: brightness, contrast, saturation, sharpness
    :rtype: ``array of float``
    """
    try:
        org_img = cv2.imread(img)
        img_hsv = cv2.cvtColor(org_img, cv2.COLOR_BGR2HSV)
        img_grey = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
        brightness = img_hsv[..., 2].mean()
        saturation = img_hsv[..., 1].mean()
        contrast = img_grey.std()
        sharpness = cv2.Laplacian(img_grey, cv2.CV_64F).var()
        # contrast = img_hsv.std()
        # sharpness = cv.Laplacian(img_hsv, cv.CV_64F).var()
        return brightness, contrast, saturation, sharpness
    except Exception as e:
        print(str(e))
        return 0, 0, 0, 0


def calculate_image_properties(image_path: str) -> ImageSettings:
    """
    Calculate Image Properties for an image and return them as a tuple.

    The properties calculated are Brightness, Contrast, Saturation, Vibrance, and Sharpness.

    Args:
        image_path (str): path to the image file.

    Returns:
        ImageSettings: Brightness, Contrast, Saturation, Vibrance, and Sharpness of the image.
    """
    # Read image
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Brightness is the average value of the pixel intensities
    brightness = np.mean(image)

    # Contrast can be approximated by the standard deviation of the pixel intensities
    contrast = np.std(image)

    # Saturation is the average saturation value (S in HSV)
    h, s, v = cv2.split(hsv_image)
    saturation = np.mean(s)

    # Vibrance is the average vibrance value (V in HSV)
    vibrance = np.mean(v)

    # Sharpness can be approximated by applying a Laplacian filter and calculating the variance
    laplacian_image = cv2.Laplacian(gray_image, cv2.CV_64F)
    sharpness = np.var(laplacian_image)

    # Return the properties as a tuple
    return ImageSettings(brightness, contrast, saturation, vibrance, sharpness)


def get_image_filter_type(img, img_filter):
    """
    This method checks the image filter.
    :param img: full path to original image
    :param img_filter: full path to image with filter applied
    :return: image filter type (bright, blossom, forest, film, glaze, mono_b)
    :rtype: string
    """
    try:
        [brightness, contrast, saturation, sharpness] = get_image_settings(img)
        [brightness_f, contrast_f, saturation_f, sharpness_f] = get_image_settings(img_filter)
        print([brightness, contrast, saturation, sharpness])
        print([brightness_f, contrast_f, saturation_f, sharpness_f])
        psnr = cv2.PSNR(cv2.imread(img), cv2.imread(img_filter))
        print("PSNR = {}".format(psnr))
        if (brightness_f > brightness
                and contrast_f < contrast
                and saturation_f < saturation
                and sharpness_f < sharpness):
            return "Bright"
        elif (brightness_f > brightness
              and contrast_f < contrast
              and saturation_f > saturation
              and sharpness_f > sharpness):
            return "Film"
        elif (brightness_f > brightness
              and contrast_f < contrast
              # and saturation_f > (saturation+200)
              and psnr < 10
              and sharpness_f < sharpness):
            return "Glaze"
        elif (brightness_f > brightness
              and contrast_f < contrast
              # and saturation_f > (saturation+120)
              and psnr < 15
              and sharpness_f < sharpness):
            return "Forest"
        elif (brightness_f > brightness
              and contrast_f < contrast
              and saturation_f > saturation
              and sharpness_f < sharpness):
            return "Blossom"
        elif (brightness_f < brightness
              and contrast_f < contrast
              and saturation_f < saturation
              and sharpness_f < sharpness):
            return "Mono B"
    except Exception as e:
        print(str(e))
        return "unknown"


def compare_images(img1, img2) -> bool:
    """
    This method checks if the 2 images are similar
    :param img1: full path to first image
    :param img2: full path to second image
    :return: True or False
    :rtype: bool
    """
    from PIL import Image
    import imagehash
    hash0 = imagehash.average_hash(Image.open(img1))
    hash1 = imagehash.average_hash(Image.open(img2))
    cutoff = 2  # maximum bits that could be different between the hashes.

    # if hash0 == hash1:
    if hash0 - hash1 < cutoff:
        return True
    else:
        return False
