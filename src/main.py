import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# Load imgae, grayscale, Gaussian blur, Otsu's threshold
def getQR(filename):
    image = cv2.imread(filename)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter for QR code
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]
            return ROI
    return ValueError("No QR code found")

def detectQR(image):
    # Decode QR code
    qrDecoder = cv2.QRCodeDetector()
    miror = cv2.flip(image, 1)
    data, points, straight_qrcode = qrDecoder.detectAndDecode(miror)

    print("Decoded Data : {}".format(data))

print(detectQR(getQR("2.jpg")))
