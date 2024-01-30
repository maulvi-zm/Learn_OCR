from paddleocr import PaddleOCR, draw_ocr

# OCR Engine
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

result = ocr.ocr("src/images/1.jpg", cls=True)
for line in result:
    print(line)



