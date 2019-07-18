
import MUSEClient3
import time

def test():
    mc = MUSEClient3.MUSEClient("localhost:8002")
    mc.runInThread()
    n = 0
    while 1:
        n += 1
        msg = {"type": "AudioAppSource",
                "data": "some data", "n":n}
        mc.sendMessage(msg)
        time.sleep(1)

test()