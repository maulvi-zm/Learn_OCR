import numpy as np
import cv2 as cv
filename = 'test/11.jpg'
img = cv.imread(filename)

def resize_img(width, img):
    # Define the desired width or height
    desired_width = width  # You can set your desired width
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    desired_height = int(desired_width / aspect_ratio)
    # Resize the image
    return cv.resize(img, (desired_width, desired_height), interpolation=cv.INTER_LINEAR)

new_img = resize_img(500, img)

gray = cv.cvtColor(new_img,cv.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
new_img[dst>0.01*dst.max()]=[0,0,255]

# cara gambar garis
# pts  = np.array([[20, 30], [70, 80], [50, 10]], dtype=np.int32)
# new_img = cv.polylines(new_img, [pts] , isClosed=True, color=100, thickness=2)
# print(dst1.max())
# max =  699983,40.0
# for i, row in enumerate(dst1):
#     for j, value in enumerate(row):
#         if (dst1[i][j] > 0.01*dst1.max()):
#             dst1[i][j] = 1
#         else:
#             dst1[i][j] = 0
# print(dst1[0])

# dst = dst1.splitlines()
# for i in dst1:
#     print(i)
#     print("\n")
# print(len(dst1))
# print(len(dst1[0]))
# print(f"Jumlah: {n0+n1}")
# print(f"n0 = {n0}")
# print(f"n1 = {n1}")

# print(dst)
# print(new_img)

# print(new_img)
cv.imshow('new_img',new_img)

if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
