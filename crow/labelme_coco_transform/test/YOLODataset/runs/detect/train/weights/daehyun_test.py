# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2
cap = cv2.VideoCapture('http://172.20.10.3:81/stream')
#cap = cv2.VideoCapture(0)
model = YOLO('best.pt')

while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  results = model(image, conf=0.3) # 정확도
  print(results)
  for result in results:
    print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())

    result_plotted = results[0].plot()
    cv2.imshow('img', result_plotted)

  if cv2.waitKey(1) == ord('q'):
    break
cap.release()



