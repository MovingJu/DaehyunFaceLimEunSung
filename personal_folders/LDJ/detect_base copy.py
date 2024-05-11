from ultralytics import YOLO
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    results = model(image, conf=0.5)

    for result in results:
        # 객체마다 고유한 색상 생성
        color = tuple(np.random.randint(0, 255, 3))

        # 바운딩 박스 그리기
        x1, y1, x2, y2 = map(int, result.xyxy[0][:4])  # 수정
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    cv2.imshow('img', image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
