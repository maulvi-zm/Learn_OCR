from paddleocr import PaddleOCR, draw_ocr, PPStructure
import cv2

ocr = PaddleOCR(show_log=True, use_angle_cls=True, lang="en")
ser = PPStructure(show_log=True)

img_path = '1.png'
img = cv2.imread(img_path)
structure_result = ser(img)