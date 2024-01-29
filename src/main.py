import cv2
import numpy as np
import os

# Resize image by width
def resize_img_byW(width, img):
    # Define the desired width or height
    desired_width = width  # You can set your desired width
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0] #lebar/tinggi
    desired_height = int(desired_width / aspect_ratio)
    # Resize the image
    return cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_LINEAR)

# Resize image by height
def resize_img_byH(height, img):
    # Define the desired height or height
    desired_height = height  # You can set your desired height
    # Calculate the corresponding height to maintain the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    desired_width = int(aspect_ratio*desired_height)
    # Resize the image
    return cv2.resize(img, (desired_width, desired_height), interpolation=cv2.INTER_LINEAR)

def resize(scale, img):
    if(img.shape[0]>img.shape[1]):
        img = resize_img_byH(scale, img)
    else:
        img = resize_img_byW(scale, img)
    return img

def drawline(lines, image):
    for line in lines:
        rho, theta = line[0]
    
        # Calculate the endpoints of the line to span the entire image
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        
        # Calculate endpoints
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    return image

def houghline(canny):
    t = 300
    j = 0

    # Loop to find lines with decreasing threshold
    while j < 8 and t > 0:
        try:
            linesP = cv2.HoughLines(canny, 1, np.pi/180, t)
            if linesP is not None:
                j = linesP.shape[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            j = 0
        t = t - 10

    # Initialize variables
    lines = linesP.reshape(linesP.shape[0], 2)
    lu = []

    # Filter duplicate lines
    for i, l in enumerate(lines):
        rho, theta = l
        is_duplicate = False
        
        for lt in lines[i + 1:]:
            rhot, thetat = lt
            # Set threshold for similarity
            rho_threshold, theta_threshold = 50, 0.5
            # Check if lines are similar
            if abs(rhot - rho) < rho_threshold and abs(thetat - theta) < theta_threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            lu.append(l)

    # Reshape and store final lines
    lr = np.asarray(lu[:])
    j = np.reshape(lr, [lr.shape[0], 1, 2])

    return j

def l_inter(line1, line2):
    r1, t1 = line1
    r2, t2 = line2
    A = np.array([[np.cos(t1), np.sin(t1)], [np.cos(t2), np.sin(t2)]])
    b = np.array([[r1], [r2]])

    try:
        # Solve the system of equations to find the intersection point
        intersection_point = np.linalg.solve(A, b)
        x, y = intersection_point.ravel()
    except np.linalg.LinAlgError:
        # Lines are parallel or nearly parallel, return None
        return None

    return [x, y]

def points_inter(lines, lower_angle_bound=70, upper_angle_bound=120):
    intersections = []

    lower_angle_bound = np.deg2rad(lower_angle_bound)
    upper_angle_bound = np.deg2rad(upper_angle_bound)

    for i, line_group in enumerate(lines[:-1]):
        for line_group_next in lines[i + 1:]:
            for line1 in line_group:
                for line2 in line_group_next:
                    intersection = l_inter(line1, line2)
                    
                    if intersection is not None:
                        # Hitung sudut garis yang terbentuk oleh dua garis yang bersilangan
                        angle = np.abs(line1[1] - line2[1])
                        
                        # Filter berdasarkan sudut
                        if lower_angle_bound <= angle <= upper_angle_bound:
                            intersections.append(intersection)
    
    return np.asarray(intersections)

def drawPoints(points, image):
    for point in points:
        cv2.circle(image, tuple(map(int, point)), 15, (0, 0, 255), -1)
    
    return image

def find_best_quadrilateral(points):
    best_points = None
    best_area = 0

    num_points = len(points)

    # Loop to find the best quadrilateral
    for i in range(num_points - 3):
        for j in range(i + 1, num_points - 2):
            for k in range(j + 1, num_points - 1):
                for l in range(k + 1, num_points):
                    p1, p2, p3, p4 = points[i], points[j], points[k], points[l]

                    quad_points = np.array([p1, p2, p3, p4])

                    # Find the convex hull of the four points
                    hull = cv2.convexHull(quad_points)

                    # Calculate the area of the convex hull
                    area = cv2.contourArea(hull)

                    # Check if the area is greater than the current best area
                    if area > best_area:
                        best_area = area
                        best_points = [p1, p2, p3, p4]

    return np.asarray(best_points)

def correctPerspective(image, points):
    r= np.zeros((4,2), dtype="float32")
    s = np.sum(points, axis=1);r[0] = points[np.argmin(s)];r[2] = points[np.argmax(s)]
    d = np.diff(points, axis=1);r[1] = points[np.argmin(d)];r[3] = points[np.argmax(d)]
    (tl, tr, br, bl) =r
    wA = np.sqrt((tl[0]-tr[0])**2 + (tl[1]-tr[1])**2 )
    wB = np.sqrt((bl[0]-br[0])**2 + (bl[1]-br[1])**2 )
    maxW = max(int(wA), int(wB))
    hA = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2 )
    hB = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2 )
    maxH = max(int(hA), int(hB))
    ds= np.array([[0,0],[maxW-1, 0],[maxW-1, maxH-1],[0, maxH-1]], dtype="float32")
    transformMatrix = cv2.getPerspectiveTransform(r,ds)
    scan = cv2.warpPerspective(image, transformMatrix, (maxW, maxH))

    return scan

def process(image):
    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(gray,kernel,iterations = 2)
    blur =cv2.GaussianBlur(dilation,(5,5),0)
    blur= cv2.erode(blur,kernel,iterations =5)

    # # 3. Canny edge detection
    threshold, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    high = threshold
    low = int(high / 3)
    canny = cv2.Canny(blur, low, high, 1)
    # # 4. Hough line detection
    lines = houghline(canny)

    points = points_inter(lines)
    best = find_best_quadrilateral(points)

    scan = correctPerspective(image, best)

    return scan

if __name__ == "__main__":
    # read all the images in the folder
    folder_path = "image"  # Replace with the actual folder path
    image_files = os.listdir(folder_path)
    os.makedirs("processed", exist_ok=True)

    i = 1
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)

        # Process the image
        processed_image = process(image)

        # Save the processed image in /processed folder
        cv2.imwrite(f"processed/{image_file}", processed_image)
