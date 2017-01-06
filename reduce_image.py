from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2 as cv
import time

###
# The default INTER_LINEAR seems to give the best results per performance
###

image = cv.imread("image1.png")
image_small_linear = cv.resize(image, (int(image.shape[1]/4), int(image.shape[0]/4)))
image_mid_linear = cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
image_small_area = cv.resize(image, (int(image.shape[1]/4), int(image.shape[0]/4)), interpolation=cv.INTER_AREA)
image_mid_area = cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)), interpolation=cv.INTER_AREA)
image_mid_nearest = cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)), interpolation=cv.INTER_NEAREST)

count = 100

currentTimeSmallLinear = time.time() * 1000.0
for i in range(count):
    cv.resize(image, (int(image.shape[1]/4), int(image.shape[0]/4)))
currentTimeSmallLinear = (time.time() * 1000.0 - currentTimeSmallLinear) / count

currentTimeMidLinear = time.time() * 1000.0
for i in range(count):
    cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
currentTimeMidLinear = (time.time() * 1000.0 - currentTimeMidLinear) / count

currentTimeSmallArea = time.time() * 1000.0
for i in range(count):
    cv.resize(image, (int(image.shape[1]/4), int(image.shape[0]/4)), interpolation=cv.INTER_AREA)
currentTimeSmallArea = (time.time() * 1000.0 - currentTimeSmallArea) / count

currentTimeMidArea = time.time() * 1000.0
for i in range(count):
    cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)), interpolation=cv.INTER_AREA)
currentTimeMidArea = (time.time() * 1000.0 - currentTimeMidArea) / count

currentTimeMidNearest = time.time() * 1000.0
for i in range(count):
    cv.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)), interpolation=cv.INTER_NEAREST)
currentTimeMidNearest = (time.time() * 1000.0 - currentTimeMidNearest) / count


print("Small Linear: \t {}".format(currentTimeSmallLinear)) 
print("Mid Linear: \t {}".format(currentTimeMidLinear)) 
print("Small Area: \t {}".format(currentTimeSmallArea)) 
print("Mid Area: \t {}".format(currentTimeMidArea)) 
print("Mid Nearest: \t {}".format(currentTimeMidNearest)) 


cv.imshow("image_original", image)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("image_small_linear", image_small_linear)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("image_mid_linear", image_mid_linear)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("image_small_area", image_small_area)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("image_mid_area", image_mid_area)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("image_mid_nearest", image_mid_nearest)
cv.waitKey()
cv.destroyAllWindows()

cv.imwrite('mid_linear.png',image_mid_linear)
cv.imwrite('mid_area.png',image_mid_area)
cv.imwrite('mid_nearest.png',image_mid_nearest)
