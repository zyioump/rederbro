from rederbro.server.server import Server
from rederbro.utils.arduino import Arduino
import time

try:
    from RPi.GPIO import GPIO
except:
    pass

class GoproServer(Server):
    def turnGopro(self, state):
        """
        Switch gopro to state value
        """
        self.logger.info("Turn gopro {}".format(state))

    def turnRelay(self, state):
        """
        Switch relay to state value
        """
        self.logger.info("Turn relay {}".format(state))

        if self.fakeMode:
            #when fake mode is on
            self.relayOn = state
            self.logger.info("Turned relay {} (fake mode)".format(state))

        else:
            #when fake mode is off
            if state:
                GPIO.output(self.config["relay_pin"], GPIO.HIGH)
            else:
                GPIO.output(self.config["relay_pin"], GPIO.LOW)

            self.logger.info("Turned relay {}".format(state))

    def takePic(self):
        """
        Ask arduino to take picture
        """
        self.logger.info("Take picture")

    def __init__(self, config):
        #Use the __init__ of the server class
        Server.__init__(self, config, "gopro")

        #dict who link a command to a method
        # a : (b, c)
        # a --> command name
        # b --> method who can treat the command
        # c --> argument for the method
        self.command = {\
            "debugOn" : (self.setDebug, True),\
            "debugOff" : (self.setDebug, False),\
            "fakeOn" : (self.setFakeMode, True),\
            "fakeOff" : (self.setFakeMode, False),\
            "goproOn" : (self.turnGopro, True),\
            "goproOff" : (self.turnGopro, False),\
            "relayOn" : (self.turnRelay, True),\
            "relayOff" : (self.turnRelay, False),\
            "takepicOn" : (self.takePic, None)\
        }

        try:
            #init arduino
            self.arduino = Arduino(self.config, self.logger)
        except:
            self.logger.error("Can't connect to arduino")
            self.setFakeMode(True)

        try:
            #init GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(self.config["relay_pin"], GPIO.OUT)
        except:
            self.logger.error("Not on a rpi")
            if not self.fakeMode:
                self.setFakeMode(True)

        #switch off relay to be sure that gopro are off
        self.turnRelay(False)

        self.goproOn = False
        self.relayOn = False

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
