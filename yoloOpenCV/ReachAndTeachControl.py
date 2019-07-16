from ControlScript import ControlScript
import time

class ReachAndTeachScript(ControlScript):
    def __init__(self):
        ControlScript.__init__(self)
        self.currentObj = None

    def handleDetectedObjects(self, yoloResults):
        print("handleDetectedObjects")
        #print("yoloResults:", yoloResults)
        objs = yoloResults['objects']
        if len(objs) == 0:
            self.currentObj = None
            return
        if len(objs) > 1:
            print("ignoring case with more than 1 object")
            return
        obj = objs[0]
        label = obj['label']
        if label == self.currentObj:
            return
        print("**** new obj", label)
        self.currentObj = label





if __name__ == "__main__":
    rt = ReachAndTeachScript()
    rt.run()

