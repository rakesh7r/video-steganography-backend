from PIL import Image
import numpy as np
from math import log10,sqrt
import cv2 as cv


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


# image1 = Image.open("colorpic.png",'r')
image2 = Image.open("res.png",'r')
image2.save("res2.png")
# image1 = cv.imread("colorpic.png")
image1 = cv.imread("res2.png")
image2 = cv.imread("res.png")
print(PSNR(image1,image2))