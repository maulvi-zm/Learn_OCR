from ultralytics import YOLO
import cv2

def textDetection(path):
    model = YOLO("best-4.pt")
    results = model.predict(path)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
          round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
          x1, y1, x2, y2, result.names[class_id], prob
        ])
    return output

def drawBoundingBoxes(image_path, output):
    # Load the image
    image = cv2.imread(image_path)

    # Draw bounding boxes on the image
    for box in output:
        x1, y1, x2, y2, label, prob = box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label_text = f"{label}: {prob}"
        cv2.putText(image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Detected Text", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
image_path = "images/4.jpg"
output_from_detection = textDetection(image_path)
drawBoundingBoxes(image_path, output_from_detection)
