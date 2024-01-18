import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Acer\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

img = cv2.imread('4.png')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
text = pytesseract.image_to_string(img)
# print(text)


# # Detecting Character
# h_img,w_img,_ = img.shape
# boxes = pytesseract.image_to_boxes(img)
# boxes = boxes.splitlines()
# for box in boxes:
#     box = box.split(' ')
#     # print(box)
#     left,top,width,height = int(box[1]), int(box[2]), int(box[3]), int(box[4])
#     cv2.rectangle(img, (left,h_img-top), (width,h_img-height), (0,0,255), 2) #sepertinya pengukuran startpoint dan endpoint dimulai dari kiri ke kanan dan atas ke bawah
#     cv2.putText(img, box[0], (left,h_img-bottom+15), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255), 1)


# Detecting Words
h_img,w_img,_ = img.shape
# conf = r'--oem 3 --psm 6 -l kor'
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
# print(data)
# print (len(data["text"]))
for row in range(len(data["text"])):
    if data["text"][row] != '' :
        # print(row)
        text = data["text"][row]
        print(text)
    #     print(box)
        left,top,width,height = int(data["left"][row]), int(data["top"][row]), int(data["width"][row]), int(data["height"][row])
        cv2.rectangle(img, (left,top), (width+left,top+height), (0,0,255), 2) #sepertinya pengukuran startpoint dan endpoint dimulai dari kiri ke kanan dan atas ke bawah
        cv2.putText(img, text, (left,top-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255), 1)

cv2.imshow('result', img)
cv2.waitKey(0)


