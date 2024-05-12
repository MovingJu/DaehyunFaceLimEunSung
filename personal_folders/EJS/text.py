from ultralytics import YOLO
import cv2

humanCount = 0
idDict = {}
outList = []
sheepList = []
cap = cv2.VideoCapture(0)
model = YOLO('yolov8n.pt')
imageNum = 0


def is_errorAllow(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    errorA = 100
    if (abs(x1 - x3) <= errorA) and (abs(y1 - y3) <= errorA) and (abs(x2 - x4) <= errorA) and (abs(y2 - y4) <= errorA):
        return True
    return False


def is_inside(id):
    if id in idDict:
        x1, y1, x2, y2 = idDict[id]['Pos']
        if (x1 >= 400):
            return False
    return True


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    results = model(image, conf=0.3)
    bounding_boxes = results[0].boxes.xyxy.tolist()
    clslist = results[0].boxes.cls.tolist()
    clsNumList = []
    posList = []

    for i in range(len(clslist)):
        if clslist[i] == 0.0:  # Assuming class 0 represents humans
            clsNumList.append(i)

    for i in clsNumList:
        posList.append(bounding_boxes[i])

    for i in range(len(clsNumList)):
        lidiMatch = False
        for j in idDict.keys():
            if not lidiMatch:
                lidiMatch = is_errorAllow(posList[i], idDict[j]['Pos'])
        if not lidiMatch:
            idDict[humanCount] = {'Pos': posList[i]}
            humanCount += 1

    for i in range(len(clsNumList)):
        for j in idDict.keys():
            if is_errorAllow(posList[i], idDict[j]['Pos']):
                idDict[j]['Pos'] = posList[i]

    print(idDict)
    print(clsNumList)
    print(posList)
    print(sheepList)
    print(outList)
    print(clslist)
    print(imageNum)

    for i in range(len(idDict)):
        if is_inside(i):
            if i in outList and i not in sheepList:
                sheepList.append(i)
                print("ALERT!")
                result_plotter = results[0].plot()
                cv2.imwrite('./crow/results/' + str(imageNum) + '.png', result_plotter)
                imageNum += 1
        else:
            if i not in outList:
                outList.append(i)

    for result in results:
        print(result.boxes.xyxy.tolist(), result.boxes.conf.tolist())

        result_plotted = results[0].plot()
        cv2.imshow('img', result_plotted)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()