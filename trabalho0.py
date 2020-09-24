import cv2
import skimage
import sys

print(cv2.__version__)
print(skimage.__version__)

img = cv2.imread("city.png")

if img is None:
    sys.exit("Could not read the image.")

cv2.imshow("Display window", img)
k = cv2.waitKey(0)