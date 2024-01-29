from paddleocr import PaddleOCR, draw_ocr
from PerspectiveCorrection import process
import matplotlib.pyplot as plt
# %matplotlib inline
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)

# Resize image by width
def resize_img_byW(width, img):
    return img.resize((width, int(img.height * (width / img.width))))

# Resize image by height
def resize_img_byH(height, img):
   return img.resize((int(img.width * (height / img.height)), height))


image = cv2.imread("assets/image/test6.jpg")
scan = process(image)
cv2.imwrite("assets/correctionImage/2.jpg", scan)
# img = "test5.jpg"
# im = cv2.imread(img)
# im = resize_img_byW(1000, im)
# cv2.imshow("image",im)
# cv2.waitKey(0)

result = ocr.ocr(scan, cls=True)

for line in result[0]:
  print(line, "\n")
# print(result)
  


# # Display the result
image = cv2.cvtColor(scan, cv2.COLOR_BGR2RGB)
# image = resize_img_byH(1000,image)
boxes = [line[0] for line in result[0]]
txts = [line[1][0] for line in result[0]]
scores = [line[1][1] for line in result[0]]
# # print(scores)
im_show = draw_ocr(image, boxes, txts, scores, font_path='assets/font/Roboto-Regular.ttf')
plt.figure(figsize=(15, 8))
plt.imshow(im_show)
plt.show()
