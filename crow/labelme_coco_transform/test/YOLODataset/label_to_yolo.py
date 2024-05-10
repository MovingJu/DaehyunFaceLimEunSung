from ultralytics import YOLO

# 모델 초기화 및 가중치 로드
model = YOLO('yolov8n.yaml')  # YOLOv8 Nano 모델 구성 파일 (필요에 따라 수정)
model = model.load('yolov8n.pt')  # 사전 훈련된 가중치 로드 (선택적)

# 데이터셋 설정
data_yaml = 'C:/Users/USER/PycharmProjects/pythonProject/labelme_coco_transform/test/YOLODataset/dataset.yaml'  # YAML 파일 위치

# 모델 학습
results = model.train(data=data_yaml, epochs=100, imgsz=640)  # 학습 에폭 및 이미지 크기 조정 가능

# 학습된 모델 저장
model.save('C:/Users/USER/PycharmProjects/pythonProject/labelme_coco_transform/test/YOLODataset/daehyun.pt')