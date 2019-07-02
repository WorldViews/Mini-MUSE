from yoloOpenCVDetector import YoloOpenCVDetector
import cv2
import time

if __name__ == "__main__":
    print("Yolo Detect")
    # hardcode the files for yolo in the next line
    config = "./models/yolov3.cfg"
    weights = "./models/yolov3.weights"
    classes = "./models/yolov3.txt"
    yolo = YoloOpenCVDetector(config,weights,classes)
    # while true
    capture = cv2.VideoCapture(0)
    while (1):
        read_flag, frame = capture.read()
        # load an image from the webcam
        #i = cv2.imread("./data/dog.jpg")
        # call yolo on that image to get json
        output=yolo.jsonFromImage(frame)
        # print json to console
        print(output)
        # sleep 2 seconds 
        time.sleep(2)