from rederbro.server.server import Server

import time

class SensorsServer(Server):
    def turnAutomode(self, state):
        self.logger.info("Auto mode turned {}".format(state))

    def __init__(self):
        Server.__init__(self, config, "sensors")

        self.command = {\
        "debugon" : (self.setDebug, True),\
        "debugoff" : (self.setDebug, False),\
        "fakeon" : (self.setFakeMode, True),\
        "fakeoff" : (self.setFakeMode, False),\
        "automodeon" : (self.turnAutomode, True),\
        "automodeoff" : (self.turnAutomode, False),\
        }

    def start(self):
        self.logger.warning("Server started")
        while self.running:
            #check data send by main server
            text = self.pipe.readText()

            for line in text:
                #if method who treat the command take an argument
                if self.command[line][1] is not None:
                    #treat command
                    self.command[line][0](self.command[line][1])
                else:
                    #treat command
                    self.command[line][0]()

            #if command receive by main server is not empty clear the pipe
            if len(text) is not 0:
                self.pipe.clean()

            time.sleep(self.delay)
