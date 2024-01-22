import cv2
import numpy as np

# Load image, grayscale, Gaussian blur, adaptive threshold
image = cv2.imread("test/13.png")
def resize_img(width, img):
    # Define the desired width or height
    desired_width = width  # You can set your desired width
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    desired_height = int(desired_width / aspect_ratio)
    # Resize the image
    return cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_LINEAR)

image = resize_img(500, image)
# cv2.imshow("img", image)
# cv2.waitKey(0)
mask = np.zeros(image.shape, dtype=np.uint8)
gray = 255 - cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 51, 3)

# Morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Find distorted rectangle contour and draw onto a mask
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
rect = cv2.minAreaRect(cnts[0])
box = cv2.boxPoints(rect)
box = np.intp(box)
cv2.drawContours(image,[box],0,(36,255,12),2)
cv2.fillPoly(mask, [box], (255,255,255))

# Find corners on the mask
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(mask, maxCorners=4, qualityLevel=0.5, minDistance=150)
print(int (corners))
# for corner in corners:
#     x,y = corner.ravel()
#     cv2.circle(image,(x,y),8,(255,120,255),-1)
#     print("({}, {})".format(x,y))

# cv2.imshow("thresh", thresh)
# cv2.imshow("opening", opening)
# cv2.imshow("mask", mask)
# cv2.imshow("image", image)
# cv2.waitKey(0)