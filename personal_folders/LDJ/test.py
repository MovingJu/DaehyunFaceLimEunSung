# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
from ultralytics import YOLO
import cv2


cap = cv2.VideoCapture(r"C:\Users\baram\OneDrive\사진\1.mp4")
# cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')
ex_dic = {}
ent_person = 0

def replace_values(dict_A, list_B, error=125):
    # A에 있는 키들의 집합
    keys_A = set(dict_A.keys())
    
    # A에 없는 키를 위한 새로운 키 값
    new_key = max(keys_A) + 1 if keys_A else 1
    
    # 변경된 딕셔너리를 담을 새로운 딕셔너리
    updated_dict_A = dict_A.copy()
    
    # B의 원소를 하나씩 검사
    for value_B in list_B:
        # B의 원소와 A의 각 값 비교
        for key, value_A in updated_dict_A.items():
            for i in range(len(value_A)):
                if abs(value_A[i] - value_B[i]) > error:
                    break
            else:  # 오차 범위 내에 있으면 해당 값을 대체하고 종료
                updated_dict_A[key] = value_B
                break
        else:  # 오차 범위 내에 없는 경우 새로운 키와 함께 추가
            updated_dict_A[new_key] = value_B
            new_key += 1
    
    return updated_dict_A


def update_values(dict_A_b, dict_A, constant, impedence = 200):
    for key, value_b in dict_A_b.items():
        # 이전 상태의 밸류 리스트와 현재 상태의 밸류 리스트
        value = dict_A[key]

        print((value_b[1] + value_b[3]) / 2, (value[1] + value[3]) / 2)

        # 이전 상태의 평균값 계산
        average_b = (value_b[1] + value_b[3]) / 2
        # 현재 상태의 평균값 계산
        average = (value[1] + value[3]) / 2
        
        # 이전 상태의 평균값이 20을 넘지 않다가 현재 상태에서 넘게 되면
        if average_b > impedence and average < impedence:
            # 상수에 1을 더함
            constant += 1
            print(f"평균값이 20을 넘는 키 {key} 발견! 상수 {constant}에 1을 더하고 리스트에 1을 추가합니다.")

    return constant

while cap.isOpened():
  success, image = cap.read()
  if not success:
    continue

  results = model(image, conf=0.3)

  for result in results:
    # print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())
    # print(result[0].boxes)
    # print(result.boxes.xyxy.tolist())

    ex_dic_b = ex_dic

    ex_dic = replace_values(ex_dic, result.boxes.xyxy.tolist())

    ent_person = update_values(ex_dic_b, ex_dic, ent_person)

    print('test:', ex_dic)
    result_plotted = results[0].plot()
    cv2.imshow('img', result_plotted)

  if cv2.waitKey(1) == ord('q'):
    print(ent_person)
    break
cap.release()