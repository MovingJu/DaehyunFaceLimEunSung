# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2
import sys
import serial
import time

flag = True
# 장치관리자에서 확인한 COM 포트 입력
ser = serial.Serial('COM6', 9600)

# ESP32 CAM의 URL을 입력 : 'URL:81/stream' 형식
cap = cv2.VideoCapture('http://192.168.0.154:81/stream')

# 훈련된 모델 불러오기
model = YOLO('crow.pt')

# 인식된 객체의 바운딩 박스가 겹치는지 확인하는 함수
def is_overlap(box1, box2):
  """
  Check if two bounding boxes overlap.
  Each box is defined by (x1, y1, x2, y2).
  """
  x1, y1, x2, y2 = box1
  x3, y3, x4, y4 = box2

  # Check if boxes overlap
  if (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1):
    return False
  return True

def checkCrow(overlapslist, crow_i):
  for pair in overlapslist:
    if crow_i in pair:
      return True
  return False

while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  results = model(image, conf=0.9)

  bounding_boxes = results[0].boxes.xyxy.tolist() #바운딩박스 정보를 리스트로 변환
  overlaps = []
  for i in range(len(bounding_boxes)):
    for j in range(i + 1, len(bounding_boxes)):
      if is_overlap(bounding_boxes[i], bounding_boxes[j]): # overlap 검사
        overlaps.append((i, j))                            # 겹치면 ovelaps리스트에 저장
  clslist = results[0].boxes.cls.tolist() # 인식된 클래스의 리스트

  if 0.0 in clslist: # 클래스 리스트에 0 (까마귀) 이 있으면
    crowidx = clslist.index(0.0) # 클래스 리스트에서의 까마귀의 인덱스를 얻고
    if checkCrow(overlaps, crowidx):
      if ser.readable():
        if flag:
          val = '1'
          val = val.encode('utf-8')
          ser.write(val) # 시리얼통신으로 '1'을 전송
          flag = False
    else:
      flag = True
  else:
    flag = True

  if len(overlaps)==0:
    flag = True

  for result in results:
    print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())

    result_plotted = results[0].plot()
    cv2.imshow('img', result_plotted)

  if cv2.waitKey(1) == ord('q'):
    break
cap.release()











