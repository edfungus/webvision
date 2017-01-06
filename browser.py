from __future__ import absolute_import
from __future__ import division
# from __future__ import print_function

from selenium import webdriver
import numpy as np
import cv2 as cv

###
# Try automating finding elements on a webpage and get the bounding box (which can be used for training)
###

browserWidth = 1200
browserHeight = 800 

browser = webdriver.Chrome()
browser.set_window_size(browserWidth, browserHeight + 74)   # 74 is for the Chrome nav bar
browser.get("https://www.tensorflow.org/how_tos/variables/")

divDetails = browser.execute_script("return document.getElementsByClassName(\"devsite-product-name-wrapper\")[0].getBoundingClientRect();")

screenshotRaw = browser.get_screenshot_as_png()

browser.quit()

print(divDetails)
top = int(divDetails["top"])
left = int(divDetails["left"])
right = int(divDetails["right"])
bottom = int(divDetails["bottom"])

screenshot = np.asarray(bytearray(screenshotRaw), dtype=np.uint8)
screenshotImage = cv.imdecode(screenshot, cv.IMREAD_UNCHANGED)
screenshotBox = cv.rectangle(screenshotImage, (left,top), (right,bottom), (0,255,0), 3)
print(screenshot.shape)
print(screenshotImage.shape)

cv.imshow("screenshot_original", screenshotBox)
cv.waitKey()
cv.destroyAllWindows()
