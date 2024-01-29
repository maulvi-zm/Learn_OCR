from paddleocr import PaddleOCR, draw_ocr
from PerspectiveCorrection import preprocess
import matplotlib.pyplot as plt
import cv2

# Activate the OCR machine
ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

# Load the image
image = cv2.imread("assets/image/test7.jpg")

# Preprocces the image
scan = preprocess(image)
cv2.imwrite("assets/correctionImage/4.jpg", scan)

# Procces the image into OCR machine
result = ocr.ocr(scan, cls=True)

# Display the result
image = cv2.cvtColor(scan, cv2.COLOR_BGR2RGB)
boxes = [line[0] for line in result[0]]
txts = [line[1][0] for line in result[0]]
scores = [line[1][1] for line in result[0]]
im_show = draw_ocr(image, boxes, txts, scores, font_path='assets/font/Roboto-Regular.ttf')
plt.figure(figsize=(15, 8))
plt.imshow(im_show)
plt.show()
