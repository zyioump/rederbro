from rederbro.server.server import Server
import serial

import time

class SensorsServer(Server):
    def turnAutomode(self, state):
        self.logger.info("Auto mode turned {}".format(state))

    def setDistance(self, distance):
        self.distance = distance
        self.logger.info("Distance between photo set to {}".format(self.distance))

    def getCoord(self):
        self.logger.info("Get coordonate")
        if self.fakeMode:
            self.logger.info("Coordonate : 0, 0, 0 (fake mode)")
            return [0, 0, 0]

        else:
            trame = [""]
            while trame[0] != "$GPGGA":
                msg = ""
                while not "\r\n" in msg:
                    msg += self.serial.read().decode()

                trame = msg.split(",")
                
            self.logger.debug(msg)

    def __init__(self, config):
        Server.__init__(self, config, "sensors")

        self.command = {\
            "debug" : (self.setDebug, True),\
            "fake" : (self.setFakeMode, True),\
            "automode" : (self.turnAutomode, True),\
            "distance" : (self.setDistance, True),\
            "getCoord" : (self.getCoord, False)\
        }

        self.distance = 5

        try:
            self.serial = serial.Serial(port=self.config["gps"]["serial"], baudrate=115200, timeout=1)
        except:
            self.setFakeMode(True)
