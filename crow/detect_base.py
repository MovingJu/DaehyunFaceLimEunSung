# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2


cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')

while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  results = model(image, conf=0.3)

  for result in results:
    print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())

    result_plotted = results[0].plot()
    cv2.imshow('img', result_plotted)

  if cv2.waitKey(1) == ord('q'):
    break
cap.release()



