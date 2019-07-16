from ControlScript import ControlScript
import time
import MUSEClient3

PAGES = {}
PAGES['heart'] = 'http://fxpal.com';
PAGES['purse'] = 'http://xerox.com';
PAGES['crane'] = 'http://palweb';


class ReachAndTeachScript(ControlScript):
    def __init__(self):
        ControlScript.__init__(self)
        self.currentObj = None
        self.mc = MUSEClient3.MUSEClient()
        self.mc.runInThread()

    def noticeNewObject(self, label):
        print("noticeNewObj", label)
        if label not in PAGES:
            print("No page for", label)
            return
        msg = {'type': 'setDisplayURL', 'label': label, 'url': PAGES[label]}
        print("msg:", msg)
        self.mc.sendMessage(msg)

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
        #print("**** new obj", label)
        self.noticeNewObject(label)
        self.currentObj = label





if __name__ == "__main__":
    rt = ReachAndTeachScript()
    rt.run()

