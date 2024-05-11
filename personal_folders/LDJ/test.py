# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2


cap = cv2.VideoCapture(r'C:\Users\baram\OneDrive\사진\KakaoTalk_20240511_201412220.mp4')
model = YOLO('yolov8n.pt')
ex_dic = {}

def replace_values(dict_A, list_B, error=10):
    # A에 있는 키들의 집합
    keys_A = set(dict_A.keys())
    
    # A에 없는 키를 위한 새로운 키 값
    new_key = max(keys_A) + 1 if keys_A else 1
    
    # B의 원소를 하나씩 검사
    for value_B in list_B:
        # B의 원소와 A의 각 값 비교
        for key, value_A in dict_A.items():
            for i in range(len(value_A)):
                if abs(value_A[i] - value_B[i]) > error:
                    break
            else:  # 오차 범위 내에 있으면 해당 값을 대체하고 종료
                dict_A[key] = value_B
                break
        else:  # 오차 범위 내에 없는 경우 새로운 키와 함께 추가
            dict_A[new_key] = value_B
            new_key += 1


while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  results = model(image, conf=0.1)

  for result in results:
    #print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())
    # print(result[0].boxes)
    replace_values(ex_dic, result.boxes.xyxy.tolist())

    print('test:', ex_dic)
    result_plotted = results[0].plot()
    cv2.imshow('img', result_plotted)

  if cv2.waitKey(1) == ord('q'):
    break
cap.release()