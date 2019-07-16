from yoloOpenCVDetector import YoloOpenCVDetector
import cv2
import time, json

class ControlScript:
    def run(self):
        print("Yolo Detect")
        # hardcode the files for yolo in the next line
        config = "./models/yolo-obj.cfg"
        weights = "./models/yolo-obj_final.weights"
        classes = "./models/obj.names"
        yolo = YoloOpenCVDetector(config,weights,classes)
        # while true
        capture = cv2.VideoCapture(0)
        while (1):
            read_flag, frame = capture.read()
            cv2.imshow("source", frame)
            cv2.waitKey(1)
            # load an image from the webcam
            #i = cv2.imread("./data/dog.jpg")
            # call yolo on that image to get json
            jsonStr=yolo.jsonFromImage(frame)
            yoloResults = json.loads(jsonStr)
            self.handleDetectedObjects(yoloResults)
            # sleep 1 seconds 
            time.sleep(1)

    def handleDetectedObjects(self, yoloResults):
        #print("yoloResults:", yoloResults)
        objs = yoloResults['objects']
        for obj in objs:
            print(obj)



if __name__ == "__main__":
    cs = ControlScript()
    cs.run()

