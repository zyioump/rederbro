from rederbro.server.server import Server
import time
import serial

try:
    from RPi.GPIO import GPIO as gpio
except:
    pass

class GoproServer(Server):
    def takePic(self, force=False):
        if not self.fakeMode:
            if force or self.goproOn:
                self.arduino.write("T")
                self.logger.debug("T send to arduino")

                answer = b""
                while answer not in (b'ERROR\r\n',b'TAKEN\r\n'):
                    time.sleep(0.5)
                    answer = self.arduino.readline()
                    self.logger.debug("{} receive from arduino".format(answer))

                if answer is b'TAKEN\r\n':
                    self.logger.info("Gopro took picture")
                    return True
                else:
                    goproStatus = self.arduino.readline().decode("ascii")
                    self.logger.debug("{} receive from arduino".format(goproStatus))
                    goproFailed = []

                    for i in range(0, len(goproStatus)):
                        if goproStatus[i] is "1":
                            goproFailed.append(i)

                    self.logger.error("Gopro {} failed to take picture".format(goproFailed))
                    return False
        else:
            self.logger.info("Gopro took picture (FakeMode)")
            return True

    def changeMode(self, force=False):
        if not self.fakeMode:
            if force or self.goproOn:
                self.arduino.write(b"M")
                self.logger.debug("M send to arduino")

                while self.arduino.readline() is not b"PHOTO_MODE\r\n":
                    self.logger.debug("{} receive from arduino".format(self.arduino.readline()))
                    time.sleep(0.5)

                self.logger.info("Gopro changed mode")
                return True

        else:
            self.logger.info("Gopro changed mode (FakeMode)")
            return True

    def turnGopro(self, state, force=False, full=True):
        if not self.fakeMode:
            if state:
                error = 0

                if not self.relayOn or force:
                    self.turnRelay(True)

                self.arduino.write(b"I")
                self.logger.debug("{} send to arduino".format(b"I"))

                while self.arduino.readline() is not b'ON\n':
                    time.sleep(0.5)
                    self.logger.debug("{} receive from arduino".format(self.arduino.readline()))


                if full:
                    error += 1 if not self.changeMode(force=True) else 0
                    error += 1 if not self.takePic(force=True) else 0

                if error is not 0:
                    self.logger.error("Gopro failed to turn on")
                    self.goproOn = False
                    return False
                else:
                    self.logger.info("Gopro turned on")
                    self.goproOn = True
                    return True
            else:
                error = 0

                if force:
                    error += 1 if not self.turnGopro(True, full=False) else 0

                if (force or self.goproOn) and error is 0:
                    self.arduino.write(b"O")
                    self.logger.debug("O send to arduino")
                    while self.arduino.readline() is not b"OFF\r\n":
                        self.logger.debug("{} receive from arduino".format(self.arduino.readline()))
                        time.sleep(0.5)

                    self.logger.info("Gopro turned off")
                    return True

                else:
                    self.logger.error("Gopro failed to turned off")
                    return False
        else:
            self.logger.info("Gopro turned {} (FakeMode)".format(state))
            self.goproOn = state
            return True

    def turnRelay(self, state, force=False):
        if not self.fakeMode:
            if state:
                if force or not self.relayOn:
                    gpio.output(self.config["relay_pin"], GPIO.HIGH)
                    self.logger.debug("Pin {} put HIGH".format(self.config["relay_pin"]))
            else:
                if not force:
                    self.turnGopro(False)

                if force or self.relayOn:
                    gpio.output(self.config["relay_pin"], GPIO.LOW)
                    self.logger.debug("Pin {} put LOW".format(self.config["relay_pin"]))
        else:
            self.logger.info("Relay turned {} (FakeMode)".format(state))
            self.relayOn = state

    def start(self):
        try:
            self.arduino = serial.Serial(self.config["arduino_serial"])
        except:
            self.logger.error("No arduino pluged --> fake mode on")
            self.setFakeMode(True)

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
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(self.config["relay_pin"], GPIO.OUT)
        except:
            self.logger.error("Not on a rpi --> fake mode on")
            self.setFakeMode(True)


        self.turnGopro(False, force=True)
        self.turnRelay(False, force=True)

        self.goproOn = False
        self.relayOn = True

        self.logger.info("Server started")
        while self.running:
            text = self.pipe.readText()

            for line in text:
                if self.command[line][1] is not None:
                    self.command[line][0](self.command[line][1])
                else:
                    self.command[line][0]()

            if len(text) is not 0:
                self.pipe.clean()

            time.sleep(self.delay)
