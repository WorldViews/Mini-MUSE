import time, threading

#from socketIO_client import SocketIO
from socketIO_client_nexus import SocketIO, LoggingNamespace

class MUSEClient:
    def __init__(self, url="http://localhost:8005"):
        self.url = url
        self.socket = None

    def on_connect(self, *args):
        print('on_connect', args)
        
    def onMessage(self, msg):
        print("On muse msg", msg)

    def sendMessage(self, msg):
        if not self.socket:
            print("Cannot send message without socket")
            return
        self.socket.emit('MUSE', msg)

    def runInThread(self):
        self.thread = threading.Thread(target=lambda s=self: s.threadFun())
        self.thread.setDaemon(1)
        self.thread.start()

    def threadFun(self):
        print("MUSEClient thread starting")
        self.run()
        print("MUSEClient thread finished")

    def run(self):
        print("trying to connect to", self.url)
        #with SocketIO('http://localhost:8005') as socketIO:
        with SocketIO(self.url) as socketIO:
            print("got socketIO", socketIO)
            self.socket = socketIO
            socketIO.on('connect', lambda args, s=self: s.on_connect(args))
            #
            print("Send status.join message")
            socketIO.emit('MUSE',
                          {'type': 'status.join', 'clientType': 'Python'})

            socketIO.on('MUSE', lambda msg, s=self: s.onMessage(msg))

            #socketIO.wait_for_callbacks(seconds=1)
            while 1:
                socketIO.wait(seconds=10)
                print("wait some more...")
    
    

if __name__ == '__main__':
    mc = MUSEClient()
    mc.runInThread()
    while 1:
        print("tick...")
        time.sleep(10)


    
