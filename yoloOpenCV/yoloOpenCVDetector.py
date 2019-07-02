import json
import os
import time

import cv2

import numpy as np


class YoloOpenCVDetector():
    def __init__(self, config, weights, classes):
        scriptdir = os.path.abspath(os.path.dirname(__file__))
        self.config = os.path.join(scriptdir, config)
        self.weights = os.path.join(scriptdir, weights)
        self.classes = os.path.join(scriptdir, classes)
        with open(classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.net = cv2.dnn.readNet(self.weights, self.config)
        self.conf_threshold = 0.25  # 0.5
        self.nms_threshold = 0.5  # 0.4

    def get_output_layers(self, net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1]
                         for i in net.getUnconnectedOutLayers()]
        return output_layers

    def draw_prediction(self,
                        img,
                        class_id,
                        confidence,
                        x,
                        y,
                        x_plus_w,
                        y_plus_h):
        label = str(self.classes[class_id])
        color = self.COLORS[class_id]
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, label, (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def detectFromBytes(self, byteArray):
        image = cv2.imdecode(np.frombuffer(byteArray, np.uint8),
                             cv2.IMREAD_UNCHANGED)
        return(self.detectFromImage(image))

    def detectFromFile(self, imagefile):
        image = cv2.imread(imagefile)
        return(self.detectFromImage(image))

    def jsonFromBytes(self, byteArray):
        image = cv2.imdecode(np.frombuffer(byteArray, np.uint8),
                             cv2.IMREAD_UNCHANGED)
        return(self.jsonFromImage(image))

    def jsonFromFile(self, imagefile):
        image = cv2.imread(imagefile)
        return(self.jsonFromImage(image))

    def detectFromImage(self, image):
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        self.COLORS = np.random.uniform(0,
                                        255,
                                        size=(len(self.classes), 3))
        blob = cv2.dnn.blobFromImage(image,
                                     scale,
                                     (416, 416),
                                     (0, 0, 0),
                                     True,
                                     crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers(self.net))
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = self.conf_threshold
        nms_threshold = self.nms_threshold
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes,
                                   confidences,
                                   conf_threshold,
                                   nms_threshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            self.draw_prediction(image,
                                 class_ids[i],
                                 confidences[i],
                                 round(x),
                                 round(y),
                                 round(x + w),
                                 round(y + h))
        success, encoded_image = cv2.imencode('.jpg', image)
        return(encoded_image.tobytes())

    def jsonFromImage(self, image):
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        self.COLORS = np.random.uniform(0,
                                        255,
                                        size=(len(self.classes), 3))
        blob = cv2.dnn.blobFromImage(image,
                                     scale,
                                     (416, 416),
                                     (0, 0, 0),
                                     True,
                                     crop=False)
        self.net.setInput(blob)
        start_time = time.time()
        outs = self.net.forward(self.get_output_layers(self.net))
        total_time = time.time() - start_time
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = self.conf_threshold
        nms_threshold = self.nms_threshold
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes,
                                   confidences,
                                   conf_threshold,
                                   nms_threshold)
        predictions = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            prediction = {"label_id": int(class_ids[i]),
                          "label": str(self.classes[class_ids[i]]),
                          "confidence": confidences[i],
                          "x": round(x),
                          "y": round(y),
                          "w": round(w),
                          "h": round(h)}
            predictions.append(prediction)
        j = {"status": "ok",
             "unixtime": time.time(),
             "time": total_time,
             "objects": predictions}
        return(json.dumps(j))

# Local Variables:
# pyvenv-activate: "venv"
# End:
