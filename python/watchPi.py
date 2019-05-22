
import urllib2, json, traceback, time

PI_URL = "http://192.168.16.39:5000/detect.json"
NUM_CALLS = 0

def sawPerson(obj):
    print "I saw a person"
    
def sawTV(obj):
    print "I saw a TV"

def sawBook(obj):
    print "I saw a book", obj
    
TARGET_OBJS = {
    'tvmonitor': sawTV,
    'person': sawPerson,
    'book': sawBook
    }

def getTrackedObjs(url):
    global NUM_CALLS
    NUM_CALLS += 1
    url = "%s?t=%s" % (url, time.time())
    print "Getting", url
    uos = urllib2.urlopen(url)
    str = uos.read()
    detectorResult = json.loads(str)
    #print detectorResult
    objs = detectorResult['objects']
    print json.dumps(objs, indent=4)
    for obj in objs:
        label = obj['label']
        #print label, obj
        if label in TARGET_OBJS:
            print "**** BINGO ****", label
            TARGET_OBJS[label](obj)
            
def watchPi():
    while True:
        try:
            getTrackedObjs(PI_URL)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    watchPi()


